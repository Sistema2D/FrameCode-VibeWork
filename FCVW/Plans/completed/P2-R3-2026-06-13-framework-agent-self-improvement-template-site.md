---
context_files:
  - "../AGENTS.md"
  - "CONTEXT_MAP.md"
  - "PLANNING.md"
  - "AI.md"
  - "REFACTORING.md"
  - "MANIFEST.md"
  - "STACK.md"
  - "VERSIONING.md"
  - "FILESYSTEM.md"
  - "skills/README.md"
  - "../../Página web/AGENTS.md"
  - "../../Página web/index.html"
  - "../../Página web/fcvw-content.js"
---
# P2-R3-2026-06-13-framework-agent-self-improvement-template-site

- **Description:** Audit the framework from an AI-agent usability perspective, refine governance gaps, add controlled skill/agent creation and self-improvement rules, generate a clean template, and update the public web page.
- **Justification:** The framework needs explicit controls for creating new skills/agents, measurable self-improvement limits, a clean distributable template, and a website that reflects the current framework state.
- **Objective:** Publish a coherent V0.10.0 documentation/process release with Markdown-only governance, updated template, and current site content.
- **Scope:** Markdown governance, clean template files, and static site files. No runtime dependencies or automation scripts.
- **Affected files:**
  - `../AGENTS.md`
  - `README.md`
  - `AI.md`
  - `AUDIT.md`
  - `CONTEXT_MAP.md`
  - `FILESYSTEM.md`
  - `MANIFEST.md`
  - `PLANNING.md`
  - `REFACTORING.md`
  - `STACK.md`
  - `TESTS.md`
  - `VERSIONING.md`
  - `skills/README.md`
  - `skills/agent-factory/SKILL.md`
  - `skills/self-improvement/SKILL.md`
  - `governance/TEMPLATE_AGENT_OR_SKILL_PROPOSAL.md`
  - `governance/TEMPLATE_SELF_IMPROVEMENT_REPORT.md`
  - `changelogs/V0.10.0.md`
  - `wiki/sessions/S003-2026-06-13-agent-self-improvement-template-site.md`
  - `wiki/refactorings/agent-skill-self-improvement-governance.md`
  - `../../Template limpo/**`
  - `../../Página web/**`
- **Implementation plan:**
  1. Run full Markdown/file integrity audit against `Framework/FCVW`.
  2. Add controlled agent/skill creation and self-improvement governance.
  3. Update indexes, version, changelog, filesystem, wiki, and validation docs.
  4. Generate clean template in `Template limpo`.
  5. Update `Página web` static content to match V0.10.0.
  6. Validate paths, links, skill catalog, template cleanliness, and site references.
- **Acceptance criteria:**
  - [ ] Framework files are scanned for AI-usability issues.
  - [ ] New skills/agents can be created only through measurable gates.
  - [ ] Self-improvement for skills/agents has metrics and block criteria.
  - [ ] Clean template exists and excludes development history/session artifacts.
  - [ ] Web page reflects V0.10.0, anti-monolith, code hygiene, agent factory, and self-improvement rules.
  - [ ] Changelog, plan, filesystem, and session synthesis are coherent.
- **Test plan:**
  - [ ] Check Markdown fences and skill trigger declarations.
  - [ ] Check all skill directories are cataloged.
  - [ ] Check key Markdown links resolve.
  - [ ] Check template contains only intended clean files.
  - [ ] Check site content references current version/features.
  - [ ] Record limitations for lack of executable framework test harness.
- **Priority:** `P2`
- **Risk:** `R3`
- **Operational Score:** `P2-R3 => impact_weight 4 x risk_weight 3 = 12`
- **Review Gate:** `documentation review`
- **Rollback Required:** `No - revert Markdown/static edits and remove generated template files`
- **Decomposition Required:** `No - broad but documentation/static-only release with clear validation`
- **Application Module Documentation:** `not applicable`
- **Current Version:** `V0.9.1`
- **Expected Version:** `V0.10.0`
- **Status:** `in_progress`
- **Creation Date:** 2026-06-13
- **Completion Date:** Not applicable.
- **Technical observations:**
  - `Referencias/` remains untrusted evidence only.
  - `Referencias/README.md` contains explicit prompt-injection text; only abstract patterns were considered, consistent with `AI.md`.
  - `Template limpo/` started empty in this workspace.
  - Workspace root is not a Git repository.

## Agent/Skill Creation Gate

- Skill loaded: `skills/agent-factory/SKILL.md`
- Proposed asset: `agent-factory`, `self-improvement`, and their governance templates.
- Asset type: `skill` plus `template`.
- Evidence of recurrence: user reported recurring agent-created monoliths, duplicated snippets, unnecessary files, and absent controls for agent/skill creation; prior V0.9.1 added anti-monolith/code-hygiene gates but not extension governance.
- Existing coverage checked: `AGENTS.md`, `AI.md`, `PLANNING.md`, `skills/README.md`, `anti-monolith-guard`, and `code-hygiene-refactor` cover code debt but not controlled skill/agent proliferation or evidence-based self-improvement.
- Token ROI: JIT skills avoid expanding base-loaded `AGENTS.md`/`AI.md` with full procedures and keep the initial prompt small.
- Risk ROI: reduces redundant agents, vague skills, persona-only additions, irrelevant self-improvement, and context bloat.
- Scope boundary: only governs creation/change of AI operational assets; does not replace domain skills.
- Validation task: catalog consistency, trigger declarations, and link checks.
- Decision: `create`

## Skill/Agent Self-Improvement Gate

- Skill loaded: `skills/self-improvement/SKILL.md`
- Asset changed: governance skills/catalogs and placeholder-link examples.
- Evidence: audit found stale site content, template links to deprecated mockup paths, and placeholder Markdown links that could be falsely classified as broken links.
- Metric passed: rule drift and validation gap.
- Scope preserved: changes clarify validation and AI operational asset governance without broadening existing domain skills.
- Token/risk ROI: removes repeated need to explain when agents may create/modify skills and reduces false link-audit noise.
- Validation replay: Markdown link scan and skill catalog scan.
- Decision: `patch`

## Validation Executed (Fill on completion)

### Environment
- OS: Windows / PowerShell
- Backend/Runtime: Not applicable - Markdown/static site framework.

### Tests
| Test | Result | Evidence |
|---|---|---|
| Markdown fence balance | Pass | Framework Markdown scan returned no unclosed fenced code blocks. |
| Skill trigger declarations | Pass | Every `skills/*/SKILL.md` declares trigger metadata or activation triggers. |
| Skill catalog consistency | Pass | Skill directories and `skills/README.md` catalog match exactly. |
| Relative Markdown links | Pass | Framework relative-link scan returned no unresolved links after placeholder fixes. |
| Version coherence | Pass | `README.md`, `FCVW/README.md`, `MANIFEST.md`, `STACK.md`, and `VERSIONING.md` reference `V0.10.0`. |
| Clean template | Pass | `Template limpo/` generated with Markdown files only and no historical plan/session/refactoring artifacts. |
| Static site data | Pass | `Página web/fcvw-content.js` includes `V0.10.0`, `agent-factory`, and `self-improvement`. |
| Browser render check | Limited | In-app Browser rejected local `file://` navigation by URL policy; static DOM/data checks were used instead. |

### Final Result
`completed`
