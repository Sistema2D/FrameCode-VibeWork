---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# In-progress plan queue fragments

Every plan in `in_progress/` has exactly one fragment here, named `<plan-id>.md`. A
fragment is the canonical source of its queue entry; `../QUEUE.md` is a view
generated from this directory.

One file per plan exists for an operational reason: parallel work on separate
branches never edits the same file, so changing the queue stops being a
guaranteed source of merge conflict. It is the same pattern already used by
`changelogs/unreleased/`.

## Fragment format

```markdown
---
schema: "fcvw/plan-queue-entry@1"
artifact_role: "project_profile"
owner: "project"
upgrade_strategy: "preserve"
plan: "P3-R2-YYYY-MM-DD-short-slug"
order: 1
category: "correction"
blocked_by: "none"
override_reason: "-"
---

# Queue entry: P3-R2-YYYY-MM-DD-short-slug

Queue entry for [`P3-R2-YYYY-MM-DD-short-slug`](../P3-R2-YYYY-MM-DD-short-slug.md).
```

`category` uses `correction`, `optimization`, `code_hygiene`, `visual`, or
`other`. `blocked_by` uses `none`, comma-separated unresolved `depends_on` IDs,
or `external: <specific reason>`. `override_reason` explains a concrete ordering
inversion, or `-`.

## Regenerating the view

```bash
python FCVW/tools/plan_queue_fcvw.py --root . --write-queues
```

## Legacy queues

A project that still keeps rows directly in `../QUEUE.md` remains valid:
fragments only take over when this directory exists. Migrate one row at a time;
there is no bulk rewrite.
