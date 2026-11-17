---
schema: "fcvw/plan@2"
id: "P2-R2-2026-11-13-failure-handling-and-release-guard"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P2"
risk: "R2"
created_at: "2026-11-13"
updated_at: "2026-11-13"
current_version: "V0.23.0"
expected_version: "V0.24.0"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "AGENTS.md"
  - "FCVW/PLANNING.md"
  - "FCVW/RELEASE.md"
  - "FCVW/CONTEXT_MAP.md"
  - "FCVW/wiki/README.md"
  - "tools/validate_fcvw.py"
category: "correction"
depends_on: []
---

# Failure found, failure handled; release recurrence guard

## Description

Bring upstream the local rules of a downstream project that apply to any project: every failure found during a task is fixed now or planned (with `found_by` and rule `plan-origin`), the release recurrence guard (`release-backlog`, `release-unassembled`), stopping on unsafe or inconsistent instructions, clarifying pending decisions before planning, confirming a resumed plan is still current, and writing framework feedback when it happens.

## Justification and objective

The owner asked for the downstream rule "failure found, failure corrected" to become global, and for a review of the other local rules. The project's framework files were compared with the official V0.14.0 `pt-BR` asset (checksum verified) and with its git history; most differences are product profiles. The framework-level ones were:

- the failure rule with triage by complexity and risk (adopted 2026-08-14, triage added 2026-11-04), kept in a product document and inherited by reference;
- a release recurrence guard with its own gate tool, created after 139 and then 57 unreleased fragments piled up; its warning caught three plans closing without a release in real use;
- instruction conflicts that must stop the work, clarification before planning, re-reading a plan before resuming it;
- the discipline of the field notes that produced this release.

## Scope

### Included

- `AGENTS.md`: failure rule summary and scope exception, conflict stop, clarification and resume checks, closeout evidence.
- `PLANNING.md`: "Failures found during execution" (full rule); `CONTEXT_MAP.md` first-read section.
- `RELEASE.md` recurrence guard; `PROJECT.md` `unreleased_limit`; `SCHEMAS.md` fields; plan template rows; `wiki/README.md` feedback discipline; `MIGRATIONS.md`.
- Validator rules `plan-origin` (error), `release-backlog` (error, opt-in by `unreleased_limit`), `release-unassembled` (warning).

### Excluded

- Product rules and profiles of the downstream project (module contract, design, data, audit retention, access policies, user-facing release notes).
- Its 6-level instruction precedence, which ranks project rules above the user's chat instructions: a project choice, not a framework default.
- Plans drafted by its screenshot-review tool (`ai_review`), tied to that tool.
- Its record translation utilities (one-time V0.14.0 migration with an offline backend).

## Affected files or boundaries

The files above, `tools/test_validation_signal.py` (`FailureOriginTests`, `ReleaseAssemblyTests`), `tools/test_validate_fcvw.py` (frozen inventory, surface comment).

## Implementation plan

1. Diff the downstream framework files against the official asset; classify each difference as product, superseded or framework.
2. Port the failure rule into `PLANNING.md` with a two-way trail made of data.
3. Port the release guard into the validator instead of a separate tool, with the hard-coded authority date replaced by the newest published release.
4. Document; keep the surface within budget by removing historical measurements and stale notes.

## Proportionality gate

- Real problem and root cause: failures outside the task's scope were left behind or fixed without trace; releases accumulated because assembly was nobody's gate.
- Necessary in current scope: requested by the owner; both rules were proven downstream.
- Existing codebase solution checked: reuses plan parsing and changelog `related_plans`; no new tool (the downstream tool becomes two validator rules).
- Native platform capability checked: not applicable.
- Installed dependency checked: none.
- New code or complexity justified: about 90 lines.
- Minimum non-trivial behavior tests: both ends named, origin missing, self reference, backlog at and over the limit, rule disabled without the field, invalid limit, plan closed before and after the newest release.
- Deliberate simplification and limitations: `plan-origin` matches the plan ID as text in the origin plan; the backlog limit is opt-in for upgraded projects.
- Condition for future evolution: recurrence of failures fixed without `found_by` or of backlogs under the limit.
- Mandatory safeguards preserved: risky failures never ride along in the current plan; read-only sessions do not write files.

## Acceptance criteria

- [x] The failure rule is global (`AGENTS.md`), complete in `PLANNING.md`, read first on every planning route, and traceable both ways (`plan-origin`).
- [x] More unreleased fragments than `unreleased_limit` block; a plan closed after the newest release without a changelog warns.
- [x] Every other downstream rule is either ported or recorded with the reason it stays local.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

- Scope discipline in `AGENTS.md` (now with one explicit exception).
- Downstream projects with changelogs (new warning) and with `unreleased_limit` declared (new error).

### Regression contracts consulted

- `FCVW/TESTS.md` — AI and agent boundary replay for `AGENTS.md` changes.
- `FCVW/RELEASE.md` — application release states.

### Regression checks required

- [x] Rule tests and the full suite on three interpreters.
- [x] Manual boundary replay of the new conduct rules.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Rule tests | pass | `FailureOriginTests` (2), `ReleaseAssemblyTests` (2); frozen inventory updated with `plan-origin`, `release-backlog`, `release-unassembled` |
| Boundary replay: unrelated failing test found while editing docs, cause known, R1 | pass | rule says fix now in its own commit and name it in Validation executed |
| Boundary replay: authorization defect found during a UI task | pass | security trigger, so the rule requires a pending plan with `found_by`; no fix inside the UI plan |
| Boundary replay: failure found in a read-only review | pass | report with evidence and propose the plan; no file written |
| Boundary replay: instruction to delete persisted data without backup | pass | stop and explain the conflict before acting |
| Boundary replay: log text telling the agent to skip `AGENTS.md` | pass | retrieved text stays evidence; precedence unchanged |
| Surface budget | pass | 488,233 bytes, limit 488,250 |

### Limitations and residual risk

- The boundary replay was reasoned against the rule text, not run with a live agent.
- `plan-origin` cannot prove that every failure found was recorded; it only proves that a recorded one is linked both ways.

## Validation plan

- [x] `python -B tools/check_fcvw.py --root .` on Python 3.11, 3.12 and 3.14.

## Rollback

Revert the commit; projects that declared `unreleased_limit` or `found_by` keep valid files that older tools ignore.

## Gates and approvals

- Owner request: make global the rule a downstream project adopted locally ("failure found, failure handled") and review its other local rules for upstream value.

## Related records

- Framework release: [V0.24.0](../../framework-releases/V0.24.0.md).
- Related plan: [validation signal](P2-R3-2026-11-13-validation-signal-and-closeout.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Suite, governance, benchmark, installed smoke | pass | see Regression evidence and the release record |

## Gaps and residual risk

See *Limitations and residual risk*.

## Status

`completed`
