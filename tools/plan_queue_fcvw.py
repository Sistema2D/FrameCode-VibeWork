#!/usr/bin/env python3
"""Derive and check the FCVW plan queue from plan frontmatter.

The queue is not a file. Each plan in `pending/` and `in_progress/` declares its
own `category`, optional `blocked_external` reason and optional
`before_in_progress` reason; blockers come from unresolved `depends_on`. The
order is computed, so there is no second copy that can drift from the plans and
no shared queue file for parallel branches to conflict on.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from frontmatter_fcvw import scalar
from plan_dependencies_fcvw import dependency_state, inspect_plan_dependencies


CATEGORIES = ("correction", "optimization", "code_hygiene", "visual", "other")
CATEGORY_RANK = {name: index for index, name in enumerate(CATEGORIES)}
STATES = ("in_progress", "pending")
MINIMUM_REASON = 12
# Pre-V0.20.0 queue files. They are project-owned, so they are never deleted
# automatically; the validator only asks for their fields to move into the plans.
LEGACY_QUEUE_FILES = ("QUEUE.md", "queue.d")


@dataclass(frozen=True)
class QueueEntry:
    state: str
    order: int
    plan_id: str
    category: str
    blocked_by: str
    before_in_progress: str


@dataclass(frozen=True)
class QueueFinding:
    rule: str
    path: str
    message: str
    severity: str = "error"


def _plans(root: Path, state: str) -> list[Path]:
    folder = root / "FCVW" / "Plans" / state
    return sorted(path for path in folder.glob("*.md") if path.name not in {"README.md", "QUEUE.md", "INDEX.md"})


def derive_queue(root: Path) -> tuple[list[QueueEntry], list[QueueFinding]]:
    """Return the ordered queue for both active states and its findings."""

    root = root.resolve()
    snapshot = inspect_plan_dependencies(root)
    findings = [QueueFinding(item.rule, item.path, item.message) for item in snapshot.findings]
    candidates: list[tuple[tuple, QueueEntry]] = []
    for state in STATES:
        for path in _plans(root, state):
            relative = path.relative_to(root).as_posix()
            plan_id = path.stem
            metadata = snapshot.metadata.get(plan_id, {})
            category = scalar(metadata, "category") or "other"
            if category not in CATEGORY_RANK:
                findings.append(QueueFinding("plan-queue-category", relative, f"invalid category: {category!r}"))
                category = "other"
            evidence = snapshot.evidence.get(plan_id, {})
            blockers = [
                dependency
                for dependency in snapshot.dependencies.get(plan_id, [])
                if dependency_state(dependency, snapshot.catalog, evidence)[0] != "satisfied"
            ]
            external = scalar(metadata, "blocked_external").strip()
            if external:
                if len(external) < MINIMUM_REASON:
                    findings.append(QueueFinding("plan-queue-blocker", relative, "blocked_external reason is too vague"))
                blockers.append(f"external: {external}")
            preempt = scalar(metadata, "before_in_progress").strip()
            if preempt and (state != "pending" or len(preempt) < MINIMUM_REASON):
                findings.append(
                    QueueFinding(
                        "plan-queue-override",
                        relative,
                        "before_in_progress needs a specific reason and applies only to pending plans",
                    )
                )
                preempt = ""
            priority = scalar(metadata, "priority")
            rank = int(priority[1:]) if len(priority) == 2 and priority[1:].isdigit() else 9
            key = (
                0 if preempt and not blockers else 1 + STATES.index(state),
                1 if blockers else 0,
                CATEGORY_RANK[category],
                rank,
                scalar(metadata, "created_at"),
                plan_id,
            )
            candidates.append((key, QueueEntry(state, 0, plan_id, category, ", ".join(blockers), preempt)))
    ordered: list[QueueEntry] = []
    counters = {state: 0 for state in STATES}
    for _, entry in sorted(candidates, key=lambda item: item[0]):
        counters[entry.state] += 1
        ordered.append(QueueEntry(entry.state, counters[entry.state], entry.plan_id, entry.category,
                                  entry.blocked_by, entry.before_in_progress))
    for state in STATES:
        folder = root / "FCVW" / "Plans" / state
        for name in LEGACY_QUEUE_FILES:
            legacy = folder / name
            if legacy.exists():
                findings.append(
                    QueueFinding(
                        "plan-queue-legacy",
                        legacy.relative_to(root).as_posix(),
                        "legacy queue is ignored; move category and blockers into plan frontmatter, then delete it",
                        "warning",
                    )
                )
    return ordered, findings


def validate_plan_queues(root: Path) -> list[QueueFinding]:
    return derive_queue(root)[1]


def recommend_next_plan(root: Path) -> tuple[str, QueueEntry] | None:
    """First unblocked plan in derived order; blocking findings suppress it."""

    entries, findings = derive_queue(root)
    if any(item.severity == "error" for item in findings):
        return None
    ordered = sorted(entries, key=lambda item: (0 if item.before_in_progress else 1, STATES.index(item.state), item.order))
    for entry in ordered:
        if not entry.blocked_by:
            return entry.state, entry
    return None


def render_aggregate_queue(root: Path) -> str:
    """Render a disposable view; it is never a source of truth."""

    entries, _ = derive_queue(root)
    recommendation = recommend_next_plan(root)
    recommended = recommendation[1].plan_id if recommendation else ""
    lines = [
        "# Plan queue",
        "",
        "> Disposable view derived from plan frontmatter.",
        "",
        "| State | Order | Plan | Category | Blocked by | Recommended |",
        "|---|---:|---|---|---|---|",
    ]
    for entry in entries:
        lines.append(
            f"| {entry.state} | {entry.order} | {entry.plan_id} | {entry.category} | "
            f"{entry.blocked_by or 'none'} | {'yes' if entry.plan_id == recommended else 'no'} |"
        )
    if not entries:
        lines.append("| - | - | none | - | - | no |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--recommend", action="store_true")
    parser.add_argument("--output", help="write a disposable Markdown view of the derived queue")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    entries, findings = derive_queue(root)
    for finding in findings:
        print(f"{finding.severity.upper()} [{finding.rule}] {finding.path}: {finding.message}")
    errors = [item for item in findings if item.severity == "error"]
    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_aggregate_queue(root), encoding="utf-8", newline="\n")
        print(f"FCVW plan queue view: output={output}")
    if args.recommend and not errors:
        recommendation = recommend_next_plan(root)
        if recommendation is None:
            print("FCVW plan queue recommendation: no unblocked plan")
        else:
            state, entry = recommendation
            print(
                "FCVW plan queue recommendation: "
                f"state={state} order={entry.order} plan={entry.plan_id} category={entry.category}"
            )
    print(f"FCVW plan queue: plans={len(entries)} findings={len(findings)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
