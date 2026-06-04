# 20 — Templates Index

This file centralizes the templates necessary to apply refactoring governance in large codebases.

## Available Templates

| Template | When to use |
|---|---|
| [`../governance/TEMPLATE_REFACTORING_OPENING.md`](../governance/TEMPLATE_REFACTORING_OPENING.md) | To formalize the start of a refactoring. |
| [`../governance/TEMPLATE_REFACTORING_MODULE_INVENTORY.md`](../governance/TEMPLATE_REFACTORING_MODULE_INVENTORY.md) | To map module, owner, criticality, dependencies, and tests. |
| [`../governance/TEMPLATE_REFACTORING_RISK_MATRIX.md`](../governance/TEMPLATE_REFACTORING_RISK_MATRIX.md) | To score and classify refactoring risk. |
| [`../governance/TEMPLATE_REFACTORING_CHARACTERIZATION_TEST_PLAN.md`](../governance/TEMPLATE_REFACTORING_CHARACTERIZATION_TEST_PLAN.md) | To record necessary tests before refactoring. |
| [`../governance/TEMPLATE_REFACTORING_ROLLBACK_PLAN.md`](../governance/TEMPLATE_REFACTORING_ROLLBACK_PLAN.md) | To plan safe rollback. |
| [`../governance/TEMPLATE_REFACTORING_DEPENDENCY_MAP.md`](../governance/TEMPLATE_REFACTORING_DEPENDENCY_MAP.md) | To map direct and indirect dependencies, and contracts. |
| [`../governance/TEMPLATE_REFACTORING_INCREMENTAL_PLAN.md`](../governance/TEMPLATE_REFACTORING_INCREMENTAL_PLAN.md) | To split large refactorings into stages. |
| [`../governance/TEMPLATE_REFACTORING_ADR.md`](../governance/TEMPLATE_REFACTORING_ADR.md) | To record architectural decisions or relevant exceptions. |
| [`../governance/TEMPLATE_REFACTORING_PULL_REQUEST.md`](../governance/TEMPLATE_REFACTORING_PULL_REQUEST.md) | To fill out refactoring PRs. |
| [`../governance/TEMPLATE_REFACTORING_POST_VALIDATION_REPORT.md`](../governance/TEMPLATE_REFACTORING_POST_VALIDATION_REPORT.md) | To record post-merge or post-deploy validation. |

## Recommended Order of Use

1. Refactoring opening.
2. Module inventory.
3. Dependency and impact map.
4. Risk matrix.
5. Test plan.
6. Incremental plan.
7. Rollback plan.
8. Refactoring PR.
9. Post-refactoring report.
10. ADR when there is a relevant technical decision.
