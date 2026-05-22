---
title: "ADR-0001: Pure Markdown Over Automation Scripts"
type: "decision"
status: "validated"
confidence: "high"
last_reviewed: "2026-05-22"
related_version: "V0.4.0"
sources:
  - "decisions/ADR-0001-pure-markdown-over-automation-scripts.md"
  - "changelogs/V0.4.0.md"
  - "wiki/sessions/S006-2026-05-18-discontinue-mockups-and-automation-scripts.md"
tags:
  - "#arch-decision"
  - "#adr-0001"
  - "#pure-markdown"
---

# ADR-0001: Pure Markdown Over Automation Scripts

## Decision

Adopt a **Pure Markdown Instruction Model** for the FrameCode VibeWork framework. Deprecate all automation scripts (`sync-filesystem.ps1`) and visual mockup directories (`mockups/`).

## Context

As of V0.3.x, the framework included PowerShell automation scripts for filesystem synchronization and a `mockups/` directory for visual calibration. These introduced:
- Cross-platform permission issues (Windows script execution policies)
- Additional dependency surface (runtime environments)
- Maintenance overhead for scripts that became misaligned with actual workflow

## Decision Rationale

Modern LLM agents (Gemini, Claude, GPT-4 class) can execute text-based validation lists and layout description reviews with high accuracy. Converting these operations to declarative Markdown instructions:

1. **Eliminates platform dependencies** — works identically on Windows, macOS, Linux, and cloud sandboxes
2. **Removes permission blockers** — no script execution policies to configure
3. **Reduces maintenance surface** — Markdown documents are self-validating via agent review
4. **Leverages LLM strengths** — agents excel at reading and applying prose-format checklists

## Consequence

- `mockups/` directory permanently removed (V0.4.0)
- `governance/scripts/sync-filesystem.ps1` permanently removed (V0.4.0)
- `DESIGN.md` expanded to absorb visual calibration rules natively
- `FILESYSTEM.md` expanded to serve as declarative layout ledger
- Future tooling should follow the same pattern: prefer SKILL.md files over scripts

## Status

`accepted` — enforced from V0.4.0 onward

## Exceptions

None. If automation is needed in a downstream project, it must be explicitly documented as a project-level deviation from this ADR, not added to the framework itself.

## Related

- [[decisions/adr-0001-pure-markdown]] → this page
- `decisions/ADR-0001-pure-markdown-over-automation-scripts.md` — original ADR record
- [[patterns/aicc-session-compression]] — AICC pattern enabled by this pivot
