#!/usr/bin/env python3
"""Parse and validate FCVW plan priority queues."""

from __future__ import annotations

import re
import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from frontmatter_fcvw import parse_frontmatter, scalar
from plan_dependencies_fcvw import PLAN_ID, dependency_state, inspect_plan_dependencies
from fcvw_cache import frontmatter as cache_frontmatter, read_text as cache_read_text


CATEGORIES = ("correction", "optimization", "code_hygiene", "visual", "other")
CATEGORY_RANK = {name: index for index, name in enumerate(CATEGORIES)}
PLAN_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
NONE_VALUES = {"", "-", "none", "n/a", "not_applicable"}
PREEMPT_PREFIX = "before_in_progress:"
TABLE_SEPARATOR = re.compile(r"^:?-{3,}:?$")
# One fragment per plan removes the single shared file that every parallel
# branch had to edit. QUEUE.md stays valid as a legacy source and becomes a
# generated view once fragments exist.
FRAGMENT_DIRECTORY = "queue.d"
FRAGMENT_SCHEMA = "fcvw/plan-queue-entry@1"
FRAGMENT_FIELDS = ("schema", "plan", "order", "category")


@dataclass(frozen=True)
class QueueEntry:
    order: int
    plan_id: str
    target: str
    category: str
    blocked_by: str
    override_reason: str


@dataclass(frozen=True)
class QueueFinding:
    rule: str
    path: str
    message: str


def parse_queue(path: Path) -> tuple[list[QueueEntry], list[QueueFinding]]:
    relative = path.as_posix()
    if not path.is_file():
        return [], [QueueFinding("plan-queue", relative, "queue file is missing")]
    lines = cache_read_text(path).splitlines()
    entries: list[QueueEntry] = []
    findings: list[QueueFinding] = []
    header_seen = False
    separator_seen = False
    for line_number, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not header_seen:
            if len(cells) == 5 and not cells[0].isdigit() and not PLAN_LINK.fullmatch(cells[1]):
                header_seen = True
            continue
        if not separator_seen:
            if len(cells) == 5 and all(TABLE_SEPARATOR.fullmatch(cell) for cell in cells):
                separator_seen = True
            continue
        if not stripped.startswith("|"):
            continue
        if len(cells) != 5:
            findings.append(QueueFinding("plan-queue-format", relative, f"invalid row at line {line_number}"))
            continue
        order_raw, plan_raw, category, blocked_by, override_reason = cells
        try:
            order = int(order_raw)
        except ValueError:
            findings.append(QueueFinding("plan-queue-order", relative, f"invalid order at line {line_number}"))
            continue
        match = PLAN_LINK.fullmatch(plan_raw)
        if not match:
            findings.append(QueueFinding("plan-queue-link", relative, f"plan must be a Markdown link at line {line_number}"))
            continue
        plan_id, target = match.groups()
        entries.append(QueueEntry(order, plan_id.strip("`"), target, category, blocked_by, override_reason))
    if not header_seen or not separator_seen:
        findings.append(QueueFinding("plan-queue-format", relative, "canonical queue table header is missing"))
    return entries, findings


def fragment_directory(folder: Path) -> Path:
    return folder / FRAGMENT_DIRECTORY


def parse_queue_fragments(folder: Path, root: Path) -> tuple[list[QueueEntry], list[QueueFinding]]:
    """Read one queue entry per file so parallel work never shares a queue file."""

    directory = fragment_directory(folder)
    entries: list[QueueEntry] = []
    findings: list[QueueFinding] = []
    seen_order: dict[int, str] = {}
    for path in sorted(directory.glob("*.md")):
        if path.name == "README.md":
            continue
        relative = path.relative_to(root).as_posix()
        metadata = cache_frontmatter(path)
        if scalar(metadata, "schema") != FRAGMENT_SCHEMA:
            findings.append(QueueFinding("plan-queue-schema", relative, "invalid or missing queue-entry schema"))
            continue
        missing = [field for field in FRAGMENT_FIELDS if not scalar(metadata, field)]
        if missing:
            findings.append(
                QueueFinding("plan-queue-schema", relative, f"missing field(s): {', '.join(missing)}")
            )
            continue
        plan_id = scalar(metadata, "plan")
        raw_order = scalar(metadata, "order")
        try:
            order = int(raw_order)
        except ValueError:
            findings.append(QueueFinding("plan-queue-order", relative, f"order must be an integer: {raw_order!r}"))
            continue
        if path.stem != plan_id:
            findings.append(
                QueueFinding("plan-queue-entry", relative, "queue fragment filename must equal its plan id")
            )
        if order in seen_order:
            findings.append(
                QueueFinding(
                    "plan-queue-order",
                    relative,
                    f"order {order} is already used by {seen_order[order]}",
                )
            )
        seen_order[order] = relative
        entries.append(
            QueueEntry(
                order=order,
                plan_id=plan_id,
                # Targets are resolved from the state directory, like a QUEUE.md row.
                target=f"{plan_id}.md",
                category=scalar(metadata, "category"),
                blocked_by=scalar(metadata, "blocked_by"),
                override_reason=scalar(metadata, "override_reason"),
            )
        )
    entries.sort(key=lambda item: item.order)
    return entries, findings


