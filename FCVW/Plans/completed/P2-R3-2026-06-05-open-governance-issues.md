---
context_files:
  - AGENTS.md
  - FCVW/PLANNING.md
  - FCVW/governance/TEMPLATE_PLAN.md
  - FCVW/AUDIT.md
  - FCVW/WORKFLOW.md
  - FCVW/REFACTORING.md
  - FCVW/AI.md
  - FCVW/wiki/README.md
  - FCVW/wiki/schema.md
  - FCVW/skills/agent-aegis/SKILL.md
  - FCVW/skills/agent-hephaestus/SKILL.md
  - FCVW/skills/agent-hermes/SKILL.md
  - FCVW/wiki/sessions/S009-2026-06-05-remove-framework-docs-artifacts.md
---
# P2-R3-2026-06-05-open-governance-issues

- **Description:** Treat GitHub issues #27, #28, and #29 by adding operational priority/risk rules, application-module documentation governance, and unified agent-journal wiki paths.
- **Justification:** The open issues identify governance gaps that affect future plan triage, application documentation consistency, and agent knowledge organization.
- **Objective:** Publish `V0.8.0` with explicit rules, templates, audit checks, and wiki structure for the three issues while preserving the `V0.7.9` removal of framework-owned documentation site artifacts.
- **Scope:**
  - Issue #28: make priority/risk classifications operationally active in planning, templates, audit, workflow, and refactoring references.
  - Issue #27: define application-owned module documentation rules and templates without recreating root `docs/` in the framework baseline.
  - Issue #29: define `FCVW/wiki/agents/<agent_name>_journal.md` as the official agent journal path and update existing agent skills.
  - Update version, changelog, filesystem tree, wiki index/log, and session synthesis.
  - Do not close GitHub issues remotely from this non-git local checkout.
- **Affected files:**
  - `AGENTS.md`
  - `README.md`
  - `FCVW/README.md`
  - `FCVW/PLANNING.md`
  - `FCVW/governance/TEMPLATE_PLAN.md`
  - `FCVW/governance/TEMPLATE_APP_DOCS_README.md`
  - `FCVW/governance/TEMPLATE_MODULE_DOCUMENTATION.md`
  - `FCVW/governance/TEMPLATE_FLOW_DOCUMENTATION.md`
  - `FCVW/APPLICATION_DOCUMENTATION.md`
  - `FCVW/AUDIT.md`
  - `FCVW/WORKFLOW.md`
  - `FCVW/REFACTORING.md`
  - `FCVW/AI.md`
  - `FCVW/SCOPE.md`
  - `FCVW/MANIFEST.md`
  - `FCVW/STACK.md`
  - `FCVW/FILESYSTEM.md`
  - `FCVW/wiki/README.md`
  - `FCVW/wiki/schema.md`
  - `FCVW/wiki/index.md`
  - `FCVW/wiki/log.md`
  - `FCVW/wiki/agents/README.md`
  - `FCVW/skills/agent-aegis/SKILL.md`
  - `FCVW/skills/agent-hephaestus/SKILL.md`
  - `FCVW/skills/agent-hermes/SKILL.md`
  - `FCVW/changelogs/V0.8.0.md`
  - `FCVW/wiki/sessions/S010-2026-06-05-open-governance-issues.md`
- **Implementation plan:**
  1. Move this plan to `Plans/in_progress/`.
  2. Implement the priority/risk operational matrix and plan template fields.
  3. Add application module documentation guide and reusable templates.
  4. Add agent journal wiki structure and update agent skill paths.
  5. Update official indexes, version fields, filesystem tree, changelog, and session synthesis.
  6. Validate removed docs baseline remains absent, links/fences/tables are valid, and issue acceptance terms are present.
  7. Complete this plan and move it to `Plans/completed/`.
- **Acceptance criteria:**
  - [x] `PLANNING.md` defines how priority and risk affect triage, validation, rollback, review, blocking, and decomposition.
  - [x] `TEMPLATE_PLAN.md` includes an operational score/decision field and rollback/review/decomposition gates.
  - [x] R4/R5 plans explicitly require rollback and expanded validation.
  - [x] High-risk low-priority plans are not automatically prioritized only because of risk score.
  - [x] Application module documentation rules exist without recreating framework-owned root `docs/`.
  - [x] Module and flow templates exist with Mermaid guidance and required fields.
  - [x] `AGENTS.md` and `AUDIT.md` require module documentation checks when relevant application modules change.
  - [x] `FCVW/wiki/agents/` exists with a README and the official journal path convention.
  - [x] Agent skills use `FCVW/wiki/agents/<agent_name>_journal.md`.
  - [x] Version fields and changelog are coherent for `V0.8.0`.
- **Test plan:**
  - [x] Confirm the three issue themes are represented in official docs and templates.
  - [x] Confirm `docs/`, `FCVW/docs/`, root package files, and root tests remain absent.
  - [x] Check Markdown code fences.
  - [x] Check internal Markdown links.
  - [x] Check Markdown tables.
  - [x] Check all `SKILL.md` files retain activation triggers.
  - [x] Record Git limitation.
- **Priority:** `P2`
- **Risk:** `R3`
- **Operational Score:** `P2-R3 => impact_weight 4 x risk_weight 3 = 12; high triage, moderate controls`
- **Review Gate:** `documentation/governance review`
- **Rollback Required:** `No; document-only changes, rollback by restoring V0.7.9 files`
- **Decomposition Required:** `No; three issues share the same governance surface and are validated together`
- **Application Module Documentation:** `not applicable; this plan changes framework governance rules and templates, not a downstream application module`
- **Current Version:** `V0.7.9`
- **Expected Version:** `V0.8.0`
- **Status:** `completed`
- **Creation Date:** 2026-06-05
- **Completion Date:** 2026-06-05
- **Technical observations:**
  - GitHub issues #27, #28, and #29 were rechecked on 2026-06-05 and remain open with no comments.
  - The local checkout has no `.git`; this plan cannot push, branch, tag, or close GitHub issues directly.

## Validation Executed (Fill on completion)

### Environment
- OS: Windows / PowerShell.
- Backend/Runtime: Not applicable; Markdown framework governance update only.

### Tests
| Test | Result | Evidence |
|---|---|---|
| Git metadata limitation | Pass with limitation | `git status --short` returned `fatal: not a git repository`, matching the known local checkout limitation. |
| Removed artifact baseline | Pass | `docs=False`; `FCVW\docs=False`; `package.json=False`; `package-lock.json=False`; `tests=False`. |
| Issue #28 governance coverage | Pass | `Operational Score`, `Review Gate`, `Rollback Required`, `Decomposition Required`, `R4`, `R5`, human approval, and high-risk low-priority rules were found in official governance files. |
| Issue #27 application documentation coverage | Pass | `FCVW/APPLICATION_DOCUMENTATION.md` and the three application documentation templates exist; app-owned `docs/` and Mermaid guidance are documented. |
| Issue #29 agent journal coverage | Pass | `FCVW/wiki/agents/README.md` exists; Aegis, Hephaestus, and Hermes skills point to `FCVW/wiki/agents/<agent_name>_journal.md`; old root journal path scan returned no matches. |
| Version coherence | Pass | Root README, framework manifest, stack file, changelog, and filesystem reference use `V0.8.0`. |
| Markdown code fences | Pass | `unclosed_fence_files=0`. |
| Internal Markdown links | Pass | `broken_internal_markdown_links=0`. |
| Markdown tables | Pass | `markdown_table_mismatches=0`. |
| Skill triggers | Pass | `skill_trigger_missing=0`. |

### Final Result
`approved`
