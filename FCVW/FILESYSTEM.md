---
title: "Project Filesystem Architecture"
type: "concept"
status: "validated"
confidence: "high"
last_reviewed: "2026-05-29"
related_version: "V0.7.5"
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
|-- .cursorrules
|-- .github/
|-- .gitignore
|-- .windsurfrules
|-- AGENTS.md
\-- FCVW/
    |-- AI.md
    |-- ARCHITECTURAL_DECISIONS.md
    |-- AUDIT.md
    |-- audits
    |   |-- README.md
    |   \-- 2026-05-29-framework-structure-audit.md
    |-- BRIEFING.md
    |-- briefings
    |   \-- README.md
    |-- CONTEXT_MAP.md
    |-- changelogs
    |   |-- V0.7.0.md
    |   |-- V0.7.1.md
    |   |-- V0.7.2.md
    |   |-- V0.7.3.md
    |   |-- V0.7.4.md
    |   |-- V0.7.5.md
    |   \-- unreleased/
    |       |-- README.md
    |       |-- P2-R2-2026-05-29-governance-state-reconciliation.md
    |       |-- P2-R3-2026-05-29-root-and-snippets-deprecation.md
    |       |-- P3-R2-2026-05-29-audit-follow-up-cleanup.md
    |       |-- P4-R1-2026-05-29-readme-flowchart-alignment.md
    |       \-- P4-R1-2026-05-29-readme-scope-wording-corrections.md
    |-- DATA.md
    |-- decisions
    |   \-- ADR-0001-pure-markdown-over-automation-scripts.md
    |-- DESIGN.md
    |-- docs
    |   \-- index.html
    |-- ENVIRONMENT.md
    |-- FILESYSTEM.md
    |-- governance
    |   |-- README_FRAMEWORK.md
    |   |-- TEMPLATE_ADR.md
    |   |-- TEMPLATE_API_SPEC.md
    |   |-- TEMPLATE_AI_RESOURCE.md
    |   |-- TEMPLATE_AI_SESSION_SYNTHESIS.md
    |   |-- TEMPLATE_BRIEFING.md
    |   |-- TEMPLATE_DATA_SCHEMA.md
    |   |-- TEMPLATE_ENV.md
    |   |-- TEMPLATE_MIGRATION_RUNNER.md
    |   |-- TEMPLATE_PLAN.md
    |   |-- TEMPLATE_REFACTORING.md
    |   |-- TEMPLATE_RELEASE.md
    |   |-- TEMPLATE_TROUBLESHOOTING.md
    |   \-- TEMPLATE_VISUAL_DIFF.md
    |-- INSTANTIATION.md
    |-- LICENSE
    |-- MANIFEST.md
    |-- PERFORMANCE.md
    |-- PLANNING.md
    |-- Plans
    |   |-- completed
    |   |   |-- P2-R2-2026-05-29-governance-state-reconciliation.md
    |   |   |-- P2-R3-2026-05-29-root-and-snippets-deprecation.md
    |   |   |-- P3-R2-2026-05-29-audit-follow-up-cleanup.md
    |   |   |-- P4-R1-2026-05-29-readme-flowchart-alignment.md
    |   |   \-- P4-R1-2026-05-29-readme-scope-wording-corrections.md
    |   |-- discontinued
    |   |-- in_progress
    |   \-- pending
    |-- README.md (Framework README)
    |-- REFACTORING.md
    |-- RELEASE.md
    |-- repository-open-graph-template.png
    |-- SCOPE.md
    |-- SECURITY.md
    |-- skills
    |   |-- README.md
    |   |-- agent-aegis
    |   |   \-- SKILL.md
    |   |-- agent-hephaestus
    |   |   \-- SKILL.md
    |   |-- agent-hermes
    |   |   \-- SKILL.md
    |   |-- agnix-linter
    |   |   \-- SKILL.md
    |   |-- aicc-compact
    |   |   \-- SKILL.md
    |   |-- brainstorming-and-tdd
    |   |   \-- SKILL.md
    |   |-- git-conventional-commits
    |   |   \-- SKILL.md
    |   |-- memory-rotation
    |   |   \-- SKILL.md
    |   |-- obsidian-markdown
    |   |   \-- SKILL.md
    |   |-- orchestrator
    |   |   \-- SKILL.md
    |   |-- project-instantiation
    |   |   \-- SKILL.md
    |   |-- release-checklist
    |   |   \-- SKILL.md
    |   |-- systematic-debugging
    |   |   \-- SKILL.md
    |   \-- wiki-lint
    |       \-- SKILL.md
    |-- STACK.md
    |-- TESTS.md
    |-- troubleshooting
    |   |-- README.md
    |   \-- 2026-05-29-governance-state-drift.md
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
    |   |   |-- S001-2026-05-29-readme-flowchart-alignment.md
    |   |   |-- S002-2026-05-29-governance-state-reconciliation.md
    |   |   |-- S003-2026-05-29-root-and-snippets-deprecation.md
    |   |   |-- S004-2026-05-29-audit-follow-up-cleanup.md
    |   |   \-- S005-2026-05-29-readme-scope-wording-corrections.md
    |   |-- sources
    |   |   \-- README.md
    |   \-- templates
    |       |-- README.md
    |       |-- TEMPLATE_DECISION.md
    |       |-- TEMPLATE_FAILURE.md
    |       |-- TEMPLATE_GENERAL_NOTE.md
    |       |-- TEMPLATE_LINT.md
    |       |-- TEMPLATE_PATTERN.md
    |       |-- TEMPLATE_QUESTION.md
    |       |-- TEMPLATE_RELEASE_SYNTHESIS.md
    |       |-- TEMPLATE_SESSION_SYNTHESIS.md
    |       \-- TEMPLATE_TECH_DEBT.md
    \-- WORKFLOW.md
