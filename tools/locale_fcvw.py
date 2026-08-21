#!/usr/bin/env python3
"""Validate independent language-specific FCVW release variants in external staging."""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

from document_graph_fcvw import build_graph
from frontmatter_fcvw import parse_frontmatter, scalar


RELEASE_VARIANTS = {
    "pt-BR": "pt-BR",
    "en-US": "en-US",
    "es": "es",
    "de": "de",
}
REFERENCE_VARIANT = "en-US"
REQUIRED_VARIANT_PATHS = {
    "AGENTS.md",
    "README.md",
    "LICENSE",
    "NOTICE",
    "FCVW/README.md",
    "FCVW/DOCUMENT_GRAPH.md",
    "FCVW/LANGUAGE_REVIEW.md",
    "tools/validate_fcvw.py",
    "tools/document_graph_fcvw.py",
    "tools/frontmatter_fcvw.py",
    "tools/release_layout_fcvw.py",
}
RELEASE_EVIDENCE_PATHS = {
    "FCVW/LANGUAGE_REVIEW.md",
    "FCVW/framework-releases/V0.14.0.md",
    "FCVW/Plans/completed/P2-R5-2026-07-27-open-issues-42-48-and-document-graph.md",
}
RELEASE_EVIDENCE_GRAPH_TARGETS = {"LANGUAGE_REVIEW.md"}
RELEASE_EVIDENCE_GRAPH_LABELS = {"FCVW/LANGUAGE_REVIEW.md"}
IGNORED_PARTS = {".git", ".obsidian", "__pycache__", ".codex-test-tmp"}
FORBIDDEN_PACKAGE_PARTS = {".git", ".github", ".obsidian", "__pycache__", ".codex-test-tmp"}
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
INLINE_CODE = re.compile(r"`([^`\n]+)`")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING = re.compile(r"^(#{1,6})\s+")
CONTROLLED_METADATA = {
    "schema",
    "id",
    "artifact_role",
    "upgrade_strategy",
    "status",
    "priority",
    "risk",
    "current_version",
    "expected_version",
    "version",
    "release_status",
    "release_type",
    "compatibility",
    "record_scope",
    "regression_contract",
    "instantiation_status",
    "state",
    "external_publication",
    "source_revision",
    "publication_revision",
    "retrieval_scope",
    "retrieval_priority",
    "authority",
    "context_files",
    "sources",
    "related_plans",
    "release_languages",
    "related_plan",
    "related_release",
    "related",
    "supersedes",
    "superseded_by",
}


@dataclass(frozen=True)
class LocaleFinding:
    rule: str
    path: str
    message: str
    severity: str = "error"


def file_manifest(variant_root: Path) -> set[str]:
    return {
        path.relative_to(variant_root).as_posix()
        for path in variant_root.rglob("*")
        if path.is_file() and not any(part in IGNORED_PARTS for part in path.relative_to(variant_root).parts)
    }


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def forbidden_package_state(package_root: Path) -> set[str]:
    found: set[str] = set()
    for path in package_root.rglob("*"):
        relative = path.relative_to(package_root)
        found.update(part for part in relative.parts if part in FORBIDDEN_PACKAGE_PARTS)
    return found


def _machine_token(value: str) -> bool:
    return bool(
        re.search(r"[/\\]|\.md\b|\.py\b|^--|^python(?:\s|$)|^fcvw/|^V\d+\.\d+", value, re.I)
        or re.fullmatch(r"(?:APP-RULE|ADR|REG|SES|P[1-5]-R[1-5])-[A-Za-z0-9_.-]+", value)
        or re.fullmatch(r"[A-Z][A-Z0-9_-]{2,}", value)
    )


def _markdown_destination(raw: str) -> str:
    value = raw.strip()
    if value.startswith("<"):
        closing = value.find(">")
        if closing != -1:
            return unquote(value[1:closing]).split("#", 1)[0]
    return unquote(value.split(maxsplit=1)[0]).split("#", 1)[0]


