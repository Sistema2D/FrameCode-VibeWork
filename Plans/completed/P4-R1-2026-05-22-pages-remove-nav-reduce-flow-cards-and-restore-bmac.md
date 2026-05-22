# P4-R1-2026-05-22-pages-remove-nav-reduce-flow-cards-and-restore-bmac

- **Description:** Remove the side navigation section from GitHub Pages, reduce flowchart card width by around 50%, and restore the original Buy Me a Coffee button visual.
- **Justification:** User requested a simpler page without navigation, narrower flowchart cards, and restoration of the original Buy Me a Coffee branded button appearance.
- **Objective:** Deliver the three requested UI adjustments while preserving multilingual sections, anchors, and runtime language switching behavior.
- **Scope:**
  - IN: `docs/index.html` style/markup adjustments, governance records, and publication.
  - OUT: content rewrites outside the requested sections, runtime logic changes unrelated to the UI request.
- **Affected files:**
  - `docs/index.html`
  - `Plans/completed/P4-R1-2026-05-22-pages-remove-nav-reduce-flow-cards-and-restore-bmac.md`
  - `changelogs/V0.5.1.md`
  - `wiki/sessions/S014-2026-05-22-pages-remove-nav-reduce-flow-cards-and-restore-bmac.md`
  - `wiki/index.md`
  - `wiki/log.md`
- **Implementation plan:**
  1. Remove the `<nav>` block from `docs/index.html` and update layout styles to single-column content flow.
  2. Reduce flowchart card width by ~50% and keep mobile responsiveness.
  3. Restore original Buy Me a Coffee image-style button markup and matching styles.
  4. Validate script syntax, anchors, section counts, and requested visual adjustments.
  5. Update changelog/wiki records, close plan, commit, and push.
- **Acceptance criteria:**
  - [x] Navigation section is removed from the page.
  - [x] Flowchart cards are ~50% narrower than the current full-width cards.
  - [x] Buy Me a Coffee button uses the original visual style (image API button) again.
  - [x] Existing language sections remain valid across all supported languages.
  - [x] Changes are pushed to remote for GitHub Pages refresh.
- **Test plan:**
  - [x] Validate inline script syntax with Node parser.
  - [x] Validate article counts remain consistent across languages.
  - [x] Validate nav removal and Buy Me a Coffee markup restoration via text checks.
  - [x] Validate flowchart width reduction and mobile fallback via text checks.
  - [x] Validate no credential-like strings were introduced.
- **Priority:** `P4` (Low)
- **Risk:** `R1` (Very Low)
- **Current Version:** `V0.5.1`
- **Expected Version:** `V0.5.1`
- **Status:** `completed`
- **Creation Date:** 2026-05-22
- **Completion Date:** 2026-05-22
- **Technical observations:**
  - Static HTML/CSS/JS update only.

## Validation Executed (Fill on completion)

### Environment
- OS: Windows
- Backend/Runtime: PowerShell

### Tests
| Test | Result | Evidence |
|---|---|---|
| Script syntax parse | pass | `script_syntax=ok` |
| Navigation cleanup markers | pass | `nav_residual_markers=0` |
| Language article parity | pass | `articles_pt=12`, `articles_en=12`, `articles_es=12`, `articles_de=12` |
| Flowchart width constraints | pass | `flow_step_width_52=1`, `flow_loop_width_52=1`, `flow_mobile_width_100=1` |
| BuyMeACoffee visual restoration | pass | `bmac_image_button=1` |
| Secret-pattern scan | pass | `secret_scan=clear` |
| Remote publication | pass | `git push origin HEAD:main` |

### Final Result
`completed`

