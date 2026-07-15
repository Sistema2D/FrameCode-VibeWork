---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Declarative automation contracts

## Scenario definitions

| Scenario | Meaning | Allowed implementation |
|---|---|---|
| Scenario 1 | Core portable baseline | Markdown contract executed manually or by an authorized agent |
| Scenario 2 | Optional local validation | Repository-owned script or command explicitly enabled by the project |
| Scenario 3 | External automation | CI, scheduler, service, or provider integration approved and documented by the project |

Scenario 1 never installs hooks, starts background processes, schedules work, or performs external side effects by implication.

## Contract types

- **Hook:** check at a named lifecycle boundary.
- **Watcher:** event/reaction rule; no continuous process is implied.
- **Daemon:** bounded recurring maintenance loop with stop conditions.
- **Governance gate:** pass/block/warn decision before state transition.

All contracts use `fcvw/automation@1` and define trigger, preconditions, actions, evidence, failure policy, rollback, owner, permissions, and execution mode.

## Execution rule

A Markdown contract describes expected behavior. It does not prove execution. Evidence must identify who or what ran the contract, when, inputs, result, and remaining failures.

Executable implementation requires a separate plan, security review, environment ownership, test strategy, disable/rollback path, and explicit user authorization when external effects are involved.
