# Template: Change Plan

This is the base template for any change in the project. Save in `Plans/pending/`.

```markdown
---
context_files: [] # List exact file paths the AI should load to execute this plan (reduces token bleed)
---
# P<Priority>-R<Risk>-YYYY-MM-DD-<short-description>

- **Description:** <What will be done.>
- **Justification:** <Why it is necessary.>
- **Objective:** <Expected result.>
- **Scope:** <What is included and what is not.>
- **Affected files:**
  - 
- **Implementation plan:**
  1. 
  2. 
- **Acceptance criteria:**
  - [ ] 
- **Test plan:**
  - [ ] 
- **Priority:** `P1` (Critical) to `P5` (Optional)
- **Risk:** `R1` (Very Low) to `R5` (Critical)
- **Operational Score:** `P{n}-R{n} => impact_weight {6 - P} x risk_weight {R} = {score}`
- **Review Gate:** `none` / `documentation review` / `technical review` / `human approval required`
- **Rollback Required:** `No` / `Yes - <rollback summary>`
- **Decomposition Required:** `No` / `Yes - <split recommendation>`
- **Application Module Documentation:** `not applicable` / `created at docs/...` / `updated at docs/...`
- **Current Version:** `Vx.y.z`
- **Expected Version:** `Vx.y.z`
- **Status:** `pending`
- **Creation Date:** YYYY-MM-DD
- **Completion Date:** Not applicable.
- **Technical observations:**
  - 

## Validation Executed (Fill on completion)

### Environment
- OS: 
- Backend/Runtime: 

### Tests
| Test | Result | Evidence |
|---|---|---|
| | | |

### Final Result
`approved` / `rejected`
```
