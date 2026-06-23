---
title: "Release Synthesis V0.9.1 — Anti‑Monolith and Code Hygiene"
type: "release"
status: "validated"
confidence: "high"
last_reviewed: "2026-06-13"
related_version: "V0.9.1"
sources:
  - "changelogs/V0.9.1.md"
  - "wiki/sessions/S002-2026-06-13-anti-monolith-code-hygiene.md"
tags:
  - "release"
  - "V0.9.1"
  - "anti-monolith"
  - "code-hygiene"
  - "governance"
---

# Release Synthesis V0.9.1 — Anti‑Monolith and Code Hygiene

## Version Summary

This patch release makes the framework actively block AI‑generated monoliths and drive code hygiene and refactoring via Markdown‑only skills, templates, and gating rules. It builds on the retroactive instantiation workflow to triage duplication, stale files and dead code without altering legacy code.

## Main Changes

1. **Anti‑Monolith Guard** — Introduced the `anti-monolith-guard` skill and a template for monolith gates, requiring agents to pause before creating mixed‑responsibility modules and to document risk and size budgets.

2. **Code Hygiene and Refactoring Skill** — Added a `code-hygiene-refactor` skill and template to identify and plan elimination of duplication, stale files and dead code during retroactive instantiation.

3. **Updated Governance Documents and Skills** — Updated `AGENTS.md`, `AI.md`, `PLANNING.md`, `REFACTORING.md`, `RETROACTIVE_INSTANTIATION.md`, and `VERSIONING.md` to reference the new gates; updated existing agent profiles to be tool‑aware and environment‑aware; refreshed the skill catalog and context map.

## Patterns and Learnings

- Tools and templates deliver active governance without scripts, preserving ADR‑0001.
- Retroactive instantiation now includes a hygiene backlog creation step rather than silently modifying legacy code.
- Domain agents are environment‑aware and fallback to manual procedures when necessary.

## Known Gaps

No automated Markdown linter is included by design, and historical encoding artifacts in older documents remain unnormalized. Agents should run the anti‑monolith and hygiene gates when planning substantive changes.
