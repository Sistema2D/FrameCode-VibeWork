# P3-R2-2026-05-22-pages-header-language-expansion-and-outline-renumbering

- **Description:** Update the GitHub Pages header, language selector, section numbering style, and page naming; add Spanish and German language versions.
- **Justification:** The user requested specific UX/content adjustments for the public page, including multilingual expansion and parity with the README support button.
- **Objective:** Deliver a four-language static page (PT-BR, EN, ES, DE) with flag-based language switch, updated title, removed slogan, refined outline numbering, and support button in the header.
- **Scope:**
  - IN: `docs/index.html` UI/content updates; governance records required by project rules.
  - OUT: framework runtime logic, repository wiki content changes, release publication.
- **Affected files:**
  - `docs/index.html`
  - `Plans/completed/P3-R2-2026-05-22-pages-header-language-expansion-and-outline-renumbering.md`
  - `changelogs/V0.5.1.md`
  - `wiki/sessions/S011-2026-05-22-pages-header-language-expansion-and-outline-renumbering.md`
  - `wiki/index.md`
  - `wiki/log.md`
- **Implementation plan:**
  1. Adjust top header: remove slogan text, rename page title, add flag-only language buttons, and insert support button beside language selector.
  2. Expand page content to ES and DE sections with equivalent structure to PT/EN.
  3. Replace linear `1)` style labels with hierarchical numeric style (`1.`, `1.1`, ..., `2.`, `2.1`, ...).
  4. Update language-switch script to support PT-BR, EN, ES, and DE.
  5. Update changelog and session synthesis artifacts, then validate anchors and language switching behavior.
- **Acceptance criteria:**
  - [x] Header no longer shows the requested slogan text.
  - [x] Language switch uses Brazil/UK/Spain/Germany flags and correctly toggles all four languages.
  - [x] Outline labels and section headings use hierarchical numbering style instead of `1)`, `2)`, `3)`.
  - [x] Main heading reads "Guia Completo do Framework" (and equivalent translations).
  - [x] Support button from README is present in the header to the right of language selector buttons.
- **Test plan:**
  - [x] Validate all language buttons toggle their corresponding section/nav.
  - [x] Validate anchor IDs referenced in all nav lists exist in the document.
  - [x] Validate no service-provider names were introduced in local-model guidance sections.
  - [x] Validate no credential-like strings were introduced.
- **Priority:** `P3` (Medium)
- **Risk:** `R2` (Low)
- **Current Version:** `V0.5.1`
- **Expected Version:** `V0.5.1`
- **Status:** `completed`
- **Creation Date:** 2026-05-22
- **Completion Date:** 2026-05-22
- **Technical observations:**
  - This change is static HTML/CSS/JS only.
  - Additional language sections increase page size but keep runtime complexity low.

## Validation Executed (Fill on completion)

### Environment
- OS: Windows
- Backend/Runtime: PowerShell

### Tests
| Test | Result | Evidence |
|---|---|---|
| Language selector coverage (4 languages) | pass | `data-lang` buttons for `pt-BR`, `en`, `es`, `de`; script `supportedLangs` includes all 4 values |
| Anchor integrity | pass | `anchors=48`, `missing=0` |
| Header requirements | pass | Old slogan removed, title updated, flags visible, support button present |
| Secret-pattern scan | pass | no credential-like string introduced; provider names scan returned no matches |

### Final Result
`completed`
