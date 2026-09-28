---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Framework instantiation

Operational document to transform the FrameCode VibeWork into a concrete application without relying on automatic bulk replacement scripts.

## Objective

Define how to copy, rename, fill out, and validate framework files when starting a new AI-assisted project.

This file replaces any previous rule based on an `init.ps1` script. Instantiation must be explicit, reviewable, and traceable.

## When to Use

Use this document when:

- a new project is started from VibeWork FrameCode;
- a cloned framework folder needs to become a real application;
- there is doubt about which files should remain generic and which should be filled out;
- an AI agent needs to rename files, folders, titles, or placeholders of the framework.

## Principles

- Start from exactly one language-specific clean release variant selected by the user at download time.
- Treat the downloaded variant as a normal monolingual framework tree; do not add, discover, or synchronize the other language variants.
- Do not perform automatic recursive replacement in all files.
- Do not alter generic templates as if they were canonical project documents.
- Do not fill in placeholders without briefing evidence or explicit confirmation from the user.
- Rename only what is within the scope of the instantiation.
- Record the change in a plan and changelog when the instantiation occurs within a versioned repository.

## Separation Between Layers

### Canonical Project Documents

They reside inside the `FCVW/` folder (except `AGENTS.md` which remains in the root as the bridge entrypoint) and must be filled with real application data:

- `FCVW/MANIFEST.md`
- `FCVW/STACK.md`
- `FCVW/SCOPE.md`
- `FCVW/DESIGN.md`, when there is UI
- `FCVW/WORKFLOW.md`
- `FCVW/DATA.md`, when there is persistence
- `FCVW/AI.md`, when there are AI features
- `AGENTS.md` (at the root)

### Framework Templates

They must remain generic, reusable, and reside inside the `FCVW/` subfolder:

- `FCVW/governance/`
- `FCVW/skills/QA/TEMPLATE_*.md`
- design-system rules in `FCVW/DESIGN.md`.

## Renaming Rules

### Project Folder Name

- Use a short name in `kebab-case`, without spaces.
- Prefer ASCII characters in the folder name to avoid problems with build tools, scripts, and CI.
- Example: `my-product`, `financial-control`, `legal-assistant`.

### Document Titles

- Replace generic titles only in root canonical documents.
- Preserve technical prefixes when they identify the role of the file, e.g., `AGENTS.md`, `STACK.md`, and `DESIGN.md`.
- Do not rename official files without updating `AGENTS.md`, `MANIFEST.md`, and cross-references.

### Placeholders

- Replace placeholders like `<project name>`, `<technology>`, `<objective>`, and `<risk>` only when there is an answer in the briefing, a recorded decision, or direct confirmation from the user.
- If the information does not exist yet, record the gap in `BRIEFING.md`, `MANIFEST.md`, or `wiki/` (`type: question` notes).
- Do not replace placeholders inside `governance/` and `skills/QA/TEMPLATE_*.md`, as they are reusable models.

### Initial Version

- Define one canonical application version source, reference it from `MANIFEST.md`, and create the first application changelog.
- Use `V0.1.0` when there is a usable initial scope.
- Use `V0.0.1` when the change is only structural, documental, or preparatory.

### Root README

- The framework source repository may ship its public root `README.md`; a downstream clean-template artifact marks it for replacement during Phase 0.
- During Phase 0, create or update the root `README.md` as the README of the instantiated application.
- The application README must describe the target product, setup, execution, and usage. It must not describe the generic framework as the main subject.
- Use `FCVW/README.md`, `FCVW/OWNERSHIP.md`, and `FCVW/FRAMEWORK_LOCK.md` as technical references.

## Instantiation Flow

1. Read `AGENTS.md`, this file, and `BRIEFING.md`.
2. Confirm if the current directory is the original framework or a derived application.
3. Record or update a plan in `FCVW/Plans/`.
4. Fill in `BRIEFING.md` with known answers.
5. Update application-owned profiles, choose one application version source, and create or update the root `README.md` for the application.
6. Translate `DESIGN.md` YAML tokens into a physical codebase configuration file (e.g., `tailwind.config.js`, `index.css`, or `theme.ts`) to establish the UI foundation.
7. Remove non-applicable sections and set each completed profile `instantiation_status` to `complete`. A profile the project does not use yet takes `not_applicable` plus a concrete `not_applicable_reason` instead of invented content; `MANIFEST.md` and `SCOPE.md` may never be waived.
8. Create a changelog fragment in `changelogs/unreleased/{plan-name}.md`.
9. Validate remaining placeholders according to artifact role.
10. Update `wiki/index.md` if the instantiation generates reusable learning.
11. Run `python FCVW/tools/validate_fcvw.py --root . --profile instantiated` for an installed release (`python tools/validate_fcvw.py ...` in the framework source checkout), then complete the plan.

## Recommended Validation

Before closing the instantiation:

- verify that no removed bootstrap script is cited as mandatory;
- look for placeholders outside templates, examples, and explicitly pending project profiles;
- confirm that the root `README.md`, when present, describes the correct application target;
- confirm that `AGENTS.md` lists existing official documents;
- confirm that plans and changelogs were created or updated;
- verify that `.gitignore` covers caches, builds, logs, and private data.
- confirm `FRAMEWORK_LOCK.md` and application version remain separate.

## Final Rule

Instantiation is not a global textual replacement. It is a controlled migration from a generic framework to a specific project, with review of affected files, traceability via plan and changelog, and preservation of reusable templates.

