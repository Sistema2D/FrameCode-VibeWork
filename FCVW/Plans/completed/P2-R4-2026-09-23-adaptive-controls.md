---
schema: "fcvw/plan@2"
id: "P2-R4-2026-09-23-adaptive-controls"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P2"
risk: "R4"
created_at: "2026-09-23"
updated_at: "2026-09-23"
current_version: "V0.18.0"
expected_version: "V0.19.0"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "FCVW/AI.md"
  - "FCVW/SECURITY.md"
  - "FCVW/DATA.md"
  - "FCVW/SCHEMAS.md"
  - "FCVW/TESTS.md"
depends_on: []
---

# Governed adaptive experiments and disposition of issues 55–57

## Description

Implement the remaining technical surfaces of issues 55, 56 and 57 and close the
issues with explicit evidence and disposition, as requested by the user. Closure
must not manufacture empirical efficacy or treat a rejected promotion as approved.

## Justification and objective

The loop evaluator exists, but there is no executable bounded feedback lifecycle,
assistance control or reproducible decision gate. Add those controls while retaining
the negative initial pilot and refusing activation without adequate evidence.

## Scope

Optional local control, evidence assessment, reversible feedback replay, explicit
selection, stagnation and rollback, CLI integration, tests and documentation.
No provider runner, autonomous promotion, paid service, default learning, new agent,
or application modification. Empirical claims remain limited to observed evidence.

## Affected files or boundaries

Existing retriever and loop evaluator, optional adaptive modules and external JSON
contracts, schemas, indexes, README, ADR and V0.19.0 preparation record.

## Implementation plan

1. Define frozen experiment, evidence decision, feedback and state contracts.
2. Reuse loop evaluation to reject missing evidence and quality inferiority.
3. Implement bounded explicit updates, deterministic replay/export/reset/rollback.
4. Add opt-in assistance, preserving eligibility and mandatory routes; block on QA
   decisions, safety incidents and stagnation before another selection.
5. Rehearse positive synthetic paths and adversarial/rollback paths; reassess the
   real pilot without relabeling it or claiming token savings.
6. Validate source and installed layouts, document scope and close issues truthfully.

## Proportionality gate

Reuse BM25, structural scoring, complete-chunk selection and loop metrics. Small
standard-library modules provide explicit invocations, not a scheduler or second
agent runtime. No default path loads learned state. Evidence and control files are
caller-supplied declarations, never authentication or proof of independent review.

## Acceptance criteria

- [x] Optional feedback is bounded, deduplicated, traceable, reversible and unable to train on holdout or unvalidated outcomes.
- [x] Assistance requires explicit scoped control/evidence, preserves mandatory context and uses safe deterministic fallback.
- [x] QA/safety/stagnation blocks survive rollback; reactivation requires a new reviewed control.
- [x] Metric gate exposes insufficient or inferior evidence and never automatically promotes a strategy.
- [x] Source/installed regressions and adversarial replays pass with documented limits.
- [x] Issues receive verified closure with implementation/evidence links and honest treatment of unmet empirical claims.

## Dependency validation

The tools from issue 55 are implemented. Its pilot is negative and insufficient for
live adaptive activation; this remains an enforced gate, not an assumed dependency pass.

## Regression impact

### Existing behaviors that may be affected

Default and shadow delivery, exact-only/excluded content, cumulative routes, budget
selection, source/installed packaging, QA decision gates and loop metric consumers.

### Regression contracts consulted

AI, SECURITY, DATA, OWNERSHIP, SCHEMAS, TESTS and REGRESSION_GUARDS; ADR-0006/0008.

### Regression checks required

CLI default parity; absent/corrupt/expired state; feedback poisoning/conflicts;
holdout isolation; source drift; budget/mandatory/exclusion guards; repeated failure;
reset/replay/rollback; evidence gate; source/installed full suite and governance.

### Regression evidence

| Protected behavior | Result | Evidence |
|---|---|---|
| Default/shadow eligibility, mandatory routes and installed compatibility | Pass: 295 source and installed tests on Python 3.12.10 and 3.14.2, Windows | outputs/adaptive-controls-validation/20260923T101455Z-31407eeb/report.json |
| Explicit adaptive state and runtime lifecycle | Pass: 22 focused tests, including actual-source CLI activation/fallback/rollback with synthetic approval | Same local report; no synthetic approval installed in the repository. |
| Governance, legacy benchmark and source integrity | Pass on both runtimes | Same report; source unchanged during checks. |
| Default CLI parity | Seven paired subprocess outputs exactly equal | outputs/adaptive-controls/20260923T101231Z/default-parity.json |
| Negative real-pilot assessment | Expected reject/exit 1 | outputs/adaptive-controls/20260923T101231Z/cli-assessment.json |
| Unknown/estimated/partial runtime usage | Selection blocked | test_estimated_or_partial_runtime_usage_cannot_evade_budget; no fabricated token measurements. |

### Limitations and residual risk

Local hashes detect accidental drift, not malicious forgery by the operator. Explicit
review/authorization references require human verification. Synthetic replay cannot
prove causal benefit; unknown provider tokens and independent labels remain unknown.