def markdown_machine_signature(path: Path) -> tuple[tuple[str, str], ...]:
    text = path.read_text(encoding="utf-8-sig")
    metadata = parse_frontmatter(text).data
    signature: list[tuple[str, str]] = []
    for field in sorted(CONTROLLED_METADATA):
        raw_value = metadata.get(field)
        values = raw_value if isinstance(raw_value, list) else [raw_value]
        for value in values:
            if isinstance(value, str) and value:
                signature.append((f"frontmatter:{field}", value))
    for match in MARKDOWN_LINK.finditer(text):
        target = _markdown_destination(match.group(1))
        if target and not re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
            signature.append(("link-target", target.replace("\\", "/")))
    for value in INLINE_CODE.findall(text):
        normalized = value.strip()
        if _machine_token(normalized):
            signature.append(("inline-code", normalized))
    if path.name == "QUEUE.md" and "Plans" in path.parts:
        for line in text.splitlines():
            if not line.strip().startswith("|"):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) == 5 and cells[0].isdigit():
                signature.extend(
                    (
                        ("queue-order", cells[0]),
                        ("queue-category", cells[2]),
                        ("queue-blocked-by", cells[3]),
                    )
                )
    marker = ""
    block: list[str] = []
    for line in text.splitlines(keepends=True):
        fence = FENCE.match(line)
        if fence and not marker:
            marker = fence.group(1)
            block = [line]
            continue
        if marker:
            block.append(line)
            if fence and fence.group(1)[0] == marker[0] and len(fence.group(1)) >= len(marker):
                signature.append(("fenced-code", hashlib.sha256("".join(block).encode("utf-8")).hexdigest()))
                marker = ""
                block = []
    if marker:
        signature.append(("fenced-code-unclosed", hashlib.sha256("".join(block).encode("utf-8")).hexdigest()))
    return tuple(sorted(Counter(signature).elements()))


def markdown_structure_signature(path: Path) -> tuple[str, ...]:
    structure: list[str] = []
    marker = ""
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        fence = FENCE.match(line)
        if fence:
            current = fence.group(1)
            if not marker:
                marker = current
            elif current[0] == marker[0] and len(current) >= len(marker):
                marker = ""
            continue
        if not marker and (heading := HEADING.match(line)):
            structure.append(f"heading:{len(heading.group(1))}")
            continue
        if marker:
            continue
        if unordered := re.match(r"^(\s*)[-+*]\s+", line):
            structure.append(f"unordered-list:{len(unordered.group(1))}")
            continue
        if ordered := re.match(r"^(\s*)\d+[.)]\s+", line):
            structure.append(f"ordered-list:{len(ordered.group(1))}")
            continue
        if quote := re.match(r"^\s*(>+)\s*", line):
            structure.append(f"blockquote:{len(quote.group(1))}")
            continue
        if line.strip().startswith("|") and line.strip().endswith("|"):
            structure.append(f"table-row:{line.count('|') - 1}")
    return tuple(structure)


def source_comparison_signature(path: Path, relative: str) -> tuple[tuple[str, str], ...]:
    signature = markdown_machine_signature(path)
    if relative != "FCVW/DOCUMENT_GRAPH.md":
        return signature
    return tuple(
        item
        for item in signature
        if not (
            (item[0] == "link-target" and item[1] in RELEASE_EVIDENCE_GRAPH_TARGETS)
            or (item[0] == "inline-code" and item[1] in RELEASE_EVIDENCE_GRAPH_LABELS)
        )
    )


