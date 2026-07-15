---
schema: "fcvw/plan@2"
id: "P2-R3-2026-07-15-final-integrity-reading-routes-and-readme"
status: "completed"
priority: "P2"
risk: "R3"
created_at: "2026-07-15"
updated_at: "2026-07-15"
current_version: "V0.13.0"
expected_version: "V0.13.0"
owner: "framework-maintainer"
regression_contract: "required"
record_scope: "framework"
context_files:
  - "AGENTS.md"
  - "README.md"
  - "FCVW/CONTEXT_MAP.md"
  - "FCVW/TOKEN_BUDGET.md"
  - "FCVW/SCHEMAS.md"
  - "FCVW/MIGRATIONS.md"
  - "FCVW/AI.md"
  - "FCVW/TOKEN_BUDGET.md"
  - "FCVW/skills/governance-validator/SKILL.md"
  - "FCVW/skills/self-improvement/SKILL.md"
  - "FCVW/skills/release-checklist/SKILL.md"
---

# Final integrity, reading routes, and explanatory README

## Description

Perform a final framework integrity audit, close incomplete Markdown reading triggers and session routes, implement missing operational scenarios in the selective context map, and replace the root README with an adoption-oriented guide.

## Justification and objective

The deterministic validator is green, but the current context map routes mainly by broad domain. Three automation policies are not named in any reading route, and nine skill session types are not explicitly represented. This can make an agent skip a necessary contract even though the file exists. The README also presents features without fully explaining lifecycle, adoption modes, ownership, selective reading, validation profiles, and limitations.

## Scope

### Included

- Audit canonical documents, links, metadata, trigger statements, skill session types, and context routes.
- Expand `CONTEXT_MAP.md` with event cues, missing scenarios, mandatory cross-domain reads, long-document section routing, and session-type aliases.
- Extend the validator and its tests to reject orphan framework policies and unmapped skill session types.
- Make the operational index and clean-package root inventory deterministic.
- Implement the documented `incremental` legacy-baseline semantics instead of leaving validation profiles as aliases.
- Narrowly update `governance-validator` when its trigger/check contract is incomplete.
- Enrich root `README.md` in Portuguese with a useful English orientation section.
- Synchronize filesystem, FCVW index, framework release record, and plan evidence.

### Excluded

- New executable CI/provider configuration.
- Application runtime code or project-profile instantiation.
- Tag, push, artifact publication, or external release mutation.
- Broad rewriting of long domain policies when section-level routing is sufficient.

## Affected files or boundaries

- `README.md`, `AGENTS.md`, `FCVW/CONTEXT_MAP.md`, `FCVW/README.md`, `FCVW/FILESYSTEM.md`, and `FCVW/TOKEN_BUDGET.md`.
- `FCVW/AI.md`, `FCVW/MIGRATIONS.md`, `FCVW/SCHEMAS.md`, and `FCVW/governance/TEMPLATE_LEGACY_BASELINE.md`.
- `FCVW/skills/governance-validator/SKILL.md` and skill catalog only if required by the confirmed gap.
- `tools/validate_fcvw.py`, `tools/test_validate_fcvw.py`.
- `FCVW/framework-releases/V0.13.0.md` and this plan.

## Implementation plan

1. Inventory canonical policies, declared trigger phrases, skill session types, and current context routes.
2. Define a single event-to-document routing contract inside `CONTEXT_MAP.md` rather than adding another competing document.
3. Add missing operational scenarios and section-level loading guidance for long documents.
4. Add deterministic route-coverage validation and negative fixtures.
5. Apply the smallest justified skill trigger/check update through `self-improvement`.
6. Rewrite the README around purpose, lifecycle, adoption, ownership, selective reading, validation, regression, automation, releases, limitations, and navigation.
7. Run structural, semantic, trigger-coverage, contamination, and regression validation; update V0.13.0 and close.

## Acceptance criteria

- [x] Every root `framework_policy` Markdown document is cataloged and named by `AGENTS.md`, `CONTEXT_MAP.md`, or `FCVW/README.md`.
- [x] Every project profile is cataloged and every skill `session_types` value has an explicit route or alias in `CONTEXT_MAP.md`.
- [x] Hooks, watchers, and daemons have explicit reading triggers.
- [x] Dependency/toolchain, environment/deploy, documentation/file movement, architecture/interface, test/QA, Git/repository, incident/containment, and closeout/handoff scenarios are routed.
- [x] Long policies have section-level selective-loading guidance that avoids unnecessary full reads.
- [x] Validator tests fail when a framework policy, operational-index entry, or skill session type becomes orphaned.
- [x] `incremental` accepts only an exact, unexpired baseline and `strict` never accepts one.
- [x] Root README explains the framework sufficiently for evaluation, adoption, daily use, upgrade, and validation.
- [x] Clean-template validator and all regression tests pass with no findings.
- [x] V0.13.0 remains coherent and explicitly `in_preparation`.

