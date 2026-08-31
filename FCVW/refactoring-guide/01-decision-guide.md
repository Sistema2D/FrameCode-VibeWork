# 01 — Decision Guide

Use this file to identify the refactoring scenario and direct the team to the applicable file.

## Quick Decision by Symptom

| Observed Symptom | Confirmation Question | Applicable File |
|---|---|---|
| Long method, difficult to understand, or with blocks that seem to have their own intention. | Are there excerpts that could have their own name? | [`02-refactoring-catalog.md`](02-refactoring-catalog.md) |
| Complex expression, confusing temporary variable, or algorithm difficult to replace. | Is the difficulty inside a method? | [`02-refactoring-catalog.md`](02-refactoring-catalog.md) |
| Method or field seems to belong to another class. | Does another class use this behavior/data more? | [`02-refactoring-catalog.md`](02-refactoring-catalog.md) |
| Class does too much work or almost nothing. | Is the responsibility incorrectly concentrated or dispersed? | [`02-refactoring-catalog.md`](02-refactoring-catalog.md) |
| Excessive dependency through call chains or useless delegation. | Does the client know too many objects or is there an intermediate without value? | [`02-refactoring-catalog.md`](02-refactoring-catalog.md) |
| Primitive data represent domain concepts. | Does the data have its own rule, validation, unit, format, or behavior? | [`02-refactoring-catalog.md`](02-refactoring-catalog.md) |
| Public fields, exposed collections, heterogeneous array, or magic number. | Is the data vulnerable to improper alteration? | [`02-refactoring-catalog.md`](02-refactoring-catalog.md) |
| Complex, duplicated, nested, or type-based conditional. | Does the decision logic hinder reading, extension, or testing? | [`02-refactoring-catalog.md`](02-refactoring-catalog.md) |
| Many `null`s, control flags, or implicit premises. | Is there a special flow that should be explicit? | [`02-refactoring-catalog.md`](02-refactoring-catalog.md) |
| Method has a bad name, too many parameters, unused parameter, or complex constructor. | Is the call interface confusing or unstable? | [`02-refactoring-catalog.md`](02-refactoring-catalog.md) |
| Method returns a value and changes state at the same time. | Does the call mix query and command? | [`02-refactoring-catalog.md`](02-refactoring-catalog.md) |
| Inheritance contains duplication, misplaced subclasses, or excessive hierarchy. | Is the problem in the abstraction between classes? | [`02-refactoring-catalog.md`](02-refactoring-catalog.md) |
| Delegation replaces inheritance or inheritance replaces delegation improperly. | Is the "is-a" or "has-a" relationship poorly modeled? | [`02-refactoring-catalog.md`](02-refactoring-catalog.md) |
| The problem was perceived as a code smell, but the technique is still unclear. | Which smell closest matches the case? | [`08-code-smells-map.md`](08-code-smells-map.md) |

## Decision Flow

```text
1. Does the change alter functional behavior?
   ├─ Yes → not pure refactoring. Separate feature/fix.
   └─ No → continue.

2. Is the problem mainly inside a method?
   ├─ Yes → use composing methods or simplifying conditional expressions.
   └─ No → continue.

3. Is the problem between classes/objects?
   ├─ Method/field in the wrong place → moving features between objects.
   ├─ Class too large/small → extract or inline class.
   ├─ Dependency chain/delegation → hide delegate or remove middle man.
   └─ Continue.

4. Is the problem in data modeling?
   ├─ Primitives, arrays, type codes, open collections → organizing data.
   └─ Continue.

5. Is the problem in the call interface?
   ├─ Bad name, parameters, constructor, error return → simplifying method calls.
   └─ Continue.

6. Is the problem in inheritance, abstraction, or structural delegation?
   ├─ Yes → dealing with generalization.
   └─ No → review code smells and scope.
```

## Rules for Choosing Between Similar Techniques

| Doubt | Preferred Choice |
|---|---|
| Extract Method or Extract Variable? | Extract variable when the problem is just an expression; extract method when there is a behavior block with its own intention. |
| Extract Class or Move Method? | Move method when the responsibility already exists in another class; extract class when a current class accumulates two responsibilities. |
| Hide Delegate or Remove Middle Man? | Hide delegation when the client knows too many details; remove middle man when the class only passes calls without adding protection, semantics, or stability. |
| Parameterize Method or Replace Parameter with Explicit Methods? | Parameterize when methods are almost the same; separate explicit methods when a parameter controls very different paths. |
| Replace Type Code with Subclasses or State/Strategy? | Use subclasses for stable type variations; use State/Strategy when behavior varies or changes at runtime. |
| Replace Conditional with Polymorphism or Decompose Conditional? | First decompose if the logic is just unreadable; use polymorphism if each branch represents different type/state behavior. |
| Extract Superclass or Extract Interface? | Superclass when there is common implementation/data; interface when the objective is a common contract and low coupling. |
| Replace Inheritance with Delegation or Push Down Method? | Push method down if inheritance still makes sense; replace with delegation if the "is-a" relationship is artificial. |

