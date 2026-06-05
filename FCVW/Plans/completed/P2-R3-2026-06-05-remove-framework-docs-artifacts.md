---
context_files:
  - AGENTS.md
  - README.md
  - package.json
  - package-lock.json
  - docs/index.html
  - tests/translation.test.js
  - tests/autoDetectLanguage.test.js
  - FCVW/README.md
  - FCVW/FILESYSTEM.md
  - FCVW/RELEASE.md
  - FCVW/AUDIT.md
  - FCVW/MANIFEST.md
  - FCVW/STACK.md
  - FCVW/TESTS.md
  - FCVW/docs/index.html
---
# P2-R3-2026-06-05-remove-framework-docs-artifacts

- **Description:** Remove the framework documentation site artifacts from both root `docs/` and `FCVW/docs/`, and remove the obsolete root Node/Jest test harness that only targeted those artifacts.
- **Justification:** GitHub Pages publication is moving to another repository, and the framework baseline should remain a pure Markdown governance framework without maintained site artifacts or package lockfiles for removed HTML tests.
- **Objective:** Leave the framework without `docs/`, `FCVW/docs/`, `package.json`, `package-lock.json`, or root `tests/`, while keeping official documentation, changelog, and validation evidence coherent.
- **Scope:**
  - Remove root `docs/`.
  - Remove `FCVW/docs/`.
  - Remove root `package.json`, `package-lock.json`, and `tests/` because their only executable purpose is testing the removed HTML site.
  - Update official current-state documents that still describe the removed documentation site or obsolete Node/Jest harness.
  - Record the GitHub open-issues triage in the final user response, without modifying issues remotely.
  - Do not rewrite historical plans, changelogs, audits, or old session syntheses except where a current official document must stop requiring the removed artifacts.
- **Affected files:**
  - `README.md`
  - `package.json`
  - `package-lock.json`
  - `docs/index.html`
  - `tests/translation.test.js`
  - `tests/autoDetectLanguage.test.js`
  - `FCVW/README.md`
  - `FCVW/FILESYSTEM.md`
  - `FCVW/RELEASE.md`
  - `FCVW/AUDIT.md`
  - `FCVW/MANIFEST.md`
  - `FCVW/STACK.md`
  - `FCVW/changelogs/V0.7.9.md`
  - `FCVW/Plans/completed/P2-R3-2026-06-05-remove-framework-docs-artifacts.md`
  - `FCVW/wiki/log.md`
  - `FCVW/wiki/sessions/S009-2026-06-05-remove-framework-docs-artifacts.md`
  - `FCVW/pr_description.txt`
- **Implementation plan:**
  1. Move this plan to `Plans/in_progress/`.
  2. Remove `docs/`, `FCVW/docs/`, root `package.json`, root `package-lock.json`, and root `tests/`.
  3. Update official current-state documents and version fields to `V0.7.9`.
  4. Create `FCVW/changelogs/V0.7.9.md`.
  5. Create an AICC session synthesis and update `FCVW/wiki/log.md`.
  6. Run structural validations for removed paths, stale active references, Markdown fences, and internal links.
  7. Complete this plan with validation evidence and move it to `Plans/completed/`.
- **Acceptance criteria:**
  - [x] `docs/` does not exist.
  - [x] `FCVW/docs/` does not exist.
  - [x] Root `package.json` and `package-lock.json` do not exist.
  - [x] Root `tests/` does not exist.
  - [x] Current official documents no longer require a framework documentation site artifact.
  - [x] Version fields and changelog are coherent for `V0.7.9`.
  - [x] Validation evidence is recorded.
- **Test plan:**
  - [x] Confirm removed paths are absent.
  - [x] Search current official documents for stale active references to `FCVW/docs/`, root `docs/`, removed package files, and removed tests.
  - [x] Validate Markdown code fences and internal links.
  - [x] Record that `npm test` is intentionally not applicable after removing the Node/Jest harness.
- **Priority:** `P2`
- **Risk:** `R3`
- **Current Version:** `V0.7.8`
- **Expected Version:** `V0.7.9`
- **Status:** `completed`
- **Creation Date:** 2026-06-05
- **Completion Date:** 2026-06-05
- **Technical observations:**
  - The GitHub repository currently has three open issues: #27, #28, and #29, all without comments at inspection time.
  - Issue #27 should not be implemented by reintroducing a framework-owned root `docs/` into the baseline. The future treatment should define application-owned documentation rules and reusable templates without conflicting with this removal.
  - `package.json`, `package-lock.json`, and root `tests/` only support Jest tests that read `docs/index.html`; they have no remaining purpose once both documentation site artifacts are removed.

## Validation Executed (Fill on completion)

### Environment
- OS: Windows / PowerShell
- Backend/Runtime: Not applicable; Markdown framework baseline. Root Node/Jest harness removed by this plan.

### Tests
| Test | Result | Evidence |
|---|---|---|
| `git status --short` | limitation | `fatal: not a git repository (or any of the parent directories): .git` |
| Removed paths check | approved | `docs=False`; `FCVW\docs=False`; `package.json=False`; `package-lock.json=False`; `tests=False`; `FCVW\pr_description.txt=False` |
| Current-state stale docs scan | approved | No active requirement for `FCVW/docs/`, root `docs/`, root package files, or root tests remained in `README.md`, `FCVW/README.md`, `FCVW/RELEASE.md`, `FCVW/AUDIT.md`, `FCVW/MANIFEST.md`, `FCVW/STACK.md`, `FCVW/FILESYSTEM.md`, `FCVW/SCOPE.md`, or `FCVW/TESTS.md`; remaining matches are negative rules or historical records. |
| Version coherence | approved | `README.md`, `FCVW/MANIFEST.md`, `FCVW/STACK.md`, and `FCVW/changelogs/V0.7.9.md` contain `V0.7.9`. |
| Plan folder coherence | approved | `in_progress_count=0`; completed plan exists. |
| Markdown fences | approved | `unclosed_fence_files=0` |
| Internal Markdown links | approved | `broken_markdown_links=0` after ignoring deliberate template placeholders and external/file examples. |
| `npm test` | not applicable | Root `package.json`, `package-lock.json`, and `tests/` were removed because they only targeted the removed documentation site. |

### Final Result
`approved`
