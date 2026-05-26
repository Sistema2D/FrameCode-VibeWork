# P2-R2-2026-05-22-fix-governance-consistency-v0-5-0

- **Description:** Correct governance/document consistency issues identified in the V0.5.0 pre-release audit.
- **Justification:** The repository has release-state, planning-state, and knowledge-link inconsistencies that can mislead agents and users (published status without tag, stale in-progress plan, broken wiki links, invalid session frontmatter, and non-portable absolute local links).
- **Objective:** Leave the framework in a coherent, portable, and lint-clean documentation state before publishing V0.5.0.
- **Scope:**
  - IN: plan lifecycle correction, changelog release status correction, wiki broken links fixes, session frontmatter normalization (S001-S004), and conversion of `file:///c:/Users/meloha/Desktop/FCVW/...` links to relative links.
  - OUT: source-code/runtime logic changes, release publishing/tagging actions.
- **Affected files:**
  - `Plans/in_progress/P1-R2-2026-05-17-repo-internationalization.md`
  - `Plans/completed/P1-R2-2026-05-17-repo-internationalization.md` (move target)
  - `changelogs/V0.5.0.md`
  - `wiki/index.md`
  - `wiki/patterns/aicc-session-compression.md`
  - `wiki/patterns/ase-jit-skill-loading.md` (create)
  - `wiki/sessions/S001-2026-05-18-ai-context-compression-implementation.md`
  - `wiki/sessions/S002-2026-05-18-integrate-token-estimations.md`
  - `wiki/sessions/S003-2026-05-18-implement-skills-engine.md`
  - `wiki/sessions/S004-2026-05-18-align-readme-directory-trees.md`
  - Markdown files containing absolute workspace links (`file:///c:/Users/meloha/Desktop/FCVW/...`)
- **Implementation plan:**
  1. Create this plan in `Plans/pending/`, then move it to `Plans/in_progress/` with status updated.
  2. Close stale internationalization plan: update status/details and move to `Plans/completed/`.
  3. Correct V0.5.0 changelog release state and include this consistency-fix batch.
  4. Resolve wiki broken links by removing stale references, fixing literal wikilink examples, and creating missing `ase-jit-skill-loading` page.
  5. Normalize session files S001-S004 to valid frontmatter-first structure and add sequential `session_number`.
  6. Convert all absolute workspace markdown links to relative links via deterministic script.
  7. Re-run link/frontmatter checks and record results.
  8. Update plan completion fields and move to `Plans/completed/`.
- **Acceptance criteria:**
  - [x] V0.5.0 changelog is not marked `published` unless tag/release exists.
  - [x] No stale high-level plan remains incorrectly in `Plans/in_progress/`.
  - [x] `wiki/index.md` has no broken `[[refactorings/complete-guide]]` link.
  - [x] `wiki/patterns/aicc-session-compression.md` no longer points to a missing page.
  - [x] Sessions S001-S004 start with YAML frontmatter and include `session_number`.
  - [x] Zero markdown links using local workspace `file:///...` URIs remain in `.md` files.
  - [x] Link/wikilink checks pass for non-template wiki pages.
- **Test plan:**
  - [x] Targeted scan confirms no markdown links still point to local workspace `file:///...` URIs.
  - [x] Frontmatter check script reports S001-S004 as frontmatter-first with `session_number`.
  - [x] Wikilink check reports zero unresolved links in non-template wiki pages.
  - [x] `git status -s` reflects the intended governance/documentation update scope.
- **Priority:** `P2` (High)
- **Risk:** `R2` (Low)
- **Current Version:** `V0.5.0`
- **Expected Version:** `V0.5.0`
- **Status:** `completed`
- **Creation Date:** 2026-05-22
- **Completion Date:** 2026-05-22
- **Technical observations:**
  - This batch is documentation/governance-only and intentionally avoids release publishing commands.
  - Relative-link normalization is required for cross-platform portability and repository relocatability.

## Validation Executed (Fill on completion)

### Environment
- OS: Windows
- Backend/Runtime: PowerShell

### Tests
| Test | Result | Evidence |
|---|---|---|
| Release status alignment | Success | `changelogs/V0.5.0.md` set to `in_preparation`; no local `v0.5.0` tag present. |
| Stale in-progress plan closure | Success | `P1-R2-2026-05-17-repo-internationalization.md` moved to `Plans/completed/` with status finalized. |
| Session frontmatter normalization | Success | S001-S004 start with `---` and include sequential `session_number` fields. |
| Internal markdown links | Success | `BrokenMarkdownLinks=0` (placeholder and external links excluded). |
| Wiki wikilinks | Success | `BrokenWikilinks=0` for non-template wiki pages. |
| Absolute workspace link portability | Success | `AbsoluteLinkMatches=0` for markdown links using `file:///c:/Users/meloha/Desktop/FCVW...`. |

### Final Result
`approved`

