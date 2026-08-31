#!/usr/bin/env python3
"""Map a clean FCVW source variant into its removable installed layout."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


ENTRYPOINT = Path("AGENTS.md")
FRAMEWORK_DIRECTORY = Path("FCVW")
# Provider bridges are only read by their tools at the repository root, so the
# contained layout keeps them there instead of burying them inside FCVW/.
ROOT_BRIDGES = (Path(".cursorrules"), Path(".windsurfrules"))
SOURCE_ONLY_ROOT_FILES = {Path("README.md"), Path(".gitignore")}
REQUIRED_INSTALLED_PATHS = {
    ENTRYPOINT,
    FRAMEWORK_DIRECTORY / "README.md",
    FRAMEWORK_DIRECTORY / "LICENSE",
    FRAMEWORK_DIRECTORY / "NOTICE",
    FRAMEWORK_DIRECTORY / "tools" / "validate_fcvw.py",
    FRAMEWORK_DIRECTORY / "tools" / "document_graph_fcvw.py",
    FRAMEWORK_DIRECTORY / "tools" / "frontmatter_fcvw.py",
    FRAMEWORK_DIRECTORY / "tools" / "package_release_fcvw.py",
    FRAMEWORK_DIRECTORY / "tools" / "release_layout_fcvw.py",
}


def governed_root(start: Path) -> Path:
    """Resolve the governed repository root from any tool or test file.

    Works in both supported layouts without guessing: the framework source
    checkout keeps its tools in a root `tools/`, while an installed release
    keeps them in `FCVW/tools/`. The root is the first ancestor that owns both
    `AGENTS.md` and `FCVW/`.
    """

    here = Path(start).resolve()
    for candidate in (here if here.is_dir() else here.parent, *here.parents):
        if (candidate / ENTRYPOINT).is_file() and (candidate / FRAMEWORK_DIRECTORY).is_dir():
            return candidate
    raise ValueError(f"no governed root above {start}")


def installed_path(relative: Path) -> Path | None:
    """Return the installed path for one source-relative payload file."""

    if relative.is_absolute() or ".." in relative.parts or relative == Path("."):
        raise ValueError(f"unsafe source payload path: {relative.as_posix()}")
    if relative == ENTRYPOINT or relative in ROOT_BRIDGES:
        return relative
    if relative.parent == FRAMEWORK_DIRECTORY and Path(relative.name) in ROOT_BRIDGES:
        return Path(relative.name)
    if relative in SOURCE_ONLY_ROOT_FILES:
        return None
    if relative.parts[0] == FRAMEWORK_DIRECTORY.name:
        return relative
    return FRAMEWORK_DIRECTORY / relative


def payload_mapping(source_root: Path, files: Iterable[Path]) -> dict[Path, Path]:
    """Build a collision-free installed-path to source-path mapping."""

    source_root = source_root.resolve()
    mapping: dict[Path, Path] = {}
    for source in files:
        source = source.resolve()
        try:
            relative = source.relative_to(source_root)
        except ValueError as error:
            raise ValueError(f"payload source is outside the variant: {source}") from error
        target = installed_path(relative)
        if target is None:
            continue
        if target in mapping:
            first = mapping[target].relative_to(source_root).as_posix()
            raise ValueError(
                f"installed layout collision at {target.as_posix()}: "
                f"{first} and {relative.as_posix()}"
            )
        mapping[target] = source
    return dict(sorted(mapping.items(), key=lambda item: item[0].as_posix()))


def materialize_release_layout(source_root: Path, destination: Path, files: Iterable[Path]) -> set[str]:
    """Write the mapped payload into an empty disposable destination."""

    destination = destination.resolve()
    if destination.exists() and any(destination.iterdir()):
        raise ValueError(f"installed layout destination must be empty: {destination}")
    destination.mkdir(parents=True, exist_ok=True)
    mapping = payload_mapping(source_root, files)
    for relative, source in mapping.items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
    return {path.as_posix() for path in mapping}


def is_installed_release_layout(root: Path) -> bool:
    """Identify an installed payload without confusing the conventional source tree."""

    return (
        (root / ENTRYPOINT).is_file()
        and (root / FRAMEWORK_DIRECTORY / "tools" / "validate_fcvw.py").is_file()
        and not (root / "tools" / "validate_fcvw.py").is_file()
    )


def validate_release_layout(root: Path) -> None:
    """Require an independently removable two-entry clean release root."""

    root = root.resolve()
    entries = {path.name for path in root.iterdir()}
    bridges = {bridge.name for bridge in ROOT_BRIDGES}
    expected_entries = {ENTRYPOINT.name, FRAMEWORK_DIRECTORY.name} | bridges
    if not entries <= expected_entries or not {ENTRYPOINT.name, FRAMEWORK_DIRECTORY.name} <= entries:
        raise ValueError(
            "installed release root must contain AGENTS.md and FCVW plus optional "
            f"provider bridges {sorted(bridges)}; found={sorted(entries)}"
        )
    missing = sorted(
        path.as_posix() for path in REQUIRED_INSTALLED_PATHS if not (root / path).is_file()
    )
    if missing:
        raise ValueError(f"installed release layout is incomplete: {missing}")
    residue = entries - {FRAMEWORK_DIRECTORY.name}
    if not residue <= ({ENTRYPOINT.name} | bridges):
        raise ValueError(
            "framework removal residue is not limited to AGENTS.md and provider "
            f"bridges: {sorted(residue)}"
        )