def render_queue(state: str, entries: list[QueueEntry], updated_at: str) -> str:
    """Render the disposable aggregate view of one state queue."""

    title = "Pending plan queue" if state == "pending" else "In-progress plan queue"
    rows = [
        f"| {entry.order} | [{entry.plan_id}]({entry.target}) | "
        f"{entry.category} | {entry.blocked_by or 'none'} | {entry.override_reason or '-'} |"
        for entry in entries
    ]
    return "\n".join(
        [
            "---",
            'schema: "fcvw/plan-queue@1"',
            'artifact_role: "generated"',
            'owner: "project"',
            'upgrade_strategy: "regenerate"',
            f'state: "{state}"',
            f'updated_at: "{updated_at}"',
            "---",
            "",
            f"# {title}",
            "",
            f"Generated from [`{FRAGMENT_DIRECTORY}/`]({FRAGMENT_DIRECTORY}/README.md). "
            "Edit a fragment, not this file. Queue policy lives in "
            "[`PLANNING.md`](../../PLANNING.md).",
            "",
            "| Order | Plan | Category | Blocked by | Override reason |",
            "|---:|---|---|---|---|",
            *rows,
            "",
        ]
    )


def validate_plan_queues(root: Path) -> list[QueueFinding]:
    root = root.resolve()
    plans_root = root / "FCVW" / "Plans"
    findings: list[QueueFinding] = []
    seen_global: dict[str, str] = {}
    dependency_snapshot = inspect_plan_dependencies(root)
    all_plan_paths = dependency_snapshot.catalog
    plan_metadata = dependency_snapshot.metadata
    plan_dependencies = dependency_snapshot.dependencies
    dependency_evidence = dependency_snapshot.evidence
    findings.extend(QueueFinding(item.rule, item.path, item.message) for item in dependency_snapshot.findings)
    for state in ("pending", "in_progress"):
        folder = plans_root / state
        queue_path = folder / "QUEUE.md"
        relative = queue_path.relative_to(root).as_posix()
        fragments = fragment_directory(folder)
        use_fragments = fragments.is_dir()
        if use_fragments:
            entries, parse_findings = parse_queue_fragments(folder, root)
            findings.extend(parse_findings)
        else:
            entries, parse_findings = parse_queue(queue_path)
            findings.extend(
                QueueFinding(item.rule, relative if item.path == queue_path.as_posix() else item.path, item.message)
                for item in parse_findings
            )
            if not queue_path.is_file():
                continue
        if queue_path.is_file():
            metadata = cache_frontmatter(queue_path)
            if scalar(metadata, "schema") != "fcvw/plan-queue@1":
                findings.append(QueueFinding("plan-queue-schema", relative, "invalid or missing queue schema"))
            if scalar(metadata, "state") != state:
                findings.append(QueueFinding("plan-queue-state", relative, f"queue state must be {state}"))
            expected_role = ("generated", "regenerate") if use_fragments else ("project_profile", "preserve")
            for field, expected in (
                ("artifact_role", expected_role[0]),
                ("owner", "project"),
                ("upgrade_strategy", expected_role[1]),
            ):
                if scalar(metadata, field) != expected:
                    findings.append(QueueFinding("plan-queue-schema", relative, f"{field} must be {expected}"))
            if not scalar(metadata, "updated_at"):
                findings.append(QueueFinding("plan-queue-schema", relative, "updated_at is required"))
        elif not use_fragments:
            continue

        plan_paths = {
            path.stem: path
            for path in folder.glob("*.md")
            if path.name not in {"README.md", "QUEUE.md", "INDEX.md"}
        }
        ids = [entry.plan_id for entry in entries]
        if len(ids) != len(set(ids)):
            findings.append(QueueFinding("plan-queue-duplicate", relative, "queue contains duplicate plan IDs"))
        missing = sorted(set(plan_paths) - set(ids))
        stale = sorted(set(ids) - set(plan_paths))
        for plan_id in missing:
            findings.append(QueueFinding("plan-queue-missing", relative, f"plan is absent from queue: {plan_id}"))
        for plan_id in stale:
            findings.append(QueueFinding("plan-queue-stale", relative, f"queue references missing plan: {plan_id}"))
        if [entry.order for entry in entries] != list(range(1, len(entries) + 1)):
            findings.append(QueueFinding("plan-queue-order", relative, "queue order must be contiguous and start at 1"))

        priorities: dict[str, int] = {}
        for plan_id, plan_path in plan_paths.items():
            current_metadata = cache_frontmatter(plan_path)
            if scalar(current_metadata, "status") != state:
                findings.append(
                    QueueFinding("plan-queue-state", relative, f"queued plan metadata does not match {state}: {plan_id}")
                )
            priority = scalar(current_metadata, "priority")
            if re.fullmatch(r"P[1-5]", priority):
                priorities[plan_id] = int(priority[1:])

        for index, entry in enumerate(entries):
            if entry.category not in CATEGORY_RANK:
                findings.append(
                    QueueFinding("plan-queue-category", relative, f"invalid category for {entry.plan_id}: {entry.category}")
                )
                continue
            target_value = entry.target.split("#", 1)[0]
            target_path = (queue_path.parent / target_value).resolve()
            expected_path = (folder / f"{entry.plan_id}.md").resolve()
            if target_path != expected_path:
                findings.append(
                    QueueFinding(
                        "plan-queue-link",
                        relative,
                        f"link target must resolve to the plan in the matching queue directory: {entry.plan_id}",
                    )
                )
            rank = CATEGORY_RANK[entry.category]
            override = entry.override_reason.strip().lower()
            bypasses_later_category = any(
                later.category in CATEGORY_RANK and CATEGORY_RANK[later.category] < rank
                for later in entries[index + 1 :]
            )
            if bypasses_later_category and override in NONE_VALUES:
                findings.append(
                    QueueFinding(
                        "plan-queue-priority",
                        relative,
                        f"{entry.plan_id} bypasses a higher-priority category without an override reason",
                    )
                )
            current_priority = priorities.get(entry.plan_id)
            bypasses_higher_priority = (
                current_priority is not None
                and any(
                    later.category == entry.category
                    and priorities.get(later.plan_id, current_priority) < current_priority
                    for later in entries[index + 1 :]
                )
            )
            if bypasses_higher_priority and override in NONE_VALUES:
                findings.append(
                    QueueFinding(
                        "plan-queue-priority",
                        relative,
                        f"{entry.plan_id} bypasses a higher-priority plan without an override reason",
                    )
                )
            if override.startswith(PREEMPT_PREFIX):
                reason = entry.override_reason.split(":", 1)[1].strip()
                if state != "pending" or len(reason) < 12:
                    findings.append(
                        QueueFinding(
                            "plan-queue-override",
                            relative,
                            f"{entry.plan_id} has an invalid cross-state override",
                        )
                    )
            blocker = entry.blocked_by.strip()
            internal_blockers: list[str] = []
            if blocker.lower() not in NONE_VALUES:
                if blocker.lower().startswith("external:"):
                    if len(blocker.split(":", 1)[1].strip()) < 8:
                        findings.append(
                            QueueFinding("plan-queue-blocker", relative, f"external blocker is too vague: {entry.plan_id}")
                        )
                else:
                    internal_blockers = [item.strip().strip("`") for item in blocker.split(",") if item.strip()]
                    for dependency in internal_blockers:
                        matches = all_plan_paths.get(dependency, [])
                        if not PLAN_ID.fullmatch(dependency):
                            findings.append(
                                QueueFinding(
                                    "plan-queue-blocker",
                                    relative,
                                    f"invalid blocker reference for {entry.plan_id}: {dependency}",
                                )
                            )
                            continue
                        if dependency == entry.plan_id:
                            findings.append(
                                QueueFinding("plan-queue-blocker", relative, f"plan blocks itself: {entry.plan_id}")
                            )
                        if len(matches) != 1:
                            findings.append(
                                QueueFinding(
                                    "plan-queue-blocker",
                                    relative,
                                    f"blocker is missing or ambiguous for {entry.plan_id}: {dependency}",
                                )
                            )
                            continue
            declared = plan_dependencies.get(entry.plan_id, [])
            evidence = dependency_evidence.get(entry.plan_id, {})
            unresolved = [
                dependency
                for dependency in declared
                if dependency_state(dependency, all_plan_paths, evidence)[0] != "satisfied"
            ]
            if declared and set(internal_blockers) != set(unresolved):
                findings.append(
                    QueueFinding(
                        "plan-queue-dependency",
                        relative,
                        f"queue blockers for {entry.plan_id} must equal unresolved depends_on IDs: "
                        f"expected {', '.join(unresolved) or 'none'}",
                    )
                )
            elif internal_blockers and not declared:
                schema = scalar(plan_metadata.get(entry.plan_id, {}), "schema")
                if schema == "fcvw/plan@2":
                    findings.append(
                        QueueFinding(
                            "plan-queue-dependency",
                            relative,
                            f"internal blockers must be declared in depends_on: {entry.plan_id}",
                        )
                    )
            if entry.plan_id in seen_global:
                findings.append(
                    QueueFinding(
                        "plan-queue-duplicate",
                        relative,
                        f"plan is queued in more than one state: {entry.plan_id}",
                    )
                )
            seen_global[entry.plan_id] = state
    return findings



