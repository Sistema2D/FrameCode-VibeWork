---
schema: "fcvw/plan@2"
id: "P2-R2-2026-09-28-role-based-policy-routing"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P2"
risk: "R2"
created_at: "2026-09-28"
updated_at: "2026-09-28"
current_version: "V0.19.0"
expected_version: "V0.19.1"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "FCVW/CONTEXT_MAP.md"
  - "FCVW/AI.md"
depends_on: []
---

# Role-based policy routing

## Description

Decide `event:policy` for `FCVW/*.md` by the declared `artifact_role` instead of path depth, and stop treating the framework schema catalog as application data. Backlog items C-01 and C-02 of the source-only maintainer backlog (`TODO.md` at the source repository root, not installed).

## Justification and objective

Editing a project profile triggered the framework policy route and loaded `SCHEMAS.md` and `AUDIT.md`. The objective is a smaller mandatory route for project profiles without weakening routes for real policies.

## Scope

### Included

- Framework policies, the lock and templates (including `FCVW/governance/`) trigger `policy`; project profiles do not.
- Deleted, unreadable or undeclared root documents stay conservative and still trigger `policy`.
- `SCHEMAS.md` no longer triggers `data`.

### Excluded

- Semantic heuristics for application code (G-03) and filesystem or AI bridge triggers (B-06, B-07).

## Affected files or boundaries

`tools/context_routing_fcvw.py`, `tools/test_retrieval_quality.py`.

## Implementation plan

1. Read the declared role through the shared cache when the file exists.
2. Keep unknown roles conservative; include governance templates.
3. Add route tests and measure the mandatory bytes before and after.

## Proportionality gate

Not applicable — a role lookup inside the existing router, reusing the shared frontmatter cache.

## Acceptance criteria

- [x] A project profile edit no longer triggers `policy`.
- [x] Policy and template edits still trigger `policy`; deletions stay conservative.
- [x] Mandatory bytes for profile edits decrease.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

Cumulative routes, operation-aware filesystem hints, private tool classification and the retrieval benchmark.

### Regression contracts consulted

- [Context map](../../CONTEXT_MAP.md) — event table and cumulative routing.
- [AI governance](../../AI.md) — mandatory routes stay authoritative.

### Regression checks required

- [x] Existing routing and benchmark tests.
- [x] New fixtures for profile, policy, template, deletion and schema catalog.
- [x] Before/after measurement with the same session and event.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Routing tests | pass | `test_retrieval_quality`, including 3 new tests |
| Benchmark | pass | `benchmark_retrieval_fcvw.py --check` through the local runner |
| Measurement | pass | session `documentation`, event `change`: `SECURITY.md` 83.6 to 50.2 KB; `SCOPE.md` 62.0 to 28.6 KB; `SCHEMAS.md` 81.8 to 62.1 KB; `PLANNING.md` unchanged at 62.0 KB |

### Limitations and residual risk

- Byte counts are file sizes of mandatory paths, not model tokens.
- An edit to the `SECURITY.md` profile still loads the security route, which is intended.

## Validation plan

Routing unit tests, benchmark, measurement and full suite.

## Rollback

Revert the commit that changed `tools/context_routing_fcvw.py`; the route tables themselves are unchanged.

## Gates and approvals

- Regression gate: passed with the evidence above.
- AI gate: mandatory event routes remain cumulative; only the policy classification of project profiles changed.
- Decomposition required: no.

## Related records

- Framework release: [V0.19.1](../../framework-releases/V0.19.1.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Local checks | pass | see the framework release record |

## Gaps and residual risk

G-03, B-06 and B-07 remain in phase 3 of the backlog.
