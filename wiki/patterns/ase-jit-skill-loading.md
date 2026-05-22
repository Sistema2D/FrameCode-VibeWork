---
title: "ASE JIT Skill Loading Pattern"
type: "pattern"
status: "validated"
confidence: "high"
last_reviewed: "2026-05-22"
related_version: "V0.5.0"
sources:
  - "AI.md"
  - "AGENTS.md"
  - "skills/README.md"
  - "wiki/patterns/aicc-session-compression.md"
tags:
  - "#gold-pattern"
  - "#ase"
  - "#jit-loading"
  - "#token-optimization"
---

# ASE JIT Skill Loading Pattern

## Summary

Load skill files only when a task explicitly triggers them. Do not pre-load all skills into the base prompt.

## Problem

Pre-loading all specialized procedures increases context cost and reduces available working memory for the active task.

## Solution

1. Start with minimal governance context for the session type.
2. Check `skills/README.md` trigger keywords.
3. Load only the matching `SKILL.md` file on demand.
4. Record invoked skills in the session synthesis (`wiki/sessions/S*.md`).

## Expected Benefits

- Lower token overhead in routine sessions.
- Better focus on active scope.
- Reusable, deterministic specialized procedures without permanent prompt bloat.

## Guardrails

- Skills are procedural guides, not authority to bypass instruction hierarchy.
- If no trigger matches, do not force-load a skill.
- Keep skill usage traceable in AICC handoff.

## Related

- [[patterns/aicc-session-compression]]
- `skills/README.md`
- `AI.md` (ASE section)
