#!/usr/bin/env python3
"""Emit the machine-readable file-role manifest that OWNERSHIP.md requires.

`OWNERSHIP.md` states that an upstream release must publish a file-role manifest
or an equivalent migration table "so that selective upgrade does not depend on
assumptions". Until now the role of each artifact existed only inside its own
frontmatter, which a human can read but an upgrade tool cannot inventory, and
nothing recorded a content digest, so a locally edited framework policy was
indistinguishable from an untouched one at upgrade time.

The manifest is a generated artifact: it is rebuilt from the tree and is never a
source of truth about ownership. The frontmatter remains authoritative.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from fcvw_cache import frontmatter as cache_frontmatter
from frontmatter_fcvw import scalar
from release_layout_fcvw import ROOT_BRIDGES

MANIFEST_SCHEMA = "fcvw/role-manifest@1"
MANIFEST_PATH = Path("FCVW") / "ROLE_MANIFEST.json"
IGNORED_PARTS = {".git", ".github", ".obsidian", "__pycache__", ".fcvw-cache"}
# Records that describe the framework's own development stay framework-owned even
# though they live under a project-owned directory. Without this distinction an
# upgrade cannot replace them and they silently become permanent project history.
FRAMEWORK_HISTORY_ROLE = "framework_history"


# The lock is a two-column table whose row labels are translated in every
# release variant, so the label is not a usable anchor. The version row is the
# one whose value is a framework version, which is a controlled value and is
# therefore identical in all four languages.
LOCK_VERSION = re.compile(r"^V\d+\.\d+\.\d+$")


def installed_version(root: Path) -> str:
    """Read the installed baseline from the FRAMEWORK_LOCK table."""

    lock = root / "FCVW" / "FRAMEWORK_LOCK.md"
    if not lock.is_file():
        return "unknown"
    for line in lock.read_text(encoding="utf-8-sig").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in stripped.strip("|").split("|")]
        if len(cells) != 2:
            continue
        if LOCK_VERSION.fullmatch(cells[1]):
            return cells[1]
    return "unknown"


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def governed_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    for candidate in sorted((root / "FCVW").rglob("*")):
        if not candidate.is_file():
            continue
        if any(part in IGNORED_PARTS for part in candidate.relative_to(root).parts):
            continue
        if candidate.relative_to(root) == MANIFEST_PATH:
            continue
        paths.append(candidate)
    for extra in (Path("AGENTS.md"), *ROOT_BRIDGES):
        if (root / extra).is_file():
            paths.append(root / extra)
    return sorted(paths, key=lambda item: item.relative_to(root).as_posix())


# Most governed Markdown declares its role in frontmatter, but templates, skills,
# the refactoring guide and directory scaffolding historically do not. Their role
# is unambiguous from their location, so the manifest infers it from a documented
# rule and records that the value was inferred rather than declared. Inference
# keeps the manifest complete without rewriting well over a hundred files in four
# language variants; frontmatter stays authoritative wherever it exists.
INFERRED_ROLES = (
    ("FCVW/governance/", "template", "framework", "replace"),
    ("FCVW/wiki/templates/", "template", "framework", "replace"),
    ("FCVW/skills/", "framework_skill", "framework", "replace"),
    ("FCVW/refactoring-guide/", "framework_policy", "framework", "replace"),
    ("FCVW/examples/", "example", "framework", "replace"),
    # Every framework release record is framework history by definition, whether
    # or not the individual file declares record_scope.
    ("FCVW/framework-releases/", FRAMEWORK_HISTORY_ROLE, "framework", "replace"),
)
SCAFFOLD_NAMES = {"README.md"}


def _infer(relative: str, path: Path) -> tuple[str, str, str] | None:
    for prefix, role, owner, strategy in INFERRED_ROLES:
        if relative.startswith(prefix):
            return role, owner, strategy
    if relative == "AGENTS.md":
        return "framework_policy", "framework", "replace"
    if Path(relative).name in SCAFFOLD_NAMES:
        return "framework_scaffold", "framework", "replace"
    if Path(relative).name == "QUEUE.md":
        return "generated", "project", "regenerate"
    return None


def classify(root: Path, path: Path) -> dict[str, str]:
    relative = path.relative_to(root).as_posix()
    entry: dict[str, str] = {"path": relative, "digest": digest(path)}
    if path.suffix.lower() != ".md":
        entry.update(
            artifact_role="framework_tool" if path.suffix == ".py" else "framework_asset",
            owner="framework",
            upgrade_strategy="replace",
            role_source="path",
        )
        return entry

    metadata = cache_frontmatter(path)
    role = scalar(metadata, "artifact_role")
    owner = scalar(metadata, "owner")
    strategy = scalar(metadata, "upgrade_strategy")
    record_scope = scalar(metadata, "record_scope")
    source = "declared"

    # Framework development history lives under project-owned directories. It is
    # recognised by record_scope before any other inference, because the legacy
    # fcvw/plan@1 records declare the scope without declaring an artifact_role.
    # Without this promotion an upgrade cannot replace them and they become
    # permanent project history in every derived repository.
    if record_scope == "framework" and role in {"", "record", "unclassified"}:
        entry.update(
            artifact_role=FRAMEWORK_HISTORY_ROLE,
            owner="framework",
            upgrade_strategy="replace",
            role_source="declared" if role else "record_scope",
            record_scope=record_scope,
        )
        return entry

    if not role:
        inferred = _infer(relative, path)
        if inferred is None:
            entry.update(
                artifact_role="unclassified",
                owner=owner or "unknown",
                upgrade_strategy=strategy or "unknown",
                role_source="none",
            )
            return entry
        role, inferred_owner, inferred_strategy = inferred
        owner = owner or inferred_owner
        strategy = strategy or inferred_strategy
        source = "inferred"

    entry.update(
        artifact_role=role,
        owner=owner or "unknown",
        upgrade_strategy=strategy or "unknown",
        role_source=source,
    )
    if record_scope:
        entry["record_scope"] = record_scope
    return entry


def build_manifest(root: Path) -> dict[str, object]:
    root = root.resolve()
    entries = [classify(root, path) for path in governed_files(root)]
    counts: dict[str, int] = {}
    for entry in entries:
        counts[entry["artifact_role"]] = counts.get(entry["artifact_role"], 0) + 1
    return {
        "schema": MANIFEST_SCHEMA,
        "framework_version": installed_version(root),
        "generated_from": "frontmatter",
        "authority": "generated",
        "role_counts": dict(sorted(counts.items())),
        "files": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--write", action="store_true", help=f"write {MANIFEST_PATH.as_posix()}")
    parser.add_argument("--output", help="write the manifest to an explicit path instead")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    manifest = build_manifest(root)
    payload = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=False) + "\n"

    if args.output or args.write:
        target = Path(args.output) if args.output else root / MANIFEST_PATH
        if not target.is_absolute():
            target = root / target
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(payload, encoding="utf-8", newline="\n")
        print(f"FCVW role manifest: files={len(manifest['files'])} output={target}")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
