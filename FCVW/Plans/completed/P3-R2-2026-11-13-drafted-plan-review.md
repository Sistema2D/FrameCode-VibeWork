---
schema: "fcvw/plan@2"
id: "P3-R2-2026-11-13-drafted-plan-review"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P3"
risk: "R2"
created_at: "2026-11-13"
updated_at: "2026-11-13"
current_version: "V0.23.0"
expected_version: "V0.24.0"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "AGENTS.md"
  - "FCVW/PLANNING.md"
  - "FCVW/SCHEMAS.md"
  - "tools/validate_fcvw.py"
  - "tools/plan_queue_fcvw.py"
category: "optimization"
depends_on: []
---

# Plans drafted outside the agent run only after review

## Description

Generalize a downstream rule: a plan written by a tool, an import or from the user's comments (the downstream project's screenshot-review application) is not executed until the agent has reviewed it whole and the user confirmed the agent's understanding. Fields `source` and `ai_review` (`pending`, `confirmed`), rule `plan-review`, and a queue blocker.

## Justification and objective

The downstream project's capture application writes plans from comments on screenshots; 29 of them were executed under a local rule ("while `ai_review` is pending, do not execute"), all now `confirmed`. Nothing in the framework stopped such a plan from running unreviewed, and the queue would have recommended it. The field names are the downstream ones, so those 29 plans and the tool stay valid without migration.

## Scope

### Included

- `validate_fcvw.py` rule `plan-review`; `plan_queue_fcvw.py` blocker; `AGENTS.md`, `PLANNING.md` (When planning applies), `SCHEMAS.md`, `MIGRATIONS.md`.

### Excluded

- The downstream tool's `review_key`, `unified` and comment markers, which belong to that tool.

## Affected files or boundaries

The files above and `DraftedPlanReviewTests`.

## Implementation plan

1. Rule and blocker reading the existing downstream field names.
2. Text in the routed first-read section of `PLANNING.md`.

## Proportionality gate

Not applicable — two optional fields already in use downstream, one rule and one queue blocker of about 25 lines; no new schema or surface.

## Acceptance criteria

- [x] A pending-review plan may wait in `pending/` but fails in `in_progress` or `completed`; an invalid value fails.
- [x] The queue never recommends a plan awaiting review.
- [x] The 29 downstream confirmed plans stay valid.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

- Queue recommendation order; plans that already use `ai_review`.

### Regression contracts consulted

- `FCVW/PLANNING.md` — priority queue derivation.

### Regression checks required

- [x] Rule and queue tests; downstream copy run.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Rule and queue | pass | `DraftedPlanReviewTests` (2) |
| Downstream plans | pass | upgrade rehearsal copy: no `plan-review` finding among 29 `confirmed` screenshot-review plans |

### Limitations and residual risk

- The rule cannot tell whether the user really confirmed; it makes skipping the step visible.

## Validation plan

- [x] `python -B tools/check_fcvw.py --root .`

## Rollback

Revert the commit; the fields stay valid and ignored by older tools.

## Gates and approvals

- Owner: "siga com suas sugestões" (2026-11-13), after the proposal to generalize the downstream rule.

## Related records

- Framework release: [V0.24.0](../../framework-releases/V0.24.0.md).
- Related plan: [failure handling](P2-R2-2026-11-13-failure-handling-and-release-guard.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Suite and rehearsal | pass | see Regression evidence |

## Gaps and residual risk

See *Limitations and residual risk*.

## Status

`completed`
