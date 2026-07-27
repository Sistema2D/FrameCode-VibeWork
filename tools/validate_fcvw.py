#!/usr/bin/env python3
"""Optional zero-dependency validator for FrameCode VibeWork."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from document_graph_fcvw import build_graph, render_catalog
from frontmatter_fcvw import FrontmatterValue, parse_frontmatter, scalar, string_list
from plan_queue_fcvw import validate_plan_queues

from urllib.parse import unquote


REQUIRED_PATHS = (
    "AGENTS.md",
    "README.md",
    "LICENSE",
    "NOTICE",
    "tools/test_validate_fcvw.py",
    "tools/test_open_issues.py",
    "tools/frontmatter_fcvw.py",
    "tools/document_graph_fcvw.py",
    "tools/plan_queue_fcvw.py",
    "tools/build_context_index.py",
    "tools/retrieve_context.py",
    "tools/locale_fcvw.py",
    "tools/package_release_fcvw.py",
    "FCVW/README.md",
    "FCVW/APP_RULES.md",
    "FCVW/DOCUMENT_GRAPH.md",
    "FCVW/Plans/pending/QUEUE.md",
    "FCVW/Plans/in_progress/QUEUE.md",
    "FCVW/FRAMEWORK_LOCK.md",
    "FCVW/OWNERSHIP.md",
    "FCVW/SCHEMAS.md",
    "FCVW/MIGRATIONS.md",
    "FCVW/PLANNING.md",
    "FCVW/CONTEXT_MAP.md",
    "FCVW/VERSIONING.md",
    "FCVW/RELEASE.md",
    "FCVW/MEMORY.md",
    "FCVW/AUTOMATION.md",
    "FCVW/REGRESSION_GUARDS.md",
    "FCVW/FILESYSTEM.md",
    "FCVW/governance/TEMPLATE_PLAN.md",
    "FCVW/governance/TEMPLATE_AUDIT.md",
    "FCVW/framework-releases/README.md",
    "FCVW/examples/minimal-change/README.md",
    "FCVW/skills/README.md",
    "FCVW/wiki/regressions/README.md",
    "FCVW/wiki/templates/TEMPLATE_REGRESSION.md",
)

PROJECT_PROFILES = (
    "BRIEFING.md",
    "DATA.md",
    "APP_RULES.md",
    "DESIGN.md",
    "ENVIRONMENT.md",
    "MANIFEST.md",
    "PERFORMANCE.md",
    "SCOPE.md",
    "SECURITY.md",
    "STACK.md",
    "WORKFLOW.md",
)

PLAN_FIELDS = (
    "id",
    "status",
    "priority",
    "risk",
    "created_at",
    "updated_at",
    "current_version",
    "expected_version",
    "owner",
    "context_files",
)

PLAN2_FIELDS = PLAN_FIELDS + ("regression_contract",)
PLAN_SCHEMAS = {"fcvw/plan@1", "fcvw/plan@2"}
PLAN_PRIORITIES = {f"P{index}" for index in range(1, 6)}
PLAN_RISKS = {f"R{index}" for index in range(1, 6)}
REGRESSION_CONTRACTS = {"required", "not_applicable"}
REGRESSION_MARKERS = (
    "### Existing behaviors that may be affected",
    "### Regression contracts consulted",
    "### Regression checks required",
    "### Regression evidence",
    "### Limitations and residual risk",
)
WIKI_TYPES = {
    "concept",
    "decision",
    "pattern",
    "failure",
    "regression",
    "refactoring",
    "audit",
    "agent",
    "release",
    "session",
    "component",
    "prompt",
    "question",
    "synthesis",
    "source",
    "raw",
}
WIKI_STATUSES = {"draft", "in_validation", "validated", "obsolete", "superseded", "contradictory"}
WIKI_CONFIDENCE = {"low", "medium", "high"}
REGRESSION_TYPES = {
    "functional",
    "interface",
    "data",
    "visual",
    "security",
    "ai",
    "governance",
    "documentation",
    "performance",
    "operations",
}
REGRESSION_STATUSES = {"detected", "mitigated", "resolved", "accepted", "superseded"}
FORBIDDEN_ROOT_ENTRIES = ("FCVW - Exemplo retirado de aplicação real",)
CLEAN_ROOT_ENTRIES = {
    ".cursorrules",
    ".git",
    ".github",
    ".gitignore",
    ".obsidian",
    ".windsurfrules",
    "AGENTS.md",
    "FCVW",
    "LICENSE",
    "NOTICE",
    "README.md",
    "tools",
}

SKILL_FIELDS = (
    "schema",
    "name",
    "description",
    "version",
    "trigger_keywords",
    "session_types",
)

SKILL_BODY_HEADINGS = {
    "purpose": ("## purpose",),
    "use conditions": ("## use conditions", "## use when", "## activation triggers", "## profiles", "## modes"),
    "non-responsibilities": (
        "## non-responsibilities",
        "## boundaries",
        "## block conditions",
        "## hard rules",
        "## non-negotiable rules",
        "## forbidden patterns",
        "## do not use for",
    ),
    "inputs": ("## inputs", "## mandatory source of truth", "## scan order", "## audit order", "## inspect order"),
    "procedure": (
        "## procedure",
        "## workflow",
        "## execution checklist",
        "## safe improvement sequence",
        "## curation loop",
        "## cleanup sequence",
        "## checks",
        "## core directives",
        "## decision ladder",
        "## hard gates",
        "## hygiene scan",
        "## fixed cost mode",
        "## scan order",
        "## audit order",
        "## inspect order",
    ),
    "required output": ("## required output", "## output required"),
    "validation": ("## validation", "## validation and exit", "## exit criteria", "## metrics", "## creation gate", "## improvement gate", "## hard gates"),
    "exit criteria": ("## exit criteria", "## validation and exit", "## definition of done", "## post-release checklist"),
}

PROVIDER_TERMS = (
    "IsSkillFile",
    "view_file",
    "AlmogBaku",
    "Superpowers methodology",
    "Spartan AI Toolkit",
)
PLAN_ID = re.compile(r"^P[1-5]-R[1-5]-\d{4}-\d{2}-\d{2}-[a-z0-9-]+$")
PLACEHOLDER = re.compile(r"<[A-Za-z][^>\n]*>")
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
INLINE_CODE = re.compile(r"`[^`]*`")
LOCAL_RELATIONSHIP_FIELDS = (
    "context_files",
    "sources",
    "related_plan",
    "related_release",
    "related",
    "supersedes",
    "superseded_by",
)
FRAMEWORK_RELEASE_FIELDS = (
    "version",
    "artifact_role",
    "owner",
    "upgrade_strategy",
    "record_scope",
    "date",
    "release_status",
    "release_type",
    "compatibility",
    "source_revision",
    "publication_revision",
    "release_languages",
    "related_plans",
)
FRAMEWORK_RELEASE_SECTIONS = (
    "Summary",
    "Related framework plans",
    "Framework surfaces added",
    "Framework surfaces changed",
    "Framework surfaces removed",
    "Ownership and path changes",
    "Schema changes",
    "Migration",
    "Validation",
    "Language-variant parity and review evidence",
    "Clean assets and package contents",
    "Checksums",
    "Downstream preservation rules",
    "Known gaps",
    "Rollback",
    "Publication evidence",
)
FRAMEWORK_RELEASE_SECTION_ALIASES = {
    "Language-variant parity and review evidence": ("Locale parity and language-review evidence",),
}
FRAMEWORK_RELEASE_LANGUAGES = {"pt-BR", "en-US", "es", "de"}


@dataclass(frozen=True)
class Finding:
    rule: str
    path: str
    message: str
    severity: str = "error"


@dataclass(frozen=True)
class BaselineEntry:
    path: str
    rule: str
    message: str
    justification: str
    owner: str
    review_due: date


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def frontmatter(text: str) -> dict[str, FrontmatterValue]:
    return parse_frontmatter(text).data


def normalized_finding_path(value: str) -> str:
    return value.strip().replace("\\", "/").removeprefix("./")


def load_legacy_baseline(path: Path) -> tuple[list[BaselineEntry], list[Finding]]:
    """Load a time-bounded exact-match baseline from the documented Markdown format."""
    label = path.as_posix()
    if not path.is_file():
        return [], [Finding("baseline-config", label, "baseline file is missing")]

    text = read_text(path)
    metadata = frontmatter(text)
    errors: list[Finding] = []
    if scalar(metadata, "schema") != "fcvw/legacy-baseline@1":
        errors.append(Finding("baseline-config", label, "invalid or missing baseline schema"))
    for field in ("created_at", "review_due", "owner"):
        if not scalar(metadata, field):
            errors.append(Finding("baseline-config", label, f"missing baseline metadata: {field}"))

    for field in ("created_at", "review_due"):
        value = scalar(metadata, field)
        if not value:
            continue
        try:
            parsed = date.fromisoformat(value)
        except ValueError:
            errors.append(Finding("baseline-config", label, f"invalid ISO date in {field}: {value}"))
            continue
        if field == "review_due" and parsed < date.today():
            errors.append(Finding("baseline-expired", label, f"baseline review expired on {value}"))

    entries: list[BaselineEntry] = []
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        cells = [cell.strip() for cell in stripped[1:-1].split("|")]
        if not cells or cells[0] == "Exact path" or all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        if len(cells) != 6 or not any(cells):
            errors.append(Finding("baseline-config", label, f"invalid baseline row at line {number}"))
            continue
        exact_path, rule, message, justification, owner, review_due = cells
        if not all((exact_path, rule, message, justification, owner, review_due)):
            errors.append(Finding("baseline-config", label, f"incomplete baseline row at line {number}"))
            continue
        try:
            due = date.fromisoformat(review_due)
        except ValueError:
            errors.append(Finding("baseline-config", label, f"invalid row review date at line {number}: {review_due}"))
            continue
        if due < date.today():
            errors.append(Finding("baseline-expired", label, f"row review expired at line {number} on {review_due}"))
            continue
        entries.append(
            BaselineEntry(
                path=normalized_finding_path(exact_path),
                rule=rule,
                message=message,
                justification=justification,
                owner=owner,
                review_due=due,
            )
        )

    if not entries:
        errors.append(Finding("baseline-config", label, "baseline has no valid exact findings"))
    return entries, errors


def apply_legacy_baseline(
    findings: list[Finding], entries: list[BaselineEntry]
) -> tuple[list[Finding], list[Finding], list[Finding]]:
    """Return blocking findings, accepted exact matches, and stale baseline warnings."""
    entry_keys = {(entry.path, entry.rule, entry.message) for entry in entries}
    matched: set[tuple[str, str, str]] = set()
    blocking: list[Finding] = []
    accepted: list[Finding] = []
    for finding in findings:
        key = (normalized_finding_path(finding.path), finding.rule, finding.message)
        if (
            finding.severity == "error"
            and finding.rule not in {"baseline-config", "baseline-expired"}
            and key in entry_keys
        ):
            accepted.append(finding)
            matched.add(key)
        else:
            blocking.append(finding)
    stale = [
        Finding(
            "baseline-stale",
            entry.path,
            f"baseline entry no longer matches an active finding: [{entry.rule}] {entry.message}",
            severity="warning",
        )
        for entry in entries
        if (entry.path, entry.rule, entry.message) not in matched
    ]
    return blocking, accepted, stale


def outside_code_fences(text: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    marker = ""
    for number, line in enumerate(text.splitlines(), 1):
        fence = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence:
            current = fence.group(1)
            if not marker:
                marker = current
            elif current[0] == marker[0] and len(current) >= len(marker):
                marker = ""
            continue
        if not marker:
            lines.append((number, line))
    return lines


def markdown_files(root: Path) -> list[Path]:
    return sorted((root / "FCVW").rglob("*.md"), key=lambda item: item.as_posix().lower())


def validate_required(root: Path, findings: list[Finding]) -> None:
    for relative in REQUIRED_PATHS:
        if not (root / relative).is_file():
            findings.append(Finding("required-path", relative, "required path is missing"))


def validate_canonical_metadata(root: Path, findings: list[Finding]) -> None:
    for path in sorted((root / "FCVW").glob("*.md")):
        relative = path.relative_to(root).as_posix()
        metadata = frontmatter(read_text(path))
        for field in ("schema", "artifact_role", "owner", "upgrade_strategy"):
            if field not in metadata:
                findings.append(Finding("canonical-metadata", relative, f"missing field: {field}"))


def validate_markdown(root: Path, findings: list[Finding]) -> None:
    for path in markdown_files(root):
        relative = path.relative_to(root).as_posix()
        text = read_text(path)
        marker = ""
        for line in text.splitlines():
            fence = re.match(r"^\s*(`{3,}|~{3,})", line)
            if not fence:
                continue
            current = fence.group(1)
            if not marker:
                marker = current
            elif current[0] == marker[0] and len(current) >= len(marker):
                marker = ""
        if marker:
            findings.append(Finding("markdown-fence", relative, f"unclosed Markdown fence: {marker}"))
        for line_number, line in outside_code_fences(text):
            code_ranges = [match.span() for match in INLINE_CODE.finditer(line)]
            for match in MARKDOWN_LINK.finditer(line):
                if any(start <= match.start() and match.end() <= end for start, end in code_ranges):
                    continue
                raw_target = match.group(1).strip()
                if raw_target.startswith("<") and ">" in raw_target:
                    target = raw_target[1:raw_target.find(">")]
                else:
                    target = raw_target.split(maxsplit=1)[0]
                target = target.split("#", 1)[0]
                if not target or target.startswith("#"):
                    continue
                target = unquote(target)
                if target.startswith("/") or re.match(r"^[A-Za-z]:[/\\]", target):
                    findings.append(
                        Finding(
                            "markdown-link-absolute",
                            relative,
                            f"line {line_number}: Markdown links must be source-relative: {target}",
                        )
                    )
                    continue
                if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                    continue
                candidate = path.parent / target
                if not candidate.exists():
                    findings.append(
                        Finding("markdown-link", relative, f"line {line_number}: missing target: {target}")
                    )


def level_two_section(text: str, title: str) -> str | None:
    lines = text.splitlines()
    start: int | None = None
    body: list[str] = []
    marker = ""
    heading = re.compile(rf"^##\s+{re.escape(title)}\s*$", re.I)
    next_heading = re.compile(r"^##\s+")
    for index, line in enumerate(lines):
        fence = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence:
            current = fence.group(1)
            if not marker:
                marker = current
            elif current[0] == marker[0] and len(current) >= len(marker):
                marker = ""
            continue
        if not marker:
            if start is None and heading.match(line.strip()):
                start = index + 1
                continue
            if start is not None and next_heading.match(line.strip()):
                return "\n".join(body).strip()
        if start is not None:
            body.append(line)
    if start is None:
        return None
    return "\n".join(body).strip()


def validate_plan_regression(
    relative: str,
    metadata: dict[str, FrontmatterValue],
    text: str,
    findings: list[Finding],
) -> None:
    if scalar(metadata, "schema") != "fcvw/plan@2":
        return
    contract = scalar(metadata, "regression_contract")
    if contract not in REGRESSION_CONTRACTS:
        findings.append(Finding("plan-regression", relative, f"invalid regression contract: {contract!r}"))
    section = level_two_section(text, "Regression impact")
    if section is None:
        findings.append(Finding("plan-regression", relative, "Regression impact section is missing"))
        return
    if not section or PLACEHOLDER.search(section):
        findings.append(Finding("plan-regression", relative, "Regression impact is empty or contains placeholders"))
    if contract == "required":
        for marker in REGRESSION_MARKERS:
            if marker.lower() not in section.lower():
                findings.append(Finding("plan-regression", relative, f"missing regression marker: {marker}"))
    elif contract == "not_applicable":
        justification = re.search(r"(?im)^Justification:\s*(.+)$", section)
        if not justification or len(justification.group(1).strip()) < 12:
            findings.append(Finding("plan-regression", relative, "not_applicable requires a specific Justification"))
    if scalar(metadata, "status") == "completed" and re.search(r"\bpending\b", section, re.I):
        findings.append(Finding("plan-regression", relative, "completed plan has pending regression evidence"))


def validate_plans(root: Path, findings: list[Finding]) -> None:
    plans_root = root / "FCVW" / "Plans"
    seen: dict[str, str] = {}
    for state in ("pending", "in_progress", "completed", "discontinued"):
        for path in sorted((plans_root / state).glob("*.md")):
            if path.name in {"README.md", "QUEUE.md", "INDEX.md"}:
                continue
            relative = path.relative_to(root).as_posix()
            text = read_text(path)
            metadata = frontmatter(text)
            plan_id = scalar(metadata, "id")
            status = scalar(metadata, "status")
            schema = scalar(metadata, "schema")
            if schema not in PLAN_SCHEMAS:
                findings.append(Finding("plan-schema", relative, "plan must use a supported FCVW plan schema"))
            required_fields = PLAN2_FIELDS if schema == "fcvw/plan@2" else PLAN_FIELDS
            for field in required_fields:
                if field not in metadata:
                    findings.append(Finding("plan-schema", relative, f"missing field: {field}"))
            scalar_fields = (
                "id",
                "status",
                "priority",
                "risk",
                "created_at",
                "updated_at",
                "current_version",
                "expected_version",
                "owner",
            )
            if schema == "fcvw/plan@2":
                scalar_fields += ("regression_contract",)
            for field in scalar_fields:
                if field in metadata and not scalar(metadata, field).strip():
                    findings.append(Finding("plan-schema", relative, f"field must be a non-empty scalar: {field}"))
            if "context_files" in metadata:
                context_files = metadata["context_files"]
                if not isinstance(context_files, list) or not context_files:
                    findings.append(Finding("plan-schema", relative, "context_files must be a non-empty list"))
            if status != state:
                findings.append(Finding("plan-state", relative, f"status {status!r} != directory {state!r}"))
            if not PLAN_ID.fullmatch(plan_id):
                findings.append(Finding("plan-id", relative, f"invalid plan id: {plan_id!r}"))
            priority = scalar(metadata, "priority")
            risk = scalar(metadata, "risk")
            if priority not in PLAN_PRIORITIES:
                findings.append(Finding("plan-priority", relative, f"invalid priority: {priority!r}"))
            if risk not in PLAN_RISKS:
                findings.append(Finding("plan-risk", relative, f"invalid risk: {risk!r}"))
            identity = re.match(r"^(P[1-5])-(R[1-5])-", plan_id)
            if identity and priority and identity.group(1) != priority:
                findings.append(Finding("plan-priority", relative, "priority does not match the plan ID"))
            if identity and risk and identity.group(2) != risk:
                findings.append(Finding("plan-risk", relative, "risk does not match the plan ID"))
            if path.stem != plan_id:
                findings.append(Finding("plan-filename", relative, "filename must equal plan id"))
            if plan_id in seen:
                findings.append(Finding("duplicate-id", relative, f"plan id also used by {seen[plan_id]}"))
            seen[plan_id] = relative
            validate_plan_regression(relative, metadata, text, findings)


def validate_skills(root: Path, findings: list[Finding]) -> None:
    skills_root = root / "FCVW" / "skills"
    catalog = read_text(skills_root / "README.md")
    seen: dict[str, str] = {}
    for path in sorted(skills_root.glob("*/SKILL.md")):
        relative = path.relative_to(root).as_posix()
        text = read_text(path)
        metadata = frontmatter(text)
        for field in SKILL_FIELDS:
            if field not in metadata:
                findings.append(Finding("skill-metadata", relative, f"missing field: {field}"))
        if scalar(metadata, "schema") != "fcvw/skill@1":
            findings.append(Finding("skill-schema", relative, "skill must use fcvw/skill@1"))
        name = scalar(metadata, "name")
        if name != path.parent.name:
            findings.append(Finding("skill-name", relative, "skill name must match directory"))
        if name in seen:
            findings.append(Finding("duplicate-id", relative, f"skill name also used by {seen[name]}"))
        seen[name] = relative
        if name not in catalog:
            findings.append(Finding("skill-catalog", relative, "skill is missing from catalog"))
        for term in PROVIDER_TERMS:
            if term in text:
                findings.append(Finding("provider-neutrality", relative, f"provider-specific core term: {term}"))
        headings = tuple(line.strip().lower() for line in text.splitlines() if line.startswith("## "))
        for concept, accepted in SKILL_BODY_HEADINGS.items():
            if not any(any(heading.startswith(marker) for marker in accepted) for heading in headings):
                findings.append(Finding("skill-contract", relative, f"missing body concept: {concept}"))


def declared_session_types(text: str) -> list[str]:
    return string_list(frontmatter(text), "session_types")


def validate_reading_routes(root: Path, findings: list[Finding]) -> None:
    context_path = root / "FCVW" / "CONTEXT_MAP.md"
    index_path = root / "FCVW" / "README.md"
    agents_path = root / "AGENTS.md"
    if not all(path.is_file() for path in (context_path, index_path, agents_path)):
        return
    context = read_text(context_path)
    fcvw_index = read_text(index_path)
    discoverability = "\n".join((read_text(agents_path), context, fcvw_index))
    for path in sorted((root / "FCVW").glob("*.md")):
        metadata = frontmatter(read_text(path))
        if scalar(metadata, "artifact_role") != "framework_policy":
            continue
        if path.name not in fcvw_index:
            findings.append(
                Finding(
                    "framework-index",
                    path.relative_to(root).as_posix(),
                    "framework policy is missing from the FCVW operational index",
                )
            )
        if path.name not in discoverability:
            findings.append(
                Finding(
                    "reading-route",
                    path.relative_to(root).as_posix(),
                    "framework policy is not discoverable from AGENTS.md, CONTEXT_MAP.md, or FCVW/README.md",
                )
            )
    for name in PROJECT_PROFILES:
        if (root / "FCVW" / name).is_file() and name not in fcvw_index:
            findings.append(
                Finding(
                    "framework-index",
                    f"FCVW/{name}",
                    "project profile is missing from the FCVW operational index",
                )
            )
    for path in sorted((root / "FCVW" / "skills").glob("*/SKILL.md")):
        relative = path.relative_to(root).as_posix()
        for session_type in declared_session_types(read_text(path)):
            if f"`{session_type}`" not in context:
                findings.append(
                    Finding(
                        "reading-route",
                        relative,
                        f"unmapped skill session type: {session_type}",
                    )
                )


def validate_wiki_ids(root: Path, findings: list[Finding]) -> None:
    wiki = root / "FCVW" / "wiki"
    seen: dict[str, str] = {}
    exempt = {"README.md", "index.md", "log.md", "metrics.md", "schema.md", "taxonomy.md"}
    for path in sorted(wiki.rglob("*.md")):
        if path.name in exempt or "templates" in path.parts:
            continue
        relative = path.relative_to(root).as_posix()
        metadata = frontmatter(read_text(path))
        page_id = scalar(metadata, "id")
        if not page_id:
            findings.append(Finding("wiki-id", relative, "knowledge page is missing a unique id"))
            continue
        if page_id in seen:
            findings.append(Finding("duplicate-id", relative, f"wiki id also used by {seen[page_id]}"))
        seen[page_id] = relative
        schema = scalar(metadata, "schema")
        if schema == "fcvw/wiki@1":
            required_scalars = (
                "id",
                "artifact_role",
                "owner",
                "upgrade_strategy",
                "record_scope",
                "retrieval_scope",
                "title",
                "type",
                "status",
                "confidence",
                "created_at",
                "last_reviewed",
            )
            for field in required_scalars:
                if not scalar(metadata, field):
                    findings.append(Finding("wiki-schema", relative, f"missing or empty field: {field}"))
            for field in ("sources", "tags"):
                if not isinstance(metadata.get(field), list) or not string_list(metadata, field):
                    findings.append(Finding("wiki-schema", relative, f"{field} must be a non-empty list"))
            if scalar(metadata, "artifact_role") != "record":
                findings.append(Finding("wiki-schema", relative, "artifact_role must be record"))
            if scalar(metadata, "upgrade_strategy") != "preserve":
                findings.append(Finding("wiki-schema", relative, "upgrade_strategy must be preserve"))
            if scalar(metadata, "record_scope") not in {"application", "framework"}:
                findings.append(Finding("wiki-schema", relative, "record_scope must be application or framework"))
            if scalar(metadata, "type") not in WIKI_TYPES:
                findings.append(Finding("wiki-schema", relative, f"invalid type: {scalar(metadata, 'type')!r}"))
            if scalar(metadata, "status") not in WIKI_STATUSES:
                findings.append(Finding("wiki-schema", relative, f"invalid status: {scalar(metadata, 'status')!r}"))
            if scalar(metadata, "confidence") not in WIKI_CONFIDENCE:
                findings.append(
                    Finding("wiki-schema", relative, f"invalid confidence: {scalar(metadata, 'confidence')!r}")
                )
        elif schema == "fcvw/regression@1":
            required_scalars = (
                "id",
                "artifact_role",
                "owner",
                "upgrade_strategy",
                "record_scope",
                "retrieval_scope",
                "title",
                "type",
                "severity",
                "status",
                "detected_at",
                "last_reviewed",
                "related_plan",
            )
            for field in required_scalars:
                if not scalar(metadata, field):
                    findings.append(Finding("regression-schema", relative, f"missing or empty field: {field}"))
            for field in ("sources", "tags"):
                if not isinstance(metadata.get(field), list) or not string_list(metadata, field):
                    findings.append(Finding("regression-schema", relative, f"{field} must be a non-empty list"))
            if scalar(metadata, "artifact_role") != "record":
                findings.append(Finding("regression-schema", relative, "artifact_role must be record"))
            if scalar(metadata, "upgrade_strategy") != "preserve":
                findings.append(Finding("regression-schema", relative, "upgrade_strategy must be preserve"))
            if scalar(metadata, "record_scope") not in {"application", "framework"}:
                findings.append(
                    Finding("regression-schema", relative, "record_scope must be application or framework")
                )
            if not re.fullmatch(r"REG-\d{8}-[a-z0-9-]+", page_id):
                findings.append(Finding("regression-schema", relative, f"invalid regression id: {page_id!r}"))
            if scalar(metadata, "type") not in REGRESSION_TYPES:
                findings.append(
                    Finding("regression-schema", relative, f"invalid type: {scalar(metadata, 'type')!r}")
                )
            if scalar(metadata, "severity") not in PLAN_RISKS:
                findings.append(
                    Finding("regression-schema", relative, f"invalid severity: {scalar(metadata, 'severity')!r}")
                )
            if scalar(metadata, "status") not in REGRESSION_STATUSES:
                findings.append(
                    Finding("regression-schema", relative, f"invalid status: {scalar(metadata, 'status')!r}")
                )
            related_plan = scalar(metadata, "related_plan")
            if related_plan and _find_plan_by_id(root, related_plan) is None:
                findings.append(
                    Finding("regression-schema", relative, f"related plan is missing or ambiguous: {related_plan}")
                )
        else:
            findings.append(Finding("wiki-schema", relative, f"unsupported knowledge schema: {schema!r}"))


def validate_audit_records(root: Path, findings: list[Finding]) -> None:
    audits = root / "FCVW" / "audits"
    seen_ids: dict[str, str] = {}
    for path in sorted(audits.glob("*.md")):
        if path.name == "README.md":
            continue
        relative = path.relative_to(root).as_posix()
        text = read_text(path)
        metadata = frontmatter(text)
        if scalar(metadata, "schema") != "fcvw/audit@1":
            findings.append(Finding("audit-schema", relative, "audit must use fcvw/audit@1"))
            continue
        for field in (
            "id",
            "artifact_role",
            "owner",
            "upgrade_strategy",
            "record_scope",
            "retrieval_scope",
            "status",
            "created_at",
            "last_reviewed",
        ):
            if not scalar(metadata, field):
                findings.append(Finding("audit-schema", relative, f"missing or empty field: {field}"))
        if not isinstance(metadata.get("sources"), list) or not string_list(metadata, "sources"):
            findings.append(Finding("audit-schema", relative, "sources must be a non-empty list"))
        if scalar(metadata, "artifact_role") != "record":
            findings.append(Finding("audit-schema", relative, "artifact_role must be record"))
        if scalar(metadata, "upgrade_strategy") != "preserve":
            findings.append(Finding("audit-schema", relative, "upgrade_strategy must be preserve"))
        audit_id = scalar(metadata, "id")
        if audit_id and not re.fullmatch(r"AUD-\d{8}-[a-z0-9-]+", audit_id):
            findings.append(Finding("audit-schema", relative, f"invalid audit id: {audit_id!r}"))
        if audit_id in seen_ids:
            findings.append(Finding("audit-schema", relative, f"audit id also used by {seen_ids[audit_id]}"))
        elif audit_id:
            seen_ids[audit_id] = relative
        if scalar(metadata, "record_scope") not in {"application", "framework"}:
            findings.append(Finding("audit-schema", relative, "record_scope must be application or framework"))
        if scalar(metadata, "status") not in {"draft", "completed", "blocked"}:
            findings.append(Finding("audit-schema", relative, f"invalid status: {scalar(metadata, 'status')!r}"))
        for section in (
            "Scope",
            "Authoritative sources",
            "Method",
            "Findings",
            "Validation",
            "Limitations and residual risk",
            "Follow-up",
        ):
            body = level_two_section(text, section)
            if body is None or not body.strip():
                findings.append(Finding("audit-schema", relative, f"missing or empty section: {section}"))


def validate_troubleshooting_records(root: Path, findings: list[Finding]) -> None:
    records = root / "FCVW" / "troubleshooting"
    seen_ids: dict[str, str] = {}
    for path in sorted(records.glob("*.md")):
        if path.name == "README.md":
            continue
        relative = path.relative_to(root).as_posix()
        text = read_text(path)
        metadata = frontmatter(text)
        schema = scalar(metadata, "schema")
        if not schema:
            continue
        if schema != "fcvw/troubleshooting@1":
            findings.append(
                Finding("troubleshooting-schema", relative, f"unsupported troubleshooting schema: {schema!r}")
            )
            continue
        required_scalars = (
            "id",
            "artifact_role",
            "owner",
            "upgrade_strategy",
            "record_scope",
            "retrieval_scope",
            "title",
            "type",
            "status",
            "confidence",
            "detected_at",
            "last_reviewed",
            "related_plan",
        )
        for field in required_scalars:
            if not scalar(metadata, field):
                findings.append(Finding("troubleshooting-schema", relative, f"missing or empty field: {field}"))
        for field in ("sources", "tags"):
            if not isinstance(metadata.get(field), list) or not string_list(metadata, field):
                findings.append(
                    Finding("troubleshooting-schema", relative, f"{field} must be a non-empty list")
                )
        record_id = scalar(metadata, "id")
        if record_id and not re.fullmatch(r"TRB-\d{8}-[a-z0-9-]+", record_id):
            findings.append(
                Finding("troubleshooting-schema", relative, f"invalid troubleshooting id: {record_id!r}")
            )
        if record_id in seen_ids:
            findings.append(
                Finding(
                    "troubleshooting-schema",
                    relative,
                    f"troubleshooting id also used by {seen_ids[record_id]}",
                )
            )
        elif record_id:
            seen_ids[record_id] = relative
        for field, expected in (
            ("artifact_role", "record"),
            ("upgrade_strategy", "preserve"),
            ("retrieval_scope", "search_only"),
            ("type", "failure"),
        ):
            if scalar(metadata, field) != expected:
                findings.append(Finding("troubleshooting-schema", relative, f"{field} must be {expected}"))
        if scalar(metadata, "record_scope") not in {"application", "framework"}:
            findings.append(
                Finding("troubleshooting-schema", relative, "record_scope must be application or framework")
            )
        if scalar(metadata, "status") not in {"draft", "in_validation", "validated", "obsolete"}:
            findings.append(
                Finding(
                    "troubleshooting-schema",
                    relative,
                    f"invalid status: {scalar(metadata, 'status')!r}",
                )
            )
        if scalar(metadata, "confidence") not in WIKI_CONFIDENCE:
            findings.append(
                Finding(
                    "troubleshooting-schema",
                    relative,
                    f"invalid confidence: {scalar(metadata, 'confidence')!r}",
                )
            )
        related_plan = scalar(metadata, "related_plan")
        if related_plan and not PLACEHOLDER.search(related_plan) and _find_plan_by_id(root, related_plan) is None:
            findings.append(
                Finding(
                    "troubleshooting-schema",
                    relative,
                    f"related plan is missing or ambiguous: {related_plan}",
                )
            )
        for section in (
            "1. Identification",
            "2. Symptom Description",
            "3. Hypotheses",
            "4. Root Cause",
            "5. Solution Applied",
            "6. Validation",
            "7. Prevention",
            "8. Wiki Promotion",
            "9. Status",
        ):
            body = level_two_section(text, section)
            if body is None or not body.strip() or PLACEHOLDER.search(body):
                findings.append(
                    Finding("troubleshooting-schema", relative, f"missing, empty, or unresolved section: {section}")
                )


def validate_profiles(root: Path, profile: str, findings: list[Finding]) -> None:
    for name in PROJECT_PROFILES:
        path = root / "FCVW" / name
        relative = path.relative_to(root).as_posix()
        if not path.is_file():
            findings.append(Finding("project-profile", relative, "project profile is missing"))
            continue
        text = read_text(path)
        metadata = frontmatter(text)
        if scalar(metadata, "artifact_role") != "project_profile":
            findings.append(Finding("ownership", relative, "profile must declare project_profile ownership"))
        if profile in {"instantiated", "strict", "incremental"}:
            if scalar(metadata, "instantiation_status") != "complete":
                findings.append(Finding("instantiation", relative, "profile is not complete"))
            if PLACEHOLDER.search(text):
                findings.append(Finding("placeholder", relative, "instantiated profile contains placeholders"))


def validate_clean_template(root: Path, findings: list[Finding]) -> None:
    fcvw = root / "FCVW"
    for name in FORBIDDEN_ROOT_ENTRIES:
        if (root / name).exists():
            findings.append(Finding("clean-contamination", name, "production-derived comparison fixture in project root"))
    for path in sorted(root.iterdir(), key=lambda item: item.name.lower()):
        if path.name not in CLEAN_ROOT_ENTRIES and path.name not in FORBIDDEN_ROOT_ENTRIES:
            findings.append(
                Finding(
                    "clean-contamination",
                    path.name,
                    "unexpected root entry in clean framework package",
                )
            )
    for folder in ("audits", "briefings", "troubleshooting"):
        for path in (fcvw / folder).glob("*.md"):
            if path.name == "README.md":
                continue
            if scalar(frontmatter(read_text(path)), "record_scope") != "framework":
                findings.append(
                    Finding(
                        "clean-contamination",
                        path.relative_to(root).as_posix(),
                        "non-framework record in clean baseline",
                    )
                )
    for path in (fcvw / "changelogs").rglob("*.md"):
        relative = path.relative_to(fcvw / "changelogs").as_posix()
        if relative != "unreleased/README.md":
            findings.append(Finding("clean-contamination", path.relative_to(root).as_posix(), "application changelog in clean baseline"))
    for state in ("pending", "in_progress", "completed", "discontinued"):
        for path in (fcvw / "Plans" / state).glob("*.md"):
            if path.name in {"README.md", "QUEUE.md", "INDEX.md"}:
                continue
            metadata = frontmatter(read_text(path))
            if scalar(metadata, "record_scope") != "framework":
                findings.append(Finding("clean-contamination", path.relative_to(root).as_posix(), "non-framework plan in clean baseline"))
    for path in (fcvw / "decisions").glob("*.md"):
        if path.name == "README.md":
            continue
        if scalar(frontmatter(read_text(path)), "record_scope") != "framework":
            findings.append(Finding("clean-contamination", path.relative_to(root).as_posix(), "non-framework decision in clean baseline"))
    wiki_exempt = {"README.md", "index.md", "log.md", "metrics.md", "schema.md", "taxonomy.md"}
    for path in (fcvw / "wiki").rglob("*.md"):
        if path.name in wiki_exempt or "templates" in path.parts:
            continue
        if scalar(frontmatter(read_text(path)), "record_scope") != "framework":
            findings.append(
                Finding(
                    "clean-contamination",
                    path.relative_to(root).as_posix(),
                    "non-framework knowledge record in clean baseline",
                )
            )
    for forbidden in ("FCVW/LICENSE", "FCVW/repository-open-graph-template.png"):
        if (root / forbidden).exists():
            findings.append(Finding("clean-contamination", forbidden, "duplicate/application artifact in clean baseline"))


def validate_regression_surfaces(root: Path, findings: list[Finding]) -> None:
    required_content = {
        "AGENTS.md": "FCVW/REGRESSION_GUARDS.md",
        "FCVW/REGRESSION_GUARDS.md": "# Regression guardrails",
        "FCVW/PLANNING.md": "fcvw/plan@2",
        "FCVW/TESTS.md": "## Minimum regression evidence by risk",
        "FCVW/GOVERNANCE_GATES.md": "| Regression |",
        "FCVW/WATCHERS.md": "## Regression-prone events",
        "FCVW/SCHEMAS.md": "fcvw/regression@1",
        "FCVW/governance/TEMPLATE_PLAN.md": "## Regression impact",
        "FCVW/wiki/templates/TEMPLATE_REGRESSION.md": "fcvw/regression@1",
        "FCVW/examples/minimal-change/plan.md": "## Regression impact",
    }
    for relative, marker in required_content.items():
        path = root / relative
        if path.is_file() and marker not in read_text(path):
            findings.append(Finding("regression-surface", relative, f"required marker is missing: {marker}"))


def _find_plan_by_id(root: Path, plan_id: str) -> Path | None:
    matches = list((root / "FCVW" / "Plans").glob(f"*/{plan_id}.md"))
    return matches[0] if len(matches) == 1 else None


def _validate_framework_release_record(root: Path, path: Path, findings: list[Finding]) -> str:
    relative = path.relative_to(root).as_posix()
    text = read_text(path)
    metadata = frontmatter(text)
    if scalar(metadata, "schema") != "fcvw/framework-release@1":
        findings.append(Finding("framework-release", relative, "invalid release schema"))
        return ""
    version = scalar(metadata, "version")
    status = scalar(metadata, "release_status")
    if path.stem != version:
        findings.append(Finding("framework-release", relative, "filename must match release version"))
    if status not in {"in_preparation", "ready", "published", "canceled"}:
        findings.append(Finding("framework-release", relative, "invalid release status"))
    current_record = scalar(metadata, "artifact_role") == "record"
    if status in {"in_preparation", "ready"} or current_record:
        for field in FRAMEWORK_RELEASE_FIELDS:
            value = metadata.get(field)
            if value is None or (isinstance(value, str) and not value.strip()) or (isinstance(value, list) and not value):
                findings.append(Finding("framework-release", relative, f"missing or empty release field: {field}"))
        if scalar(metadata, "release_type") not in {"patch", "minor", "major"}:
            findings.append(Finding("framework-release", relative, "invalid release_type"))
        if scalar(metadata, "compatibility") not in {"backward_compatible", "migration_required", "breaking"}:
            findings.append(Finding("framework-release", relative, "invalid compatibility"))
        if current_record:
            for field, expected in (
                ("owner", "framework"),
                ("upgrade_strategy", "preserve"),
                ("record_scope", "framework"),
            ):
                if scalar(metadata, field) != expected:
                    findings.append(Finding("framework-release", relative, f"{field} must be {expected}"))
        for section in FRAMEWORK_RELEASE_SECTIONS:
            accepted_sections = (section, *FRAMEWORK_RELEASE_SECTION_ALIASES.get(section, ()))
            body = next(
                (
                    candidate_body
                    for candidate in accepted_sections
                    if (candidate_body := level_two_section(text, candidate)) is not None
                ),
                None,
            )
            if body is None or not body.strip():
                findings.append(Finding("framework-release", relative, f"missing or empty section: {section}"))
    related_plans = string_list(metadata, "related_plans")
    for plan_id in related_plans:
        plan = _find_plan_by_id(root, plan_id)
        if plan is None:
            findings.append(Finding("framework-release", relative, f"related plan is missing or ambiguous: {plan_id}"))
            continue
        if status == "published" and scalar(frontmatter(read_text(plan)), "status") != "completed":
            findings.append(Finding("framework-release", relative, f"published release has incomplete plan: {plan_id}"))
    if status in {"ready", "published"} and current_record:
        source_revision = scalar(metadata, "source_revision")
        if not re.fullmatch(r"[0-9a-fA-F]{40}", source_revision):
            findings.append(
                Finding("framework-release", relative, f"{status} release requires a 40-character source revision")
            )
    if status in {"in_preparation", "ready"} and current_record:
        if scalar(metadata, "publication_revision") != "UNPUBLISHED":
            findings.append(
                Finding(
                    "framework-release",
                    relative,
                    f"{status} release must keep publication_revision as UNPUBLISHED",
                )
            )
    if status == "published" and current_record:
        source_revision = scalar(metadata, "source_revision")
        publication_revision = scalar(metadata, "publication_revision")
        if not re.fullmatch(r"[0-9a-fA-F]{40}", publication_revision):
            findings.append(
                Finding("framework-release", relative, "published release requires a 40-character publication revision")
            )
        elif source_revision == publication_revision:
            findings.append(
                Finding(
                    "framework-release",
                    relative,
                    "source_revision and publication_revision must identify different lifecycle commits",
                )
            )
        languages = set(string_list(metadata, "release_languages"))
        if languages != FRAMEWORK_RELEASE_LANGUAGES:
            findings.append(
                Finding(
                    "framework-release",
                    relative,
                    "published language-specific release must contain pt-BR, en-US, es, and de assets",
                )
            )
        assets = level_two_section(text, "Clean assets and package contents") or ""
        expected_assets = {
            language: f"FrameCode-VibeWork-{version}-{language}.zip"
            for language in FRAMEWORK_RELEASE_LANGUAGES
        }
        missing_assets = [name for name in expected_assets.values() if name not in assets]
        if missing_assets:
            findings.append(
                Finding(
                    "framework-release",
                    relative,
                    f"published release is missing language assets: {', '.join(sorted(missing_assets))}",
                )
            )
        checksums = level_two_section(text, "Checksums") or ""
        asset_hashes: dict[str, str] = {}
        for language, asset_name in expected_assets.items():
            line = next((item for item in checksums.splitlines() if asset_name in item), "")
            match = re.search(r"\b[0-9a-fA-F]{64}\b", line)
            if match:
                asset_hashes[language] = match.group(0).lower()
        missing_checksums = sorted(FRAMEWORK_RELEASE_LANGUAGES - set(asset_hashes))
        if missing_checksums:
            findings.append(
                Finding(
                    "framework-release",
                    relative,
                    "published release requires one SHA-256 checksum per language-specific asset; "
                    f"missing: {', '.join(missing_checksums)}",
                )
            )
        elif len(set(asset_hashes.values())) != len(asset_hashes):
            findings.append(
                Finding(
                    "framework-release",
                    relative,
                    "language-specific assets must not reuse an identical SHA-256 checksum",
                )
            )
        publication = level_two_section(text, "Publication evidence") or ""
        if not re.search(r"https://github\.com/[^/\s]+/[^/\s]+/releases/tag/[^\s)]+", publication):
            findings.append(
                Finding(
                    "framework-release",
                    relative,
                    "published release requires a GitHub Release URL",
                )
            )
    return status


def validate_version(root: Path, findings: list[Finding]) -> None:
    lock_text = read_text(root / "FCVW" / "FRAMEWORK_LOCK.md")
    match = re.search(r"Installed version.*?(V\d+\.\d+\.\d+)", lock_text)
    version = match.group(1) if match else ""
    state_match = re.search(r"Release state.*?`([^`]+)`", lock_text)
    lock_state = state_match.group(1) if state_match else ""
    if not version:
        findings.append(Finding("framework-version", "FCVW/FRAMEWORK_LOCK.md", "installed version not found"))
        return
    if version not in read_text(root / "README.md"):
        findings.append(Finding("framework-version", "README.md", f"README does not reference {version}"))
    release_path = root / "FCVW" / "framework-releases" / f"{version}.md"
    if not release_path.is_file():
        findings.append(Finding("framework-release", release_path.relative_to(root).as_posix(), "release record missing"))
    else:
        release_metadata = frontmatter(read_text(release_path))
        if scalar(release_metadata, "schema") != "fcvw/framework-release@1":
            findings.append(Finding("framework-release", release_path.relative_to(root).as_posix(), "invalid release schema"))
        if scalar(release_metadata, "version") != version:
            findings.append(Finding("framework-release", release_path.relative_to(root).as_posix(), "version does not match framework lock"))
        release_status = scalar(release_metadata, "release_status")
        if lock_state not in {"ready", "published"}:
            findings.append(
                Finding(
                    "framework-version",
                    "FCVW/FRAMEWORK_LOCK.md",
                    "release state must be ready or published",
                )
            )
        if release_status != lock_state:
            findings.append(
                Finding(
                    "framework-release",
                    release_path.relative_to(root).as_posix(),
                    "framework lock state must match its release record",
                )
            )
    active_records: list[tuple[Path, str]] = []
    for candidate in sorted((root / "FCVW" / "framework-releases").glob("V*.md")):
        status = _validate_framework_release_record(root, candidate, findings)
        if status in {"in_preparation", "ready"}:
            active_records.append((candidate, status))
    if len(active_records) > 1:
        findings.append(
            Finding(
                "framework-release",
                "FCVW/framework-releases",
                f"multiple releases are active candidates: {', '.join(path.name for path, _ in active_records)}",
            )
        )
    ready_records = [path for path, status in active_records if status == "ready"]
    if ready_records and (lock_state != "ready" or ready_records[0].stem != version):
        findings.append(
            Finding(
                "framework-version",
                "FCVW/FRAMEWORK_LOCK.md",
                f"ready candidate {ready_records[0].stem} must be the ready framework lock",
            )
        )
    preparing_records = [path for path, status in active_records if status == "in_preparation"]
    if preparing_records and lock_state != "published":
        findings.append(
            Finding(
                "framework-version",
                "FCVW/FRAMEWORK_LOCK.md",
                "an in_preparation candidate requires the installed lock to remain published",
            )
        )
    if (root / "FCVW" / "changelogs" / f"{version}.md").exists():
        findings.append(Finding("version-namespace", f"FCVW/changelogs/{version}.md", "framework release in application namespace"))


def validate_application_releases(root: Path, findings: list[Finding]) -> None:
    changelogs = root / "FCVW" / "changelogs"
    for path in sorted(changelogs.rglob("*.md")):
        if path.name == "README.md":
            continue
        relative = path.relative_to(root).as_posix()
        text = read_text(path)
        metadata = frontmatter(text)
        if scalar(metadata, "schema") != "fcvw/changelog@1":
            findings.append(Finding("application-release", relative, "invalid application release schema"))
            continue
        for field in ("version", "date", "release_status", "release_type"):
            if not scalar(metadata, field):
                findings.append(Finding("application-release", relative, f"missing or empty field: {field}"))
        if not isinstance(metadata.get("related_plans"), list) or not string_list(metadata, "related_plans"):
            findings.append(Finding("application-release", relative, "related_plans must be a non-empty list"))
        status = scalar(metadata, "release_status")
        if status not in {"unreleased", "in_preparation", "published", "canceled"}:
            findings.append(Finding("application-release", relative, f"invalid release_status: {status!r}"))
        if scalar(metadata, "release_type") not in {"patch", "minor", "major"}:
            findings.append(
                Finding("application-release", relative, f"invalid release_type: {scalar(metadata, 'release_type')!r}")
            )
        role = scalar(metadata, "artifact_role")
        if role == "record":
            for field in ("owner", "external_publication", "source_revision", "publication_revision"):
                if not scalar(metadata, field):
                    findings.append(Finding("application-release", relative, f"record field is required: {field}"))
            if scalar(metadata, "upgrade_strategy") != "preserve":
                findings.append(Finding("application-release", relative, "record upgrade_strategy must be preserve"))
            if scalar(metadata, "record_scope") != "application":
                findings.append(Finding("application-release", relative, "record_scope must be application"))
            if not isinstance(metadata.get("release_languages"), list) or not string_list(
                metadata,
                "release_languages",
            ):
                findings.append(Finding("application-release", relative, "release_languages must be a non-empty list"))
            source_revision = scalar(metadata, "source_revision")
            if source_revision and source_revision != "not_applicable" and not re.fullmatch(
                r"[0-9a-fA-F]{40}",
                source_revision,
            ):
                findings.append(
                    Finding(
                        "application-release",
                        relative,
                        "source_revision must be a 40-character revision or not_applicable",
                    )
                )
            publication_revision = scalar(metadata, "publication_revision")
            if publication_revision and publication_revision not in {"UNPUBLISHED", "not_applicable"} and not re.fullmatch(
                r"[0-9a-fA-F]{40}",
                publication_revision,
            ):
                findings.append(
                    Finding(
                        "application-release",
                        relative,
                        "publication_revision must be a 40-character revision, UNPUBLISHED, or not_applicable",
                    )
                )
        for section in ("Summary", "Validation", "Known gaps", "Rollback"):
            body = level_two_section(text, section)
            if body is None or not body.strip():
                findings.append(Finding("application-release", relative, f"missing or empty section: {section}"))
        if level_two_section(text, "Affected areas") is None and not any(
            level_two_section(text, section) is not None for section in ("Added", "Changed", "Fixed", "Removed")
        ):
            findings.append(
                Finding(
                    "application-release",
                    relative,
                    "release requires Affected areas or Added/Changed/Fixed/Removed sections",
                )
            )
        if role == "record":
            for section in (
                "Security and data impact",
                "Migration",
                "Assets and package contents",
                "Checksums",
                "Publication evidence",
                "Post-release validation",
            ):
                body = level_two_section(text, section)
                if body is None or not body.strip():
                    findings.append(
                        Finding("application-release", relative, f"missing or empty section: {section}")
                    )
        for plan_id in string_list(metadata, "related_plans"):
            plan = _find_plan_by_id(root, plan_id)
            if plan is None:
                findings.append(
                    Finding("application-release", relative, f"related plan is missing or ambiguous: {plan_id}")
                )
                continue
            if status == "published" and scalar(frontmatter(read_text(plan)), "status") != "completed":
                findings.append(
                    Finding("application-release", relative, f"published release has incomplete plan: {plan_id}")
                )
        external = scalar(metadata, "external_publication")
        if external and external not in {"not_applicable", "pending", "published"}:
            findings.append(
                Finding("application-release", relative, f"invalid external_publication: {external!r}")
            )
        if external == "published":
            if not re.fullmatch(r"[0-9a-fA-F]{40}", scalar(metadata, "publication_revision")):
                findings.append(
                    Finding(
                        "application-release",
                        relative,
                        "externally published release requires a 40-character publication revision",
                    )
                )
            publication = level_two_section(text, "Publication evidence") or ""
            if not re.search(r"https?://[^\s)]+", publication):
                findings.append(
                    Finding("application-release", relative, "external publication requires an evidence URL")
                )


def _looks_like_local_relationship(field: str, value: str) -> bool:
    if field == "context_files":
        return True
    if re.match(r"^[a-z][a-z0-9+.-]*:", value, re.I):
        return False
    return (
        value.startswith((".", "/"))
        or "/" in value
        or "\\" in value
        or value.lower().endswith(".md")
    )


def _relationship_candidate(root: Path, source: Path, value: str) -> Path | None:
    target = unquote(value.strip().strip("<>")).split("#", 1)[0]
    if not target or PLACEHOLDER.search(target):
        return None
    target = target.replace("\\", "/")
    if target.startswith("/"):
        return root / target.lstrip("/")
    if target.startswith(("FCVW/", "AGENTS.md", "README.md")):
        return root / target
    return source.parent / target


def validate_frontmatter_documents(root: Path, findings: list[Finding]) -> None:
    roles = {"framework_policy", "framework_lock", "project_profile", "template", "record", "generated", "example"}
    strategies = {"replace", "replace_with_migration", "preserve", "regenerate", "merge"}
    retrieval_scopes = {"always", "routed", "search_only", "exact_only", "excluded_by_default"}
    authorities = {"canonical", "routed", "historical", "generated"}
    retrieval_priorities = {"high", "normal", "low"}
    paths = sorted(
        {*(root.glob("*.md")), *markdown_files(root)},
        key=lambda item: item.relative_to(root).as_posix().lower(),
    )
    for path in paths:
        relative = path.relative_to(root).as_posix()
        text = read_text(path)
        result = parse_frontmatter(text)
        for issue in result.issues:
            findings.append(Finding("frontmatter", relative, f"line {issue.line}: {issue.message}"))
        metadata = result.data
        if not metadata:
            continue
        role = scalar(metadata, "artifact_role")
        strategy = scalar(metadata, "upgrade_strategy")
        scope = scalar(metadata, "retrieval_scope")
        authority = scalar(metadata, "authority")
        retrieval_priority = scalar(metadata, "retrieval_priority")
        if role and role not in roles:
            findings.append(Finding("frontmatter-role", relative, f"invalid artifact_role: {role}"))
        if strategy and strategy not in strategies:
            findings.append(Finding("frontmatter-upgrade", relative, f"invalid upgrade_strategy: {strategy}"))
        if scope and scope not in retrieval_scopes:
            findings.append(Finding("frontmatter-retrieval", relative, f"invalid retrieval_scope: {scope}"))
        if authority and authority not in authorities:
            findings.append(Finding("frontmatter-retrieval", relative, f"invalid authority: {authority}"))
        expected_authority = {
            "framework_policy": "canonical",
            "framework_lock": "canonical",
            "project_profile": "routed",
            "record": "historical",
            "generated": "generated",
            "template": "generated",
            "example": "generated",
        }.get(role)
        if authority and expected_authority and authority != expected_authority:
            findings.append(
                Finding(
                    "frontmatter-retrieval",
                    relative,
                    f"{role} artifacts cannot elevate or change authority from {expected_authority}",
                )
            )
        if retrieval_priority and retrieval_priority not in retrieval_priorities:
            findings.append(
                Finding("frontmatter-retrieval", relative, f"invalid retrieval_priority: {retrieval_priority}")
            )
        if role in {"generated", "template", "example"} and scope and scope != "excluded_by_default":
            findings.append(
                Finding("frontmatter-retrieval", relative, f"{role} artifacts cannot elevate retrieval_scope")
            )
        if role == "generated" and strategy and strategy != "regenerate":
            findings.append(Finding("frontmatter-ownership", relative, "generated artifacts must use regenerate"))
        template_surface = path.name.upper().startswith("TEMPLATE_") or role in {"template", "example"} or any(
            part.lower() in {"templates", "examples"} for part in path.relative_to(root).parts
        )
        if template_surface:
            continue
        historical_legacy = (
            not role
            and "Plans" in path.relative_to(root).parts
            and any(state in path.relative_to(root).parts for state in ("completed", "discontinued"))
        )
        for field in ("created_at", "updated_at", "last_reviewed", "detected_at", "date"):
            value = scalar(metadata, field)
            if value:
                try:
                    date.fromisoformat(value)
                except ValueError:
                    findings.append(Finding("frontmatter-date", relative, f"invalid ISO date in {field}: {value}"))
        for field in LOCAL_RELATIONSHIP_FIELDS:
            if field not in metadata:
                continue
            raw_value = metadata[field]
            if field == "context_files" and not isinstance(raw_value, list):
                findings.append(Finding("frontmatter-list", relative, "context_files must be a first-level list"))
                continue
            values = string_list(metadata, field)
            normalized = [normalized_finding_path(item) for item in values]
            if not historical_legacy and len(normalized) != len(set(normalized)):
                findings.append(Finding("frontmatter-relationship", relative, f"{field} contains duplicates"))
            for target in dict.fromkeys(normalized):
                if not target or not _looks_like_local_relationship(field, target):
                    continue
                candidate = _relationship_candidate(root, path, target)
                if candidate is None:
                    continue
                try:
                    resolved = candidate.resolve()
                    resolved.relative_to(root.resolve())
                except (ValueError, OSError):
                    findings.append(
                        Finding("frontmatter-relationship", relative, f"{field} escapes repository root: {target}")
                    )
                    continue
                if not resolved.exists():
                    findings.append(
                        Finding("frontmatter-relationship", relative, f"{field} target is missing: {target}")
                    )


def validate_document_graph(root: Path, findings: list[Finding]) -> None:
    graph = build_graph(root)
    findings.extend(Finding(item.rule, item.path, item.message, item.severity) for item in graph.findings)
    catalog = root / "FCVW" / "DOCUMENT_GRAPH.md"
    if catalog.is_file() and read_text(catalog) != render_catalog(root, catalog):
        findings.append(
            Finding(
                "document-catalog-stale",
                "FCVW/DOCUMENT_GRAPH.md",
                "generated catalog does not match the current Markdown filesystem",
            )
        )


def validate_queues(root: Path, findings: list[Finding]) -> None:
    findings.extend(Finding(item.rule, item.path, item.message) for item in validate_plan_queues(root))


def validate_app_rules(root: Path, profile: str, findings: list[Finding]) -> None:
    path = root / "FCVW" / "APP_RULES.md"
    relative = "FCVW/APP_RULES.md"
    if not path.is_file():
        return
    text = read_text(path)
    metadata = frontmatter(text)
    if scalar(metadata, "schema") != "fcvw/app-rules@1":
        findings.append(Finding("app-rules-schema", relative, "invalid or missing APP_RULES schema"))
    if scalar(metadata, "artifact_role") != "project_profile":
        findings.append(Finding("app-rules-ownership", relative, "APP_RULES must be a project_profile"))
    instantiation_status = scalar(metadata, "instantiation_status")
    if instantiation_status not in {"pending", "complete"}:
        findings.append(Finding("app-rules-status", relative, "instantiation_status must be pending or complete"))
    prose_lines = [line for _, line in outside_code_fences(text)]
    prose = "\n".join(prose_lines)
    matches = list(re.finditer(r"(?m)^##\s+(APP-RULE-\d{3,})\b[^\n]*$", prose))
    identifiers = [match.group(1) for match in matches]
    if len(identifiers) != len(set(identifiers)):
        findings.append(Finding("app-rules-id", relative, "APP_RULES contains duplicate rule IDs"))
    if profile in {"instantiated", "strict", "incremental"} and instantiation_status == "complete":
        if not identifiers:
            findings.append(Finding("app-rules-empty", relative, "completed APP_RULES has no application rules"))
        required_sections = (
            "Status",
            "Rule",
            "Affected components",
            "Rationale and expected behavior",
            "Exceptions",
            "Related records",
        )
        for index, match in enumerate(matches):
            rule_id = match.group(1)
            end = matches[index + 1].start() if index + 1 < len(matches) else len(prose)
            block = prose[match.end():end]
            sections = {
                title.lower(): body.strip()
                for title, body in re.findall(
                    r"(?ms)^###\s+([^\n]+)\n(.*?)(?=^###\s+|\Z)",
                    block,
                )
            }
            for section in required_sections:
                body = sections.get(section.lower(), "")
                if not body or PLACEHOLDER.search(body):
                    findings.append(
                        Finding("app-rules-contract", relative, f"{rule_id} has missing or empty section: {section}")
                    )
            status_body = sections.get("status", "").splitlines()
            status = status_body[0].strip().lower() if status_body else ""
            if status not in {"active", "deprecated", "superseded"}:
                findings.append(Finding("app-rules-contract", relative, f"{rule_id} has invalid status: {status!r}"))
            for section in ("affected components", "related records"):
                body = sections.get(section, "")
                if body and not MARKDOWN_LINK.search(body):
                    findings.append(
                        Finding("app-rules-contract", relative, f"{rule_id} section must contain a Markdown link: {section}")
                    )
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument(
        "--profile",
        choices=("clean-template", "instantiated", "incremental", "strict"),
        default="clean-template",
    )
    parser.add_argument(
        "--baseline",
        help="legacy baseline Markdown file; valid only with --profile incremental",
    )
    args = parser.parse_args()
    root = Path(args.root).resolve()
    findings: list[Finding] = []
    baseline_entries: list[BaselineEntry] = []
    accepted: list[Finding] = []

    if args.baseline and args.profile != "incremental":
        findings.append(
            Finding(
                "baseline-config",
                args.baseline,
                "--baseline is valid only with --profile incremental",
            )
        )
    elif args.baseline:
        baseline_path = Path(args.baseline)
        if not baseline_path.is_absolute():
            baseline_path = root / baseline_path
        baseline_entries, baseline_errors = load_legacy_baseline(baseline_path.resolve())
        findings.extend(baseline_errors)

    validate_required(root, findings)
    if not (root / "FCVW").is_dir():
        for finding in findings:
            print(f"ERROR [{finding.rule}] {finding.path}: {finding.message}")
        return 1

    validate_markdown(root, findings)
    validate_frontmatter_documents(root, findings)
    validate_queues(root, findings)
    validate_document_graph(root, findings)
    validate_canonical_metadata(root, findings)
    validate_plans(root, findings)
    validate_skills(root, findings)
    validate_reading_routes(root, findings)
    validate_wiki_ids(root, findings)
    validate_audit_records(root, findings)
    validate_troubleshooting_records(root, findings)
    validate_profiles(root, args.profile, findings)
    validate_app_rules(root, args.profile, findings)
    validate_version(root, findings)
    validate_application_releases(root, findings)
    validate_regression_surfaces(root, findings)
    if args.profile == "clean-template":
        validate_clean_template(root, findings)

    if args.profile == "incremental" and baseline_entries:
        findings, accepted, stale = apply_legacy_baseline(findings, baseline_entries)
        findings.extend(stale)

    errors = [item for item in findings if item.severity == "error"]
    for finding in accepted:
        print(f"BASELINE [{finding.rule}] {finding.path}: {finding.message}")
    for finding in findings:
        print(f"{finding.severity.upper()} [{finding.rule}] {finding.path}: {finding.message}")
    print(
        f"FCVW validation: profile={args.profile} errors={len(errors)} "
        f"findings={len(findings)} baseline={len(accepted)}"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
