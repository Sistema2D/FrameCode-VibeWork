# Troubleshooting and Issue History

This document defines the rules for recording, consulting, updating, and closing failures identified in the application.

The goal is to maintain a technical history of failures and remedies so that human developers and AI agents can consult previous occurrences, reuse validated solutions, and avoid repeating unsuccessful attempts.

## Mandatory Consultation Rule

Before starting any handling of a failure, bug, unexpected behavior, build error, execution error, visual regression, persistence issue, or integration failure, the `troubleshooting/` folder must be consulted.

The consultation must look for:

- failures with similar symptoms;
- files or modules affected in previous occurrences;
- hypotheses already tested;
- attempts that failed;
- solutions already applied;
- validations required to confirm the fix.

When a similar failure is already documented, the new handling should reuse the registered learning and update the existing file if it is the same occurrence or a direct recurrence.

## Relationship with Change Plans

The record in `troubleshooting/` does not replace the formal change plans defined in `PLANNING.md`.

When the solution of a failure requires functional, visual, structural, documental, or configuration changes, a corresponding plan must exist in `Plans/` before the alteration is applied.

Recommended workflow:

1. Consult `troubleshooting/`.
2. Record or update the issue in `troubleshooting/`.
3. Create or locate the corresponding plan in `Plans/`.
4. Execute the change according to the planning methodology.
5. Update the issue with handlings, results, and validation.
6. Close the issue only after objective confirmation.

When a failure generates reusable learning, the governance `wiki/` should be evaluated to receive a synthesis in `wiki/failures/` or `wiki/patterns/`.

## Location of Records

```text
troubleshooting/
```

Each failure must be documented in its own Markdown file.

## Naming Pattern

```text
YYYY-MM-DD-short-description-of-failure.md
```

The status of the issue must reside inside the file, not just depend on the filename.

## Allowed Statuses

- `open`: failure recorded, no conclusive analysis yet.
- `in_analysis`: failure under investigation, with reproduction, logs, or hypotheses in progress.
- `in_progress`: solution in implementation or test.
- `awaiting_validation`: fix applied, awaiting confirmation.
- `resolved`: failure fixed and validated.
- `recurring`: failure recurred after previous handling.
- `discarded`: record closed because it was not confirmed as a failure, was out of scope, or was replaced.

## Minimum Structure of an Issue

```markdown
# Issue Title

## Status

`open`

## Date of Identification

YYYY-MM-DD

## Date of Resolution

Not applicable.

## Application Version

`Vx.y.z`

## Environment

- Operating System:
- Build:
- Environment observations:

## Summary

Short description of the problem.

## Detailed Description

Context, symptoms, and conditions under which the failure occurs.

## Steps to Reproduce

1.
2.
3.

## Expected Behavior

-

## Observed Behavior

-

## Impact

-

## Files, Modules, or Screens Possibly Affected

-

## Evidence

- Logs:
- Error messages:
- Visual observations:

## Hypotheses

-

## Handlings Attempted

### Attempt 1 — YYYY-MM-DD HH:MM

- Action:
- Result:
- Worked: `yes` / `no` / `partial`
- Observations:

## Result of Handlings

-

## Solution Applied

Not applicable while the issue is open.

## Related Plan

-

## Validation Executed

-

## Prevention or Future Recommendations

-

## Technical Observations

-
```

## Record of Handlings

All handlings must be recorded, including those that did not work.

Each attempt must indicate: date and approximate time, executed action, observed result, whether it worked or failed, and new hypothesis generated.

Do not erase old attempts. When a hypothesis is discarded, record the reason.

## Criteria to Close an Issue

An issue can only be marked as `resolved` when:

- the probable or confirmed cause is documented;
- the applied solution is described;
- there is objective validation;
- relevant tests have been executed or the limitation is recorded;
- the related plan is completed, when the solution required a formal change.

## Evidence and Logs

Rules:

- do not record tokens, secrets, or credentials;
- do not record private user data;
- remove or anonymize personal paths when they are not necessary;
- summarize long logs instead of pasting excessive content;
- preserve error messages with enough fidelity for future searches.

## Recommended Consultation

Before starting a new handling, use textual search in `troubleshooting/`.

Examples:

```powershell
rg -n "<symptom or module>" troubleshooting
rg -n "<symptom or module>" Plans
```

## Responsibility of AI Agents

AI agents must:

- consult `troubleshooting/` before proposing a failure correction;
- record new failures when identified during analysis, implementation, or testing;
- update handlings with real results of executed commands;
- not declare an issue as resolved without objective validation;
- create a formal plan in `Plans/` before applying changes to the application;
- preserve the history of attempts, including unsuccessful ones.

## Models and Templates

To create new troubleshooting records, use the template in:
`governance/TEMPLATE_TROUBLESHOOTING.md`

The template includes: identification metadata, symptom description, hypotheses table, root cause, solution steps, validation checklist, prevention notes, and a wiki promotion decision field.

