---
context_files:
  - AGENTS.md
  - FCVW/FILESYSTEM.md
  - FCVW/MANIFEST.md
  - FCVW/STACK.md
  - FCVW/VERSIONING.md
  - FCVW/DATA.md
  - FCVW/skills/aicc-compact/SKILL.md
  - FCVW/refactoring-guide/
  - FCVW/docs/tests/
status: completed
priority: P2
risk: R3
current_version: "V0.7.6"
expected_version: "V0.7.7"
---

# P2-R3-2026-06-04-global-consistency-corrections

- **Description:** Resolve the confirmed global audit inconsistencies across governance metadata, versioning, filesystem mapping, AICC references, refactoring-guide links, tests, and obvious encoding drift.
- **Justification:** The global audit found internal contradictions that reduce traceability and make autonomous agent execution unreliable.
- **Objective:** Restore coherence between official documents, physical files, plans, changelogs, tests, and session handoff records.
- **Scope:** Includes only confirmed consistency corrections from the audit. It does not recreate Git history or initialize a new repository.
- **Affected files:**
  - `AGENTS.md`
  - `FCVW/DATA.md`
  - `FCVW/FILESYSTEM.md`
  - `FCVW/MANIFEST.md`
  - `FCVW/STACK.md`
  - `FCVW/CONTEXT_MAP.md`
  - `FCVW/changelogs/`
  - `FCVW/Plans/completed/`
  - `FCVW/skills/aicc-compact/SKILL.md`
  - `FCVW/skills/README.md`
  - `FCVW/refactoring-guide/`
  - `FCVW/docs/package.json`
  - `FCVW/docs/tests/`
  - `FCVW/wiki/log.md`
  - `FCVW/wiki/sessions/`
- **Implementation plan:**
  1. Normalize release metadata and compile pending fragments into `V0.7.7`.
  2. Correct the AICC template source of truth and stale session references.
  3. Remove the baseline `FCVW/data/` contradiction from filesystem/data docs.
  4. Repair internal links after refactoring-guide file renames.
  5. Fix docs test paths and assertions after the `textContent` security fix.
  6. Correct visible mojibake in official guidance files.
  7. Regenerate `FILESYSTEM.md` tree and run validations.
- **Acceptance criteria:**
  - [x] Current version references are coherent.
  - [x] Changelog statuses use allowed values.
  - [x] No internal Markdown link points to a missing file.
  - [x] AICC session synthesis has one template source of truth.
  - [x] `FILESYSTEM.md` matches the current physical tree.
  - [x] Docs tests execute successfully or limitation is recorded.
- **Test plan:**
  - [x] Run internal Markdown link check.
  - [x] Run unclosed code fence check.
  - [x] Run targeted string scans for stale names and mojibake.
  - [x] Run `npm test -- --runInBand` in `FCVW/docs`.
  - [x] Confirm root and canonical docs HTML hashes still match.
- **Priority:** `P2`
- **Risk:** `R3`
- **Current Version:** `V0.7.6`
- **Expected Version:** `V0.7.7`
- **Status:** `completed`
- **Creation Date:** 2026-06-04
- **Completion Date:** 2026-06-04
- **Technical observations:**
  - `git status --short` cannot run because this directory is not currently a Git repository.

## Validation Executed

### Environment
- OS: Windows / PowerShell
- Runtime: Node.js / npm local dependencies under `FCVW/docs`
- Repository metadata: `git status --short` returned `fatal: not a git repository (or any of the parent directories): .git`

### Tests
| Test | Result | Evidence |
|---|---|---|
| Internal Markdown links excluding `node_modules` | approved | `broken_links=0` |
| Markdown code fences excluding `node_modules` | approved | `unclosed_fence_files=0` |
| Changelog release statuses | approved | `invalid_release_statuses=0` |
| Version coherence | approved | `manifest=V0.7.7`; `stack=V0.7.7`; `changelog_V0.7.7=True` |
| Unreleased fragments | approved | only `FCVW/changelogs/unreleased/README.md` remains |
| Documentation tests | approved | `Test Suites: 2 passed, 2 total`; `Tests: 10 passed, 10 total` |
| Root/canonical docs mirror | approved | `docs/index.html` and `FCVW/docs/index.html` share SHA256 `E4F028513B12BF7AB7E126F5215B2615C89967652D8BBE8977D99A3C2CEE3AC1` |

### Final Result
`approved`
