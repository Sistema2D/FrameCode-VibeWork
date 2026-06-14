---
context_files:
  - "../AGENTS.md"
  - "PLANNING.md"
  - "AI.md"
  - "FILESYSTEM.md"
  - "VERSIONING.md"
  - "../../Página web/AGENTS.md"
  - "../../Página web/docs.html"
  - "../../Página web/fcvw-content.js"
  - "../../Template limpo/**"
---
# P3-R2-2026-06-13-v0101-cleanup-optimization

- **Description:** Apply follow-up cleanup and optimization after V0.10.0, focusing on raw HTML in Markdown, static-site data size, and clean-template history leakage.
- **Justification:** A second audit found material improvements still inside the current scope: README files used raw HTML, `fcvw-content.js` embedded all Markdown as a large generated monolith, and `Template limpo/FCVW/MANIFEST.md` still carried framework-development history.
- **Objective:** Publish V0.10.1 as a focused cleanup patch that strengthens Markdown purity, anti-monolith behavior, and clean-template distribution quality.
- **Scope:** Markdown documentation, generated clean template, and static site data/loading behavior.
- **Affected files:**
  - `README.md`
  - `FCVW/README.md`
  - `FCVW/MANIFEST.md`
  - `FCVW/STACK.md`
  - `FCVW/VERSIONING.md`
  - `FCVW/CONTEXT_MAP.md`
  - `FCVW/FILESYSTEM.md`
  - `FCVW/changelogs/V0.10.1.md`
  - `FCVW/wiki/sessions/S004-2026-06-13-v0101-cleanup-optimization.md`
  - `../../Template limpo/**`
  - `../../Página web/**`
- **Implementation plan:**
  1. Remove raw HTML from framework Markdown READMEs.
  2. Replace embedded site Markdown blob with small manifest and lazy Markdown fetch.
  3. Sanitize clean-template manifest and regenerate template tree.
  4. Update version references, changelog, session synthesis, and filesystem tree.
  5. Validate Markdown, links, site behavior, template cleanliness, and version coherence.
- **Acceptance criteria:**
  - [ ] Framework READMEs avoid raw HTML for images/support links.
  - [ ] `Página web/fcvw-content.js` is no longer a large embedded-content monolith.
  - [ ] `Template limpo/FCVW/MANIFEST.md` has no framework-development history leakage.
  - [ ] Current version references are coherent at `V0.10.1`.
  - [ ] Site documents still render via the docs page when served locally.
- **Test plan:**
  - [ ] Markdown fence scan.
  - [ ] Raw HTML scan for non-template Markdown content.
  - [ ] Skill catalog consistency scan.
  - [ ] Relative Markdown link scan.
  - [ ] Clean-template Markdown-only/history scan.
  - [ ] Static site data-size and localhost browser check.
- **Priority:** `P3`
- **Risk:** `R2`
- **Operational Score:** `P3-R2 => impact_weight 3 x risk_weight 2 = 6`
- **Review Gate:** `self-review`
- **Rollback Required:** `No - revert documentation/static site patch`
- **Decomposition Required:** `No - small cleanup patch`
- **Application Module Documentation:** `not applicable`
- **Current Version:** `V0.10.0`
- **Expected Version:** `V0.10.1`
- **Status:** `in_progress`
- **Creation Date:** 2026-06-13
- **Completion Date:** 2026-06-14

## Anti-Monolith Gate

- Skill loaded: `skills/anti-monolith-guard/SKILL.md`
- Target artifact: `Página web/fcvw-content.js`
- Primary responsibility: expose site metadata and a document manifest.
- Explicit non-responsibilities: store full Markdown document bodies or duplicate canonical documentation content.
- Size budget: keep generated JS under 25 KB by loading Markdown files lazily from the existing mirrored `.md` files.
- Similar code checked: existing `docs.html` already has a viewer and site folder already mirrors `.md` documents.
- Split decision: `proceed`
- Validation: static size check and localhost browser check.

## Code Hygiene Scan

- Skill loaded: `skills/code-hygiene-refactor/SKILL.md`
- Scan level: `module`
- Duplicate candidates: Markdown content duplicated inside both `.md` files and `fcvw-content.js`.
- Large/monolithic candidates: `Página web/fcvw-content.js` at more than 230 KB.
- Dead/stale candidates: raw HTML image/support snippets in Markdown READMEs; historical manifest content inside clean template.
- Cleanup batch selected: manifest-only site data, lazy Markdown fetch, sanitized clean manifest, Markdown-native README links.
- Behavior preservation evidence: docs list remains generated from current mirrored Markdown files; viewer fetches selected document on demand.
- Deferred debt: none.

## Validation Executed

### Environment

- OS: Windows / PowerShell
- Site validation target: `http://127.0.0.1:8765/`

### Tests

| Test | Result | Evidence |
|---|---|---|
| Markdown fence scan | Pass | No unclosed fenced code blocks in framework, template, or site Markdown. |
| Raw HTML scan | Pass | No anchor, image, script, iframe, or style HTML tags in non-template Markdown content. |
| Skill catalog consistency | Pass | `skills/README.md` matches all `skills/*/SKILL.md` directories. |
| Relative Markdown links | Pass | Framework relative links resolve or are intentional placeholders/external links. |
| Version coherence | Pass | Framework, site, and clean template current-version references use `V0.10.1`. |
| Clean-template hygiene | Pass | `Template limpo/` remains Markdown-only and has no historical plan/session/refactoring artifacts. |
| Clean-template manifest | Pass | `Template limpo/FCVW/MANIFEST.md` has no old framework release history or plan references. |
| Site manifest size | Pass | `Página web/fcvw-content.js` is 8,454 bytes and has no embedded `markdownFiles` blob. |
| Browser check | Pass | `index.html` and `docs.html` loaded over local HTTP; docs viewer rendered 26 documents with no console errors. |

### Final Result

`completed`
