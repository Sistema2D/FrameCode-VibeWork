---
schema: "fcvw/plan@2"
id: "P2-R3-2026-09-30-harness-hooks"
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
  - "FCVW/SECURITY.md"
  - "FCVW/AI.md"
  - "FCVW/TESTS.md"
  - "FCVW/REGRESSION_GUARDS.md"
category: "optimization"
depends_on: []
---

# Opt-in harness hooks for Claude Code and Codex

## Description

Add `tools/hook_fcvw.py` (session start status, pre-edit plan check, stop validation) with documented configurations for Claude Code and Codex, and measure it before deciding how it ships.

## Justification and objective

The MCP server made checks callable, but nothing made an agent call them. TODO H-05 requires that tokens and quality do not get worse before activation, so the hooks were measured on a real project first.

## Scope

### Included

- `tools/hook_fcvw.py`, `tools/test_hook_fcvw.py`.
- `AUTOMATION.md` section with both harness configurations and the measurement; [ADR-0014](../../decisions/ADR-0014-optional-harness-hooks.md); migration note; V0.23.0 record; `TODO.md`.

### Excluded

- Enabling hooks by default; inspecting shell commands; live Codex execution (no Codex binary in the environment).

## Affected files or boundaries

The two tool files, `FCVW/AUTOMATION.md`, `FCVW/MIGRATIONS.md`, ADR-0014, the V0.23.0 record, `TODO.md`, this plan.

## Implementation plan

1. Confirm both hook protocols from primary sources (Claude Code behaviour in live runs; Codex generated hook schemas and handlers in `openai/codex`).
2. Implement one provider-neutral command; test with both payload shapes.
3. Measure with headless Claude Code; fix what the measurement shows; document and decide shipping.

## Proportionality gate

- Real problem and root cause: governance depended on the agent remembering it.
- Necessary in current scope: requested after the MCP server release.
- Existing codebase solution checked: reuses the validator and plan layout; no new policy.
- Native platform capability checked: both harnesses run commands with JSON on stdin.
- Installed dependency checked: none.
- New code or complexity justified: one module of about 200 lines and its tests.
- Minimum non-trivial behavior tests: both payload shapes, outside and ignored paths, plan and closeout states, disable switch, stop loop guard, malformed input.
- Deliberate simplification and limitations: shell edits not inspected; opt-in only.
- Condition for future evolution: default activation only with a larger sample (TODO H-05: at least 10 comparable plans).
- Mandatory safeguards preserved: no writes, no git mutation, no network; a failing validator never traps the agent; the stop hook blocks at most once per cycle.

## Acceptance criteria

- [x] Claude Code and Codex payloads produce the documented decisions.
- [x] Measured effect recorded, including the defect it revealed and its fix.
- [x] Hooks ship opt-in with a contract requirement and a disable switch.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

- None by default: nothing activates without project configuration.
- In an opting-in project: edits without a plan are denied; a stop with validation errors continues once.

### Regression contracts consulted

- `FCVW/AUTOMATION.md` — Scenario 2 requires explicit project authorization and a contract.
- `FCVW/SECURITY.md` — no writes, no network, bounded execution.
- `FCVW/TESTS.md` — AI and agent boundary replay.

### Regression checks required

- [x] Hook tests with both harness payloads.
- [x] Full suite and local runner.
- [x] Live A/B runs with headless Claude Code.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Hook tests | pass | `test_hook_fcvw.py`: 10 tests |
| Full suite and local runner | pass | `check_fcvw.py`: tests, governance, benchmark and installed smoke pass |
| Round 1 (4 runs) | discarded | the permission allowlist accepted `python3` but not `python`; runs that did not retry could not run tests, a harness artefact unrelated to hooks |
| Round 2 (4 runs, same task naming FCVW) | defect found | all runs correct; hooks runs cost US$0.51 and US$0.50 against US$0.34 and US$0.40, each after one denial of a closeout edit once the plan was already in `completed/` |
| Round 3 (6 runs) | pass | fixed hooks: 0 denials; task naming FCVW US$0.49 and US$0.29 (mean US$0.39 against US$0.37 without hooks); task not naming FCVW: plan before code 2/2 with hooks against 1/2 without, mean US$0.38 against US$0.30; every final state passed tests and `validate --profile instantiated` |

### Limitations and residual risk

- Two runs per condition on one small project: indicative, not the H-05 gate; hence opt-in.
- Codex was verified against its published schemas and source, not in a live session.

## Validation plan

- [x] `python -B tools/check_fcvw.py`
- [x] A/B runs recorded above.

## Rollback

`FCVW_HOOKS=off`, remove the harness configuration, or revert the commit.

## Gates and approvals

- User authorization: "pode prosseguir" after the V0.22.0 release, for hooks and declarative contracts.
- Regression gate: required and met; activation gate kept closed (opt-in).

## Related records

- Decision: [ADR-0014](../../decisions/ADR-0014-optional-harness-hooks.md).
- Framework release: [V0.23.0](../../framework-releases/V0.23.0.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Suite, governance, live runs | pass | see Regression evidence |

## Gaps and residual risk

See *Limitations and residual risk*.

## Status

`completed`
