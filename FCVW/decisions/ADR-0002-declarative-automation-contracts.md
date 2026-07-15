---
schema: "fcvw/adr@1"
id: "ADR-0002"
status: "accepted"
date: "2026-07-15"
artifact_role: "record"
record_scope: "framework"
---

# ADR-0002: Declarative automation contracts

## Context

Hooks, watchers, daemons, and gates are useful governance concepts, but their execution differs across local tools, CI providers, operating systems, and hosted services. Treating one implementation as universal would couple policy to infrastructure.

## Decision

Scenario 1 defines automation as Markdown-only `fcvw/automation@1` contracts. Scenario 2 may use optional local adapters, and Scenario 3 may use external orchestration. Every adapter must preserve the declared trigger, preconditions, actions, evidence, failure policy, and rollback.

## Consequences

- A contract can be reviewed before any executable adapter exists.
- Runtime implementations are replaceable and provider-specific.
- “Automated” may not be claimed unless execution evidence exists.
- Failure behavior and rollback are part of the policy, not hidden inside a script.

## Supersession

Changes to the contract schema follow `SCHEMAS.md` and require migration guidance when compatibility breaks.
