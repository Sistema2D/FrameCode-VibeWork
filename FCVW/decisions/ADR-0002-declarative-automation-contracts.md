# ADR-0002 — Declarative Automation Contracts over Executable Automation

## Status

`accepted`

## Date

2026-06-23

## Context

ADR-0001 established that FrameCode VibeWork must remain a pure Markdown governance framework without local automation scripts, package dependencies, installed hooks, or runtime requirements.

However, recurring governance risks still need clearer operational handling: filesystem drift, forgotten changelog fragments, plan-state mismatch, wiki frontmatter gaps, broken internal links, unsafe interpretation of AI tool actions, and inconsistent maintenance loops.

The project therefore needs automation semantics without executable automation.

## Decision

Define hooks, watchers, daemons, maintenance loops, and governance gates as Markdown-only declarative automation contracts.

In Scenario 1, these contracts are executed manually by humans or agentically by AI tools that read and follow Markdown. They are not scripts, services, installed Git hooks, background processes, package-managed tools, or CI/CD workflows.

## Allowed in Scenario 1

- Markdown pseudo-hook checklists.
- Markdown watcher rules.
- Markdown daemon loop protocols.
- Markdown governance gate matrices.
- Markdown templates for future automation contracts.
- Manual or AI-driven inspection using official FCVW documents.
- Evidence recorded in plans, changelogs, audits, wiki logs, or troubleshooting records.

## Forbidden in Scenario 1

- Executable scripts.
- Installed Git hooks.
- Local background daemons.
- File-system watchers implemented with code.
- CI/CD workflows.
- Package manifests or dependency installation.
- API-key integrations or provider SDKs.
- Any automation that bypasses `AGENTS.md`, `PLANNING.md`, `SECURITY.md`, `AI.md`, or ADR-0001.

## SantanderAI Inspiration Credit

This ADR is inspired by architectural patterns observed in the public SantanderAI organization at `https://github.com/SantanderAI`, especially:

- agent-loop and stop-signal concepts from `SantanderAI/ralph`;
- vault/lint and progressive-disclosure knowledge maintenance ideas from `SantanderAI/ralph-vault-skill`;
- hard-gate governance concepts from `SantanderAI/mech-gov-framework`;
- guardrail evaluation thinking from `SantanderAI/autoguardrails`.

No SantanderAI source code is copied into FCVW. The influence is conceptual and architectural only.

## Consequences

### Positive

- The framework gains repeatable operational semantics without losing portability.
- Agents get clearer maintenance triggers and stop conditions.
- Governance drift can be detected earlier by humans or AI agents.
- Future CLI evolution remains possible without contaminating the Scenario 1 baseline.

### Negative

- Enforcement is still manual/agentic, not deterministic.
- Agents may still miss checks unless `AGENTS.md` and `CONTEXT_MAP.md` route them correctly.
- The new documents add governance surface area that must stay synchronized with `FILESYSTEM.md`, skills, and templates.

## Relationship with ADR-0001

ADR-0002 does not replace ADR-0001. It clarifies that automation-related vocabulary may exist in FCVW only when the artifact remains Markdown-only and non-executable.

If a future plan introduces real scripts, hooks, daemons, watchers, local services, or provider integrations, that work belongs to Scenario 2 and requires a separate architecture decision.
