# Refactoring Governance

Governance structure for deciding, executing, reviewing, and auditing refactorings based on the Refactoring.Guru catalog scenarios, supplemented with operational controls for large codebases.

> Core principle: refactoring improves the internal structure of the code without altering the observable behavior of the system. Every change must be small, testable, reversible, and recorded.

## How to Use

1. Start with [`01-decision-guide.md`](01-decision-guide.md) to identify the technical scenario.
2. Use [`08-code-smells-map.md`](08-code-smells-map.md) when the problem is perceived as a "code smell", but the technique is not yet clear.
3. For large codebases, first fill out [`10-code-inventory-and-classification.md`](10-code-inventory-and-classification.md), [`11-refactoring-risk-matrix.md`](11-refactoring-risk-matrix.md), and [`16-dependency-and-impact-map.md`](16-dependency-and-impact-map.md).
4. Define tests, pipeline, rollback, and an incremental plan before opening PRs with medium, high, or critical risk.
5. Use [`20-templates.md`](20-templates.md) to copy the necessary templates.
6. Use [`09-pr-checklist.md`](09-pr-checklist.md) before opening or approving a Pull Request.

## Governance Files

| File | Purpose |
|---|---|
| [`00-general-governance.md`](00-general-governance.md) | Universal rules, roles, entry and exit criteria, risks, and approval levels. |
| [`01-decision-guide.md`](01-decision-guide.md) | Decision-making guide to identify the scenario and direct to the applicable file. |
| [`02-composing-methods.md`](02-composing-methods.md) | Rules for long methods, difficult expressions, temporary variables, algorithms, and method extraction/substitution (Composing Methods). |
| [`03-moving-features-between-objects.md`](03-moving-features-between-objects.md) | Rules for moving methods/fields, extracting/inlining classes, delegation, and local extension (Moving Features between Objects). |
| [`04-organizing-data.md`](04-organizing-data.md) | Rules for encapsulation, value/reference objects, collections, arrays, type codes, and associations (Organizing Data). |
| [`05-simplifying-conditional-expressions.md`](05-simplifying-conditional-expressions.md) | Rules for complex conditionals, duplicate, nested, flags, polymorphism, null object, and assertions (Simplifying Conditional Expressions). |
| [`06-making-method-calls-simpler.md`](06-making-method-calls-simpler.md) | Rules for names, parameters, constructors, query/modifier, exceptions, and method visibility (Making Method Calls Simpler). |
| [`07-dealing-with-generalization.md`](07-dealing-with-generalization.md) | Rules for inheritance, delegation, extracting superclass/interface/subclass, template method, and collapsing hierarchy (Dealing with Generalization). |
| [`08-code-smells-map.md`](08-code-smells-map.md) | Diagnostic map by code smell, providing directions to applicable techniques. |
| [`09-pr-checklist.md`](09-pr-checklist.md) | Objective checklist for review, evidence, tests, rollback, and acceptance. |
| [`10-code-inventory-and-classification.md`](10-code-inventory-and-classification.md) | Inventory of modules, dependencies, criticality, owners, coverage, and critical points. |
| [`11-refactoring-risk-matrix.md`](11-refactoring-risk-matrix.md) | Risk scoring matrix and mandatory controls by level. |
| [`12-testing-strategy-before-refactoring.md`](12-testing-strategy-before-refactoring.md) | Testing strategy for characterization, regression, integration, contract, e2e, and smoke tests. |
| [`13-ci-cd-pipeline-and-quality-gates.md`](13-ci-cd-pipeline-and-quality-gates.md) | Minimum CI/CD and quality gates for safe merge/deploy. |
| [`14-rollback-plan.md`](14-rollback-plan.md) | Rollback strategies, triggers, and post-rollback validation. |
| [`15-incremental-refactoring-plan.md`](15-incremental-refactoring-plan.md) | Splitting large refactorings into small, reversible increments. |
| [`16-dependency-and-impact-map.md`](16-dependency-and-impact-map.md) | Mapping of direct and indirect consumers, contracts, data, events, and configuration. |
| [`17-branch-and-pull-request-policy.md`](17-branch-and-pull-request-policy.md) | Rules for branches, commits, PRs, approvals, and merges. |
| [`18-behavioral-refactoring-vs-rewrite.md`](18-behavioral-refactoring-vs-rewrite.md) | Separation between pure refactoring, feature, fix, partial rewrite, and total rewrite. |
| [`19-stopping-criteria.md`](19-stopping-criteria.md) | Criteria to pause, split, replan, revert, or cancel refactorings. |
| [`20-templates.md`](20-templates.md) | Templates index for practical application of the governance. |

## Templates

Official templates are indexed in [`../governance/README.md`](../governance/README.md). For PRs, use [`../governance/TEMPLATE_REFACTORING_PULL_REQUEST.md`](../governance/TEMPLATE_REFACTORING_PULL_REQUEST.md) and copy it to the target repository only when that repository uses pull requests.

## Technical Coverage

This governance covers the six families from the refactoring catalog:

- Composing Methods;
- Moving Features between Objects;
- Organizing Data;
- Simplifying Conditional Expressions;
- Making Method Calls Simpler;
- Dealing with Generalization.

It also includes a decision map by code smells to support the initial problem identification.

## Operational Coverage for Large Codebases

Beyond techniques, the governance now covers:

- Code inventory and classification;
- Risk matrix;
- Testing strategy before refactoring;
- Pipeline and quality gates;
- Rollback;
- Incremental plan;
- Dependency and impact map;
- Branches and PRs policy;
- Separation between refactoring and rewrite;
- Stopping criteria.

## Reference Sources

- Refactoring.Guru — Refactoring Catalog: https://refactoring.guru/refactoring/catalog
- Refactoring.Guru — Code Smells: https://refactoring.guru/refactoring/smells
