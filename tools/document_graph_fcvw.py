#!/usr/bin/env python3
"""Build and validate the portable Markdown graph used by FCVW and Obsidian."""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import quote, unquote

from frontmatter_fcvw import parse_frontmatter, scalar
from fcvw_cache import frontmatter as cache_frontmatter, read_text as cache_read_text


MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
MALFORMED_MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]\n]+\]\s+\(([^)\n]+)\)")
MALFORMED_ATX_HEADING = re.compile(r"^\s*#{1,6}[^#\s]")
MALFORMED_TASK_ITEM = re.compile(r"^\s*[-+*]\s+\[\](?:\s|$)")
WIKILINK = re.compile(r"(?<!!)\[\[([^\]]+)\]\]")
FENCE = re.compile(r"^\s*(```+|~~~+)")
EXTERNAL = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)
INLINE_CODE = re.compile(r"`[^`]*`")
DEFAULT_ENTRYPOINTS = ("AGENTS.md", "README.md", "FCVW/README.md")
NON_AUTHORITATIVE_RELATIONSHIPS = {"FCVW/DOCUMENT_GRAPH.md"}
ORPHAN_EXCEPTION_FIELDS = ("orphan_reason", "orphan_owner", "orphan_review_due")


@dataclass(frozen=True)
class GraphFinding:
    rule: str
    path: str
    message: str
    severity: str = "error"


@dataclass(frozen=True)
class DocumentGraph:
    nodes: tuple[str, ...]
    outgoing: dict[str, tuple[str, ...]]
    incoming: dict[str, tuple[str, ...]]
    entrypoints: tuple[str, ...]
    findings: tuple[GraphFinding, ...]


def _outside_fences(text: str) -> list[str]:
    result: list[str] = []
    marker = ""
    for line in text.splitlines():
        fence = FENCE.match(line)
        if fence:
            current = fence.group(1)
            if not marker:
                marker = current
            elif current[0] == marker[0] and len(current) >= len(marker):
                marker = ""
            continue
        if not marker:
            result.append(line)
    return result


def markdown_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    for path in root.rglob("*.md"):
        relative = path.relative_to(root)
        if any(part in {".git", ".obsidian", ".codex-test-tmp", "__pycache__"} for part in relative.parts):
            continue
        paths.append(path)
    return sorted(paths, key=lambda item: item.relative_to(root).as_posix().lower())


def _link_destination(raw_target: str) -> str:
    value = raw_target.strip()
    if value.startswith("<"):
        closing = value.find(">")
        if closing >= 0:
            return value[1:closing]
    return value.split(maxsplit=1)[0]


def _candidate(root: Path, source: Path, raw_target: str, *, vault_relative: bool = False) -> Path | None:
    target = unquote(_link_destination(raw_target))
    target = target.split("#", 1)[0]
    if not target or target.startswith("#"):
        return None
    if re.match(r"^[A-Za-z]:[/\\]", target):
        return Path("__outside_root__") / target.replace("\\", "/")
    if EXTERNAL.match(target):
        return None
    target = target.replace("\\", "/")
    if target.startswith("/"):
        if vault_relative:
            candidate = root / target.lstrip("/")
        else:
            return Path("__outside_root__") / target.lstrip("/")
    elif vault_relative and target.startswith("FCVW/"):
        candidate = root / target
    else:
        candidate = source.parent / target
    if candidate.suffix and candidate.suffix.lower() != ".md":
        return None
    if not candidate.suffix:
        if candidate.is_file():
            return None
        markdown = candidate.with_suffix(".md")
        candidate = markdown if markdown.exists() else candidate / "README.md"
    # `root` is already resolved by the caller, and Markdown link targets are
    # portable repository paths rather than filesystem links. Normalising the
    # path lexically therefore gives the same answer as `Path.resolve()` while
    # avoiding two filesystem round trips for every link in the repository.
    try:
        normalized = Path(os.path.normpath(candidate))
        normalized.relative_to(root)
        return normalized
    except (ValueError, OSError):
        return Path("__outside_root__") / target


def _wikilink_target(value: str) -> str:
    target = value.split("|", 1)[0].strip()
    return target


def _validated_orphan_exception(
    metadata: dict[str, object],
    relative: str,
    findings: list[GraphFinding],
) -> bool:
    if scalar(metadata, "orphan_policy") != "allowed":
        return False
    missing = [field for field in ORPHAN_EXCEPTION_FIELDS if not scalar(metadata, field)]
    if missing:
        findings.append(
            GraphFinding(
                "document-orphan-exception",
                relative,
                f"orphan exception is missing: {', '.join(missing)}",
            )
        )
        return False
    review_due = scalar(metadata, "orphan_review_due")
    try:
        due = date.fromisoformat(review_due)
    except ValueError:
        findings.append(
            GraphFinding("document-orphan-exception", relative, f"invalid orphan_review_due: {review_due}")
        )
        return False
    if due < date.today():
        findings.append(
            GraphFinding("document-orphan-exception", relative, f"orphan exception expired on {review_due}")
        )
        return False
    return True


