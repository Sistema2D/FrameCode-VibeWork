---
status: completed
priority: P4
risk: R1
current_version: "V0.7.6"
expected_version: "V0.7.7"
---

# P4-R1-2026-06-04-governance-history-fix

## Status
`completed`

## Goal
Sanitize the project's documentary and historical governance debt by resolving orphaned plans, missing templates, naming convention violations, and erroneous session logs discovered during the V2 impartial analysis.

## Execution
- Completed and archived the abandoned `P3-R2-2026-06-04-integrate-refactoring-guide.md` plan.
- Generated the 10 missing `TEMPLATE_REFACTORING_*.md` files in `FCVW/governance/`, replacing the monolithic old template and satisfying the refactoring guide dependencies.
- Renamed non-compliant plans (`plan_fix_xss.md`, `translation-fallback-tests.md`) to follow the mandatory `PLANNING.md` structure.
- Removed the orphan `S001.md` session draft and fixed the typographical year error in the `S006` session.
- Updated the `FILESYSTEM.md` declarative visual tree to account for the 10 new refactoring templates.

## Changes
- [MOVE/MODIFY] `FCVW/Plans/in_progress/P3-R2-2026-06-04-integrate-refactoring-guide.md` -> `completed/`
- [RENAME] `plan_fix_xss.md` -> `P1-R4-2026-06-01-fix-xss-vulnerability.md`
- [RENAME] `translation-fallback-tests.md` -> `P3-R2-2026-06-04-translation-fallback-tests.md`
- [RENAME] `S006-2024-06-01-fix-xss-vulnerability.md` -> `S006-2026-06-01-fix-xss-vulnerability.md`
- [DELETE] `FCVW/wiki/sessions/S001.md`
- [DELETE] `FCVW/governance/TEMPLATE_REFACTORING.md`
- [NEW] 10 files `FCVW/governance/TEMPLATE_REFACTORING_*.md`
- [MODIFY] `FCVW/FILESYSTEM.md`

## Acceptance Criteria
- Historical plan names follow the mandatory naming convention.
- Missing refactoring templates are present.
- Erroneous session draft and obsolete monolithic template are absent.

## Test Plan / Validation
- Manual directory check confirms `FCVW/governance/` now holds all 10 refactoring templates.
- Directory listing of `FCVW/Plans/completed/` confirms all plan names now strictly follow `P{Priority}-R{Risk}-{Date}-{Name}.md`.
- `in_progress` folder is empty.
