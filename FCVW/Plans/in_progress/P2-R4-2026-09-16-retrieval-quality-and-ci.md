---
schema: "fcvw/plan@2"
id: "P2-R4-2026-09-16-retrieval-quality-and-ci"
artifact_role: "record"
upgrade_strategy: "preserve"
record_scope: "framework"
retrieval_scope: "exact_only"
status: "in_progress"
priority: "P2"
risk: "R4"
created_at: "2026-09-16"
updated_at: "2026-09-16"
current_version: "V0.17.0"
expected_version: "V0.18.0"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "AGENTS.md"
  - "FCVW/CONTEXT_MAP.md"
  - "FCVW/AI.md"
  - "FCVW/SECURITY.md"
  - "FCVW/TESTS.md"
  - "FCVW/AUTOMATION.md"
  - "FCVW/RELEASE.md"
depends_on: []
---

# Retrieval precision, routing evidence and continuous validation

## Description

Implement the user's approved optimization sequence and publish V0.18.0.

## Justification and objective

Fix accidental exact-only matches, make required context explainable, evaluate
retrieval quality and remove redundant work without enabling learned selection.

## Scope

Exact matching, CI, reproducible labeled benchmark, structured mandatory routes,
chunk identity and optional budget selection, larger shadow candidate pool,
shared graph inventory, documentation, future-work issues and release assets.
Learning and production adaptive assist remain deferred to tracked issues.

## Affected files or boundaries

Retrieval/index/graph tools, regression tests, repository CI, context and AI
contracts, README, inventories, framework release and migration records.

## Implementation plan

1. Fix exact identity and add regression cases.
2. Add read-only CI and installed-package validation.
3. Add labeled benchmark and quality metrics.
4. Derive explainable routes from canonical Markdown and select bounded chunks.
5. Reuse graph reads, measure changes, publish issues and the release.

## Proportionality gate

- Real problem and root cause: substring matches and manual-only validation.
- Necessary in current scope: expressly requested reliability and context efficiency.
- Existing codebase solution checked: BM25, graph builders, cache and packager reused.
- Native platform capability checked: Python standard library and GitHub Actions.
- Installed dependency checked: no runtime dependency added.
- New code or complexity justified: routing, benchmark and package verification have distinct responsibilities.
- Minimum non-trivial behavior tests: false exact matches, routing union, bounded chunks, cache parity and installed validation.
- Deliberate simplification and limitations: no semantic classifier or learned production selection.
- Condition for future evolution: independently labeled task outcomes and quality non-inferiority.
- Mandatory safeguards preserved: security, ownership, traceability, regression and rollback.

## Acceptance criteria

- [ ] Incidental substrings cannot activate exact-only records.
- [ ] Structured routes are cumulative, explained and source-derived.
- [ ] Context chunks retain identity and respect optional budgets.
- [ ] Benchmark reports labeled quality and measured cost without invented outcomes.
- [ ] CI, clean installations and release assets pass checks.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

Retrieval ordering, filtering, mandatory context, graph semantics, CLI output,
installed paths, source trust and release ownership.

### Regression contracts consulted

- [AI](../../AI.md), [context map](../../CONTEXT_MAP.md),
  [tests](../../TESTS.md), [regression guards](../../REGRESSION_GUARDS.md).

### Regression checks required

- Baseline suite, adversarial identity/routing cases, budget and chunk invariants,
  graph parity, benchmark replay, CI matrix and extracted-asset validation.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Baseline | pass | 198 tests before modification. |
| Candidate | pending | Focused and full checks before completion. |

### Limitations and residual risk

Synthetic labels do not prove task execution quality. Structured event inputs
remain caller-owned; missing semantic events cannot be inferred with certainty.

## Validation plan

Run source and installed suites, labeled benchmark, governance, locale parity,
artifact checksums and CI. Compare structural outputs and cold/warm timings.

## Rollback

Omit new optional selection and routing arguments; disable repository CI by
removing its workflow. Reinstall V0.17.0 by ownership if required, preserving
project records. Exact-match correction intentionally stays stricter.

## Gates and approvals

User explicitly approved implementation, future-work GitHub issues, README
update and release publication. Scenario 3 CI uses contents-read permissions,
no secrets, immutable action pins, bounded runtime and failure propagation.
Evidence lives in CI logs; failures block release, not by changing branch rules.

## Related records

- [Framework releases](../../framework-releases/README.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Final validation | pending | Recorded before completion. |

## Gaps and residual risk

Real-task efficacy, persistent learning and adaptive production assist require
separate evaluation and are recorded as GitHub issues rather than enabled.
