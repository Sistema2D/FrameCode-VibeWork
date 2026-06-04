# 17 — Branch and Pull Request Policy

This file defines rules for organizing branches, commits, Pull Requests, and approvals in refactorings.

## Objective

To keep refactorings reviewable, traceable, and reversible.

## Governance rule

> Refactoring must be proposed in a PR with a clear scope, without mixing with a feature or functional fix, except for justified and approved exceptions.

## Branch name

Recommended pattern:

```text
refactor/<module>/<short-objective>
```

Examples:

```text
refactor/auth/extract-token-validator
refactor/orders/introduce-parameter-object
refactor/ui/split-large-component
refactor/shared/encapsulate-collection
```

## Commit types

Use small and semantic commits:

```text
refactor(auth): extract token validation method
refactor(order): move pricing calculation to PricingService
test(order): add characterization tests for discount rules
chore(ci): add affected module test job
```

## Rules for commits

1. Each commit should compile whenever possible.
2. Separate test, movement, renaming, and cleanup commits.
3. Avoid "format all files" along with refactoring.
4. Messages should explain the intention, not just the altered files.
5. Tool-generated commits must be identified.

## PR Size

| Level | Guidance |
|---|---|
| Low | Small PR, simple review. |
| Medium | PR limited to one module or objective. |
| High | Divide into sequential PRs; review by owner. |
| Critical | Minimal PR, with plan, window, rollback, and formal validation. |

## Mandatory PR content

Every refactoring PR must inform:

- problem/symptom;
- code smell, if applicable;
- refactoring technique used;
- main files altered;
- justification for not altering behavior;
- executed tests;
- classified risk;
- rollback;
- relevant evidence.

## Approval

| Risk | Minimum approval |
|---|---|
| Low | 1 reviewer or module owner, according to team policy. |
| Medium | 1 technical reviewer. |
| High | 2 reviewers, including module owner. |
| Critical | Technical owner + functional/architecture lead when applicable. |

## Merge rules

Do not allow merge when:

- pipeline failed;
- there is an unresolved conflict;
- scope grew without updating the risk matrix;
- tests were removed without justification;
- there is undeclared functional alteration;
- rollback was not defined for medium or higher risk;
- review requested PR division and this was not addressed.

## Chained PRs policy

For incremental refactoring:

1. Open base PR with characterization tests.
2. Open preparation/abstraction PR.
3. Open migration PRs per module.
4. Open legacy removal PR.
5. Open final cleanup/documentation PR.

## Applicable template

Use [`../governance/TEMPLATE_REFACTORING_PULL_REQUEST.md`](../governance/TEMPLATE_REFACTORING_PULL_REQUEST.md) and copy to `.github/pull_request_template.md` in the destination repository when you want a standard PR template.
