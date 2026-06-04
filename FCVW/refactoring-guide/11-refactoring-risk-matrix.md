# 11 — Refactoring Risk Matrix

This file defines how to classify the risk of each refactoring and which controls should be applied before, during, and after the change.

## Objective

Reduce the risk of breakage in large codebases through an objective assessment of impact, complexity, and test protection.

## Governance rule

> Every refactoring must have its risk classified before the first relevant commit. The risk level defines tests, approvals, maximum PR size, and rollback requirements.

## Risk factors

Score each factor from 0 to 3.

| Factor | 0 points | 1 point | 2 points | 3 points |
|---|---|---|---|---|
| Physical scope | 1 file | 2–5 files | 6–20 files | More than 20 files |
| Logical scope | Local method/function | Class/component | Module | Multiple modules |
| Exposure | Internal and private | Shared internal | Public internal API | External API/public contract |
| Test coverage | High | Medium | Low | Absent |
| Functional criticality | Low | Medium | High | Critical |
| Coupling | Low | Medium | High | Unknown/high and unmapped |
| Persisted data | Does not change | Read only | Write/serialization | Migration/persisted model |
| Integrations | None | Internal | External service | Critical external service |
| Concurrency/asynchronous | Not applicable | Low usage | Jobs/events | Critical concurrent flow |
| Build/deploy | Does not affect | Affects locally | Affects pipeline | Affects release/deploy/runtime |

## Risk level calculation

| Total score | Level | Interpretation |
|---:|---|---|
| 0–5 | Low | Local, reversible, and well-protected refactoring. |
| 6–12 | Medium | May affect module or internal consumers. |
| 13–20 | High | May cause relevant regression or require coordination. |
| 21–30 | Critical | May affect production, public contract, data, or multiple modules. |

## Controls per level

| Level | Mandatory actions |
|---|---|
| Low | Small PR; local tests; PR checklist; rollback by revert. |
| Medium | Module inventory; characterization tests; full CI; 1 technical reviewer. |
| High | Dependency map; incremental plan; rollback plan; integration/regression tests; 2 reviewers, 1 being an owner. |
| Critical | Formal technical approval; change window; feature flag when applicable; smoke test; validated rollback; post-merge monitoring. |

## Blocking rules

Refactoring must be blocked when any of the following conditions occur:

- complete absence of tests in a critical area;
- unknown technical owner for a critical module;
- unmapped public dependencies;
- functional change mixed with refactoring;
- non-existent rollback plan for high or critical risk;
- database change without reversible migration or compensatory strategy;
- PR too large for effective review.

## Strategies to reduce risk

| Identified risk | Mitigation action |
|---|---|
| Many files | Divide by module, layer, or functional flow. |
| Low coverage | Create characterization tests before changing. |
| Public API | Preserve compatibility, create an adapter, or do gradual deprecation. |
| Circular dependency | Break into stages: interface, adapter, migration, cleanup. |
| Legacy code without owner | Define temporary owner and approve limited scope. |
| Persisted data | Create migration, backup, rollback, and validation plan. |
| Multiple consumers | Create consumer map and prior communication. |

## Evidence required in the PR

```markdown
### Refactoring risk
- Total score:
- Risk level:
- Highest weight factors:
- Mitigations applied:
- Test evidence:
- Rollback strategy:
- Mandatory approvers:
```

## Applicable template

Use [`../governance/TEMPLATE_REFACTORING_RISK_MATRIX.md`](../governance/TEMPLATE_REFACTORING_RISK_MATRIX.md).
