---
title: "Release Synthesis V0.9.0 — Governance Gap Closure"
type: "release"
status: "validated"
confidence: "high"
last_reviewed: "2026-06-11"
related_version: "V0.9.0"
sources:
  - "changelogs/V0.9.0.md"
  - "wiki/sessions/S001-2026-06-11-governance-gaps-closure.md"
tags:
  - "release"
  - "V0.9.0"
  - "governance"
  - "gap-closure"
  - "documentation"
---

# Release Synthesis V0.9.0 — Governance Gap Closure

## Version Summary

This release consolidates four governance gaps identified during hypothesis testing. It introduces mandatory service research, a documented PR/branch workflow, an environment promotion workflow, and a multi-agent concurrency protocol. All changes are documentation-only and adhere to ADR 0001 (pure Markdown). Version number progressed from V0.8.0 to V0.9.0.

## Main Changes

1. **Service Research Mandate** — Added third party service research rule and integration protocol to `AGENTS.md` and `FCVW/AI.md`, preventing agents from recommending services from training memory alone.

2. **PR/Branch and Code Review Workflow** — Added branch naming conventions, PR workflow steps, and review standards by risk level to `AGENTS.md` and updated `CONTEXT_MAP.md` to include pull request session types.

3. **Environment Promotion Workflow** — Added a table of environment roles and promotion gates in `ENVIRONMENT.md`, expanded release states in `RELEASE.md`, and linked deployment promotion to release processes.

4. **Multi Agent Concurrency Protocol** — Defined plan based signaling, coordination checks, journal usage, scope locking, conflict resolution, and branch isolation guidelines in `AGENTS.md` and added collaboration session type to `CONTEXT_MAP.md`.

## Patterns and Learnings

- **Gap Hypothesis → Plan → Implementation → Review → Completion** — Reinforced as the canonical pattern for closing governance gaps.
- **Stale File Convention** — Completed plans mark superseded copies to prevent confusion; future auditors should remove stale copies physically.
- **Soft Lock via Directory Convention** — Using `Plans/in_progress/` as a signal for active work.

## Known Gaps

Duplicate plan files remain on disk in `Plans/pending/` and `Plans/in_progress/` and unreleased changelog fragments remain under `changelogs/unreleased/`. These are marked superseded but still require physical cleanup.
