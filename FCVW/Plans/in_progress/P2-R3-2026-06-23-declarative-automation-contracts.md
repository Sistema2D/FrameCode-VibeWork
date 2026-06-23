---
context_files:
  - "AGENTS.md"
  - "FCVW/PLANNING.md"
  - "FCVW/decisions/ADR-0001-pure-markdown-over-automation-scripts.md"
  - "FCVW/CONTEXT_MAP.md"
  - "FCVW/STACK.md"
  - "FCVW/MANIFEST.md"
  - "FCVW/FILESYSTEM.md"
  - "FCVW/AI.md"
  - "FCVW/SECURITY.md"
  - "FCVW/WORKFLOW.md"
  - "FCVW/skills/governance-validator/SKILL.md"
  - "FCVW/skills/wiki-lint/SKILL.md"
  - "FCVW/skills/agent-factory/SKILL.md"
  - "FCVW/skills/self-improvement/SKILL.md"
---
# P2-R3-2026-06-23-declarative-automation-contracts

- **Description:** Add Markdown-only declarative automation contracts for pseudo-hooks, watcher rules, daemon loops, and governance gates while preserving ADR-0001's pure Markdown baseline.
- **Justification:** The framework already depends on manual/agentic validation loops, but recurring maintenance risks such as filesystem drift, missing changelogs, plan-state mismatch, wiki lint gaps, and unsafe interpretation of automation terminology need explicit operational contracts without introducing executable automation.
- **Objective:** Provide clear Markdown contracts that let humans and AI agents reason about hooks, watchers, daemons, and gates without adding scripts, installed Git hooks, package dependencies, CI/CD workflows, or background processes.
- **Scope:**
  - Included:
    - Create declarative automation official documents.
    - Create reusable Markdown templates for future contracts.
    - Add an ADR clarifying that automation remains Markdown-only in Scenario 1.
    - Update central navigation, stack, manifest, workflow, AI, security, filesystem, and validation skills.
    - Credit SantanderAI as architectural inspiration where applicable.
  - Excluded:
    - No executable scripts.
    - No installed Git hooks.
    - No local daemons or watchers.
    - No package manifest or dependency setup.
    - No CI/CD or GitHub Actions workflows.
    - No API-key or CLI-provider integration.
- **Affected files:**
  - `FCVW/decisions/ADR-0002-declarative-automation-contracts.md`
  - `FCVW/AUTOMATION.md`
  - `FCVW/HOOKS.md`
  - `FCVW/WATCHERS.md`
  - `FCVW/DAEMONS.md`
  - `FCVW/GOVERNANCE_GATES.md`
  - `FCVW/governance/TEMPLATE_AUTOMATION_CONTRACT.md`
  - `FCVW/governance/TEMPLATE_HOOK_CHECK.md`
  - `FCVW/governance/TEMPLATE_WATCHER_RULE.md`
  - `FCVW/governance/TEMPLATE_DAEMON_LOOP.md`
  - `FCVW/governance/TEMPLATE_GOVERNANCE_GATE_REPORT.md`
  - `AGENTS.md`
  - `FCVW/CONTEXT_MAP.md`
  - `FCVW/STACK.md`
  - `FCVW/MANIFEST.md`
  - `FCVW/WORKFLOW.md`
  - `FCVW/AI.md`
  - `FCVW/SECURITY.md`
  - `FCVW/FILESYSTEM.md`
  - `FCVW/skills/governance-validator/SKILL.md`
  - `FCVW/skills/wiki-lint/SKILL.md`
  - `FCVW/skills/README.md`
  - `FCVW/changelogs/unreleased/P2-R3-2026-06-23-declarative-automation-contracts.md`
- **Implementation plan:**
  1. Create ADR-0002 to clarify Markdown-only automation contracts.
  2. Create official declarative automation documents.
  3. Create reusable governance templates for contract expansion.
  4. Update navigation and central framework documents.
  5. Patch existing validation skills rather than creating a new skill.
  6. Update filesystem source of truth and changelog fragment.
  7. Validate that no executable automation was introduced and that internal references are coherent.
