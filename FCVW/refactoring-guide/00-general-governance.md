# 00 — General Refactoring Governance

## Objective

Establish common rules for any refactoring, regardless of the applied technique.

## Operational Definition

A change is classified as **refactoring** when:

- It does not alter the functional behavior perceived by the user;
- It does not add a requirement, business rule, or new feature;
- It improves readability, modularity, testability, isolation, cohesion, coupling, or maintainability;
- It can be validated by automated tests, controlled manual tests, or before/after comparison.

## Mandatory Rules

1. **Do not mix refactoring with a feature.** If there is a new feature, separate it into another PR or commit.
2. **Create a baseline before the change.** Record existing tests, expected behavior, and risk points.
3. **Make small changes.** Prefer several small refactorings instead of a massive change.
4. **Preserve public APIs, unless explicitly decided otherwise.** Public changes require versioning, a migration plan, and communication.
5. **Run tests before and after.** When there are no tests, create characterization tests before refactoring.
6. **Ensure simple rollback.** The PR must allow reversion without data loss or irreversible contract alteration.
7. **Record intention.** Each PR must declare the code smell, the scenario, and the applied technique.
8. **Avoid refactoring unstable code unnecessarily.** Prioritize areas that are frequently changed, have recurring bugs, or high maintenance costs.
9. **Maintain domain names.** Do not replace terms recognized by the business with generic names.
10. **Measure impact when possible.** Cyclomatic complexity, duplication, method/class size, test coverage, and dependencies can be used as evidence.

## Roles

| Role | Responsibility |
|---|---|
| Refactoring Author | Diagnose scenario, apply technique, write tests, and document evidence. |
| Technical Reviewer | Verify preservation of behavior, architectural coherence, and adherence to this guide. |
| Module Owner | Approve changes to public contracts, data models, integrations, and critical rules. |
| QA/Validator | Validate critical flows when the functional risk is medium or high. |

## Risk Levels and Approval

| Level | Example | Minimum Requirement |
|---|---|---|
| Low | Rename private method, extract variable, remove isolated dead code. | 1 technical reviewer + local tests. |
| Medium | Extract class, move method between classes, alter internal encapsulation. | 1 technical reviewer + module owner + automated tests. |
| High | Alter public contract, class hierarchy, persisted data model, or critical flow. | 2 reviewers + module owner + rollback plan + functional validation. |

## Entry Criteria

Before starting, confirm:

- Identified problem and candidate technique;
- Delimited scope;
- Tests or characterization scenario available;
- Affected dependencies mapped;
- Known risks recorded.

## Exit Criteria

The refactoring can only be considered complete when:

- Previous behavior was preserved;
- Relevant tests passed;
- Names, responsibilities, and dependencies became clearer;
- There was no unjustified increase in complexity;
- Obsolete documentation or comments were removed or updated;
- PR checklist was completed.

## Commit Policy

Use small and semantic commits:

```text
refactor(method): extract calculation of monthly balance
refactor(data): replace type code with state strategy
refactor(api): preserve whole object in scheduling service
```

## When Not to Refactor

Do not execute refactoring when:

- There is no test, nor time to create a characterization test;
- The module will be discarded in the short term;
- The gain is merely aesthetic and increases risk;
- The change would require altering multiple consumers without a plan;
- The problem is a poorly defined business rule, not a bad code structure.

## Minimum Evidence in the PR

- Identified scenario;
- Applied technique;
- File from this governance used;
- Summarized before/after;
- Executed tests;
- Risks and rollback;
- Pending items, if any.
