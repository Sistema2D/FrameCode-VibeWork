---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace_with_migration"
---

# Regression guardrails

## Principle

A change is not complete merely because its new behavior works. It must also demonstrate that relevant protected behavior was preserved, or record a specific validation limitation, residual risk, owner, and follow-up decision.

Regression evidence is change-specific. Running a large suite without identifying what it protects is weaker than a focused replay tied to an explicit contract.

## Applicability

Every `fcvw/plan@2` plan contains a Regression impact section. Use `regression_contract: required` when existing behavior, interfaces, data, permissions, visuals, governance, automation, or AI boundaries may change. Use `regression_contract: not_applicable` only with a concrete justification; “documentation only” is not sufficient when navigation, schemas, instructions, or generated outputs can drift.

Legacy `fcvw/plan@1` records remain valid historical evidence. A legacy plan substantively reopened under the current framework migrates to `fcvw/plan@2`.

## Regression classes

| Class | Protected behavior examples | Typical evidence |
|---|---|---|
| Functional/workflow | primary and alternate journeys, invalid input, recovery | focused automated test and workflow replay |
| Interface/API | public signatures, status codes, file formats, CLI contracts | contract test, compatibility diff, consumer replay |
| Data/filesystem | existing records, migration, import/export, paths, retention | representative old-data fixture, reconciliation, backup and rollback rehearsal |
| Visual/accessibility | layout, states, focus, keyboard flow, contrast | before/after capture, viewport/state matrix, accessibility check |
| Security/permission | denial paths, least privilege, secrets, destructive actions | negative authorization tests and misuse cases |
| AI/agent/memory | instruction hierarchy, allowed actions, retrieval sources, retention | boundary replay, adversarial prompt case, source and memory checks |
| Governance/documentation | links, schemas, ownership, lifecycle, version surfaces | structural validator, semantic cross-check, negative fixture |
| Performance/operations | latency, capacity, startup, deploy and recovery | measured baseline comparison and operational smoke test |

## Plan contract

Before implementation, record:

1. existing behaviors and consumers that may be affected;
2. source contracts consulted;
3. selected regression checks and why they are proportional;
4. baseline or pre-change evidence when comparison matters;
5. rollback and residual-risk handling.

Before completion, replace every pending result with `pass`, `fail`, `blocked`, or `not_applicable`, and attach reproducible evidence. A check marked `not_applicable` requires a reason.

## Minimum evidence by risk

`TESTS.md` owns the risk matrix. Risk is raised by blast radius, reversibility, security/data sensitivity, compatibility surface, and uncertainty—not by the apparent number of edited lines. Authentication, permissions, persistent data, public interfaces, agent rules, memory, filesystem, automation, migration, and release changes are never classified R1 without an explicit rationale.

## Regression gate

The Regression gate blocks completion when any applicable condition holds:

- Regression impact is absent, empty, generic, or still pending.
- Protected behavior changed without a contract update or compatibility decision.
- Evidence is below the plan's risk level or does not cover the identified blast radius.
- A failing or unavailable check has no limitation, residual risk, owner, and decision.
- A known regression is hidden, normalized as expected behavior, or omitted from history.
- Rollback is required but untested or no longer possible without explicit approval.
- The implementation touches unrelated boundaries without splitting or expanding the plan.

A bypass requires named authority, justification, expiry or review date, residual risk, and follow-up. Silence, a passing new-feature test, or “works on my machine” is not a pass.

## Confirmed regression lifecycle

When a regression is detected:

1. create or update a troubleshooting record when diagnosis is non-trivial;
2. create a `fcvw/regression@1` record under `wiki/regressions/` when the learning is reusable;
3. identify the missing or failed guardrail;
4. add or strengthen a replay check, policy, contract, or watcher;
5. link the plan and application or framework release record;
6. validate that the new guardrail fails on the regressed state and passes on the corrected state when practical.

Repeated recurrence of the same regression is a signal that the prior guardrail was ineffective; it must trigger stronger prevention rather than another duplicate note.

## Relationships

- `PLANNING.md` and `governance/TEMPLATE_PLAN.md` define the plan body and lifecycle.
- `TESTS.md` defines risk-proportional execution evidence.
- `GOVERNANCE_GATES.md` defines pass, warn, block, and bypass handling.
- `WATCHERS.md` maps observable drift to the Regression gate.
- `TROUBLESHOOTING.md` owns diagnosis evidence.
- `wiki/regressions/` preserves reusable recurrence-prevention knowledge.
- `AGENTS.md` prevents humans and agents from closing work on new behavior alone.
