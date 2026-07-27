---
schema: "fcvw/adr@1"
id: "ADR-0003"
status: "accepted"
date: "2026-07-27"
artifact_role: "record"
owner: "framework"
upgrade_strategy: "preserve"
record_scope: "framework"
retrieval_scope: "routed"
language: "en-US"
---

# ADR-0003: Proportionality and contextual anti-monolith gates

## Context

Open issues [#46](https://github.com/Sistema2D/FrameCode-VibeWork/issues/46) and [#48](https://github.com/Sistema2D/FrameCode-VibeWork/issues/48) identify two related failures: code-oriented size limits can fragment legitimate documentation, while new abstractions, dependencies, wrappers, files, and layers may be introduced before existing or native options are checked.

## Alternatives considered

1. Create a standalone anti-overengineering skill.
2. Add one new universal blocking gate.
3. Integrate a proportionality ladder into planning, hygiene, audit, and the existing anti-monolith gate.
4. Leave the current behavior unchanged and rely on reviewer judgment.

## Decision

Use option 3.

- Classify the artifact before applying numeric anti-monolith thresholds.
- Automatically enforce size budgets only for source or executable/operational artifacts.
- Evaluate documentation, records, templates, and generated catalogs by cohesion, ownership, schema, navigation, and graph integrity.
- Permit evidence-based threshold resizing when a split could harm security, architecture, functional integrity, performance, or cognitive load.
- Before adding non-trivial complexity, check necessity, codebase reuse, native capabilities, and installed dependencies in that order.
- Preserve mandatory security, privacy, accessibility, traceability, validation, audit, compliance, integrity, documentation, and risk-based testing.

## Justification

The integrated approach covers the decision points already owned by planning, code hygiene, and anti-monolith review. A new skill would duplicate those procedures and would make the framework's own anti-overengineering mechanism more complex than necessary.

## Consequences

- Long cohesive Markdown documents no longer fail on line count alone.
- New technical complexity requires an explicit proportionality record when material.
- Exceptions remain possible but require concrete risk evidence, validation, ownership, and a revisit condition.
- Small bounded changes do not acquire a ceremonial gate.

## Skill self-improvement report

### Evidence

- Assets changed: [`anti-monolith-guard`](../skills/anti-monolith-guard/SKILL.md) and [`code-hygiene-refactor`](../skills/code-hygiene-refactor/SKILL.md).
- Drift: issue #46 demonstrates that the former size table did not classify documentary artifacts; issue #48 requires proportionality checks already adjacent to code-hygiene ownership.
- Severity: P2 framework-governance change because false blocking or needless complexity can affect every downstream project.

### Improvement metrics

| Metric | Result | Evidence |
|---|---|---|
| Failure or drift | pass | Two independent open issues identify complementary gate gaps. |
| Scope preservation | pass | Existing skills retain their owners; rules are narrowed and clarified. |
| Backward compatibility | pass | Existing triggers and output blocks remain valid with additive fields. |
| Token/risk ROI | pass | Reuses two routed skills instead of introducing a third skill and route. |
| Validation replay | pending | Source, operational Markdown, documentary Markdown, and complexity scenarios in the V0.14.0 test suite. |

## Conditions for review

- Repeated false positives remain after artifact classification.
- A real workflow cannot be covered without a distinct owner.
- Project-specific thresholds prove unsafe or materially inefficient.

## Relationships

- Active implementation plan: [P2-R5 open-issues update](../Plans/in_progress/P2-R5-2026-07-27-open-issues-42-48-and-document-graph.md).
- Governing policies: [Planning](../PLANNING.md), [Governance gates](../GOVERNANCE_GATES.md), and [Audit](../AUDIT.md).
