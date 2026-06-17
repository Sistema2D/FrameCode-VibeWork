# LLM Wiki Log

Chronological log of relevant wiki events.

Clean distributions should use `Template limpo/` as the empty baseline when generated or distributed outside the canonical framework tree. This working framework repository may record framework-evolution events.

---

## Recommended Format

```markdown
## [YYYY-MM-DD HH:MM] <type> | <short title>

- Source:
- Executed action:
- Pages created:
- Pages updated:
- Pages obsolete:
- Result:
- Gaps:
```

---

## Event Types

- `init`: initialization of the wiki.
- `ingest`: entry of new source.
- `synthesis`: creation or update of synthesis.
- `promotion`: promotion of record to reusable knowledge.
- `lint`: structural check of the wiki.
- `audit`: learning derived from audit.
- `failure`: learning derived from troubleshooting.
- `refactoring`: learning derived from refactoring.
- `release`: learning derived from release.
- `decision`: consolidated decision.
- `obsolete`: marking page as obsolete.
- `contradiction`: identified contradiction.
- `maintenance`: general maintenance.

---

## Records

## [2026-06-17 09:00] release | V0.10.3 release governance JIT fixes

- Source: user-requested correction patch after V0.10.2 release review.
- Executed action: corrected completed plan status, normalized V0.10.2 changelog schema, created V0.10.3 changelog, expanded Portuguese JIT triggers, strengthened release-checklist activation, and added plan-state coherence checks.
- Pages created:
  - `wiki/sessions/S006-2026-06-17-v0103-release-governance-jit-fixes.md`
- Pages updated:
  - `wiki/index.md`
  - `wiki/log.md`
- Pages obsolete: none.
- Result: governance release flow and skill activation coverage improved without adding scripts or runtime dependencies.
- Gaps: GitHub Release/tag was not published; changelog records `GitHub Release Status: not_applicable`.

## [2026-06-14 10:30] audit | Final compliance QA

- Source: user-requested final compliance and QA review.
- Executed action: removed false broken wikilinks from wiki examples/templates, restored resolvable site mirror subdirectories, updated version references, and refreshed validation artifacts.
- Pages created:
  - `wiki/sessions/S005-2026-06-14-final-compliance-qa.md`
- Pages updated:
  - `wiki/index.md`
  - `wiki/log.md`
- Pages obsolete: none.
- Result: final compliance checks now pass across framework, clean template, and static site mirror.
- Gaps: none material in the audited scope.

## [2026-06-14 09:00] maintenance | V0.10.1 cleanup optimization

- Source: follow-up audit of V0.10.0 scope.
- Executed action: removed raw HTML from Markdown READMEs, reduced static site content from embedded Markdown bodies to a manifest, and sanitized the clean template manifest.
- Pages created:
  - `wiki/sessions/S004-2026-06-13-v0101-cleanup-optimization.md`
- Pages updated:
  - `wiki/index.md`
  - `wiki/log.md`
- Pages obsolete: none.
- Result: Markdown purity, static site size, and clean-template quality improved without changing framework philosophy.
- Gaps: browser verification should use a local HTTP server because `file://` may be blocked.

## [2026-06-13 18:00] governance | Agent factory, self-improvement, clean template, and site

- Source: user-requested framework audit and refinement.
- Executed action: added controlled creation and self-improvement gates for skills/agents, repaired AI-usability template issues, generated clean template, and refreshed the public web page.
- Pages created:
  - `wiki/refactorings/agent-skill-self-improvement-governance.md`
  - `wiki/sessions/S003-2026-06-13-agent-self-improvement-template-site.md`
- Pages updated:
  - `wiki/index.md`
  - `wiki/log.md`
- Pages obsolete: none.
- Result: skill/agent growth now requires recurrence, coverage, token/risk ROI, scope, and validation metrics.
- Gaps: framework validation remains Markdown-only and declarative by ADR-0001.

## [2026-06-13 16:00] refactoring | Anti-monolith and code hygiene gates

- Source: user request to make the framework block monolith creation and actively clean duplication, stale files, dead code, and unnecessary artifacts.
- Executed action: added anti-monolith and code hygiene skills, updated planning/refactoring/retroactive instantiation gates, made domain agents tool-aware, and recorded V0.9.1.
- Pages created:
  - `wiki/refactorings/anti-monolith-and-code-hygiene-gates.md`
  - `wiki/sessions/S002-2026-06-13-anti-monolith-code-hygiene.md`
- Pages updated:
  - `wiki/index.md`
  - `wiki/log.md`
- Pages obsolete: none.
- Result: agents now have Markdown-only gates before large module creation and cleanup/refactoring work.
- Gaps: historical encoding artifacts remain in older documents.

## [2026-06-05 15:30] maintenance | Open governance issues treatment

- Source: user request to treat GitHub issues #27, #28, and #29 according to prior triage.
- Executed action: added operational priority/risk gates, application module documentation governance/templates, centralized agent journals, and prepared `V0.8.0`.
- Pages created:
  - `wiki/agents/README.md`
  - `wiki/sessions/S010-2026-06-05-open-governance-issues.md`
- Pages updated:
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/schema.md`
- Pages obsolete: none.
- Result: open governance issues are treated locally in the framework baseline.
- Gaps: remote GitHub issues remain open until these local changes are synchronized to the repository and reviewed.

## [2026-06-05 14:30] maintenance | Framework docs artifacts removal

- Source: user request to remove root `docs/`, move GitHub Pages elsewhere, remove `FCVW/docs/index.html`, and verify package files.
- Executed action: removed framework docs site artifacts, removed obsolete Node/Jest harness, removed stale PR description, updated official baseline documents, published `V0.7.9`, and refreshed session memory.
- Pages created:
  - `wiki/sessions/S009-2026-06-05-remove-framework-docs-artifacts.md`
- Pages updated:
  - `wiki/index.md`
  - `wiki/log.md`
- Pages obsolete:
  - `docs/`
  - `FCVW/docs/`
  - root Node/Jest docs-test harness
- Result: framework baseline is pure Markdown again; public documentation publication is external to this repository.
- Gaps: GitHub issues #27, #28, and #29 remain open for separate governed plans.
