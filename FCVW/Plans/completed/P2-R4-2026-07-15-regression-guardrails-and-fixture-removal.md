---
schema: "fcvw/plan@2"
id: "P2-R4-2026-07-15-regression-guardrails-and-fixture-removal"
status: "completed"
priority: "P2"
risk: "R4"
created_at: "2026-07-15"
updated_at: "2026-07-15"
current_version: "V0.13.0"
expected_version: "V0.13.0"
owner: "framework-maintainer"
regression_contract: "required"
record_scope: "framework"
context_files:
  - "AGENTS.md"
  - "FCVW/PLANNING.md"
  - "FCVW/TESTS.md"
  - "FCVW/GOVERNANCE_GATES.md"
  - "FCVW/WATCHERS.md"
  - "FCVW/wiki/schema.md"
  - "FCVW/skills/governance-validator/SKILL.md"
  - "FCVW/skills/wiki-lint/SKILL.md"
  - "FCVW/skills/release-checklist/SKILL.md"
---

# Regression guardrails and comparison-fixture removal

## Description

Remove the production-derived comparison directory from the project root and implement the regression-governance issue as a coherent framework contract.

## Justification and objective

The comparison fixture has already served its migration purpose and now creates distribution and context-contamination risk. The framework also lacks a single mandatory contract proving both new behavior and preservation of protected behavior. The outcome is a self-contained clean template with explicit, risk-proportional regression gates and executable structural validation.

## Scope

### Included

- Delete `FCVW - Exemplo retirado de aplicação real/` after exact path verification.
- Add `REGRESSION_GUARDS.md`, regression plan requirements, gate, watchers, risk matrix, wiki category, and templates.
- Extend the optional validator with deterministic regression-contract and clean-root checks.
- Remove application-specific testing instructions still present in framework policy.
- Synchronize navigation, schemas, filesystem, migration, and the in-preparation framework release record.

### Excluded

- Application runtime test implementation.
- CI provider configuration, merge protection, tag, push, or external publication.
- Rewriting completed legacy plans to the new regression body contract.

## Affected files or boundaries

- Project root comparison directory and `AGENTS.md`.
- FCVW regression, planning, tests, gates, watchers, schemas, context, filesystem, wiki, templates, and release records.
- `tools/validate_fcvw.py`.

## Implementation plan

1. Record pre-deletion inventory and verify the removal target is exactly inside the workspace root.
2. Delete only the named comparison directory and verify absence.
3. Implement the issue's policy, plan, gate, test, watcher, history, and agent requirements.
4. Add structural checks that prevent reintroduction and empty regression sections.
5. Audit remaining framework content for application-specific residue, placeholders outside permitted roles, broken links, inconsistent schemas, and version drift.
6. Update the V0.13.0 in-preparation release record and close the plan after validation.

## Acceptance criteria

- [x] The comparison directory is absent and the clean-root guard rejects its reintroduction.
- [x] `FCVW/REGRESSION_GUARDS.md` defines regression types, evidence, blocking conditions, exceptions, and relationships.
- [x] New plans must include a non-empty Regression Impact section or explicit not-applicable justification.
- [x] Governance gate, testing risk matrix, and watcher events cover functional, visual, data, security, AI, workflow, and documentation regression.
- [x] `FCVW/wiki/regressions/` and a schema-aligned regression template exist without fabricating a historical incident.
- [x] Agent instructions require preservation evidence before completion.
- [x] Application-specific test commands are removed from the reusable framework policy.
- [x] Clean-template validation passes with no findings.
- [x] Framework release, filesystem, navigation, schemas, and migration notes are synchronized.

## Regression impact

### Existing behaviors that may be affected

- Clean-template validation and required-path checks.
- Plan completion rules and compatibility with legacy completed plans.
- Wiki page validation and clean-template contamination rules.
- Framework release content and distribution boundary.

### Regression contracts consulted

- `PLANNING.md`, `TESTS.md`, `GOVERNANCE_GATES.md`, `WATCHERS.md`, `SCHEMAS.md`, `OWNERSHIP.md`, and the issue supplied by the user.

### Regression checks required