```
<!-- END_TREE -->

---

## 2. Directory and File Roles

| Path | Primary Role | Stakeholders / Sources | Git Ignored? |
|---|---|---|---|
| `/FCVW/Plans/` | Contains chronological implementation change plans. | [PLANNING.md](PLANNING.md) | No |
| `/FCVW/audits/` | Stores formal audit records and pre-release review evidence. | [AUDIT.md](AUDIT.md) | No |
| `/FCVW/briefings/` | Stores Phase 0 discovery and instantiation records. | [BRIEFING.md](BRIEFING.md) / [INSTANTIATION.md](INSTANTIATION.md) | No |
| `/FCVW/decisions/` | Stores formal Architectural Decision Records (ADRs). | [ARCHITECTURAL_DECISIONS.md](ARCHITECTURAL_DECISIONS.md) | No |
| `/FCVW/changelogs/` | Formal version release notes and unreleased plan fragments. | [VERSIONING.md](VERSIONING.md) | No |
| `/FCVW/governance/` | Reusable empty blueprint templates. | [INSTANTIATION.md](INSTANTIATION.md) | No |
| `/FCVW/troubleshooting/` | Stores issue records, hypotheses, handlings, and validation evidence. | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | No |
| `/FCVW/wiki/` | Continuous technical learning vault of the project. | [AI.md](AI.md) / `wiki/schema.md` | No |
| `/FCVW/data/` | Stores local SQLite database and backups. | [DATA.md](DATA.md) | **Yes** (strict) |

---

## 3. Maintenance and Self-Healing Rules

1. **AI Checkpoints:** Whenever a new feature is requested, the AI must check `FILESYSTEM.md` before writing code to confirm where the new files belong.
2. **Declarative Layout Integrity:** The detailed visual tree in `FILESYSTEM.md` must be updated manually by the agent whenever files are added or deleted. Summary documents should link to this file instead of duplicating the full tree.
3. **Audit Closure:** The final step of any plan that alters directories is a manual verification of this document's visual tree.
