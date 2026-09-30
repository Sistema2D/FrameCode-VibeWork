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

from hook_fcvw import edited_paths, main
from release_layout_fcvw import governed_root

ROOT = governed_root(Path(__file__))
SCRIPT = str(Path(__file__).with_name("hook_fcvw.py"))


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=root,
                   check=True, capture_output=True)


def run_hook(event: str, payload: dict, *extra: str, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-B", SCRIPT, event, *extra], input=json.dumps(payload),
                          capture_output=True, text=True, timeout=180, env={**os.environ, **(env or {})})


class Repo(unittest.TestCase):
    def repo(self, *, full: bool = False) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name).resolve() / "repo"
        if full:
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", ".fcvw-cache", "__pycache__"))
        else:
            (root / "FCVW" / "Plans").mkdir(parents=True)
            (root / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
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
