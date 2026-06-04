# 03 — Moving Features Between Objects

Use this file when methods, fields, or responsibilities are improperly distributed between classes.

Base source: https://refactoring.guru/refactoring/techniques/moving-features-between-objects

## General Family Rules

- Apply only when observable behavior can be preserved.
- Prefer small steps, with tests executed between each step.
- Record the scenario, the technique, and the evidence that behavior did not change in the PR.
- Stop refactoring if a need for functional change arises; open a separate task.

## Scenarios, Decisions, and Actions

### Move Method

**Scenario:** Method uses more data/behavior from another class than from its own.

**Governed action:** Create a method in the most appropriate class, move the logic, and transform/remove the old method.

**Specific rules:**

- Preserve temporary compatibility if the method is public.
- Avoid increasing coupling.
- Move tests and documentation together.

**Acceptance criteria:**

- More cohesive responsibility.
- Updated calls or controlled delegation.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Move Method`.

### Move Field

**Scenario:** Field is more used by another class than by the current class.

**Governed action:** Create the field in the correct class and redirect accesses.

**Specific rules:**

- Evaluate persistence/serialization first.
- Do not break invariants.
- Use encapsulation during transition.

**Acceptance criteria:**

- Data owner becomes clear.
- Old accesses handled.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Move Field`.

### Extract Class

**Scenario:** A class accumulates responsibilities from two or more abstractions.

**Governed action:** Create a new class and move fields/methods of the extracted responsibility.

**Specific rules:**

- Define boundary by cohesion.
- Avoid extracting an anemic class without behavior.
- Maintain integration tests between classes.

**Acceptance criteria:**

- Original class reduced.
- New class with named responsibility.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Extract Class`.

### Inline Class

**Scenario:** Class does not have enough responsibility and only increases indirection.

**Governed action:** Move its features to another class and remove the incorporated class.

**Specific rules:**

- Validate external consumers.
- Do not apply if the class represents a domain concept.
- Avoid inflating the receiving class.

**Acceptance criteria:**

- Less indirection.
- Final responsibility remains cohesive.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Inline Class`.

### Hide Delegate

**Scenario:** Client needs to navigate to an internal object to call behavior.

**Governed action:** Create a method on the principal object that delegates the call to the internal object.

**Specific rules:**

- Use to protect encapsulation.
- Do not create an excessive facade for everything.
- Name by the client's intention.

**Acceptance criteria:**

- Client knows fewer internal details.
- Less coupling.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Hide Delegate`.

### Remove Middle Man

**Scenario:** Class has many methods that only pass calls.

**Governed action:** Remove delegating methods and allow direct calls to the final object.

**Specific rules:**

- Do not remove delegation that stabilizes a contract.
- Evaluate impact on public API.
- Keep only delegations with semantic value.

**Acceptance criteria:**

- Less valueless code.
- Direct calls documented.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Remove Middle Man`.

### Introduce Foreign Method

**Scenario:** Library class lacks a necessary method and cannot be altered.

**Governed action:** Create a method in the client class receiving the library instance as an argument.

**Specific rules:**

- Use for an occasional need.
- Clearly isolate external dependency.
- Do not spread duplicated foreign methods.

**Acceptance criteria:**

- Localized and tested method.
- No library modification.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Introduce Foreign Method`.

### Introduce Local Extension

**Scenario:** Library class lacks several necessary methods and cannot be altered.

**Governed action:** Create a wrapper or local subclass with the additional methods.

**Specific rules:**

- Prefer wrapper when inheriting from the library is risky.
- Centralize extensions.
- Document compatibility with library version.

**Acceptance criteria:**

- Reusable extension.
- Encapsulated external dependency.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Introduce Local Extension`.

## Recommended Order

1. Identify who actually uses the data/behavior.
2. Verify if the problem is ownership of responsibility, delegation, or lack of abstraction.
3. Prefer `Move Method`/`Move Field` for specific adjustments.
4. Use `Extract Class` when there is an entire responsibility to separate.
5. Use `Hide Delegate` to reduce client knowledge about internal objects.
6. Use `Remove Middle Man` when delegation became noise without architectural value.