def _run_clean_validator(variant_root: Path) -> tuple[bool, str]:
    validator = Path(__file__).resolve().with_name("validate_fcvw.py")
    if not validator.is_file():
        return False, "authoritative clean-template validator is missing"
    try:
        result = subprocess.run(
            [sys.executable, "-B", str(validator), "--root", str(variant_root), "--profile", "clean-template"],
            cwd=validator.parent,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        return False, "authoritative clean-template validation timed out"
    except OSError as error:
        return False, f"authoritative clean-template validator could not run: {error}"
    detail = (result.stdout + result.stderr).strip().replace("\n", " | ")
    return result.returncode == 0, detail[-600:]


def validate_release_variants(
    staging_root: Path,
    *,
    require_complete: bool = False,
    source_root: Path | None = None,
    source_revision: str = "",
    run_clean_validation: bool | None = None,
) -> list[LocaleFinding]:
    staging_root = staging_root.resolve()
    source_root = source_root.resolve() if source_root is not None else None
    run_clean_validation = require_complete if run_clean_validation is None else run_clean_validation
    present = {name for name in RELEASE_VARIANTS if (staging_root / name).is_dir()}
    if not present:
        if require_complete:
            return [
                LocaleFinding("locale-missing", name, "required language-specific release variant is missing")
                for name in RELEASE_VARIANTS
            ]
        return []

    findings: list[LocaleFinding] = []
    missing_variants = set(RELEASE_VARIANTS) - present
    for name in sorted(missing_variants):
        findings.append(LocaleFinding("locale-missing", name, "release staging is missing this language variant"))
    if missing_variants:
        return findings
    if require_complete and source_root is None:
        findings.append(
            LocaleFinding(
                "locale-source-baseline",
                ".",
                "--source-root must identify the authoritative clean template",
            )
        )
    if require_complete and source_root is not None:
        try:
            source_root.relative_to(staging_root)
        except ValueError:
            pass
        else:
            findings.append(
                LocaleFinding(
                    "locale-source-baseline",
                    str(source_root),
                    "--source-root must be external to release staging",
                )
            )
    if require_complete and not re.fullmatch(r"[0-9a-fA-F]{40}", source_revision):
        findings.append(
            LocaleFinding(
                "locale-source-revision",
                ".",
                "--source-revision must be an immutable 40-character Git revision",
            )
        )

    reference_root = staging_root / REFERENCE_VARIANT
    reference_manifest = file_manifest(reference_root)
    source_manifest = file_manifest(source_root) if source_root is not None and source_root.is_dir() else None
    if require_complete and source_root is not None and source_manifest is None:
        findings.append(LocaleFinding("locale-source-baseline", str(source_root), "source root is missing"))
    if source_root is not None and source_manifest is not None:
        for state in sorted(forbidden_package_state(source_root)):
            findings.append(
                LocaleFinding(
                    "locale-source-baseline",
                    f"{source_root}/{state}",
                    f"clean source baseline contains forbidden repository/editor state: {state}",
                )
            )
    if run_clean_validation and source_root is not None and source_manifest is not None:
        passed, detail = _run_clean_validator(source_root)
        if not passed:
            findings.append(
                LocaleFinding(
                    "locale-source-baseline",
                    str(source_root),
                    f"source clean-template validation failed: {detail or 'no output'}",
                )
            )
    if source_manifest is not None:
        functional_source_manifest = source_manifest - RELEASE_EVIDENCE_PATHS
        functional_reference_manifest = reference_manifest - RELEASE_EVIDENCE_PATHS
        for missing in sorted(functional_source_manifest - functional_reference_manifest):
            findings.append(
                LocaleFinding(
                    "locale-source-parity",
                    f"{REFERENCE_VARIANT}/{missing}",
                    "path is missing relative to the clean source baseline",
                )
            )
        for extra in sorted(functional_reference_manifest - functional_source_manifest):
            findings.append(
                LocaleFinding(
                    "locale-source-parity",
                    f"{REFERENCE_VARIANT}/{extra}",
                    "extra functional path relative to the clean source baseline",
                )
            )
    for name, language in RELEASE_VARIANTS.items():
        variant_root = staging_root / name
        for state in sorted(forbidden_package_state(variant_root)):
            findings.append(
                LocaleFinding(
                    "locale-package-state",
                    f"{name}/{state}",
                    f"repository, cache, or editor state must not enter a language-specific release variant: {state}",
                )
            )
        manifest = file_manifest(variant_root)
        for required in sorted(REQUIRED_VARIANT_PATHS - manifest):
            findings.append(
                LocaleFinding("locale-required-path", f"{name}/{required}", "required release-variant path is missing")
            )
        for missing in sorted(reference_manifest - manifest):
            findings.append(
                LocaleFinding(
                    "locale-parity",
                    f"{name}/{missing}",
                    f"path is missing relative to {REFERENCE_VARIANT}",
                )
            )
        for extra in sorted(manifest - reference_manifest):
            findings.append(
                LocaleFinding(
                    "locale-parity",
                    f"{name}/{extra}",
                    f"extra path relative to {REFERENCE_VARIANT}",
                )
            )

        review_path = variant_root / "FCVW" / "LANGUAGE_REVIEW.md"
        if review_path.is_file():
            metadata = parse_frontmatter(review_path.read_text(encoding="utf-8-sig")).data
            if scalar(metadata, "schema") != "fcvw/language-review@1":
                findings.append(LocaleFinding("locale-review", f"{name}/FCVW/LANGUAGE_REVIEW.md", "invalid review schema"))
            if scalar(metadata, "language") != language:
                findings.append(LocaleFinding("locale-review", f"{name}/FCVW/LANGUAGE_REVIEW.md", "language does not match locale"))
            if scalar(metadata, "status") != "approved":
                findings.append(LocaleFinding("locale-review", f"{name}/FCVW/LANGUAGE_REVIEW.md", "language review is not approved"))
            for field in ("reviewer", "reviewed_at", "source_revision"):
                if not scalar(metadata, field):
                    findings.append(
                        LocaleFinding("locale-review", f"{name}/FCVW/LANGUAGE_REVIEW.md", f"missing review field: {field}")
                    )
            if source_revision and scalar(metadata, "source_revision") != source_revision:
                findings.append(
                    LocaleFinding(
                        "locale-review",
                        f"{name}/FCVW/LANGUAGE_REVIEW.md",
                        "source_revision does not match the release source revision",
                    )
                )

        for relative in sorted(path for path in manifest if path.endswith(".md")):
            metadata = parse_frontmatter((variant_root / relative).read_text(encoding="utf-8-sig")).data
            declared_language = scalar(metadata, "language")
            if declared_language and declared_language != language:
                findings.append(
                    LocaleFinding(
                        "locale-language-metadata",
                        f"{name}/{relative}",
                        f"declared language must match {language}",
                    )
                )

        for relative in sorted(reference_manifest & manifest):
            reference_path = reference_root / relative
            variant_path = variant_root / relative
            if reference_path.suffix.lower() != ".md" and digest(reference_path) != digest(variant_path):
                findings.append(
                    LocaleFinding(
                        "locale-machine-parity",
                        f"{name}/{relative}",
                        f"non-Markdown surface differs from {REFERENCE_VARIANT}",
                    )
                )
            if reference_path.suffix.lower() == ".md":
                reference_schema = scalar(
                    parse_frontmatter(reference_path.read_text(encoding="utf-8-sig")).data,
                    "schema",
                )
                variant_schema = scalar(
                    parse_frontmatter(variant_path.read_text(encoding="utf-8-sig")).data,
                    "schema",
                )
                if reference_schema != variant_schema:
                    findings.append(
                        LocaleFinding(
                            "locale-schema-parity",
                            f"{name}/{relative}",
                            f"schema differs from {REFERENCE_VARIANT}",
                        )
                    )
                if markdown_machine_signature(reference_path) != markdown_machine_signature(variant_path):
                    findings.append(
                        LocaleFinding(
                            "locale-machine-parity",
                            f"{name}/{relative}",
                            f"Markdown machine identifiers or link targets differ from {REFERENCE_VARIANT}",
                        )
                    )
                if markdown_structure_signature(reference_path) != markdown_structure_signature(variant_path):
                    findings.append(
                        LocaleFinding(
                            "locale-markdown-structure",
                            f"{name}/{relative}",
                            f"Markdown heading structure differs from {REFERENCE_VARIANT}",
                        )
                    )

        graph = build_graph(variant_root)
        findings.extend(
            LocaleFinding(f"locale-{item.rule}", f"{name}/{item.path}", item.message, item.severity)
            for item in graph.findings
        )
        if run_clean_validation:
            passed, detail = _run_clean_validator(variant_root)
            if not passed:
                findings.append(
                    LocaleFinding(
                        "locale-clean-template",
                        name,
                        f"clean-template validation failed: {detail or 'no output'}",
                    )
                )
    if source_root is not None and source_manifest is not None:
        for relative in sorted((source_manifest - RELEASE_EVIDENCE_PATHS) & (reference_manifest - RELEASE_EVIDENCE_PATHS)):
            source_path = source_root / relative
            reference_path = reference_root / relative
            if source_path.suffix.lower() != ".md" and digest(source_path) != digest(reference_path):
                findings.append(
                    LocaleFinding(
                        "locale-source-parity",
                        f"{REFERENCE_VARIANT}/{relative}",
                        "non-Markdown surface differs from source",
                    )
                )
            if source_path.suffix.lower() == ".md" and source_comparison_signature(
                source_path,
                relative,
            ) != source_comparison_signature(reference_path, relative):
                findings.append(
                    LocaleFinding(
                        "locale-source-parity",
                        f"{REFERENCE_VARIANT}/{relative}",
                        "Markdown machine surface differs from source",
                    )
                )
            if (
                source_path.suffix.lower() == ".md"
                and relative != "FCVW/DOCUMENT_GRAPH.md"
                and markdown_structure_signature(source_path)
                != markdown_structure_signature(reference_path)
            ):
                findings.append(
                    LocaleFinding(
                        "locale-source-parity",
                        f"{REFERENCE_VARIANT}/{relative}",
                        "Markdown heading structure differs from source",
                    )
                )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=".",
        help="external release-staging root containing pt-BR/, en-US/, es/, and de/",
    )
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--source-root")
    parser.add_argument("--source-revision", default="")
    args = parser.parse_args()
    findings = validate_release_variants(
        Path(args.root),
        require_complete=args.require_complete,
        source_root=Path(args.source_root) if args.source_root else None,
        source_revision=args.source_revision,
    )
    for finding in findings:
        print(f"{finding.severity.upper()} [{finding.rule}] {finding.path}: {finding.message}")
    errors = [item for item in findings if item.severity == "error"]
    present = sum((Path(args.root) / name).is_dir() for name in RELEASE_VARIANTS)
    print(
        "FCVW release variants: "
        f"present={present}/{len(RELEASE_VARIANTS)} errors={len(errors)} findings={len(findings)}"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
