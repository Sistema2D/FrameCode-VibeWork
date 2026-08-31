#!/usr/bin/env python3
"""Validate and build deterministic FCVW language-specific release archives."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import zipfile
from pathlib import Path

from document_graph_fcvw import render_catalog
from frontmatter_fcvw import parse_frontmatter, scalar
from locale_fcvw import RELEASE_VARIANTS, LocaleFinding, validate_release_variants
from role_manifest_fcvw import MANIFEST_PATH, build_manifest
from release_layout_fcvw import materialize_release_layout, validate_release_layout


VERSION = re.compile(r"V\d+\.\d+\.\d+")
ARCHIVE_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
FORBIDDEN_ARCHIVE_PARTS = {
    ".git",
    ".github",
    ".obsidian",
    ".codex-test-tmp",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}
REVIEW_PATH = Path("FCVW/LANGUAGE_REVIEW.md")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def package_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        forbidden = FORBIDDEN_ARCHIVE_PARTS.intersection(relative.parts)
        if forbidden:
            raise ValueError(f"forbidden package state: {relative.as_posix()}")
        if path.suffix.lower() in {".pyc", ".pyo"}:
            raise ValueError(f"compiled Python artifact is forbidden: {relative.as_posix()}")
        if path.is_symlink():
            raise ValueError(f"symbolic links are forbidden in release payloads: {relative.as_posix()}")
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())


def candidate_review_findings(staging_root: Path) -> list[LocaleFinding]:
    findings: list[LocaleFinding] = []
    for language in RELEASE_VARIANTS:
        review = staging_root / language / REVIEW_PATH
        if not review.is_file():
            continue
        metadata = parse_frontmatter(review.read_text(encoding="utf-8-sig")).data
        if scalar(metadata, "status") != "in_review":
            findings.append(
                LocaleFinding(
                    "locale-review",
                    f"{language}/{REVIEW_PATH.as_posix()}",
                    "local candidate review status must be in_review",
                )
            )
    return findings


def blocking_findings(findings: list[LocaleFinding], *, allow_in_review: bool) -> list[LocaleFinding]:
    if not allow_in_review:
        return [item for item in findings if item.severity == "error"]
    return [
        item
        for item in findings
        if item.severity == "error"
        and not (item.rule == "locale-review" and item.message == "language review is not approved")
    ]


def write_archive(source: Path, destination: Path, archive_root: str) -> None:
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in package_files(source):
            relative = path.relative_to(source).as_posix()
            info = zipfile.ZipInfo(f"{archive_root}/{relative}", date_time=ARCHIVE_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            mode = 0o755 if path.suffix.lower() == ".sh" else 0o644
            info.external_attr = (mode & 0xFFFF) << 16
            info.flag_bits |= 0x800
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def inspect_archive(path: Path, archive_root: str, expected_files: set[str]) -> None:
    with zipfile.ZipFile(path) as archive:
        members = [name for name in archive.namelist() if not name.endswith("/")]
        expected = {f"{archive_root}/{relative}" for relative in expected_files}
        if set(members) != expected:
            missing = sorted(expected - set(members))
            extra = sorted(set(members) - expected)
            raise ValueError(f"archive manifest mismatch; missing={missing[:3]} extra={extra[:3]}")
        for member in members:
            relative = Path(member).relative_to(archive_root)
            forbidden = FORBIDDEN_ARCHIVE_PARTS.intersection(relative.parts)
            if forbidden:
                raise ValueError(f"archive contains forbidden package state: {member}")
            if Path(member).suffix.lower() in {".pyc", ".pyo"}:
                raise ValueError(f"archive contains compiled Python artifact: {member}")
            if Path(member).is_absolute() or ".." in Path(member).parts:
                raise ValueError(f"archive contains unsafe path: {member}")
        first_level = {Path(member).relative_to(archive_root).parts[0] for member in members}
        allowed_root = {"AGENTS.md", "FCVW", ".cursorrules", ".windsurfrules"}
        if not first_level <= allowed_root or not {"AGENTS.md", "FCVW"} <= first_level:
            raise ValueError(
                "archive payload root must contain AGENTS.md and FCVW plus optional "
                "provider bridges; "
                f"found={sorted(first_level)}"
            )


def create_archives(staging_root: Path, output_root: Path, version: str, *, replace: bool = False) -> dict[str, str]:
    if not VERSION.fullmatch(version):
        raise ValueError(f"invalid framework version: {version}")
    staging_root = staging_root.resolve()
    output_root = output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    asset_paths = {
        language: output_root / f"FrameCode-VibeWork-{version}-{language}.zip"
        for language in RELEASE_VARIANTS
    }
    checksum_path = output_root / "SHA256SUMS.txt"
    existing = [path for path in (*asset_paths.values(), checksum_path) if path.exists()]
    if existing and not replace:
        names = ", ".join(path.name for path in existing)
        raise FileExistsError(f"release assets already exist: {names}")
    for path in existing:
        if not path.is_file() or path.parent != output_root:
            raise ValueError(f"refusing to replace unexpected target: {path}")

    temporary_assets: dict[str, Path] = {}
    checksums: dict[str, str] = {}
    temporary_checksum: Path | None = None
    try:
        with tempfile.TemporaryDirectory(prefix="fcvw-release-layout-") as layout_directory:
            layout_root = Path(layout_directory)
            for language, destination in asset_paths.items():
                variant = staging_root / language
                if not variant.is_dir():
                    raise FileNotFoundError(f"release variant is missing: {variant}")
                installed = layout_root / language
                materialize_release_layout(variant, installed, package_files(variant))
                graph_path = installed / "FCVW" / "DOCUMENT_GRAPH.md"
                graph_path.write_text(render_catalog(installed, graph_path), encoding="utf-8", newline="\n")
                # The role manifest records a path and a digest per file, so a
                # manifest built from the source tree would describe paths the
                # payload does not have and digests the packager just changed.
                # It has to be rebuilt from the materialised installed layout.
                manifest_path = installed / MANIFEST_PATH
                manifest_path.write_text(
                    json.dumps(build_manifest(installed), ensure_ascii=False, indent=2) + chr(10),
                    encoding="utf-8",
                    newline=chr(10),
                )
                validate_release_layout(installed)
                manifest = {path.relative_to(installed).as_posix() for path in package_files(installed)}

                descriptor, temporary_name = tempfile.mkstemp(
                    dir=output_root,
                    prefix=f".{destination.name}.",
                    suffix=".tmp",
                )
                os.close(descriptor)
                temporary = Path(temporary_name)
                temporary_assets[language] = temporary
                archive_root = destination.stem
                write_archive(installed, temporary, archive_root)
                inspect_archive(temporary, archive_root, manifest)
                checksums[destination.name] = sha256(temporary)
        descriptor, temporary_name = tempfile.mkstemp(
            dir=output_root,
            prefix=".SHA256SUMS.",
            suffix=".tmp",
        )
        os.close(descriptor)
        temporary_checksum = Path(temporary_name)
        temporary_checksum.write_text(
            "".join(f"{digest}  {name}\n" for name, digest in sorted(checksums.items())),
            encoding="utf-8",
            newline="\n",
        )
        for language, destination in asset_paths.items():
            os.replace(temporary_assets[language], destination)
        os.replace(temporary_checksum, checksum_path)
    finally:
        for temporary in temporary_assets.values():
            if temporary.exists():
                temporary.unlink()
        if temporary_checksum is not None and temporary_checksum.exists():
            temporary_checksum.unlink()
    return checksums


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="external staging root containing the four variants")
    parser.add_argument("--source-root", required=True, help="authoritative clean source outside staging")
    parser.add_argument("--source-revision", required=True, help="immutable 40-character content revision")
    parser.add_argument("--version", required=True, help="framework version such as V0.14.0")
    parser.add_argument("--output", required=True, help="directory for ZIP assets and SHA256SUMS.txt")
    parser.add_argument(
        "--allow-in-review",
        action="store_true",
        help="build local candidate ZIPs while preserving the publication blocker",
    )
    parser.add_argument("--replace", action="store_true", help="replace only the exact expected asset files")
    args = parser.parse_args()

    staging_root = Path(args.root)
    findings = validate_release_variants(
        staging_root,
        require_complete=True,
        source_root=Path(args.source_root),
        source_revision=args.source_revision,
    )
    if args.allow_in_review:
        findings.extend(candidate_review_findings(staging_root))
    blocking = blocking_findings(findings, allow_in_review=args.allow_in_review)
    for finding in findings:
        tolerated = finding not in blocking
        label = "CANDIDATE" if tolerated else finding.severity.upper()
        print(f"{label} [{finding.rule}] {finding.path}: {finding.message}")
    if blocking:
        print(f"FCVW packaging blocked: errors={len(blocking)}")
        return 1
    try:
        checksums = create_archives(
            staging_root,
            Path(args.output),
            args.version,
            replace=args.replace,
        )
    except (FileExistsError, FileNotFoundError, OSError, ValueError, zipfile.BadZipFile) as error:
        print(f"ERROR [release-package] {error}")
        return 1
    for name, digest in sorted(checksums.items()):
        print(f"SHA256 {digest}  {name}")
    state = "candidate" if args.allow_in_review else "approved"
    print(f"FCVW release packages: assets={len(checksums)} state={state}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