## Expected Decision Output

At the end, record in the PR:

```markdown
### Refactoring Diagnosis
- Observed symptom:
- Related code smell, if applicable:
- Chosen scenario:
- Governance file used:
- Applied technique(s):
- Justification for non-alteration of behavior:
```
## Operational Layer for Large Bases

After identifying the technical scenario, apply the operational triage below.

| Condition | Mandatory File |
|---|---|
| Refactoring involves more than one module, folder, or package. | [`10-code-inventory-and-classification.md`](10-code-inventory-and-classification.md) |
| Refactoring involves critical, public area, without tests or with unknown dependencies. | [`11-refactoring-risk-matrix.md`](11-refactoring-risk-matrix.md) |
| Legacy code, without coverage or with poorly documented behavior. | [`12-testing-strategy-before-refactoring.md`](12-testing-strategy-before-refactoring.md) |
| PR depends on build, tests, lint, static analysis, or controlled deploy. | [`13-ci-cd-pipeline-and-quality-gates.md`](13-ci-cd-pipeline-and-quality-gates.md) |
| Medium, high, or critical risk refactoring. | [`14-rollback-plan.md`](14-rollback-plan.md) |
| Large change, with many files or multiple stages. | [`15-incremental-refactoring-plan.md`](15-incremental-refactoring-plan.md) |
| Move, rename, extract class, alter signature, contract, or data. | [`16-dependency-and-impact-map.md`](16-dependency-and-impact-map.md) |
| Open PR, define branch, review, or approve. | [`17-branch-and-pull-request-policy.md`](17-branch-and-pull-request-policy.md) |
| Doubt whether the change is a refactoring, bugfix, feature, or rewrite. | [`18-behavioral-refactoring-vs-rewrite.md`](18-behavioral-refactoring-vs-rewrite.md) |
| Scope grew, tests failed, or unforeseen risks emerged. | [`19-stopping-criteria.md`](19-stopping-criteria.md) |

## Recommended Full Flow

```text
1. Identify if the change is pure refactoring.
   ├─ If it changes behavior → separate feature/fix or use 18.
   └─ If it does not change behavior → continue.

2. Identify technical scenario.
   ├─ Method → 02 or 05.
   ├─ Objects/classes → 03.
   ├─ Data → 04.
   ├─ Calls/API → 06.
   └─ Inheritance/delegation → 07.

3. Diagnose code smell, if necessary → 08.

4. Classify operational governance.
   ├─ Inventory → 10.
   ├─ Risk → 11.
   ├─ Tests → 12.
   ├─ Pipeline → 13.
   ├─ Rollback → 14.
   ├─ Incremental plan → 15.
   ├─ Dependencies/impact → 16.
   ├─ Branch/PR → 17.
   └─ Stopping criteria → 19.

5. Fill out required templates → 20.
```

## Routing Map by Scenario (read on demand for AI)

To optimize tokens, read only what is necessary for the current activity.

| Situation | Read | Observation |
|---|---|---|
| Common base (once per session or opening) | [`00-general-governance.md`](00-general-governance.md) | Does not need to be reread for each activity. |
| Doubt if it is pure refactoring | [`18-behavioral-refactoring-vs-rewrite.md`](18-behavioral-refactoring-vs-rewrite.md) | Classifies refactoring vs fix/feature/rewrite. |
| Symptom inside method/expression | [`02-refactoring-catalog.md`](02-refactoring-catalog.md) | Use when the problem is inside the method. |
| Complex conditional, flags, or `null` | [`02-refactoring-catalog.md`](02-refactoring-catalog.md) | Use when the decision is difficult to read/test. |
| Responsibility between classes/objects | [`02-refactoring-catalog.md`](02-refactoring-catalog.md) | Method/field in the wrong place, class too large/small. |
| Data/encapsulation problem | [`02-refactoring-catalog.md`](02-refactoring-catalog.md) | Primitives, exposed collections, type codes. |
| Confusing call interface | [`02-refactoring-catalog.md`](02-refactoring-catalog.md) | Bad name, many parameters, mixed return/effect. |
| Abstraction, inheritance, or delegation | [`02-refactoring-catalog.md`](02-refactoring-catalog.md) | Excessive hierarchy, improper inheritance. |
| Smell without clear technique | [`08-code-smells-map.md`](08-code-smells-map.md) | Use to discover the technical file. |
| Specific operational conditions | Table “Operational Layer for Large Bases” | Read only the file(s) pointed to by the condition. |
| Needs template | [`20-templates.md`](20-templates.md) | Copy only the applicable template. |
