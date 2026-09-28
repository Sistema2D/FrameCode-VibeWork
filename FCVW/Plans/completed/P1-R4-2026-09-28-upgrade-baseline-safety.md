---
schema: "fcvw/plan@2"
id: "P1-R4-2026-09-28-upgrade-baseline-safety"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P1"
risk: "R4"
created_at: "2026-09-28"
updated_at: "2026-09-28"
current_version: "V0.19.0"
expected_version: "V0.19.1"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "FCVW/OWNERSHIP.md"
  - "FCVW/MIGRATIONS.md"
  - "FCVW/REGRESSION_GUARDS.md"
  - "FCVW/TESTS.md"
depends_on: []
---

# Upgrade baseline safety

## Description

Stop the selective upgrade from overwriting local customizations. Backlog items A-01, A-06 and A-07 of the source-only maintainer backlog (`TODO.md` at the source repository root, not installed).

## Justification and objective

Reproduced defect: without `FCVW/ROLE_MANIFEST.json`, or after regenerating it as `AGENTS.md` instructed, `upgrade_fcvw.py` rebuilt the baseline from the live tree and reported a locally edited `PLANNING.md` as `REPLACE … safe to replace`. The objective is that an upgrade never classifies an unverifiable local difference as safe.

## Scope

### Included

- Safe mode without a trustworthy baseline: a divergent replaceable file becomes `conflict`.
- `role_manifest_fcvw.py --write` refuses to overwrite an installed baseline; `--output` remains available.
- `--apply` records the applied release manifest as the next baseline.
- `--accept-conflicts` refuses to overwrite an earlier `.local` backup.
- JSON output reports what was actually applied.
- Documentation that told users to regenerate the manifest.

### Excluded

- Removal of files dropped upstream (A-08, `--prune`); deferred to the reduction phase that needs it.
- Any change to ownership roles or release packaging.

## Affected files or boundaries

`tools/upgrade_fcvw.py`, `tools/role_manifest_fcvw.py`, `tools/test_validate_fcvw.py`, `AGENTS.md`, `FCVW/README.md`, `FCVW/FILESYSTEM.md`, `FCVW/TESTS.md`, `FCVW/MIGRATIONS.md`, `FCVW/governance/TEMPLATE_CI_WORKFLOW.md`.

## Implementation plan

1. Return no baseline for a missing or unreadable manifest; inventory live roles only.
2. Classify identical files as unchanged, then unverifiable differences as conflicts.
3. Write the release manifest after a successful apply; refuse existing backups before any write.
4. Refuse `--write` over an installed baseline; update the instructions.
5. Add regression tests and prove they fail on the V0.19.0 tools.

## Proportionality gate

Not applicable — the change removes an unsafe fallback and adds refusals inside the two existing tools; no new file, dependency or mechanism.

## Acceptance criteria

- [x] Missing, unreadable and regenerated baselines never yield `replace` for a locally edited framework file.
- [x] An applied upgrade leaves no false conflict for the same release.
- [x] An earlier `.local` backup is never overwritten.
- [x] JSON states `applied`, `files_applied` and the baseline source.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

Upgrade verdicts for untouched policies, preservation of project profiles and records, path containment, link refusal, and installed-release verification that writes a manifest programmatically.

### Regression contracts consulted

- [Ownership](../../OWNERSHIP.md) — replace versus preserve by role.
- [Migrations](../../MIGRATIONS.md) — the V0.15.0 to V0.16.0 first-time manifest step.

### Regression checks required

- [x] Existing `UpgradePlanTests` (untouched replace with baseline, local conflict, profile preservation, containment, symlink refusal).
- [x] New negative fixtures fail on the V0.19.0 tools.
- [x] Full source suite, governance and installed smoke through the local runner.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Upgrade and manifest tests | pass | `python -B -m unittest test_validate_fcvw.UpgradePlanTests`: 12 tests |
| Guardrail proof | pass | the same tests against V0.19.0 `upgrade_fcvw.py`/`role_manifest_fcvw.py`: 4 failures and 2 errors, as expected |
| Full suite | pass | 324 tests on Linux with Python 3.10, 3.11, 3.12 and 3.13 |
| Installed verification | pass | `verify_release_fcvw.py --smoke --run-tests` through `check_fcvw.py` |

### Limitations and residual risk

- The test that previously expected `replace` without any baseline now writes a baseline first; that behaviour change is intended and documented in the migration note.
- Installations that already regenerated their manifest after local edits cannot recover the lost digests; the migration note tells them to compare against the release they installed.

## Validation plan

Focused upgrade tests, negative proof against V0.19.0, full suite on four interpreters, governance validation.

## Rollback

Revert the commit that changed `tools/upgrade_fcvw.py` and `tools/role_manifest_fcvw.py`; stored manifests remain valid JSON for either version.

## Gates and approvals

- Regression gate: passed with the evidence above.
- Security/data gate: the change only adds refusals; no new write target besides the manifest the tool already owned.
- Decomposition required: no. The user asked to proceed with phase 1 of the backlog.

## Related records

- Framework release: [V0.19.1](../../framework-releases/V0.19.1.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Local checks | pass | see the framework release record |

## Gaps and residual risk

A-08 (`--prune`) remains open and is scheduled with the file reduction.
