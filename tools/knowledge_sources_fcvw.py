#!/usr/bin/env python3
"""Validate tracked FCVW knowledge sources and derive review candidates."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from frontmatter_fcvw import FrontmatterValue, scalar


SOURCE_TYPES = {"repository_file", "web", "document", "dataset", "issue", "api", "conversation", "other"}
SOURCE_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
EXTERNAL_SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)


@dataclass(frozen=True)
class SourceFinding:
    rule: str
    path: str
    message: str
    severity: str = "error"


def _tracked_path(root: Path, page: Path, value: str) -> Path | None:
    target = value.strip().strip("<>").split("#", 1)[0]
    if not target or EXTERNAL_SCHEME.match(target):
        return None
    target = target.replace("\\", "/")
    if target.startswith("/"):
        candidate = root / target.lstrip("/")
    elif target.startswith(("FCVW/", "AGENTS.md", "README.md")):
        candidate = root / target
    else:
        candidate = page.parent / target
    try:
        resolved = candidate.resolve()
        resolved.relative_to(root)
    except (OSError, ValueError):
        return None
    return resolved


def validate_source_page(
    root: Path,
    path: Path,
    metadata: dict[str, FrontmatterValue],
) -> tuple[bool, list[SourceFinding]]:
    relative = path.relative_to(root).as_posix()
    findings: list[SourceFinding] = []
    source_type = scalar(metadata, "source_type")
    source_path = scalar(metadata, "source_path")
    source_url = scalar(metadata, "source_url")
    source_digest = scalar(metadata, "source_digest")
    provenance_present = any(
        (
            source_type,
            source_path,
            source_url,
            source_digest,
            scalar(metadata, "ingested_at"),
            scalar(metadata, "last_checked"),
        )
    )
    if provenance_present and scalar(metadata, "type") != "source":
        findings.append(SourceFinding("knowledge-source", relative, "source provenance fields require type: source"))
    if source_type and source_type not in SOURCE_TYPES:
        findings.append(SourceFinding("knowledge-source", relative, f"invalid source_type: {source_type}"))
    if source_url and not re.match(r"^https?://", source_url, re.I):
        findings.append(SourceFinding("knowledge-source", relative, "source_url must use http or https"))
    if source_digest and not SOURCE_DIGEST.fullmatch(source_digest):
        findings.append(SourceFinding("knowledge-source", relative, "source_digest must be sha256:<64 lowercase hex>"))
    if not source_path:
        return False, findings
    tracked = _tracked_path(root, path, source_path)
    if tracked is None or not tracked.is_file():
        findings.append(SourceFinding("knowledge-source", relative, f"source_path is missing: {source_path}"))
        return False, findings
    if not source_digest or not SOURCE_DIGEST.fullmatch(source_digest):
        return False, findings
    actual = "sha256:" + hashlib.sha256(tracked.read_bytes()).hexdigest()
    if actual == source_digest:
        return False, findings
    findings.append(
        SourceFinding(
            "knowledge-source-stale",
            relative,
            f"tracked source digest changed: expected {source_digest}, actual {actual}",
            "warning",
        )
    )
    return True, findings


def dependent_review_findings(
    edges: list[dict[str, object]],
    stale_sources: set[str],
) -> list[SourceFinding]:
    findings: list[SourceFinding] = []
    for edge in edges:
        if edge["derived"] or edge["relation"] != "derived_from":
            continue
        target_path = str(edge["target_path"])
        if target_path in stale_sources:
            findings.append(
                SourceFinding(
                    "knowledge-review-candidate",
                    str(edge["source_path"]),
                    f"derived knowledge requires review because source changed: {target_path}",
                    "warning",
                )
            )
    return findings


def review_date_findings(
    root: Path,
    wiki_pages: list[tuple[Path, dict[str, FrontmatterValue]]],
) -> list[SourceFinding]:
    findings: list[SourceFinding] = []
    for path, metadata in wiki_pages:
        next_review = scalar(metadata, "next_review")
        if not next_review:
            continue
        try:
            overdue = date.fromisoformat(next_review) < date.today()
        except ValueError:
            continue
        if overdue:
            findings.append(
                SourceFinding(
                    "knowledge-review-due",
                    path.relative_to(root).as_posix(),
                    f"next_review is overdue: {next_review}",
                    "warning",
                )
            )
    return findings
