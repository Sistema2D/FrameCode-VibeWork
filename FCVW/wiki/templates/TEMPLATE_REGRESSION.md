# Template: confirmed regression

```markdown
---
schema: "fcvw/regression@1"
id: "REG-YYYYMMDD-short-id"
title: "<Short title>"
type: "functional | interface | data | visual | security | ai | governance | documentation | performance | operations"
severity: "R1 | R2 | R3 | R4 | R5"
status: "detected | mitigated | resolved | accepted | superseded"
detected_at: "YYYY-MM-DD"
last_reviewed: "YYYY-MM-DD"
related_plan: "<plan-id>"
sources:
  - "<failure, test, diff, log, or authoritative path>"
tags:
  - "regression-prevention"
---

# <Regression title>

## What regressed

<Previously protected behavior and observed unwanted change.>

## Detection

<How and where the regression was detected.>

## Root cause

<Supported cause; distinguish it from symptoms.>

## Missing or failed guardrail

<Why existing checks did not prevent or detect it earlier.>

## Permanent guardrail

<Test, contract, policy, watcher, or boundary added or strengthened.>

## Replay test

<Procedure that fails on the regressed state and passes on the corrected state, when practical.>

## Related release and records

- Plan: `<plan-id>`
- Changelog/framework release: `<path>`
- Troubleshooting/decision: `<path or not applicable>`

## Residual risk and review

<Remaining risk, owner, and review trigger/date; or `None`.>
```