## Validation plan

Focused boundary tests, deterministic actual-source CLI replay, immutable initial
pilot reassessment, local validation on Windows/Python 3.12 and 3.14. No Linux or
hardware efficacy claim; adapters remain platform-neutral standard-library code.

## Rollback

Omit adaptive flags or use the explicit disable control before the next selection.
Restore an exported state by validated replay, or reset to empty weights. Preserve
evidence and stop latches; switching retrieval does not undo application mutations.

## Gates and approvals

The user authorized implementation and issue closure. This does not supply missing
independent evidence or operational promotion approval. Isolation fixtures exercise
activation without enabling it in this repository. Never ask fewer QA questions to
improve cost. The operator owns external JSON retention; raw prompts are not collected.

## Related records

[V0.19.0 preparation](../../framework-releases/V0.19.0.md),
[loop evaluation](../completed/P2-R4-2026-09-22-loop-evaluation.md).

## Validation executed

Source and installed tests pass with 295 cases per runtime, including 22 new
adaptive-control cases. The free local runner also verifies governance and the
existing benchmark. Full evidence: outputs/adaptive-controls-validation/20260923T101455Z-31407eeb/report.json.

The first focused run exposed a Windows stdout-encoding mismatch in the new CLI
test and aliasing of a returned observation to its input object. The test now
requests UTF-8 explicitly; runtime snapshots deep-copy observations. Both failure
paths were replayed successfully. The subsequent review added token origin and
call-scope completeness to prevent partial/estimated runtime counts bypassing limits.

Default CLI median subprocess time in the seven-pair sample was 211.040 ms before
and 220.715 ms after; outputs were identical. The small sample does not establish
latency non-inferiority or savings. No background scan/collector was introduced.
The experiment-control path deliberately pays for source hashing, evidence replay
and structural scoring only when explicitly selected.

## Gaps and residual risk

No promise of superiority, non-inferiority or real provider savings from this implementation.


## Aegis Security Pass

- Skill loaded: [agent-aegis](../../skills/agent-aegis/SKILL.md).
- Selected hardening: derived feedback/runtime cannot silently authorize training,
  suppress QA stops or use estimated/partial counts to bypass budgets.
- Severity: hardening; scope is the new optional control, learning and retrieval boundary.
- Fix: strict schemas, reviewed identities, recomputed loop evidence, source/index
  binding, ledger replay, holdout rejection, stop latches and safe baseline fallback.
- Validation: poisoning, duplicate/conflicting evidence, forged weights with a fresh
  checksum, incomplete usage, state drift, expiry, missing/corrupt state, runtime
  history rewriting and blocked rollback all exercised by the focused/full suite.
- Knowledge update: yes, in the canonical adaptive experiment contract.
- Residual risk: local declarations and hashes are not authentication. Operators
  own the current-runtime pointer, serialize updates and verify actual reviewer
  authority. No protection against an operator fabricating the complete evidence
  set is claimed; this does not create permissions beyond existing retrieval.

## Experimental decision and issue disposition

The frozen pilot source/labels/events are unchanged. Reassessment rejects the
experiment: one task-specific forbidden public catalog was proposed in shadow,
UI useful recall degraded under the budget, provider tokens are unknown, reviewer
independence is absent and no agent-execution/late-follow-up sample exists. No
learning update or operational assist was activated on this evidence.

Technical controls are delivered. The empirical efficacy/promotion portions cannot
truthfully be marked completed. The user requested issue closure; recorded explicit
not-planned dispositions for the unfulfilled empirical campaign/promotion, retain
unchecked empirical criteria and link implemented capability/evidence. Issue closure
does not turn the missing evidence into a satisfied activation prerequisite.

The hypothesis of replacing AI reasoning by deterministic checks was not causally
measured: CLI timing includes startup but is not a with/without-model comparison.
This limitation is part of the decision to decline promotion, not a claimed saving.
Future activation requires a new independently reviewed measured campaign. No new
backlog issue, paid infrastructure or promise of unattended follow-up is created.


## Verified external closeout

Implementation pushed as [2014ad6](https://github.com/Sistema2D/FrameCode-VibeWork/commit/2014ad60ad5aec2ee3dbefb97f01950f3c74c2f5).
Issues [55](https://github.com/Sistema2D/FrameCode-VibeWork/issues/55),
[56](https://github.com/Sistema2D/FrameCode-VibeWork/issues/56) and
[57](https://github.com/Sistema2D/FrameCode-VibeWork/issues/57) were closed on
2026-09-23 with reason NOT_PLANNED, preserving their unmet empirical criteria and
recording the delivered code, validation, negative evidence and explicit decision
not to promote. This is not a declaration that every original empirical acceptance
criterion passed. Technical capabilities are retained as optional experimental tools.

GitHub responses were read back and matched the posted bodies/state/reason.
Evidence: outputs/adaptive-issue-closure/verified-closures.json and per-issue
before/after snapshots. No empirical dependency was silently waived by closure.
The framework release remains V0.19.0 in preparation; no publication is claimed.
