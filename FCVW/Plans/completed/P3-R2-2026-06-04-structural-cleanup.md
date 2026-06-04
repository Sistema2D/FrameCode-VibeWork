---
status: completed
priority: P3
risk: R2
current_version: "V0.7.6"
expected_version: "V0.7.7"
---

# P3-R2-2026-06-04-structural-cleanup

## Status
`completed`

## Goal
Fix architectural and structural flaws identified during global impartial analysis, enforcing the framework's stack-agnostic rule and ensuring declarative file tracking accuracy.

## Execution
- Moved the entire Node.js/Jest testing stack (`package.json`, `package-lock.json`, and `tests/`) from the root to `FCVW/docs/`, cleaning the root of non-markdown execution files.
- Deleted the obsolete `FCVW/pr_description.txt` artifact.
- Synchronized `FCVW/FILESYSTEM.md` to document the exact location of the Node.js files in `FCVW/docs/` and officially map the complete `refactoring-guide/` structure.

## Changes
- [MOVE] `package.json` -> `FCVW/docs/package.json`
- [MOVE] `package-lock.json` -> `FCVW/docs/package-lock.json`
- [MOVE] `tests/` -> `FCVW/docs/tests/`
- [DELETE] `FCVW/pr_description.txt`
- [MODIFY] `FCVW/FILESYSTEM.md` (Updated visual tree and role table)

## Acceptance Criteria
- Root contains only baseline files and directories expected by `FILESYSTEM.md`.
- Documentation test stack resides under `FCVW/docs/`.
- Obsolete transient artifacts are removed.

## Test Plan / Validation
- Manual directory listing verified that the root is now completely clean and strictly follows the documented `FILESYSTEM.md` baseline (contains only `AGENTS.md`, `README.md`, `docs/`, `FCVW/`, and hidden files/git).
- `FILESYSTEM.md` correctly maps `refactoring-guide/`.
