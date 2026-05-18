---
title: "Project Filesystem Architecture"
type: "concept"
status: "validated"
confidence: "high"
last_reviewed: "2026-05-17"
related_version: "V0.0.2"
sources:
  - "STACK.md"
  - "SCOPE.md"
  - "DESIGN.md"
  - "DATA.md"
tags:
  - "filesystem"
  - "architecture"
---

# Project Filesystem Architecture

This document defines the physical directory structure of the application. It serves as the single source of truth for the file organization, ensuring absolute consistency between design rules, stack requirements, and physical implementation.

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
|-- DESIGN.md
|-- FILESYSTEM.md
|-- governance
|   |-- README_FRAMEWORK.md
|   |-- scripts
|   |   \-- sync-filesystem.ps1
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
|-- mockups
|   |-- actual
|   |   \-- .gitkeep
|   |-- design
|   |   \-- .gitkeep
|   |-- diffs
|   |   \-- .gitkeep
|   \-- README.md
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
|   |   \-- P5-R1-2026-05-15-add-star-history.md
|   |-- in_progress
|   |   \-- P1-R2-2026-05-17-repo-internationalization.md
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
|   |   \-- S004-2026-05-18-align-readme-directory-trees.md
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
| `/Plans/` | Contains chronological implementation change plans. | [PLANNING.md](file:///c:/Users/Hugo/Desktop/FCVW/PLANNING.md) | No |
| `/changelogs/` | Formal versions releases notes (`Vx.y.z.md`). | [VERSIONING.md](file:///c:/Users/Hugo/Desktop/FCVW/VERSIONING.md) | No |
| `/governance/` | Reusable empty blueprints and automation scripts. | [INSTANTIATION.md](file:///c:/Users/Hugo/Desktop/FCVW/INSTANTIATION.md) | No |
| `/snippets/` | Shared catalog of premade CSS/JS UI snippets. | [DESIGN.md](file:///c:/Users/Hugo/Desktop/FCVW/DESIGN.md) | No |
| `/wiki/` | Continuous technical learning vault of the project. | [AI.md](file:///c:/Users/Hugo/Desktop/FCVW/AI.md) / `wiki/schema.md` | No |
| `/data/` | Stores local SQLite database and backups. | [DATA.md](file:///c:/Users/Hugo/Desktop/FCVW/DATA.md) | **Yes** (strict) |

---

## 3. Automation Bootstrap Script

*Use the following PowerShell script to instantly generate this directory layout on a fresh instantiation:*

```powershell
# Create standard folders
New-Item -ItemType Directory -Force -Path "data", "public/assets", "src/components/common", "src/services", "src/styles", "src/utils", "tests"

# Create core files
New-Item -ItemType File -Force -Path "src/styles/tokens.css", "src/App.jsx", "src/main.jsx"
```

---

## 4. Maintenance and Self-Healing Rules

1. **AI Checkpoints:** Whenever a new feature is requested, the AI must check `FILESYSTEM.md` before writing code to confirm where the new files belong.
2. **Auto-Check:** During initialization or wiki lints, the AI will execute the tree synchronization script located in `governance/scripts/sync-filesystem.ps1` to keep this document dynamically in sync with the physical filesystem.
3. **Definition of Done:** Every plan that introduces or removes folders must run the synchronization script before closure.
