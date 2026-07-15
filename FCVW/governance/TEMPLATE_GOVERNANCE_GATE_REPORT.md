# Template: governance gate report

```markdown
---
schema: "fcvw/automation@1"
id: "GATE-YYYY-MM-DD-slug"
kind: "gate"
status: "active"
owner: "<owner>"
execution_mode: "scenario_1"
created_at: "YYYY-MM-DD"
updated_at: "YYYY-MM-DD"
---

# Gate name

## Trigger and transition controlled

## Preconditions and permissions

## Evidence reviewed

## Checks

| Check | Result | Evidence |
|---|---|---|
| | pass / warn / block | |

## Decision

`pass | warn | block`

## Required actions and owner

## Failure policy

## Bypass, residual risk, and expiry

## Rollback or disable

For a Regression gate, include the protected behaviors, consulted contracts, replay results, limitations, rollback status, and the related plan's Regression impact section.
```
