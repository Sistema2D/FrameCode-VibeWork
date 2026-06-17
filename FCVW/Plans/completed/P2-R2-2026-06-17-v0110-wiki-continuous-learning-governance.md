---
context_files:
  - "AGENTS.md"
  - "README.md"
  - "FCVW/AI.md"
  - "FCVW/CONTEXT_MAP.md"
  - "FCVW/MANIFEST.md"
  - "FCVW/STACK.md"
  - "FCVW/VERSIONING.md"
  - "FCVW/wiki/schema.md"
  - "FCVW/wiki/README.md"
  - "FCVW/wiki/index.md"
  - "FCVW/wiki/log.md"
  - "FCVW/skills/README.md"
  - "FCVW/skills/release-checklist/SKILL.md"
  - "FCVW/skills/governance-validator/SKILL.md"
  - "FCVW/skills/agent-factory/SKILL.md"
  - "FCVW/skills/self-improvement/SKILL.md"
  - "FCVW/skills/wiki-lint/SKILL.md"
---
# P2-R2-2026-06-17-v0110-wiki-continuous-learning-governance

- **Description:** Add governed continuous-learning support for the LLM Wiki through a dedicated wiki curation skill, taxonomy, metrics, schema updates, and release records.
- **Justification:** The framework already had Ingest/Query/Lint, but lacked an explicit low-cost AI curation loop for incorporating new knowledge, revising existing pages, clustering related notes, and managing thematic frontmatter metadata.
- **Objective:** Ensure future AI agents can keep the wiki evolving continuously while preserving on-demand updates, measurable freshness, and low token cost.
- **Scope:** Include wiki curation governance, fixed optimized cost mode, skill/catalog updates, taxonomy/metrics pages, version bump, changelog, session synthesis, and release synthesis. Exclude runtime code, external services, automation scripts, and bulk retagging of historical wiki pages.
- **Affected files:**
  - `AGENTS.md`
  - `README.md`
  - `FCVW/README.md`
  - `FCVW/AI.md`
  - `FCVW/AUDIT.md`
  - `FCVW/CONTEXT_MAP.md`
  - `FCVW/FILESYSTEM.md`
  - `FCVW/MANIFEST.md`
  - `FCVW/STACK.md`
  - `FCVW/TESTS.md`
  - `FCVW/VERSIONING.md`
  - `FCVW/changelogs/V0.11.0.md`
  - `FCVW/skills/README.md`
  - `FCVW/skills/wiki-curator/SKILL.md`
  - `FCVW/skills/wiki-lint/SKILL.md`
  - `FCVW/wiki/index.md`
  - `FCVW/wiki/log.md`
  - `FCVW/wiki/metrics.md`
  - `FCVW/wiki/README.md`
  - `FCVW/wiki/releases/v0-11-0-summary.md`
  - `FCVW/wiki/schema.md`
  - `FCVW/wiki/sessions/S007-2026-06-17-v0110-wiki-continuous-learning-governance.md`
  - `FCVW/wiki/taxonomy.md`
- **Implementation plan:**
  1. Add `wiki-curator` skill with a fixed optimized cost mode.
  2. Add wiki taxonomy and metrics pages.
  3. Extend `AI.md` and `wiki/schema.md` with continuous curation, metadata, and metric rules.
  4. Update catalogs, context map, stack, README files, audit/test rules, manifest, versioning, wiki-lint type coverage, changelog, session, and release synthesis.
  5. Regenerate `FILESYSTEM.md` and validate governance coherence.
- **Acceptance criteria:**
  - [x] New curation flow is documented as JIT and low-cost.
  - [x] Only one standard optimized cost mode is exposed.
  - [x] Tags/themes/frontmatter colors have a canonical taxonomy.
  - [x] Metrics define freshness, duplication, taxonomy coverage, and release synthesis coverage.
  - [x] Skill catalog, stack, context map, wiki index, log, changelog, and version references are coherent.
  - [x] GitHub Release `v0.11.0` is prepared after merge.
- **Test plan:**
  - [x] Execute `git diff --check`.
  - [x] Execute wiki structural lint for minor release.
  - [x] Execute governance validation for skill catalog, plan state, version coherence, and filesystem coverage.
  - [x] Verify release asset and GitHub release after publication.
- **Priority:** `P2`
- **Risk:** `R2`
- **Operational Score:** `P2-R2 => impact_weight 4 x risk_weight 2 = 8`
- **Review Gate:** `documentation review / self-review acceptable`
- **Rollback Required:** `No - revert release commit and delete GitHub tag/release if publication must be withdrawn`
- **Decomposition Required:** `No`
- **Application Module Documentation:** `not applicable`
- **Current Version:** `V0.10.3`
- **Expected Version:** `V0.11.0`
- **Status:** `completed`
- **Creation Date:** 2026-06-17
- **Completion Date:** 2026-06-17
- **Technical observations:**
  - The release is minor because it adds a new skill and wiki governance pages.
  - Historical wiki pages were not bulk-retagged to preserve low-cost behavior and avoid unrelated churn.

## Agent/Skill Creation Gate

- Skill loaded: `skills/agent-factory/SKILL.md`
- Proposed asset: `skills/wiki-curator/SKILL.md`
- Asset type: `skill`
- Evidence of recurrence: user requested continuous wiki evolution; existing release/wiki flow repeatedly creates sessions/changelogs without a dedicated curation loop.
- Existing coverage checked: `wiki-lint` validates structure, `aicc-compact` compresses sessions, and `memory-rotation` controls old sessions, but no existing skill owns promotion, clustering, metrics, and thematic frontmatter curation end to end.
- Token ROI: avoids adding a long curation procedure to `AGENTS.md`, `AI.md`, and `wiki/schema.md`; keeps curation JIT.
- Risk ROI: reduces stale wiki, duplicate notes, unpromoted release learning, and inconsistent tag/theme metadata.
- Scope boundary: one trigger family (`wiki/knowledge curation`), one primary output (`curated wiki updates with metrics`), one validation path (`wiki-lint` + governance checks).
- Validation task: replay this release by checking that new wiki pages, taxonomy, metrics, index, log, and release synthesis are coherent.
- Decision: `create`

## Skill/Agent Self-Improvement Gate

- Skill loaded: `skills/self-improvement/SKILL.md`
- Asset changed: skill catalog, routing documents, and `skills/wiki-lint/SKILL.md`
- Evidence: new canonical skill changes ASE routing and AICC session pages use `type: "session"`, which wiki-lint must recognize to avoid false positives.
- Metric passed: rule drift/catalog coverage; token ROI through JIT routing; validation gap closed for session frontmatter.
- Scope preserved: no existing skill responsibility was broadened.
- Token/risk ROI: reduces repeated manual wiki-curation instructions, catalog drift, and false lint findings.
- Validation replay: catalog consistency checked against physical `skills/*/SKILL.md`.
- Decision: `patch`

## Validation Executed

### Environment
- OS: Windows / PowerShell
- Backend/Runtime: Markdown-only framework; no runtime build.

### Tests
| Test | Result | Evidence |
|---|---|---|
| GitHub source verification | passed | `gh repo view` confirmed `v0.10.3` as latest release before edits; clean clone at `fdab188`. |
| `git diff --check` | passed | No whitespace errors. |
| Wiki lint | passed | New wiki pages have required frontmatter; index/log/release synthesis updated; no new broken wiki links found. |
| Governance validation | passed | Skill catalog, version coherence, plan status, changelog, and filesystem coverage checked. |
| Release asset preparation | passed | Clean-template asset generation and GitHub publication are executed after PR merge and verified in the release workflow. |

### Final Result
`approved`
