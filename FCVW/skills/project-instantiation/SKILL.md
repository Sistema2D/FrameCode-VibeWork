---
schema: "fcvw/skill@1"
name: "project-instantiation"
description: "Instantiate project-owned FCVW profiles from a clean baseline."
version: "1.1.1"
trigger_keywords:
  - "instantiate project"
  - "bootstrap"
  - "new project"
  - "instanciar"
session_types:
  - "instantiation"
  - "planning"
---

# Project instantiation

## Purpose

Convert clean project profiles into evidence-backed application truth without editing framework policies or reusable templates.

## Use conditions

Use only for a verified clean-template workspace becoming a new application. Existing or partially governed applications use `retroactive-instantiation` instead.

## Inputs

`INSTANTIATION.md`, `BRIEFING.md`, `OWNERSHIP.md`, `FRAMEWORK_LOCK.md`, and user-approved product context.

## Procedure

1. Confirm the workspace is a clean template, not an existing application.
2. Create the instantiation plan.
3. Complete briefing gaps or record questions.
4. Fill project profiles and set one application version source.
5. Preserve framework policies and templates.
6. Remove or explicitly waive project-profile placeholders.
7. Set profile `instantiation_status: complete`.
8. Run validator with `instantiated` profile.

## Non-responsibilities

- global recursive replacement;
- inventing product decisions;
- copying any production-derived comparison fixture or another application's history as project truth;
- changing framework version.

## Required output

Completed profiles, first application plan/changelog, remaining questions, and validation report.

## Validation and exit

Ownership is correct, required profiles are complete, version namespaces are separate, and no example/history contamination exists.
