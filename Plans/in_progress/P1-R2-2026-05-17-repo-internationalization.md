# P1-R2-2026-05-17-repo-internationalization

- **Description:** Translate all repository files and folders into English (internationalization), keeping README.md in a bilingual format (Portuguese and English).
- **Justification:** User request for internationalization of the repository, facilitating contributions from developers around the world.
- **Objective:** Establish an internationalized repository with translated file names, folders, and contents in English, and a bilingual README.md.
- **Scope:** All Markdown, HTML, and CSS files in the root and subfolders (Plans, governance, wiki, snippets, changelogs, etc.). Does not include the `.git` folder.
- **Affected files:** All files in the repository (renamed and translated).
- **Implementation plan:**
  1. Create the change plan in `Plans/pending/`.
  2. Move the plan to `Plans/in_progress/` and update status to `in_progress`.
  3. Translate and rename root files (except README.md, which will be translated and kept bilingual).
  4. Translate and rename files inside `governance`, `wiki`, `snippets`, `changelogs`, `Plans`, and other folders.
  5. Rename folders to their English names (`Planos` -> `Plans`, `governança` -> `governance`, `decisoes` -> `decisions`, etc.).
  6. Translate the change plan file itself into English.
  7. Update internal references in all files (markdown links, file references, indexes).
  8. Create the changelog `changelogs/V0.1.0.md` recording the changes.
  9. Validate the integrity of markdown links and coherence of translations.
  10. Complete the plan and move it to `Plans/completed/`.
- **Acceptance criteria:**
  - [ ] All files translated into English (with the exception of README.md which is bilingual).
  - [ ] All folders and files renamed into English.
  - [ ] Markdown links updated and working.
  - [ ] Document governance structure maintained in English (e.g., `AGENTS.md` translated, `MANIFEST.md` -> `MANIFEST.md`, etc.).
  - [ ] Changelog `changelogs/V0.1.0.md` created in English.
  - [ ] Change plan updated and moved to `Plans/completed/`.
- **Test plan:**
  - [ ] Manually verify links between main files.
  - [ ] Validate the integrity of the English structure based on the new governance rules.
- **Priority:** `P1` (Critical)
- **Risk:** `R2` (Medium-Low)
- **Current Version:** `V0.0.1`
- **Expected Version:** `V0.1.0`
- **Status:** `in_progress`
- **Creation Date:** 2026-05-17
- **Completion Date:** Not applicable.
- **Technical observations:**
  - The complete document structure will be kept, but its titles and directory names will be translated into English.
  - The README.md will have a Portuguese section followed by an English section, keeping both perfectly readable.

## Validation Executed (Fill on completion)

### Environment
- OS: Windows
- Backend/Runtime: PowerShell

### Tests
| Test | Result | Evidence |
|---|---|---|
| | | |

### Final Result
`pending`
