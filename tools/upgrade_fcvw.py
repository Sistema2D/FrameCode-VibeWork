#!/usr/bin/env python3
"""Plan and apply a selective FCVW framework upgrade.

`OWNERSHIP.md` defines a nine-step upgrade algorithm and then leaves every step
to be executed by hand. That makes the riskiest operation in the lifecycle the
least assisted one: nothing inventories roles before copying, and nothing can
tell an untouched framework policy from one the project edited locally, which is
exactly the case where `upgrade_strategy: replace` destroys work.

This tool reads the role manifest of both the installed tree and the target
release, compares content digests, and reports what each path would do. It is a
dry run by default and refuses to apply over a local modification unless that is
explicitly accepted.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

from role_manifest_fcvw import MANIFEST_PATH, build_manifest, digest

# Roles the framework owns and may replace on a compatible upgrade.
REPLACEABLE_ROLES = {
    "framework_policy",
    "framework_lock",
    "framework_skill",
    "framework_tool",
    "framework_asset",
    "framework_scaffold",
    "framework_history",
    "template",
    "example",
}
# Roles that carry project truth and are never overwritten.
PRESERVED_ROLES = {"project_profile", "record"}
REGENERATED_ROLES = {"generated"}


@dataclass(frozen=True)
class Action:
    verdict: str
    path: str
    role: str
    detail: str


def load_manifest(root: Path) -> dict[str, dict[str, str]]:
    """Prefer a stored manifest; fall back to rebuilding it from the tree."""

    stored = root / MANIFEST_PATH
    if stored.is_file():
        data = json.loads(stored.read_text(encoding="utf-8"))
    else:
        data = build_manifest(root)
    return {entry["path"]: entry for entry in data["files"]}


def plan_upgrade(installed_root: Path, release_root: Path) -> list[Action]:
    installed = load_manifest(installed_root)
    # The release is the authority on roles for the version being installed.
    release = {entry["path"]: entry for entry in build_manifest(release_root)["files"]}

    actions: list[Action] = []
    for path in sorted(set(installed) | set(release)):
        target = release.get(path)
        current = installed.get(path)
        role = (target or current or {}).get("artifact_role", "unclassified")

        if target is None:
            if role in PRESERVED_ROLES:
                actions.append(Action("preserve", path, role, "project artifact absent upstream"))
            else:
                actions.append(Action("removed", path, role, "dropped by the target release"))
            continue

        if current is None:
            actions.append(Action("new", path, role, "added by the target release"))
            continue

        try:
            live = contained(installed_root, path)
        except ValueError:
            actions.append(Action("review", path, role, "manifest path escapes the tree"))
            continue
        live_digest = digest(live) if live.is_file() else None

        if role in PRESERVED_ROLES:
            actions.append(Action("preserve", path, role, "project-owned"))
            continue
        if role in REGENERATED_ROLES:
            actions.append(Action("regenerate", path, role, "rebuild after the upgrade"))
            continue
        if role not in REPLACEABLE_ROLES:
            actions.append(Action("review", path, role, f"unknown role: {role}"))
            continue

        if live_digest is None:
            actions.append(Action("new", path, role, "missing locally"))
        elif live_digest != current.get("digest"):
            actions.append(
                Action("conflict", path, role, "framework file was modified locally since installation")
            )
        elif live_digest == target.get("digest"):
            actions.append(Action("unchanged", path, role, "identical to the target release"))
        else:
            actions.append(Action("replace", path, role, "safe to replace"))
    return actions


def contained(root: Path, relative: str) -> Path:
    """Resolve one manifest path inside the tree, or refuse it.

    A stored manifest is ordinary repository data and may have been edited. The
    upgrade only ever writes paths that appear in the freshly computed release
    manifest, so containment already held by construction; this makes it an
    explicit precondition instead of an emergent property a later refactor
    could quietly drop.
    """

    root = root.resolve()
    target = Path(os.path.normpath(root / relative))
    try:
        target.relative_to(root)
    except ValueError as error:
        raise ValueError(f"manifest path escapes the tree: {relative}") from error
    return target


def apply_upgrade(installed_root: Path, release_root: Path, actions: list[Action], accept_conflicts: bool) -> int:
    applied = 0
    for action in actions:
        if action.verdict == "replace" or action.verdict == "new":
            source = release_root / action.path
            if not source.is_file():
                continue
            target = contained(installed_root, action.path)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            applied += 1
        elif action.verdict == "conflict" and accept_conflicts:
            source = release_root / action.path
            target = contained(installed_root, action.path)
            backup = target.with_suffix(target.suffix + ".local")
            shutil.copy2(target, backup)
            shutil.copy2(source, target)
            applied += 1
    return applied


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="installed project root")
    parser.add_argument("--release", required=True, help="root of the target release payload")
    parser.add_argument("--apply", action="store_true", help="write changes; omit for a dry run")
    parser.add_argument(
        "--accept-conflicts",
        action="store_true",
        help="also replace locally modified framework files, keeping a .local backup of each",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    installed_root = Path(args.root).resolve()
    release_root = Path(args.release).resolve()
    if not (release_root / "FCVW").is_dir():
        print(f"ERROR: {release_root} is not an FCVW release payload", file=sys.stderr)
        return 2

    actions = plan_upgrade(installed_root, release_root)
    counts: dict[str, int] = {}
    for action in actions:
        counts[action.verdict] = counts.get(action.verdict, 0) + 1
    conflicts = [action for action in actions if action.verdict == "conflict"]

    if args.format == "json":
        print(
            json.dumps(
                {
                    "installed_root": str(installed_root),
                    "release_root": str(release_root),
                    "applied": False,
                    "counts": dict(sorted(counts.items())),
                    "actions": [
                        {"verdict": a.verdict, "path": a.path, "role": a.role, "detail": a.detail}
                        for a in actions
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for action in actions:
            if action.verdict == "unchanged":
                continue
            print(f"{action.verdict.upper():10} [{action.role}] {action.path}: {action.detail}")
        summary = " ".join(f"{key}={value}" for key, value in sorted(counts.items()))
        print(f"FCVW upgrade plan: {summary}")

    if not args.apply:
        if conflicts:
            print(
                f"FCVW upgrade: {len(conflicts)} locally modified framework file(s); "
                "review them before applying",
                file=sys.stderr,
            )
        return 1 if conflicts else 0

    if conflicts and not args.accept_conflicts:
        print(
            f"FCVW upgrade refused: {len(conflicts)} locally modified framework file(s). "
            "Re-run with --accept-conflicts to replace them and keep .local backups.",
            file=sys.stderr,
        )
        return 1

    applied = apply_upgrade(installed_root, release_root, actions, args.accept_conflicts)
    print(f"FCVW upgrade applied: files={applied}")
    print("Next: regenerate derived artifacts and run the validator before updating FRAMEWORK_LOCK.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
