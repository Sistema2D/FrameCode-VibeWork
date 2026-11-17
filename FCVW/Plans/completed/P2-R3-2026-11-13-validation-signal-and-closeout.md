---
schema: "fcvw/plan@2"
id: "P2-R3-2026-11-13-validation-signal-and-closeout"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P2"
risk: "R3"
created_at: "2026-11-13"
updated_at: "2026-11-13"
current_version: "V0.23.0"
expected_version: "V0.24.0"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "tools/validate_fcvw.py"
  - "tools/retrieve_context.py"
  - "tools/hook_fcvw.py"
  - "tools/mcp_server_fcvw.py"
  - "FCVW/PLANNING.md"
  - "FCVW/SCHEMAS.md"
  - "FCVW/MIGRATIONS.md"
  - "FCVW/REGRESSION_GUARDS.md"
category: "correction"
depends_on: []
---

# Validation signal and decided closeout

## Description

Make the validator a usable gate on a real project: infer the profile, generate and stabilise the legacy baseline, read `context_files` as the consumer reads them, name proven successors from git history, classify history instead of failing it, and make `completed` mean "every checklist item decided", with deferred criteria carried as data by the receiving plan.

## Justification and objective

Field notes from an application that uses FCVW (V0.14.0 installed, 1,524 commits) recorded four failures that V0.23.0 still has:

- **Permanently red gate.** Without `--profile` the validator chose `clean-template` (4,482 findings instead of 2,792); separating new findings from debt required an ad hoc script over internal functions. The baseline existed but had no generator, matched messages that embed line numbers, and printed every accepted row.
- **`context_files` read from the wrong folder.** The validator resolved them relative to the plan while `retrieve_context.py` reads them from the root; 1,617 findings came from that and from moved files, and 1,561 had a mechanical fix in git's rename history that the validator did not suggest.
- **Undecided closeout.** 171 open boxes sat in completed plans and 7 `[~]` items named no destination; a criterion deferred "to the cutover" in prose was never delivered because the target plan never knew it carried it.
- **`pending` read as a word.** Fixed upstream in V0.19.1 (A-04); this plan keeps the fix and closes the formatted variants (`` `pending` ``, `**pending**`).

The objective is a default command whose exit code means "this change introduced a defect".

## Scope

### Included

- `validate_fcvw.py`: `--profile auto` (default), `--write-baseline` and its options, `--show-baseline`, stable baseline matching, translated header rows and escaped pipes, rules `plan-acceptance` and `plan-deferral`, repository-root `context_files`, git rename successors and `--fix-moved-links` for frontmatter, deleted-after-record history warnings, placeholders read outside inline code, formatted pending results, legacy baselines under `audits/`.
- `retrieve_context.py` resolves `context_files` like the validator; `hook_fcvw.py` and `mcp_server_fcvw.py` default to `auto`.
- Successor hints from `MIGRATIONS.md` tables in every language variant: the V0.23.0 `pt-BR`, `es` and `de` assets translate the headers (`Removido`, `Eliminado`, `Entfernt`, `Arquivo legado`…), so the lineage was empty outside English.
- `AGENTS.md`, `PLANNING.md`, `SCHEMAS.md`, `MIGRATIONS.md`, `INSTANTIATION.md`, `governance-validator`, plan and baseline templates.
- Reconcile the two undecided criteria the new rule found in this repository's own completed plans.

### Excluded

- Rewriting historical evidence: the two reconciled items keep their text; only the decision marker changed.
- A differential mode that validates an older git revision (the baseline covers the need with less machinery).

## Affected files or boundaries

The tools and documents above, `tools/test_validation_signal.py`, `tools/test_validate_fcvw.py` (frozen rule inventory, surface guard), two completed plans of Phase 2 and Phase 3, this plan.

## Implementation plan

1. Profile inference from language-independent lock tokens and `PROJECT.md`.
2. Baseline writer, comparable message form, header and pipe parsing, default location, summary output.
3. Shared `context_files` resolution; git rename and deletion history, read lazily once per run.
4. Closeout grammar and the cross-plan deferral check.
5. Measure on the real project read-only; correct what the measurement shows; document.

## Proportionality gate

- Real problem and root cause: the gate's output did not distinguish regression from debt, so it was ignored; closeout semantics existed only as prose.
- Necessary in current scope: every item comes from a measured case in the field notes.
- Existing codebase solution checked: reuses the existing baseline schema, `--fix-moved-links`, the plan parser and title aliases; no new schema.
- Native platform capability checked: git's own rename detection and ignore rules instead of heuristics.
- Installed dependency checked: standard library only.
- New code or complexity justified: about 450 lines in the validator, mostly the two closeout rules and the baseline writer.
- Minimum non-trivial behavior tests: 38 tests in `test_validation_signal.py`, including an end-to-end write-baseline-then-regress run.
- Deliberate simplification and limitations: one baseline row covers identical findings in the same file; a project-chosen baseline path must be passed explicitly.
- Condition for future evolution: a differential mode only if baselines prove too costly to maintain.
- Mandatory safeguards preserved: `strict` and `clean-template` accept no baseline; configuration errors cannot be baselined; history warnings apply only to completed or discontinued plans and only when git proves the file existed.

