#!/usr/bin/env python3
"""Inspect durable FCVW plan dependencies and their validation evidence."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from frontmatter_fcvw import FrontmatterValue, parse_frontmatter, scalar, string_list


PLAN_ID = re.compile(r"^P[1-5]-R[1-5]-\d{4}-\d{2}-\d{2}-[a-z0-9-]+$")
PLAN_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
TABLE_SEPARATOR = re.compile(r"^:?-{3,}:?$")
DEPENDENCY_HEADING = "## Dependency validation"
DEPENDENCY_STATES = {"pending", "satisfied", "invalidated"}
EVIDENCE_NONE_VALUES = {"", "-", "none", "n/a", "not_applicable", "pending"}


@dataclass(frozen=True)
class DependencyFinding:
    rule: str
    path: str
    message: str


@dataclass(frozen=True)
class DependencyEvidence:
    dependency: str
    blocking_reason: str
    unblock_criteria: str
    status: str
    evidence: str


@dataclass(frozen=True)
class DependencySnapshot:
    catalog: dict[str, list[Path]]
    metadata: dict[str, dict[str, FrontmatterValue]]
    dependencies: dict[str, list[str]]
    evidence: dict[str, dict[str, DependencyEvidence]]
    findings: tuple[DependencyFinding, ...]


def _table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_dependency_evidence(
    text: str,
    relative: str,
) -> tuple[dict[str, DependencyEvidence], list[DependencyFinding]]:
    lines = text.splitlines()
    start = next((index for index, line in enumerate(lines) if line.strip() == DEPENDENCY_HEADING), None)
    if start is None:
        return {}, [DependencyFinding("plan-dependency-evidence", relative, "Dependency validation section is missing")]
    section: list[tuple[int, str]] = []
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            break
        section.append((index + 1, lines[index]))
    table_lines = [(line_number, line) for line_number, line in section if line.strip().startswith("|")]
    if not table_lines:
        return {}, [DependencyFinding("plan-dependency-evidence", relative, "dependency validation table is missing")]
    if len(table_lines) < 2 or len(_table_cells(table_lines[0][1])) != 5:
        return {}, [DependencyFinding("plan-dependency-evidence", relative, "dependency validation header is invalid")]
    separator = _table_cells(table_lines[1][1])
    if len(separator) != 5 or not all(TABLE_SEPARATOR.fullmatch(cell) for cell in separator):
        return {}, [DependencyFinding("plan-dependency-evidence", relative, "dependency validation separator is invalid")]

    evidence: dict[str, DependencyEvidence] = {}
    findings: list[DependencyFinding] = []
    for line_number, line in table_lines[2:]:
        cells = _table_cells(line)
        if len(cells) != 5:
            findings.append(DependencyFinding("plan-dependency-evidence", relative, f"invalid dependency row at line {line_number}"))
            continue
        dependency, reason, criteria, status, proof = cells
        dependency = dependency.strip("`")
        link = PLAN_LINK.fullmatch(dependency)
        if link:
            dependency = link.group(1).strip("`")
        status = status.strip("`").lower()
        if dependency in evidence:
            findings.append(DependencyFinding("plan-dependency-evidence", relative, f"duplicate dependency evidence: {dependency}"))
            continue
        if status not in DEPENDENCY_STATES:
            findings.append(
                DependencyFinding(
                    "plan-dependency-evidence",
                    relative,
                    f"invalid dependency status for {dependency}: {status or '<empty>'}",
                )
            )
        if len(reason.strip()) < 8 or len(criteria.strip()) < 8:
            findings.append(
                DependencyFinding(
                    "plan-dependency-evidence",
                    relative,
                    f"blocking reason and unblock criteria must be specific for {dependency}",
                )
            )
        evidence[dependency] = DependencyEvidence(dependency, reason, criteria, status, proof)
    return evidence, findings


def plan_catalog(plans_root: Path) -> dict[str, list[Path]]:
    catalog: dict[str, list[Path]] = {}
    for path in plans_root.glob("*/*.md"):
        if path.name not in {"README.md", "QUEUE.md", "INDEX.md"}:
            catalog.setdefault(path.stem, []).append(path)
    return catalog


def _dependency_cycles(graph: dict[str, list[str]]) -> list[list[str]]:
    cycles: set[tuple[str, ...]] = set()
    active: list[str] = []
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in active:
            body = active[active.index(node) :]
            rotations = [tuple(body[index:] + body[:index]) for index in range(len(body))]
            cycles.add(min(rotations) + (min(rotations)[0],))
            return
        if node in visited:
            return
        active.append(node)
        for dependency in graph.get(node, []):
            if dependency in graph:
                visit(dependency)
        active.pop()
        visited.add(node)

    for plan_id in graph:
        visit(plan_id)
    return [list(cycle) for cycle in sorted(cycles)]


def dependency_state(
    dependency: str,
    catalog: dict[str, list[Path]],
    evidence: dict[str, DependencyEvidence],
) -> tuple[str, str]:
    matches = catalog.get(dependency, [])
    if len(matches) != 1:
        return "invalid", "dependency is missing or ambiguous"
    prerequisite_status = scalar(parse_frontmatter(matches[0].read_text(encoding="utf-8-sig")).data, "status")
    record = evidence.get(dependency)
    if prerequisite_status == "completed":
        if record and record.status == "satisfied" and record.evidence.strip().lower() not in EVIDENCE_NONE_VALUES:
            return "satisfied", "completed prerequisite has validation evidence"
        return "pending", "completed prerequisite lacks satisfied validation evidence"
    if prerequisite_status == "discontinued":
        return "invalidated", "discontinued prerequisite remains blocking"
    return "pending", f"prerequisite status is {prerequisite_status or 'unknown'}"


def inspect_plan_dependencies(root: Path) -> DependencySnapshot:
    root = root.resolve()
    plans_root = root / "FCVW" / "Plans"
    catalog = plan_catalog(plans_root)
    metadata_by_id: dict[str, dict[str, FrontmatterValue]] = {}
    dependencies_by_id: dict[str, list[str]] = {}
    evidence_by_id: dict[str, dict[str, DependencyEvidence]] = {}
    findings: list[DependencyFinding] = []

    for plan_id, paths in sorted(catalog.items()):
        if len(paths) != 1:
            continue
        path = paths[0]
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8-sig")
        metadata = parse_frontmatter(text).data
        metadata_by_id[plan_id] = metadata
        raw_dependencies = metadata.get("depends_on")
        if raw_dependencies is None:
            dependencies_by_id[plan_id] = []
            continue
        if not isinstance(raw_dependencies, list):
            findings.append(DependencyFinding("plan-dependency-schema", relative, "depends_on must be a first-level list"))
        dependencies = string_list(metadata, "depends_on")
        dependencies_by_id[plan_id] = dependencies
        if len(dependencies) != len(set(dependencies)):
            findings.append(DependencyFinding("plan-dependency-schema", relative, "depends_on contains duplicate plan IDs"))
        if not dependencies:
            evidence_by_id[plan_id] = {}
            continue
        evidence, evidence_findings = parse_dependency_evidence(text, relative)
        evidence_by_id[plan_id] = evidence
        findings.extend(evidence_findings)
        for dependency in dependencies:
            if not PLAN_ID.fullmatch(dependency):
                findings.append(DependencyFinding("plan-dependency-schema", relative, f"invalid dependency plan ID: {dependency}"))
            if dependency == plan_id:
                findings.append(DependencyFinding("plan-dependency-cycle", relative, "plan depends on itself"))
            matches = catalog.get(dependency, [])
            if len(matches) != 1:
                findings.append(DependencyFinding("plan-dependency-schema", relative, f"dependency is missing or ambiguous: {dependency}"))
            record = evidence.get(dependency)
            if record is None:
                findings.append(DependencyFinding("plan-dependency-evidence", relative, f"dependency has no validation row: {dependency}"))
                continue
            if len(matches) != 1:
                continue
            prerequisite_status = scalar(parse_frontmatter(matches[0].read_text(encoding="utf-8-sig")).data, "status")
            if prerequisite_status in {"pending", "in_progress"} and record.status != "pending":
                findings.append(DependencyFinding("plan-dependency-evidence", relative, f"active prerequisite must remain pending: {dependency}"))
            if prerequisite_status == "discontinued" and (
                record.status != "invalidated" or record.evidence.strip().lower() in EVIDENCE_NONE_VALUES
            ):
                findings.append(
                    DependencyFinding(
                        "plan-dependency-evidence",
                        relative,
                        f"discontinued prerequisite requires invalidated status and evidence: {dependency}",
                    )
                )
            if record.status == "satisfied" and (
                prerequisite_status != "completed" or record.evidence.strip().lower() in EVIDENCE_NONE_VALUES
            ):
                findings.append(
                    DependencyFinding(
                        "plan-dependency-evidence",
                        relative,
                        f"satisfied dependency requires a completed plan and concrete evidence: {dependency}",
                    )
                )
        for extra in sorted(set(evidence) - set(dependencies)):
            findings.append(
                DependencyFinding("plan-dependency-evidence", relative, f"validation row is not declared in depends_on: {extra}")
            )

    for cycle in _dependency_cycles(dependencies_by_id):
        path = catalog[cycle[0]][0].relative_to(root).as_posix()
        findings.append(DependencyFinding("plan-dependency-cycle", path, f"dependency cycle: {' -> '.join(cycle)}"))
    for plan_id, dependencies in dependencies_by_id.items():
        if scalar(metadata_by_id.get(plan_id, {}), "status") != "completed":
            continue
        evidence = evidence_by_id.get(plan_id, {})
        unresolved = [item for item in dependencies if dependency_state(item, catalog, evidence)[0] != "satisfied"]
        if unresolved:
            path = catalog[plan_id][0].relative_to(root).as_posix()
            findings.append(
                DependencyFinding(
                    "plan-dependency-completion",
                    path,
                    f"completed plan has unresolved dependencies: {', '.join(unresolved)}",
                )
            )
    return DependencySnapshot(catalog, metadata_by_id, dependencies_by_id, evidence_by_id, tuple(findings))
