---
context_files:
  - FCVW/README.md
  - FCVW/SCOPE.md
  - FCVW/MANIFEST.md
  - FCVW/STACK.md
  - FCVW/RELEASE.md
  - FCVW/FILESYSTEM.md
  - FCVW/wiki/index.md
  - FCVW/wiki/log.md
---
# P4-R1-2026-05-29-readme-scope-wording-corrections

- **Description:** Correct README wording that can imply outdated scope after root/docs/snippets cleanup.
- **Justification:** The README is broadly aligned with the current framework scope, but a few phrases still over-emphasize GitHub Pages, can blur the distinction between framework root and instantiated application root, and present token-cost estimates without enough calibration context.
- **Objective:** Keep `FCVW/README.md` consistent with the current scope and release rules without changing framework behavior.
- **Scope:**
  - Reword public documentation publishing flow to treat GitHub Pages as an optional example, not an inherent framework scope.
  - Clarify that project-filled documents live in the root of the instantiated application.
  - Clarify that token-consumption values are planning estimates, not recalibrated measurements after every governance edit.
  - Update mandatory changelog fragment, AICC session synthesis, wiki index/log, and filesystem tree.
- **Affected files:**
  - FCVW/README.md
  - FCVW/FILESYSTEM.md
  - FCVW/changelogs/unreleased/P4-R1-2026-05-29-readme-scope-wording-corrections.md
  - FCVW/wiki/sessions/S005-2026-05-29-readme-scope-wording-corrections.md
  - FCVW/wiki/index.md
  - FCVW/wiki/log.md
- **Implementation plan:**
  1. Create this plan, move it to `in_progress`, and update status.
  2. Patch the Portuguese and English README sections.
  3. Add changelog fragment and session synthesis.
  4. Update filesystem/wiki indexes and close this plan.
  5. Validate with `git diff --check`, custom structural scan, and `git status --short`.
- **Acceptance criteria:**
  - [x] README no longer presents GitHub Pages as a built-in framework scope.
  - [x] README clarifies that filled project documents belong to the instantiated application root.
  - [x] README marks token values as planning estimates that require recalibration after material document growth.
  - [x] Required changelog and AICC records exist.
- **Test plan:**
  - [x] `git diff --check`
  - [x] Custom structural scan for links, fences, tables, skill triggers, and expected README wording.
  - [x] `git status --short`
- **Priority:** `P4`
- **Risk:** `R1`
- **Current Version:** `V0.7.5`
- **Expected Version:** `V0.7.5`
- **Status:** `completed`
- **Creation Date:** 2026-05-29
- **Completion Date:** 2026-05-29
- **Technical observations:**
  - Scope is intentionally limited to wording and governance records.
  - `agnix-linter` was used as a validation checklist because the task involved governance consistency.

## Validation Executed (Fill on completion)

### Environment
- OS: Windows
- Backend/Runtime: Not applicable - Markdown governance framework

### Tests
| Test | Result | Evidence |
|---|---|---|
| `git diff --check` | Passed | No whitespace errors. Git reported LF-to-CRLF working-copy warnings only. |
| Custom structural scan | Passed | `CUSTOM STRUCTURAL SCAN: PASS`; Markdown files checked: 103; skill files checked: 14. |
| README wording check | Passed | `rg` confirmed optional publishing wording, instantiated-root wording, and recalibration disclaimer in Portuguese and English. |
| `git status --short` | Passed | Working tree contains expected documentation/governance changes from the current sequence. |

### Final Result
`approved`
