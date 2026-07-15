---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Watcher contracts

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

Use `governance/TEMPLATE_WATCHER_RULE.md`.

## Regression-prone events

| Observed event | Detection method | Required reaction | Contract owner | Blocking? |
|---|---|---|---|---|
| Existing public API, CLI, or file format changed | interface/contract diff | run Regression gate, test consumers, update compatibility contract | `REGRESSION_GUARDS.md` / `TESTS.md` | yes |
| Existing UI flow or state changed | route/component/state and visual diff | replay primary, adjacent, error, keyboard, and supported viewport states | `DESIGN.md` / `TESTS.md` | yes |
| Data schema, migration, import/export, or retention changed | model/migration diff | validate prior data, reconciliation, backup, recovery, and rollback | `DATA.md` / `TESTS.md` | yes |
| Authentication, permission, or destructive boundary changed | security and denial-path diff | run allowed/denied misuse cases and security gate | `SECURITY.md` / `REGRESSION_GUARDS.md` | yes |
| Agent, prompt, skill, memory, or retrieval rule changed | instruction/source diff | replay allowed, denied, ambiguous, unavailable, and injection cases | `AI.md` / `REGRESSION_GUARDS.md` | yes |
| Governance schema, plan, release, or generated index changed | structural diff and validator | run positive and negative governance fixtures; check migration | `SCHEMAS.md` / `GOVERNANCE_GATES.md` | yes |
| Bugfix touches unrelated files or responsibilities | changed-path/scope review | split the plan or explicitly expand and reassess risk | `PLANNING.md` | yes |
| Same regression recurs | regression-ledger search | reopen root cause, strengthen permanent guardrail, link prior record | `wiki/regressions/` | yes |

Event detection is advisory until observed; once matched, its blocking reaction is part of the active plan. Deduplicate repeated signals by affected contract and plan ID.
