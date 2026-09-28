# Template: automation contract

One envelope for every kind described in [AUTOMATION.md](../AUTOMATION.md). The sections after the envelope are the kind-specific checklists.

```markdown
---
schema: "fcvw/automation@1"
id: "AUT-YYYY-MM-DD-slug"
kind: "hook | watcher | daemon | governance_gate"
status: "draft | active | paused | retired"
owner: "<owner>"
scenario: "1 | 2 | 3"
execution_mode: "scenario_1 | scenario_2 | scenario_3"
authorized_by: "<required for scenario 2 or 3>"
trigger: "<event or boundary>"
preconditions: "<what must hold before running>"
actions: "<ordered checks or reactions>"
evidence: "<where results are recorded>"
failure_policy: "<pass, warn and block handling; timeout>"
rollback: "<disable or revert procedure>"
created_at: "YYYY-MM-DD"
updated_at: "YYYY-MM-DD"
---

# Contract title

## Trigger and scope

## Preconditions and permissions

## Ordered actions

## Evidence

## Pass, warn, block, and failure policy

## Idempotency, retry, and concurrency

## Timeout and stop conditions

## Rollback or disable

## Validation
```

## Template: hook check

Use `TEMPLATE_AUTOMATION_CONTRACT.md` with `kind: hook` and add:

```markdown
## Lifecycle event

`pre_edit | pre_commit | pre_release | post_deploy | session_close | custom`

## Checks

- [ ] Check, expected result, evidence destination.

## Bypass

- Authority:
- Justification:
- Expiry:
- Follow-up:
```

## Template: watcher rule

Use `TEMPLATE_AUTOMATION_CONTRACT.md` with `kind: watcher` and add:

```markdown
## Event source and match

## Debounce and deduplication

## Bounded reaction

## Retry and maximum attempts

## Alert and disable condition
```

## Template: maintenance loop

Use `TEMPLATE_AUTOMATION_CONTRACT.md` with `kind: daemon` and add:

```markdown
## Cadence

## One iteration

## Work and time budget

## Lock and checkpoint

## Stop, pause, and escalation
```

## Template: governance gate report

Use `TEMPLATE_AUTOMATION_CONTRACT.md` with `kind: governance_gate` and add:

```markdown
## Transition controlled

## Evidence reviewed

## Checks

| Check | Result | Evidence |
|---|---|---|
| | pass / warn / block | |

## Decision

`pass | warn | block`

## Required actions and owner

## Bypass, residual risk, and expiry

For a Regression gate, include the protected behaviors, consulted contracts, replay results, limitations, rollback status, and the related plan's Regression impact section.
```
