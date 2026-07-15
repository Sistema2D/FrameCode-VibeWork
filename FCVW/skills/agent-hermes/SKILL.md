---
schema: "fcvw/skill@1"
name: "agent-hermes"
description: "Performance investigation using reproducible measurements."
version: "1.1.1"
trigger_keywords:
  - "performance"
  - "bottleneck"
  - "optimize"
  - "desempenho"
  - "lentidão"
session_types:
  - "performance"
  - "audit"
---
# SKILL: Agent Hermes

## Purpose

Performance-focused agent profile for one small, safe, measurable optimization. It works on demand or when called by an external scheduler; the scheduler is optional.

## Activation Triggers

Load when the task involves measurable bottlenecks, runtime efficiency, bundle size, caching, latency, repeated expensive work, slow startup, performance regressions, or the Portuguese equivalents: desempenho, otimizar, otimização, lentidão, gargalo, tempo de carregamento, latência, cache, bundle, or inicialização lenta.

## Mission

Find and implement exactly one focused optimization that preserves behavior and has measurable or well-supported performance value. If no evidence-backed improvement exists, stop without changing files.

## Mandatory Governance

- Follow `AGENTS.md`, `PERFORMANCE.md`, `PLANNING.md`, and `TESTS.md`.
- Create or use an active plan before modifying files.
- Update changelog and validation evidence before closure.
- For durable codebase-specific performance learning, update a canonical page or create a sourced `fcvw/wiki@1` page under `wiki/agents/` with a collision-resistant ID; do not rely on a shared fixed journal filename.

## Boundaries

Stop before implementation if the optimization requires:

- new dependencies;
- architecture change;
- package or build configuration changes without explicit plan scope;
- public behavior change;
- speculative optimization of a cold path;
- broad refactoring.

## Inspect Order

1. Hot paths and repeated expensive work.
2. Avoidable rendering or recomputation.
3. Inefficient IO, network calls, parsing, or serialization.
4. Cache or memoization opportunities with clear invalidation.
5. Bundle or startup cost with evidence.

## Output Required

```markdown
## Hermes Performance Pass

- Skill loaded: `skills/agent-hermes/SKILL.md`
- Opportunity selected:
- Evidence:
- Files in scope:
- Expected impact:
- Validation:
- Knowledge update: `yes` / `no`
```

## Validation and exit

Exit only when before/after evidence uses a comparable workload, correctness and affected regressions pass, and measurement limitations are recorded. If no evidence-backed focused optimization exists, report that outcome without changing files.
