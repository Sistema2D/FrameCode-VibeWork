---
schema: "fcvw/plan@2"
id: "P2-R2-2026-09-30-v0230-pre-release-review"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P2"
risk: "R2"
created_at: "2026-09-30"
updated_at: "2026-09-30"
current_version: "V0.22.0"
expected_version: "V0.23.0"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "FCVW/AUTOMATION.md"
  - "FCVW/SCHEMAS.md"
  - "FCVW/TESTS.md"
  - "FCVW/REGRESSION_GUARDS.md"
category: "correction"
depends_on: []
---

# V0.23.0 pre-release review of the harness hooks

## Description

Review the V0.23.0 candidate (harness hooks and declarative hook contracts) before publication and fix the defects found.

## Justification and objective

The maintainer asked for a deeper review before the release. The review replayed edge cases in an instantiated copy of the test project and found six defects, two of them false validator errors on valid configurations, and one unfilled template placeholder.

## Scope

### Included

- `automation-binding` read the event only right after the script name, so `hook_fcvw.py --profile strict pre-edit` counted as not configured (false error). Commands are now tokenized; options may come before or after the event.
- On Python 3.10 (supported) a Codex `.codex/config.toml` could not be read, so an active contract was reported as not configured (false error). It is now a warning naming the Python 3.11+ requirement.
- The stop hook's validation timeout equalled the documented 120-second harness timeout, so the harness killed the hook instead of the hook allowing. It is now 100 seconds.
- A contract with `implementation: hook_fcvw.py` and a `kind` other than `hook` was silently ignored and surfaced only as unrelated binding errors. `automation-contract` now names the cause.
- The session-start context pointed to `tools/retrieve_context.py`, which does not exist in the installed layout. It now names the path of the running layout.
- The stop hook matched changed file names as substrings (a change to `PROJECT.md` claimed errors naming `TEMPLATE_PROJECT.md`). It now matches whole names.
- The ready contract template kept the generic `Lifecycle event` placeholder; it now lists the hook's events and the new timeout.

### Excluded

- Behavior of the MCP server and other V0.22.0 surfaces (reviewed in their own release).

## Affected files or boundaries

`tools/hook_fcvw.py`, `tools/validate_fcvw.py`, `tools/test_hook_fcvw.py`, `FCVW/governance/TEMPLATE_AUTOMATION_CONTRACT.md`, the V0.23.0 record, this plan.

## Implementation plan

1. Replay configuration, contract and payload edge cases in a copy of the test project.
2. Fix each confirmed defect with a test that fails without the fix.
3. Rerun the suite, the local runner and the replay.

## Proportionality gate

- Real problem and root cause: each defect reproduced in the replay; causes named in Scope.
- Necessary in current scope: the candidate is not yet published.
- Existing codebase solution checked: `shlex` from the standard library; no new module.
- Native platform capability checked: `tomllib` stays optional.
- Installed dependency checked: none.
- New code or complexity justified: about 60 lines and five tests.
- Minimum non-trivial behavior tests: options before the event, chained commands, wrong kind, TOML without `tomllib`, whole-name matching, layout path.
- Deliberate simplification and limitations: shell commands in hook configuration are tokenized, not interpreted.
- Condition for future evolution: none.
- Mandatory safeguards preserved: hooks stay read-only; `FCVW_HOOKS=off` remains.

## Acceptance criteria

- [x] A valid configuration with options before the event produces no finding.
- [x] Codex TOML on Python 3.10 yields a warning, not an error.
- [x] The hook's validation timeout is below the documented harness timeout.
- [x] A wrong `kind` is reported on the contract.
- [x] Session-start names a path that exists in the running layout.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

- `automation-binding` findings for existing configurations; stop-hook error filtering; the session-start text.

### Regression contracts consulted

- `FCVW/AUTOMATION.md` — hooks table, configurations, contract switch.
- `FCVW/SCHEMAS.md` — `fcvw/automation@1` binding fields.

### Regression checks required

- [x] Previous hook and binding tests unchanged and passing.
- [x] Full suite and local runner.
- [x] Replay in the instantiated test project.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Hook and binding tests | pass | `test_hook_fcvw.py`: 21 tests (16 previous, 5 new) |
| Full suite and local runner | pass | `check_fcvw.py` |
| Replay, options before event | pass | before: 1 `automation-binding` error; after: 0 findings |
| Replay, wrong kind | pass | before: 6 unrelated binding errors; after: `automation-contract` names `kind: "hook"` |
| Replay, pre-edit, session-start, stop | pass | edit denied without a plan; context names `FCVW/tools/retrieve_context.py`; broken link keeps the agent working (exit 2) |

### Limitations and residual risk

- Codex still not run live; its configuration is checked by parsing.

## Validation plan

- [x] `python -B tools/check_fcvw.py`
- [x] Replay above.

## Rollback

Revert the commit.

## Gates and approvals

- User authorization: pre-release review and fixes requested by the maintainer in this session.

## Related records

- Framework release: [V0.23.0](../../framework-releases/V0.23.0.md).
- Contracts plan: [declarative hook contracts](P2-R3-2026-09-30-declarative-hook-contracts.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Suite, governance, replay | pass | see Regression evidence |

## Gaps and residual risk

See *Limitations and residual risk*.

## Status

`completed`
