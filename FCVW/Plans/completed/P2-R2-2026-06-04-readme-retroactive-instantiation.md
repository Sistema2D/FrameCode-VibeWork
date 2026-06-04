---
context_files:
  - AGENTS.md
  - README.md
  - FCVW/CONTEXT_MAP.md
  - FCVW/INSTANTIATION.md
  - FCVW/MANIFEST.md
  - FCVW/SCOPE.md
  - FCVW/STACK.md
  - FCVW/skills/README.md
status: completed
priority: P2
risk: R2
current_version: "V0.7.7"
expected_version: "V0.7.8"
---

# P2-R2-2026-06-04-readme-retroactive-instantiation

- **Description:** Update the repository root README and add an autonomous retroactive-instantiation workflow for adopting FCVW in advanced applications or projects using older framework versions.
- **Justification:** The root README does not yet reflect the current post-refactoring framework scope or provide a clear path for retroactive adoption. Existing instantiation guidance focuses on new projects.
- **Objective:** Make retroactive framework adoption executable by an AI agent without human intervention, while preserving non-destructive merge rules and current governance traceability.
- **Scope:** Includes documentation, indexes, skill catalog, changelog, session synthesis, and filesystem map updates. It does not apply the retroactive process to any downstream application.
- **Affected files:**
  - `README.md`
  - `AGENTS.md`
  - `FCVW/README.md`
  - `FCVW/RETROACTIVE_INSTANTIATION.md`
  - `FCVW/CONTEXT_MAP.md`
  - `FCVW/FILESYSTEM.md`
  - `FCVW/INSTANTIATION.md`
  - `FCVW/MANIFEST.md`
  - `FCVW/SCOPE.md`
  - `FCVW/STACK.md`
  - `FCVW/changelogs/`
  - `FCVW/skills/README.md`
  - `FCVW/skills/retroactive-instantiation/SKILL.md`
  - `FCVW/wiki/index.md`
  - `FCVW/wiki/log.md`
  - `FCVW/wiki/sessions/`
- **Implementation plan:**
  1. Add a canonical retroactive-instantiation Markdown guide with autonomous AI execution rules.
  2. Add a JIT skill that points agents to the canonical guide when the task is retroactive adoption or framework migration.
  3. Refresh the root and framework READMEs to match the current framework scope, version, refactoring feature, docs structure, and retroactive-instantiation path.
  4. Update operational indexes and metadata so the new workflow is discoverable.
  5. Publish a patch changelog and session synthesis, then regenerate the filesystem map.
- **Acceptance criteria:**
  - [x] Root and framework READMEs reflect the current framework scope and recent refactoring feature.
  - [x] Retroactive-instantiation instructions are clear enough for autonomous AI execution.
  - [x] A skill exists for on-demand activation of the retroactive-instantiation workflow.
  - [x] Official indexes mention the new document and skill consistently.
  - [x] Version/changelog/session records are coherent.
  - [x] Validation evidence is recorded before closure.
- **Test plan:**
  - [x] Run internal Markdown link check.
  - [x] Run unclosed code fence check.
  - [x] Run targeted scans for `RETROACTIVE_INSTANTIATION`, `retroactive-instantiation`, and `V0.7.8`.
  - [x] Run `npm test -- --runInBand` in `FCVW/docs`.
  - [x] Confirm root/canonical docs HTML hash parity remains unchanged or record the reason if changed.
- **Priority:** `P2`
- **Risk:** `R2`
- **Current Version:** `V0.7.7`
- **Expected Version:** `V0.7.8`
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
| Internal Markdown links excluding dependency folders, `file://` examples, and placeholders | approved | `broken_links=0` |
| Markdown code fences excluding dependency folders | approved | `unclosed_fence_files=0` |
| Changelog release statuses | approved | `invalid_release_statuses=0` |
| Version coherence | approved | `MANIFEST.md`, `STACK.md`, `README.md`, and `FCVW/README.md` contain `V0.7.8` |
| Retroactive workflow discoverability | approved | `RETROACTIVE_INSTANTIATION.md` and `skills/retroactive-instantiation/SKILL.md` exist and are indexed |
| Documentation tests | approved | `Test Suites: 2 passed, 2 total`; `Tests: 10 passed, 10 total` |
| Root/canonical docs mirror | approved | `docs/index.html` and `FCVW/docs/index.html` share SHA256 `E4F028513B12BF7AB7E126F5215B2615C89967652D8BBE8977D99A3C2CEE3AC1` |
| Unreleased fragments | approved | only `FCVW/changelogs/unreleased/README.md` remains |

### Final Result
`approved`
