# P3-R1-2026-05-17-mockups-system-implementation

- **Description:** Implement the `mockups/` directory structure with `.gitkeep` files, create the visual mapping guide `mockups/README.md`, and create the operational blueprint template `governance/TEMPLATE_VISUAL_DIFF.md`. Update indices in `AGENTS.md`, `MANIFEST.md`, `STACK.md`, and `wiki/index.md` to reference this new capability under version `V0.1.2`.
- **Justification:** Pixel-perfect visual fidelity requires a centralized mapping structure that avoids functional creep. Adding this system keeps visual specifications traceable without polluting the clean blueprint with temporary example images.
- **Objective:** Establish the pristine mockup mapping subsystem to support pixel-perfect visual validation for new applications.
- **Scope:** Includes `/mockups/` structure creation, `.gitkeep` files, `mockups/README.md` guide, `governance/TEMPLATE_VISUAL_DIFF.md` template, system updates, and `changelogs/V0.1.2.md`. Excludes any dummy example images or mock screens.
- **Affected files:**
  - `mockups/README.md`
  - `mockups/design/.gitkeep`
  - `mockups/actual/.gitkeep`
  - `mockups/diffs/.gitkeep`
  - `governance/TEMPLATE_VISUAL_DIFF.md`
  - `AGENTS.md`
  - `MANIFEST.md`
  - `STACK.md`
  - `wiki/index.md`
  - `changelogs/V0.1.2.md`
- **Implementation plan:**
  1. Create `/mockups/design/`, `/mockups/actual/`, and `/mockups/diffs/` with empty `.gitkeep` files.
  2. Create `mockups/README.md` describing screen scaling, DPI mapping, and coordinates tracking rules.
  3. Create `governance/TEMPLATE_VISUAL_DIFF.md` to serve as the blueprint template for pixel discrepancies.
  4. Run `powershell -ExecutionPolicy Bypass -File "governance/scripts/sync-filesystem.ps1"` to automatically update the `FILESYSTEM.md` tree.
  5. Update indices in `AGENTS.md`, `MANIFEST.md`, `STACK.md`, and `wiki/index.md`.
  6. Create `changelogs/V0.1.2.md` for this version release.
- **Acceptance criteria:**
  - [x] `/mockups/` and its subdirectories exist and are tracked by git.
  - [x] `mockups/README.md` is successfully created and fully translated to English.
  - [x] `governance/TEMPLATE_VISUAL_DIFF.md` is present.
  - [x] Visual tree in `FILESYSTEM.md` is updated and clean.
- **Test plan:**
  - [x] Verify that directories are created correctly on disk.
  - [x] Execute `sync-filesystem.ps1` and verify the updated ASCII tree shows the new folders.
- **Priority:** `P2` (High)
- **Risk:** `R1` (Very Low)
- **Current Version:** `V0.1.1`
- **Expected Version:** `V0.1.2`
- **Status:** `completed`
- **Creation Date:** 2026-05-17
- **Completion Date:** 2026-05-17
- **Technical observations:**
  - Using empty `.gitkeep` files allows Git to track the directory layout while keeping it pristine and free of mock data.
  - Updated visual trees dynamically inside `FILESYSTEM.md`.

## Validation Executed (Fill on completion)

### Environment
- OS: Windows 11
- Backend/Runtime: PowerShell 5.1

### Tests
| Test | Result | Evidence |
|---|---|---|
| Verify mockups structure | `approved` | Created `/mockups/design/`, `/mockups/actual/`, `/mockups/diffs/` with `.gitkeep` files on disk. |
| Execute tree sync script | `approved` | Automatically verified that tree contains `/mockups/` subfolders in `FILESYSTEM.md`. |
| Index references check | `approved` | Confirmed all link mappings in `AGENTS.md`, `MANIFEST.md`, `STACK.md`, `wiki/index.md`. |

### Final Result
`approved`
