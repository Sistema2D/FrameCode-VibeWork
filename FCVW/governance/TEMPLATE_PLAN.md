# Template: change plan

Save as `Plans/pending/P{1..5}-R{1..5}-YYYY-MM-DD-<slug>.md` and replace every placeholder before execution.

```markdown
---
schema: "fcvw/plan@2"
id: "P3-R2-YYYY-MM-DD-short-description"
artifact_role: "record"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "pending"
priority: "P3"
risk: "R2"
created_at: "YYYY-MM-DD"
updated_at: "YYYY-MM-DD"
current_version: "Vx.y.z"
expected_version: "Vx.y.z | assigned_at_release"
owner: "<human-or-agent-role>"
regression_contract: "required | not_applicable"
context_files:
  - "path/to/file"
depends_on: []
---

# Short change title

## Description

<What will change.>

## Justification and objective

<Why and expected result.>

## Scope

### Included

- <Included boundary.>

### Excluded

- <Excluded boundary.>

## Affected files or boundaries

- <Path or responsibility.>

## Implementation plan

1. <Bounded step.>

## Proportionality gate

Complete this section when the change adds a dependency, abstraction, service, wrapper, architectural layer, parallel mechanism, or other non-trivial technical complexity.

- Real problem and root cause:
- Necessary in current scope:
- Existing codebase solution checked:
- Native platform capability checked:
- Installed dependency checked:
- New code or complexity justified:
- Minimum non-trivial behavior tests:
- Deliberate simplification and limitations:
- Condition for future evolution:
- Mandatory safeguards preserved: security, privacy, accessibility, traceability, validation, audit, compliance, data integrity, documentation, and risk-required tests.

For a trivial bounded change, state `Not applicable — <specific reason>`.

## Acceptance criteria

- [ ] <Observable result.>

## Dependency validation

None. When `depends_on` is non-empty, replace this line with:

| Dependency | Blocking reason | Unblock criteria | Status | Evidence |
|---|---|---|---|---|
| P3-R2-YYYY-MM-DD-prerequisite | <Specific reason> | <Observable criteria> | pending | pending |

Use `satisfied` only after the prerequisite is completed and concrete evidence is recorded. Use `invalidated` for a discontinued prerequisite and keep the dependent plan blocked until it is explicitly replanned, replaced, or discontinued.

## Regression impact

### Existing behaviors that may be affected

- <Protected behavior, consumer, interface, data, visual state, permission, or governance contract.>

### Regression contracts consulted

- `<authoritative path or interface>` — <what it protects>.

### Regression checks required

- [ ] <Focused automated test, manual workflow replay, visual check, compatibility check, security denial case, AI boundary replay, or structural negative fixture.>

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| <Protected behavior> | pending | <command/procedure and artifact> |

### Limitations and residual risk

- <Limitation, owner, decision, and follow-up; or `None`.>

For `regression_contract: not_applicable`, replace the subsections with `Justification: <specific reason>` and retain any applicable structural check. A plan cannot close with placeholders or pending regression results.

## Validation plan

- [ ] <Command or procedure and expected result.>

## Rollback

<Procedure or explicit approved reason it does not apply.>

## Gates and approvals

- Regression gate:
- Security/data/refactoring/skill/release gate:
- Decomposition required:
The plan must be listed by its state queue and contain at least one portable Markdown link to an authoritative source or related record before closeout.


## Related records

- Changelog/framework release:
- Decision:
- Failure/regression:
- Other plan:

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| <Check> | <pass/fail/blocked/not_applicable> | <Evidence> |

## Gaps and residual risk

- <Gap, owner, and follow-up; or `None`.>
```
