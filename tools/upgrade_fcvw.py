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


def load_manifest(root: Path) -> dict[str, dict[str, str]] | None:
    """Return the installation baseline, or None when there is none to trust.

    The baseline is the manifest shipped with the installed release. Rebuilding
    it from the live tree would record local edits as if they were upstream
    content, so a missing or unreadable manifest yields None and the upgrade
    falls back to treating every divergent framework file as a conflict.
    """

    stored = root / MANIFEST_PATH
    if not stored.is_file():
        return None
    try:
        data = json.loads(stored.read_text(encoding="utf-8"))
        return {entry["path"]: entry for entry in data["files"]}
    except (OSError, ValueError, KeyError, TypeError):
        return None


def dropped_action(installed_root: Path, path: str, role: str, current: dict | None, trusted: bool) -> Action:
    """Classify a file the target release no longer ships.

    Only a framework-owned file whose bytes still equal the installation
    baseline is "obsolete" and may be pruned; anything else is kept.
    """

    if role in PRESERVED_ROLES:
        return Action("preserve", path, role, "project artifact absent upstream")
    try:
        live = contained(installed_root, path)
    except ValueError:
        return Action("review", path, role, "manifest path escapes the tree")
    if not live.is_file():
        return Action("removed", path, role, "dropped by the target release; already absent")
    if not trusted:
        return Action("removed", path, role, "dropped by the target release; kept without a baseline")
    if digest(live) != (current or {}).get("digest"):
        return Action("review", path, role, "dropped by the target release but modified locally; kept")
    return Action("obsolete", path, role, "dropped by the target release; unmodified, removed by --prune")


def plan_upgrade(installed_root: Path, release_root: Path) -> list[Action]:
    baseline = load_manifest(installed_root)
    # Without a baseline, inventory the live tree for roles only; its digests are
    # never trusted as upstream content.
    installed = baseline if baseline is not None else {
        entry["path"]: entry for entry in build_manifest(installed_root)["files"]
    }
    # The release is the authority on roles for the version being installed.
    release = {entry["path"]: entry for entry in build_manifest(release_root)["files"]}

    actions: list[Action] = []
    for path in sorted(set(installed) | set(release)):
        target = release.get(path)
        current = installed.get(path)
        role = (target or current or {}).get("artifact_role", "unclassified")

        if target is None:
            actions.append(dropped_action(installed_root, path, role, current, baseline is not None))
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
        elif live_digest == target.get("digest"):
            actions.append(Action("unchanged", path, role, "identical to the target release"))
        elif baseline is None:
            actions.append(
                Action("conflict", path, role, "no installation baseline; local edits cannot be ruled out")
            )
        elif live_digest != current.get("digest"):
            actions.append(
                Action("conflict", path, role, "framework file was modified locally since installation")
            )
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
        parts = target.relative_to(root).parts
    except ValueError as error:
        raise ValueError(f"manifest path escapes the tree: {relative}") from error
    current = root
    for part in parts:
        current = current / part
        if current.is_symlink() or (hasattr(current, "is_junction") and current.is_junction()):
            raise ValueError(f"manifest path crosses a filesystem link: {relative}")
    if not target.resolve().is_relative_to(root):
        raise ValueError(f"manifest path resolves outside the tree: {relative}")
    return target


def existing_backups(installed_root: Path, actions: list[Action]) -> list[str]:
    """Conflict backups that an accepted replacement would overwrite."""

    found = []
    for action in actions:
        if action.verdict != "conflict":
            continue
        target = contained(installed_root, action.path)
        if target.with_suffix(target.suffix + ".local").exists():
            found.append(action.path + ".local")
    return found


def apply_upgrade(
    installed_root: Path, release_root: Path, actions: list[Action], accept_conflicts: bool, prune: bool = False
) -> int:
    if accept_conflicts and (backups := existing_backups(installed_root, actions)):
        raise ValueError("earlier conflict backups would be overwritten: " + ", ".join(backups))
    applied = 0
    for action in actions:
        if action.verdict == "replace" or action.verdict == "new":
            source = contained(release_root, action.path)
            if not source.is_file():
                continue
            target = contained(installed_root, action.path)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            applied += 1
        elif action.verdict == "conflict" and accept_conflicts:
            source = contained(release_root, action.path)
            target = contained(installed_root, action.path)
            backup = target.with_suffix(target.suffix + ".local")
            shutil.copy2(target, backup)
            shutil.copy2(source, target)
            applied += 1
        elif action.verdict == "obsolete" and prune:
            target = contained(installed_root, action.path)
            target.unlink()
            remove_empty_parents(installed_root, target.parent)
            applied += 1
    # The applied release becomes the next baseline. A conflict that was kept
    # locally keeps differing from it, so the next upgrade reports it again.
    # Obsolete files that were not pruned stay in the baseline so a later
    # --prune can still prove they are unmodified.
    manifest = build_manifest(release_root)
    previous = load_manifest(installed_root) or {}
    kept = [
        previous[action.path]
        for action in actions
        if action.verdict == "obsolete" and not prune and action.path in previous
    ]
    manifest["files"] = sorted([*manifest["files"], *kept], key=lambda item: item["path"])
    baseline = contained(installed_root, MANIFEST_PATH.as_posix())
    baseline.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return applied


def remove_empty_parents(root: Path, folder: Path) -> None:
    """Remove directories emptied by pruning, never the governed root itself."""

    stop = {root.resolve(), (root / "FCVW").resolve()}
    folder = folder.resolve()
    while folder not in stop and folder.is_relative_to(root.resolve()) and not any(folder.iterdir()):
        folder.rmdir()
        folder = folder.parent


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
    parser.add_argument(
        "--prune",
        action="store_true",
        help="with --apply, delete framework files dropped upstream that are identical to the baseline",
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
    baseline = (installed_root / MANIFEST_PATH).is_file()

    status, applied, message = 0, None, ""
    if not args.apply:
        if conflicts:
            status = 1
            message = (f"FCVW upgrade: {len(conflicts)} locally modified or unverifiable framework file(s); "
                       "review them before applying")
    elif conflicts and not args.accept_conflicts:
        status = 1
        message = (f"FCVW upgrade refused: {len(conflicts)} locally modified or unverifiable framework file(s). "
                   "Re-run with --accept-conflicts to replace them and keep .local backups.")
    else:
        try:
            applied = apply_upgrade(installed_root, release_root, actions, args.accept_conflicts, args.prune)
        except ValueError as error:
            status, message = 1, f"FCVW upgrade refused: {error}"

    if args.format == "json":
        print(
            json.dumps(
                {
                    "installed_root": str(installed_root),
                    "release_root": str(release_root),
                    "baseline": "installed_manifest" if baseline else "missing",
                    "applied": applied is not None,
                    "files_applied": applied or 0,
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
        if not baseline:
            print("FCVW upgrade: no installation baseline (FCVW/ROLE_MANIFEST.json); "
                  "every divergent framework file is treated as a conflict.")
        if applied is not None:
            print(f"FCVW upgrade applied: files={applied}")
            print("Next: regenerate derived artifacts and run the validator before updating FRAMEWORK_LOCK.md.")
    if message:
        print(message, file=sys.stderr)
    return status


if __name__ == "__main__":
    sys.exit(main())
