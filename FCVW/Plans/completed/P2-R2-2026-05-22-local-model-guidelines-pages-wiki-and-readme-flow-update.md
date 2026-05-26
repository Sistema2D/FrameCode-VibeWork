# P2-R2-2026-05-22-local-model-guidelines-pages-wiki-and-readme-flow-update

- **Description:** Add local AI model sizing recommendations to GitHub Pages and project Wiki (PT-BR/EN), align Pages visual language with NVIDIA design references, and validate/update README lifecycle flowchart.
- **Justification:** The user requested explicit operational guidance for local models and confirmation that README lifecycle flow remains real after recent documentation/publication changes.
- **Objective:** Deliver bilingual recommendations with actionable parameter/context thresholds, keep visuals aligned with NVIDIA-inspired design constraints, and ensure README lifecycle diagram matches current framework reality.
- **Scope:**
  - IN: `docs/index.html`, `README.md` lifecycle mermaid review/update, internal governance records, and external GitHub Wiki page updates.
  - OUT: runtime/framework logic changes and release publication.
- **Affected files:**
  - `docs/index.html`
  - `README.md`
  - `Plans/completed/P2-R2-2026-05-22-local-model-guidelines-pages-wiki-and-readme-flow-update.md`
  - `changelogs/V0.5.1.md`
  - `wiki/sessions/S010-2026-05-22-local-model-guidelines-pages-wiki-and-readme-flow-update.md`
  - `wiki/index.md`
  - `wiki/log.md`
  - GitHub Wiki repository pages (published via `FrameCode-VibeWork.wiki.git`)
- **Implementation plan:**
  1. Load NVIDIA `DESIGN.md` reference and map applicable tokens/principles to GitHub Pages styling.
  2. Add bilingual local-model recommendations (parameter and context window thresholds) to `docs/index.html`.
  3. Update/confirm README lifecycle mermaid flow for post-V0.5.0 reality; patch if needed.
  4. Add equivalent bilingual recommendations to GitHub Wiki pages and publish.
  5. Update changelog V0.5.1, session synthesis S010, wiki index/log, and finalize plan.
- **Acceptance criteria:**
  - [x] GitHub Pages content includes PT-BR/EN local-model recommendations with parameter and context guidance.
  - [x] Wiki contains equivalent bilingual guidance without mentioning model-serving services.
  - [x] `docs/index.html` follows NVIDIA-inspired visual constraints (palette, angular geometry, restrained elevation).
  - [x] README lifecycle mermaid is verified and updated if needed.
  - [x] Governance artifacts (plan, changelog, synthesis, wiki index/log) are updated.
- **Test plan:**
  - [x] Validate presence of recommendation sections in `docs/index.html` for both languages.
  - [x] Validate README mermaid blocks changed/confirmed with explicit rationale.
  - [x] Validate wiki pages updated and pushed.
  - [x] Run secret-pattern scan across modified files.
- **Priority:** `P2` (High)
- **Risk:** `R2` (Low)
- **Current Version:** `V0.5.1`
- **Expected Version:** `V0.5.1`
- **Status:** `completed`
- **Creation Date:** 2026-05-22
- **Completion Date:** 2026-05-22
- **Technical observations:**
  - GitHub Wiki is a separate git repository and was updated/published independently (`c70e389`).
  - GitHub Pages visual styling was normalized toward NVIDIA reference constraints (single green accent, 2px angular geometry, monochrome structure).

## Validation Executed

### Environment
- OS: Windows
- Backend/Runtime: PowerShell

### Tests
| Test | Result | Evidence |
|---|---|---|
| Page anchor integrity | pass | `TotalAnchors=24`, `MissingAnchors=0` in `docs/index.html` |
| Bilingual local-model sections | pass | `HasPtLocalSection=True`, `HasEnLocalSection=True` |
| NVIDIA visual constraints | pass | `#76b900` accent and `--radius: 2px` detected; no gradient/shadow decorative layer |
| README lifecycle flow update | pass | Mermaid blocks contain `Documentação pública/Public documentation (Wiki + GitHub Pages)` |
| Secret-pattern scan | pass | No credential-like matches in modified files |
| External Wiki publication | pass | `FrameCode-VibeWork.wiki.git` pushed (`e5c58b2..c70e389`) |

### Final Result
`completed`
