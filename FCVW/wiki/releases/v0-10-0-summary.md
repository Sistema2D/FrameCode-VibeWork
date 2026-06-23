---
title: "Release Synthesis V0.10.0 — Agent Factory and Self‑Improvement"
type: "release"
status: "validated"
confidence: "high"
last_reviewed: "2026-06-13"
related_version: "V0.10.0"
sources:
  - "changelogs/V0.10.0.md"
  - "wiki/sessions/S003-2026-06-13-agent-self-improvement-template-site.md"
tags:
  - "release"
  - "V0.10.0"
  - "agent-factory"
  - "self-improvement"
  - "clean-template"
---

# Release Synthesis V0.10.0 — Agent Factory and Self‑Improvement

## Version Summary

This minor release introduces controlled creation and self‑improvement of skills and agent profiles, repairs AI‑usability issues in templates, generates a clean Markdown‑only project baseline, and refreshes the public static site to align with the current framework.

## Main Changes

1. **Agent Factory and Self‑Improvement Skills** — Added `agent-factory` and `self-improvement` skills, along with proposal and report templates, enabling measurable creation and evidence‑based refinement of skills and agents.

2. **Template and Catalog Updates** — Updated governance templates (`TEMPLATE_AGENT_OR_SKILL_PROPOSAL.md`, `TEMPLATE_SELF_IMPROVEMENT_REPORT.md`) and the skill catalog to reflect new rules; updated `AGENTS.md`, `AI.md`, `PLANNING.md`, `AUDIT.md`, `TESTS.md`, `CONTEXT_MAP.md`, `STACK.md`, `MANIFEST.md`, `VERSIONING.md`, and `skills/README.md`.

3. **Clean Template and Static Site Refresh** — Generated a clean Markdown‑only baseline under `Template limpo/` that excludes development history; rebuilt the static site under `Página web/` to reflect version V0.10.0 and the new governance features.

## Patterns and Learnings

- Governed creation and improvement cycles allow the framework to evolve sustainably without uncontrolled sprawl.
- Separation of the canonical FCVW tree from the public static site preserves governance integrity: edits must occur under `FCVW/`, and the site is a mirror only.

## Known Gaps

Browser‑level visual verification of the static site may require serving `Página web/` over HTTP because direct `file://` rendering can be blocked. No runtime code changes were included.
