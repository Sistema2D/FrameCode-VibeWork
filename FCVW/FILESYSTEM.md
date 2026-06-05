---
title: "Project Filesystem Architecture"
type: "concept"
status: "validated"
confidence: "high"
last_reviewed: "2026-06-05"
related_version: "V0.8.0"
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
|   \-- FUNDING.yml
|-- .gitignore
|-- .windsurfrules
|-- AGENTS.md
|-- README.md
\-- FCVW/
    |-- AI.md
    |-- APPLICATION_DOCUMENTATION.md
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
    |   |-- V0.7.6.md
    |   |-- V0.7.7.md
    |   |-- V0.7.8.md
    |   |-- V0.7.9.md
    |   |-- V0.8.0.md
    |   \-- unreleased/
    |       |-- README.md
    |       |-- P1-R2-2024-06-01-fix-xss-vulnerability.md
    |       |-- P2-R2-2026-05-29-governance-state-reconciliation.md
    |       |-- P2-R3-2026-05-29-root-and-snippets-deprecation.md
    |       |-- P3-R2-2026-05-29-audit-follow-up-cleanup.md
    |       |-- P4-R1-2026-05-29-readme-flowchart-alignment.md
    |       |-- P4-R1-2026-05-29-readme-scope-wording-corrections.md
    |       |-- translation-fallback-tests.md
    |       \-- V0.7.5.md
    |-- DATA.md
    |-- decisions
    |   \-- ADR-0001-pure-markdown-over-automation-scripts.md
    |-- DESIGN.md
    |-- ENVIRONMENT.md
    |-- FILESYSTEM.md
    |-- governance
    |   |-- README_FRAMEWORK.md
    |   |-- TEMPLATE_ADR.md
    |   |-- TEMPLATE_APP_DOCS_README.md
    |   |-- TEMPLATE_API_SPEC.md
    |   |-- TEMPLATE_AI_RESOURCE.md
    |   |-- TEMPLATE_AI_SESSION_SYNTHESIS.md
    |   |-- TEMPLATE_BRIEFING.md
    |   |-- TEMPLATE_DATA_SCHEMA.md
    |   |-- TEMPLATE_ENV.md
    |   |-- TEMPLATE_MIGRATION_RUNNER.md
    |   |-- TEMPLATE_MODULE_DOCUMENTATION.md
    |   |-- TEMPLATE_PLAN.md
    |   |-- TEMPLATE_REFACTORING.md
    |   |-- TEMPLATE_REFACTORING_ADR.md
    |   |-- TEMPLATE_REFACTORING_CHARACTERIZATION_TEST_PLAN.md
    |   |-- TEMPLATE_REFACTORING_DEPENDENCY_MAP.md
    |   |-- TEMPLATE_REFACTORING_INCREMENTAL_PLAN.md
    |   |-- TEMPLATE_REFACTORING_MODULE_INVENTORY.md
    |   |-- TEMPLATE_REFACTORING_OPENING.md
    |   |-- TEMPLATE_REFACTORING_POST_VALIDATION_REPORT.md
    |   |-- TEMPLATE_REFACTORING_PULL_REQUEST.md
    |   |-- TEMPLATE_REFACTORING_RISK_MATRIX.md
    |   |-- TEMPLATE_REFACTORING_ROLLBACK_PLAN.md
    |   |-- TEMPLATE_FLOW_DOCUMENTATION.md
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
    |   |   |-- add_language_detection_tests.md
    |   |   |-- P1-R2-2024-06-01-fix-xss-vulnerability.md
    |   |   |-- P1-R4-2026-06-01-fix-xss-vulnerability.md
    |   |   |-- P2-R2-2026-05-29-governance-state-reconciliation.md
    |   |   |-- P2-R2-2026-06-04-readme-retroactive-instantiation.md
    |   |   |-- P2-R3-2026-05-29-root-and-snippets-deprecation.md
    |   |   |-- P2-R3-2026-06-04-global-consistency-corrections.md
    |   |   |-- P2-R3-2026-06-05-remove-framework-docs-artifacts.md
    |   |   |-- P2-R3-2026-06-05-open-governance-issues.md
    |   |   |-- P3-R2-2026-05-29-add-language-detection-tests.md
    |   |   |-- P3-R2-2026-05-29-audit-follow-up-cleanup.md
    |   |   |-- P3-R2-2026-06-04-integrate-refactoring-guide.md
    |   |   |-- P3-R2-2026-06-04-structural-cleanup.md
    |   |   |-- P3-R2-2026-06-04-translate-refactoring-guide.md
    |   |   |-- P3-R2-2026-06-04-translation-fallback-tests.md
    |   |   |-- P4-R1-2026-05-29-readme-flowchart-alignment.md
    |   |   |-- P4-R1-2026-05-29-readme-scope-wording-corrections.md
    |   |   |-- P4-R1-2026-06-04-final-residual-cleanup.md
    |   |   |-- P4-R1-2026-06-04-governance-history-fix.md
    |   |   |-- P4-R1-2026-06-04-governance-logical-sync.md
    |   |   |-- P4-R1-2026-06-04-paradox-resolution.md
    |   |   |-- P4-R1-2026-06-04-wiki-schema-structural-sync.md
    |   |   |-- plan_fix_xss.md
    |   |   \-- translation-fallback-tests.md
    |   |-- discontinued
    |   |-- in_progress
    |   \-- pending
    |-- README.md (Framework README)
    |-- REFACTORING.md
    |-- refactoring-guide
    |   |-- 00-general-governance.md
    |   |-- 01-decision-guide.md
    |   |-- 02-composing-methods.md
    |   |-- 03-moving-features-between-objects.md
    |   |-- 04-organizing-data.md
    |   |-- 05-simplifying-conditional-expressions.md
    |   |-- 06-making-method-calls-simpler.md
    |   |-- 07-dealing-with-generalization.md
    |   |-- 08-code-smells-map.md
    |   |-- 09-pr-checklist.md
    |   |-- 10-code-inventory-and-classification.md
    |   |-- 11-refactoring-risk-matrix.md
    |   |-- 12-testing-strategy-before-refactoring.md
    |   |-- 13-ci-cd-pipeline-and-quality-gates.md
    |   |-- 14-rollback-plan.md
    |   |-- 15-incremental-refactoring-plan.md
    |   |-- 16-dependency-and-impact-map.md
    |   |-- 17-branch-and-pull-request-policy.md
    |   |-- 18-behavioral-refactoring-vs-rewrite.md
    |   |-- 19-stopping-criteria.md
    |   |-- 20-templates.md
    |   |-- MANIFEST.md
    |   \-- README.md
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
    |   |-- retroactive-instantiation
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
    |   |-- agents
    |   |   \-- README.md
    |   |-- audits
    |   |   \-- README.md
    |   |-- components
    |   |   \-- README.md
    |   |-- concepts
    |   |   \-- README.md
    |   |-- decisions
    |   |   \-- README.md
    |   |-- failures
    |   |   \-- README.md
    |   |-- inbox
    |   |   \-- README.md
    |   |-- index.md
    |   |-- log.md
    |   |-- patterns
    |   |   \-- README.md
    |   |-- prompts
    |   |   \-- README.md
    |   |-- questions
    |   |   \-- README.md
    |   |-- raw
    |   |   \-- README.md
    |   |-- refactorings
    |   |   \-- README.md
    |   |-- releases
    |   |   \-- v0-6-0.md
    |   |-- README.md
    |   |-- schema.md
    |   |-- sessions
    |   |   |-- README.md
    |   |   |-- S001-2026-05-29-readme-flowchart-alignment.md
    |   |   |-- S002-2026-05-29-governance-state-reconciliation.md
    |   |   |-- S003-2026-05-29-root-and-snippets-deprecation.md
    |   |   |-- S004-2026-05-29-audit-follow-up-cleanup.md
    |   |   |-- S005-2026-05-29-readme-scope-wording-corrections.md
    |   |   |-- S006-2024-06-01-fix-xss-vulnerability.md
    |   |   |-- S009-2026-06-05-remove-framework-docs-artifacts.md
    |   |   |-- S010-2026-06-05-open-governance-issues.md
    |   |   \-- S001.md
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
| `/FCVW/APPLICATION_DOCUMENTATION.md` | Rules for downstream application-owned module documentation. | [AGENTS.md](../AGENTS.md) | No |
| `/FCVW/troubleshooting/` | Stores issue records, hypotheses, handlings, and validation evidence. | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | No |
| `/FCVW/wiki/` | Continuous technical learning vault of the project. | [AI.md](AI.md) / `wiki/schema.md` | No |
| `/FCVW/wiki/agents/` | Agent-specific journals and journal path convention. | [AI.md](AI.md) / `wiki/schema.md` | No |
| `/FCVW/data/` | Stores local SQLite database and backups. | [DATA.md](DATA.md) | **Yes** (strict) |

---

## 3. Maintenance and Self-Healing Rules

1. **AI Checkpoints:** Whenever a new feature is requested, the AI must check `FILESYSTEM.md` before writing code to confirm where the new files belong.
2. **Declarative Layout Integrity:** The detailed visual tree in `FILESYSTEM.md` must be updated manually by the agent whenever files are added or deleted. Summary documents should link to this file instead of duplicating the full tree.
3. **Audit Closure:** The final step of any plan that alters directories is a manual verification of this document's visual tree.
