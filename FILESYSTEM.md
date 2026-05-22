---
title: "Project Filesystem Architecture"
type: "concept"
status: "validated"
confidence: "high"
last_reviewed: "2026-05-18"
related_version: "V0.4.0"
sources:
  - "STACK.md"
  - "SCOPE.md"
  - "DESIGN.md"
  - "decisions/ADR-0001-pure-markdown-over-automation-scripts.md"
tags:
  - "filesystem"
  - "architecture"
---

# Project Filesystem Architecture

This document defines the physical directory structure of the application. It serves as the single source of truth for the file organization, ensuring absolute consistency between design rules, stack requirements, and physical implementation.

In accordance with [ADR-0001](decisions/ADR-0001-pure-markdown-over-automation-scripts.md), this directory layout is maintained purely declaratively in Markdown and verified manually by agents, eliminating dependencies on local environment scripts.

---

## 1. Visual Application Tree

<!-- START_TREE -->
```text
[project-root]/
|-- .gitignore
|-- AGENTS.md
|-- AI.md
|-- ARCHITECTURAL_DECISIONS.md
|-- AUDIT.md
|-- BRIEFING.md
|-- changelogs
|   |-- V0.0.0.md
|   |-- V0.0.1.md
|   |-- V0.1.0.md
|   |-- V0.1.1.md
|   |-- V0.1.2.md
|   |-- V0.1.3.md
|   |-- V0.2.0.md
|   |-- V0.2.1.md
|   |-- V0.3.0.md
|   \-- V0.3.1.md
|-- DATA.md
|-- decisions
|   \-- ADR-0001-pure-markdown-over-automation-scripts.md
|-- DESIGN.md
|-- FILESYSTEM.md
|-- governance
|   |-- README_FRAMEWORK.md
|   |-- TEMPLATE_ADR.md
|   |-- TEMPLATE_AI_RESOURCE.md
|   |-- TEMPLATE_AI_SESSION_SYNTHESIS.md
|   |-- TEMPLATE_BRIEFING.md
|   |-- TEMPLATE_DATA_SCHEMA.md
|   |-- TEMPLATE_PLAN.md
|   |-- TEMPLATE_REFACTORING.md
|   |-- TEMPLATE_RELEASE.md
|   \-- TEMPLATE_VISUAL_DIFF.md
|-- INSTANTIATION.md
|-- LICENSE
|-- MANIFEST.md
|-- PLANNING.md
|-- Plans
|   |-- completed
|   |   |-- 20260515-sync-readme.md
|   |   |-- P2-R1-2026-05-17-filesystem-implementation.md
|   |   |-- P3-R1-2026-05-17-mockups-system-implementation.md
|   |   |-- P3-R1-2026-05-18-token-estimations-readme-integration.md
|   |   |-- P3-R1-2026-05-18-update-readme-directory-trees.md
|   |   |-- P3-R2-2026-05-18-ai-context-compression-implementation.md
|   |   |-- P3-R2-2026-05-18-skills-engine-and-obsidian-markdown-integration.md
|   |   |-- P4-R1-2026-05-17-database-schemas-and-token-optimization.md
|   |   \-- P5-R1-2025-05-15-add-star-history.md
|   |-- in_progress
|   |   \-- P4-R2-2026-05-18-discontinue-mockups-and-automation-scripts.md
|   \-- pending
|-- README.md
|-- REFACTORING.md
|-- RELEASE.md
|-- SCOPE.md
|-- SECURITY.md
|-- skills
|   |-- obsidian-markdown
|   |   \-- SKILL.md
|   \-- README.md
|-- snippets
|   |-- gallery.html
|   |-- README.md
|   |-- tokens.css
|   \-- ui
|       |-- backgrounds
|       |   \-- background-dark.md
|       |-- buttons
|       |   \-- button-primary.md
|       |-- cards
|       |   \-- card-glass.md
|       \-- modals
|           \-- modal-confirmation.md
|-- STACK.md
|-- TESTS.md
|-- TROUBLESHOOTING.md
|-- VERSIONING.md
|-- wiki
|   |-- components
|   |   \-- README.md
|   |-- concepts
|   |   \-- README.md
|   |-- inbox
|   |   \-- README.md
|   |-- index.md
|   |-- log.md
|   |-- prompts
|   |   \-- README.md
|   |-- raw
|   |   \-- README.md
|   |-- README.md
|   |-- schema.md
|   |-- sessions
|   |   |-- README.md
|   |   |-- S001-2026-05-18-ai-context-compression-implementation.md
|   |   |-- S002-2026-05-18-integrate-token-estimations.md
|   |   |-- S003-2026-05-18-implement-skills-engine.md
|   |   |-- S004-2026-05-18-align-readme-directory-trees.md
|   |   \-- S005-framework-optimization-analysis.md
|   |-- sources
|   |   \-- README.md
|   |-- syntheses
|   |   \-- S005-framework-optimization-analysis.md
|   \-- templates
|       |-- README.md
|       |-- TEMPLATE_DECISION.md
|       |-- TEMPLATE_FAILURE.md
|       |-- TEMPLATE_GENERAL_NOTE.md
|       |-- TEMPLATE_LINT.md
|       |-- TEMPLATE_PATTERN.md
|       |-- TEMPLATE_QUESTION.md
|       |-- TEMPLATE_RELEASE_SYNTHESIS.md
|       \-- TEMPLATE_SESSION_SYNTHESIS.md
\-- WORKFLOW.md
```
<!-- END_TREE -->

---

## 2. Directory and File Roles

| Path | Primary Role | Stakeholders / Sources | Git Ignored? |
|---|---|---|---|
| `/Plans/` | Contains chronological implementation change plans. | [PLANNING.md](PLANNING.md) | No |
| `/decisions/` | Stores formal Architectural Decision Records (ADRs). | [ARCHITECTURAL_DECISIONS.md](ARCHITECTURAL_DECISIONS.md) | No |
| `/changelogs/` | Formal versions releases notes (`Vx.y.z.md`). | [VERSIONING.md](VERSIONING.md) | No |
| `/governance/` | Reusable empty blueprint templates. | [INSTANTIATION.md](INSTANTIATION.md) | No |
| `/snippets/` | Shared catalog of premade CSS/JS UI snippets. | [DESIGN.md](DESIGN.md) | No |
| `/wiki/` | Continuous technical learning vault of the project. | [AI.md](AI.md) / `wiki/schema.md` | No |
| `/data/` | Stores local SQLite database and backups. | [DATA.md](DATA.md) | **Yes** (strict) |

---

## 3. Maintenance and Self-Healing Rules

1. **AI Checkpoints:** Whenever a new feature is requested, the AI must check `FILESYSTEM.md` before writing code to confirm where the new files belong.
2. **Declarative Layout Integrity:** Visual trees in `FILESYSTEM.md` and `README.md` must be updated manually by the agent whenever files are added or deleted.
3. **Audit Closure:** The final step of any plan that alters directories is a manual verification of this document's visual tree.


