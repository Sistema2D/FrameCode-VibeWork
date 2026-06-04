# 06 — Making Method Calls Simpler

Use this file when the method interface is confusing: bad names, excessive parameters, control parameters, complex constructors, inappropriate exceptions, or excessively broad visibility.

Base source: https://refactoring.guru/refactoring/techniques/simplifying-method-calls

## General family rules

- Apply only when the observable behavior can be preserved.
- Prefer small steps, with tests executed between each step.
- Document the scenario, the technique, and the evidence that the behavior hasn't changed in the PR.
- Stop the refactoring if a functional change becomes necessary; open a separate task.

## Scenarios, decisions, and actions

### Rename Method

**Scenario:** The method's name doesn't explain its behavior.

**Governed action:** Rename it to reveal intent and update callers.

**Specific rules:**

- follow domain vocabulary.
- preserve compatibility if it's a public method.
- rename tests and documentation.

**Acceptance criteria:**

- self-explanatory name.
- callers updated.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Rename Method`.

### Add Parameter

**Scenario:** The method doesn't have enough data to perform the action.

**Governed action:** Add the necessary parameter to the method's contract.

**Specific rules:**

- avoid adding a parameter out of convenience if the object already has the data.
- evaluate Preserve Whole Object or Introduce Parameter Object.
- update all callers.

**Acceptance criteria:**

- complete contract.
- no redundant parameters.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Add Parameter`.

### Remove Parameter

**Scenario:** A parameter is not used by the method.

**Governed action:** Remove the parameter and update callers.

**Specific rules:**

- verify interfaces/overrides.
- preserve public compatibility via deprecation when necessary.
- remove obsolete tests.

**Acceptance criteria:**

- simpler signature.
- no broken callers.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Remove Parameter`.

### Separate Query from Modifier

**Scenario:** A method returns a value and alters state.

**Governed action:** Separate it into a query method and a command method.

**Specific rules:**

- query must not have side effects.
- command must make the change explicit.
- update callers that depend on both.

**Acceptance criteria:**

- explicit side effects.
- separate tests for query and command.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Separate Query from Modifier`.

### Parameterize Method

**Scenario:** Multiple methods do almost the same thing with different values.

**Governed action:** Unify them into a parameterized method.

**Specific rules:**

- apply when the behavior is the same.
- do not create a parameter that controls incompatible branches.
- name the parameter by concept.

**Acceptance criteria:**

- reduced duplication.
- clear contract.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Parameterize Method`.

### Replace Parameter with Explicit Methods

**Scenario:** A parameter decides which part of the method to execute.

**Governed action:** Create explicit methods for each action and remove the control parameter.

**Specific rules:**

- use when branches have different intents.
- names must reveal the action.
- avoid an explosion of semantically identical methods.

**Acceptance criteria:**

- clearer calls.
- fewer internal conditionals.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Replace Parameter with Explicit Methods`.

### Preserve Whole Object

**Scenario:** A caller extracts several values from an object to pass them as parameters.

**Governed action:** Pass the whole object to the method.

**Specific rules:**

- ensure the callee can depend on the object's type.
- do not unduly increase coupling.
- prefer a parameter object if data comes from multiple sources.

**Acceptance criteria:**

- smaller signature.
- less coupling to individual fields.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Preserve Whole Object`.

### Replace Parameter with Method Call

**Scenario:** A caller calculates a value via a query and passes it to a method that could calculate it internally.

**Governed action:** Remove the parameter and call the query inside the method.

**Specific rules:**

- apply if the method has natural access to the required object.
- do not hide an expensive or unstable dependency.
- avoid side effects.

**Acceptance criteria:**

- simplified caller.
- calculation responsibility centralized.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Replace Parameter with Method Call`.

### Introduce Parameter Object

**Scenario:** A group of parameters appears repeatedly.

**Governed action:** Create an object that aggregates the related parameters.

**Specific rules:**

- object must represent a coherent concept.
- add validations to the object when it makes sense.
- avoid a generic bag of data.

**Acceptance criteria:**

- smaller signatures.
- reusable and validatable group.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Introduce Parameter Object`.

### Remove Setting Method

**Scenario:** A field should only be defined at creation and then remain immutable.

**Governed action:** Remove the setter and configure the value via constructor/factory.

**Specific rules:**

- ensure intended immutability.
- update frameworks that require setters.
- validate serialization/ORM.

**Acceptance criteria:**

- protected state.
- less accidental mutability.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Remove Setting Method`.

### Hide Method

**Scenario:** A method is not used externally or is only used in its own hierarchy.

**Governed action:** Reduce visibility to private/protected/internal according to the language.

**Specific rules:**

- do not break public API without migration.
- verify usage by reflection/frameworks.
- keep tests at the public level when possible.

**Acceptance criteria:**

- smaller public surface.
- reinforced encapsulation.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Hide Method`.

### Replace Constructor with Factory Method

**Scenario:** A constructor is complex or needs to decide which object to create.

**Governed action:** Create a factory method and replace constructor calls.

**Specific rules:**

- use when creation has logic, alternative names, or subtypes.
- keep constructor private/protected if possible.
- test creation paths.

**Acceptance criteria:**

- expressive creation.
- centralized construction logic.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Replace Constructor with Factory Method`.

### Replace Error Code with Exception

**Scenario:** A method returns a special code to indicate an error.

**Governed action:** Throw an appropriate exception instead of a special return.

**Specific rules:**

- use for exceptional errors, not expected flow.
- define exception type.
- update callers for handling.

**Acceptance criteria:**

- error cannot be ignored.
- clear failure contract.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Replace Error Code with Exception`.

### Replace Exception with Test

**Scenario:** An exception is used where a simple test would resolve the expected flow.

**Governed action:** Replace the exception with a conditional check before the operation.

**Specific rules:**

- use when the condition is predictable and common.
- do not mask real failures.
- keep exception for unexpected conditions.

**Acceptance criteria:**

- expected flow without exception.
- better readability/performance.

**Minimum evidence in PR:**

- Before/after of the affected code; tests executed; justification for using `Replace Exception with Test`.

## Recommended order

1. Fix bad names before changing signatures.
2. Remove unused parameters.
3. Separate query from command when there is a hidden side effect.
4. Reduce long lists with whole object or parameter object.
5. Swap control parameters for explicit methods when each value represents a different intent.
6. Adjust constructors and error handling after stabilizing the interface.

## Special attention

Changes to public signatures require a migration plan, temporary deprecation, or versioning. Methods used by frameworks, reflection, HTTP routes, serializers, and ORMs must be treated as public contracts until proven otherwise.
