# P4-R2-2026-05-18-discontinue-mockups-and-automation-scripts

- **Description:** Deprecate and physically remove the `mockups/` folder and the filesystem synchronization script `governance/scripts/sync-filesystem.ps1`. Transfer all visual layout standards, comparison mechanisms, and file blueprint layouts directly into robust Markdown files (`DESIGN.md` and `FILESYSTEM.md`). Transition the framework to a pure-markdown instruction model.
- **Justification:** Aligns with the user's architectural direction to eliminate environment script dependencies and visual folder clutter, keeping the framework 100% focused on pure-markdown agent instructions and highly robust visual design rules.
- **Objective:** transition the workspace from an automated script model to a pure, declarative Markdown instruction model.
- **Scope:**
  - Delete `mockups/` folder.
  - Delete `governance/scripts/sync-filesystem.ps1`.
  - Rewrite `DESIGN.md` to be extremely robust, incorporating visual specifications, visual regression verification workflows, and component calibrations in pure prose.
  - Create `decisions/ADR-0001-pure-markdown-over-automation-scripts.md` documenting this architectural pivot.
  - Update `AGENTS.md` and `AI.md` to remove all checklist steps and policies related to running `sync-filesystem.ps1` and mockup calibration.
  - Update `MANIFEST.md` and `STACK.md` to version bump to `V0.4.0` and reflect the pure-markdown model.
  - Update the root `README.md` to remove the mockups folder and script references.
  - Create `changelogs/V0.4.0.md`.
- **Affected files:**
  - `mockups/` (Deleted)
  - `governance/scripts/sync-filesystem.ps1` (Deleted)
  - [`DESIGN.md`](file:///c:/Users/meloha/Desktop/FCVW/DESIGN.md) (Modified)
  - [`decisions/ADR-0001-pure-markdown-over-automation-scripts.md`](file:///c:/Users/meloha/Desktop/FCVW/decisions/ADR-0001-pure-markdown-over-automation-scripts.md) (Created)
  - [`AGENTS.md`](file:///c:/Users/meloha/Desktop/FCVW/AGENTS.md) (Modified)
  - [`MANIFEST.md`](file:///c:/Users/meloha/Desktop/FCVW/MANIFEST.md) (Modified)
  - [`STACK.md`](file:///c:/Users/meloha/Desktop/FCVW/STACK.md) (Modified)
  - [`README.md`](file:///c:/Users/meloha/Desktop/FCVW/README.md) (Modified)
  - [`changelogs/V0.4.0.md`](file:///c:/Users/meloha/Desktop/FCVW/changelogs/V0.4.0.md) (Created)
- **Implementation plan:**
  1. Create the ADR record `decisions/ADR-0001-pure-markdown-over-automation-scripts.md`.
  2. Physically delete the `mockups/` folder and `governance/scripts/sync-filesystem.ps1` script.
  3. Rewrite `DESIGN.md` to be an extremely robust technical design system, mapping interactive elements, layout rules, and prose calibration guidelines.
  4. Modify `AGENTS.md` and `AI.md` to prune script execution checklists and mockup rules.
  5. Update `MANIFEST.md` and `STACK.md` to version bump to `V0.4.0`.
  6. Update directory visual trees in `README.md` and `FILESYSTEM.md` to reflect the new cleaner filesystem state.
  7. Create `changelogs/V0.4.0.md`.
  8. Validate and close the plan in `Plans/completed/`.
- **Acceptance criteria:**
  - [x] `mockups/` folder is deleted.
  - [x] `sync-filesystem.ps1` script is deleted.
  - [x] `decisions/ADR-0001-...` is accepted and active.
  - [x] `DESIGN.md` is robust and complete.
  - [x] All checkouts and references to filesystem script and mockups are removed from `AGENTS.md` and `AI.md`.
  - [x] Version `V0.4.0` is registered.
- **Test plan:**
  - [x] Verify that no references to the deleted script remain in checklists and active rules.
- **Priority:** `P4` (High)
- **Risk:** `R2` (Low)
- **Current Version:** `V0.3.1`
- **Expected Version:** `V0.4.0`
- **Status:** `completed`
- **Creation Date:** 2026-05-18
- **Completion Date:** 2026-05-18
- **Technical observations:**
  - None.

## Validation Executed (Fill on completion)

### Environment
- OS: Windows 11
- Backend/Runtime: PowerShell

### Tests
| Test | Result | Evidence |
|---|---|---|
| Verify script & folder removal | Success | `mockups/` and `sync-filesystem.ps1` completely removed from workspace. |
| Checklists prune audit | Success | Verified `AGENTS.md` and `AI.md` have no active script bypass commands or visual mockup requirements. |
| Version bump validation | Success | Version `V0.4.0` successfully registered. |

### Final Result
`approved`
