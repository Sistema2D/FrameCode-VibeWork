# P3-R1-2026-05-22-readme-and-stack-sync-v0.5.0

- **Description:** Sync README.md and STACK.md to reflect the V0.5.0 state of the framework.
- **Justification:** Post-V0.5.0 audit revealed two files not updated during the optimization session: (1) README.md lacks CONTEXT_MAP.md in directory trees, new skills in catalog, updated token table, and version reference; (2) STACK.md still shows V0.4.0 and unresolved placeholders.
- **Objective:** README.md and STACK.md accurately represent the current V0.5.0 framework state.
- **Scope:**
  - IN: README.md, STACK.md
  - OUT: all other files
- **Affected files:**
  - `README.md` (modified)
  - `STACK.md` (modified)
- **Implementation plan:**
  1. Update README.md PT section: directory tree (add CONTEXT_MAP.md, expand skills/, update wiki/), add 6th pillar (ASE), update token table with Release scenario, update version
  2. Update README.md EN section: same changes mirrored
  3. Update STACK.md: fill all placeholders with FCVW framework information, bump version to V0.5.0
  4. Update changelogs/V0.5.0.md to include these files
- **Acceptance criteria:**
  - [x] README.md directory trees include CONTEXT_MAP.md (both PT and EN)
  - [x] README.md skills/ tree shows all 4 skills
  - [x] README.md token table includes Release scenario with skill reference
  - [x] STACK.md version is V0.5.0
  - [x] STACK.md has no `<placeholder>` fields
- **Test plan:**
  - [x] Grep CONTEXT_MAP in README.md — 2 matches (PT + EN)
  - [x] Grep `<` in STACK.md — zero non-intentional matches
- **Priority:** `P3` (Medium)
- **Risk:** `R1` (Very Low — documentation only)
- **Current Version:** `V0.5.0`
- **Expected Version:** `V0.5.0` (patch, no bump needed — within same release scope)
- **Status:** `completed`
- **Creation Date:** 2026-05-22
- **Completion Date:** 2026-05-22
- **Technical observations:**
  - STACK.md is designed as a template for downstream projects but still describes the framework itself at root level — fill it accordingly (like MANIFEST.md was filled).
  - README.md is public-facing — the directory trees must exactly match the physical filesystem to avoid confusion for new users cloning the repo.
