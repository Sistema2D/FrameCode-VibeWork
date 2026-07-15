#!/usr/bin/env python3
"""Optional zero-dependency validator for FrameCode VibeWork."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import unquote


REQUIRED_PATHS = (
    "AGENTS.md",
    "README.md",
    "LICENSE",
    "NOTICE",
    "tools/test_validate_fcvw.py",
    "FCVW/README.md",
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
    "FCVW/framework-releases/README.md",
    "FCVW/examples/minimal-change/README.md",
    "FCVW/skills/README.md",
    "FCVW/wiki/regressions/README.md",
    "FCVW/wiki/templates/TEMPLATE_REGRESSION.md",
)

PROJECT_PROFILES = (
    "BRIEFING.md",
    "DATA.md",
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
REGRESSION_CONTRACTS = {"required", "not_applicable"}
REGRESSION_MARKERS = (
    "### Existing behaviors that may be affected",
    "### Regression contracts consulted",
    "### Regression checks required",
    "### Regression evidence",
    "### Limitations and residual risk",
)
FORBIDDEN_ROOT_ENTRIES = ("FCVW - Exemplo retirado de aplicação real",)
CLEAN_ROOT_ENTRIES = {
    ".cursorrules",
    ".git",
    ".github",
    ".gitignore",
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
BACKTICK_FENCE = chr(96) * 3
PLAN_ID = re.compile(r"^P[1-5]-R[1-5]-\d{4}-\d{2}-\d{2}-[a-z0-9-]+$")
PLACEHOLDER = re.compile(r"<[A-Za-z][^>\n]*>")
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


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


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    lines = text.splitlines()
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}
    result: dict[str, str] = {}
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if match:
            key, value = match.groups()
            result[key] = value.strip().strip("\"'")
    return result


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
    if metadata.get("schema") != "fcvw/legacy-baseline@1":
        errors.append(Finding("baseline-config", label, "invalid or missing baseline schema"))
    for field in ("created_at", "review_due", "owner"):
        if not metadata.get(field):
            errors.append(Finding("baseline-config", label, f"missing baseline metadata: {field}"))

    for field in ("created_at", "review_due"):
        value = metadata.get(field)
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
    in_fence = False
    marker = ""
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.lstrip()
        if stripped.startswith((BACKTICK_FENCE, "~~~")):
            current = stripped[:3]
            if not in_fence:
                in_fence, marker = True, current
            elif current == marker:
                in_fence, marker = False, ""
            continue
        if not in_fence:
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
        if sum(1 for line in text.splitlines() if line.lstrip().startswith(BACKTICK_FENCE)) % 2:
            findings.append(Finding("markdown-fence", relative, "unbalanced triple-backtick fence"))
        for line_number, line in outside_code_fences(text):
            for match in MARKDOWN_LINK.finditer(line):
                target = match.group(1).strip().strip("<>")
                target = target.split(maxsplit=1)[0].split("#", 1)[0]
                if not target or re.match(r"^[a-z]+://", target, re.I) or target.startswith(("mailto:", "#")):
                    continue
                target = unquote(target)
                if re.match(r"^[A-Za-z]:[/\\]", target):
                    continue
                candidate = (root / target) if target.startswith("FCVW/") else (path.parent / target)
                if not candidate.exists():
                    findings.append(
                        Finding("markdown-link", relative, f"line {line_number}: missing target: {target}")
                    )


def level_two_section(text: str, title: str) -> str | None:
    lines = text.splitlines()
    start: int | None = None
    heading = re.compile(rf"^##\s+{re.escape(title)}\s*$", re.I)
    next_heading = re.compile(r"^##\s+")
    for index, line in enumerate(lines):
        if start is None and heading.match(line.strip()):
            start = index + 1
            continue
        if start is not None and next_heading.match(line.strip()):
            return "\n".join(lines[start:index]).strip()
    if start is None:
        return None
    return "\n".join(lines[start:]).strip()


def validate_plan_regression(
    relative: str,
    metadata: dict[str, str],
    text: str,
    findings: list[Finding],
) -> None:
    if metadata.get("schema") != "fcvw/plan@2":
        return
    contract = metadata.get("regression_contract", "")
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
    if metadata.get("status") == "completed" and re.search(r"\bpending\b", section, re.I):
        findings.append(Finding("plan-regression", relative, "completed plan has pending regression evidence"))


def validate_plans(root: Path, findings: list[Finding]) -> None:
    plans_root = root / "FCVW" / "Plans"
    seen: dict[str, str] = {}
    for state in ("pending", "in_progress", "completed", "discontinued"):
        for path in sorted((plans_root / state).glob("*.md")):
            if path.name == "README.md":
                continue
            relative = path.relative_to(root).as_posix()
            text = read_text(path)
            metadata = frontmatter(text)
            plan_id = metadata.get("id", "")
            status = metadata.get("status", "")
            schema = metadata.get("schema", "")
            if schema not in PLAN_SCHEMAS:
                findings.append(Finding("plan-schema", relative, "plan must use a supported FCVW plan schema"))
            required_fields = PLAN2_FIELDS if schema == "fcvw/plan@2" else PLAN_FIELDS
            for field in required_fields:
                if field not in metadata:
                    findings.append(Finding("plan-schema", relative, f"missing field: {field}"))
            if status != state:
                findings.append(Finding("plan-state", relative, f"status {status!r} != directory {state!r}"))
            if not PLAN_ID.fullmatch(plan_id):
                findings.append(Finding("plan-id", relative, f"invalid plan id: {plan_id!r}"))
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
        if metadata.get("schema") != "fcvw/skill@1":
            findings.append(Finding("skill-schema", relative, "skill must use fcvw/skill@1"))
        name = metadata.get("name", "")
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
    values: list[str] = []
    capture = False
    for line in text.splitlines():
        if line.startswith("session_types:"):
            capture = True
            continue
        if capture and re.match(r"^\S", line):
            break
        if capture:
            match = re.match(r"\s+-\s+[\"']?([^\"']+)", line)
            if match:
                values.append(match.group(1).strip())
    return values


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
        if metadata.get("artifact_role") != "framework_policy":
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
        page_id = metadata.get("id")
        if not page_id:
            findings.append(Finding("wiki-id", relative, "knowledge page is missing a unique id"))
            continue
        if page_id in seen:
            findings.append(Finding("duplicate-id", relative, f"wiki id also used by {seen[page_id]}"))
        seen[page_id] = relative


def validate_profiles(root: Path, profile: str, findings: list[Finding]) -> None:
    for name in PROJECT_PROFILES:
        path = root / "FCVW" / name
        relative = path.relative_to(root).as_posix()
        if not path.is_file():
            findings.append(Finding("project-profile", relative, "project profile is missing"))
            continue
        text = read_text(path)
        metadata = frontmatter(text)
        if metadata.get("artifact_role") != "project_profile":
            findings.append(Finding("ownership", relative, "profile must declare project_profile ownership"))
        if profile in {"instantiated", "strict", "incremental"}:
            if metadata.get("instantiation_status") != "complete":
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
            if path.name != "README.md":
                findings.append(Finding("clean-contamination", path.relative_to(root).as_posix(), "project record in clean baseline"))
    for path in (fcvw / "changelogs").rglob("*.md"):
        relative = path.relative_to(fcvw / "changelogs").as_posix()
        if relative != "unreleased/README.md":
            findings.append(Finding("clean-contamination", path.relative_to(root).as_posix(), "application changelog in clean baseline"))
    for state in ("pending", "in_progress", "completed", "discontinued"):
        for path in (fcvw / "Plans" / state).glob("*.md"):
            if path.name == "README.md":
                continue
            metadata = frontmatter(read_text(path))
            if metadata.get("record_scope") != "framework":
                findings.append(Finding("clean-contamination", path.relative_to(root).as_posix(), "non-framework plan in clean baseline"))
    for path in (fcvw / "decisions").glob("*.md"):
        if path.name == "README.md":
            continue
        if frontmatter(read_text(path)).get("record_scope") != "framework":
            findings.append(Finding("clean-contamination", path.relative_to(root).as_posix(), "non-framework decision in clean baseline"))
    wiki_exempt = {"README.md", "index.md", "log.md", "metrics.md", "schema.md", "taxonomy.md"}
    for path in (fcvw / "wiki").rglob("*.md"):
        if path.name in wiki_exempt or "templates" in path.parts:
            continue
        findings.append(Finding("clean-contamination", path.relative_to(root).as_posix(), "knowledge record in clean baseline"))
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


def validate_version(root: Path, findings: list[Finding]) -> None:
    lock_text = read_text(root / "FCVW" / "FRAMEWORK_LOCK.md")
    match = re.search(r"Installed version.*?(V\d+\.\d+\.\d+)", lock_text)
    version = match.group(1) if match else ""
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
        if release_metadata.get("schema") != "fcvw/framework-release@1":
            findings.append(Finding("framework-release", release_path.relative_to(root).as_posix(), "invalid release schema"))
        if release_metadata.get("version") != version:
            findings.append(Finding("framework-release", release_path.relative_to(root).as_posix(), "version does not match framework lock"))
        if release_metadata.get("release_status") not in {"in_preparation", "published", "canceled"}:
            findings.append(Finding("framework-release", release_path.relative_to(root).as_posix(), "invalid release status"))
    if (root / "FCVW" / "changelogs" / f"{version}.md").exists():
        findings.append(Finding("version-namespace", f"FCVW/changelogs/{version}.md", "framework release in application namespace"))


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
    validate_canonical_metadata(root, findings)
    validate_plans(root, findings)
    validate_skills(root, findings)
    validate_reading_routes(root, findings)
    validate_wiki_ids(root, findings)
    validate_profiles(root, args.profile, findings)
    validate_version(root, findings)
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
