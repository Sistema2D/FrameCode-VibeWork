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

## Template: FCVW harness hooks

Ready contract for `FCVW/tools/hook_fcvw.py`. Keep only the `hook_events` and `harnesses` the project configures; the validator checks that both sides match, and the hooks act only while `status` is `active`. Link the saved contract from `PROJECT.md`.

```markdown
---
schema: "fcvw/automation@1"
id: "AUT-YYYY-MM-DD-harness-hooks"
kind: "hook"
status: "active"
owner: "<owner>"
scenario: "2"
execution_mode: "scenario_2"
authorized_by: "<person and date who enabled the hooks>"
implementation: "FCVW/tools/hook_fcvw.py"
hook_events:
  - "session-start"
  - "pre-edit"
  - "stop"
harnesses:
  - "claude-code"
  - "codex"
trigger: "SessionStart, PreToolUse on file edits and Stop of the listed harnesses"
preconditions: "python3 available; Codex project trusted"
actions: "session-start adds FCVW status; pre-edit denies versioned edits without a plan in progress; stop validates changes since HEAD"
evidence: "harness transcript (hook events) and the plan's validation section"
failure_policy: "deny edits without a plan; stop continues once on validation errors; tool errors or timeouts allow"
rollback: "set status to paused or retired; FCVW_HOOKS=off for one session; remove the harness configuration"
created_at: "YYYY-MM-DD"
updated_at: "YYYY-MM-DD"
---

# FCVW harness hooks

## Trigger and scope

Agent sessions in this repository run by the listed harnesses (`.claude/settings.json`, `.codex/hooks.json`).

## Preconditions and permissions

Read access to the repository and permission to run `python3`. The hooks write nothing, change no git state and call no network.

## Ordered actions

1. Session start: add plans in progress and routing guidance.
2. Before an edit: deny it when no plan is in `FCVW/Plans/in_progress/` and none was completed in uncommitted work.
3. Before the agent stops: validate changes since `HEAD`.

## Evidence

Hook events in the harness transcript; validation results in the active plan.

## Pass, warn, block, and failure policy

Deny edits without a plan. Stop continues once with the listed errors. A hook error or timeout allows the action.

## Idempotency, retry, and concurrency

Stateless checks; safe to repeat. The stop hook does not block twice in one stop cycle.

## Timeout and stop conditions

Stop validation times out after 120 seconds and then allows.

## Rollback or disable

Set `status` to `paused` (every hook stops acting) or `retired`; `FCVW_HOOKS=off` for one session.

## Validation

`validate_fcvw.py` checks that the contract and the harness configuration match (`automation-binding`).

## Lifecycle event

`pre_edit | session_close | custom`

## Checks

- [ ] Plan in progress before versioned edits; decision in the harness transcript.

## Bypass

- Authority: <owner>.
- Justification: trivial prose fixes allowed by AGENTS.md.
- Expiry: per session (`FCVW_HOOKS=off`).
- Follow-up: none.
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
