# P2-R2-2026-05-22-framework-optimization-and-ase-expansion

- **Description:** Apply all optimization (OPT-1 to OPT-4) and new feature (FEAT-1 to FEAT-4, FEAT-6) items identified in the framework architectural analysis session of 2026-05-22.
- **Justification:** Multiple gaps and opportunities were formally identified in the repository analysis: unfilled placeholders block agent context, the wiki is structurally sound but empty, the ASE has only one skill, and the AICC templates are duplicated with inconsistencies. This plan resolves all identified items in a single coordinated session.
- **Objective:** Bring the framework to a fully operational, self-consistent V0.5.0 state — with populated manifest/scope, a live wiki, an expanded ASE (3 new skills), a CONTEXT_MAP.md for session optimization, a formal troubleshooting template, and all document inconsistencies resolved.
- **Scope:**
  - IN: MANIFEST.md, SCOPE.md, wiki/index.md, wiki/log.md, wiki/index.md, wiki/sessions/S006 frontmatter, governance templates, skills/, CONTEXT_MAP.md
  - OUT: any changes to application source code, DESIGN.md visual tokens, SECURITY.md, DATA.md
- **Affected files:**
  - `MANIFEST.md` (modified)
  - `SCOPE.md` (modified)
  - `wiki/index.md` (modified)
  - `wiki/log.md` (modified)
  - `wiki/sessions/S006-*.md` (frontmatter fix)
  - `wiki/patterns/aicc-session-compression.md` (created)
  - `wiki/decisions/adr-0001-pure-markdown.md` (created)
  - `wiki/releases/v0-4-0.md` (created)
  - `governance/TEMPLATE_AI_SESSION_SYNTHESIS.md` (modified — add session_number field)
  - `wiki/templates/TEMPLATE_SESSION_SYNTHESIS.md` (modified — align with governance template)
  - `governance/TEMPLATE_TROUBLESHOOTING.md` (created)
  - `TROUBLESHOOTING.md` (modified — reference new template)
  - `CONTEXT_MAP.md` (created)
  - `AGENTS.md` (modified — reference CONTEXT_MAP.md)
  - `skills/git-conventional-commits/SKILL.md` (created)
  - `skills/wiki-lint/SKILL.md` (created)
  - `skills/release-checklist/SKILL.md` (created)
  - `skills/README.md` (modified — register 3 new skills)
  - `Plans/pending/P2-R2-2026-05-22-publish-v0.4.0.md` (created)
  - `changelogs/V0.5.0.md` (created)
  - `MANIFEST.md` version bump to V0.5.0
- **Implementation plan:**
  1. Create `Plans/pending/P2-R2-2026-05-22-publish-v0.4.0.md` (OPT-4)
  2. Fill placeholders in `MANIFEST.md` and `SCOPE.md`; fix wiki/index.md broken link (OPT-1)
  3. Fix S006 frontmatter YAML; unify AICC templates (OPT-3)
  4. Create wiki knowledge pages: patterns/aicc, decisions/adr-0001, releases/v0-4-0 (OPT-2)
  5. Update wiki/index.md and wiki/log.md to reflect new pages (OPT-2)
  6. Create skill: git-conventional-commits (FEAT-1)
  7. Create skill: wiki-lint (FEAT-2)
  8. Create skill: release-checklist (FEAT-3)
  9. Update skills/README.md to register 3 new skills (FEAT-1/2/3)
  10. Create CONTEXT_MAP.md (FEAT-6)
  11. Create governance/TEMPLATE_TROUBLESHOOTING.md; update TROUBLESHOOTING.md (FEAT-4)
  12. Update AGENTS.md to reference CONTEXT_MAP.md
  13. Create changelogs/V0.5.0.md and bump MANIFEST.md to V0.5.0
  14. Create AICC session synthesis S007
- **Acceptance criteria:**
  - [x] MANIFEST.md has no `<placeholder>` fields
  - [x] SCOPE.md has no `<placeholder>` fields
  - [x] wiki/index.md has no reference to deprecated mockups/
  - [x] S006 has valid YAML frontmatter
  - [x] governance/ and wiki/templates/ AICC templates are structurally aligned
  - [x] wiki/ contains at least 3 new knowledge pages with valid frontmatter
  - [x] skills/ has 3 new skill directories with SKILL.md
  - [x] skills/README.md lists all 4 active skills
  - [x] CONTEXT_MAP.md exists at root
  - [x] governance/TEMPLATE_TROUBLESHOOTING.md exists
  - [x] Plans/discontinued/ contains the V0.4.0 publish plan (discontinued — V0.4.0 already published)
  - [x] changelogs/V0.5.0.md exists
  - [x] MANIFEST.md version is V0.5.0
- **Test plan:**
  - [x] Grep `<` in MANIFEST.md and SCOPE.md — zero non-intentional matches
  - [x] Grep `mockups/` in wiki/index.md — zero matches
  - [x] YAML frontmatter verified in all 3 new wiki pages
  - [x] All 4 SKILL.md files contain Triggers section — verified by PowerShell grep
- **Priority:** `P2` (High)
- **Risk:** `R2` (Low — pure documentation changes, no code logic)
- **Current Version:** `V0.4.0`
- **Expected Version:** `V0.5.0`
- **Status:** `completed`
- **Creation Date:** 2026-05-22
- **Completion Date:** 2026-05-22
- **Technical observations:**
  - The framework IS the product — MANIFEST.md and SCOPE.md describe the framework itself, not a downstream application.
  - The two AICC templates (governance/ and wiki/templates/) are structurally identical; the governance/ version is the authoritative one (referenced by AI.md). The wiki/templates/ version serves as the canonical copy inside the wiki. Both should remain but be kept in sync.
  - ADR-0001 decided against automation scripts; new skills follow the Pure Markdown model (no scripts).
