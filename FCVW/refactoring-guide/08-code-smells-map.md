# 08 — Code Smells Map

Use this file when the problem was perceived as a code smell, but the technique is not yet clear.

Base source: https://refactoring.guru/refactoring/smells

## Bloaters

| Code smell | Diagnosis | Recommended actions | Applicable files |
|---|---|---|---|
| Long Method | Method grew and became hard to understand or change. | Extract Method, Decompose Conditional, Replace Temp with Query, Replace Method with Method Object. | [`02`](02-refactoring-catalog.md), [`05`](02-refactoring-catalog.md) |
| Large Class | Class concentrates too many data and behaviors. | Extract Class, Move Method/Field, Encapsulate Record, Extract Superclass/Interface if there is real abstraction. | [`03`](02-refactoring-catalog.md), [`04`](02-refactoring-catalog.md), [`07`](02-refactoring-catalog.md) |
| Primitive Obsession | Primitives represent rich domain concepts. | Replace Data Value with Object, Replace Type Code with Class/Subclasses/State/Strategy, Introduce Parameter Object. | [`04`](02-refactoring-catalog.md), [`06`](02-refactoring-catalog.md) |
| Long Parameter List | Method demands too many parameters. | Preserve Whole Object, Introduce Parameter Object, Replace Parameter with Method Call, Remove Parameter. | [`06`](02-refactoring-catalog.md) |
| Data Clumps | The same data group appears together in several places. | Introduce Parameter Object, Extract Class, Replace Array with Object. | [`04`](02-refactoring-catalog.md), [`06`](02-refactoring-catalog.md) |

## Object-Orientation Abusers

| Code smell | Diagnosis | Recommended actions | Applicable files |
|---|---|---|---|
| Switch Statements | Decisions by type/state appear repeatedly. | Replace Conditional with Polymorphism, Replace Type Code with Subclasses or State/Strategy, Decompose Conditional. | [`04`](02-refactoring-catalog.md), [`05`](02-refactoring-catalog.md) |
| Temporary Field | Field is only used at certain moments, leaving state inconsistent. | Extract Class, Introduce Null Object, Replace Method with Method Object when state belongs to a computation. | [`02`](02-refactoring-catalog.md), [`03`](02-refactoring-catalog.md), [`05`](02-refactoring-catalog.md) |
| Refused Bequest | Subclass inherits members it doesn't use or shouldn't expose. | Push Down Method/Field, Replace Inheritance with Delegation, Extract Interface. | [`07`](02-refactoring-catalog.md) |
| Alternative Classes with Different Interfaces | Classes do similar things with different names/contracts. | Rename Method, Extract Interface, Move Method, Parameterize Method. | [`06`](02-refactoring-catalog.md), [`07`](02-refactoring-catalog.md), [`03`](02-refactoring-catalog.md) |

## Change Preventers

| Code smell | Diagnosis | Recommended actions | Applicable files |
|---|---|---|---|
| Divergent Change | One class changes for different reasons. | Extract Class, Move Method/Field, organize data by responsibility. | [`03`](02-refactoring-catalog.md), [`04`](02-refactoring-catalog.md) |
| Shotgun Surgery | A small change requires editing many places. | Move Method/Field to centralize responsibility, Extract Class, Hide Delegate, Introduce Parameter Object. | [`03`](02-refactoring-catalog.md), [`06`](02-refactoring-catalog.md) |
| Parallel Inheritance Hierarchies | Creating a subclass in one hierarchy forces creating a subclass in another. | Move Method/Field, Replace Inheritance with Delegation, Collapse Hierarchy, Extract Interface. | [`03`](02-refactoring-catalog.md), [`07`](02-refactoring-catalog.md) |

## Dispensables

| Code smell | Diagnosis | Recommended actions | Applicable files |
|---|---|---|---|
| Comments | Comments explain confusing code instead of complementing decision. | Extract Method, Rename Method, Extract Variable, Introduce Assertion for assumptions. | [`02`](02-refactoring-catalog.md), [`06`](02-refactoring-catalog.md), [`05`](02-refactoring-catalog.md) |
| Duplicate Code | Repeated code blocks appear in methods, classes or hierarchies. | Extract Method, Pull Up Method, Form Template Method, Extract Class. | [`02`](02-refactoring-catalog.md), [`07`](02-refactoring-catalog.md), [`03`](02-refactoring-catalog.md) |
| Lazy Class | Class does not justify its existence. | Inline Class, Collapse Hierarchy, remove speculative abstraction. | [`03`](02-refactoring-catalog.md), [`07`](02-refactoring-catalog.md) |
| Data Class | Class only has exposed data, without behavior. | Encapsulate Field/Collection, Move Method into the class, Replace Data Value with Object. | [`04`](02-refactoring-catalog.md), [`03`](02-refactoring-catalog.md) |
| Dead Code | Code is not called or is no longer needed. | Remove Method/Field/Class, Hide Method first if in doubt, validate coverage. | [`06`](02-refactoring-catalog.md), [`03`](02-refactoring-catalog.md) |
| Speculative Generality | Abstractions created for hypothetical future. | Collapse Hierarchy, Inline Class, Remove Parameter, Hide Method. | [`07`](02-refactoring-catalog.md), [`03`](02-refactoring-catalog.md), [`06`](02-refactoring-catalog.md) |

## Couplers

| Code smell | Diagnosis | Recommended actions | Applicable files |
|---|---|---|---|
| Feature Envy | Method seems more interested in data of another class. | Move Method, Extract Method, Preserve Whole Object. | [`03`](02-refactoring-catalog.md), [`02`](02-refactoring-catalog.md), [`06`](02-refactoring-catalog.md) |
| Inappropriate Intimacy | Classes know too much about each other's internal details. | Move Method/Field, Hide Delegate, Encapsulate Field/Collection, Replace Inheritance with Delegation. | [`03`](02-refactoring-catalog.md), [`04`](02-refactoring-catalog.md), [`07`](02-refactoring-catalog.md) |
| Message Chains | Client navigates through several chained calls to get something. | Hide Delegate, Extract Method, Preserve Whole Object. | [`03`](02-refactoring-catalog.md), [`02`](02-refactoring-catalog.md), [`06`](02-refactoring-catalog.md) |
| Middle Man | Class just delegates calls to another. | Remove Middle Man, Inline Class. | [`03`](02-refactoring-catalog.md) |
| Incomplete Library Class | Library lacks necessary method and cannot be changed. | Introduce Foreign Method or Introduce Local Extension. | [`03`](02-refactoring-catalog.md) |

## Final selection criterion

When a smell points to several techniques, choose the smallest intervention that:

1. solves the observed problem;
2. preserves behavior;
3. reduces coupling or complexity;
4. does not create speculative abstraction;
5. improves the next actual maintenance point.
