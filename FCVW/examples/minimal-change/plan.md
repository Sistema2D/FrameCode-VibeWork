---
schema: "fcvw/plan@2"
artifact_role: example
id: "P3-R1-YYYY-MM-DD-short-slug"
status: "pending"
priority: "P3"
risk: "R1"
created_at: "YYYY-MM-DD"
updated_at: "YYYY-MM-DD"
current_version: "Vx.y.z"
expected_version: "Vx.y.z"
owner: "<owner>"
regression_contract: "required"
context_files:
  - "<path>"
---

# <Outcome-oriented title>

## Objective

<Observable result.>

## Scope

- Included: <bounded surface>.
- Excluded: <explicit boundary>.

## Acceptance criteria

- [ ] <Behavior or document contract is satisfied.>
- [ ] <Relevant validation passes.>

## Regression impact

### Existing behaviors that may be affected

- <Protected behavior.>

### Regression contracts consulted

- `<authoritative path>` — <protected contract>.

### Regression checks required

- [ ] <Focused preservation check.>

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| <Protected behavior> | pending | <command or procedure> |

### Limitations and residual risk

- <Limitation and owner, or `None`.>

## Validation

- `<command>` — <expected result>.

## Rollback

<Safe reversal procedure.>