## Application-rule and graph initialization

During Phase 0, review `APP_RULES.md` with briefing evidence. Set `instantiation_status: complete` only after known cross-cutting rules are recorded or the absence of current rules is explicitly justified.

Create the first plan in `pending/`, add it to `pending/QUEUE.md`, then move both plan state and queue membership transactionally. After generated records or documentation are added, regenerate `DOCUMENT_GRAPH.md` and require zero blocking orphans before closeout.

## Retroactive instantiation

Use this mode to adopt FCVW in an existing, advanced, legacy, or partially governed application without losing history, code, or existing documentation.

> **Purpose**: Adopt FrameCode VibeWork (FCVW) in an existing, advanced, legacy, or partially governed application — without losing history, code, or existing documentation.

### When to Use

Use this workflow when you have an existing project (with code, history, partial docs) and want to adopt the FCVW governance framework *retroactively* — as opposed to starting a new project from the framework baseline (see `INSTANTIATION.md` for greenfield projects).

### Core Principle

**Preserve everything non-destructively.** Never delete or rewrite existing application files, history, or documentation as part of the instantiation. FCVW documents are *added* to the repository, coexisting with existing content.

### Prerequisites

- Git repository with existing code and commit history.
- Read access to all existing documentation, configuration, and build files.
- Decision on whether to keep the existing root `README.md` or merge it with framework docs.

### Step-by-Step Workflow

#### Phase 1 — Assessment

1. **Map existing structure**: Inventory all directories, configuration files, documentation, and data schemas.
2. **Identify governance gaps**: Compare the repository with `MANIFEST.md` and the filesystem layout in `OWNERSHIP.md`; record which canonical profiles and record directories are missing.
3. **Record baseline**: Create a record in `FCVW/briefings/` describing the pre-adoption state.
4. **Run hygiene triage**: Load `skills/code-hygiene-refactor/SKILL.md` and identify duplicate snippets, stale files, dead code candidates, catch-all modules, and monolithic files without modifying application code.
5. **Run anti-monolith triage**: Load `skills/anti-monolith-guard/SKILL.md` for any large or mixed-responsibility area that will receive new FCVW-driven changes.

#### Phase 2 — Framework Integration

1. **Copy one clean distribution**: Use the single language-specific FCVW release artifact chosen by the user. Exclude comparison evidence and downstream/application history from a source checkout; governed framework history may remain when the release contract includes it. Do not copy all language variants or add automatic language selection.
2. **Copy AGENTS.md** to the project root as the bridge entrypoint.
3. **Merge README.md**: Keep the existing project README. Add a section referencing `AGENTS.md` as the governance entry point.
4. **Update `.gitignore`**: Preserve project-specific rules and add only the exclusions required by files actually adopted.
5. **Preserve existing CI/CD**: Do not modify existing pipelines unless explicitly required.

#### Phase 3 — Backfill

1. **Fill BRIEFING.md**: Document the project's origin, scope, and current state.
2. **Fill MANIFEST.md** §1: Set project name, version, lead, and repository URL.
3. **Fill STACK.md**: Document existing technology stack.
4. **Create initial wiki pages** only for reusable learnings already accumulated.
5. **Mark historical artifacts**: Existing documentation not yet migrated to FCVW can be marked as `pre-fcvw` or left in place with a note.
6. **Create hygiene backlog**: Record high-value cleanup candidates as `#tech-debt`, `wiki/` (`type: refactoring` notes), or future plans. Do not refactor during adoption unless explicitly requested.

#### Phase 4 — First Plan

1. Create a P3-R2 plan documenting the retroactive instantiation itself.
2. The plan scope covers: copied files, filled metadata, created wiki records.
3. Validate that existing workflows (build, test, deploy) continue to function.
4. The first post-adoption implementation plan that touches an identified monolith must pass the Anti-Monolith Gate before editing.

### Important Restrictions

- **Do not** run recursive scripts to rename or replace content in batch.
- **Do not** rebase or rewrite Git history.
- **Do not** delete existing documentation without explicit project owner approval.
- **Do not** move or restructure existing source code to fit a preconceived tree.
- **Do not** normalize monoliths during framework adoption unless the user explicitly requested active refactoring and a separate plan exists.
- **Do not** add new behavior to an identified monolith without first passing `anti-monolith-guard`.

### Relationship with Other Skills

- Use `skill:project-instantiation` for greenfield projects (see `FCVW/INSTANTIATION.md`).
- Use `skill:retroactive-instantiation` as the ASE skill for JIT procedural guidance.
- Use `FCVW/CONTEXT_MAP.md` for selective document loading after adoption.

### See Also

- `FCVW/INSTANTIATION.md` — greenfield project instantiation
- `FCVW/skills/retroactive-instantiation/SKILL.md` — ASE skill version
- `FCVW/CONTEXT_MAP.md` — session type: Briefing / Instantiation

### Application-rule and graph backfill

During retroactive adoption:

1. inventory business rules already enforced by code, tests, workflows, and user-facing behavior;
2. promote only confirmed application rules to `FCVW/APP_RULES.md`, with stable IDs and affected boundaries;
3. build `FCVW/DOCUMENT_GRAPH.md` after the adopted files are linked from official entrypoints;
4. report pre-existing orphan records explicitly instead of inventing relationships; and
5. if an incremental orphan baseline is temporarily approved for legacy content, restrict it to exact paths and never add new artifacts to it.
