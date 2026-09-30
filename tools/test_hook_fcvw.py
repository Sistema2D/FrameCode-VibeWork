#!/usr/bin/env python3
"""Hook behaviour with Claude Code and Codex payloads, in throwaway repositories."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from hook_fcvw import configured_hooks, edited_paths, hook_contracts, main
from validate_fcvw import Finding, validate_automation, validate_automation_binding
from release_layout_fcvw import governed_root

ROOT = governed_root(Path(__file__))
SCRIPT = str(Path(__file__).with_name("hook_fcvw.py"))


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=root,
                   check=True, capture_output=True)


def contract(status: str = "active", events=("session-start", "pre-edit", "stop"),
             harnesses=("claude-code", "codex"), implementation: str = "FCVW/tools/hook_fcvw.py") -> str:
    listed = lambda items: "".join(f'  - "{item}"\n' for item in items)
    return (
        '---\nschema: "fcvw/automation@1"\nid: "AUT-2026-01-01-hooks"\nkind: "hook"\n'
        f'status: "{status}"\nowner: "t"\nscenario: "2"\nexecution_mode: "scenario_2"\nauthorized_by: "t"\n'
        f'implementation: "{implementation}"\nhook_events:\n{listed(events)}harnesses:\n{listed(harnesses)}'
        'trigger: "t"\npreconditions: "t"\nactions: "t"\nevidence: "t"\nfailure_policy: "t"\nrollback: "t"\n'
        '---\n\n# Hooks\n'
    )


def write_contract(root: Path, text: str, *, stub: bool = True) -> None:
    (root / "FCVW" / "automation").mkdir(parents=True, exist_ok=True)
    (root / "FCVW" / "automation" / "AUT-hooks.md").write_text(text, encoding="utf-8")
    if stub:
        (root / "FCVW" / "tools").mkdir(parents=True, exist_ok=True)
        (root / "FCVW" / "tools" / "hook_fcvw.py").write_text("# stub\n", encoding="utf-8")


def run_hook(event: str, payload: dict, *extra: str, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-B", SCRIPT, event, *extra], input=json.dumps(payload),
                          capture_output=True, text=True, timeout=180, env={**os.environ, **(env or {})})


class Repo(unittest.TestCase):
    def repo(self, *, full: bool = False, status: str | None = "active", **kwargs) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name).resolve() / "repo"
        if full:
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", ".fcvw-cache", "__pycache__"))
            # A coherent opt-in: an active stop contract and the configuration that runs it.
            tool = "tools/hook_fcvw.py" if (root / "tools" / "hook_fcvw.py").is_file() else "FCVW/tools/hook_fcvw.py"
            write_contract(root, contract(events=("stop",), harnesses=("claude-code",), implementation=tool), stub=False)
            (root / "FCVW" / "README.md").write_text((root / "FCVW" / "README.md").read_text(encoding="utf-8")
                                                     + "\n[Hooks contract](automation/AUT-hooks.md)\n", encoding="utf-8")
            (root / ".claude").mkdir(exist_ok=True)
            (root / ".claude" / "settings.json").write_text(json.dumps({"hooks": {"Stop": [{"hooks": [
                {"type": "command", "command": f"python3 {tool} stop"}]}]}}), encoding="utf-8")
            status = None
        else:
            (root / "FCVW" / "Plans").mkdir(parents=True)
            (root / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
        if status:
            write_contract(root, contract(status, **kwargs))
        (root / ".gitignore").write_text("build/\n", encoding="utf-8")
        git(root, "init", "-q")
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "base")
        return root


class PathTests(unittest.TestCase):
    def test_edit_payloads_of_both_harnesses(self) -> None:
        self.assertEqual(["/r/a.py"], edited_paths({"tool_name": "Edit", "tool_input": {"file_path": "/r/a.py"}}))
        self.assertEqual(["n.ipynb"], edited_paths({"tool_name": "NotebookEdit", "tool_input": {"notebook_path": "n.ipynb"}}))
        patch = ("*** Begin Patch\n*** Update File: src/a.py\n@@\n-x\n+y\n*** Add File: docs/b.md\n+hi\n"
                 "*** Delete File: old.txt\n*** Update File: c.py\n*** Move to: d.py\n*** End Patch\n")
        self.assertEqual(["src/a.py", "docs/b.md", "old.txt", "c.py", "d.py"],
                         edited_paths({"tool_name": "apply_patch", "tool_input": {"command": patch}}))
        self.assertEqual([], edited_paths({"tool_name": "Edit", "tool_input": "bad"}))


class PreEditTests(Repo):
    def decision(self, root: Path, payload: dict) -> str | None:
        run = run_hook("pre-edit", {"cwd": str(root), "hook_event_name": "PreToolUse", **payload})
        self.assertEqual(0, run.returncode, run.stderr)
        return json.loads(run.stdout)["hookSpecificOutput"]["permissionDecision"] if run.stdout.strip() else None

    def test_blocks_versioned_edits_without_a_plan_in_progress(self) -> None:
        root = self.repo()
        self.assertEqual("deny", self.decision(root, {"tool_name": "Edit", "tool_input": {"file_path": str(root / "src/app.py")}}))
        patch = "*** Begin Patch\n*** Update File: src/app.py\n*** End Patch\n"
        self.assertEqual("deny", self.decision(root, {"tool_name": "apply_patch", "tool_input": {"command": patch}}))

    def test_allows_plan_files_ignored_paths_outside_paths_and_other_tools(self) -> None:
        root = self.repo()
        allowed = [
            {"tool_name": "Write", "tool_input": {"file_path": str(root / "FCVW/Plans/pending/P3-R2-x.md")}},
            {"tool_name": "Write", "tool_input": {"file_path": str(root / "build/out.txt")}},
            {"tool_name": "Write", "tool_input": {"file_path": "/tmp/elsewhere.txt"}},
            {"tool_name": "Bash", "tool_input": {"command": "echo hi > src/app.py"}},
            {"tool_name": "Read", "tool_input": {"file_path": str(root / "src/app.py")}},
        ]
        for payload in allowed:
            self.assertIsNone(self.decision(root, payload), payload)

    def test_plan_in_progress_unlocks_edits(self) -> None:
        root = self.repo()
        (root / "FCVW/Plans/in_progress").mkdir()
        (root / "FCVW/Plans/in_progress/P3-R2-2026-01-01-x.md").write_text("# Plan\n", encoding="utf-8")
        self.assertIsNone(self.decision(root, {"tool_name": "Edit", "tool_input": {"file_path": str(root / "src/app.py")}}))

    def test_uncommitted_completed_plan_allows_closeout_edits(self) -> None:
        root = self.repo()
        payload = {"tool_name": "Edit", "tool_input": {"file_path": str(root / "FCVW/APP_RULES.md")}}
        (root / "FCVW/Plans/completed").mkdir()
        (root / "FCVW/Plans/completed/P3-R2-2026-01-01-x.md").write_text("# Plan\n", encoding="utf-8")
        self.assertIsNone(self.decision(root, payload))
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "close")
        self.assertEqual("deny", self.decision(root, payload))

    def test_disable_switch_and_non_fcvw_directories_stay_silent(self) -> None:
        root = self.repo()
        payload = {"cwd": str(root), "tool_name": "Edit", "tool_input": {"file_path": str(root / "a.py")}}
        off = run_hook("pre-edit", payload, env={"FCVW_HOOKS": "off"})
        self.assertEqual(("", 0), (off.stdout, off.returncode))
        with tempfile.TemporaryDirectory() as other:
            plain = run_hook("pre-edit", {**payload, "cwd": other, "tool_input": {"file_path": f"{other}/a.py"}})
            self.assertEqual(("", 0), (plain.stdout, plain.returncode))


class SessionStartTests(Repo):
    def test_context_names_active_plans(self) -> None:
        root = self.repo()
        (root / "FCVW/Plans/in_progress").mkdir()
        (root / "FCVW/Plans/in_progress/P3-R2-2026-01-01-x.md").write_text("# Plan\n", encoding="utf-8")
        run = run_hook("session-start", {"cwd": str(root), "hook_event_name": "SessionStart", "source": "startup"})
        output = json.loads(run.stdout)["hookSpecificOutput"]
        self.assertEqual("SessionStart", output["hookEventName"])
        self.assertIn("P3-R2-2026-01-01-x", output["additionalContext"])
        self.assertLess(len(output["additionalContext"].encode()), 1500)


class StopTests(Repo):
    def test_clean_tree_and_repeated_stop_pass(self) -> None:
        root = self.repo()
        self.assertEqual(0, run_hook("stop", {"cwd": str(root), "stop_hook_active": False}).returncode)
        (root / "new.md").write_text("[x](missing.md)\n", encoding="utf-8")
        self.assertEqual(0, run_hook("stop", {"cwd": str(root), "stop_hook_active": True}).returncode)

    def test_errors_in_changes_keep_the_agent_working(self) -> None:
        root = self.repo(full=True)
        base = {"cwd": str(root), "stop_hook_active": False}
        with open(root / "FCVW" / "README.md", "a", encoding="utf-8") as handle:
            handle.write("\nA plain sentence.\n")
        self.assertEqual(0, run_hook("stop", base, "--profile", "clean-template").returncode)
        with open(root / "FCVW" / "README.md", "a", encoding="utf-8") as handle:
            handle.write("\n[broken](does-not-exist.md)\n")
        run = run_hook("stop", base, "--profile", "clean-template")
        self.assertEqual(2, run.returncode)
        self.assertIn("does-not-exist.md", run.stderr)


class ContractSwitchTests(Repo):
    EDIT = {"tool_name": "Edit", "tool_input": {"file_path": "src/app.py"}}

    def outputs(self, root: Path) -> tuple[str, str]:
        payload = {**self.EDIT, "cwd": str(root)}
        return (run_hook("pre-edit", payload).stdout.strip(),
                run_hook("session-start", {"cwd": str(root)}).stdout.strip())

    def test_hooks_act_only_while_an_active_contract_declares_them(self) -> None:
        self.assertTrue(all(self.outputs(self.repo())))
        self.assertEqual(("", ""), self.outputs(self.repo(status=None)))
        self.assertEqual(("", ""), self.outputs(self.repo(status="paused")))
        self.assertEqual(("", ""), self.outputs(self.repo(status="retired")))
        only_stop = self.outputs(self.repo(events=("stop",)))
        self.assertEqual(("", ""), only_stop)

    def test_contract_must_name_this_script(self) -> None:
        root = self.repo(implementation="scripts/other.py")
        self.assertEqual([], hook_contracts(root))
        self.assertEqual(("", ""), self.outputs(root))


class BindingTests(unittest.TestCase):
    def root(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name).resolve()
        (root / "FCVW").mkdir()
        (root / ".claude").mkdir()
        (root / ".codex").mkdir()
        return root

    @staticmethod
    def configure(root: Path, harness: str, events: tuple[str, ...]) -> None:
        names = {"session-start": "SessionStart", "pre-edit": "PreToolUse", "stop": "Stop"}
        hooks = {names[e]: [{"hooks": [{"type": "command", "command": f"python3 FCVW/tools/hook_fcvw.py {e}"}]}] for e in events}
        target = root / (".claude/settings.json" if harness == "claude-code" else ".codex/hooks.json")
        target.write_text(json.dumps({"hooks": hooks}), encoding="utf-8")

    def findings(self, root: Path) -> list[Finding]:
        findings: list[Finding] = []
        validate_automation(root, findings)
        validate_automation_binding(root, findings)
        return findings

    def test_matching_contract_and_configuration(self) -> None:
        root = self.root()
        write_contract(root, contract())
        self.configure(root, "claude-code", ("session-start", "pre-edit", "stop"))
        self.configure(root, "codex", ("session-start", "pre-edit", "stop"))
        self.assertEqual({"claude-code": {"session-start", "pre-edit", "stop"},
                          "codex": {"session-start", "pre-edit", "stop"}}, configured_hooks(root))
        self.assertEqual([], self.findings(root))

    def test_configured_hook_without_active_contract(self) -> None:
        root = self.root()
        self.configure(root, "claude-code", ("pre-edit",))
        errors = [f for f in self.findings(root) if f.rule == "automation-binding"]
        self.assertEqual(["error"], [f.severity for f in errors])
        write_contract(root, contract("paused", events=("pre-edit",), harnesses=("claude-code",)))
        warnings = [f for f in self.findings(root) if f.rule == "automation-binding"]
        self.assertEqual(["warning"], [f.severity for f in warnings])

    def test_active_contract_without_configuration(self) -> None:
        root = self.root()
        write_contract(root, contract(harnesses=("codex",)))
        self.configure(root, "codex", ("stop",))
        messages = [f.message for f in self.findings(root) if f.rule == "automation-binding"]
        self.assertTrue(any("pre-edit, session-start" in m and "codex" in m for m in messages), messages)

    def test_contract_field_checks(self) -> None:
        root = self.root()
        write_contract(root, contract(events=("pre-edit", "bogus"), harnesses=("vim",), implementation="FCVW/tools/missing.py"))
        messages = [f.message for f in self.findings(root) if f.rule == "automation-contract"]
        self.assertTrue(any("unknown hook_events: bogus" in m for m in messages))
        self.assertTrue(any("unknown harnesses: vim" in m for m in messages))
        self.assertTrue(any("implementation is missing" in m for m in messages))


class InProcessTests(unittest.TestCase):
    def test_main_accepts_empty_and_malformed_stdin(self) -> None:
        import io
        from contextlib import redirect_stdout
        for text in ("", "not json", "[1]"):
            stdin, sys.stdin = sys.stdin, io.StringIO(text)
            try:
                with redirect_stdout(io.StringIO()):
                    self.assertEqual(0, main(["pre-edit", "--root", str(ROOT)]))
            finally:
                sys.stdin = stdin


if __name__ == "__main__":
    unittest.main()
