# Declarative Automation

## Objective

Define how FrameCode VibeWork represents automation without introducing executable automation in the Scenario 1 baseline.

This document is the parent contract for `HOOKS.md`, `WATCHERS.md`, `DAEMONS.md`, and `GOVERNANCE_GATES.md`.

## Definition

In Scenario 1, automation means repeatable Markdown procedures executed by humans or AI agents that read and follow the repository governance documents.

Automation contracts are operational descriptions. They do not execute by themselves.

## Non-Goals

The Scenario 1 baseline must not introduce:

- executable scripts;
- installed Git hooks;
- local daemons;
- file-system watchers implemented with code;
- CI/CD workflows;
- package manifests;
- runtime dependencies;
- API-key integrations;
- provider SDKs;
- command execution permissions.

## Automation Contract Types

| Type | Document | Purpose |
|---|---|---|
| Pseudo-hooks | `HOOKS.md` | Checklists evaluated before or after repository operations. |
| Watcher rules | `WATCHERS.md` | Event/reaction rules for changes that require governance attention. |
| Daemon loops | `DAEMONS.md` | Repeatable manual/agentic maintenance loops. |
| Governance gates | `GOVERNANCE_GATES.md` | Central mapping of trigger, evidence, blocking condition, and owner document. |

## Execution Rule

Automation contracts are evaluated manually or agentically. A human or AI agent may read a contract, apply its checklist, and record evidence, but must not install or execute hidden automation under Scenario 1.

## Precedence

Declarative automation contracts are subordinate to:

1. System and execution environment rules.
2. `AGENTS.md`.
3. `PLANNING.md`.
4. `SECURITY.md`.
5. `AI.md`.
6. ADR-0001 and ADR-0002.

If an automation contract appears to conflict with a higher rule, stop and report the conflict before proceeding.

## Evidence Rule

Any contract that blocks, warns, or validates a change must leave evidence in the active plan, changelog, audit record, wiki log, troubleshooting record, or PR description.

## SantanderAI Inspiration Credit

The declarative automation layer is conceptually inspired by public SantanderAI repositories at `https://github.com/SantanderAI`, especially the agent-loop, stop-signal, vault-lint, hard-gate, and guardrail patterns observed in `ralph`, `ralph-vault-skill`, `mech-gov-framework`, and `autoguardrails`.

No SantanderAI code is copied. The influence is limited to architectural ideas adapted into Markdown-only FCVW governance contracts.

## Scenario 2 Boundary

If a future plan requires real hooks, watchers, scripts, daemons, API keys, or CLI execution, it must be treated as Scenario 2 and must not be implemented inside the pure Markdown baseline without a new architecture decision.
