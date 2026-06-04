# 16 — Dependency and Impact Map

This file defines how to identify dependencies before moving, renaming, extracting, inlining, or altering code interfaces.

## Objective

To prevent a local refactoring from causing breakages in direct or indirect consumers.

## Governance rule

> Before changing a signature, moving a file/class/method, changing a contract, reorganizing a package, or encapsulating shared data, it is mandatory to map input and output dependencies.

## Dependency types

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

## Mandatory map

For each altered item, record:

- source of the change;
- direct consumers;
- indirect consumers;
- public contracts;
- existing tests;
- risk of breakage;
- compatibility plan;
- validation plan.

## Impact questions

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

## Impact classification

| Impact | Criterion | Action |
|---|---|---|
| Local | Only the altered file consumes the change. | Local tests and simple PR. |
| Intra-module | Several files in the same module. | Module tests and owner review. |
| Inter-module | Other modules depend on it. | Dependency map and incremental PR. |
| Internal public | Other internal teams/services consume it. | Contract, communication, and compatibility. |
| External public | External consumers or integrations. | Versioning, deprecation, and formal plan. |

## Techniques that require an impact map

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

## Compatibility strategy

When consumers cannot be updated all at once:

- keep a temporary alias;
- create an old method delegating to the new one;
- add an adapter;
- version API;
- deprecate with warning;
- migrate consumers in batches;
- remove legacy only after confirmation.

## Evidence in the PR

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

## Applicable template

Use [`../governance/TEMPLATE_REFACTORING_DEPENDENCY_MAP.md`](../governance/TEMPLATE_REFACTORING_DEPENDENCY_MAP.md).
