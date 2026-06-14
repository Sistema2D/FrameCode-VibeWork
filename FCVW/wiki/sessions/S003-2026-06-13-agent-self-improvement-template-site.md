---
title: "Agent Self-Improvement, Clean Template, and Site Refresh"
type: "synthesis"
status: "validated"
confidence: "high"
last_reviewed: "2026-06-13"
related_version: "V0.10.0"
tags:
  - "session-synthesis"
  - "agent-factory"
  - "self-improvement"
  - "clean-template"
skills_invoked:
  - "skills/agent-factory/SKILL.md"
  - "skills/self-improvement/SKILL.md"
  - "skills/governance-validator/SKILL.md"
---

# Agent Self-Improvement, Clean Template, and Site Refresh

## Context

User requested a full AI-usability audit of the framework, controlled creation of new skills and agents, self-improvement metrics for skills/agents, a clean template folder, and a web page aligned with the current framework.

## Changes

- Added `agent-factory` and `self-improvement` skills.
- Added proposal/report templates for new AI operational assets and their evidence-based improvement.
- Updated `AGENTS.md`, `AI.md`, `PLANNING.md`, `AUDIT.md`, `TESTS.md`, `CONTEXT_MAP.md`, `STACK.md`, `MANIFEST.md`, `VERSIONING.md`, and skill catalog references.
- Repaired visual-diff and placeholder-link templates that could confuse Markdown link validation.
- Generated a clean Markdown-only baseline under `Template limpo/`.
- Rebuilt the static site in `Página web/` to reflect `V0.10.0`.

## Next Agent Notes

- Do not create or modify skills/agents without the new gates.
- Keep `Template limpo/` free of development history and non-Markdown assets.
- Treat `Página web/` as a static documentation mirror, not the framework source of truth.
