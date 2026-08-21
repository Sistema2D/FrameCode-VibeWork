#!/usr/bin/env python3
"""Build and validate the disposable FCVW typed knowledge graph."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

from frontmatter_fcvw import FrontmatterValue, parse_frontmatter, scalar, string_list
from knowledge_sources_fcvw import dependent_review_findings, review_date_findings, validate_source_page


TYPED_RELATION_FIELDS = (
    "related",
    "depends_on",
    "supports",
    "contradicts",
    "implements",
    "derived_from",
    "invalidates",
    "supersedes",
    "superseded_by",
    "canonical_page",
)
RELATION_INVERSES = {
    "related": "related",
    "depends_on": "required_by",
    "supports": "supported_by",
    "contradicts": "contradicts",
    "implements": "implemented_by",
    "derived_from": "source_for",
    "invalidates": "invalidated_by",
    "supersedes": "superseded_by",
    "superseded_by": "supersedes",
    "canonical_page": "canonical_for",
}
KNOWLEDGE_MATURITY = {"hypothesis", "provisional", "established", "disputed"}
EXTERNAL_SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)


@dataclass(frozen=True)
class KnowledgeFinding:
    rule: str
    path: str
    message: str
    severity: str = "error"


@dataclass(frozen=True)
class KnowledgeGraph:
    nodes: tuple[dict[str, object], ...]
    edges: tuple[dict[str, object], ...]
    findings: tuple[KnowledgeFinding, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "schema": "fcvw/knowledge-graph@1",
            "authority_notice": "Derived from governed Markdown; source artifacts remain authoritative.",
            "nodes": list(self.nodes),
            "edges": list(self.edges),
        }


def _metadata_files(root: Path) -> list[tuple[Path, dict[str, FrontmatterValue]]]:
    records: list[tuple[Path, dict[str, FrontmatterValue]]] = []
    for path in sorted(root.rglob("*.md"), key=lambda item: item.as_posix().lower()):
        if any(part in {".git", ".obsidian", ".fcvw-cache", "__pycache__"} for part in path.parts):
            continue
        metadata = parse_frontmatter(path.read_text(encoding="utf-8-sig")).data
        if metadata:
            records.append((path, metadata))
    return records


def _relationship_values(metadata: dict[str, FrontmatterValue], field: str) -> list[str]:
    return string_list(metadata, field)


def _candidate(root: Path, source: Path, value: str) -> Path | None:
    target = unquote(value.strip().strip("<>")).split("#", 1)[0]
    if not target or EXTERNAL_SCHEME.match(target):
        return None
    target = target.replace("\\", "/")
    if target.startswith("/"):
        return root / target.lstrip("/")
    if target.startswith(("FCVW/", "AGENTS.md", "README.md")):
        return root / target
    return source.parent / target


def _resolve_target(
    root: Path,
    source: Path,
    value: str,
    ids: dict[str, list[Path]],
) -> tuple[Path | None, str]:
    matches = ids.get(value, [])
    if len(matches) == 1:
        return matches[0], "id"
    if len(matches) > 1:
        return None, "ambiguous_id"
    candidate = _candidate(root, source, value)
    if candidate is None:
        return None, "external_or_invalid"
    try:
        resolved = candidate.resolve()
        resolved.relative_to(root)
    except (OSError, ValueError):
        return None, "outside_root"
    if not resolved.is_file() or resolved.suffix.lower() != ".md":
        return None, "missing_markdown"
    return resolved, "path"


def _node(
    root: Path,
    path: Path,
    metadata: dict[str, FrontmatterValue],
    *,
    referenced_only: bool = False,
) -> dict[str, object]:
    relative = path.relative_to(root).as_posix()
    authority = scalar(metadata, "authority")
    if not authority:
        authority = {
            "framework_policy": "canonical",
            "framework_lock": "canonical",
            "project_profile": "routed",
            "record": "historical",
            "generated": "generated",
            "template": "generated",
            "example": "generated",
        }.get(scalar(metadata, "artifact_role"), "routed")
    return {
        "id": scalar(metadata, "id", relative),
        "path": relative,
        "schema": scalar(metadata, "schema"),
        "type": scalar(metadata, "type", "artifact" if referenced_only else "knowledge"),
        "status": scalar(metadata, "status"),
        "confidence": scalar(metadata, "confidence"),
        "maturity": scalar(metadata, "maturity"),
        "authority": authority,
        "sources": string_list(metadata, "sources"),
        "source_digest": scalar(metadata, "source_digest"),
        "referenced_only": referenced_only,
    }


def _cycles(edges: list[dict[str, object]], relation: str) -> list[list[str]]:
    graph: dict[str, list[str]] = {}
    for edge in edges:
        if edge["relation"] == relation and not edge["derived"]:
            graph.setdefault(str(edge["source_path"]), []).append(str(edge["target_path"]))
    found: set[tuple[str, ...]] = set()
    active: list[str] = []
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in active:
            cycle = active[active.index(node) :] + [node]
            body = cycle[:-1]
            rotations = [tuple(body[index:] + body[:index]) for index in range(len(body))]
            found.add(min(rotations) + (min(rotations)[0],))
            return
        if node in visited:
            return
        active.append(node)
        for target in graph.get(node, []):
            visit(target)
        active.pop()
        visited.add(node)

    for node in graph:
        visit(node)
    return [list(item) for item in sorted(found)]


def build_knowledge_graph(root: Path) -> KnowledgeGraph:
    root = root.resolve()
    metadata_files = _metadata_files(root)
    metadata_by_path = {path.resolve(): metadata for path, metadata in metadata_files}
    ids: dict[str, list[Path]] = {}
    wiki_pages: list[tuple[Path, dict[str, FrontmatterValue]]] = []
    findings: list[KnowledgeFinding] = []
    for path, metadata in metadata_files:
        artifact_id = scalar(metadata, "id")
        if artifact_id:
            ids.setdefault(artifact_id, []).append(path.resolve())
        if scalar(metadata, "schema") in {"fcvw/wiki@1", "fcvw/regression@1"}:
            wiki_pages.append((path.resolve(), metadata))

    nodes: dict[str, dict[str, object]] = {}
    edges: list[dict[str, object]] = []
    explicit: set[tuple[str, str, str]] = set()
    stale_sources: set[str] = set()

    for path, metadata in wiki_pages:
        relative = path.relative_to(root).as_posix()
        nodes[relative] = _node(root, path, metadata)
        maturity = scalar(metadata, "maturity")
        if maturity and maturity not in KNOWLEDGE_MATURITY:
            findings.append(KnowledgeFinding("knowledge-maturity", relative, f"invalid maturity: {maturity}"))

        source_stale, source_findings = validate_source_page(root, path, metadata)
        if source_stale:
            stale_sources.add(relative)
        findings.extend(
            KnowledgeFinding(item.rule, item.path, item.message, item.severity)
            for item in source_findings
        )

        for field in TYPED_RELATION_FIELDS:
            raw_value = metadata.get(field)
            if raw_value is None:
                continue
            if field == "canonical_page" and not isinstance(raw_value, str):
                findings.append(KnowledgeFinding("knowledge-relation", relative, "canonical_page must be a scalar"))
            if field != "canonical_page" and not isinstance(raw_value, list):
                findings.append(
                    KnowledgeFinding("knowledge-relation", relative, f"{field} must be a first-level list")
                )
            values = _relationship_values(metadata, field)
            if len(values) != len(set(values)):
                findings.append(KnowledgeFinding("knowledge-relation", relative, f"{field} contains duplicates"))
            for value in values:
                target, resolution = _resolve_target(root, path, value, ids)
                if target is None:
                    findings.append(
                        KnowledgeFinding(
                            "knowledge-relation-target",
                            relative,
                            f"{field} target cannot be resolved ({resolution}): {value}",
                        )
                    )
                    continue
                target_relative = target.relative_to(root).as_posix()
                if target_relative == relative:
                    findings.append(KnowledgeFinding("knowledge-relation-self", relative, f"self relation: {field}"))
                    continue
                target_metadata = metadata_by_path.get(target, {})
                nodes.setdefault(target_relative, _node(root, target, target_metadata, referenced_only=True))
                key = (relative, field, target_relative)
                if key in explicit:
                    continue
                explicit.add(key)
                source_id = str(nodes[relative]["id"])
                target_id = str(nodes[target_relative]["id"])
                edges.append(
                    {
                        "source": source_id,
                        "source_path": relative,
                        "relation": field,
                        "target": target_id,
                        "target_path": target_relative,
                        "derived": False,
                    }
                )
                inverse = RELATION_INVERSES[field]
                edges.append(
                    {
                        "source": target_id,
                        "source_path": target_relative,
                        "relation": inverse,
                        "target": source_id,
                        "target_path": relative,
                        "derived": True,
                    }
                )

    explicit_pairs = {(str(e["source_path"]), str(e["relation"]), str(e["target_path"])) for e in edges if not e["derived"]}
    for source, relation, target in sorted(explicit_pairs):
        inverse = RELATION_INVERSES.get(relation)
        if inverse and (target, inverse, source) in explicit_pairs:
            findings.append(
                KnowledgeFinding(
                    "knowledge-relation-redundant-inverse",
                    source,
                    f"explicit inverse is redundant because it is derived: {relation} -> {target}",
                    "warning",
                )
            )
        if relation == "supports" and (source, "invalidates", target) in explicit_pairs:
            findings.append(
                KnowledgeFinding("knowledge-relation-conflict", source, f"both supports and invalidates: {target}")
            )
        if relation == "supports" and (source, "contradicts", target) in explicit_pairs:
            findings.append(
                KnowledgeFinding(
                    "knowledge-relation-conflict",
                    source,
                    f"both supports and contradicts: {target}",
                    "warning",
                )
            )
    for cycle in _cycles(edges, "supersedes"):
        findings.append(
            KnowledgeFinding("knowledge-relation-cycle", cycle[0], f"supersedes cycle: {' -> '.join(cycle)}")
        )

    source_findings = [*dependent_review_findings(edges, stale_sources), *review_date_findings(root, wiki_pages)]
    findings.extend(
        KnowledgeFinding(item.rule, item.path, item.message, item.severity)
        for item in source_findings
    )

    return KnowledgeGraph(
        tuple(nodes[path] for path in sorted(nodes)),
        tuple(sorted(edges, key=lambda item: (str(item["source_path"]), str(item["relation"]), str(item["target_path"]), bool(item["derived"])))),
        tuple(findings),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", help="write derived graph JSON to a disposable path")
    parser.add_argument("--review-output", help="write warning-only review candidates as JSON")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    graph = build_knowledge_graph(root)
    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(graph.as_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.review_output:
        review = Path(args.review_output)
        if not review.is_absolute():
            review = root / review
        review.parent.mkdir(parents=True, exist_ok=True)
        warnings = [finding.__dict__ for finding in graph.findings if finding.severity == "warning"]
        review.write_text(json.dumps(warnings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for finding in graph.findings:
        print(f"{finding.severity.upper()} [{finding.rule}] {finding.path}: {finding.message}")
    errors = [finding for finding in graph.findings if finding.severity == "error"]
    print(f"FCVW knowledge graph: nodes={len(graph.nodes)} edges={len(graph.edges)} errors={len(errors)} findings={len(graph.findings)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
