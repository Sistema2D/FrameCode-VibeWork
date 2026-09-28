---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---


# Refactoring guide

Detailed reference for [REFACTORING.md](REFACTORING.md). Load only the section that the current refactoring needs; the policy and its block criteria stay in REFACTORING.md. Templates for every stage are sections of [TEMPLATE_REFACTORING.md](governance/TEMPLATE_REFACTORING.md).


## How to use this guide


Governance structure for deciding, executing, reviewing, and auditing refactorings based on the Refactoring.Guru catalog scenarios, supplemented with operational controls for large codebases.

> Core principle: refactoring improves the internal structure of the code without altering the observable behavior of the system. Every change must be small, testable, reversible, and recorded.

### How to Use

1. Start with [section 01](#01--decision-guide) to identify the technical scenario.
2. Use [section 08](#08--code-smells-map) when the problem is perceived as a "code smell", but the technique is not yet clear.
3. For large codebases, first fill out [section 10](#10--code-inventory-and-classification), [section 11](#11--refactoring-risk-matrix), and [section 16](#16--dependency-and-impact-map).
4. Define tests, pipeline, rollback, and an incremental plan before opening PRs with medium, high, or critical risk.
5. Use [TEMPLATE_REFACTORING.md](governance/TEMPLATE_REFACTORING.md) to copy the necessary templates.
6. Use [section 09](#09--refactoring-pull-request-checklist) before opening or approving a Pull Request.

### Governance Files

| File | Purpose |
|---|---|
| [section 00](#00--general-refactoring-governance) | Universal rules, roles, entry and exit criteria, risks, and approval levels. |
| [section 01](#01--decision-guide) | Decision-making guide to identify the scenario and direct to the applicable file. |
| [section 02](#02--refactoring-catalog) | Symptom-to-family routing for the classic catalog, general family rules, and the mandatory FCVW governance for each. The literature is referenced, not reproduced. |
| [section 08](#08--code-smells-map) | Diagnostic map by code smell, providing directions to applicable techniques. |
| [section 09](#09--refactoring-pull-request-checklist) | Objective checklist for review, evidence, tests, rollback, and acceptance. |
| [section 10](#10--code-inventory-and-classification) | Inventory of modules, dependencies, criticality, owners, coverage, and critical points. |
| [section 11](#11--refactoring-risk-matrix) | Risk scoring matrix and mandatory controls by level. |
| [section 12](#12--testing-strategy-before-refactoring) | Testing strategy for characterization, regression, integration, contract, e2e, and smoke tests. |
| [section 13](#13--cicd-pipeline-and-quality-gates) | Minimum CI/CD and quality gates for safe merge/deploy. |
| [section 14](#14--rollback-plan) | Rollback strategies, triggers, and post-rollback validation. |
| [section 15](#15--incremental-refactoring-plan) | Splitting large refactorings into small, reversible increments. |
| [section 16](#16--dependency-and-impact-map) | Mapping of direct and indirect consumers, contracts, data, events, and configuration. |
| [section 17](#17--branch-and-pull-request-policy) | Rules for branches, commits, PRs, approvals, and merges. |
| [section 18](#18--behavioral-refactoring-vs-rewrite) | Separation between pure refactoring, feature, fix, partial rewrite, and total rewrite. |
| [section 19](#19--stopping-criteria) | Criteria to pause, split, replan, revert, or cancel refactorings. |
| [TEMPLATE_REFACTORING.md](governance/TEMPLATE_REFACTORING.md) | Templates index for practical application of the governance. |

### Templates

Official templates are indexed in [governance/README.md](governance/README.md). For PRs, use the *pull request* section of [TEMPLATE_REFACTORING.md](governance/TEMPLATE_REFACTORING.md) and copy it to the target repository only when that repository uses pull requests.

### Technical Coverage

This governance covers the six families from the refactoring catalog:

- Composing Methods;
- Moving Features between Objects;
- Organizing Data;
- Simplifying Conditional Expressions;
- Making Method Calls Simpler;
- Dealing with Generalization.

It also includes a decision map by code smells to support the initial problem identification.

### Operational Coverage for Large Codebases

Beyond techniques, the governance now covers:

- Code inventory and classification;
- Risk matrix;
- Testing strategy before refactoring;
- Pipeline and quality gates;
- Rollback;
- Incremental plan;
- Dependency and impact map;
- Branches and PRs policy;
- Separation between refactoring and rewrite;
- Stopping criteria.

### Reference Sources

- Refactoring.Guru — Refactoring Catalog: https://refactoring.guru/refactoring/catalog
- Refactoring.Guru — Code Smells: https://refactoring.guru/refactoring/smells

## 00 — General Refactoring Governance

### Objective

Establish common rules for any refactoring, regardless of the applied technique.

### Operational Definition

A change is classified as **refactoring** when:

- It does not alter the functional behavior perceived by the user;
- It does not add a requirement, business rule, or new feature;
- It improves readability, modularity, testability, isolation, cohesion, coupling, or maintainability;
- It can be validated by automated tests, controlled manual tests, or before/after comparison.

### Mandatory Rules

1. **Do not mix refactoring with a feature.** If there is a new feature, separate it into another PR or commit.
2. **Create a baseline before the change.** Record existing tests, expected behavior, and risk points.
3. **Make small changes.** Prefer several small refactorings instead of a massive change.
4. **Preserve public APIs, unless explicitly decided otherwise.** Public changes require versioning, a migration plan, and communication.
5. **Run tests before and after.** When there are no tests, create characterization tests before refactoring.
6. **Ensure simple rollback.** The PR must allow reversion without data loss or irreversible contract alteration.
7. **Record intention.** Each PR must declare the code smell, the scenario, and the applied technique.
8. **Avoid refactoring unstable code unnecessarily.** Prioritize areas that are frequently changed, have recurring bugs, or high maintenance costs.
9. **Maintain domain names.** Do not replace terms recognized by the business with generic names.
10. **Measure impact when possible.** Cyclomatic complexity, duplication, method/class size, test coverage, and dependencies can be used as evidence.

### Roles

| Role | Responsibility |
|---|---|
| Refactoring Author | Diagnose scenario, apply technique, write tests, and document evidence. |
| Technical Reviewer | Verify preservation of behavior, architectural coherence, and adherence to this guide. |
| Module Owner | Approve changes to public contracts, data models, integrations, and critical rules. |
| QA/Validator | Validate critical flows when the functional risk is medium or high. |

### Risk Levels and Approval

| Level | Example | Minimum Requirement |
|---|---|---|
| Low | Rename private method, extract variable, remove isolated dead code. | 1 technical reviewer + local tests. |
| Medium | Extract class, move method between classes, alter internal encapsulation. | 1 technical reviewer + module owner + automated tests. |
| High | Alter public contract, class hierarchy, persisted data model, or critical flow. | 2 reviewers + module owner + rollback plan + functional validation. |

### Entry Criteria

Before starting, confirm:

- Identified problem and candidate technique;
- Delimited scope;
- Tests or characterization scenario available;
- Affected dependencies mapped;
- Known risks recorded.

### Exit Criteria

The refactoring can only be considered complete when:

- Previous behavior was preserved;
- Relevant tests passed;
- Names, responsibilities, and dependencies became clearer;
- There was no unjustified increase in complexity;
- Obsolete documentation or comments were removed or updated;
- PR checklist was completed.

### Commit Policy

Use small and semantic commits:

```text
refactor(method): extract calculation of monthly balance
refactor(data): replace type code with state strategy
refactor(api): preserve whole object in scheduling service
```

### When Not to Refactor

Do not execute refactoring when:

- There is no test, nor time to create a characterization test;
- The module will be discarded in the short term;
- The gain is merely aesthetic and increases risk;
- The change would require altering multiple consumers without a plan;
- The problem is a poorly defined business rule, not a bad code structure.

### Minimum Evidence in the PR

- Identified scenario;
- Applied technique;
- File from this governance used;
- Summarized before/after;
- Executed tests;
- Risks and rollback;
- Pending items, if any.

## 01 — Decision Guide

Use this file to identify the refactoring scenario and direct the team to the applicable file.

### Quick Decision by Symptom

| Observed Symptom | Confirmation Question | Applicable File |
|---|---|---|
| Long method, difficult to understand, or with blocks that seem to have their own intention. | Are there excerpts that could have their own name? | [section 02](#02--refactoring-catalog) |
| Complex expression, confusing temporary variable, or algorithm difficult to replace. | Is the difficulty inside a method? | [section 02](#02--refactoring-catalog) |
| Method or field seems to belong to another class. | Does another class use this behavior/data more? | [section 02](#02--refactoring-catalog) |
| Class does too much work or almost nothing. | Is the responsibility incorrectly concentrated or dispersed? | [section 02](#02--refactoring-catalog) |
| Excessive dependency through call chains or useless delegation. | Does the client know too many objects or is there an intermediate without value? | [section 02](#02--refactoring-catalog) |
| Primitive data represent domain concepts. | Does the data have its own rule, validation, unit, format, or behavior? | [section 02](#02--refactoring-catalog) |
| Public fields, exposed collections, heterogeneous array, or magic number. | Is the data vulnerable to improper alteration? | [section 02](#02--refactoring-catalog) |
| Complex, duplicated, nested, or type-based conditional. | Does the decision logic hinder reading, extension, or testing? | [section 02](#02--refactoring-catalog) |
| Many `null`s, control flags, or implicit premises. | Is there a special flow that should be explicit? | [section 02](#02--refactoring-catalog) |
| Method has a bad name, too many parameters, unused parameter, or complex constructor. | Is the call interface confusing or unstable? | [section 02](#02--refactoring-catalog) |
| Method returns a value and changes state at the same time. | Does the call mix query and command? | [section 02](#02--refactoring-catalog) |
| Inheritance contains duplication, misplaced subclasses, or excessive hierarchy. | Is the problem in the abstraction between classes? | [section 02](#02--refactoring-catalog) |
| Delegation replaces inheritance or inheritance replaces delegation improperly. | Is the "is-a" or "has-a" relationship poorly modeled? | [section 02](#02--refactoring-catalog) |
| The problem was perceived as a code smell, but the technique is still unclear. | Which smell closest matches the case? | [section 08](#08--code-smells-map) |

### Decision Flow

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

### Rules for Choosing Between Similar Techniques

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

### Expected Decision Output

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
### Operational Layer for Large Bases

After identifying the technical scenario, apply the operational triage below.

| Condition | Mandatory File |
|---|---|
| Refactoring involves more than one module, folder, or package. | [section 10](#10--code-inventory-and-classification) |
| Refactoring involves critical, public area, without tests or with unknown dependencies. | [section 11](#11--refactoring-risk-matrix) |
| Legacy code, without coverage or with poorly documented behavior. | [section 12](#12--testing-strategy-before-refactoring) |
| PR depends on build, tests, lint, static analysis, or controlled deploy. | [section 13](#13--cicd-pipeline-and-quality-gates) |
| Medium, high, or critical risk refactoring. | [section 14](#14--rollback-plan) |
| Large change, with many files or multiple stages. | [section 15](#15--incremental-refactoring-plan) |
| Move, rename, extract class, alter signature, contract, or data. | [section 16](#16--dependency-and-impact-map) |
| Open PR, define branch, review, or approve. | [section 17](#17--branch-and-pull-request-policy) |
| Doubt whether the change is a refactoring, bugfix, feature, or rewrite. | [section 18](#18--behavioral-refactoring-vs-rewrite) |
| Scope grew, tests failed, or unforeseen risks emerged. | [section 19](#19--stopping-criteria) |

### Recommended Full Flow

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

### Routing Map by Scenario (read on demand for AI)

To optimize tokens, read only what is necessary for the current activity.

| Situation | Read | Observation |
|---|---|---|
| Common base (once per session or opening) | [section 00](#00--general-refactoring-governance) | Does not need to be reread for each activity. |
| Doubt if it is pure refactoring | [section 18](#18--behavioral-refactoring-vs-rewrite) | Classifies refactoring vs fix/feature/rewrite. |
| Symptom inside method/expression | [section 02](#02--refactoring-catalog) | Use when the problem is inside the method. |
| Complex conditional, flags, or `null` | [section 02](#02--refactoring-catalog) | Use when the decision is difficult to read/test. |
| Responsibility between classes/objects | [section 02](#02--refactoring-catalog) | Method/field in the wrong place, class too large/small. |
| Data/encapsulation problem | [section 02](#02--refactoring-catalog) | Primitives, exposed collections, type codes. |
| Confusing call interface | [section 02](#02--refactoring-catalog) | Bad name, many parameters, mixed return/effect. |
| Abstraction, inheritance, or delegation | [section 02](#02--refactoring-catalog) | Excessive hierarchy, improper inheritance. |
| Smell without clear technique | [section 08](#08--code-smells-map) | Use to discover the technical file. |
| Specific operational conditions | Table “Operational Layer for Large Bases” | Read only the file(s) pointed to by the condition. |
| Needs template | [TEMPLATE_REFACTORING.md](governance/TEMPLATE_REFACTORING.md) | Copy only the applicable template. |

## 02 — Refactoring Catalog

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

### General family rules

These rules apply to every technique in the catalog and are the part FCVW
actually enforces:

- apply only when observable behavior can be preserved;
- prefer small steps, with tests run between each step;
- record the scenario, the technique, and the evidence that behavior did not change;
- stop refactoring if a functional change becomes necessary, and open a separate task;
- a refactoring and a behavior change never share the same batch without explicit plan scope.

### Symptom to family routing

Use this table to choose the family and then consult the source for the exact
technique. The governance column names what must exist in the active plan.

| Observed symptom | Catalog family | Mandatory FCVW governance |
|---|---|---|
| Long method, unclear expression, confusing temporary variable | Composing methods | [section 11](#11--refactoring-risk-matrix) |
| Responsibility on the wrong object, feature envy, inappropriate intimacy | Moving features between objects | [section 16](#16--dependency-and-impact-map) |
| Public field, type code, exposed collection, bidirectional association | Organizing data | [section 12](#12--testing-strategy-before-refactoring) |
| Complex conditional, duplicated branch, nesting, control flag | Simplifying conditional expressions | [section 12](#12--testing-strategy-before-refactoring) |
| Poor name, long parameter list, overloaded constructor, exception used as flow | Making method calls simpler | [section 09](#09--refactoring-pull-request-checklist) |
| Wrong hierarchy, duplication across subclasses, inheritance used as a shortcut | Dealing with generalization | [section 18](#18--behavioral-refactoring-vs-rewrite) |

### Where the FCVW-specific policy lives

The rest of this guide was not condensed, because it carries its own rules
rather than reproducing literature:

- decision and inventory: [section 01](#01--decision-guide),
  [section 10](#10--code-inventory-and-classification);
- risk, testing, and stopping: [section 11](#11--refactoring-risk-matrix),
  [section 12](#12--testing-strategy-before-refactoring),
  [section 19](#19--stopping-criteria);
- execution and rollback: [section 15](#15--incremental-refactoring-plan),
  [section 14](#14--rollback-plan);
- boundaries: [section 18](#18--behavioral-refactoring-vs-rewrite).

Top-level refactoring policy stays in [`REFACTORING.md`](REFACTORING.md), and
the size and responsibility gate in
[`skills/anti-monolith-guard/SKILL.md`](skills/anti-monolith-guard/SKILL.md).

### Relationships

Governed by [section 00](#00--general-refactoring-governance) and
catalogued in [How to use this guide](#how-to-use-this-guide).

## 08 — Code Smells Map

Use this file when the problem was perceived as a code smell, but the technique is not yet clear.

Base source: https://refactoring.guru/refactoring/smells

### Bloaters

| Code smell | Diagnosis | Recommended actions | Applicable files |
|---|---|---|---|
| Long Method | Method grew and became hard to understand or change. | Extract Method, Decompose Conditional, Replace Temp with Query, Replace Method with Method Object. | [`02`](#02--refactoring-catalog), [`05`](#02--refactoring-catalog) |
| Large Class | Class concentrates too many data and behaviors. | Extract Class, Move Method/Field, Encapsulate Record, Extract Superclass/Interface if there is real abstraction. | [`03`](#02--refactoring-catalog), [`04`](#02--refactoring-catalog), [`07`](#02--refactoring-catalog) |
| Primitive Obsession | Primitives represent rich domain concepts. | Replace Data Value with Object, Replace Type Code with Class/Subclasses/State/Strategy, Introduce Parameter Object. | [`04`](#02--refactoring-catalog), [`06`](#02--refactoring-catalog) |
| Long Parameter List | Method demands too many parameters. | Preserve Whole Object, Introduce Parameter Object, Replace Parameter with Method Call, Remove Parameter. | [`06`](#02--refactoring-catalog) |
| Data Clumps | The same data group appears together in several places. | Introduce Parameter Object, Extract Class, Replace Array with Object. | [`04`](#02--refactoring-catalog), [`06`](#02--refactoring-catalog) |

### Object-Orientation Abusers

| Code smell | Diagnosis | Recommended actions | Applicable files |
|---|---|---|---|
| Switch Statements | Decisions by type/state appear repeatedly. | Replace Conditional with Polymorphism, Replace Type Code with Subclasses or State/Strategy, Decompose Conditional. | [`04`](#02--refactoring-catalog), [`05`](#02--refactoring-catalog) |
| Temporary Field | Field is only used at certain moments, leaving state inconsistent. | Extract Class, Introduce Null Object, Replace Method with Method Object when state belongs to a computation. | [`02`](#02--refactoring-catalog), [`03`](#02--refactoring-catalog), [`05`](#02--refactoring-catalog) |
| Refused Bequest | Subclass inherits members it doesn't use or shouldn't expose. | Push Down Method/Field, Replace Inheritance with Delegation, Extract Interface. | [`07`](#02--refactoring-catalog) |
| Alternative Classes with Different Interfaces | Classes do similar things with different names/contracts. | Rename Method, Extract Interface, Move Method, Parameterize Method. | [`06`](#02--refactoring-catalog), [`07`](#02--refactoring-catalog), [`03`](#02--refactoring-catalog) |

### Change Preventers

| Code smell | Diagnosis | Recommended actions | Applicable files |
|---|---|---|---|
| Divergent Change | One class changes for different reasons. | Extract Class, Move Method/Field, organize data by responsibility. | [`03`](#02--refactoring-catalog), [`04`](#02--refactoring-catalog) |
| Shotgun Surgery | A small change requires editing many places. | Move Method/Field to centralize responsibility, Extract Class, Hide Delegate, Introduce Parameter Object. | [`03`](#02--refactoring-catalog), [`06`](#02--refactoring-catalog) |
| Parallel Inheritance Hierarchies | Creating a subclass in one hierarchy forces creating a subclass in another. | Move Method/Field, Replace Inheritance with Delegation, Collapse Hierarchy, Extract Interface. | [`03`](#02--refactoring-catalog), [`07`](#02--refactoring-catalog) |

### Dispensables

| Code smell | Diagnosis | Recommended actions | Applicable files |
|---|---|---|---|
| Comments | Comments explain confusing code instead of complementing decision. | Extract Method, Rename Method, Extract Variable, Introduce Assertion for assumptions. | [`02`](#02--refactoring-catalog), [`06`](#02--refactoring-catalog), [`05`](#02--refactoring-catalog) |
| Duplicate Code | Repeated code blocks appear in methods, classes or hierarchies. | Extract Method, Pull Up Method, Form Template Method, Extract Class. | [`02`](#02--refactoring-catalog), [`07`](#02--refactoring-catalog), [`03`](#02--refactoring-catalog) |
| Lazy Class | Class does not justify its existence. | Inline Class, Collapse Hierarchy, remove speculative abstraction. | [`03`](#02--refactoring-catalog), [`07`](#02--refactoring-catalog) |
| Data Class | Class only has exposed data, without behavior. | Encapsulate Field/Collection, Move Method into the class, Replace Data Value with Object. | [`04`](#02--refactoring-catalog), [`03`](#02--refactoring-catalog) |
| Dead Code | Code is not called or is no longer needed. | Remove Method/Field/Class, Hide Method first if in doubt, validate coverage. | [`06`](#02--refactoring-catalog), [`03`](#02--refactoring-catalog) |
| Speculative Generality | Abstractions created for hypothetical future. | Collapse Hierarchy, Inline Class, Remove Parameter, Hide Method. | [`07`](#02--refactoring-catalog), [`03`](#02--refactoring-catalog), [`06`](#02--refactoring-catalog) |

### Couplers

| Code smell | Diagnosis | Recommended actions | Applicable files |
|---|---|---|---|
| Feature Envy | Method seems more interested in data of another class. | Move Method, Extract Method, Preserve Whole Object. | [`03`](#02--refactoring-catalog), [`02`](#02--refactoring-catalog), [`06`](#02--refactoring-catalog) |
| Inappropriate Intimacy | Classes know too much about each other's internal details. | Move Method/Field, Hide Delegate, Encapsulate Field/Collection, Replace Inheritance with Delegation. | [`03`](#02--refactoring-catalog), [`04`](#02--refactoring-catalog), [`07`](#02--refactoring-catalog) |
| Message Chains | Client navigates through several chained calls to get something. | Hide Delegate, Extract Method, Preserve Whole Object. | [`03`](#02--refactoring-catalog), [`02`](#02--refactoring-catalog), [`06`](#02--refactoring-catalog) |
| Middle Man | Class just delegates calls to another. | Remove Middle Man, Inline Class. | [`03`](#02--refactoring-catalog) |
| Incomplete Library Class | Library lacks necessary method and cannot be changed. | Introduce Foreign Method or Introduce Local Extension. | [`03`](#02--refactoring-catalog) |

### Final selection criterion

When a smell points to several techniques, choose the smallest intervention that:

1. solves the observed problem;
2. preserves behavior;
3. reduces coupling or complexity;
4. does not create speculative abstraction;
5. improves the next actual maintenance point.

## 09 — Refactoring Pull Request Checklist

Use this checklist before opening, reviewing, or approving any refactoring PR.

### Identification

```markdown
- [ ] The PR is pure refactoring, with no new feature or rule.
- [ ] The refactoring scenario was identified.
- [ ] The applicable governance file was cited.
- [ ] The related code smell was informed, when applicable.
- [ ] The scope is delimited and didn't grow during the change.
```

### Functional safety

```markdown
- [ ] Tests were executed before the change, when existing.
- [ ] Characterization tests were created when there wasn't enough coverage.
- [ ] Tests were executed after the change.
- [ ] The affected critical flows were validated.
- [ ] There was no intentional change of observable behavior.
```

### Refactoring quality

```markdown
- [ ] The change reduced complexity, duplication, coupling, or ambiguity.
- [ ] The new names reflect intent and domain vocabulary.
- [ ] Responsibilities became more cohesive.
- [ ] Encapsulation was preserved or improved.
- [ ] No speculative abstraction was created.
- [ ] There was no unjustified increase in indirection.
```

### Contracts and compatibility

```markdown
- [ ] Public APIs were preserved or have a migration plan.
- [ ] Changed public signatures were approved by the module owner.
- [ ] Persistence, serialization, routes, events, and integrations were verified.
- [ ] Frameworks that use reflection/annotations/conventions were considered.
```

### Evidence in PR

```markdown
- [ ] The PR describes before/after in objective language.
- [ ] The PR lists affected files/modules.
- [ ] The PR informs tests executed and result.
- [ ] The PR describes residual risks.
- [ ] The PR informs rollback strategy.
```

### Review

```markdown
- [ ] Reviewer confirmed that the applied technique matches the scenario.
- [ ] Reviewer verified that the change could be reverted without structural damage.
- [ ] Reviewer evaluated if a simpler technique would solve the same problem.
- [ ] Module owner approved, if the risk is medium or high.
- [ ] QA/functional validation approved, if there's any critical flow affected.
```

### PR description template

```markdown
## Type
Pure refactoring

## Scenario
E.g.: Long Method / Extract Method

## Governance file used
E.g.: 02-composing-methods.md

## Motivation
Explain the observed maintenance problem.

## Performed change
Explain what changed structurally, without focusing on feature.

## Preserved behavior
Explain why the external behavior remains the same.

## Executed tests
- [ ] Unit
- [ ] Integration
- [ ] E2E
- [ ] Controlled manual

## Risks
List residual risks.

## Rollback
Explain how to revert.
```
### Additional checklist for large codebases

- [ ] Module inventory filled when the change goes beyond local scope.
- [ ] Risk matrix filled.
- [ ] Dependencies and impact map attached.
- [ ] Characterization tests created for legacy code or without coverage.
- [ ] Pipeline executed with gates applicable to the risk level.
- [ ] Rollback plan registered.
- [ ] Incremental plan defined for broad changes.
- [ ] PR does not mix refactoring with feature, bugfix, or rewrite without justification.
- [ ] Stopping criteria known by the team.
- [ ] Refactoring PR template filled.

## 10 — Code Inventory and Classification

This file defines how to inventory an application before starting refactoring in large codebases, especially when there are thousands of files, multiple folders, legacy modules, or poorly documented dependencies.

### Objective

Prevent the team from refactoring "in the dark". No structural refactoring should begin without a minimal overview of:

- existing modules, packages, services, components, libraries, and routes;
- files critical for execution, build, deploy, authentication, authorization, payments, data, or integrations;
- internal and external dependencies;
- areas with low test coverage;
- areas with high change frequency;
- areas without a clear technical owner.

### When to use

Mandatory use before any refactoring that involves:

- more than one module, folder, or package;
- moving files, classes, services, components, or public functions;
- changing a public signature;
- changing shared code;
- changes to infrastructure, build, configuration, routes, databases, or APIs;
- code without sufficient automated tests.

### Governance rule

> Refactoring a large codebase requires a minimal inventory before the first change. Without an inventory, refactoring must be limited to local scope, reversible, and low-impact.

### Mandatory minimal inventory

| Item | What to map | Expected evidence |
|---|---|---|
| Physical structure | Folders, files, modules, packages, and subprojects. | Summarized tree or inventory report. |
| Entrypoints | Initialization files, routes, commands, jobs, workers, scripts, and main pages. | List with path and purpose. |
| Functional domains | Business areas or system capabilities. | Map module → domain. |
| Internal dependencies | Who calls whom, imports, extends, delegates, events, and contracts. | Graph, table, or report. |
| External dependencies | Libraries, SDKs, APIs, services, queues, databases, and external files. | Versioned list. |
| Existing tests | Unit, integration, contract, e2e, smoke, and manual tests. | Test paths and estimated coverage. |
| Critical points | Authentication, authorization, data, payments, integration, security, compliance, and deploy. | Criticality tags. |
| Technical owners | Person/team responsible for review and acceptance. | Defined owner per module. |
| Legacy code | Areas without tests, without an owner, with low readability, or obsolete dependencies. | `LEGACY` tag. |
| Dead code | Files, methods, classes, or routes with no confirmed usage. | `CANDIDATE_FOR_REMOVAL` tag, never remove without validation. |

### Classification by module

Each module must receive the following classification:

| Field | Options | Criteria |
|---|---|---|
| Functional criticality | Low / Medium / High / Critical | Impact on users, operations, or revenue. |
| Exposure | Internal / Public / External | If it is used by other modules, clients, or integrations. |
| Test coverage | High / Medium / Low / Absent | Protection against regression. |
| Coupling | Low / Medium / High | Quantity and strength of dependencies. |
| Volatility | Low / Medium / High | Change frequency in recent cycles. |
| Complexity | Low / Medium / High | Size, branching, duplication, and reading difficulty. |
| Technical owner | Name/team | Responsible for approval. |
| Change window | Free / Controlled / Restricted | When it can be changed or deployed. |

### Inventory levels

#### Level 1 — Quick inventory

Applicable to local and low-risk refactorings.

Mandatory to map:

- modified file(s);
- existing tests;
- direct calls;
- expected behavior before/after;
- rollback strategy via `git revert`.

#### Level 2 — Module inventory

Applicable to medium refactorings.

Mandatory to map:

- complete module;
- inbound and outbound dependencies;
- owner;
- characterization tests;
- public contracts;
- build/deploy risks.

#### Level 3 — Systemic inventory

Applicable to broad refactorings.

Mandatory to map:

- dependencies between modules;
- critical business flows;
- persisted data;
- external integrations;
- jobs/queues/events;
- incremental plan;
- rollback plan;
- technical and functional approval.

### Useful indicators

To prioritize areas, collect when possible:

- number of files per module;
- number of lines per module;
- cyclomatic complexity;
- duplication;
- test coverage;
- change frequency via `git log`;
- number of recent bugs per module;
- build and test time;
- obsolete dependencies;
- number of imports/cross-calls.

### Rules for very large codebases

1. Do not start with critical areas without tests.
2. Do not combine refactoring with a feature or functional fix.
3. Do not move many files in a single PR without justification and a validation plan.
4. Do not remove apparently dead code without confirmation through static search, logs, metrics, or owner validation.
5. Do not change a public signature without a map of consumers.
6. Do not change directory structure used by build, import aliases, bundlers, automatic routes, or framework conventions without a specific test.
7. Do not rely solely on textual search; use dependency analysis when the language/framework allows.

### Mandatory actions

Before refactoring:

- fill out the module inventory template;
- classify initial risk;
- define maximum scope of the first PR;
- identify minimum tests;
- register owner and approvers.

During refactoring:

- keep commits small;
- update the inventory if unmapped dependencies emerge;
- interrupt if the scope grows without approval.

After refactoring:

- update architecture documentation;
- record changes in dependencies;
- record validation evidence;
- archive the decision in the PR or ADR.

### Applicable template

Use the *module inventory* section of [TEMPLATE_REFACTORING.md](governance/TEMPLATE_REFACTORING.md).

## 11 — Refactoring Risk Matrix

This file defines how to classify the risk of each refactoring and which controls should be applied before, during, and after the change.

### Objective

Reduce the risk of breakage in large codebases through an objective assessment of impact, complexity, and test protection.

### Governance rule

> Every refactoring must have its risk classified before the first relevant commit. The risk level defines tests, approvals, maximum PR size, and rollback requirements.

### Risk factors

Score each factor from 0 to 3.

| Factor | 0 points | 1 point | 2 points | 3 points |
|---|---|---|---|---|
| Physical scope | 1 file | 2–5 files | 6–20 files | More than 20 files |
| Logical scope | Local method/function | Class/component | Module | Multiple modules |
| Exposure | Internal and private | Shared internal | Public internal API | External API/public contract |
| Test coverage | High | Medium | Low | Absent |
| Functional criticality | Low | Medium | High | Critical |
| Coupling | Low | Medium | High | Unknown/high and unmapped |
| Persisted data | Does not change | Read only | Write/serialization | Migration/persisted model |
| Integrations | None | Internal | External service | Critical external service |
| Concurrency/asynchronous | Not applicable | Low usage | Jobs/events | Critical concurrent flow |
| Build/deploy | Does not affect | Affects locally | Affects pipeline | Affects release/deploy/runtime |

### Risk level calculation

| Total score | Level | Interpretation |
|---:|---|---|
| 0–5 | Low | Local, reversible, and well-protected refactoring. |
| 6–12 | Medium | May affect module or internal consumers. |
| 13–20 | High | May cause relevant regression or require coordination. |
| 21–30 | Critical | May affect production, public contract, data, or multiple modules. |

### Controls per level

| Level | Mandatory actions |
|---|---|
| Low | Small PR; local tests; PR checklist; rollback by revert. |
| Medium | Module inventory; characterization tests; full CI; 1 technical reviewer. |
| High | Dependency map; incremental plan; rollback plan; integration/regression tests; 2 reviewers, 1 being an owner. |
| Critical | Formal technical approval; change window; feature flag when applicable; smoke test; validated rollback; post-merge monitoring. |

### Blocking rules

Refactoring must be blocked when any of the following conditions occur:

- complete absence of tests in a critical area;
- unknown technical owner for a critical module;
- unmapped public dependencies;
- functional change mixed with refactoring;
- non-existent rollback plan for high or critical risk;
- database change without reversible migration or compensatory strategy;
- PR too large for effective review.

### Strategies to reduce risk

| Identified risk | Mitigation action |
|---|---|
| Many files | Divide by module, layer, or functional flow. |
| Low coverage | Create characterization tests before changing. |
| Public API | Preserve compatibility, create an adapter, or do gradual deprecation. |
| Circular dependency | Break into stages: interface, adapter, migration, cleanup. |
| Legacy code without owner | Define temporary owner and approve limited scope. |
| Persisted data | Create migration, backup, rollback, and validation plan. |
| Multiple consumers | Create consumer map and prior communication. |

### Evidence required in the PR

```markdown
### Refactoring risk
- Total score:
- Risk level:
- Highest weight factors:
- Mitigations applied:
- Test evidence:
- Rollback strategy:
- Mandatory approvers:
```

### Applicable template

Use the *risk matrix* section of [TEMPLATE_REFACTORING.md](governance/TEMPLATE_REFACTORING.md).

## 12 — Testing Strategy Before Refactoring

This file defines the minimum protection necessary before refactoring. The goal is to ensure that the observable behavior remains the same after the change.

### Principle

> Before improving the internal structure, it is necessary to capture the current behavior. In legacy code, characterization tests are more important than idealized tests.

### Test layers

| Layer | Purpose | When to require |
|---|---|---|
| Characterization tests | Freeze current behavior, including strange behaviors that already exist. | Legacy code, without tests or with unclear rules. |
| Unit tests | Protect isolated functions/classes. | Local or rule refactoring. |
| Integration tests | Protect communication between modules, database, queues, services, or layers. | Module or dependency refactoring. |
| Contract tests | Ensure APIs, events, DTOs, and formats have not changed. | Public interfaces or those consumed by third parties. |
| End-to-end tests | Validate critical user flows. | High-impact modules. |
| Smoke tests | Confirm that the system initializes and essential flows respond. | After merge/deploy. |
| Visual regression | Validate screens/components. | UI, reports, dashboards, PDFs, or layouts. |
| Performance baseline | Compare time, memory, queries, or processing. | Algorithms, loops, queries, jobs, and large data volumes. |

### Minimum criteria by risk level

| Level | Minimum tests before refactoring |
|---|---|
| Low | Unit test or simple characterization; local execution. |
| Medium | Characterization tests + relevant unit tests + CI. |
| High | Characterization + integration + affected flow regression + smoke. |
| Critical | All of the above + contract/e2e/performance when applicable + checklist-guided manual validation. |

### Characterization tests

Use when current behavior is not clearly documented.

#### Rules

1. Do not try to "fix" the behavior in the test.
2. Record the current behavior as it is.
3. Cover common inputs, boundaries, and known strange cases.
4. Use anonymized real data or representative fixtures.
5. Run the tests before and after each small refactoring.

#### What to characterize

- inputs and outputs;
- exceptions and messages;
- side effects;
- important logs;
- database/file/cache changes;
- simulated external calls;
- event order when relevant;
- behavior on `null`, empty, boundary, and error.

### Tests before moving code

Before applying refactorings like `Move Method`, `Move Field`, `Extract Class`, `Extract Superclass`, `Extract Interface`, or module changes:

- test current calls;
- test direct consumers;
- test serialization/deserialization if there are DTOs;
- test imports, routes, or automatic framework resolution;
- test clean project build;
- test relative paths and aliases.

### Tests before changing public calls

Before `Rename Method`, `Add Parameter`, `Remove Parameter`, `Introduce Parameter Object`, `Replace Constructor with Factory Method` or similar changes:

- list consumers;
- preserve compatibility when possible;
- create contract tests;
- temporarily keep old method if there are external consumers;
- define deprecation when necessary.

### Tests before changing data

Before encapsulating a collection, replacing value/reference object, changing type code, replacing array with object, or changing association:

- test serialization;
- test persistence;
- test migration, if any;
- test equality and identity;
- test validations;
- test compatibility with old data.

### Entry criteria

Refactoring can only begin when:

- current tests have been executed and the initial state is known;
- pre-existing failures have been recorded;
- characterization tests have been created for critical behavior without coverage;
- local environment or CI can reproduce the tests;
- test data has been stabilized.

### Exit criteria

Refactoring can only be considered completed when:

- all relevant tests pass;
- coverage has not decreased without justification;
- observable behavior has been preserved;
- new tests have been kept, not just temporarily used;
- evidence has been attached to the PR.

### Applicable template

Use the *characterization test plan* section of [TEMPLATE_REFACTORING.md](governance/TEMPLATE_REFACTORING.md).

## 13 — CI/CD Pipeline and Quality Gates

This file defines the automation controls that must protect refactorings before merge and, when applicable, before deploy.

### Objective

Ensure that a refactoring does not enter the main branch without minimal automated evidence of quality, build, testing, and compatibility.

### Governance rule

> No medium, high, or critical risk refactoring should be approved with a broken pipeline, ignored tests without justification, or pending quality analysis.

### Minimum gates

| Gate | Purpose | Mandatory for |
|---|---|---|
| Clean build | Confirm compilation/packaging. | All levels. |
| Lint/format | Avoid noise and divergent patterns. | All levels. |
| Unit tests | Validate local behavior. | All levels when they exist. |
| Integration tests | Validate communication between parts. | Medium or higher. |
| Contract tests | Validate APIs/events/DTOs. | High/critical or public interface. |
| E2e/smoke tests | Validate user flow or initialization. | High/critical. |
| Type check | Validate static types when applicable. | Typed projects. |
| Static analysis | Detect bugs, vulnerabilities, duplication, complexity. | Medium or higher. |
| Coverage | Prevent unjustified reduction. | Medium or higher. |
| Dependency scan | Detect library impact and security. | When dependencies change. |
| Artifact generation | Confirm packaging/deploy. | High/critical. |

### Pipeline policy

1. The main branch pipeline must be green before starting.
2. Pre-existing failures must be registered before refactoring.
3. New failures block merge.
4. Removed or ignored tests require explicit justification.
5. Changes to the pipeline itself must be in a separate PR.
6. Refactoring must not relax quality rules to pass.
7. Quality metrics should improve or remain stable.

### Gates by risk

#### Low

- build;
- lint/format;
- local tests or available CI;
- PR checklist.

#### Medium

- build;
- lint/format;
- unit tests;
- characterization tests when applicable;
- coverage without unjustified drop;
- 1 technical reviewer.

#### High

- all medium risk gates;
- integration/regression tests;
- static analysis;
- attached impact map;
- rollback plan;
- 2 reviewers.

#### Critical

- all high risk gates;
- smoke/e2e of critical flows;
- artifact validation;
- execution in staging/homologation environment when it exists;
- post-deploy monitoring;
- formal approval from the owner.

### Recommended metrics

- coverage before/after;
- build time before/after;
- test time before/after;
- cyclomatic complexity;
- duplication;
- number of changed files;
- number of added/removed lines;
- added/removed dependencies;
- number of warnings.

### Rules for monorepos or very large codebases

- Execute tests affected by the dependency graph when available.
- Run the full suite before merge on high-impact PRs.
- Avoid global formatting changes together with logical refactoring.
- Separate dependency update PR from refactoring PR.
- On import/path changes, validate clean build from scratch.

### Evidence in the PR

```markdown
### Executed gates
- Build: passed/failed/link
- Lint/format: passed/failed/link
- Unit tests: passed/failed/link
- Integration/e2e/smoke: passed/failed/link
- Coverage before/after:
- Static analysis:
- Observations:
```

## 14 — Rollback Plan

This file defines how to plan safe rollback of refactorings when there is a failure, instability, regression, or unexpected impact.

### Objective

Ensure that every relevant refactoring is reversible without improvisation.

### Governance rule

> Medium, high, or critical risk refactorings must have a rollback plan registered before merge. Critical refactorings must have the rollback tested or simulated.

### Rollback types

| Type | When to use | Observation |
|---|---|---|
| `git revert` | Purely structural refactoring, without data migration. | Preferable for low/medium risk. |
| Rollback via previous release | When deploy allows reverting artifact/version. | Requires available previous version. |
| Feature flag | When the change can be turned on/off. | Ideal for high/critical risk. |
| Compatibility adapter | When old and new APIs coexist. | Reduces impact on consumers. |
| Reversible migration | When there is a database/persisted data. | Must include reversal script or compensatory strategy. |
| Reversible configuration | When change depends on env/config. | Record key, old value, and new value. |
| Corrective hotfix | Last resort when complete rollback is unfeasible. | Requires approval and exception record. |

### What the plan must contain

- previous safe version/commit;
- exact scope of the change;
- signals that trigger rollback;
- person responsible for the decision;
- reversal steps;
- validation after reversal;
- risks of reverting;
- estimated reversal time;
- necessary communication;
- plan to preserve data, if applicable.

### Criteria that trigger rollback

Rollback must be considered when the following occurs:

- failure in critical flow;
- error increase in production;
- relevant performance degradation;
- public contract break;
- build/deploy failure not quickly resolved;
- data inconsistency;
- authentication/authorization failure;
- user complaints in directly affected flow;
- divergent behavior without identified cause.

### Rules for database changes

1. Do not remove column/field used by previous version in the same release.
2. Prefer expand/contract migrations.
3. Maintain compatibility between old and new version during transition window.
4. Have backup or snapshot when risk is high/critical.
5. Validate migration in representative environment.
6. Define strategy for data created by the new version.

### Rules for APIs and integrations

1. Do not break contract without versioning or communication.
2. Temporarily preserve old endpoints/methods when there are external consumers.
3. Record known consumers.
4. Test compatibility with old and new payload.
5. Have adapter or fallback when possible.

### Validation after rollback

After reverting, execute:

- build;
- smoke test;
- affected flow test;
- log/error check;
- data validation, if applicable;
- stabilization communication.

### Applicable template

Use the *rollback plan* section of [TEMPLATE_REFACTORING.md](governance/TEMPLATE_REFACTORING.md).

## 15 — Incremental Refactoring Plan

This file defines how to break down large refactorings into small, reviewable, and reversible steps.

### Objective

To avoid "big bang refactoring", that is, a large change that is difficult to review, test, revert, and understand.

### Governance rule

> Every refactoring that spans more than one module, one layer, or 20 files must be planned in increments. Each increment must compile, test, and preserve behavior.

### Principles

1. A PR must have a main objective.
2. Each commit must be understandable and reversible.
3. Mechanical changes must be separated from structural changes.
4. Mass renamings must be separated from logic changes.
5. Gradual deprecation is preferable to immediate breaking.
6. At each step, the system must continue working.

### Breakdown strategies

| Strategy | When to use | Example |
|---|---|---|
| By module | Modularized system. | Refactor `billing` before `orders`. |
| By layer | Layered architecture. | First domain, then application, then UI. |
| By flow | Clear business flows. | Login, registration, checkout. |
| By technique | Many possible techniques. | First extract methods, then move classes. |
| By compatibility | APIs or public data. | Create adapter, migrate consumers, remove legacy. |
| By risk | Critical and non-critical areas. | Start with the least critical module. |

### Recommended sequence

1. Inventory and dependency map.
2. Characterization tests.
3. Low-risk local cleanup.
4. Introduction of abstraction/adapter, if necessary.
5. Migration of consumers in parts.
6. Removal of legacy code.
7. Consolidation of names, documentation, and tests.
8. Post-refactoring validation.

### Recommended PR size

| Risk | Suggested size |
|---|---|
| Low | Up to 5 files, local scope. |
| Medium | Up to 10 files or a small module. |
| High | Prefer up to 8 files per PR and one intention at a time. |
| Critical | Minimal PRs, with feature flag/adapter and specific validation. |

> The number of files is a reference, not an absolute rule. Automatically generated changes, renamings, and formatting must be explicitly justified.

### Increment patterns

#### Expand → Migrate → Contract

Use when there is a public contract, database, DTO, API, or shared dependency.

1. Create a new compatible structure.
2. Keep the old structure working.
3. Migrate consumers gradually.
4. Monitor and validate.
5. Remove the old structure.

#### Temporary adapter

Use when the new code cannot replace the old one all at once.

1. Create a common interface.
2. Wrap the old implementation.
3. Introduce the new implementation.
4. Toggle usage by module/flag.
5. Remove the adapter when migration is finished.

#### Strangler Fig

Use to replace part of a legacy subsystem.

1. Isolate the legacy boundary.
2. Create a new component alongside it.
3. Redirect cases gradually.
4. Validate equivalent behavior.
5. Deactivate the old section.

### What not to do

- Mix refactoring with new functionality.
- Open a giant PR with "general adjustments".
- Replace the entire architecture without a rollback path.
- Refactor code without an owner and without tests.
- Perform global renaming along with behavioral changes.
- Remove legacy code before migrating consumers.

### Applicable template

Use the *incremental plan* section of [TEMPLATE_REFACTORING.md](governance/TEMPLATE_REFACTORING.md).

## 16 — Dependency and Impact Map

This file defines how to identify dependencies before moving, renaming, extracting, inlining, or altering code interfaces.

### Objective

To prevent a local refactoring from causing breakages in direct or indirect consumers.

### Governance rule

> Before changing a signature, moving a file/class/method, changing a contract, reorganizing a package, or encapsulating shared data, it is mandatory to map input and output dependencies.

### Dependency types

| Type | Examples | Risk |
|---|---|---|
| Direct call | imports, method calls, component usage. | Compilation/runtime breakage. |
| Inheritance | extends, implements, mixins, traits. | Behavior and polymorphism breakage. |
| Reflection/convention | automatic routes, decorators, annotations, file names. | Difficult to detect by textual search. |
| Data | DTOs, schemas, database, cache, files, localStorage. | Data incompatibility. |
| Events | queues, pub/sub, webhooks, signals. | Silent asynchronous breakage. |
| Configuration | env vars, paths, aliases, build config. | Build/deploy failure. |
| UI | components, styles, routes, assets. | Visual/functional regression. |
| External integration | APIs, SDKs, partners, automations. | Breakage outside the repository. |

### Mandatory map

For each altered item, record:

- source of the change;
- direct consumers;
- indirect consumers;
- public contracts;
- existing tests;
- risk of breakage;
- compatibility plan;
- validation plan.

### Impact questions

Before the change:

1. Who imports this file?
2. Who calls this method/function?
3. Who instantiates this class?
4. Is there usage by string, reflection, configuration, or convention?
5. Is there a related route, event, job, or automation?
6. Is there a schema, migration, DTO, or external contract?
7. Is there serialization in database, cache, session, or file?
8. Is there documentation or an example that will become obsolete?
9. Is there a test that will fail if the behavior changes?
10. Is there a consumer outside the repository?

### Impact classification

| Impact | Criterion | Action |
|---|---|---|
| Local | Only the altered file consumes the change. | Local tests and simple PR. |
| Intra-module | Several files in the same module. | Module tests and owner review. |
| Inter-module | Other modules depend on it. | Dependency map and incremental PR. |
| Internal public | Other internal teams/services consume it. | Contract, communication, and compatibility. |
| External public | External consumers or integrations. | Versioning, deprecation, and formal plan. |

### Techniques that require an impact map

Mandatory for:

- Move Method;
- Move Field;
- Extract Class;
- Inline Class;
- Hide Delegate;
- Remove Middle Man;
- Encapsulate Field;
- Encapsulate Collection;
- Replace Type Code with Class/Subclasses/State/Strategy;
- Rename Method;
- Add/Remove Parameter;
- Introduce Parameter Object;
- Replace Constructor with Factory Method;
- Extract Superclass/Interface/Subclass;
- Replace Inheritance with Delegation;
- Replace Delegation with Inheritance.

### Compatibility strategy

When consumers cannot be updated all at once:

- keep a temporary alias;
- create an old method delegating to the new one;
- add an adapter;
- version API;
- deprecate with warning;
- migrate consumers in batches;
- remove legacy only after confirmation.

### Evidence in the PR

```markdown
### Impact map
- Altered item:
- Direct consumers:
- Indirect consumers:
- Public contracts:
- Risk of breakage:
- Compatibility strategy:
- Executed tests:
```

### Applicable template

Use the *dependency map* section of [TEMPLATE_REFACTORING.md](governance/TEMPLATE_REFACTORING.md).

## 17 — Branch and Pull Request Policy

This file defines rules for organizing branches, commits, Pull Requests, and approvals in refactorings.

### Objective

To keep refactorings reviewable, traceable, and reversible.

### Governance rule

> Refactoring must be proposed in a PR with a clear scope, without mixing with a feature or functional fix, except for justified and approved exceptions.

### Branch name

Recommended pattern:

```text
refactor/<module>/<short-objective>
```

Examples:

```text
refactor/auth/extract-token-validator
refactor/orders/introduce-parameter-object
refactor/ui/split-large-component
refactor/shared/encapsulate-collection
```

### Commit types

Use small and semantic commits:

```text
refactor(auth): extract token validation method
refactor(order): move pricing calculation to PricingService
test(order): add characterization tests for discount rules
chore(ci): add affected module test job
```

### Rules for commits

1. Each commit should compile whenever possible.
2. Separate test, movement, renaming, and cleanup commits.
3. Avoid "format all files" along with refactoring.
4. Messages should explain the intention, not just the altered files.
5. Tool-generated commits must be identified.

### PR Size

| Level | Guidance |
|---|---|
| Low | Small PR, simple review. |
| Medium | PR limited to one module or objective. |
| High | Divide into sequential PRs; review by owner. |
| Critical | Minimal PR, with plan, window, rollback, and formal validation. |

### Mandatory PR content

Every refactoring PR must inform:

- problem/symptom;
- code smell, if applicable;
- refactoring technique used;
- main files altered;
- justification for not altering behavior;
- executed tests;
- classified risk;
- rollback;
- relevant evidence.

### Approval

| Risk | Minimum approval |
|---|---|
| Low | 1 reviewer or module owner, according to team policy. |
| Medium | 1 technical reviewer. |
| High | 2 reviewers, including module owner. |
| Critical | Technical owner + functional/architecture lead when applicable. |

### Merge rules

Do not allow merge when:

- pipeline failed;
- there is an unresolved conflict;
- scope grew without updating the risk matrix;
- tests were removed without justification;
- there is undeclared functional alteration;
- rollback was not defined for medium or higher risk;
- review requested PR division and this was not addressed.

### Chained PRs policy

For incremental refactoring:

1. Open base PR with characterization tests.
2. Open preparation/abstraction PR.
3. Open migration PRs per module.
4. Open legacy removal PR.
5. Open final cleanup/documentation PR.

### Applicable template

Use the *pull request* section of [TEMPLATE_REFACTORING.md](governance/TEMPLATE_REFACTORING.md) and copy to `.github/pull_request_template.md` in the destination repository when you want a standard PR template.

## 18 — Behavioral Refactoring vs. Rewrite

This file helps separate pure refactoring from a fix, feature, behavioral change, and rewrite.

### Principle

> Refactoring alters the internal structure without altering observable behavior. If the behavior changes, the change must be treated as a fix, feature, or partial rewrite, not as pure refactoring.

### Change classification

| Type | External behavior changes? | Example | How to treat |
|---|---|---|---|
| Pure refactoring | No | Extract method, move class while maintaining API. | Refactoring PR. |
| Preparatory refactoring | Not now | Create interface/adapter for future feature. | Refactoring PR with clear motivation. |
| Fix | Yes | Fix calculation, rule, or validation. | Separate bugfix PR. |
| Feature | Yes | Add new flow, field, endpoint. | Separate feature PR. |
| Partial rewrite | Might change | Replace legacy module with new implementation. | Formal plan with compatibility and validation. |
| Total rewrite | Yes/high risk | Replace entire system or subsystem. | Separate project, not just refactoring PR. |

### Signs it is not pure refactoring

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

### When to separate PRs

Always separate when there is:

- bugfix along with structural cleanup;
- change of public contract;
- database alteration;
- dependency update;
- pipeline alteration;
- visual change;
- new functionality;
- behavior alteration in an existing test.

### Recommended order

When a feature depends on structural cleanup:

1. PR 1 — characterization tests;
2. PR 2 — preparatory refactoring without changing behavior;
3. PR 3 — feature/fix;
4. PR 4 — post-feature cleanup, if necessary.

### When to accept an exception

Only accept mixing refactoring and fix when:

- the fix is minimal and unavoidable to make the test reliable;
- the old behavior was clearly defective and was documented;
- the reviewer explicitly agreed;
- the PR describes exactly what changed.

### Decision: refactor or rewrite?

| Situation | Preference |
|---|---|
| Code works, but is hard to maintain. | Refactor incrementally. |
| Code has isolated bugs and acceptable architecture. | Fix and refactor in stages. |
| Code has no tests, but behavior is critical. | Create characterization before any decision. |
| Code depends on obsolete and unsupported technology. | Plan incremental replacement. |
| Code no longer meets the domain and requires new logic. | Partial rewrite/feature project, not pure refactoring. |
| Entire system is unmaintainable. | Evaluate rewrite as a separate project, with migration. |

### Evidence in the PR

```markdown
### Nature of the change
- Type: pure refactoring / preparatory / fix / feature / partial rewrite
- External behavior altered? Yes/No
- Evidence of behavior preservation:
- Functional changes, if any:
- Justification for keeping in the same PR, if applicable:
```

## 19 — Stopping Criteria

This file defines when to stop, divide, replan, or revert a refactoring.

### Objective

To prevent a refactoring from continuing even when signs show increased risk, loss of control, or unexpected impact.

### Governance rule

> The team must stop refactoring when the actual risk exceeds the approved risk, when the behavior becomes uncertain, or when validation cannot keep up with the change.

### Technical stopping criteria

Stop immediately when:

- previously green tests start failing without a clear cause;
- build breaks in areas outside the scope;
- relevant unmapped dependencies arise;
- PR grows larger than planned;
- change requires altering an unforeseen public contract;
- observed behavior diverges from characterization tests;
- there is data loss or inconsistency in the test environment;
- performance degrades significantly;
- review shows that the change has become a rewrite;
- automatic tool altered unexpected files.

### Organizational stopping criteria

Stop when:

- technical owner is not available to approve;
- change window has ended;
- another team depends on the affected area;
- there is a critical release in progress;
- there is an active incident related to the module;
- the objective of the refactoring is no longer clear.

### Actions after stopping

| Situation | Action |
|---|---|
| Small and localized failure | Fix within the same PR, if it does not alter scope. |
| Scope increased | Pause, update risk, and divide PR. |
| Unmapped dependency | Update impact map before continuing. |
| Behavior breakage | Revert the last increment and review tests. |
| PR became feature/rewrite | Separate into a new plan and new PR. |
| Failure in production | Trigger rollback plan. |

### Possible states

| State | Meaning |
|---|---|
| Continue | Controlled risk and sufficient validation. |
| Pause | Uncertain risk; requires analysis. |
| Divide | Scope larger than reviewable. |
| Replan | Assumptions have changed. |
| Revert | Change is not safe or broke behavior. |
| Cancel | Benefit does not outweigh risk/cost. |

### Stopping checklist

When stopping, record:

- reason;
- affected commit/PR;
- evidence;
- new risk;
- decision made;
- responsible person;
- next action;
- deadline for re-evaluation.

### Resumption

Refactoring can only be resumed when:

- cause of the stop has been understood;
- risk has been reclassified;
- tests have been adjusted or added;
- scope has been reduced, if necessary;
- owner approved the resumption;
- rollback plan remains valid.

### Decision record

Use ADR when the stop results in an architectural change, module replanning, approach replacement, or relevant cancellation.

Recommended template: the *adr* section of [TEMPLATE_REFACTORING.md](governance/TEMPLATE_REFACTORING.md).
