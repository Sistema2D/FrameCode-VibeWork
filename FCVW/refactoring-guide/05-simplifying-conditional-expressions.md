# 05 — Simplifying Conditional Expressions

Use this file when conditional logic, duplicated branches, nesting, flags, or null checks hinder readability, extension, or testing.

Base source: https://refactoring.guru/refactoring/techniques/simplifying-conditional-expressions

## General family rules

- Apply only when the observable behavior can be preserved.
- Prefer small steps, with tests executed between each step.
- Document the scenario, the technique, and the evidence that the behavior hasn't changed in the PR.
- Stop the refactoring if a functional change becomes necessary; open a separate task.

## Scenarios, decisions, and actions

### Decompose Conditional

**Scenario:** An if/else or switch conditional is complex.

**Governed action:** Extract the condition, then block, and else block into methods with clear names.

**Specific rules:**

- extracted methods must explain intent.
- do not change the order of evaluation with side effects.
- cover edge cases.

**Acceptance criteria:**

- readable conditional flow.
- reduced local complexity.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Decompose Conditional`.

### Consolidate Conditional Expression

**Scenario:** Multiple conditionals lead to the same result/action.

**Governed action:** Combine conditions into a single expression or decision method.

**Specific rules:**

- use a named method if the expression gets long.
- preserve short-circuiting when relevant.
- validate logical precedence.

**Acceptance criteria:**

- consolidated rule.
- less duplication of result.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Consolidate Conditional Expression`.

### Consolidate Duplicate Conditional Fragments

**Scenario:** The same code appears in all branches of a conditional.

**Governed action:** Move the duplicated code fragment outside the conditional.

**Specific rules:**

- ensure it executes exactly once.
- position it before/after according to the branch dependency.
- do not move code that depends on the branch.

**Acceptance criteria:**

- duplication removed.
- execution order preserved.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Consolidate Duplicate Conditional Fragments`.

### Remove Control Flag

**Scenario:** A boolean variable controls the exit/continuation of a flow.

**Governed action:** Replace the flag with break, continue, return, or method extraction.

**Specific rules:**

- avoid flags that mask flow.
- use early return with clarity.
- do not hide domain rules.

**Acceptance criteria:**

- direct flow.
- less temporary state.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Remove Control Flag`.

### Replace Nested Conditional with Guard Clauses

**Scenario:** Nested conditionals make it difficult to see the normal flow.

**Governed action:** Isolate special cases at the beginning with guard clauses and leave the main flow flat.

**Specific rules:**

- guards must represent exceptions/special cases.
- keep the main flow at the end.
- avoid multiple confusing returns without a pattern.

**Acceptance criteria:**

- reduction of indentation.
- evident happy path.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Replace Nested Conditional with Guard Clauses`.

### Replace Conditional with Polymorphism

**Scenario:** A conditional executes different actions based on type, state, or property of the object.

**Governed action:** Create subclasses/strategies with a common method and move each branch to the corresponding implementation.

**Specific rules:**

- apply when variations are real behaviors.
- avoid artificial hierarchy for a simple condition.
- use a factory/strategy for selection.

**Acceptance criteria:**

- reduced switch/if.
- extension by new type without changing the core decision.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Replace Conditional with Polymorphism`.

### Introduce Null Object

**Scenario:** Many null checks appear for the same type of object.

**Governed action:** Return a null object with default behavior instead of null.

**Specific rules:**

- do not hide absence when it's a business error.
- document the default behavior.
- test calls without null checks.

**Acceptance criteria:**

- fewer null checks.
- explicit default behavior.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Introduce Null Object`.

### Introduce Assertion

**Scenario:** Code depends on an assumption that must be true.

**Governed action:** Add an explicit assertion for the expected condition.

**Specific rules:**

- use for internal invariants, not user validation.
- do not replace expected error handling.
- message must explain the assumption.

**Acceptance criteria:**

- detectable assumption failures.
- clear internal contract.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Introduce Assertion`.

## Recommended order

1. Write tests for each relevant branch.
2. Remove duplication of common fragments.
3. Decompose complex conditions into named methods.
4. Flatten nested conditionals with guard clauses.
5. Evaluate polymorphism only when branches represent real type/state variations.
6. Use null object only when default behavior is safe and expected.

## Blockers

Do not replace conditional with polymorphism if:

- the rule changes frequently through simple configuration;
- the branches are few and trivial;
- the resulting hierarchy would be artificial;
- the object's absence represents an error that must be handled explicitly.
