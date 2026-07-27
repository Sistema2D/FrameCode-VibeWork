#!/usr/bin/env python3
"""Build an optional, non-authoritative FCVW Markdown section index."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path

from frontmatter_fcvw import parse_frontmatter, scalar, string_list


HEADING = re.compile(r"^(#{2,3})\s+(.+?)\s*$")
FENCE = re.compile(r"^\s*(```+|~~~+)")
EXCLUDED_PARTS = {"templates", "examples", ".git", ".obsidian", "__pycache__"}


def slug(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^a-z0-9\s-]", "", ascii_value.lower())
    return re.sub(r"[\s-]+", "-", normalized).strip("-") or "section"


def default_scope(path: Path, metadata: dict[str, object]) -> str:
    declared = scalar(metadata, "retrieval_scope")
    if declared:
        return declared
    parts = {part.lower() for part in path.parts}
    role = scalar(metadata, "artifact_role")
    schema = scalar(metadata, "schema")
    if parts & EXCLUDED_PARTS or path.name.upper().startswith("TEMPLATE_") or role in {"template", "example", "generated"}:
        return "excluded_by_default"
    if "archive" in parts:
        return "search_only"
    if schema in {"fcvw/plan@1", "fcvw/plan@2", "fcvw/changelog@1", "fcvw/framework-release@1"}:
        return "exact_only"
    if role == "record" or parts & {"audits", "troubleshooting", "sessions", "regressions"}:
        return "search_only"
    return "routed"


def default_authority(metadata: dict[str, object]) -> str:
    declared = scalar(metadata, "authority")
    if declared:
        return declared
    role = scalar(metadata, "artifact_role")
    if role in {"framework_policy", "framework_lock"}:
        return "canonical"
    if role == "project_profile":
        return "routed"
    if role == "record":
        return "historical"
    if role in {"generated", "template", "example"}:
        return "generated"
    return "routed"


def sections(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    chunks: list[tuple[str, list[str]]] = []
    heading = "Document"
    content: list[str] = []
    fence = ""
    for line in lines:
        marker = FENCE.match(line)
        if marker:
            current = marker.group(1)
            if not fence:
                fence = current
            elif current[0] == fence[0] and len(current) >= len(fence):
                fence = ""
        match = None if fence else HEADING.match(line)
        if match:
            if any(item.strip() for item in content):
                chunks.append((heading, content))
            heading = match.group(2).strip()
            content = [line]
        else:
            content.append(line)
    if any(item.strip() for item in content):
        chunks.append((heading, content))
    return [(title, "\n".join(body).strip()) for title, body in chunks]


def build_index(root: Path, include_excluded: bool = False) -> list[dict[str, object]]:
    root = root.resolve()
    records: list[dict[str, object]] = []
    for path in sorted(root.rglob("*.md"), key=lambda item: item.as_posix().lower()):
        relative_path = path.relative_to(root)
        if any(part in {".git", ".obsidian", "__pycache__"} for part in relative_path.parts):
            continue
        text = path.read_text(encoding="utf-8-sig")
        result = parse_frontmatter(text)
        metadata = result.data
        scope = default_scope(relative_path, metadata)
        if scope == "excluded_by_default" and not include_excluded:
            continue
        slug_counts: dict[str, int] = {}
        for heading, content in sections(text):
            digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
            relative = relative_path.as_posix()
            base_slug = slug(heading)
            slug_counts[base_slug] = slug_counts.get(base_slug, 0) + 1
            chunk_slug = (
                base_slug
                if slug_counts[base_slug] == 1
                else f"{base_slug}-{slug_counts[base_slug]}"
            )
            records.append(
                {
                    "chunk_id": f"{relative}#{chunk_slug}",
                    "path": relative,
                    "heading": heading,
                    "schema": scalar(metadata, "schema"),
                    "artifact_role": scalar(metadata, "artifact_role"),
                    "authority": default_authority(metadata),
                    "language": scalar(metadata, "language"),
                    "retrieval_scope": scope,
                    "retrieval_priority": scalar(metadata, "retrieval_priority", "normal"),
                    "theme": scalar(metadata, "theme"),
                    "tags": string_list(metadata, "tags"),
                    "status": scalar(metadata, "status"),
                    "last_reviewed": scalar(metadata, "last_reviewed"),
                    "content_hash": f"sha256:{digest}",
                    "content": content,
                }
            )
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", required=True)
    parser.add_argument("--include-excluded", action="store_true")
    args = parser.parse_args()
    records = build_index(Path(args.root), args.include_excluded)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"FCVW context index: chunks={len(records)} output={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
