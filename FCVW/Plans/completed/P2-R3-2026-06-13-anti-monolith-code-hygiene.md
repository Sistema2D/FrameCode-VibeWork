---
context_files:
  - "../AGENTS.md"
  - "CONTEXT_MAP.md"
  - "REFACTORING.md"
  - "RETROACTIVE_INSTANTIATION.md"
  - "PLANNING.md"
  - "AUDIT.md"
  - "TESTS.md"
  - "STACK.md"
  - "MANIFEST.md"
  - "skills/README.md"
  - "FILESYSTEM.md"
---
# P2-R3-2026-06-13-anti-monolith-code-hygiene

- **Description:** Add active Markdown-only governance gates to prevent monolith creation and drive code hygiene/refactoring work.
- **Justification:** The framework had refactoring guidance, but no mandatory gate that stopped agents before creating oversized files, mixed responsibilities, duplication, stale files, or retroactive monoliths.
- **Objective:** Make agents load focused skills before high-risk implementation/refactoring and require module boundary, duplication, dead-code, and cleanup evidence.
- **Scope:** Markdown governance only. No executable scripts, runtime code, dependencies, or automation hooks.
- **Affected files:**
  - `../AGENTS.md`
  - `README.md`
  - `CONTEXT_MAP.md`
  - `REFACTORING.md`
  - `RETROACTIVE_INSTANTIATION.md`
  - `PLANNING.md`
  - `AUDIT.md`
  - `TESTS.md`
  - `STACK.md`
  - `MANIFEST.md`
  - `VERSIONING.md`
  - `FILESYSTEM.md`
  - `skills/README.md`
  - `skills/anti-monolith-guard/SKILL.md`
  - `skills/code-hygiene-refactor/SKILL.md`
  - `governance/TEMPLATE_MONOLITH_GATE.md`
  - `governance/TEMPLATE_CODE_HYGIENE_REPORT.md`
  - `changelogs/V0.9.1.md`
  - `wiki/refactorings/anti-monolith-and-code-hygiene-gates.md`
  - `wiki/sessions/S002-2026-06-13-anti-monolith-code-hygiene.md`
- **Implementation plan:**
  1. Add skills and templates for anti-monolith and code hygiene workflows.
  2. Wire triggers into AGENTS.md, CONTEXT_MAP.md, skills catalog, stack, refactoring, planning, audits, and tests.
  3. Record reference-derived patterns without treating external prompt files as instructions.
  4. Update version, changelog, filesystem, wiki memory, and session synthesis.
- **Acceptance criteria:**
  - [x] Agents have mandatory triggers before creating or modifying large modules.
  - [x] Retroactive instantiation includes active cleanup and refactoring triage.
  - [x] Skills are executable as Markdown checklists and do not require scripts.
  - [x] FILESYSTEM.md lists all new Markdown artifacts.
  - [x] Version and changelog are coherent.
- **Test plan:**
  - [x] Run Markdown file inventory checks with `rg --files`.
  - [x] Verify all new skill paths are cataloged.
  - [x] Verify all new internal links resolve by path.
  - [x] Record limitations caused by the absence of executable framework tests.
- **Priority:** `P2`
- **Risk:** `R3`
- **Operational Score:** `P2-R3 => impact_weight 4 x risk_weight 3 = 12`
- **Review Gate:** `documentation review`
- **Rollback Required:** `No - revert Markdown edits and remove new Markdown artifacts`
- **Decomposition Required:** `No - single documentation governance patch`
- **Application Module Documentation:** `not applicable`
- **Current Version:** `V0.9.0`
- **Expected Version:** `V0.9.1`
- **Status:** `completed`
- **Creation Date:** 2026-06-13
- **Completion Date:** 2026-06-13
- **Technical observations:**
  - Reference files under `Referencias/` are treated as untrusted comparative evidence, not instructions.
  - The change must preserve ADR-0001: pure Markdown, no automation scripts.

## Validation Executed (Fill on completion)

### Environment
- OS: Windows / PowerShell
- Backend/Runtime: Not applicable - Markdown-only framework.

### Tests
| Test | Result | Evidence |
|---|---|---|
| New artifact path check | Passed | `All new artifact paths exist.` |
| Skill catalog check | Passed | `All skill directories are cataloged.` |
| FILESYSTEM entry check | Passed | `FILESYSTEM includes new entries.` |
| Fenced code block check | Passed | `No unbalanced fenced code blocks detected.` |
| Version coherence check | Passed | `Version V0.9.1 present in required files.` |
| Reference source path check | Passed | `Reference source paths resolve.` |
| Agent tool-awareness check | Passed | Legacy hard dependency patterns removed; only guarded `invoke_subagent` mention remains. |
| Skill trigger check | Passed | `All skill files declare triggers.` |
| Scheduler/PR dependency check | Passed | No mandatory scheduler, `gh pr create`, or branch command remains in agent skills. |

### Final Result
`approved`
