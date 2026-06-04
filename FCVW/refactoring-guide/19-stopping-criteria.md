# 19 — Stopping Criteria

This file defines when to stop, divide, replan, or revert a refactoring.

## Objective

To prevent a refactoring from continuing even when signs show increased risk, loss of control, or unexpected impact.

## Governance rule

> The team must stop refactoring when the actual risk exceeds the approved risk, when the behavior becomes uncertain, or when validation cannot keep up with the change.

## Technical stopping criteria

Stop immediately when:

- previously green tests start failing without a clear cause;
- build breaks in areas outside the scope;
- relevant unmapped dependencies arise;
- PR grows larger than planned;
- change requires altering an unforeseen public contract;
- observed behavior diverges from characterization tests;
- there is data loss or inconsistency in the test environment;
- performance degrades significantly;
- review shows that the change has become a rewrite;
- automatic tool altered unexpected files.

## Organizational stopping criteria

Stop when:

- technical owner is not available to approve;
- change window has ended;
- another team depends on the affected area;
- there is a critical release in progress;
- there is an active incident related to the module;
- the objective of the refactoring is no longer clear.

## Actions after stopping

| Situation | Action |
|---|---|
| Small and localized failure | Fix within the same PR, if it does not alter scope. |
| Scope increased | Pause, update risk, and divide PR. |
| Unmapped dependency | Update impact map before continuing. |
| Behavior breakage | Revert the last increment and review tests. |
| PR became feature/rewrite | Separate into a new plan and new PR. |
| Failure in production | Trigger rollback plan. |

## Possible states

| State | Meaning |
|---|---|
| Continue | Controlled risk and sufficient validation. |
| Pause | Uncertain risk; requires analysis. |
| Divide | Scope larger than reviewable. |
| Replan | Assumptions have changed. |
| Revert | Change is not safe or broke behavior. |
| Cancel | Benefit does not outweigh risk/cost. |

## Stopping checklist

When stopping, record:

- reason;
- affected commit/PR;
- evidence;
- new risk;
- decision made;
- responsible person;
- next action;
- deadline for re-evaluation.

## Resumption

Refactoring can only be resumed when:

- cause of the stop has been understood;
- risk has been reclassified;
- tests have been adjusted or added;
- scope has been reduced, if necessary;
- owner approved the resumption;
- rollback plan remains valid.

## Decision record

Use ADR when the stop results in an architectural change, module replanning, approach replacement, or relevant cancellation.

Recommended template: [`../governance/TEMPLATE_REFACTORING_ADR.md`](../governance/TEMPLATE_REFACTORING_ADR.md).
