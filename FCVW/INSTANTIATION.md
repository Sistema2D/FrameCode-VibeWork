# Framework Instantiation

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
- `FCVW/wiki/templates/`
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
- If the information does not exist yet, record the gap in `BRIEFING.md`, `MANIFEST.md`, or `wiki/questions/`.
- Do not replace placeholders inside `governance/` and `wiki/templates/`, as they are reusable models.

### Initial Version

- Define the initial version in `MANIFEST.md`, `STACK.md`, and the first changelog.
- Use `V0.1.0` when there is a usable initial scope.
- Use `V0.0.1` when the change is only structural, documental, or preparatory.

### Root README

- The framework baseline should not ship a generic root `README.md`.
- During Phase 0, create or update the root `README.md` as the README of the instantiated application.
- The application README must describe the target product, setup, execution, and usage. It must not describe the generic framework as the main subject.
- Use `FCVW/README.md` and `FCVW/governance/README_FRAMEWORK.md` as technical references for VibeWork FrameCode.

## Instantiation Flow

1. Read `AGENTS.md`, this file, and `BRIEFING.md`.
2. Confirm if the current directory is the original framework or a derived application.
3. Record or update a plan in `Plans/`.
4. Fill in `BRIEFING.md` with known answers.
5. Update `MANIFEST.md`, `STACK.md`, `SCOPE.md`, and create or update the root `README.md` for the application.
6. Translate `DESIGN.md` YAML tokens into a physical codebase configuration file (e.g., `tailwind.config.js`, `index.css`, or `theme.ts`) to establish the UI foundation.
7. Remove non-applicable sections in canonical documents.
8. Create a changelog fragment in `changelogs/unreleased/{plan-name}.md`.
9. Validate remaining placeholders outside templates.
10. Update `wiki/index.md` and `wiki/log.md` if the instantiation generates reusable learning.
11. Complete the plan and move it to the final status folder.

## Recommended Validation

Before closing the instantiation:

- verify that no removed bootstrap script is cited as mandatory;
- look for placeholders outside `governance/` and `wiki/templates/`;
- confirm that the root `README.md`, when present, describes the correct application target;
- confirm that `AGENTS.md` lists existing official documents;
- confirm that plans and changelogs were created or updated;
- verify that `.gitignore` covers caches, builds, logs, and private data.

## Final Rule

Instantiation is not a global textual replacement. It is a controlled migration from a generic framework to a specific project, with review of affected files, traceability via plan and changelog, and preservation of reusable templates.
