# 18 — Behavioral Refactoring vs. Rewrite

This file helps separate pure refactoring from a fix, feature, behavioral change, and rewrite.

## Principle

> Refactoring alters the internal structure without altering observable behavior. If the behavior changes, the change must be treated as a fix, feature, or partial rewrite, not as pure refactoring.

## Change classification

| Type | External behavior changes? | Example | How to treat |
|---|---|---|---|
| Pure refactoring | No | Extract method, move class while maintaining API. | Refactoring PR. |
| Preparatory refactoring | Not now | Create interface/adapter for future feature. | Refactoring PR with clear motivation. |
| Fix | Yes | Fix calculation, rule, or validation. | Separate bugfix PR. |
| Feature | Yes | Add new flow, field, endpoint. | Separate feature PR. |
| Partial rewrite | Might change | Replace legacy module with new implementation. | Formal plan with compatibility and validation. |
| Total rewrite | Yes/high risk | Replace entire system or subsystem. | Separate project, not just refactoring PR. |

## Signs it is not pure refactoring

- changes returned result;
- changes layout or user flow;
- changes business rule;
- changes API payload;
- changes database schema;
- changes permission/authorization;
- changes error handling;
- intentionally and measurably changes performance;
- removes old behavior;
- adds new functional dependency;
- alters configuration necessary to operate.

## When to separate PRs

Always separate when there is:

- bugfix along with structural cleanup;
- change of public contract;
- database alteration;
- dependency update;
- pipeline alteration;
- visual change;
- new functionality;
- behavior alteration in an existing test.

## Recommended order

When a feature depends on structural cleanup:

1. PR 1 — characterization tests;
2. PR 2 — preparatory refactoring without changing behavior;
3. PR 3 — feature/fix;
4. PR 4 — post-feature cleanup, if necessary.

## When to accept an exception

Only accept mixing refactoring and fix when:

- the fix is minimal and unavoidable to make the test reliable;
- the old behavior was clearly defective and was documented;
- the reviewer explicitly agreed;
- the PR describes exactly what changed.

## Decision: refactor or rewrite?

| Situation | Preference |
|---|---|
| Code works, but is hard to maintain. | Refactor incrementally. |
| Code has isolated bugs and acceptable architecture. | Fix and refactor in stages. |
| Code has no tests, but behavior is critical. | Create characterization before any decision. |
| Code depends on obsolete and unsupported technology. | Plan incremental replacement. |
| Code no longer meets the domain and requires new logic. | Partial rewrite/feature project, not pure refactoring. |
| Entire system is unmaintainable. | Evaluate rewrite as a separate project, with migration. |

## Evidence in the PR

```markdown
### Nature of the change
- Type: pure refactoring / preparatory / fix / feature / partial rewrite
- External behavior altered? Yes/No
- Evidence of behavior preservation:
- Functional changes, if any:
- Justification for keeping in the same PR, if applicable:
```
