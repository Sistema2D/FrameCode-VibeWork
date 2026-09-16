#!/usr/bin/env python3
"""Verify clean installed payloads using the trusted source validator."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tempfile
import zipfile

from document_graph_fcvw import render_catalog
from package_release_fcvw import FORBIDDEN_ARCHIVE_PARTS
from release_layout_fcvw import materialize_release_layout, validate_release_layout, governed_root
from role_manifest_fcvw import build_manifest


def tool_directory(root: Path) -> Path:
    return root / "tools" if (root / "tools/validate_fcvw.py").is_file() else root / "FCVW/tools"


def validate_installed(root: Path, source_root: Path, *, run_tests: bool = False) -> None:
    validate_release_layout(root)
    source_tools, installed_tools = tool_directory(source_root), root / "FCVW/tools"
    expected = {p.name for p in source_tools.glob("*.py")}
    actual = {p.relative_to(installed_tools).as_posix() for p in installed_tools.rglob("*") if p.is_file()}
    if not expected or expected != actual:
        raise ValueError("installed tool inventory differs from trusted source")
    for name in sorted(expected):
        if (source_tools / name).read_text(encoding="utf-8-sig") != (installed_tools / name).read_text(encoding="utf-8-sig"):
            raise ValueError(f"installed tool differs from trusted source: {name}")
    subprocess.run([sys.executable, "-B", str(source_tools / "validate_fcvw.py"),
                    "--root", str(root), "--profile", "clean-template"], check=True)
    if run_tests:
        # Executable files were bound to caller-selected trusted sources above.
        subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s", str(installed_tools),
                        "-p", "test_*.py"], check=True, cwd=root)


def verify_archive(archive: Path, checksum_file: Path, source_root: Path, *, run_tests: bool = False) -> None:
    expected = {}
    for line in checksum_file.read_text(encoding="utf-8-sig").splitlines():
        fields = line.split()
        if len(fields) != 2 or not re.fullmatch(r"[a-fA-F0-9]{64}", fields[0]) or fields[1] in expected:
            raise ValueError("invalid or duplicate checksum record")
        expected[fields[1]] = fields[0].lower()
    if hashlib.sha256(archive.read_bytes()).hexdigest() != expected.get(archive.name):
        raise ValueError("archive checksum mismatch or missing checksum")
    version = re.fullmatch(r"FrameCode-VibeWork-(V\d+\.\d+\.\d+)-(pt-BR|en-US|es|de)", archive.stem)
    if not version:
        raise ValueError("unexpected release archive name")
    with tempfile.TemporaryDirectory(prefix="fcvw-verify-") as temp:
        destination = Path(temp)
        with zipfile.ZipFile(archive) as z:
            infos = z.infolist()
            if len(infos) > 20000 or sum(i.file_size for i in infos) > 128 * 1024 * 1024:
                raise ValueError("archive exceeds verification limits")
            seen = set()
            for item in infos:
                name = item.filename
                path = PurePosixPath(name)
                identity = name.rstrip("/").casefold()
                if ("\\" in name or ":" in name or path.is_absolute() or not path.parts
                        or any(p in {"..", "."} for p in name.split("/")) or "//" in name
                        or path.parts[0] != archive.stem or identity in seen
                        or FORBIDDEN_ARCHIVE_PARTS.intersection(path.parts)
                        or stat.S_ISLNK(item.external_attr >> 16)):
                    raise ValueError("unsafe archive member")
                seen.add(identity)
            z.extractall(destination)
        root = destination / archive.stem
        lock = (root / "FCVW/FRAMEWORK_LOCK.md").read_text(encoding="utf-8-sig")
        installed_versions = re.findall(r"\|\s*`(V\d+\.\d+\.\d+)`\s*\|", lock)
        if installed_versions != [version[1]]:
            raise ValueError("archive name and installed version disagree")
        validate_installed(root, source_root, run_tests=run_tests)


def smoke_source(source_root: Path, *, run_tests: bool = False) -> None:
    """Exercise the contained layout without manufacturing language reviews."""
    source_root = source_root.resolve()
    files = [p for p in source_root.rglob("*") if p.is_file()
             and not {".git", ".github", ".fcvw-cache", ".obsidian", "__pycache__", ".codex-test-tmp"}.intersection(p.relative_to(source_root).parts)]
    with tempfile.TemporaryDirectory(prefix="fcvw-source-smoke-") as temp:
        installed = Path(temp) / "installed"
        materialize_release_layout(source_root, installed, files)
        graph = installed / "FCVW/DOCUMENT_GRAPH.md"
        graph.write_text(render_catalog(installed, graph), encoding="utf-8")
        (installed / "FCVW/ROLE_MANIFEST.json").write_text(json.dumps(build_manifest(installed), indent=2), encoding="utf-8")
        validate_installed(installed, source_root, run_tests=run_tests)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", default=str(governed_root(Path(__file__))))
    parser.add_argument("--archive")
    parser.add_argument("--checksums")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--run-tests", action="store_true", help="execute installed tests only after source code parity verification")
    args = parser.parse_args()
    if args.smoke and (args.archive or args.checksums) or not args.smoke and not (args.archive and args.checksums):
        parser.error("choose --smoke or both --archive and --checksums")
    try:
        source = Path(args.source_root).resolve()
        if args.smoke:
            smoke_source(source, run_tests=args.run_tests)
        else:
            verify_archive(Path(args.archive), Path(args.checksums), source, run_tests=args.run_tests)
    except (OSError, ValueError, zipfile.BadZipFile, subprocess.CalledProcessError) as error:
        parser.exit(1, f"release verification failed: {error}\n")
    print("FCVW installed payload verification: pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
