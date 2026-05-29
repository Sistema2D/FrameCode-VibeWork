---
context_files:
  - AGENTS.md
  - README.md
  - docs/index.html
  - FCVW/README.md
  - FCVW/docs/index.html
  - FCVW/DESIGN.md
  - FCVW/SCOPE.md
  - FCVW/INSTANTIATION.md
  - FCVW/CONTEXT_MAP.md
  - FCVW/FILESYSTEM.md
  - FCVW/MANIFEST.md
  - FCVW/STACK.md
  - FCVW/AI.md
  - FCVW/skills/project-instantiation/SKILL.md
  - FCVW/snippets/
  - FCVW/wiki/index.md
  - FCVW/wiki/log.md
---
# P2-R3-2026-05-29-root-and-snippets-deprecation

- **Description:** Deprecate framework-owned root artifacts and the snippets library, keeping framework documentation inside `FCVW/`.
- **Justification:** The framework root must remain available for the application being instantiated. The root README and root `docs/` duplicate framework documentation, while `FCVW/snippets/` duplicates responsibilities that should be covered by `FCVW/DESIGN.md`.
- **Objective:** Make the framework self-contained under `FCVW/`, remove obsolete snippet/sample storage, and update instantiation rules so root README generation belongs to the target application.
- **Scope:**
  - Remove `README.md` from the repository root.
  - Remove root `docs/` because it duplicates `FCVW/docs/` and occupies application-owned space.
  - Keep `FCVW/docs/` as the framework documentation site artifact.
  - Remove `FCVW/snippets/` and all current snippet baseline files.
  - Update official governance documents and skills that reference root README, root docs, or snippets.
  - Update `FCVW/DESIGN.md` to explicitly act as the design-system source of truth.
  - Create audit, changelog, and AICC session records.
  - Preserve historical records that mention removed files as past evidence.
- **Affected files:**
  - README.md
  - docs/index.html
  - FCVW/snippets/README.md
  - FCVW/snippets/tokens.css
  - FCVW/snippets/gallery.html
  - FCVW/README.md
  - FCVW/DESIGN.md
  - FCVW/SCOPE.md
  - FCVW/INSTANTIATION.md
  - FCVW/CONTEXT_MAP.md
  - FCVW/FILESYSTEM.md
  - FCVW/MANIFEST.md
  - FCVW/STACK.md
  - FCVW/AI.md
  - FCVW/skills/project-instantiation/SKILL.md
  - FCVW/audits/2026-05-29-framework-structure-audit.md
  - FCVW/changelogs/unreleased/P2-R3-2026-05-29-root-and-snippets-deprecation.md
  - FCVW/wiki/sessions/S003-2026-05-29-root-and-snippets-deprecation.md
  - FCVW/wiki/index.md
  - FCVW/wiki/log.md
- **Implementation plan:**
  1. Create this plan in `pending`, update status to `in_progress`, and move to `Plans/in_progress/`.
  2. Remove root README, root docs duplicate, and snippets files/folder.
  3. Update governance references so `FCVW/README.md`, `FCVW/docs/`, and `FCVW/DESIGN.md` become the canonical framework sources.
  4. Update instantiation flow so root `README.md` is generated for the application during Phase 0.
  5. Run an Agnix-style structural audit and record findings/opportunities.
  6. Create changelog fragment and AICC session synthesis.
  7. Validate with `git diff --check`, structural scan, and `git status --short`.
- **Acceptance criteria:**
  - [x] Root `README.md` is removed from the framework baseline.
  - [x] Root `docs/` duplicate is removed; `FCVW/docs/index.html` remains.
  - [x] `FCVW/snippets/` is removed and no current official document depends on it.
  - [x] `FCVW/DESIGN.md` explicitly supersedes reusable UI snippet storage.
  - [x] Instantiation docs/skill state that the application root README is generated during Phase 0.
  - [x] `FCVW/FILESYSTEM.md`, `FCVW/MANIFEST.md`, `FCVW/SCOPE.md`, `FCVW/CONTEXT_MAP.md`, `FCVW/README.md`, `FCVW/STACK.md`, and `FCVW/AI.md` are aligned with the new structure.
  - [x] Audit report lists remaining failures and optimization opportunities.
  - [x] Changelog fragment and AICC synthesis are created and indexed.
- **Test plan:**
  - [x] `git diff --check`
  - [x] Custom structural scan for required paths, removed paths, links, tables, fences, README/docs/snippets references, and version fields.
  - [x] `git status --short`
- **Priority:** `P2`
- **Risk:** `R3`
- **Current Version:** `V0.7.5`
- **Expected Version:** `V0.7.5`
- **Status:** `completed`
- **Creation Date:** 2026-05-29
- **Completion Date:** 2026-05-29
- **Technical observations:**
  - This plan intentionally supersedes the earlier baseline that temporarily created `FCVW/snippets/`.
  - Historical plans, changelogs, troubleshooting records, and session syntheses may continue to mention removed files as past evidence.
  - Root `docs/` was byte-for-byte identical to `FCVW/docs/` at audit time and was removed from the framework baseline.

## Validation Executed (Fill on completion)

### Environment
- OS: Windows
- Backend/Runtime: Not applicable - Markdown governance framework

### Tests
| Test | Result | Evidence |
|---|---|---|
| `git diff --check` | pass | Exit code 0. Output contained only line-ending warnings such as `LF will be replaced by CRLF the next time Git touches it`. |
| Custom structural scan | pass | `missingRequired: []`, `removedStillPresent: []`, `fcvwDocsRetained: true`, `brokenLinkCount: 0`, `tableIssueCount: 0`, `skillTriggerIssues: []`, `activeDependencyRefs: []`. |
| `git status --short` | pass | Executed. Shows expected deletion of root `README.md` and root `docs/index.html`, plus modified/new governance records. |

### Final Result
`approved`
