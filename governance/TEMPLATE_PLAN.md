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
