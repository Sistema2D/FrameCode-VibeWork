---
context_files:
  - AGENTS.md
  - README.md
  - FCVW/CONTEXT_MAP.md
  - FCVW/PLANNING.md
  - FCVW/TROUBLESHOOTING.md
  - FCVW/VERSIONING.md
  - FCVW/MANIFEST.md
  - FCVW/STACK.md
  - FCVW/README.md
  - FCVW/FILESYSTEM.md
  - FCVW/skills/README.md
  - FCVW/skills/aicc-compact/SKILL.md
  - FCVW/skills/agent-aegis/SKILL.md
  - FCVW/skills/agent-hephaestus/SKILL.md
  - FCVW/skills/agent-hermes/SKILL.md
  - FCVW/skills/memory-rotation/SKILL.md
  - FCVW/skills/obsidian-markdown/SKILL.md
  - FCVW/wiki/sessions/README.md
  - FCVW/wiki/index.md
  - FCVW/wiki/log.md
---
# P2-R2-2026-05-29-governance-state-reconciliation

- **Description:** Reconcile the repository governance state after structural audit findings.
- **Justification:** The current repository tag is `v0.7.5`, but official governance documents still reference older versions, the mandatory troubleshooting folder is absent, the root README lost its explanatory content in the working tree, and some skill metadata/links do not satisfy the active lint rules.
- **Objective:** Restore coherent project documentation and governance structure without changing application behavior.
- **Scope:**
  - Restore the root `README.md` documentation while preserving the updated operational routing flowchart.
  - Align current-version references in `FCVW/MANIFEST.md` and `FCVW/STACK.md` with `V0.7.5`.
  - Create the mandatory `FCVW/troubleshooting/` structure and record the confirmed governance drift issue.
  - Create minimal official baselines for referenced `FCVW/audits/`, `FCVW/briefings/`, and `FCVW/snippets/` directories.
  - Update skill catalog references in `FCVW/STACK.md`, `FCVW/README.md`, and `FCVW/CONTEXT_MAP.md` where they are demonstrably stale.
  - Fix broken skill links and explicit activation trigger headings in affected `SKILL.md` files.
  - Create the missing formal `FCVW/changelogs/V0.7.5.md` record for the current tagged version.
  - Record changelog and AICC session synthesis for this correction.
  - Do not change runtime source code, Git history, tags, or unrelated user changes.
- **Affected files:**
  - README.md
  - FCVW/MANIFEST.md
  - FCVW/STACK.md
  - FCVW/README.md
  - FCVW/CONTEXT_MAP.md
  - FCVW/FILESYSTEM.md
  - FCVW/skills/aicc-compact/SKILL.md
  - FCVW/skills/agent-aegis/SKILL.md
  - FCVW/skills/agent-hephaestus/SKILL.md
  - FCVW/skills/agent-hermes/SKILL.md
  - FCVW/skills/memory-rotation/SKILL.md
  - FCVW/skills/obsidian-markdown/SKILL.md
  - FCVW/audits/README.md
  - FCVW/briefings/README.md
  - FCVW/snippets/README.md
  - FCVW/snippets/tokens.css
  - FCVW/snippets/gallery.html
  - FCVW/troubleshooting/README.md
  - FCVW/troubleshooting/2026-05-29-governance-state-drift.md
  - FCVW/changelogs/V0.7.5.md
  - FCVW/changelogs/unreleased/P2-R2-2026-05-29-governance-state-reconciliation.md
  - FCVW/wiki/sessions/S002-2026-05-29-governance-state-reconciliation.md
  - FCVW/wiki/index.md
  - FCVW/wiki/log.md
- **Implementation plan:**
  1. Create this plan in `pending`, update it to `in_progress`, then move it to `Plans/in_progress/`.
  2. Create the missing troubleshooting directory and issue record for the confirmed governance drift.
  3. Create missing official directory baselines referenced by governance documents.
  4. Restore root README explanatory sections and keep the updated Mermaid routing flowchart.
  5. Align version fields and active skill catalogs with the current repository state.
  6. Fix broken internal skill links and explicit trigger-section formatting.
  7. Create the formal current-version changelog, plan changelog fragment, and AICC session synthesis.
  8. Run structural validations and update this plan with evidence before moving it to `completed`.
- **Acceptance criteria:**
  - [x] Root `README.md` keeps bilingual explanatory documentation and includes the updated routing flowchart.
  - [x] `FCVW/MANIFEST.md` and `FCVW/STACK.md` current-version fields match `V0.7.5`.
  - [x] `FCVW/troubleshooting/` exists and contains an index plus this issue record.
  - [x] `FCVW/audits/`, `FCVW/briefings/`, and `FCVW/snippets/` exist where official docs reference them.
  - [x] Skill inventory references match the actual directories under `FCVW/skills/`.
  - [x] `FCVW/changelogs/V0.7.5.md` exists and records the current tagged version.
  - [x] Internal Markdown link scan reports no unexpected broken links from modified files.
  - [x] All `SKILL.md` files expose explicit activation trigger information near the top.
  - [x] Changelog fragment and AICC session synthesis are created and indexed.
- **Test plan:**
  - [x] `git diff --check`
  - [x] Custom Markdown structural scan for required folders, tables, fences, links, skills, and version fields.
  - [x] `git status --short`
- **Priority:** `P2`
- **Risk:** `R2`
- **Current Version:** `V0.7.5`
- **Expected Version:** `V0.7.5`
- **Status:** `completed`
- **Creation Date:** 2026-05-29
- **Completion Date:** 2026-05-29
- **Technical observations:**
  - Pre-existing user/worktree changes are present in `README.md`, `FCVW/wiki/index.md`, `FCVW/wiki/log.md`, and the prior README-flowchart plan artifacts.
  - The repository `HEAD` is tagged `v0.7.5`, while governance documents still contain older current-version values.
  - `FCVW/changelogs/V0.7.5.md` was reconstructed from Git history because no prior formal changelog existed for the current tag.

## Validation Executed (Fill on completion)

### Environment
- OS: Windows
- Backend/Runtime: Not applicable - Markdown governance framework

### Tests
| Test | Result | Evidence |
|---|---|---|
| `git diff --check` | pass | Exit code 0. Output only line-ending warnings such as `LF will be replaced by CRLF the next time Git touches it`. |
| Custom Markdown structural scan | pass | `missingRequired: []`, `brokenLinkCount: 0`, `tableIssueCount: 0`, `skillTriggerIssues: []`, `manifestCurrent: true`, `stackCurrent: true`, `noEdgePlaceholders: true`. |
| `git status --short` | pass | Executed. Shows expected modified governance/docs files and untracked plan/changelog/wiki/baseline files from this and the previous README-flowchart work. |

### Final Result
`approved`
