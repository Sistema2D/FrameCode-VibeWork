---
context_files: ["docs/index.html", "FCVW/docs/index.html", "FCVW/RELEASE.md"]
---
# P4-R1-2026-05-29-remove-duplicate-docs

- **Description:** Remove the duplicate `docs/index.html` file from the repository root.
- **Justification:** The framework documentation site artifact should live in `FCVW/docs/`. According to `FCVW/RELEASE.md` and `FCVW/audits/2026-05-29-framework-structure-audit.md`, the root `docs/` directory is not meant to be kept permanently in the framework baseline. It was added for GitHub Pages compatibility during `V0.7.x` sequence but is a duplicate and should be removed.
- **Objective:** Improve maintainability by keeping a single source of truth for the documentation (`FCVW/docs/index.html`) and adhering to the framework rules regarding the root `docs/` folder.
- **Scope:**
  - Remove `docs/index.html`.
  - Remove the root `docs/` directory.
- **Affected files:**
  - `docs/index.html`
- **Implementation plan:**
  1. Remove `docs/index.html`.
  2. Remove the `docs/` directory.
- **Acceptance criteria:**
  - [ ] `docs/index.html` and `docs/` directory are removed.
  - [ ] `FCVW/docs/index.html` remains intact.
- **Test plan:**
  - [ ] Run `ls -la docs` to confirm it no longer exists.
  - [ ] Run `ls -la FCVW/docs/index.html` to confirm it still exists.
- **Priority:** `P4` (Low)
- **Risk:** `R1` (Very Low)
- **Current Version:** `V0.7.5`
- **Expected Version:** `V0.7.6`
- **Status:** `completed`
- **Creation Date:** 2026-05-29
- **Completion Date:** 2026-06-02
- **Technical observations:**
  - The root `docs/` might be required by a GitHub Pages release process, but the current state is that we want to remove the static duplication to avoid code drift.

## Validation Executed (Fill on completion)

### Environment
- OS:
- Backend/Runtime:

### Tests
| Test | Result | Evidence |
|---|---|---|
| | | |

### Final Result
`approved` / `rejected`
### Tests
| Test | Result | Evidence |
|---|---|---|
| ls -la docs | passed | ls: cannot access 'docs': No such file or directory |
| ls -la FCVW/docs/index.html | passed | -rw-rw-r-- 1 jules jules 75272 Jun 2 16:11 FCVW/docs/index.html |

### Final Result
`approved`

## Execution Notes
Removed the duplicated root docs folder successfully.
