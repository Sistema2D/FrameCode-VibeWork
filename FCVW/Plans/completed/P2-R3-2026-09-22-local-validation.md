---
schema: "fcvw/plan@2"
id: "P2-R3-2026-09-22-local-validation"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P2"
risk: "R3"
created_at: "2026-09-22"
updated_at: "2026-09-22"
current_version: "V0.18.0"
expected_version: "V0.19.0"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "FCVW/TESTS.md"
  - "FCVW/AUTOMATION.md"
  - "FCVW/GOVERNANCE_GATES.md"
  - "FCVW/OWNERSHIP.md"
  - "FCVW/SECURITY.md"
depends_on: []
---

# Free local validation

## Description

Replace unavailable hosted Actions with an explicit local validation command.

## Justification and objective

The user cannot fund GitHub Actions and closed issue 58 as not planned. Preserve reproducible quality checks without paid services or an unattended runner.

## Scope

Local standard-library runner, runtime evidence, full checks, optional archive checks, reports, docs and removal of automatic hosted workflow. Existing published releases stay immutable. No new external service, runner registration, hooks, billing changes or automatic publication.

## Affected files or boundaries

Tools, regression tests, automation contracts, source-only workflow, README, inventories and next framework release record.

## Implementation plan

1. Reuse existing validators, tests, benchmark and package verifier.
2. Add explicit local orchestration with per-command logs and machine-readable evidence.
3. Retire hosted automation and document manual cross-platform execution.
4. Verify successes, failures, timeouts, runtime coverage and package boundaries; commit the scoped change.

## Proportionality gate

- Real cause: external account billing prevents hosted execution.
- Necessary scope: user explicitly requests a financially viable alternative.
- Existing solution: reuse all validation tools; no duplicated validation rules.
- Native capability: Python subprocess and local files.
- Dependencies: standard library only; user-selected installed interpreters.
- Complexity: one small orchestration command replaces repeated manual commands.
- Tests: failed steps, missing interpreters/assets, timeout, evidence and output isolation.
- Simplification: no scheduler, daemon, hosted account or self-hosted runner.
- Future evolution: run the same command on another OS when available.
- Safeguards: no inferred coverage, automatic downloads, credentials, publication or bypassed failures.

## Acceptance criteria

- [x] One local command runs all existing checks and returns nonzero on any failure.
- [x] Reports identify runtime, OS, source hash/revision, commands and logs.
- [x] Optional releases require a complete four-language asset set and source-bound verification.
- [x] Automatic GitHub jobs are removed and current documentation names the local replacement.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

Validation exit status, installed payload safety, benchmark checks, source cleanliness and declared platform coverage.

### Regression contracts consulted

- [Tests](../../TESTS.md), [automation](../../AUTOMATION.md), [regression guards](../../REGRESSION_GUARDS.md).

### Regression checks required

Focused runner tests plus full local source/governance/benchmark/install runs on Python 3.12 and 3.14. Verify a previously published asset set against its matching source without modifying it.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Runner and preserved checks | pass | 228 source and installed tests on Windows/Python 3.12 and 3.14; benchmark and governance pass. |
| Existing release archives | pass | Four V0.18.0 language ZIPs, each with 219 installed tests on both runtimes, bound to matching trusted source. |
| Failure propagation | pass | Missing interpreter, failed command, timeout, incomplete assets, source/output boundaries and source changes tested. |
| Initial archive replay | fail, then pass | First en-US/Python 3.12 replay raised WinError 145 during temporary fixture cleanup. The initial failed report was retained and an explicit complete repeat passed. |

### Limitations and residual risk

Local checks execute trusted repository code. Human invocation is required. Linux coverage remains unverified until a maintainer runs on Linux; no remote status or automated PR enforcement is claimed.

## Validation plan

Run focused negative cases, both installed runtimes and archive validation; review commands, reports, lifecycle metadata and links.

## Rollback

Revert the new tool and documentation if required. Existing individual commands remain usable. Restore a hosted workflow only by a new explicit decision, not as an automatic fallback.

## Gates and approvals

The user requested a free alternative and continuation. Local subprocesses execute only explicitly chosen interpreters and repository checks; logs remain local. Prior repository implementation and push authorization continues. No release publication is needed for switching source validation.

## Related records

- [Next framework release](../../framework-releases/V0.19.0.md).
- [Closed hosted infrastructure issue](https://github.com/Sistema2D/FrameCode-VibeWork/issues/58).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Local evidence | pass | Report 20260922T110942Z-fee3be8a; per-command logs, interpreter identity, source hash and asset hashes retained externally. |

## Gaps and residual risk

Maintainer runs local checks before accepting changes; another OS requires an actual separate execution. Language assets for the next version remain a separate release gate.
