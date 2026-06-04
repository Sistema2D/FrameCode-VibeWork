# 07 — Dealing with Generalization

Use this file when the problem lies in the class hierarchy, generalization, specialization, interfaces, template method, improper inheritance, or excessive delegation.

Base source: https://refactoring.guru/refactoring/techniques/dealing-with-generalization

## General family rules

- Apply only when the observable behavior can be preserved.
- Prefer small steps, with tests executed between each step.
- Document the scenario, the technique, and the evidence that the behavior hasn't changed in the PR.
- Stop the refactoring if a functional change becomes necessary; open a separate task.

## Scenarios, decisions, and actions

### Pull Up Field

**Scenario:** Subclasses have the same field.

**Governed action:** Move the common field to the superclass.

**Specific rules:**

- ensure the same meaning across all subclasses.
- do not pull up a field used in an incompatible way.
- adjust constructors.

**Acceptance criteria:**

- duplication removed.
- common field centralized.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Pull Up Field`.

### Pull Up Method

**Scenario:** Subclasses have identical or equivalent methods.

**Governed action:** Move the common method to the superclass.

**Specific rules:**

- confirm identical behavior.
- extract differences beforehand if necessary.
- do not force subclass dependencies into the superclass.

**Acceptance criteria:**

- single common implementation.
- simpler subclasses.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Pull Up Method`.

### Pull Up Constructor Body

**Scenario:** Subclass constructors share initialization.

**Governed action:** Move common parts to the superclass constructor or a common initialization method.

**Specific rules:**

- preserve initialization order.
- do not call overridden methods dangerously in the constructor.
- test creation of all subclasses.

**Acceptance criteria:**

- common initialization centralized.
- smaller constructors.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Pull Up Constructor Body`.

### Push Down Method

**Scenario:** A superclass method is only relevant to some subclasses.

**Governed action:** Move the method to the subclasses that actually use it.

**Specific rules:**

- do not leave public contract inconsistent.
- evaluate separate interface.
- remove artificial dependencies from the superclass.

**Acceptance criteria:**

- cleaner superclass.
- behavior where it is needed.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Push Down Method`.

### Push Down Field

**Scenario:** A superclass field is only used by some subclasses.

**Governed action:** Move the field to the applicable subclasses.

**Specific rules:**

- verify serialization/constructors.
- do not duplicate field with different meanings.
- update protected access.

**Acceptance criteria:**

- leaner superclass.
- specific state in correct subtypes.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Push Down Field`.

### Extract Subclass

**Scenario:** A subset of objects of a class has specialized behavior/data.

**Governed action:** Create a subclass for the specific variation.

**Specific rules:**

- use when the variation is stable and semantic.
- do not create subclassification by explosive combination.
- centralize creation.

**Acceptance criteria:**

- isolated variation.
- simplified base class.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Extract Subclass`.

### Extract Superclass

**Scenario:** Different classes have common fields/methods.

**Governed action:** Create a superclass and move common elements.

**Specific rules:**

- use if there is an "is-a" conceptual relationship.
- do not extract merely due to structural coincidence.
- test all subtypes.

**Acceptance criteria:**

- reduced duplication.
- clear common abstraction.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Extract Superclass`.

### Extract Interface

**Scenario:** Classes share a contract that must be consumed without coupling to implementation.

**Governed action:** Create an interface with common methods used by clients.

**Specific rules:**

- interface must reflect client's role.
- do not include unused methods.
- version public contract.

**Acceptance criteria:**

- clients depend on abstraction.
- interchangeable implementations.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Extract Interface`.

### Collapse Hierarchy

**Scenario:** Superclass and subclass have no relevant differences.

**Governed action:** Merge classes and remove unnecessary level from the hierarchy.

**Specific rules:**

- ensure absence of differentiated behavior.
- evaluate compatibility with consumers.
- clean tests and documentation.

**Acceptance criteria:**

- smaller hierarchy.
- no empty abstraction.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Collapse Hierarchy`.

### Form Template Method

**Scenario:** Subclasses execute a similar algorithm with common steps and punctual variations.

**Governed action:** Create a template method in the superclass and override steps in the subclasses.

**Specific rules:**

- use when algorithm sequence is stable.
- do not force inheritance when Strategy resolves better.
- document mandatory/optional hooks.

**Acceptance criteria:**

- common algorithm centralized.
- variations isolated in steps.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Form Template Method`.

### Replace Inheritance with Delegation

**Scenario:** Subclass uses only part of the superclass or the "is-a" relationship is artificial.

**Governed action:** Replace inheritance with a delegated field and forward necessary calls.

**Specific rules:**

- use when composition models better.
- avoid exposing all delegate methods without criteria.
- plan API migration.

**Acceptance criteria:**

- reduced coupling.
- "has-a" relationship explicit.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Replace Inheritance with Delegation`.

### Replace Delegation with Inheritance

**Scenario:** Class delegates almost everything to another and the "is-a" relationship is valid.

**Governed action:** Transform delegation into inheritance.

**Specific rules:**

- apply with caution.
- confirm substitutability.
- do not use just to save code.

**Acceptance criteria:**

- less mechanical delegation.
- semantically valid hierarchy.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Replace Delegation with Inheritance`.

## Recommended order

1. Confirm whether the correct relationship is "is-a" or "has-a".
2. Remove simple duplication with Pull Up, if the abstraction is already valid.
3. Push down behavior when the superclass is contaminated by specific cases.
4. Extract interface when clients need a contract, not an implementation.
5. Collapse hierarchies with no real difference.
6. Replace inheritance with delegation when substitutability is not true.
7. Replace delegation with inheritance only when the conceptual relationship is strong and stable.

## Substitutability criterion

Before approving any inheritance change, validate whether a subclass instance can be safely used where the superclass is expected, without behavioral surprises, stronger preconditions, or weaker postconditions.
