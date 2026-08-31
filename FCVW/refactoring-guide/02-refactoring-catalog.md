# 02 — Refactoring Catalog

This file replaces the six family files that previously reproduced the classic
refactoring catalog (methods, moving features between objects, organizing data,
conditionals, method calls, and generalization).

The reproduction was removed deliberately. The catalog is public, stable
knowledge that any competent AI agent already holds; keeping it here cost about
49 KB, had to be reviewed on every release, and had to be translated into four
languages, while adding nothing to what FCVW governs. What FCVW governs is
**when** to refactor, **at what risk**, and **with what evidence** — and that
stays in this guide's policy files.

Base source: <https://refactoring.guru/refactoring/techniques>

## General family rules

These rules apply to every technique in the catalog and are the part FCVW
actually enforces:

- apply only when observable behavior can be preserved;
- prefer small steps, with tests run between each step;
- record the scenario, the technique, and the evidence that behavior did not change;
- stop refactoring if a functional change becomes necessary, and open a separate task;
- a refactoring and a behavior change never share the same batch without explicit plan scope.

## Symptom to family routing

Use this table to choose the family and then consult the source for the exact
technique. The governance column names what must exist in the active plan.

| Observed symptom | Catalog family | Mandatory FCVW governance |
|---|---|---|
| Long method, unclear expression, confusing temporary variable | Composing methods | [`11-refactoring-risk-matrix.md`](11-refactoring-risk-matrix.md) |
| Responsibility on the wrong object, feature envy, inappropriate intimacy | Moving features between objects | [`16-dependency-and-impact-map.md`](16-dependency-and-impact-map.md) |
| Public field, type code, exposed collection, bidirectional association | Organizing data | [`12-testing-strategy-before-refactoring.md`](12-testing-strategy-before-refactoring.md) |
| Complex conditional, duplicated branch, nesting, control flag | Simplifying conditional expressions | [`12-testing-strategy-before-refactoring.md`](12-testing-strategy-before-refactoring.md) |
| Poor name, long parameter list, overloaded constructor, exception used as flow | Making method calls simpler | [`09-pr-checklist.md`](09-pr-checklist.md) |
| Wrong hierarchy, duplication across subclasses, inheritance used as a shortcut | Dealing with generalization | [`18-behavioral-refactoring-vs-rewrite.md`](18-behavioral-refactoring-vs-rewrite.md) |

## Where the FCVW-specific policy lives

The rest of this guide was not condensed, because it carries its own rules
rather than reproducing literature:

- decision and inventory: [`01-decision-guide.md`](01-decision-guide.md),
  [`10-code-inventory-and-classification.md`](10-code-inventory-and-classification.md);
- risk, testing, and stopping: [`11-refactoring-risk-matrix.md`](11-refactoring-risk-matrix.md),
  [`12-testing-strategy-before-refactoring.md`](12-testing-strategy-before-refactoring.md),
  [`19-stopping-criteria.md`](19-stopping-criteria.md);
- execution and rollback: [`15-incremental-refactoring-plan.md`](15-incremental-refactoring-plan.md),
  [`14-rollback-plan.md`](14-rollback-plan.md);
- boundaries: [`18-behavioral-refactoring-vs-rewrite.md`](18-behavioral-refactoring-vs-rewrite.md).

Top-level refactoring policy stays in [`REFACTORING.md`](../REFACTORING.md), and
the size and responsibility gate in
[`skills/anti-monolith-guard/SKILL.md`](../skills/anti-monolith-guard/SKILL.md).

## Relationships

Governed by [`00-general-governance.md`](00-general-governance.md) and
catalogued in [`README.md`](README.md).
