# P3-R1-2026-05-18-token-estimations-readme-integration

- **Description:** Integrate estimated token consumption metrics for each mapped scenario (both Portuguese and English) into the project's README.md and AI.md.
- **Justification:** Gives developers clear visibility into API costs and highlights the concrete token-saving benefits of the AICC system.
- **Objective:** Establish bilingual token footprint tables inside the core documentation files.
- **Scope:**
  - Update [README.md](file:///c:/Users/meloha/Desktop/FCVW/README.md) to add "Token Footprint" sections in Portuguese and English.
  - Update [AI.md](file:///c:/Users/meloha/Desktop/FCVW/AI.md) to link to these estimates under the AICC guidelines.
  - Update [MANIFEST.md](file:///c:/Users/meloha/Desktop/FCVW/MANIFEST.md) and [STACK.md](file:///c:/Users/meloha/Desktop/FCVW/STACK.md) to bump the version to `V0.2.1`.
  - Create the version `V0.2.1` changelog.
- **Affected files:**
  - [`README.md`](file:///c:/Users/meloha/Desktop/FCVW/README.md)
  - [`AI.md`](file:///c:/Users/meloha/Desktop/FCVW/AI.md)
  - [`MANIFEST.md`](file:///c:/Users/meloha/Desktop/FCVW/MANIFEST.md)
  - [`STACK.md`](file:///c:/Users/meloha/Desktop/FCVW/STACK.md)
  - [`changelogs/V0.2.1.md`](file:///c:/Users/meloha/Desktop/FCVW/changelogs/V0.2.1.md)
- **Implementation plan:**
  1. Add Portuguese token estimations section to the Portuguese part of [README.md](file:///c:/Users/meloha/Desktop/FCVW/README.md).
  2. Add English token estimations section to the English part of [README.md](file:///c:/Users/meloha/Desktop/FCVW/README.md).
  3. Edit [AI.md](file:///c:/Users/meloha/Desktop/FCVW/AI.md) to integrate cross-links to these metrics.
  4. Edit [MANIFEST.md](file:///c:/Users/meloha/Desktop/FCVW/MANIFEST.md) and [STACK.md](file:///c:/Users/meloha/Desktop/FCVW/STACK.md) to bump the version to `V0.2.1`.
  5. Automatically synchronize tree architecture via `sync-filesystem.ps1`.
  6. Create `changelogs/V0.2.1.md`.
  7. Validate criteria and finalize plan into `Plans/completed/`.
- **Acceptance criteria:**
  - [x] Bilingual token footprint tables exist in [README.md](file:///c:/Users/meloha/Desktop/FCVW/README.md).
  - [x] Tables compare "Custo Inicial" vs "Custo Com AICC" accurately.
  - [x] `AI.md` references the README token metrics table.
  - [x] Version `V0.2.1` is declared in `MANIFEST.md`, `STACK.md`, and the changelogs.
- **Test plan:**
  - [x] Verify markdown links and rendering.
  - [x] Confirm no placeholder syntax remains in edited files.
- **Priority:** `P3` (Medium)
- **Risk:** `R1` (Very Low)
- **Current Version:** `V0.2.0`
- **Expected Version:** `V0.2.1`
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
| Bilingual Markdown Rendering | Success | Both Portuguese and English sections verified for layout, formatting, and heading alignment. |
| Link Cross-Doc Integrity | Success | Checked link destination in `AI.md` points precisely to target heading in `README.md`. |
| Directory Re-synchronization | Success | Re-ran script successfully to dynamic tree update validation. |

### Final Result
`approved`
