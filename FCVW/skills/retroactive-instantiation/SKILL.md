---
name: "retroactive-instantiation"
version: "1.0.0"
trigger_keywords: ["retroactive instantiation", "instanciação retroativa", "instanciacao retroativa", "existing app", "advanced app", "legacy app", "migrate old FCVW", "framework migration", "governance retrofit", "adotar FCVW", "migrar framework antigo"]
session_types: ["retroactive_instantiation", "migration", "document_audit", "refactoring"]
---

# SKILL: Retroactive Instantiation

High-density activation guide for adopting FrameCode VibeWork inside an existing, advanced, legacy, or partially governed application.

## Activation Triggers

Load this skill with `view_file` and `IsSkillFile: true` when:

- the user asks for retroactive FCVW adoption in an existing application;
- the repository already contains application code before FCVW is installed;
- an older or partial `FCVW/` structure must be migrated forward;
- the task mentions "instanciação retroativa", "adotar FCVW", "migrar framework antigo", "legacy app", "advanced app", or "governance retrofit".

Use `project-instantiation` instead for blank or fresh Phase 0 projects.

## Mandatory Source of Truth

Read and follow `FCVW/RETROACTIVE_INSTANTIATION.md`.

This skill is only the JIT trigger and compact checklist. Do not duplicate or override the canonical workflow.

## Execution Checklist

1. Read `AGENTS.md`, `FCVW/RETROACTIVE_INSTANTIATION.md`, and `FCVW/CONTEXT_MAP.md`.
2. Inspect the current repository and classify it:
   - Case A: no FCVW present;
   - Case B: older FCVW present;
   - Case C: partial or inconsistent FCVW present.
3. Create or update `FCVW/Plans/in_progress/P2-R4-{date}-retroactive-instantiation.md`.
4. Preserve application files first: source code, root README, runtime configs, data, tests, deployment files, and existing docs.
5. Import, repair, or migrate FCVW under `FCVW/` using non-destructive merges.
6. Fill project documents from evidence; use `To be defined` for missing facts.
7. Preserve historical plans, changelogs, troubleshooting records, decisions, audits, and wiki pages.
8. Add a changelog fragment, validation evidence, wiki log entry, session synthesis, and filesystem update.
9. Run safe local tests and structural checks; record limitations instead of inventing results.
10. Move the plan to the final status folder only after validation is recorded.

## Hard Rules

- Do not run recursive replacement across the repository.
- Do not overwrite application code or product docs with framework templates.
- Do not copy secrets or private data into FCVW records.
- Do not claim historical FCVW governance for work that happened before FCVW adoption.
- Do not refactor application code during retroactive instantiation unless the user explicitly requested it.

