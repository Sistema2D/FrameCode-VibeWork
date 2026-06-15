---
context_files: [".cursorrules", ".windsurfrules", "AGENTS.md"]
---
# P3-R2-2024-06-15-symlink-cursorrules

- **Description:** Replace `.windsurfrules` with a symlink to `.cursorrules`.
- **Justification:** Both files contain identical framework governance rules. Using a symlink prevents them from falling out of sync and improves maintainability.
- **Objective:** Ensure AI agent rules remain consistent across editor configurations.
- **Scope:** Modify `.windsurfrules` to be a symlink to `.cursorrules`.
- **Affected files:**
  - `.windsurfrules`
- **Implementation plan:**
  1. Remove the existing `.windsurfrules` file.
  2. Create a symlink from `.windsurfrules` to `.cursorrules`.
- **Acceptance criteria:**
  - [ ] `.windsurfrules` is a symlink pointing to `.cursorrules`.
  - [ ] The content of `.windsurfrules` matches `.cursorrules`.
- **Test plan:**
  - [ ] Run `ls -l .windsurfrules` to verify it's a symlink.
  - [ ] Run `cat .windsurfrules` and compare output with `cat .cursorrules`.
- **Priority:** `P3`
- **Risk:** `R2`
- **Operational Score:** `P3-R2 => impact_weight 3 x risk_weight 2 = 6`
- **Review Gate:** `technical review`
- **Rollback Required:** `No`
- **Decomposition Required:** `No`
- **Application Module Documentation:** `not applicable`
- **Current Version:** `N/A`
- **Expected Version:** `N/A`
- **Status:** `approved`
- **Creation Date:** 2024-06-15
- **Completion Date:** Not applicable.
- **Technical observations:**
  - Ensure the symlink is created correctly on the filesystem.

## Validation Executed (Fill on completion)

### Environment
- OS: Linux
- Backend/Runtime: Bash

### Tests
| Test | Result | Evidence |
|---|---|---|
| Verify symlink creation | | |
| Verify content match | | |

### Final Result
`approved`

## Execution Notes
| Verify symlink creation | Pass | symlink created successfully |
| Verify content match | Pass | cat outputs matched |
