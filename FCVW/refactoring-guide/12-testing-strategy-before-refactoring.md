# 12 — Testing Strategy Before Refactoring

This file defines the minimum protection necessary before refactoring. The goal is to ensure that the observable behavior remains the same after the change.

## Principle

> Before improving the internal structure, it is necessary to capture the current behavior. In legacy code, characterization tests are more important than idealized tests.

## Test layers

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

## Minimum criteria by risk level

| Level | Minimum tests before refactoring |
|---|---|
| Low | Unit test or simple characterization; local execution. |
| Medium | Characterization tests + relevant unit tests + CI. |
| High | Characterization + integration + affected flow regression + smoke. |
| Critical | All of the above + contract/e2e/performance when applicable + checklist-guided manual validation. |

## Characterization tests

Use when current behavior is not clearly documented.

### Rules

1. Do not try to "fix" the behavior in the test.
2. Record the current behavior as it is.
3. Cover common inputs, boundaries, and known strange cases.
4. Use anonymized real data or representative fixtures.
5. Run the tests before and after each small refactoring.

### What to characterize

- inputs and outputs;
- exceptions and messages;
- side effects;
- important logs;
- database/file/cache changes;
- simulated external calls;
- event order when relevant;
- behavior on `null`, empty, boundary, and error.

## Tests before moving code

Before applying refactorings like `Move Method`, `Move Field`, `Extract Class`, `Extract Superclass`, `Extract Interface`, or module changes:

- test current calls;
- test direct consumers;
- test serialization/deserialization if there are DTOs;
- test imports, routes, or automatic framework resolution;
- test clean project build;
- test relative paths and aliases.

## Tests before changing public calls

Before `Rename Method`, `Add Parameter`, `Remove Parameter`, `Introduce Parameter Object`, `Replace Constructor with Factory Method` or similar changes:

- list consumers;
- preserve compatibility when possible;
- create contract tests;
- temporarily keep old method if there are external consumers;
- define deprecation when necessary.

## Tests before changing data

Before encapsulating a collection, replacing value/reference object, changing type code, replacing array with object, or changing association:

- test serialization;
- test persistence;
- test migration, if any;
- test equality and identity;
- test validations;
- test compatibility with old data.

## Entry criteria

Refactoring can only begin when:

- current tests have been executed and the initial state is known;
- pre-existing failures have been recorded;
- characterization tests have been created for critical behavior without coverage;
- local environment or CI can reproduce the tests;
- test data has been stabilized.

## Exit criteria

Refactoring can only be considered completed when:

- all relevant tests pass;
- coverage has not decreased without justification;
- observable behavior has been preserved;
- new tests have been kept, not just temporarily used;
- evidence has been attached to the PR.

## Applicable template

Use [`../governance/TEMPLATE_REFACTORING_CHARACTERIZATION_TEST_PLAN.md`](../governance/TEMPLATE_REFACTORING_CHARACTERIZATION_TEST_PLAN.md).
