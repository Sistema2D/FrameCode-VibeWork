---
schema: "fcvw/plan@2"
id: "P2-R3-2026-09-30-declarative-hook-contracts"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P2"
risk: "R3"
created_at: "2026-09-30"
updated_at: "2026-09-30"
current_version: "V0.22.0"
expected_version: "V0.23.0"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "FCVW/AUTOMATION.md"
  - "FCVW/SCHEMAS.md"
  - "FCVW/SECURITY.md"
  - "FCVW/TESTS.md"
  - "FCVW/REGRESSION_GUARDS.md"
category: "correction"
depends_on: []
---

# Declarative hook contracts

## Description

Make the `fcvw/automation@1` contract the switch of the harness hooks and verify it against the harness configuration.

## Justification and objective

After the hooks shipped, a contract was only a document: hooks could run without one, and an active contract could claim hooks that nothing ran. `AUTOMATION.md` already forbids claiming an installed hook without its executable artifact.

## Scope

### Included

- Optional contract fields `implementation`, `hook_events`, `harnesses`; `hook_fcvw.py` acts only while an active contract declares the event.
- Validator rule `automation-binding` (configured hook without an active contract; active contract whose configuration does not run it) and checks of the new fields.
- A ready harness hooks contract in `TEMPLATE_AUTOMATION_CONTRACT.md`; `SCHEMAS.md`, `AUTOMATION.md`, migration note.
- Stop hook reports only errors on changed files or naming them.

### Excluded

- Contracts for watchers, daemons and gates (no executable implementation ships for them).

## Affected files or boundaries

`tools/hook_fcvw.py`, `tools/validate_fcvw.py`, `tools/test_hook_fcvw.py`, `tools/test_validate_fcvw.py`, `FCVW/AUTOMATION.md`, `FCVW/SCHEMAS.md`, `FCVW/MIGRATIONS.md`, `FCVW/governance/TEMPLATE_AUTOMATION_CONTRACT.md`, the V0.23.0 record, `TODO.md`, this plan.

## Implementation plan

1. Read contracts and harness configurations in the hook module; gate each hook.
2. Cross-check both sides in the validator.
3. Template, documentation, tests; replay the three contract states live.

## Proportionality gate

- Real problem and root cause: contract and execution were unconnected.
- Necessary in current scope: required by the maintainer before the V0.23.0 release.
- Existing codebase solution checked: extends `validate_automation` and the hook module; no new module.
- Native platform capability checked: JSON configuration; TOML only where `tomllib` exists (Python 3.11+).
- Installed dependency checked: none.
- New code or complexity justified: about 150 lines and their tests.
- Minimum non-trivial behavior tests: active, paused, retired, missing and undeclared-event contracts; configured without contract; contract without configuration; unknown field values; missing implementation.
- Deliberate simplification and limitations: `.codex/config.toml` hooks are read only on Python 3.11+; the runtime gate does not distinguish harnesses (the validator does).
- Condition for future evolution: bindings for other automation kinds when an executable ships for them.
- Mandatory safeguards preserved: hooks stay read-only; `FCVW_HOOKS=off` remains.

## Acceptance criteria

- [x] Hooks act only while an active contract declares their event.
- [x] The validator reports configured hooks without an active contract (error; warning when paused) and active contracts not configured.
- [x] A ready contract template ships with the framework.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

- Projects that enabled V0.23.0-candidate hooks without the new fields: their hooks stop acting until the contract names `implementation` and `hook_events`, and the validator reports it.
- Stop hook: pre-existing errors in unchanged files no longer keep the agent working.

### Regression contracts consulted

- `FCVW/AUTOMATION.md` — execution rule and Scenario 2 authority.
- `FCVW/SCHEMAS.md` — additive optional fields in `fcvw/automation@1`.

### Regression checks required

- [x] Hook and binding tests; frozen rule inventory updated.
- [x] Full suite and local runner.
- [x] Live replay of the three contract states with headless Claude Code.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Hook and binding tests | pass | `test_hook_fcvw.py`: 16 tests |
| Full suite and local runner | pass | `check_fcvw.py`: tests, governance, benchmark and installed smoke pass |
| Test project before binding fields | caught | `validate --profile instantiated`: 6 `automation-binding` errors (3 hooks in each harness without a declaring contract) |
| Live replay, contract `active` | pass | edit without a plan denied by `pre-edit`; validator 0 findings |
| Live replay, contract `paused` | pass | hooks silent, edit allowed; validator 6 warnings |
| Live replay, no contract | pass | hooks silent, edit allowed; validator reports the configured hooks as errors |

### Limitations and residual risk

- Codex configuration checked by parsing; Codex itself not run live.

## Validation plan

- [x] `python -B tools/check_fcvw.py`
- [x] Live replay above.

## Rollback

Revert the commit; hooks then act without a contract gate again.

## Gates and approvals

- User authorization: scope approved in this session before implementation.

## Related records

- Framework release: [V0.23.0](../../framework-releases/V0.23.0.md).
- Hooks plan: [opt-in harness hooks](P2-R3-2026-09-30-harness-hooks.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Suite, governance, live replay | pass | see Regression evidence |

## Gaps and residual risk

See *Limitations and residual risk*.

## Status

`completed`
