# 04 — Organizing Data

Use this file when the problem is in the way data is represented, accessed, encapsulated, or associated.

Base source: https://refactoring.guru/refactoring/techniques/organizing-data

## General Family Rules

- Apply only when observable behavior can be preserved.
- Prefer small steps, with tests executed between each step.
- Record the scenario, the technique, and the evidence that behavior did not change in the PR.
- Stop refactoring if a need for functional change arises; open a separate task.

## Scenarios, Decisions, and Actions

### Self Encapsulate Field

**Scenario:** The class itself directly accesses private fields and needs to control internal access.

**Governed action:** Create getter/setter and use these methods within the class.

**Specific rules:**

- Use when there is validation, lazy loading, notification, or access control.
- Do not add unnecessary setters.
- Preserve invariants.

**Acceptance criteria:**

- Controlled internal access.
- Centralized rules.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Self Encapsulate Field`.

### Replace Data Value with Object

**Scenario:** Simple value has behavior, validation, or associated data.

**Governed action:** Create a class for the value and store an instance of this class in the original object.

**Specific rules:**

- Name with a domain concept.
- Move validations to the new object.
- Consider immutability.

**Acceptance criteria:**

- Primitive replaced by expressive type.
- Behavior close to the data.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Replace Data Value with Object`.

### Change Value to Reference

**Scenario:** There are several identical instances that should represent the same entity.

**Governed action:** Replace duplicate objects with a single shared/registered reference.

**Specific rules:**

- Use identity when the lifecycle matters.
- Define origin of the reference.
- Care for concurrency/cache.

**Acceptance criteria:**

- Unique identity preserved.
- Controlled duplications.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Change Value to Reference`.

### Change Reference to Value

**Scenario:** Referenced object is small, immutable, or rarely altered and does not justify its own lifecycle.

**Governed action:** Transform into a value object.

**Specific rules:**

- Ensure equality by value.
- Prefer immutability.
- Do not apply if identity is relevant.

**Acceptance criteria:**

- Simpler object.
- No artificial reference management.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Change Reference to Value`.

### Replace Array with Object

**Scenario:** Array contains data of different types/meanings.

**Governed action:** Create an object with named fields for each element.

**Specific rules:**

- Do not depend on magic index.
- Name fields by meaning.
- Validate serialization/contracts.

**Acceptance criteria:**

- Access by name.
- Error reduction by position.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Replace Array with Object`.

### Duplicate Observed Data

**Scenario:** Domain data is stuck in graphical interface classes.

**Governed action:** Separate data into domain classes and keep synchronization with the GUI.

**Specific rules:**

- Domain must not depend on the interface.
- Use explicit update/observation mechanism.
- Test synchronization.

**Acceptance criteria:**

- Domain testable without GUI.
- Interface only presents/alters data via contract.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Duplicate Observed Data`.

### Change Unidirectional Association to Bidirectional

**Scenario:** Two classes need to access each other, but the association only exists in one direction.

**Governed action:** Add a reverse association in the class that needs to navigate back.

**Specific rules:**

- Define the owner of the association.
- Synchronize both sides.
- Avoid unnecessary cycles.

**Acceptance criteria:**

- Necessary navigation available.
- Consistency between sides.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Change Unidirectional Association to Bidirectional`.

### Change Bidirectional Association to Unidirectional

**Scenario:** Bidirectional association exists, but one side does not use the other.

**Governed action:** Remove the unused side of the association.

**Specific rules:**

- Verify serialization/ORM.
- Ensure that queries do not depend on the removed link.
- Reduce cycles.

**Acceptance criteria:**

- Reduced coupling.
- No loss of necessary navigation.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Change Bidirectional Association to Unidirectional`.

### Replace Magic Number with Symbolic Constant

**Scenario:** Literal number has specific meaning in the code.

**Governed action:** Create a constant with an explanatory name and replace occurrences.

**Specific rules:**

- Do not replace trivial 0/1 without gain.
- Centralize domain constants.
- Record unit when applicable.

**Acceptance criteria:**

- Explicit meaning.
- Less literal duplication.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Replace Magic Number with Symbolic Constant`.

### Encapsulate Field

**Scenario:** Public field allows direct alteration.

**Governed action:** Make field private/protected and provide controlled access.

**Specific rules:**

- Expose only what is necessary.
- Validate alterations via method.
- Preserve compatibility if public API.

**Acceptance criteria:**

- Invariants protected.
- Controlled external access.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Encapsulate Field`.

### Encapsulate Collection

**Scenario:** Collection is exposed directly and can be altered by consumers.

**Governed action:** Return a read-only view or specific methods to add/remove items.

**Specific rules:**

- Do not expose internal mutable collection.
- Validate add/remove operations.
- Keep bidirectional consistency when applicable.

**Acceptance criteria:**

- Protected collection.
- Explicit domain operations.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Encapsulate Collection`.

### Replace Type Code with Class

**Scenario:** Primitive type code represents a concept without complex variable behavior.

**Governed action:** Create a class to represent the type.

**Specific rules:**

- Use when a set of types needs its own meaning.
- Avoid enum/primitive with scattered rules.
- Centralize validation.

**Acceptance criteria:**

- Expressive type.
- Fewer loose conditionals.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Replace Type Code with Class`.

### Replace Type Code with Subclasses

**Scenario:** Type code determines stable and mutually exclusive behavior.

**Governed action:** Create subclasses for each type and move specific behavior.

**Specific rules:**

- Use when types are stable.
- Do not apply if type changes at runtime.
- Protect creation via factory when necessary.

**Acceptance criteria:**

- Behavior by subtype.
- Less switch/if by type.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Replace Type Code with Subclasses`.

### Replace Type Code with State/Strategy

**Scenario:** Type code determines behavior that can vary, grow, or change in execution.

**Governed action:** Replace type with State or Strategy object.

**Specific rules:**

- Use when there is dynamic variation.
- Define common interface.
- Avoid empty strategies.

**Acceptance criteria:**

- Conditionals replaced by composition.
- Controlled behavior swap.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Replace Type Code with State/Strategy`.

### Replace Subclass with Fields

**Scenario:** Subclasses differ only by constant values/fields, without their own behavior.

**Governed action:** Remove subclasses and represent variations with fields.

**Specific rules:**

- Do not apply if there is specialized behavior.
- Validate creation contracts.
- Maintain domain names in values.

**Acceptance criteria:**

- Simplified hierarchy.
- Variations represented by data.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Replace Subclass with Fields`.

## Recommended Order

1. Protect invariants with encapsulation.
2. Replace primitives, arrays, and magic numbers with named concepts.
3. Evaluate identity: value object or reference.
4. Organize associations only when there is real necessary navigation.
5. Replace type codes with class, subclass, or State/Strategy according to behavior variation.

## Special Attention

Data changes can affect persistence, serialization, API contracts, migrations, and compatibility. Classify as medium or high risk when there is external impact.
