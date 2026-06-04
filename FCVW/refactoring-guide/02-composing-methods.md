# 02 — Composing Methods

Use this file when the problem is concentrated inside methods: excessive length, unclear expressions, confusing temporary variables, or algorithms difficult to replace.

Base source: https://refactoring.guru/refactoring/techniques/composing-methods

## General Family Rules

- Apply only when observable behavior can be preserved.
- Prefer small steps, with tests executed between each step.
- Record the scenario, the technique, and the evidence that behavior did not change in the PR.
- Stop refactoring if a need for functional change arises; open a separate task.

## Scenarios, Decisions, and Actions

### Extract Method

**Scenario:** Code snippet groupable inside a method.

**Governed action:** Extract the snippet to a new method/function with a name that reveals intention and replace the original snippet with a call to the new method.

**Specific rules:**

- The new method must have a single intention.
- Parameters must be minimal and clear.
- Do not extract if the name becomes generic like processData or handleStuff.

**Acceptance criteria:**

- Calling method tests preserved.
- Size/complexity reduction or clear reading gain.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Extract Method`.

### Inline Method

**Scenario:** The method body is clearer than the name or the method's existence creates useless indirection.

**Governed action:** Replace calls with the method body and remove the old method.

**Specific rules:**

- Check calls in subclasses/superclasses.
- Do not apply in public methods without a migration plan.
- Do not apply if the method expresses an important domain rule.

**Acceptance criteria:**

- Updated calls.
- No relevant duplication introduced.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Inline Method`.

### Extract Variable

**Scenario:** Expression difficult to understand.

**Governed action:** Create a local variable with a self-explanatory name for the result of the expression or part of it.

**Specific rules:**

- Name must explain business/technical meaning.
- Do not create a variable for a trivial expression.
- Maintain immutability when possible.

**Acceptance criteria:**

- More readable expression.
- No alteration of precedence or evaluation.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Extract Variable`.

### Inline Temp

**Scenario:** Temporary variable only stores a simple expression and adds no meaning.

**Governed action:** Replace references to the variable with the expression itself and remove the variable.

**Specific rules:**

- Do not apply if the variable documents intention.
- Do not unnecessarily duplicate an expensive calculation.
- Validate side effects of the expression.

**Acceptance criteria:**

- Smaller and equally clear code.
- No improper re-execution of logic.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Inline Temp`.

### Replace Temp with Query

**Scenario:** Expression result is stored in a local variable and used later.

**Governed action:** Move the expression to a query method and replace the variable with a call to the method.

**Specific rules:**

- The query must not alter state.
- Cache only if there is a measurable cost.
- Name by the question answered.

**Acceptance criteria:**

- Testable query.
- No relevant performance regression.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Replace Temp with Query`.

### Split Temporary Variable

**Scenario:** Same local variable stores different intermediate values.

**Governed action:** Create distinct variables, one for each responsibility/value.

**Specific rules:**

- Do not reuse variable to save lines.
- Except for loop counters/indexes, each variable must have a meaning.
- Prefer specific names.

**Acceptance criteria:**

- Each variable has a single purpose.
- Reduction of ambiguity.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Split Temporary Variable`.

### Remove Assignments to Parameters

**Scenario:** Parameter receives a new value inside the method.

**Governed action:** Create a local variable for the new value and preserve the parameter as immutable input.

**Specific rules:**

- Do not alter input parameter.
- Avoid confusion between received value and calculated value.
- In languages with mutable references, evaluate internal mutation separately.

**Acceptance criteria:**

- Preserved input.
- More predictable flow.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Remove Assignments to Parameters`.

### Replace Method with Method Object

**Scenario:** Long method has deeply intertwined local variables and does not allow simple extractions.

**Governed action:** Transform the method into its own class/object, converting local variables into fields and splitting behavior into smaller methods.

**Specific rules:**

- Apply when isolated Extract Method does not resolve.
- Name the class by the represented process/algorithm.
- Do not leak internal details to the caller.

**Acceptance criteria:**

- Class with clear responsibility.
- Smaller and testable internal methods.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Replace Method with Method Object`.

### Substitute Algorithm

**Scenario:** Current algorithm needs to be replaced by a clearer, simpler, or more correct version.

**Governed action:** Replace the method body with a new algorithm while preserving the external contract.

**Specific rules:**

- Ensure before/after equivalence tests.
- Maintain input/output contract.
- Record performance impact when applicable.

**Acceptance criteria:**

- Same expected results.
- Edge cases covered.

**Minimum evidence in the PR:**

- Before/after of the affected snippet; executed tests; justification for using `Substitute Algorithm`.

## Recommended Order

1. Create characterization tests for the current method.
2. Reduce local ambiguity with `Extract Variable` or `Split Temporary Variable`.
3. Remove improper mutations with `Remove Assignments to Parameters`.
4. Extract blocks with `Extract Method`.
5. If extraction fails due to intertwined variables, use `Replace Method with Method Object`.
6. Only then replace the entire algorithm, if necessary.
