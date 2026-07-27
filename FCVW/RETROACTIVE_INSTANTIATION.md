---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Retroactive Instantiation

> **Purpose**: Adopt FrameCode VibeWork (FCVW) in an existing, advanced, legacy, or partially governed application — without losing history, code, or existing documentation.

## When to Use

Use this workflow when you have an existing project (with code, history, partial docs) and want to adopt the FCVW governance framework *retroactively* — as opposed to starting a new project from the framework baseline (see `INSTANTIATION.md` for greenfield projects).

## Core Principle

**Preserve everything non-destructively.** Never delete or rewrite existing application files, history, or documentation as part of the instantiation. FCVW documents are *added* to the repository, coexisting with existing content.

## Prerequisites

- Git repository with existing code and commit history.
- Read access to all existing documentation, configuration, and build files.
- Decision on whether to keep the existing root `README.md` or merge it with framework docs.

## Step-by-Step Workflow

### Phase 1 — Assessment

1. **Map existing structure**: Inventory all directories, configuration files, documentation, and data schemas.
2. **Identify governance gaps**: Compare the repository with `MANIFEST.md`, `FILESYSTEM.md`, and `OWNERSHIP.md`; record which canonical profiles and record directories are missing.
3. **Record baseline**: Create a record in `FCVW/briefings/` describing the pre-adoption state.
4. **Run hygiene triage**: Load `skills/code-hygiene-refactor/SKILL.md` and identify duplicate snippets, stale files, dead code candidates, catch-all modules, and monolithic files without modifying application code.
5. **Run anti-monolith triage**: Load `skills/anti-monolith-guard/SKILL.md` for any large or mixed-responsibility area that will receive new FCVW-driven changes.

### Phase 2 — Framework Integration

1. **Copy one clean distribution**: Use the single language-specific FCVW release artifact chosen by the user. Exclude comparison evidence and downstream/application history from a source checkout; governed framework history may remain when the release contract includes it. Do not copy all language variants or add automatic language selection.
2. **Copy AGENTS.md** to the project root as the bridge entrypoint.
3. **Merge README.md**: Keep the existing project README. Add a section referencing `AGENTS.md` as the governance entry point.
4. **Update `.gitignore`**: Preserve project-specific rules and add only the exclusions required by files actually adopted.
5. **Preserve existing CI/CD**: Do not modify existing pipelines unless explicitly required.

### Phase 3 — Backfill

1. **Fill BRIEFING.md**: Document the project's origin, scope, and current state.
2. **Fill MANIFEST.md** §1: Set project name, version, lead, and repository URL.
3. **Fill STACK.md**: Document existing technology stack.
4. **Create initial wiki pages** only for reusable learnings already accumulated.
5. **Mark historical artifacts**: Existing documentation not yet migrated to FCVW can be marked as `pre-fcvw` or left in place with a note.
6. **Create hygiene backlog**: Record high-value cleanup candidates as `#tech-debt`, `wiki/refactorings/`, or future plans. Do not refactor during adoption unless explicitly requested.

### Phase 4 — First Plan

1. Create a P3-R2 plan documenting the retroactive instantiation itself.
2. The plan scope covers: copied files, filled metadata, created wiki records.
3. Validate that existing workflows (build, test, deploy) continue to function.
4. The first post-adoption implementation plan that touches an identified monolith must pass the Anti-Monolith Gate before editing.

## Important Restrictions

- **Do not** run recursive scripts to rename or replace content in batch.
- **Do not** rebase or rewrite Git history.
- **Do not** delete existing documentation without explicit project owner approval.
- **Do not** move or restructure existing source code to fit a preconceived tree.
- **Do not** normalize monoliths during framework adoption unless the user explicitly requested active refactoring and a separate plan exists.
- **Do not** add new behavior to an identified monolith without first passing `anti-monolith-guard`.

## Relationship with Other Skills

- Use `skill:project-instantiation` for greenfield projects (see `FCVW/INSTANTIATION.md`).
- Use `skill:retroactive-instantiation` as the ASE skill for JIT procedural guidance.
- Use `FCVW/CONTEXT_MAP.md` for selective document loading after adoption.

## See Also

- `FCVW/INSTANTIATION.md` — greenfield project instantiation
- `FCVW/skills/retroactive-instantiation/SKILL.md` — ASE skill version
- `FCVW/CONTEXT_MAP.md` — session type: Briefing / Instantiation

## Application-rule and graph backfill

During retroactive adoption:

1. inventory business rules already enforced by code, tests, workflows, and user-facing behavior;
2. promote only confirmed application rules to `FCVW/APP_RULES.md`, with stable IDs and affected boundaries;
3. build `FCVW/DOCUMENT_GRAPH.md` after the adopted files are linked from official entrypoints;
4. report pre-existing orphan records explicitly instead of inventing relationships; and
5. if an incremental orphan baseline is temporarily approved for legacy content, restrict it to exact paths and never add new artifacts to it.
