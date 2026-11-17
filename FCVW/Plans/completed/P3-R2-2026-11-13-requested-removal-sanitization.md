---
schema: "fcvw/plan@2"
id: "P3-R2-2026-11-13-requested-removal-sanitization"
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
  - "FCVW/REFACTORING.md"
  - "FCVW/skills/code-hygiene-refactor/SKILL.md"
  - "FCVW/CONTEXT_MAP.md"
  - "tools/validate_fcvw.py"
category: "correction"
depends_on: []
---

# Requested removal includes sanitization

## Description

Bring upstream the rule a downstream project adopted locally: a removal the user asks for includes removing the code that existed only for the item. Add `REFACTORING.md` section 26, `code-hygiene-refactor` 1.4.0, a `removal` route in the context map and rule `plan-removal`.

## Justification and objective

Reviewing captures, a project owner had to write "delete the Next button and sanitize all of its code" because nothing in FCVW required it; the same project measured that retiring dead features shrank its monoliths by about 4,000 lines with no refactoring at all. Section 25 and the skill treated dead code as a cautious finding ("mark `CANDIDATE_FOR_REMOVAL`") and told agents not to mix cleanup with delivery, which pushed the residue of a requested removal to "another plan". The project adopted section 26 and skill 1.3.0 locally on 2026-10-22; because `REFACTORING.md` uses `upgrade_strategy: replace`, the next upgrade would have deleted it.

## Scope

### Included

- `REFACTORING.md` section 26 and the trigger in section 25; skill 1.4.0 (trigger, non-negotiable rule, plan block, exit criterion, `removal` session type); context-map route, alias and first-read section; catalog row; `plan-removal`.

### Excluded

- Requiring a fixed vocabulary for the final search: real records write it in prose, in Portuguese.

## Affected files or boundaries

The files above, the skill change report, `RemovalSanitizationTests`.

## Implementation plan

1. Port section 26 in English, keeping the downstream numbering so the upgrade replaces the local copy with the same section.
2. Change the skill through the self-improvement gate.
3. Add the route and the rule; measure the rule on real records.

## Proportionality gate

- Real problem and root cause: no rule linked a removal request to removing its exclusive code.
- Necessary in current scope: listed in the field notes as an upstream candidate.
- Existing codebase solution checked: extends section 25 and the existing skill instead of a new skill.
- Native platform capability checked: not applicable; policy text and one structural rule.
- Installed dependency checked: none.
- New code or complexity justified: about 30 lines for the rule.
- Minimum non-trivial behavior tests: prose record, labelled list with nested items, empty section, placeholder, blank field, markup in inline code.
- Deliberate simplification and limitations: the rule checks that the record exists and is filled, not that the search was clean.
- Condition for future evolution: recurrence of removals closed with residue despite a filled record.
- Mandatory safeguards preserved: persisted data, public contracts, shared code and history are explicit exceptions.

## Acceptance criteria

- [x] Section 26 and skill 1.4.0 state inventory, exceptions and evidence.
- [x] A removal request routes to section 26 and the skill.
- [x] An empty, placeholder or blank-field Removal sanitization section in a completed plan fails; prose passes.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

- Refactoring routes now read section 26 first as well (about 2.4 KB more).
- Plans with a Removal sanitization section.

### Regression contracts consulted

- `FCVW/REFACTORING.md` section 25 — cautious handling of dead code found by chance stays unchanged.
- `FCVW/skills/self-improvement/SKILL.md` — skill change gate.

### Regression checks required

- [x] Reading-route and skill validation; retrieval benchmark.
- [x] Rule measured on the downstream project's real removal records.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Routes and skills | pass | `validate_fcvw.py --root .`: 0 findings (`removal` session type mapped) |
| Benchmark | pass | `benchmark_retrieval_fcvw.py --root . --check` |
| Real records | pass | first draft flagged 58 prose records as empty and 1 that quoted `<select>` in code; the rule now accepts prose and reads placeholders outside inline code: 0 findings |

### Limitations and residual risk

- The rule cannot verify that the final search was actually run.

## Validation plan

- [x] `python -B -m unittest discover -s tools -p "test_*.py"`

## Rollback

Revert the commit; downstream projects that kept a local section 26 keep it through the upgrade conflict report.

## Gates and approvals

- Self-improvement gate: [skill change report](../../audits/2026-11-13-skill-closeout-and-removal.md).

## Related records

- Framework release: [V0.24.0](../../framework-releases/V0.24.0.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Suite, routes, real records | pass | see Regression evidence |

## Gaps and residual risk

None beyond the limitation above.

## Status

`completed`
