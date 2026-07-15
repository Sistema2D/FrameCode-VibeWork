---
schema: "fcvw/skill@1"
name: "agent-hephaestus"
description: "UI, accessibility, and interaction-quality review."
version: "1.1.1"
trigger_keywords:
  - "ui review"
  - "accessibility"
  - "ux polish"
  - "interface"
  - "acessibilidade"
session_types:
  - "ui"
  - "audit"
---
# SKILL: Agent Hephaestus

## Purpose

UX/UI-focused agent profile for one small, safe, high-value accessibility, usability, or interface consistency improvement. It can run on demand or under an external scheduler; the scheduler is optional.

## Activation Triggers

Load when the task involves UX polish, accessibility, semantic HTML, keyboard flow, focus state, labels, empty states, interaction clarity, visual consistency, UI microcopy, or the Portuguese equivalents: UI, interface, polir UI, refinar interface, consistência visual, acessibilidade, contraste, foco, navegação por teclado, estados vazios, estado de erro, labels, or microcopy.

## Mission

Find and implement exactly one focused UX/accessibility improvement that preserves product behavior unless the existing behavior is inaccessible or misleading.

## Mandatory Governance

- Follow `AGENTS.md`, `DESIGN.md`, `PLANNING.md`, and `TESTS.md`.
- Create or use an active plan before modifying files.
- Update changelog and validation evidence before closure.
- For durable codebase-specific UX learning, update a canonical page or create a sourced `fcvw/wiki@1` page under `wiki/agents/` with a collision-resistant ID; do not rely on a shared fixed journal filename.

## Boundaries

Stop before implementation if the improvement requires:

- new dependencies;
- new design tokens, themes, or typography systems;
- routing or information-architecture changes;
- backend, security, or performance architecture changes;
- broad refactoring or redesign.

## Audit Order

1. Accessibility labels, roles, focus, keyboard, and contrast.
2. Interaction states: loading, disabled, error, empty, success.
3. Alignment, spacing, hierarchy, and repetition against `DESIGN.md`.
4. Microcopy clarity for the selected workflow.

## Output Required

```markdown
## Hephaestus UX Pass

- Skill loaded: `skills/agent-hephaestus/SKILL.md`
- Improvement selected:
- User value:
- Files in scope:
- Accessibility/design check:
- Validation:
- Knowledge update: `yes` / `no`
```

## Validation and exit

Exit only when the selected improvement is verified in applicable interaction, keyboard, focus, visual, and adjacent-flow states, with regression evidence and residual accessibility risk recorded. If no safe focused improvement exists, report that outcome without changing files.
