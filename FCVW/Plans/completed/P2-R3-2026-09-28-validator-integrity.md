---
schema: "fcvw/plan@2"
id: "P2-R3-2026-09-28-validator-integrity"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P2"
risk: "R3"
created_at: "2026-09-28"
updated_at: "2026-09-28"
current_version: "V0.19.0"
expected_version: "V0.19.1"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "FCVW/PLANNING.md"
  - "FCVW/REGRESSION_GUARDS.md"
  - "FCVW/SCHEMAS.md"
  - "FCVW/TESTS.md"
depends_on: []
---

# Validator integrity fixes

## Description

Close validator loopholes and false positives found by the repository analysis: backlog items B-01, B-02, A-02, A-03, A-04, A-09 and G-04 of the source-only maintainer backlog (`TODO.md` at the source repository root, not installed). The source allowlist also accepts the source-only `TODO.md`.

## Justification and objective

Reproduced defects: an active `fcvw/plan@1` P1-R5 plan without regression impact or rollback passed with zero findings; `--since` reported zero errors after a deleted file left three broken referrers; duplicated dictionary keys dropped localized headings. The objective is that each loophole produces a finding and that prose mentioning "pending" no longer blocks completion.

## Scope

### Included

- `fcvw/plan@1` only in `completed/` and `discontinued/`.
- Troubleshooting records must declare their schema.
- Repository-wide findings selected by rule family prefix; untracked Markdown joins the `--since` scope.
- Merged `LOCALIZED_TITLES` entries and a standard-library duplicate-key test for every tool.
- "pending" blocks completion only as a recorded result.
- `record_scope` in both plan templates.
- `TODO.md` accepted as a source-only root entry and excluded from installed payloads.

### Excluded

- Removal of translation dictionaries from source (F-04) and declarative record schemas (E-01).

## Affected files or boundaries

`tools/validate_fcvw.py`, `tools/test_validate_fcvw.py`, `tools/path_policy_fcvw.py`, `tools/release_layout_fcvw.py`, `FCVW/governance/TEMPLATE_PLAN.md`, `FCVW/governance/TEMPLATE_PLAN_COMPACT.md`.

## Implementation plan

1. Add the legacy-state rule, the troubleshooting schema finding and the pending-result pattern.
2. Replace the exact repository-wide list with a helper and prefixes; list untracked files.
3. Merge duplicated keys and add the static test.
4. Prove the new tests fail on V0.19.0 and pass now; replay both original reproductions.

## Proportionality gate

Not applicable — edits inside the existing validator and tests; one small helper replaces a drifting list.

## Acceptance criteria

- [x] Active legacy plans, schema-less troubleshooting records and cross-file findings of unchanged files are reported.
- [x] Historical legacy plans and prose mentions of pending remain valid.
- [x] No tool contains duplicate constant dictionary keys.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

Validation of the 17 historical plans, `--since` output size, existing pending-result detection, compact-plan sections, root allowlist and release payload mapping.

### Regression contracts consulted

- [Planning](../../PLANNING.md) — legacy plans remain readable.
- [Regression guards](../../REGRESSION_GUARDS.md) — pending results block completion.
- [Tests](../../TESTS.md) — `--since` keeps repository-wide rules.

### Regression checks required

- [x] Existing validator suites, including the table-cell pending fixture.
- [x] New negative fixtures fail on V0.19.0.
- [x] Clean-template governance of the repository and installed smoke.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| New fixtures | pass | `PhaseOneIntegrityTests` and `StaticIntegrityTests`: 9 tests |
| Guardrail proof | pass | 7 of those tests fail against the V0.19.0 validator; the 2 preservation tests pass on both |
| Deleted-file replay | pass | `--since HEAD~1` after deleting a linked record: 3 errors (was 0) |
| Legacy-plan replay | pass | active P1-R5 `plan@1` fixture: `plan-schema` error (was 0 findings) |
| Governance | pass | `validate_fcvw.py --profile clean-template`: 0 findings |

### Limitations and residual risk

- Downstream projects with an active `fcvw/plan@1` plan or a troubleshooting record without schema will see new findings; the migration note gives the conversion.
- `--since` now reports pre-existing cross-file findings in unchanged files; that is the documented contract, not noise.

## Validation plan

Unit fixtures, negative proof, replay of the two reproductions, full suite on four interpreters and governance.

## Rollback

Revert the commit that changed `tools/validate_fcvw.py`; restore the previous allowlists in `tools/path_policy_fcvw.py` and `tools/release_layout_fcvw.py`.

## Gates and approvals

- Regression gate: passed with the evidence above.
- Release gate: recorded in the V0.19.1 record in preparation; no publication.
- Decomposition required: no.

## Related records

- Framework release: [V0.19.1](../../framework-releases/V0.19.1.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Local checks | pass | see the framework release record |

## Gaps and residual risk

None beyond the downstream migration described above.
