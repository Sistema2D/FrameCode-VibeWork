# 09 — Refactoring Pull Request Checklist

Use this checklist before opening, reviewing, or approving any refactoring PR.

## Identification

```markdown
- [ ] The PR is pure refactoring, with no new feature or rule.
- [ ] The refactoring scenario was identified.
- [ ] The applicable governance file was cited.
- [ ] The related code smell was informed, when applicable.
- [ ] The scope is delimited and didn't grow during the change.
```

## Functional safety

```markdown
- [ ] Tests were executed before the change, when existing.
- [ ] Characterization tests were created when there wasn't enough coverage.
- [ ] Tests were executed after the change.
- [ ] The affected critical flows were validated.
- [ ] There was no intentional change of observable behavior.
```

## Refactoring quality

```markdown
- [ ] The change reduced complexity, duplication, coupling, or ambiguity.
- [ ] The new names reflect intent and domain vocabulary.
- [ ] Responsibilities became more cohesive.
- [ ] Encapsulation was preserved or improved.
- [ ] No speculative abstraction was created.
- [ ] There was no unjustified increase in indirection.
```

## Contracts and compatibility

```markdown
- [ ] Public APIs were preserved or have a migration plan.
- [ ] Changed public signatures were approved by the module owner.
- [ ] Persistence, serialization, routes, events, and integrations were verified.
- [ ] Frameworks that use reflection/annotations/conventions were considered.
```

## Evidence in PR

```markdown
- [ ] The PR describes before/after in objective language.
- [ ] The PR lists affected files/modules.
- [ ] The PR informs tests executed and result.
- [ ] The PR describes residual risks.
- [ ] The PR informs rollback strategy.
```

## Review

```markdown
- [ ] Reviewer confirmed that the applied technique matches the scenario.
- [ ] Reviewer verified that the change could be reverted without structural damage.
- [ ] Reviewer evaluated if a simpler technique would solve the same problem.
- [ ] Module owner approved, if the risk is medium or high.
- [ ] QA/functional validation approved, if there's any critical flow affected.
```

## PR description template

```markdown
## Type
Pure refactoring

## Scenario
E.g.: Long Method / Extract Method

## Governance file used
E.g.: 02-composing-methods.md

## Motivation
Explain the observed maintenance problem.

## Performed change
Explain what changed structurally, without focusing on feature.

## Preserved behavior
Explain why the external behavior remains the same.

## Executed tests
- [ ] Unit
- [ ] Integration
- [ ] E2E
- [ ] Controlled manual

## Risks
List residual risks.

## Rollback
Explain how to revert.
```
## Additional checklist for large codebases

- [ ] Module inventory filled when the change goes beyond local scope.
- [ ] Risk matrix filled.
- [ ] Dependencies and impact map attached.
- [ ] Characterization tests created for legacy code or without coverage.
- [ ] Pipeline executed with gates applicable to the risk level.
- [ ] Rollback plan registered.
- [ ] Incremental plan defined for broad changes.
- [ ] PR does not mix refactoring with feature, bugfix, or rewrite without justification.
- [ ] Stopping criteria known by the team.
- [ ] Refactoring PR template filled.
