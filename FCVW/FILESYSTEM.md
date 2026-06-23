---
title: "Project Filesystem Architecture"
type: "concept"
status: "validated"
confidence: "high"
last_reviewed: "2026-06-23"
related_version: "V0.12.0"
sources:
  - "STACK.md"
  - "SCOPE.md"
  - "DESIGN.md"
  - "decisions/ADR-0001-pure-markdown-over-automation-scripts.md"
  - "decisions/ADR-0002-declarative-automation-contracts.md"
tags:
  - "filesystem"
  - "architecture"
  - "declarative-automation"
---

# Project Filesystem Architecture

This document defines the physical directory structure of the application. It serves as the single source of truth for the file organization, ensuring absolute consistency between design rules, stack requirements, and physical implementation.

In accordance with [ADR-0001](decisions/ADR-0001-pure-markdown-over-automation-scripts.md), this directory layout is maintained declaratively in Markdown and verified manually by agents, eliminating dependencies on local environment scripts.

In accordance with [ADR-0002](decisions/ADR-0002-declarative-automation-contracts.md), hook, watcher, daemon, and governance-gate artifacts are represented as Markdown-only contracts, not executable automation.

---

## 1. Visual Application Tree

<!-- START_TREE -->
```text
[project-root]/
|-- .github/
|   \-- FUNDING.yml
|-- FCVW/
|   |-- audits/
|   |   \-- README.md
|   |-- briefings/
|   |   \-- README.md
|   |-- changelogs/
|   |   |-- unreleased/
|   |   |   |-- P2-R3-2026-06-23-declarative-automation-contracts.md
|   |   |   \-- README.md
|   |   |-- V0.10.0.md
|   |   |-- V0.10.1.md
|   |   |-- V0.10.2.md
|   |   |-- V0.10.3.md
|   |   |-- V0.11.0.md
|   |   |-- V0.9.0.md
|   |   \-- V0.9.1.md
|   |-- decisions/
|   |   |-- ADR-0001-pure-markdown-over-automation-scripts.md
|   |   \-- ADR-0002-declarative-automation-contracts.md
|   |-- governance/
|   |   |-- README_FRAMEWORK.md
|   |   |-- TEMPLATE_ADR.md
|   |   |-- TEMPLATE_AGENT_OR_SKILL_PROPOSAL.md
|   |   |-- TEMPLATE_AI_RESOURCE.md
|   |   |-- TEMPLATE_AI_SESSION_SYNTHESIS.md
|   |   |-- TEMPLATE_API_SPEC.md
|   |   |-- TEMPLATE_APP_DOCS_README.md
|   |   |-- TEMPLATE_AUTOMATION_CONTRACT.md
|   |   |-- TEMPLATE_BRIEFING.md
|   |   |-- TEMPLATE_CODE_HYGIENE_REPORT.md
|   |   |-- TEMPLATE_DAEMON_LOOP.md
|   |   |-- TEMPLATE_DATA_SCHEMA.md
|   |   |-- TEMPLATE_ENV.md
|   |   |-- TEMPLATE_FLOW_DOCUMENTATION.md
|   |   |-- TEMPLATE_GOVERNANCE_GATE_REPORT.md
|   |   |-- TEMPLATE_HOOK_CHECK.md
|   |   |-- TEMPLATE_MIGRATION_RUNNER.md
|   |   |-- TEMPLATE_MODULE_DOCUMENTATION.md
|   |   |-- TEMPLATE_MONOLITH_GATE.md
|   |   |-- TEMPLATE_PLAN.md
|   |   |-- TEMPLATE_REFACTORING.md
|   |   |-- TEMPLATE_REFACTORING_ADR.md
|   |   |-- TEMPLATE_REFACTORING_CHARACTERIZATION_TEST_PLAN.md
|   |   |-- TEMPLATE_REFACTORING_DEPENDENCY_MAP.md
|   |   |-- TEMPLATE_REFACTORING_INCREMENTAL_PLAN.md
|   |   |-- TEMPLATE_REFACTORING_MODULE_INVENTORY.md
|   |   |-- TEMPLATE_REFACTORING_OPENING.md
|   |   |-- TEMPLATE_REFACTORING_POST_VALIDATION_REPORT.md
|   |   |-- TEMPLATE_REFACTORING_PULL_REQUEST.md
|   |   |-- TEMPLATE_REFACTORING_RISK_MATRIX.md
|   |   |-- TEMPLATE_REFACTORING_ROLLBACK_PLAN.md
|   |   |-- TEMPLATE_RELEASE.md
|   |   |-- TEMPLATE_SELF_IMPROVEMENT_REPORT.md
|   |   |-- TEMPLATE_TROUBLESHOOTING.md
|   |   |-- TEMPLATE_VISUAL_DIFF.md
|   |   \-- TEMPLATE_WATCHER_RULE.md
|   |-- Plans/
|   |   |-- completed/
|   |   |   |-- P1-R4-2026-06-11-service-research-mandate.md
|   |   |   |-- P2-R1-2026-06-17-v0103-github-release-publication.md
|   |   |   |-- P2-R2-2026-06-17-v0103-release-governance-jit-fixes.md
|   |   |   |-- P2-R2-2026-06-17-v0110-wiki-continuous-learning-governance.md
|   |   |   |-- P2-R3-2026-06-11-environment-promotion-workflow.md
|   |   |   |-- P2-R3-2026-06-11-pr-branch-workflow.md
|   |   |   |-- P2-R3-2026-06-13-anti-monolith-code-hygiene.md
|   |   |   |-- P2-R3-2026-06-13-framework-agent-self-improvement-template-site.md
|   |   |   |-- P2-R4-2026-06-11-multi-agent-concurrency.md
|   |   |   |-- P3-R2-2026-06-13-v0101-cleanup-optimization.md
|   |   |   |-- P3-R2-2026-06-14-final-compliance-qa.md
|   |   |   \-- README.md
|   |   |-- discontinued/
|   |   |   \-- README.md
|   |   |-- in_progress/
|   |   |   |-- P2-R3-2026-06-23-declarative-automation-contracts.md
|   |   |   \-- README.md
|   |   |-- pending/
|   |   |   \-- README.md
|   |   \-- README.md
|   |-- refactoring-guide/
|   |   |-- 00-general-governance.md
|   |   |-- 01-decision-guide.md
|   |   |-- 02-composing-methods.md
|   |   |-- 03-moving-features-between-objects.md
|   |   |-- 04-organizing-data.md
|   |   |-- 05-simplifying-conditional-expressions.md
|   |   |-- 06-making-method-calls-simpler.md
|   |   |-- 07-dealing-with-generalization.md
|   |   |-- 08-code-smells-map.md
|   |   |-- 09-pr-checklist.md
|   |   |-- 10-code-inventory-and-classification.md
|   |   |-- 11-refactoring-risk-matrix.md
|   |   |-- 12-testing-strategy-before-refactoring.md
|   |   |-- 13-ci-cd-pipeline-and-quality-gates.md
|   |   |-- 14-rollback-plan.md
|   |   |-- 15-incremental-refactoring-plan.md
|   |   |-- 16-dependency-and-impact-map.md
|   |   |-- 17-branch-and-pull-request-policy.md
|   |   |-- 18-behavioral-refactoring-vs-rewrite.md
|   |   |-- 19-stopping-criteria.md
|   |   |-- 20-templates.md
|   |   |-- MANIFEST.md
|   |   \-- README.md
|   |-- skills/
|   |   |-- agent-aegis/
|   |   |   \-- SKILL.md
|   |   |-- agent-factory/
|   |   |   \-- SKILL.md
|   |   |-- agent-hephaestus/
|   |   |   \-- SKILL.md
|   |   |-- agent-hermes/
|   |   |   \-- SKILL.md
|   |   |-- agnix-linter/
|   |   |   \-- SKILL.md
|   |   |-- aicc-compact/
|   |   |   \-- SKILL.md
|   |   |-- anti-monolith-guard/
|   |   |   \-- SKILL.md
|   |   |-- brainstorming-and-tdd/
|   |   |   \-- SKILL.md
|   |   |-- code-hygiene-refactor/
|   |   |   \-- SKILL.md
|   |   |-- git-conventional-commits/
|   |   |   \-- SKILL.md
|   |   |-- governance-validator/
|   |   |   \-- SKILL.md
|   |   |-- memory-rotation/
|   |   |   \-- SKILL.md
|   |   |-- obsidian-markdown/
|   |   |   \-- SKILL.md
|   |   |-- orchestrator/
|   |   |   \-- SKILL.md
|   |   |-- project-instantiation/
|   |   |   \-- SKILL.md
|   |   |-- release-checklist/
|   |   |   \-- SKILL.md
|   |   |-- retroactive-instantiation/
|   |   |   \-- SKILL.md
|   |   |-- self-improvement/
|   |   |   \-- SKILL.md
|   |   |-- systematic-debugging/
|   |   |   \-- SKILL.md
|   |   |-- wiki-curator/
|   |   |   \-- SKILL.md
|   |   |-- wiki-lint/
|   |   |   \-- SKILL.md
|   |   \-- README.md
|   |-- troubleshooting/
|   |   \-- README.md
|   |-- wiki/
|   |   |-- agents/
|   |   |   \-- README.md
|   |   |-- audits/
|   |   |   \-- README.md
|   |   |-- components/
|   |   |   \-- README.md
|   |   |-- concepts/
|   |   |   \-- README.md
|   |   |-- decisions/
|   |   |   \-- README.md
|   |   |-- failures/
|   |   |   \-- README.md
|   |   |-- inbox/
|   |   |   \-- README.md
|   |   |-- patterns/
|   |   |   \-- README.md
|   |   |-- prompts/
|   |   |   \-- README.md
|   |   |-- questions/
|   |   |   \-- README.md
|   |   |-- raw/
|   |   |   \-- README.md
|   |   |-- refactorings/
|   |   |   |-- agent-skill-self-improvement-governance.md
|   |   |   |-- anti-monolith-and-code-hygiene-gates.md
|   |   |   \-- README.md
|   |   |-- releases/
|   |   |   |-- README.md
|   |   |   |-- v0-8-0-summary.md
|   |   |   |-- v0-9-0-summary.md
|   |   |   |-- v0-9-1-summary.md
|   |   |   |-- v0-10-0-summary.md
|   |   |   |-- v0-10-1-summary.md
|   |   |   |-- v0-10-2-summary.md
|   |   |   |-- v0-10-3-summary.md
|   |   |   \-- v0-11-0-summary.md
|   |   |-- sessions/
|   |   |   |-- README.md
|   |   |   |-- S001-2026-06-11-governance-gaps-closure.md
|   |   |   |-- S002-2026-06-13-anti-monolith-code-hygiene.md
|   |   |   |-- S003-2026-06-13-agent-self-improvement-template-site.md
|   |   |   |-- S004-2026-06-13-v0101-cleanup-optimization.md
|   |   |   |-- S005-2026-06-14-final-compliance-qa.md
|   |   |   |-- S006-2026-06-17-v0103-release-governance-jit-fixes.md
|   |   |   \-- S007-2026-06-17-v0110-wiki-continuous-learning-governance.md
|   |   |-- sources/
|   |   |   |-- README.md
|   |   |   \-- santanderai-declarative-automation-inspiration.md
|   |   |-- syntheses/
|   |   |   \-- README.md
|   |   |-- templates/
|   |   |   |-- README.md
|   |   |   |-- TEMPLATE_DECISION.md
|   |   |   |-- TEMPLATE_FAILURE.md
|   |   |   |-- TEMPLATE_GENERAL_NOTE.md
|   |   |   |-- TEMPLATE_LINT.md
|   |   |   |-- TEMPLATE_PATTERN.md
|   |   |   |-- TEMPLATE_QUESTION.md
|   |   |   |-- TEMPLATE_RELEASE_SYNTHESIS.md
|   |   |   |-- TEMPLATE_SESSION_SYNTHESIS.md
|   |   |   \-- TEMPLATE_TECH_DEBT.md
|   |   |-- index.md
|   |   |-- log.md
|   |   |-- metrics.md
|   |   |-- README.md
|   |   |-- schema.md
|   |   \-- taxonomy.md
|   |-- AI.md
|   |-- APPLICATION_DOCUMENTATION.md
|   |-- ARCHITECTURAL_DECISIONS.md
|   |-- AUDIT.md
|   |-- AUTOMATION.md
|   |-- BRIEFING.md
|   |-- CONTEXT_MAP.md
|   |-- DAEMONS.md
|   |-- DATA.md
|   |-- DESIGN.md
|   |-- ENVIRONMENT.md
|   |-- FILESYSTEM.md
|   |-- GOVERNANCE_GATES.md
|   |-- HOOKS.md
|   |-- INSTANTIATION.md
|   |-- LICENSE
|   |-- MANIFEST.md
|   |-- PERFORMANCE.md
|   |-- PLANNING.md
|   |-- README.md
|   |-- REFACTORING.md
|   |-- RELEASE.md
|   |-- repository-open-graph-template.png
|   |-- RETROACTIVE_INSTANTIATION.md
|   |-- SCOPE.md
|   |-- SECURITY.md
|   |-- STACK.md
|   |-- TESTS.md
|   |-- TROUBLESHOOTING.md
|   |-- VERSIONING.md
|   |-- WATCHERS.md
|   \-- WORKFLOW.md
|-- .cursorrules
|-- .gitignore
|-- .windsurfrules
|-- AGENTS.md
|-- README.md
\-- relatorio_auditoria_fcvw.md
```
<!-- END_TREE -->

