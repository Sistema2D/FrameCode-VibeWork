---
schema: "fcvw/plan@2"
id: "P2-R3-2026-09-22-qa-user-decision"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P2"
risk: "R3"
created_at: "2026-09-22"
updated_at: "2026-09-22"
current_version: "V0.18.0"
expected_version: "V0.19.0"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "FCVW/skills/QA/SKILL.md"
  - "FCVW/wiki/product/README.md"
  - "FCVW/wiki/templates/TEMPLATE_QA_RUN.md"
  - "FCVW/skills/self-improvement/SKILL.md"
  - "FCVW/TESTS.md"
depends_on: []
---

# Mandatory user decisions for QA divergences

## Description

Require QA to question the user whenever expected and actual behavior diverge. Track consultation coverage and pending decisions in the selected-run checker, with a blocking decision gate.

## Justification and objective

The user explicitly requires direction to be decided by the user. Preserving failure evidence alone does not prevent an agent from choosing which behavior should prevail.

## Scope

QA procedure, product contract, run template, optional checker, tests and preparation release record. No application changes, automatic messages, new adapter or release publication.

## Affected files or boundaries

User authority over behavior; audit decision evidence; backward-readable historical runs; optional JSON output and documentation.

## Implementation plan

1. Define 100% consultation coverage and zero pending decisions before acting on a divergence.
2. Require expected/actual evidence, question reference and explicit user decision reference.
3. Infer undeclared discrepancies from failed cases so omitting a table cannot bypass the gate.
4. Test pending/answered/omitted/invalid decisions and preserve failures, hashes and unrelated routes.

## Proportionality gate

Reuse the selected-page checker and existing Markdown tables. No service or dependency. A small decision table and derived metrics make the mandatory question auditable; static validation cannot prove the user actually answered. No context cost is added to default sessions.

## Skill/Agent Self-Improvement Gate

- Skill loaded: `skills/self-improvement/SKILL.md`.
- Asset changed: QA 1.0.0 to 1.1.0; trigger family unchanged.
- Evidence: explicit user requirement changes the canonical divergence-handling rule.
- Metric passed: rule drift; existing profile lacks mandatory consultation.
- Scope preserved: QA still tests and maintains knowledge; users choose direction; implementation remains a separate handoff.
- Token/risk ROI: no savings claimed; prevents unilateral requirement changes and repairs.
- Validation replay: synthetic failed case with no question, pending answer and explicit choices.
- Decision: patch under explicit user authorization.

## Self-improvement report

This fills the [report template](../../governance/TEMPLATE_SELF_IMPROVEMENT_REPORT.md). Before: discrepancies were retained, but consultation was not mandatory. After: each divergence requires a question and user-sourced direction, measured independently from test success. Rule drift passes; recurrence, failure count and numerical token ROI are unmeasured. Scope preservation passes; unchanged triggers and additive output preserve normal passing runs. Historical failing runs remain readable but lack decision evidence and cannot authorize new actions. Changes belong to the QA procedure, product contract and run template; no catalog trigger or base route changes. Replay evidence and remaining limits are recorded below. Next review follows an actual unasked divergence or false decision attribution.

## Acceptance criteria

- [x] Every declared divergence or failed case requires user consultation.
- [x] Missing question/answer blocks dependent corrections and requirement changes; independent tests may continue.
- [x] Silence, preselected options and generic prior authorization cannot count as decisions.
- [x] User decisions never convert a historical failure into a pass; changed contracts require new testing.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

Failed-run parsing, first-run discovery, contract hashes, unknown expectations, selected-page cost and historical evidence preservation.

### Regression contracts consulted

[Product contract](../../wiki/product/README.md), [QA](../../skills/QA/SKILL.md), [tests](../../TESTS.md) and [regression guards](../../REGRESSION_GUARDS.md).

### Regression checks required

Focused decision-state negative tests, full source and installed tests, clean-template validation and unchanged unrelated context routes.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Decision state accounting | pass | 21 focused QA tests, including seven new tests for missing questions, unanswered questions, four explicit directions, invalid references/decisions, partial consultation, provisional discrepancies and no-divergence behavior. |
| Preserved outcomes and contracts | pass | Answered decisions retain fail and the original contract hash; old unknown/stale-pass guards and unrelated routing tests still pass. |
| Full source and installed checks | pass | 249 tests per layout on Windows Python 3.12.10 and 3.14.2; governance and labeled benchmark pass for each runtime. |
| Historical replay | pass | Existing synthetic browser/CLI audit remains readable; its one deliberate failure now reports 0% consultation, one unanswered decision and blocked gate, CLI exit 1. No historical file or user answer was fabricated. |

### Limitations and residual risk

The checker validates declared evidence and cannot verify conversation truth or detect an agent concealing a mismatch as a pass. The procedural requirement applies to all observed divergences on every target; no real product decision is inferred from synthetic tests.

## Validation plan

Run focused tests, the local source/installed runner and final governance checks. No new live browser replay is necessary for decision-accounting logic.

## Rollback

Revert procedure/tool changes while preserving user questions, decisions and all original QA outcomes. Do not remove downstream evidence.

## Gates and approvals

Explicit user authorization for the mandatory question rule. This task changes the framework; it does not ask the user to decide a fabricated application behavior.

## Related records

[V0.19.0 preparation](../../framework-releases/V0.19.0.md), [previous QA implementation](../completed/P2-R4-2026-09-22-product-wiki-qa.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Local runner | pass | outputs/qa-user-decision-validation/20260922T162728Z-1276e541/report.json; source identity unchanged during validation. |
| Historical gate report | pass | outputs/qa-user-decision-validation/historical-failure-gate.json. This is a structural replay, not new live execution or an actual user-decision request. |
| Documentation closeout | pass | Plan moved, queue removed, graph/manifest regenerated, final clean-template validation and diff check performed. AGENTS and context routes unchanged. |

## Gaps and residual risk

Evidence references require human/host verification. No runtime can force a noncompliant model to ask; the explicit instruction and failing gate expose declared noncompliance.
