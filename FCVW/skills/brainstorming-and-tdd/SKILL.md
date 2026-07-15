---
schema: "fcvw/skill@1"
name: "brainstorming-and-tdd"
description: "Clarify behavior and use test-first implementation when applicable."
version: "1.2.0"
trigger_keywords:
  - "new feature"
  - "fix bug"
  - "tdd"
  - "brainstorm"
session_types:
  - "feature"
  - "bugfix"
---

# Behavior design and test-first development

## Purpose

Turn an implementation request into observable behavior and use the smallest useful test-first loop to reduce ambiguity and regression risk.

## Use conditions

Use for behavior changes where an automated unit, integration, contract, or end-to-end check is practical. Ask a blocking question only when missing information would materially change scope or outcome; otherwise state a bounded assumption and proceed.

## Non-responsibilities

- requiring TDD for pure documentation, exploratory spikes, or surfaces with no practical harness;
- expanding the feature beyond agreed acceptance criteria;
- replacing product decisions with test implementation details;
- creating brittle tests that assert incidental structure instead of behavior.

## Inputs

User outcome, current behavior, edge cases, constraints, acceptance criteria, affected interfaces, existing tests, and active plan.

## Procedure

1. Express the request as actors, trigger, observable result, boundaries, and failure cases.
2. Resolve material ambiguity and record assumptions.
3. Select the narrowest test level that proves the behavior.
4. For a defect, reproduce it with a failing regression check when feasible; for legacy code, use a characterization test before changing behavior.
5. Run the new check and confirm it fails for the intended reason.
6. Implement the smallest plan-scoped change that satisfies it.
7. Rerun the focused check, then the relevant regression suite.
8. Refactor only while all checks remain green and within scope.

## Required output

Concise behavior specification, assumptions, test level, red/green evidence, implementation scope, regression results, and any justified manual validation.

## Validation

The test fails before implementation for the expected reason, passes after the change, remains meaningful if the defect is reintroduced, and does not depend on irrelevant internals.

## Exit criteria

Exit when acceptance criteria are demonstrated by appropriate evidence, or when the missing test capability and alternative validation are recorded explicitly.