---

## 2. Directory and File Roles

| Path | Primary Role | Stakeholders / Sources | Git Ignored? |
|---|---|---|---|
| `/FCVW/Plans/` | Contains chronological implementation change plans. | `PLANNING.md` | No |
| `/FCVW/audits/` | Stores formal audit records and pre-release review evidence. | `AUDIT.md` | No |
| `/FCVW/briefings/` | Stores Phase 0 discovery and instantiation records. | `BRIEFING.md` / `INSTANTIATION.md` | No |
| `/FCVW/decisions/` | Stores formal Architectural Decision Records (ADRs). | `ARCHITECTURAL_DECISIONS.md` | No |
| `/FCVW/changelogs/` | Formal version release notes and unreleased plan fragments. | `VERSIONING.md` | No |
| `/FCVW/governance/` | Reusable empty blueprint templates. | `INSTANTIATION.md` | No |
| `/FCVW/wiki/` | Continuous technical learning vault of the project. | `AI.md` / `wiki/schema.md` | No |
| `/FCVW/wiki/sources/` | External source notes and conceptual inspiration records. | `wiki/schema.md` / `wiki-lint` | No |
| `/FCVW/AUTOMATION.md` | Parent contract for Markdown-only declarative automation. | `AGENTS.md` / ADR-0002 | No |
| `/FCVW/HOOKS.md` | Defines pseudo-hook checklists without installing Git hooks. | `AUTOMATION.md` / `PLANNING.md` | No |
| `/FCVW/WATCHERS.md` | Defines event/reaction watcher rules without coded watchers. | `AUTOMATION.md` / `governance-validator` | No |
| `/FCVW/DAEMONS.md` | Defines manual/agentic maintenance loops without background processes. | `AUTOMATION.md` / `AI.md` / `SECURITY.md` | No |
| `/FCVW/GOVERNANCE_GATES.md` | Maps gate triggers, evidence, owners, and blocking conditions. | `PLANNING.md` / `skills/` | No |
| `/FCVW/APPLICATION_DOCUMENTATION.md` | Rules for downstream application-owned module documentation. | `AGENTS.md` | No |
| `/FCVW/troubleshooting/` | Stores issue records, hypotheses, handlings, and validation evidence. | `TROUBLESHOOTING.md` | No |
| `/FCVW/data/` | Stores local SQLite database and backups when an instantiated app needs persistence. | `DATA.md` | **Yes** (strict) |

---

## 3. Maintenance and Self-Healing Rules

1. **AI Checkpoints:** Whenever a new feature is requested, the AI must check `FILESYSTEM.md` before writing code to confirm where the new files belong.
2. **Declarative Layout Integrity:** The detailed visual tree in `FILESYSTEM.md` must be updated manually by the agent whenever files are added, moved, renamed, or deleted. Summary documents should link to this file instead of duplicating the full tree.
3. **Automation Boundary Integrity:** Hook, watcher, daemon, and gate files must remain Markdown-only contracts under Scenario 1. They must not introduce scripts, installed hooks, coded watchers, background daemons, package manifests, CI/CD workflows, provider SDKs, or API-key flows.
4. **Audit Closure:** The final step of any plan that alters directories is a manual verification of this document's visual tree.
5. **Baseline Accuracy:** This document must always reflect the actual on-disk state. If a directory is empty (only a `README.md` placeholder), the tree must show only the placeholder. Do not list files that do not exist.
6. **Credit Traceability:** External conceptual inspiration, such as SantanderAI public repositories, must be recorded in relevant documents or `wiki/sources/` without implying copied code.