- **Acceptance criteria:**
  - [ ] New automation documents clearly state they are Markdown-only contracts.
  - [ ] SantanderAI credit is recorded as inspiration, not as copied code.
  - [ ] No executable scripts, installed hooks, package files, daemons, CI workflows, or dependencies are introduced.
  - [ ] `AGENTS.md` and `CONTEXT_MAP.md` expose the new session type and loading path.
  - [ ] `STACK.md` and `MANIFEST.md` preserve the pure Markdown baseline.
  - [ ] `SECURITY.md` and `AI.md` prevent executable interpretation of automation contracts.
  - [ ] `FILESYSTEM.md` lists all new files.
  - [ ] Validation skills cover declarative automation integrity.
  - [ ] Changelog fragment exists.
- **Test plan:**
  - [ ] Manual governance review against ADR-0001 and ADR-0002.
  - [ ] Manual search for prohibited executable artifacts: `scripts/`, `.githooks/`, `.github/workflows/`, `package.json`, `pyproject.toml`, executable hook files.
  - [ ] Manual link/reference review of new documents.
  - [ ] Manual verification that new files appear in `FILESYSTEM.md`.
  - [ ] Manual validation that skill changes use existing self-improvement gate rather than uncontrolled skill creation.
- **Priority:** `P2`
- **Risk:** `R3`
- **Operational Score:** `P2-R3 => impact_weight 4 x risk_weight 3 = 12`
- **Review Gate:** `documentation review`
- **Rollback Required:** `Yes - revert the new declarative automation documents, templates, ADR-0002, changelog fragment, and all references added to central documents.`
- **Decomposition Required:** `No - the change is documentation-only and has a single validation path, but it is split internally by document family.`
- **Application Module Documentation:** `not applicable`
- **Current Version:** `V0.11.0`
- **Expected Version:** `V0.12.0`
- **Status:** `in_progress`
- **Creation Date:** 2026-06-23
- **Completion Date:** Not applicable.
- **Technical observations:**
  - Scenario 1 preserves ADR-0001 by using Markdown-only operational contracts.
  - SantanderAI repositories are credited only as architectural inspiration for loop, vault/lint, and gate patterns; no code is copied.

## Agent/Skill Creation Gate

- Skill loaded: `skills/agent-factory/SKILL.md`
- Proposed asset: dedicated declarative automation skill
- Asset type: `skill`
- Evidence of recurrence: automation-related governance risks recur across filesystem validation, wiki lint, release checks, and plan-state coherence.
- Existing coverage checked: `governance-validator`, `wiki-lint`, `release-checklist`, `agent-factory`, and `self-improvement` already cover most execution logic.
- Token ROI: a new skill may reduce future loading later, but initial evidence does not yet prove a dedicated skill is better than official documents plus existing skills.
- Risk ROI: risk reduction is achieved by official contract documents and patches to existing validators.
- Scope boundary: one trigger family, but overlaps existing validation skills.
- Validation task: use this implementation as the representative task.
- Decision: `defer`

## Skill/Agent Self-Improvement Gate

- Skill loaded: `skills/self-improvement/SKILL.md`
- Asset changed: `skills/governance-validator/SKILL.md`, `skills/wiki-lint/SKILL.md`, and `skills/README.md`
- Evidence: new official automation contract documents create a rule drift where validators would otherwise miss Markdown-only automation integrity.
- Metric passed: `Rule drift` and `Validation gap`.
- Scope preserved: patches add checks for the new official documents without broadening the skills into runtime automation tools.
- Token/risk ROI: reduces risk of agents interpreting hook/watcher/daemon terminology as executable automation.
- Validation replay: verify that new documents exist, are listed, and explicitly prohibit scripts, installed hooks, daemons, and CI/CD.
- Decision: `patch`

## Validation Executed (Fill on completion)

### Environment
- OS: GitHub repository edit via connector
- Backend/Runtime: Not applicable — Markdown-only documentation change

### Tests
| Test | Result | Evidence |
|---|---|---|
| ADR consistency review | pending | Pending completion |
| Prohibited artifact review | pending | Pending completion |
| Filesystem listing review | pending | Pending completion |
| Link/reference review | pending | Pending completion |
| Skill gate review | pending | Pending completion |

### Final Result
`pending`
