# P3-R1-2026-05-18-update-readme-directory-trees

- **Description:** Update the directory structure visual trees in both Portuguese and English sections of README.md to include recently added core folders and files (FILESYSTEM.md, skills/, mockups/, and wiki/sessions/).
- **Justification:** Ensures that our main user-facing documentation accurately reflects the physical state and folder architecture of version V0.3.0+ of the framework.
- **Objective:** Synchronize README.md directory maps with the actual workspace filesystem structure.
- **Scope:**
  - Update [README.md](../../README.md) Portuguese directory tree.
  - Update [README.md](../../README.md) English directory tree.
  - Update [MANIFEST.md](../../MANIFEST.md) and [STACK.md](../../STACK.md) to bump version to `V0.3.1`.
  - Re-run filesystem sync script.
  - Create `changelogs/V0.3.1.md`.
- **Affected files:**
  - [`README.md`](../../README.md)
  - [`MANIFEST.md`](../../MANIFEST.md)
  - [`STACK.md`](../../STACK.md)
  - [`changelogs/V0.3.1.md`](../../changelogs/V0.3.1.md)
- **Implementation plan:**
  1. Update directory structure tree in the Portuguese section of [README.md](../../README.md).
  2. Update directory structure tree in the English section of [README.md](../../README.md).
  3. Bump version to `V0.3.1` in [MANIFEST.md](../../MANIFEST.md) and [STACK.md](../../STACK.md).
  4. Automatically synchronize directory tree layout inside [FILESYSTEM.md](../../FILESYSTEM.md).
  5. Create `changelogs/V0.3.1.md`.
  6. Validate and close the plan in `Plans/completed/`.
- **Acceptance criteria:**
  - [x] Both Portuguese and English directory trees inside `README.md` list `FILESYSTEM.md`, `skills/`, `mockups/`, and `wiki/sessions/`.
  - [x] Version `V0.3.1` is declared in Manifest and Stack records.
- **Test plan:**
  - [x] Verify markdown syntax and link integrity.
- **Priority:** `P3` (Medium)
- **Risk:** `R1` (Very Low)
- **Current Version:** `V0.3.0`
- **Expected Version:** `V0.3.1`
- **Status:** `completed`
- **Creation Date:** 2026-05-18
- **Completion Date:** 2026-05-18
- **Technical observations:**
  - None.

## Validation Executed (Fill on completion)

### Environment
- OS: Windows 11
- Backend/Runtime: Powershell

### Tests
| Test | Result | Evidence |
|---|---|---|
| Verify README trees content | Success | Confirmed trees list all target elements: `skills/`, `mockups/`, `FILESYSTEM.md`, and `wiki/sessions/`. |
| Dynamic tree layout sync | Success | `sync-filesystem.ps1` rebuilt layout maps cleanly. |
| Version registration check | Success | Bumps validated in Manifest and Stack records. |

### Final Result
`approved`


