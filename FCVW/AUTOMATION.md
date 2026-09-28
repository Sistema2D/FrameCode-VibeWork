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

All contracts use `fcvw/automation@1` and define trigger, preconditions, actions, evidence, failure policy, rollback, owner, permissions, and execution mode. Write every kind from [TEMPLATE_AUTOMATION_CONTRACT.md](governance/TEMPLATE_AUTOMATION_CONTRACT.md); the sections below list what each kind adds.

## Execution rule

A Markdown contract describes expected behavior. It does not prove execution. Evidence must identify who or what ran the contract, when, inputs, result, and remaining failures.

Executable implementation requires a separate plan, security review, environment ownership, test strategy, disable/rollback path, and explicit user authorization when external effects are involved.


## Local framework validation

The user-authorized [local validation contract](governance/LOCAL_VALIDATION_CONTRACT.md) implements Scenario 2. A maintainer explicitly invokes the runner; no hosted service, payment, credentials, scheduler or background process is required. The previous [hosted contract](https://github.com/Sistema2D/FrameCode-VibeWork/blob/5c3ed95a27d02ce1939bb937af7ab11dfee9c71d/FCVW/governance/CI_CONTRACT.md) is retired and its source workflow removed. Downloading a template does not activate automation.

## Hooks

A hook is a deterministic checklist at a lifecycle boundary such as pre-edit, pre-commit, pre-release, post-deploy, or session close.

Each hook declares:

- event and scope;
- execution mode: manual, agent, local tool, or CI;
- preconditions and required permissions;
- ordered checks;
- pass, warn, and block outcomes;
- evidence destination;
- timeout/failure behavior;
- bypass authority and expiry;
- rollback or disable procedure.

Scenario 1 hooks are Markdown checklists. Do not claim a Git hook is installed unless its executable artifact exists and was authorized.

## Watchers

A watcher maps an observable event to a bounded reaction.

Required fields:

- event source and matching condition;
- polling/event mechanism, if executable;
- debounce, deduplication, and idempotency;
- allowed actions and side effects;
- retry/backoff and maximum attempts;
- evidence and alert destination;
- stop/disable condition;
- owner and permission boundary.

In Scenario 1, a watcher is evaluated when an authorized human or agent observes the event. It is not a background process.


## Regression-prone events

| Observed event | Detection method | Required reaction | Contract owner | Blocking? |
|---|---|---|---|---|
| Existing public API, CLI, or file format changed | interface/contract diff | run Regression gate, test consumers, update compatibility contract | `REGRESSION_GUARDS.md` / `TESTS.md` | yes |
| Existing UI flow or state changed | route/component/state and visual diff | replay primary, adjacent, error, keyboard, and supported viewport states | `PROJECT.md` (design) / `TESTS.md` | yes |
| Data schema, migration, import/export, or retention changed | model/migration diff | validate prior data, reconciliation, backup, recovery, and rollback | `DATA.md` / `TESTS.md` | yes |
| Authentication, permission, or destructive boundary changed | security and denial-path diff | run allowed/denied misuse cases and security gate | `SECURITY.md` / `REGRESSION_GUARDS.md` | yes |
| Agent, prompt, skill, memory, or retrieval rule changed | instruction/source diff | replay allowed, denied, ambiguous, unavailable, and injection cases | `AI.md` / `REGRESSION_GUARDS.md` | yes |
| Governance schema, plan, release, or generated index changed | structural diff and validator | run positive and negative governance fixtures; check migration | `SCHEMAS.md` / `AUTOMATION.md` | yes |
| Bugfix touches unrelated files or responsibilities | changed-path/scope review | split the plan or explicitly expand and reassess risk | `PLANNING.md` | yes |
| Same regression recurs | regression-ledger search | reopen root cause, strengthen permanent guardrail, link prior record | `wiki/` (`type: regression` notes) | yes |

Event detection is advisory until observed; once matched, its blocking reaction is part of the active plan. Deduplicate repeated signals by affected contract and plan ID.

## Daemons (maintenance loops)

A daemon contract describes recurring maintenance but does not authorize a background service.

Define:

- objective and owner;
- cadence or trigger;
- bounded input set;
- one iteration's actions;
- maximum duration/work items;
- checkpoint and evidence;
- stop, pause, and failure conditions;
- concurrency lock;
- resource and permission limits;
- rollback/cleanup.

Scenario 1 executes at most one explicitly requested iteration. Persistent scheduling belongs to Scenario 3 and requires separate authorization.

## Governance gates

| Gate | Trigger | Minimum evidence | Blocking condition |
|---|---|---|---|
| Plan | versioned change | active plan and scope | no plan or wrong state |
| Regression | functional, visual, data, AI, security, refactoring, workflow, interface, operation, or documentation change | Regression impact, consulted contracts, protected-behavior replay, limitations, residual risk, rollback status | missing/generic/pending evidence, insufficient risk coverage, hidden known regression, or unapproved rollback gap |
| Security | auth, secrets, sensitive data, permissions | threat/misuse analysis and tests | unmitigated critical risk |
| Data | schema, migration, import/export, deletion | rehearsal and reconciliation | no backup/rollback for R4/R5 |
| Refactoring | behavior-preserving structural work | characterization and regression tests | mixed rewrite/refactor without split |
| Skill creation | new reusable AI procedure | recurrence and ownership gap | existing skill already owns it |
| Skill improvement | existing AI procedure changes | evidence and replay | scope expansion without factory review |
| Release | version/publication | completed plans, validation, rollback | unresolved applicable P1/P2 |
| Framework upgrade | FCVW baseline change | ownership map, migration, clean validation | project history overwrite risk |

Outcomes are `pass`, `warn`, or `block`. A bypass records authority, justification, expiry, residual risk, and follow-up. Silence is not a pass.


The Regression gate is evaluated before plan completion. See `REGRESSION_GUARDS.md` for bypass requirements and confirmed-regression handling.

### Additional cross-cutting gates

| Gate | Trigger | Minimum evidence | Blocking condition |
|---|---|---|---|
| Proportionality | new dependency, abstraction, wrapper, module, service, layer, or material file | need, reuse search, native capability, installed dependency, new-code justification | no current need, avoidable duplication, speculative scope, or mandatory safeguard removed |
| Document graph | governed Markdown added, moved, renamed, removed, or generated | incoming link, authoritative outgoing relationship for records, entrypoint reachability, regenerated catalog | orphan, unreachable artifact, broken/ambiguous link, or record without source |
| Plan queue | plan created or changes active state | status equals directory; valid `category`, specific external blocker and override reasons | invalid category, vague blocker, misplaced `before_in_progress` |

The Proportionality gate is advisory when evidence is adequate. It may not bypass security, privacy, accessibility, compliance, audit, data-integrity, documentation, or risk-proportional testing requirements.