## Acceptance criteria

- [x] Without `--profile`, an instantiated project is validated as `instantiated`, or `incremental` with its baseline; the reason is printed.
- [x] `--write-baseline` records current debt; the next default run exits 0 and a new finding exits 1 (end-to-end test).
- [x] Moving text inside a file does not turn baselined debt into a new finding.
- [x] Root-relative and plan-relative `context_files` resolve in both the validator and `retrieve_context.py`.
- [x] A renamed target gets a proven successor and `--fix-moved-links` rewrites links and frontmatter.
- [x] A completed plan with `[ ]`, or `[~]` without `deferred:`/`waived:`, fails; a deferral the target does not carry fails.
- [x] Measured on the real project without changing it.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

- Explicit `--profile` runs, `--baseline` files written by hand, `--since` scoping, JSON consumers (hooks, MCP).
- Plans that wrote `context_files` plan-relative.
- Completed plans in downstream projects (new findings by design).

### Regression contracts consulted

- `FCVW/MIGRATIONS.md` — never rewrite history to satisfy a new rule; record debt in a baseline.
- `FCVW/REGRESSION_GUARDS.md` — result grammar `pass`, `fail`, `blocked`, `not_applicable`, `pending`.
- `tools/test_validate_fcvw.py` — frozen rule inventory and existing baseline tests.

### Regression checks required

- [x] Full suite on Python 3.11, 3.12 and 3.14 (Windows).
- [x] Existing baseline, `--since`, pending and placeholder tests unchanged and passing.
- [x] Read-only field run on the real project.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Full suite | pass | `check_fcvw.py` on Windows with Python 3.11.15, 3.12.10 and 3.14.6: 372 tests (326 before), 2 skipped, governance, benchmark and installed smoke pass; source unchanged during each run |
| Governance of this repository | pass | `validate_fcvw.py --root .` (auto: clean-template): 0 findings after reconciling 2 undecided criteria the new rule found here |
| Explicit profiles and JSON | pass | hook and MCP tests pass with the `auto` default; summary line format unchanged |
| Field run, V0.23.0 vs V0.24.0 | pass | real project, read-only: default profile clean-template with 34,461 errors became `instantiated` with 2,921 errors and 170 warnings; validator 70 s to 26 s; `plan-acceptance` found 167 undecided items and 7 unaddressed `[~]`, matching the manual count (171 and 7) |
| False positives found by the field run | pass | first draft of `plan-removal` flagged 58 prose records; 3 of 4 regression "placeholders" were markup in inline code; both corrected and covered by tests |
| Localized lineage | pass | headers read from the four V0.23.0 ZIPs; `LocalizedLineageTests` names the successor in `pt-BR`, `es`, `de` and `en-US` |

### Limitations and residual risk

- The real project runs V0.14.0 content, so most remaining errors are migration items (troubleshooting schema, rollback sections) that its upgrade must handle or baseline.
- Git-derived hints need a git work tree whose top level is the validated root.
- 122 relationship errors there name files of an absorbed repository; they stay red until baselined, by design.

## Validation plan

- [x] `python -B -m unittest discover -s tools -p "test_*.py"`
- [x] `python -B tools/validate_fcvw.py --root .`
- [x] Read-only field comparison (tree digest and `.git/index` checked; concurrent edits by another session were identified and excluded).

## Rollback

Revert the commit. Projects keep working with explicit `--profile` and `--baseline`. A baseline written by `--write-baseline` stays loadable by V0.23.0 when passed with `--profile incremental --baseline` from outside `audits/`, but V0.23.0 compares messages with their line numbers, so those rows report as stale there.

## Gates and approvals

- Regression gate: required and met.
- Framework schema gate: additive fields and rules; migration note in `MIGRATIONS.md`.
- User request: "create a new, improved version of the framework that fixes every problem identified in the field notes".

## Related records

- Decision: [ADR-0015](../../decisions/ADR-0015-validation-signal-and-proportional-gates.md).
- Framework release: [V0.24.0](../../framework-releases/V0.24.0.md).
- Skill change report: [governance-validator and code-hygiene-refactor](../../audits/2026-11-13-skill-closeout-and-removal.md).
- Other plans: [graph inventory](P2-R3-2026-11-13-graph-inventory-and-generation.md), [gates](P3-R2-2026-11-13-proportional-gates.md), [removal](P3-R2-2026-11-13-requested-removal-sanitization.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Suite, governance, field run | pass | see Regression evidence |

## Gaps and residual risk

See *Limitations and residual risk*. Linux and macOS were not exercised in this session.

## Status

`completed`