## Regression impact

### Existing behaviors that may be affected

- Selective context loading and token consumption.
- Skill activation and session classification.
- Governance validator success criteria.
- README quick-start paths and release-state presentation.
- Compatibility with existing skill metadata and legacy plan records.

### Regression contracts consulted

- `AGENTS.md` — instruction entrypoint and required change flow.
- `CONTEXT_MAP.md` — current routing source of truth.
- `TOKEN_BUDGET.md` — selective loading and context discipline.
- `SCHEMAS.md` — canonical ownership and skill metadata.
- `governance-validator` and `self-improvement` — validation and skill-change gates.

### Regression checks required

- [x] Existing clean-template validator remains green.
- [x] Existing validator regression tests remain green.
- [x] New orphan-policy, incomplete-index, unmapped-session, root-contamination, and legacy-baseline fixtures fail as intended.
- [x] All README and context-map Markdown links resolve.
- [x] No route requires full wiki/history loading by default.
- [x] Application contamination and stale-skill scans remain empty.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Clean structural validation | pass | clean-template: 0 errors, 0 findings |
| Reading route and operational-index coverage | pass | 25 policies and 21 skills; deterministic validator checks |
| Negative governance fixtures | pass | 14-test suite covers route, index, contamination, regression, skill, and baseline failures |
| Token-selective routing preserved | pass | cumulative event triggers plus section-level routes; no default archive/full-wiki load |
| README navigation resolves | pass | validator Markdown reference check |
| Legacy baseline safety | pass | exact matching, changed-message blocking, expiry, stale warning, and non-baselineable configuration errors |

### Limitations and residual risk

- The framework can validate declared routes structurally, but it cannot force an arbitrary external agent to read a file; adapters must honor `AGENTS.md`.
- No valid Git worktree is available for diff or publication evidence.

## Validation plan

- `python -m py_compile tools/validate_fcvw.py tools/test_validate_fcvw.py`.
- `python tools/test_validate_fcvw.py`.
- `python tools/validate_fcvw.py --root . --profile clean-template`.
- Canonical-policy and skill-session route inventory.
- Application residue, provider term, stale skill, and comparison-fixture scans.
- Physical path and version/release-state checks.

## Rollback

Restore the previous V0.13.0 documentation and validator from a verified framework artifact. If route validation proves too strict, remove only the new deterministic route rules while keeping the expanded human-readable context map and README.

## Gates and approvals

- Regression gate: required.
- Skill improvement gate: required only for confirmed `governance-validator` drift.
- Release gate: update the in-preparation framework record; do not publish.
- Decomposition: one coherent documentation/validator contract; no application work.

## Related records

- Framework release: `FCVW/framework-releases/V0.13.0.md`.
- Prior plans: `P1-R4-2026-07-15-fcvw-clean-framework-reconstruction`, `P2-R4-2026-07-15-regression-guardrails-and-fixture-removal`.

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Baseline validator suite | pass | initial 6 tests; clean-template 0 errors and 0 findings |
| Initial reading-route inventory | fail, corrected | 3 orphan policies and 9 unmapped skill session types identified before remediation |
| Final validator suite | pass | 14 tests passed |
| Final clean-template validation | pass | 0 errors, 0 findings, 0 baseline acceptances |
| Final inventory | pass | 25 policies, 21 skills, 0 non-Markdown FCVW files, comparison fixture absent |
| Provider/application residue review | pass | 0 provider terms in skill bodies; only generic localhost example in reusable environment template |

## Gaps and residual risk

- Markdown routes cannot force an arbitrary external runtime to comply; provider bridges only redirect to `AGENTS.md`.
- No valid Git worktree is available, so diff, commit, tag, checksum, and publication evidence remain unavailable. V0.13.0 stays `in_preparation`.

## Skill/Agent Self-Improvement Gate

- Skill loaded: `skills/self-improvement/SKILL.md`.
- Asset changed: `skills/governance-validator/SKILL.md` and its catalog entry.
- Evidence: the skill omitted policy-route/index validation triggers and its documented `incremental` baseline behavior was not implemented by the optional validator.
- Metric passed: rule drift and validation gap.
- Scope preserved: the skill remains a governance validator; no application-runtime or auto-remediation responsibility was added.
- Token/risk ROI: deterministic route and exact-baseline checks prevent silent under-reading and hidden new debt with a small standard-library implementation.
- Validation replay: 14 focused tests plus clean-template validation.
- Decision: `patch`.

## Status

`completed`
