---
schema: "fcvw/plan@2"
id: "P3-R2-2026-11-13-proportional-gates"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P3"
risk: "R2"
created_at: "2026-11-13"
updated_at: "2026-11-13"
current_version: "V0.23.0"
expected_version: "V0.24.0"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "tools/gates_fcvw.py"
  - "tools/validate_fcvw.py"
  - "FCVW/TESTS.md"
  - "FCVW/PROJECT.md"
category: "optimization"
depends_on: []
---

# Gates proportional to the surface a diff touches

## Description

Add `gates_fcvw.py`, which reads the surfaces a project declares in `PROJECT.md` and prints the minimum gate set for the current diff, escalating to `full` when in doubt; add rule `project-gates` for the declaration and the policy in `TESTS.md`.

## Justification and objective

Field notes measured a commit that only added six plans, a queue and a synthesis (9 files, 691 lines): the project rule ran TypeScript (19.2 s), the build (about 30 s) and 1,859 tests (about 56 s), almost two minutes and thousands of output lines with no causal path to the changed Markdown, while the contracts that did change validated in under a second. FCVW declared proportional evidence in plan text but not in the procedure before commit.

## Scope

### Included

- `tools/gates_fcvw.py` (print-only; text and JSON), `project-gates` rule, `PROJECT.md` Validation gates table with a stable anchor, `TESTS.md` section, `AGENTS.md`, `FCVW/README.md`, `SCHEMAS.md`, `MIGRATIONS.md`.

### Excluded

- Running the gates: FCVW is not a runtime; the agent or person runs what is printed and records it.

## Affected files or boundaries

The files above and `GateSelectionTests` in `tools/test_validation_signal.py`.

## Implementation plan

1. Table parser located by `<a id="validation-gates"></a>`, so translated headings do not break it.
2. Diff classification with the shared repository globs; conservative escalation.
3. Validator rule and documentation.

## Proportionality gate

- Real problem and root cause: no procedure turned the documented proportionality into a gate choice.
- Necessary in current scope: measured cost in the field notes.
- Existing codebase solution checked: reuses the glob semantics of the inventory and the plan frontmatter for risk.
- Native platform capability checked: `git diff --name-only` plus untracked files.
- Installed dependency checked: none.
- New code or complexity justified: one module of about 200 lines.
- Minimum non-trivial behavior tests: documentation-only diff, union of surfaces, unmatched path, R4 and release escalation, no table, invalid table, CLI.
- Deliberate simplification and limitations: prints commands; does not infer surfaces from code.
- Condition for future evolution: hooks may call it once the H-05 activation gate allows.
- Mandatory safeguards preserved: any undeclared path, R4/R5 or release runs `full`; the validator still runs on every surface.

## Acceptance criteria

- [x] A governance-only diff selects only `git diff --check`, the validator and the queue.
- [x] A path outside every surface, an R4/R5 in-progress plan or `--release` selects `full`.
- [x] A declared table without `full`, or with an invalid row, fails `project-gates`.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

- `PROJECT.md` of existing projects (the section is optional; absent table means built-in governance surface only).

### Regression contracts consulted

- `FCVW/TESTS.md` — minimum evidence by risk stays the floor.
- `FCVW/REGRESSION_GUARDS.md` — evidence below the plan's risk blocks completion.

### Regression checks required

- [x] New gate tests and the clean template's own `PROJECT.md` (placeholder rows skipped, no finding).

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Gate tests | pass | `GateSelectionTests`: 5 tests |
| Clean template | pass | `validate_fcvw.py --root .`: 0 findings with the new table |
| Self-applied | pass | `gates_fcvw.py --root .` on this change escalates to `full` because tools changed, as intended |

### Limitations and residual risk

- The decision is only as good as the declared surfaces; the `full` fallback bounds the risk.

## Validation plan

- [x] `python -B -m unittest discover -s tools -p "test_*.py"`

## Rollback

Revert the commit; a declared table is ignored by older tools.

## Gates and approvals

- Regression gate: required and met.

## Related records

- Decision: [ADR-0015](../../decisions/ADR-0015-validation-signal-and-proportional-gates.md).
- Framework release: [V0.24.0](../../framework-releases/V0.24.0.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Suite and governance | pass | see Regression evidence |

## Gaps and residual risk

None beyond the limitation above.

## Status

`completed`