def recommend_next_plan(root: Path) -> tuple[str, QueueEntry] | None:
    """Return the first unblocked in-progress entry, then pending entry."""

    if validate_plan_queues(root):
        return None
    plans_root = root.resolve() / "FCVW" / "Plans"
    pending_entries, _ = parse_queue(plans_root / "pending" / "QUEUE.md")
    for entry in pending_entries:
        if (
            entry.blocked_by.strip().lower() in NONE_VALUES
            and entry.override_reason.strip().lower().startswith(PREEMPT_PREFIX)
        ):
            return "pending", entry
    for state in ("in_progress", "pending"):
        entries, _ = parse_queue(plans_root / state / "QUEUE.md")
        for entry in entries:
            if entry.blocked_by.strip().lower() in NONE_VALUES:
                return state, entry
    return None


def render_aggregate_queue(root: Path) -> str:
    """Render a disposable combined view without creating another source of truth."""

    root = root.resolve()
    plans_root = root / "FCVW" / "Plans"
    recommendation = recommend_next_plan(root)
    recommended_id = recommendation[1].plan_id if recommendation else ""
    lines = [
        "# Aggregate plan queue",
        "",
        "> Disposable view generated from the canonical in-progress and pending queues.",
        "",
        "| State | Order | Plan | Category | Blocked by | Recommended |",
        "|---|---:|---|---|---|---|",
    ]
    for state in ("in_progress", "pending"):
        entries, _ = parse_queue(plans_root / state / "QUEUE.md")
        for entry in entries:
            lines.append(
                f"| {state} | {entry.order} | {entry.plan_id} | {entry.category} | "
                f"{entry.blocked_by or 'none'} | {'yes' if entry.plan_id == recommended_id else 'no'} |"
            )
    if len(lines) == 6:
        lines.append("| - | - | none | - | - | no |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument(
        "--write-queues",
        action="store_true",
        help="regenerate each QUEUE.md view from its queue.d/ fragments",
    )
    parser.add_argument("--recommend", action="store_true")
    parser.add_argument("--output", help="write a disposable aggregate Markdown view")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if args.write_queues:
        from datetime import date

        written = []
        for state in ("pending", "in_progress"):
            folder = root / "FCVW" / "Plans" / state
            if not fragment_directory(folder).is_dir():
                continue
            entries, fragment_findings = parse_queue_fragments(folder, root)
            if fragment_findings:
                for finding in fragment_findings:
                    print(f"ERROR [{finding.rule}] {finding.path}: {finding.message}")
                return 1
            (folder / "QUEUE.md").write_text(
                render_queue(state, entries, date.today().isoformat()),
                encoding="utf-8",
                newline="\n",
            )
            written.append(f"{state} ({len(entries)})")
        print(f"FCVW plan queue views regenerated: {', '.join(written) if written else 'none'}")
    findings = validate_plan_queues(root)
    for finding in findings:
        print(f"ERROR [{finding.rule}] {finding.path}: {finding.message}")
    if findings:
        print(f"FCVW plan queues: findings={len(findings)}")
        return 1
    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_aggregate_queue(root), encoding="utf-8", newline="\n")
        print(f"FCVW aggregate plan queue: output={output}")
    if args.recommend:
        recommendation = recommend_next_plan(root)
        if recommendation is None:
            print("FCVW plan queue recommendation: no unblocked plan")
        else:
            state, entry = recommendation
            print(
                "FCVW plan queue recommendation: "
                f"state={state} order={entry.order} plan={entry.plan_id} category={entry.category}"
            )
    else:
        print("FCVW plan queues: findings=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