- Structural validator positive run on the clean template.
- Negative fixtures for missing/empty Regression Impact and forbidden comparison directory.
- Markdown link and fence validation.
- Scan for application-specific residue and forbidden provider terms.
- Version/release namespace validation.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Clean template still validates | pass | `python tools/validate_fcvw.py --root . --profile clean-template`: 0 errors, 0 findings |
| Legacy completed plan remains accepted | pass | prior `fcvw/plan@1` record included in the clean-template validation |
| Empty new regression block is rejected | pass | `test_missing_regression_section_fails` |
| Comparison directory reintroduction is rejected | pass | `test_comparison_fixture_in_root_fails_clean_profile` |
| Rollback remains documented | pass | this plan and `framework-releases/V0.13.0.md` |

### Limitations and residual risk

- No valid Git worktree is available; structural, content, and temporary-fixture checks must provide the regression evidence for this framework-only change.

## Validation plan

- `python -m py_compile tools/validate_fcvw.py`.
- `python tools/validate_fcvw.py --root . --profile clean-template`.
- Isolated temporary-tree negative tests for new deterministic rules.
- Repository scans for stale application references, broken ownership, and disallowed histories.
- Physical verification that the deleted directory no longer exists.

## Rollback

Restore the comparison data only from the user-controlled original source, outside the framework project. Revert policy changes from a verified pre-change framework artifact; do not recreate production-derived files from memory.

## Gates and approvals

- Destructive gate: passed by the user's explicit request to remove the named directory; exact path still requires verification.
- Regression gate: required before completion.
- Release gate: V0.13.0 remains `in_preparation`; no publication authority inferred.
- Skill gate: `self-improvement` required for the narrow stale-reference correction in `project-instantiation`.

## Related records

- Framework release: `FCVW/framework-releases/V0.13.0.md`.
- Source issue: user-provided “Strengthen Regression Guardrails / Fortalecer guardrails contra regressões”.
- Prior plan: `P1-R4-2026-07-15-fcvw-clean-framework-reconstruction`.

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Pre-change governance and issue review | pass | applicable policies and three JIT skills read completely |
| Exact-path removal | pass | 1,099 files, 55 directories, 3,278,999 bytes; no reparse points; target absent afterward |
| Python syntax | pass | `python -m py_compile tools/validate_fcvw.py tools/test_validate_fcvw.py` |
| Validator regression suite | pass | 6 tests, including positive/negative plan, clean-root, and skill-contract fixtures |
| Clean-template profile | pass | 0 errors and 0 findings |
| Application contamination scan | pass | 0 application commands, changelogs, non-framework plans, and non-Markdown FCVW artifacts |
| Skill drift/provider scan | pass | 0 obsolete session/journal/publication/vendor terms; all 21 skills satisfy the eight body concepts |
| Canonical metadata and references | pass | all root FCVW documents have schema/role/owner/upgrade metadata; validator links and fences pass |

## Gaps and residual risk

- No valid Git worktree is currently available, so Git diff, commit, tag, artifact checksum, and publication checks remain unavailable. V0.13.0 correctly remains `in_preparation`.

## Skill/Agent Self-Improvement Gate

- Skill loaded: `skills/self-improvement/SKILL.md`
- Asset changed: 15 existing skills: `agent-aegis`, `agent-factory`, `agent-hephaestus`, `agent-hermes`, `aicc-compact`, `anti-monolith-guard`, `code-hygiene-refactor`, `git-conventional-commits`, `obsidian-markdown`, `orchestrator`, `project-instantiation`, `release-checklist`, `retroactive-instantiation`, `self-improvement`, and `wiki-curator`.
- Evidence: clean-template and wiki identity rules had drifted from fixed journal/example references; the Git skill required obsolete sequential sessions, hardcoded versions, mixed release assumptions, and external publication without a distinct authority gate; several bodies also omitted one or more concepts required by `fcvw/skill@1`.
- Metric passed: rule drift and validation gap.
- Scope preserved: each edit retains its existing responsibility; the Git rewrite narrows external actions and delegates release decisions to `release-checklist`.
- Token/risk ROI: prevents searches for a deleted fixture, concurrent wiki overwrites, namespace mistakes, and unauthorized publication without broadening responsibilities.
- Validation replay: provider/residue scan, clean-template validator, enforced eight-concept skill contract, and validator regression tests.
- Decision: `patch`
