#!/usr/bin/env python3
"""Parse and validate FCVW plan priority queues."""

from __future__ import annotations

import re
import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from frontmatter_fcvw import parse_frontmatter, scalar


CATEGORIES = ("correction", "optimization", "code_hygiene", "visual", "other")
CATEGORY_RANK = {name: index for index, name in enumerate(CATEGORIES)}
PLAN_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
NONE_VALUES = {"", "-", "none", "n/a", "not_applicable"}
PREEMPT_PREFIX = "before_in_progress:"
TABLE_SEPARATOR = re.compile(r"^:?-{3,}:?$")


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
    lines = path.read_text(encoding="utf-8-sig").splitlines()
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


def validate_plan_queues(root: Path) -> list[QueueFinding]:
    root = root.resolve()
    plans_root = root / "FCVW" / "Plans"
    findings: list[QueueFinding] = []
    seen_global: dict[str, str] = {}
    all_plan_paths: dict[str, list[Path]] = {}
    for path in plans_root.glob("*/*.md"):
        if path.name in {"README.md", "QUEUE.md", "INDEX.md"}:
            continue
        all_plan_paths.setdefault(path.stem, []).append(path)
    for state in ("pending", "in_progress"):
        folder = plans_root / state
        queue_path = folder / "QUEUE.md"
        relative = queue_path.relative_to(root).as_posix()
        entries, parse_findings = parse_queue(queue_path)
        findings.extend(
            QueueFinding(item.rule, relative if item.path == queue_path.as_posix() else item.path, item.message)
            for item in parse_findings
        )
        if not queue_path.is_file():
            continue
        metadata = parse_frontmatter(queue_path.read_text(encoding="utf-8-sig")).data
        if scalar(metadata, "schema") != "fcvw/plan-queue@1":
            findings.append(QueueFinding("plan-queue-schema", relative, "invalid or missing queue schema"))
        if scalar(metadata, "state") != state:
            findings.append(QueueFinding("plan-queue-state", relative, f"queue state must be {state}"))
        for field, expected in (
            ("artifact_role", "project_profile"),
            ("owner", "project"),
            ("upgrade_strategy", "preserve"),
        ):
            if scalar(metadata, field) != expected:
                findings.append(QueueFinding("plan-queue-schema", relative, f"{field} must be {expected}"))
        if not scalar(metadata, "updated_at"):
            findings.append(QueueFinding("plan-queue-schema", relative, "updated_at is required"))

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
            plan_metadata = parse_frontmatter(plan_path.read_text(encoding="utf-8-sig")).data
            if scalar(plan_metadata, "status") != state:
                findings.append(
                    QueueFinding("plan-queue-state", relative, f"queued plan metadata does not match {state}: {plan_id}")
                )
            priority = scalar(plan_metadata, "priority")
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
            if blocker.lower() not in NONE_VALUES:
                if blocker.lower().startswith("external:"):
                    if len(blocker.split(":", 1)[1].strip()) < 8:
                        findings.append(
                            QueueFinding("plan-queue-blocker", relative, f"external blocker is too vague: {entry.plan_id}")
                        )
                else:
                    dependencies = [item.strip().strip("`") for item in blocker.split(",") if item.strip()]
                    for dependency in dependencies:
                        matches = all_plan_paths.get(dependency, [])
                        if not re.fullmatch(
                            r"P[1-5]-R[1-5]-\d{4}-\d{2}-\d{2}-[a-z0-9-]+",
                            dependency,
                        ):
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
                        dependency_metadata = parse_frontmatter(
                            matches[0].read_text(encoding="utf-8-sig")
                        ).data
                        if scalar(dependency_metadata, "status") in {"completed", "discontinued"}:
                            findings.append(
                                QueueFinding(
                                    "plan-queue-blocker",
                                    relative,
                                    f"resolved blocker remains in queue for {entry.plan_id}: {dependency}",
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--recommend", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    findings = validate_plan_queues(root)
    for finding in findings:
        print(f"ERROR [{finding.rule}] {finding.path}: {finding.message}")
    if findings:
        print(f"FCVW plan queues: findings={len(findings)}")
        return 1
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
