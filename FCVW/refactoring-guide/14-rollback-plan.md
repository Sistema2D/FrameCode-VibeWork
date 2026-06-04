# 14 — Rollback Plan

This file defines how to plan safe rollback of refactorings when there is a failure, instability, regression, or unexpected impact.

## Objective

Ensure that every relevant refactoring is reversible without improvisation.

## Governance rule

> Medium, high, or critical risk refactorings must have a rollback plan registered before merge. Critical refactorings must have the rollback tested or simulated.

## Rollback types

| Type | When to use | Observation |
|---|---|---|
| `git revert` | Purely structural refactoring, without data migration. | Preferable for low/medium risk. |
| Rollback via previous release | When deploy allows reverting artifact/version. | Requires available previous version. |
| Feature flag | When the change can be turned on/off. | Ideal for high/critical risk. |
| Compatibility adapter | When old and new APIs coexist. | Reduces impact on consumers. |
| Reversible migration | When there is a database/persisted data. | Must include reversal script or compensatory strategy. |
| Reversible configuration | When change depends on env/config. | Record key, old value, and new value. |
| Corrective hotfix | Last resort when complete rollback is unfeasible. | Requires approval and exception record. |

## What the plan must contain

- previous safe version/commit;
- exact scope of the change;
- signals that trigger rollback;
- person responsible for the decision;
- reversal steps;
- validation after reversal;
- risks of reverting;
- estimated reversal time;
- necessary communication;
- plan to preserve data, if applicable.

## Criteria that trigger rollback

Rollback must be considered when the following occurs:

- failure in critical flow;
- error increase in production;
- relevant performance degradation;
- public contract break;
- build/deploy failure not quickly resolved;
- data inconsistency;
- authentication/authorization failure;
- user complaints in directly affected flow;
- divergent behavior without identified cause.

## Rules for database changes

1. Do not remove column/field used by previous version in the same release.
2. Prefer expand/contract migrations.
3. Maintain compatibility between old and new version during transition window.
4. Have backup or snapshot when risk is high/critical.
5. Validate migration in representative environment.
6. Define strategy for data created by the new version.

## Rules for APIs and integrations

1. Do not break contract without versioning or communication.
2. Temporarily preserve old endpoints/methods when there are external consumers.
3. Record known consumers.
4. Test compatibility with old and new payload.
5. Have adapter or fallback when possible.

## Validation after rollback

After reverting, execute:

- build;
- smoke test;
- affected flow test;
- log/error check;
- data validation, if applicable;
- stabilization communication.

## Applicable template

Use [`../governance/TEMPLATE_REFACTORING_ROLLBACK_PLAN.md`](../governance/TEMPLATE_REFACTORING_ROLLBACK_PLAN.md).
