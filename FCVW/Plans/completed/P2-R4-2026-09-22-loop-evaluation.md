---
schema: "fcvw/plan@2"
id: "P2-R4-2026-09-22-loop-evaluation"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P2"
risk: "R4"
created_at: "2026-09-22"
updated_at: "2026-09-22"
current_version: "V0.18.0"
expected_version: "V0.19.0"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "FCVW/SCHEMAS.md"
  - "FCVW/AI.md"
  - "FCVW/SECURITY.md"
  - "FCVW/TESTS.md"
  - "FCVW/REGRESSION_GUARDS.md"
depends_on: []
---

# Local validated-completion evaluation

## Description

Implement [issue 55](https://github.com/Sistema2D/FrameCode-VibeWork/issues/55): a frozen evaluation protocol, local loop-run aggregation, retrieval/quality metrics, reproducible reports and an external pilot on concrete framework tasks. The user confirmed no dataset exists and requested that this task produce it.

## Justification and objective

Existing retrieval benchmarks describe ranking and caller-supplied outcomes, not the full execution cycle. Measure completion cost without treating missing data, interrupted tasks or unchanged shadow delivery as improvement.

## Scope

Optional standard-library schemas/tool, bounded tests, protocol template/documentation, a separately retained real-repository audit pilot and release preparation notes. No learning, active adaptive assistance, paid infrastructure, model execution service or automatic promotion. Full causal efficacy remains conditional on genuine comparable runs and measurement availability.

## Affected files or boundaries

Loop input/output contract, source/installed tools, evaluation provenance, schemas, test policy, catalogs, migration and external pilot evidence. Existing retrieval/default routes and QA decision requirements are preserved.

## Implementation plan

1. Freeze metric semantics, cohort/label provenance and run identity rules.
2. Validate explicit local inputs; deduplicate resumed records and reject conflicting identities.
3. Calculate completion, rework, failure, context and quality metrics with denominators and missingness.
4. Compare strategies descriptively with matched pairs, uncertainty and explicit evidence gaps; never auto-promote.
5. Build a labeled pilot from concrete repository audits before retrieval replay; preserve execution and attribution limits.
6. Exercise error/recovery workflows, installed layout, regression and governance, then record actual coverage.

## Proportionality gate

- Existing benchmark remains authoritative for retrieval-only replay and its labels.
- Distinct loop/run units justify a separate opt-in aggregator and a small input-contract module; no background instrumentation.
- Python standard library only; no network, model runner, weight updates or canonical writes.
- Minimum checks: missing tokens, duplicates/conflicts, resumption, incomplete tasks, false completion, quality violations, shadow attribution and unsafe output paths.
- No synthetic test can prove task efficacy; retain negative/inconclusive results and reviewer limitations.

## Acceptance criteria

- [x] Versioned protocol/run contracts and compatible local CLI are documented and tested.
- [x] TVC, IVC, RTR, FPVR, TTVS, RFR and UCTR distinguish unknown, estimated, measured and not-applicable data.
- [x] All planned runs, interrupted tasks and late-quality observations remain visible; mandatory misses and forbidden hits fail checks.
- [x] Shadow proposals and actual delivery are separated; comparisons disclose pairing/coverage limits and cannot authorize promotion.
- [x] An external repository pilot retains frozen labels, commands, revision, outputs and actual measurement gaps.
- [x] Existing retrieval, QA, source and installed behavior pass proportionate regression checks.

## Dependency validation

None. Issues 56 and 57 consume this evidence but are not implemented or authorized here.

## Regression impact

### Existing behaviors that may be affected

Benchmark formats, mandatory routing, optional context selection, privacy boundaries, installed packaging, clean-template ownership and QA consultation.

### Regression contracts consulted

[Schemas](../../SCHEMAS.md), [AI](../../AI.md), [security](../../SECURITY.md), [testing](../../TESTS.md), [ownership](../../OWNERSHIP.md) and [regression guards](../../REGRESSION_GUARDS.md).

### Regression checks required

Focused mathematical/negative fixtures, CLI and resume replay, privacy/input/output boundaries, full local source/installed tests and unchanged default retrieval.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Metric math, evidence and resource boundaries | 24 focused tests pass | Missing/estimated tokens, resumption/conflicts, unasked QA decisions, shadow attribution, limits and real CLI roundtrip. |
| Source and installed regression | 273 tests pass on each of Python 3.12.10 and 3.14.2, Windows | outputs/loop-evaluation-validation/20260922T232742Z-982c6994/report.json |
| Governance and existing benchmark | Pass on both runtimes | Same local report; source tree unchanged during checks. |
| Real-repository audit pilot | 24/24 bounded audits pass; evaluation gate fails | outputs/loop-evaluation-pilot/20260922T232407Z/report-final.json; preserve the negative shadow proposal and UI recall loss. |
| Recovery and default delivery | 24 duplicates ignored; eight shadow deliveries exactly match baseline | Pilot aggregation-validation.json; no retriever or default route was changed. |

### Limitations and residual risk

Declared provenance is not independent attestation. This host may not expose task-scoped provider token usage or permit isolated model repetitions. The pilot must state these limits instead of fabricating measurements or claiming general non-inferiority. No supplied independent dataset exists; labels are authored from source requirements before retrieval and that reviewer limitation remains visible.

## Validation plan

Exact-value fixtures and malformed inputs, real-repository pilot outside the clean source, full local checks and final governance. Test rollback by omitting the optional tool and preserving existing benchmark output/commands.

## Rollback

Stop invoking the optional evaluator or revert its tools/contracts. Preserve external run evidence; do not delete application records. Existing retrieval/check commands remain usable without a loop protocol or cache.

## Gates and approvals

Explicit authorization to implement issue 55 and create its initial dataset. References are inert; no supplied strings execute. CLI output cannot overwrite inputs or canonical files. Sensitive evidence remains external and requires deliberate sanitized references. No application rule is changed in this clean framework.

## Related records

[V0.19.0 preparation](../../framework-releases/V0.19.0.md), [decision](../../decisions/ADR-0008-loop-evaluation.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Free local runner | Pass; no hosted CI dependency | outputs/loop-evaluation-validation/20260922T232742Z-982c6994/report.json |
| Pilot protocol integrity | Frozen hashes and source snapshot unchanged | outputs/loop-evaluation-pilot/20260922T232407Z/frozen-input-hashes.json |
| Negative experimental gate | Expected exit 1, invariant_violation | One pilot-forbidden public catalog proposed in ai-shadow; no forbidden actual delivery. |

## Gaps and residual risk

The implementation and pilot do not automatically satisfy the issue's empirical efficacy gate or enable issues 56/57. Record whether evidence is sufficient, inconclusive or violating invariants, with actual outstanding conditions.


## Pilot results and issue status

The implementation/initial-pilot scope is complete; issue 55 remains open for its
stronger empirical acceptance criteria. Eight tasks span security, migration, AI,
UI, refactoring, documentation, release and troubleshooting. Documentation and
refactoring are adjustment tasks; the other six are evaluation tasks. One repetition
and three configurations yield 24 audits. Labels and exact commands were frozen
before retrieval; the implementer authored the labels, so they are not independent.

All bounded audit commands passed, but the experimental gate failed. Mandatory
recall is 100% on actual deliveries; forbidden actual hits are zero. The shadow AI
proposal includes FCVW/Plans/completed/README.md#document, forbidden by the pilot's
task-specific labels. It is a public catalog, not secret content or an improperly
unlocked archived plan. Retain the original label and result; do not present it as
a security-policy failure or remove it after observing the ranking.

Budgeted UI useful recall fell from 1.0 to 0.5; mean evaluation recall fell from
0.3889 to 0.3056. Shadow actual delivery exactly matches baseline in all eight tasks.
No claimed improvement is justified by fewer estimated excerpt tokens. The pilot
does not contain model-driven development runs; internal audit fixtures remain
synthetic, even though the audited contracts are actual repository behavior.

TVC/RTR/monetary cost are unavailable. There is no current task-scoped provider
usage, independent label review, sufficient agent-execution sample, human-correction
observation or completed 24-hour follow-up. Historical session token records are
not measurements of these runs and were not imported. Issues 56/57 remain gated.

The external pilot retains source snapshot, index, protocol, labels, analysis,
commands, harness and outputs. The frozen evaluator report remains report.json;
report-final.json reaggregates the same evidence with the final UCTR denominator
clarification. No labels or observed runs were rewritten. RESUMO.md explains limits.
Release V0.19.0 remains in preparation; this work does not claim a new publication.
