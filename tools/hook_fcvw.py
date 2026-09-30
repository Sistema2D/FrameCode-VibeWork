#!/usr/bin/env python3
"""Optional agent-harness hooks that turn three FCVW rules into checks.

One provider-neutral command for Claude Code and Codex, whose hook protocols
agree on what is used here: JSON on stdin; `hookSpecificOutput.additionalContext`
on SessionStart; `hookSpecificOutput.permissionDecision: "deny"` with a reason
on PreToolUse; exit code 2 with a message on stderr to keep a Stop from ending.

    session-start  add a short FCVW status (active plans, next plan, how to route)
    pre-edit       deny edits to versioned project files while no plan is in progress
                   (a plan completed in the uncommitted work still counts, for closeout edits)
    stop           validate the uncommitted work; ask the agent to fix the errors it caused

The contract is the switch: a hook acts only when an `fcvw/automation@1`
contract with `status: active` names this script in `implementation` and the
event in `hook_events` (see FCVW/AUTOMATION.md). Without one, or with the
contract `paused` or `retired`, the hook does nothing. `FCVW_HOOKS=off` is the
emergency switch for one session. The
hooks read the repository and run the validator; they never write files, call
the network or change git. Shell commands are not inspected, so an edit made
through a shell escapes the pre-edit check.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from frontmatter_fcvw import parse_frontmatter, scalar, string_list

EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit", "apply_patch"}
PATCH_PATH = re.compile(r"^\*\*\* (?:Update|Add|Delete) File: (.+?)\s*$|^\*\*\* Move to: (.+?)\s*$", re.M)
# Paths an agent may create or change while opening a plan, plus disposable state.
PLAN_FREE_PREFIXES = ("FCVW/Plans/", ".fcvw-cache/", ".git/")
VALIDATE_TIMEOUT = 120
HOOK_EVENTS = ("session-start", "pre-edit", "stop")
HARNESSES = ("claude-code", "codex")
SCRIPT_NAME = "hook_fcvw.py"
HOOK_COMMAND = re.compile(r"hook_fcvw\.py[\"']?\s+(session-start|pre-edit|stop)\b")
HARNESS_CONFIGS = {
    "claude-code": (".claude/settings.json", ".claude/settings.local.json"),
    "codex": (".codex/hooks.json", ".codex/config.toml"),
}
MAX_REPORTED = 8


def governed_root(start: Path) -> Path | None:
    """Nearest directory at or above start that holds AGENTS.md and FCVW/."""

    for candidate in (start, *start.parents):
        if (candidate / "AGENTS.md").is_file() and (candidate / "FCVW").is_dir():
            return candidate
    return None


def hook_contracts(root: Path) -> list[dict]:
    """Every fcvw/automation@1 contract that binds this script, with its declared events and harnesses."""

    contracts = []
    for path in sorted((root / "FCVW").rglob("*.md")):
        if path.name.startswith("TEMPLATE_") or ".fcvw-cache" in path.parts:
            continue
        try:
            with path.open(encoding="utf-8-sig") as handle:
                head = handle.read(8192)
        except OSError:
            continue
        if not head.startswith("---") or "fcvw/automation@1" not in head:
            continue
        metadata = parse_frontmatter(path.read_text(encoding="utf-8-sig")).data
        if scalar(metadata, "schema") != "fcvw/automation@1" or scalar(metadata, "kind") != "hook":
            continue
        implementation = scalar(metadata, "implementation")
        if Path(implementation).name != SCRIPT_NAME:
            continue
        contracts.append({
            "path": path.relative_to(root).as_posix(),
            "id": scalar(metadata, "id"),
            "status": scalar(metadata, "status"),
            "implementation": implementation,
            "events": string_list(metadata, "hook_events"),
            "harnesses": string_list(metadata, "harnesses"),
        })
    return contracts


def active_events(root: Path) -> set[str]:
    return {event for contract in hook_contracts(root) if contract["status"] == "active" for event in contract["events"]}


def configured_hooks(root: Path) -> dict[str, set[str]]:
    """Events of this script that each harness configuration file runs."""

    configured: dict[str, set[str]] = {}
    for harness, files in HARNESS_CONFIGS.items():
        for name in files:
            path = root / name
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
                if name.endswith(".toml"):
                    try:
                        import tomllib
                    except ImportError:  # Python 3.10: TOML hooks are not inspected
                        continue
                    data = tomllib.loads(text)
                else:
                    data = json.loads(text)
            except (OSError, ValueError):
                continue
            commands: list[str] = []

            def collect(node) -> None:
                if isinstance(node, dict):
                    if isinstance(node.get("command"), str):
                        commands.append(node["command"])
                    for value in node.values():
                        collect(value)
                elif isinstance(node, list):
                    for value in node:
                        collect(value)

            collect(data.get("hooks", {}))
            for command in commands:
                configured.setdefault(harness, set()).update(HOOK_COMMAND.findall(command))
    return configured


def plans(root: Path, state: str) -> list[str]:
    folder = root / "FCVW" / "Plans" / state
    return sorted(path.stem for path in folder.glob("*.md")) if folder.is_dir() else []


def edited_paths(payload: dict) -> list[str]:
    """File paths named by a Claude Code edit tool or a Codex apply_patch call."""

    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return []
    if payload.get("tool_name") == "apply_patch":
        patch = tool_input.get("command") or tool_input.get("input") or ""
        return [first or second for first, second in PATCH_PATH.findall(patch if isinstance(patch, str) else "")]
    value = tool_input.get("file_path") or tool_input.get("notebook_path")
    return [value] if isinstance(value, str) and value else []


def relative_to_root(root: Path, cwd: Path, value: str) -> str | None:
    """Repository-relative POSIX path, or None when the path is outside the root."""

    path = Path(value)
    resolved = (path if path.is_absolute() else cwd / path).resolve()
    try:
        return resolved.relative_to(root).as_posix()
    except ValueError:
        return None


def closing_plans(root: Path) -> list[str]:
    """Plans completed or discontinued in the uncommitted work: their closeout edits belong to the same batch."""

    try:
        run = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all", "--", "FCVW/Plans"],
                             cwd=root, capture_output=True, text=True, timeout=10, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return []
    found = []
    for line in run.stdout.splitlines():
        path = line[3:].split(" -> ")[-1].strip().strip('"')
        if re.match(r"FCVW/Plans/(completed|discontinued)/[^/]+\.md$", path):
            found.append(Path(path).stem)
    return found


def git_ignored(root: Path, relative: str) -> bool:
    try:
        run = subprocess.run(["git", "check-ignore", "-q", "--", relative], cwd=root,
                             capture_output=True, timeout=10, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return run.returncode == 0


def session_start(root: Path, payload: dict) -> tuple[int, str, str]:
    active = plans(root, "in_progress")
    pending = plans(root, "pending")
    lines = [
        "FCVW governs this repository. Read AGENTS.md first.",
        "Mandatory reading: call the fcvw_routes MCP tool (or tools/retrieve_context.py) with the session, "
        "events and changed files, then read only the returned ranges.",
        "Versioned changes need a plan in FCVW/Plans/in_progress/ before any edit; the pre-edit hook enforces it.",
        f"Plans in progress: {', '.join(active) if active else 'none'}.",
    ]
    if pending:
        lines.append(f"Pending plans: {', '.join(pending[:5])}{' ...' if len(pending) > 5 else ''}.")
    output = {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "\n".join(lines)}}
    return 0, json.dumps(output), ""


def pre_edit(root: Path, payload: dict) -> tuple[int, str, str]:
    if payload.get("tool_name") not in EDIT_TOOLS:
        return 0, "", ""
    cwd = Path(payload.get("cwd") or root)
    governed = []
    for value in edited_paths(payload):
        relative = relative_to_root(root, cwd, value)
        if relative is None or relative.startswith(PLAN_FREE_PREFIXES) or git_ignored(root, relative):
            continue
        governed.append(relative)
    if not governed or plans(root, "in_progress") or closing_plans(root):
        return 0, "", ""
    reason = (
        f"FCVW: no plan in FCVW/Plans/in_progress/, so editing {', '.join(governed[:3])} is blocked. "
        "Create the plan from FCVW/governance/TEMPLATE_PLAN.md (or TEMPLATE_PLAN_COMPACT.md for P4/P5-R1), "
        "move it to FCVW/Plans/in_progress/, then retry. A trivial prose fix (AGENTS.md) needs a human bypass: "
        "FCVW_HOOKS=off."
    )
    output = {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                     "permissionDecisionReason": reason}}
    return 0, json.dumps(output), ""


def stop(root: Path, payload: dict, profile: str) -> tuple[int, str, str]:
    if payload.get("stop_hook_active"):
        return 0, "", ""  # already asked once in this stop cycle; never loop
    try:
        status = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=root, capture_output=True,
                                text=True, timeout=20, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return 0, "", ""
    if status.returncode != 0 or not status.stdout.strip():
        return 0, "", ""
    validator = Path(__file__).with_name("validate_fcvw.py")
    try:
        run = subprocess.run([sys.executable, "-B", str(validator), "--root", str(root), "--profile", profile,
                              "--since", "HEAD", "--format", "json", "--fail-on", "never"],
                             capture_output=True, text=True, encoding="utf-8", errors="replace",
                             timeout=VALIDATE_TIMEOUT, check=False)
        report = json.loads(run.stdout)
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError):
        return 0, "", ""  # a broken validator run never traps the agent
    # Only what the uncommitted work caused: findings on a changed file, or naming one
    # (a renamed heading breaks links elsewhere). Older debt never traps the agent.
    changed = {line[3:].split(" -> ")[-1].strip().strip('"') for line in status.stdout.splitlines()}
    names = {Path(path).name for path in changed}
    errors = [
        item for item in report.get("findings", [])
        if item.get("severity") == "error"
        and (item.get("path") in changed or any(name and name in item.get("message", "") for name in names))
    ]
    if not errors:
        return 0, "", ""
    listed = "\n".join(f"- [{item['rule']}] {item['path']}: {item['message']}" for item in errors[:MAX_REPORTED])
    more = f"\n- ... {len(errors) - MAX_REPORTED} more" if len(errors) > MAX_REPORTED else ""
    message = (f"FCVW validation ({profile}) found {len(errors)} error(s) in the changes since HEAD. "
               f"Fix them before finishing, or explain why they stay:\n{listed}{more}")
    return 2, "", message


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("event", choices=("session-start", "pre-edit", "stop"))
    parser.add_argument("--root", help="repository root; default: nearest governed root above the hook cwd")
    parser.add_argument("--profile", default="instantiated",
                        choices=("clean-template", "instantiated", "incremental", "strict"))
    args = parser.parse_args(argv)
    if os.environ.get("FCVW_HOOKS", "").lower() in {"off", "0", "false"}:
        return 0
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}
    start = Path(args.root or payload.get("cwd") or os.getcwd()).resolve()
    root = governed_root(start)
    if root is None:
        return 0  # not an FCVW repository: stay silent
    if args.event not in active_events(root):
        return 0  # no active contract declares this hook: it does nothing
    if args.event == "session-start":
        code, out, err = session_start(root, payload)
    elif args.event == "pre-edit":
        code, out, err = pre_edit(root, payload)
    else:
        code, out, err = stop(root, payload, args.profile)
    if out:
        print(out)
    if err:
        print(err, file=sys.stderr)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
