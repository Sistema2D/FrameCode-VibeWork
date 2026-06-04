# 15 — Incremental Refactoring Plan

This file defines how to break down large refactorings into small, reviewable, and reversible steps.

## Objective

To avoid "big bang refactoring", that is, a large change that is difficult to review, test, revert, and understand.

## Governance rule

> Every refactoring that spans more than one module, one layer, or 20 files must be planned in increments. Each increment must compile, test, and preserve behavior.

## Principles

1. A PR must have a main objective.
2. Each commit must be understandable and reversible.
3. Mechanical changes must be separated from structural changes.
4. Mass renamings must be separated from logic changes.
5. Gradual deprecation is preferable to immediate breaking.
6. At each step, the system must continue working.

## Breakdown strategies

| Strategy | When to use | Example |
|---|---|---|
| By module | Modularized system. | Refactor `billing` before `orders`. |
| By layer | Layered architecture. | First domain, then application, then UI. |
| By flow | Clear business flows. | Login, registration, checkout. |
| By technique | Many possible techniques. | First extract methods, then move classes. |
| By compatibility | APIs or public data. | Create adapter, migrate consumers, remove legacy. |
| By risk | Critical and non-critical areas. | Start with the least critical module. |

## Recommended sequence

1. Inventory and dependency map.
2. Characterization tests.
3. Low-risk local cleanup.
4. Introduction of abstraction/adapter, if necessary.
5. Migration of consumers in parts.
6. Removal of legacy code.
7. Consolidation of names, documentation, and tests.
8. Post-refactoring validation.

## Recommended PR size

| Risk | Suggested size |
|---|---|
| Low | Up to 5 files, local scope. |
| Medium | Up to 10 files or a small module. |
| High | Prefer up to 8 files per PR and one intention at a time. |
| Critical | Minimal PRs, with feature flag/adapter and specific validation. |

> The number of files is a reference, not an absolute rule. Automatically generated changes, renamings, and formatting must be explicitly justified.

## Increment patterns

### Expand → Migrate → Contract

Use when there is a public contract, database, DTO, API, or shared dependency.

1. Create a new compatible structure.
2. Keep the old structure working.
3. Migrate consumers gradually.
4. Monitor and validate.
5. Remove the old structure.

### Temporary adapter

Use when the new code cannot replace the old one all at once.

1. Create a common interface.
2. Wrap the old implementation.
3. Introduce the new implementation.
4. Toggle usage by module/flag.
5. Remove the adapter when migration is finished.

### Strangler Fig

Use to replace part of a legacy subsystem.

1. Isolate the legacy boundary.
2. Create a new component alongside it.
3. Redirect cases gradually.
4. Validate equivalent behavior.
5. Deactivate the old section.

## What not to do

- Mix refactoring with new functionality.
- Open a giant PR with "general adjustments".
- Replace the entire architecture without a rollback path.
- Refactor code without an owner and without tests.
- Perform global renaming along with behavioral changes.
- Remove legacy code before migrating consumers.

## Applicable template

Use [`../governance/TEMPLATE_REFACTORING_INCREMENTAL_PLAN.md`](../governance/TEMPLATE_REFACTORING_INCREMENTAL_PLAN.md).
