# P3-R2-2026-05-22-pages-accordion-quickstart-flowchart-and-es-de-parity

- **Description:** Refine GitHub Pages UX/content by simplifying header badges, converting navigation groups into single-open accordions, updating quick-start guidance to AGENTS.md-driven AI flow, replacing lifecycle prose with framework flowchart, and improving ES/DE parity.
- **Justification:** The public page must be more direct and polished for human users while preserving framework governance guidance and multilingual consistency.
- **Objective:** Deliver a cleaner multilingual page where navigation is language-scoped and accordion-driven, quick start is AI-assisted via AGENTS.md mention, lifecycle sections use the official framework flowchart, and ES/DE sections match PT/EN topical completeness.
- **Scope:**
  - IN: `docs/index.html` UI/content/behavior updates; governance artifacts required by process; GitHub publication via standard branch push.
  - OUT: runtime/framework logic changes, non-page refactors, release status transition.
- **Affected files:**
  - `docs/index.html`
  - `Plans/completed/P3-R2-2026-05-22-pages-accordion-quickstart-flowchart-and-es-de-parity.md`
  - `changelogs/V0.5.1.md`
  - `wiki/sessions/S012-2026-05-22-pages-accordion-quickstart-flowchart-and-es-de-parity.md`
  - `wiki/index.md`
  - `wiki/log.md`
- **Implementation plan:**
  1. Remove extra top badges so only `Version: V0.5.0+` remains.
  2. Refactor navigation into accordion groups that allow only one expanded topic at a time and keep only selected-language topics visible.
  3. Rewrite `3.4` quick-start guidance in PT/EN/ES/DE to emphasize “mention AGENTS.md to the AI in your IDE and request the task”.
  4. Replace lifecycle text blocks (`1.3`) with framework flowcharts aligned with README lifecycle logic.
  5. Expand ES/DE sections to include all major topic details currently present in PT/EN, preserving anchor structure.
  6. Update changelog/wiki synthesis records, validate anchors/accordion/language behavior, and publish via git push.
- **Acceptance criteria:**
  - [x] Header badges show only `Version: V0.5.0+`.
  - [x] Navigation is accordion-based with exactly one open group per language nav at any time.
  - [x] Navigation displays only the selected language topics.
  - [x] Quick-start content is updated to AGENTS.md-driven AI-guided execution in all languages.
  - [x] Lifecycle sections use a flowchart representation of framework operation in all languages.
  - [x] ES/DE sections have full topical parity quality with PT/EN for listed topics.
  - [x] Changes are pushed to remote so GitHub Pages can update.
- **Test plan:**
  - [x] Validate only one accordion group can remain open after repeated toggles.
  - [x] Validate language switch hides/shows both content and corresponding nav.
  - [x] Validate all nav anchors resolve to existing section IDs.
  - [x] Validate quick-start wording no longer requires manual instantiation-first flow as primary path.
  - [x] Validate flowchart blocks exist for PT/EN/ES/DE lifecycle sections.
  - [x] Validate no credential-like strings were introduced.
- **Priority:** `P3` (Medium)
- **Risk:** `R2` (Low)
- **Current Version:** `V0.5.1`
- **Expected Version:** `V0.5.1`
- **Status:** `completed`
- **Creation Date:** 2026-05-22
- **Completion Date:** 2026-05-22
- **Technical observations:**
  - Static HTML/CSS/JS changes only.
  - GitHub Pages publication occurs via push to the configured source branch (`main`) with `/docs`.

## Validation Executed (Fill on completion)

### Environment
- OS: Windows
- Backend/Runtime: PowerShell

### Tests
| Test | Result | Evidence |
|---|---|---|
| Badge cleanup check | pass | `badge_count=1` and removed tag strings count = 0 |
| Anchor integrity check | pass | `anchors=48`, `missing=0` |
| Language section parity count | pass | `articles_pt=12`, `articles_en=12`, `articles_es=12`, `articles_de=12` |
| Script syntax parse | pass | `script_syntax=ok` (Node parse via `new Function`) |
| Accordion logic verification | pass | `ensureSingleOpen` enforces single open group per language nav |
| Remote publication | pass | `git push origin main` executed successfully |

### Final Result
`completed`