def build_graph(root: Path) -> DocumentGraph:
    root = root.resolve()
    files = markdown_files(root)
    node_set = {path.relative_to(root).as_posix() for path in files}
    outgoing_mutable: dict[str, set[str]] = defaultdict(set)
    findings: list[GraphFinding] = []

    for path in files:
        relative = path.relative_to(root).as_posix()
        text = cache_read_text(path)
        lines = _outside_fences(text)
        targets: list[tuple[str, bool]] = []
        for line in lines:
            code_ranges = [match.span() for match in INLINE_CODE.finditer(line)]
            if MALFORMED_ATX_HEADING.match(line):
                findings.append(
                    GraphFinding(
                        "document-heading-syntax",
                        relative,
                        f"ATX heading marker must be followed by whitespace: {line.strip()}",
                    )
                )
            if MALFORMED_TASK_ITEM.match(line):
                findings.append(
                    GraphFinding(
                        "document-task-list-syntax",
                        relative,
                        f"task-list marker must contain a space, x, or X: {line.strip()}",
                    )
                )
            for match in MALFORMED_MARKDOWN_LINK.finditer(line):
                if not any(start <= match.start() and match.end() <= end for start, end in code_ranges):
                    findings.append(
                        GraphFinding(
                            "document-link-syntax",
                            relative,
                            f"Markdown link has whitespace before its destination: {match.group(1)}",
                        )
                    )
            for match in MARKDOWN_LINK.finditer(line):
                if not any(start <= match.start() and match.end() <= end for start, end in code_ranges):
                    targets.append((match.group(1), False))
            for match in WIKILINK.finditer(line):
                if not any(start <= match.start() and match.end() <= end for start, end in code_ranges):
                    targets.append((_wikilink_target(match.group(1)), True))
        for target, vault_relative in targets:
            candidate = _candidate(root, path, target, vault_relative=vault_relative)
            if candidate is None:
                continue
            try:
                normalized = candidate.relative_to(root).as_posix()
            except ValueError:
                findings.append(GraphFinding("document-link-outside-root", relative, f"target escapes root: {target}"))
                continue
            if normalized not in node_set:
                findings.append(GraphFinding("document-link", relative, f"missing Markdown target: {target}"))
                continue
            outgoing_mutable[relative].add(normalized)

    incoming_mutable: dict[str, set[str]] = defaultdict(set)
    for source, targets in outgoing_mutable.items():
        for target in targets:
            incoming_mutable[target].add(source)

    entrypoints = tuple(path for path in DEFAULT_ENTRYPOINTS if path in node_set)
    reachable: set[str] = set(entrypoints)
    queue: deque[str] = deque(entrypoints)
    while queue:
        source = queue.popleft()
        for target in outgoing_mutable.get(source, set()):
            if target not in reachable:
                reachable.add(target)
                queue.append(target)

    for path in files:
        relative = path.relative_to(root).as_posix()
        metadata = cache_frontmatter(path)
        allowed = _validated_orphan_exception(metadata, relative, findings)
        if relative not in entrypoints and not incoming_mutable.get(relative) and not allowed:
            findings.append(GraphFinding("document-orphan", relative, "Markdown artifact has no incoming link"))
        if relative not in reachable and not allowed:
            findings.append(
                GraphFinding("document-unreachable", relative, "Markdown artifact is unreachable from an official entrypoint")
            )
        if outgoing_mutable.get(relative) == {relative}:
            findings.append(GraphFinding("document-self-only", relative, "artifact links only to itself"))
        role = scalar(metadata, "artifact_role")
        authoritative = set(outgoing_mutable.get(relative, set())) - NON_AUTHORITATIVE_RELATIONSHIPS - {relative}
        if role in {"generated", "record"} and not authoritative and not allowed:
            findings.append(
                GraphFinding(
                    "document-source-link",
                    relative,
                    f"{role} artifact has no outgoing authoritative relationship",
                )
            )

    return DocumentGraph(
        nodes=tuple(sorted(node_set)),
        outgoing={key: tuple(sorted(value)) for key, value in outgoing_mutable.items()},
        incoming={key: tuple(sorted(value)) for key, value in incoming_mutable.items()},
        entrypoints=entrypoints,
        findings=tuple(sorted(findings, key=lambda item: (item.path, item.rule, item.message))),
    )


def render_catalog(root: Path, catalog: Path) -> str:
    root = root.resolve()
    catalog = catalog.resolve()
    groups: dict[str, list[str]] = defaultdict(list)
    for path in markdown_files(root):
        relative = path.relative_to(root).as_posix()
        if path == catalog:
            continue
        group = relative.rsplit("/", 1)[0] if "/" in relative else "Repository root"
        groups[group].append(relative)

    lines = [
        "---",
        'schema: "fcvw/document-graph@1"',
        'artifact_role: "generated"',
        'owner: "framework"',
        'upgrade_strategy: "regenerate"',
        f'last_reviewed: "{date.today().isoformat()}"',
        "---",
        "",
        "# Document graph catalog",
        "",
        "Generated navigation for governed Markdown artifacts. The physical files and their canonical contracts remain authoritative.",
        "",
    ]
    for group in sorted(groups, key=str.lower):
        lines.extend((f"## {group}", ""))
        for relative in sorted(groups[group], key=str.lower):
            link = Path(os.path.relpath(root / relative, start=catalog.parent))
            lines.append(f"- [`{relative}`]({quote(link.as_posix())})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--catalog", default="FCVW/DOCUMENT_GRAPH.md")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"ERROR [document-root] {root}: root directory is missing")
        return 1
    catalog = (root / args.catalog).resolve()
    try:
        catalog.relative_to(root)
    except ValueError:
        print(f"ERROR [document-catalog] {catalog}: catalog must remain inside the root")
        return 1
    if args.write:
        catalog.parent.mkdir(parents=True, exist_ok=True)
        catalog.write_text(render_catalog(root, catalog), encoding="utf-8")
    graph = build_graph(root)
    for finding in graph.findings:
        print(f"{finding.severity.upper()} [{finding.rule}] {finding.path}: {finding.message}")
    print(
        f"FCVW document graph: nodes={len(graph.nodes)} entrypoints={len(graph.entrypoints)} "
        f"findings={len(graph.findings)}"
    )
    return 1 if any(item.severity == "error" for item in graph.findings) else 0


if __name__ == "__main__":
    sys.exit(main())
