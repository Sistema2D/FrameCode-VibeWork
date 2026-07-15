---
schema: "fcvw/skill@1"
name: "systematic-debugging"
description: "Use evidence and hypotheses to diagnose failures before fixing them."
version: "1.2.0"
trigger_keywords:
  - "debug"
  - "stack trace"
  - "root cause"
  - "diagnose"
  - "depurar"
session_types:
  - "bugfix"
  - "troubleshooting"
---

# Systematic debugging

## Purpose

Find the smallest evidence-supported cause of a failure and distinguish diagnosis from implementation authorization.

## Use conditions

Use for reproducible defects, crashes, failed checks, unexpected behavior, or inconsistent runtime state. For a question limited to diagnosis, do not apply a fix. For an authorized fix, follow the active plan and changelog contract.

## Non-responsibilities

- unrelated refactoring or speculative cleanup;
- suppressing symptoms without explaining the cause;
- publishing secrets, credentials, or unnecessary raw logs;
- treating an unverified hypothesis as a finding.

## Inputs

Expected behavior, observed behavior, environment, reproduction steps, logs or stack traces, recent changes, and the narrowest relevant source and test files.

## Procedure

1. Reproduce the problem or state why reproduction is currently impossible.
2. Capture the exact symptom, environment, and smallest failing case.
3. Form one ranked hypothesis tied to concrete evidence.
4. Design a check that can disprove that hypothesis.
5. Run the check and update the hypothesis from the result.
6. Repeat until the cause is supported or the investigation is explicitly inconclusive.
7. If a fix is authorized, add or identify a regression check, apply the minimal change, remove temporary instrumentation, and rerun affected validation.
8. Promote durable incident learning to a troubleshooting record when recurrence, severity, or operational value justifies it.

## Required output

Symptom, reproduction status, evidence, tested hypotheses, supported root cause or remaining uncertainty, affected scope, and validation results. If code changed, link the active plan and changelog entry.

## Validation

The original failure is reproduced before the fix when feasible, the causal check changes as predicted, the regression check passes afterward, and unrelated validation has not regressed.

## Exit criteria

Exit when the cause is supported and the authorized fix is validated, or when the remaining blocker and next evidence needed are recorded without presenting speculation as resolution.
