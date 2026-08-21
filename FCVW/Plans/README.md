# Plans

This directory stores formal change plans for the project, organized by status.

- `pending/` — Plans approved but not yet started.
- `in_progress/` — Plans actively being executed.
- `completed/` — Validated and closed plans.
- `discontinued/` — Canceled plans with justification.

For the planning methodology, see `FCVW/PLANNING.md`.

## Operational queues

- [`in_progress/QUEUE.md`](in_progress/QUEUE.md) ? first source for the next executable plan.
- [`pending/QUEUE.md`](pending/QUEUE.md) ? ordered backlog after active work.

Every plan in either active directory appears exactly once in its queue. Completed and discontinued plans remain reachable through [`../DOCUMENT_GRAPH.md`](../DOCUMENT_GRAPH.md) and their related release, changelog, decision, regression, or audit records.

Blocking plan prerequisites are declared durably through `depends_on` and a Dependency validation table. Queue blocker cells contain only unresolved prerequisite IDs or a specific external condition. The two queues remain canonical; a combined view may be generated to `.fcvw-cache/` with `tools/plan_queue_fcvw.py --output`.
