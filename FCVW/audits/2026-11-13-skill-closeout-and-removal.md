---
schema: "fcvw/audit@1"
id: "AUD-20261113-skill-closeout-and-removal"
artifact_role: "record"
record_scope: "framework"
owner: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "search_only"
status: "completed"
created_at: "2026-11-13"
last_reviewed: "2026-11-13"
sources:
  - "FCVW/skills/code-hygiene-refactor/SKILL.md"
  - "FCVW/skills/governance-validator/SKILL.md"
  - "FCVW/CONTEXT_MAP.md"
  - "FCVW/Plans/completed/P3-R2-2026-11-13-requested-removal-sanitization.md"
  - "FCVW/Plans/completed/P2-R3-2026-11-13-validation-signal-and-closeout.md"
---

# Skill self-improvement: code-hygiene-refactor 1.4.0 and governance-validator 2.1.0

## Scope

- Assets: [code-hygiene-refactor](../skills/code-hygiene-refactor/SKILL.md) 1.3.1 to 1.4.0 and [governance-validator](../skills/governance-validator/SKILL.md) 2.0.1 to 2.1.0, plus the [context map](../CONTEXT_MAP.md) route `removal`.
- Drift: a downstream project had to fork `code-hygiene-refactor` (local 1.3.0) and `REFACTORING.md` to make a requested removal include its sanitization; the validator skill still told operators to pass `--profile` and a hand-written baseline.
- Severity: medium; the fork would be lost on the next upgrade.

## Authoritative sources

- The [removal plan](../Plans/completed/P3-R2-2026-11-13-requested-removal-sanitization.md) and the [validation signal plan](../Plans/completed/P2-R3-2026-11-13-validation-signal-and-closeout.md), with their field measurements.

## Method

Compared the downstream fork with the upstream skill line by line, kept the downstream rule and block in English, mapped the new session type to a route, and replayed the new rule against the downstream project's real removal records before fixing its false positives.

## Findings

| Metric | Evidence | Decision |
|---|---|---|
| Failure or drift | downstream fork with a removal trigger, rule and plan block; validator skill describing the pre-V0.24.0 workflow | fixed |
| Scope preservation | dead code found by chance keeps the cautious path; the removal path applies only to user-requested removals | retained |
| Backward compatibility | existing triggers and output blocks unchanged; `removal` is an added session type | retained |
| Token/risk ROI | one route reads section 26 (about 2.4 KB) instead of a new skill | pass |
| Validation replay | first draft of `plan-removal` rejected 58 real prose records; corrected to accept prose | fixed |

## Validation

`check_fcvw.py`: 372 tests passed (2 skipped) on Windows with Python 3.11, 3.12 and 3.14; `validate_fcvw.py --root .`: 0 findings, including reading-route coverage for the new session type; retrieval benchmark check passed.

## Limitations and residual risk

Agent activation of the new route in a live session was not measured. The rule checks that the sanitization record exists and is filled, not that the search was clean.

## Follow-up

The [skills catalog](../skills/README.md) lists the extended responsibility. Downstream projects with a local section 26 reconcile it through the upgrade conflict report ([V0.24.0](../framework-releases/V0.24.0.md)).
