---
schema: "fcvw/plan@2"
id: "P2-R4-2026-09-16-connectome-shadow-routing"
artifact_role: "record"
upgrade_strategy: "preserve"
record_scope: "framework"
retrieval_scope: "exact_only"
status: "completed"
priority: "P2"
risk: "R4"
created_at: "2026-09-16"
updated_at: "2026-09-16"
current_version: "V0.16.0"
expected_version: "V0.17.0"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "AGENTS.md"
  - "FCVW/CONTEXT_MAP.md"
  - "FCVW/AI.md"
  - "FCVW/SECURITY.md"
  - "FCVW/TESTS.md"
  - "FCVW/RELEASE.md"
depends_on: []
---

# Connectome feasibility and optional shadow routing

## Description

Evaluate the supplied research and six proposed plans against V0.16.0; deliver
a bounded structural experiment through the existing retriever and V0.17.0.

## Justification and objective

Signed graph propagation is absent from BM25. Measure it without changing the
context delivered to agents or claiming unmeasured token or quality benefits.

## Scope

Include deterministic build/analyze/shadow/compare, synthetic boundary fixtures,
feasibility decision, migration, documentation, clean packages and publication.
Exclude plastic learning, production assist, automatic promotion, SNN runtime,
biological datasets, and implementation of unproven later research phases.

## Affected files or boundaries

The retrieval module and a small optional router; tests; AI, token, schema and
test contracts; ADR, indexes, release record, framework lock and generated inventories.

## Implementation plan

1. Preserve pre-change suite and retrieval evidence.
2. Add optional signed propagation and topology analysis using existing graphs.
3. Replay authority, exclusion, malformed-state and deterministic boundaries.
4. Validate source and installed packages, rehearse disabled rollback, publish.

## Proportionality gate

- Real problem and root cause: lexical ranking cannot evaluate signed relationships.
- Necessary in current scope: an isolated experiment tests the supplied hypothesis.
- Existing codebase solution checked: BM25, mandatory_paths and typed graph reused.
- Native platform capability checked: Python standard library is sufficient.
- Installed dependency checked: no dependency added.
- New code or complexity justified: bounded propagation and inspectable comparison.
- Minimum non-trivial behavior tests: mandatory immunity, exclusion, fallback, CLI parity.
- Deliberate simplification and limitations: disabled by default; shadow output only.
- Condition for future evolution: independent held-out quality and usefulness labels.
- Mandatory safeguards preserved: authority, privacy, validation, traceability and rollback.

## Acceptance criteria

- [x] Disabled CLI preserves baseline output; shadow preserves delivered results.
- [x] Mandatory paths cannot be pruned or scored by the optional layer.
- [x] Signed propagation is bounded, deterministic and explained.
- [x] Graph build/analyze and comparison are available without external dependencies.
- [x] Source and clean installed fixtures pass governance and regression checks.

## Dependency validation

None. Supplied plans are research inputs, not adopted dependency records.

## Regression impact

### Existing behaviors that may be affected

BM25 ordering, typed graph semantics, exact-only/excluded retrieval, mandatory
path reporting, source trust, portable installation and release ownership.

### Regression contracts consulted

- [Context map](../../CONTEXT_MAP.md), [AI](../../AI.md),
  [regression guards](../../REGRESSION_GUARDS.md), [release](../../RELEASE.md).

### Regression checks required

- Baseline full suite; CLI comparison; negative authority/exclusion cases;
  invalid graph fallback; bounded deterministic scoring; source and installed validation.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Baseline and changed behavior | pass | 178 pre-change tests; 198 source and installed tests. |
| CLI and rollback | pass | Eight synthetic session families preserve delivered results and mandatory paths; disabled CLI is byte-equivalent. |
| Performance | pass | Eight queries, five repetitions: baseline median 26–29 ms; shadow adds 154–161 ms on Python 3.14.6 / Windows. |

### Limitations and residual risk

Synthetic fixtures establish software invariants only. Framework maintainer owns
held-out real-task evaluation before learning or production assist is proposed.

## Validation plan

Run all unittest suites, source validator, graph/manifest/queue generators,
installed-layout checks. Language parity and publication evidence are tracked by the release record. Record measurements without claiming efficacy.

## Rollback

Omit --adaptive-mode shadow to restore the original retrieval path. No persistent
learning or migration exists. Revert this feature commit or reinstall V0.16.0 by
ownership, preserving project profiles and records. Replay baseline parity.

## Gates and approvals

R4 security review covers untrusted graphs, path escape, injection, exclusion and
bounded work. User explicitly authorized implementation in the repository and a
new release. No new permission or delegated agent is required.

## Related records

- [Framework releases](../../framework-releases/README.md)

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Implementation validation | pass | python -B -m unittest discover -s tools -p test_*.py: 198 tests. |
| Source and installed governance | pass | clean-template: errors=0 warnings=0 findings=0. |
| Scope and security review | pass | No learning, imported adaptive cache, production mutation, dependency or external dataset; bounded negative-case replay. |

## Gaps and residual risk

No real-task efficacy or automatic semantic event classification is claimed.
