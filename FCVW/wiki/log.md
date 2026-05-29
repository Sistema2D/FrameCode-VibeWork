# LLM Wiki Log

Chronological log of relevant wiki events.

This repository is intentionally distributed with a clean wiki baseline. Register events from your own project lifecycle.

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

## [2026-05-29 13:30] audit | Audit follow-up cleanup

- Source: framework structure audit follow-up request.
- Executed action: removed obsolete `FCVW/pr_description.txt`, documented `FCVW/docs/` publication rules, added root-ownership audit check, reduced duplicate structure declarations, and backfilled `V0.7.0` through `V0.7.4` changelogs.
- Pages created:
  - `wiki/sessions/S004-2026-05-29-audit-follow-up-cleanup.md`
- Pages updated:
  - `wiki/index.md`
  - `wiki/log.md`
- Pages obsolete: none.
- Result: actionable audit follow-up items resolved; historical references to removed paths preserved as evidence.
- Gaps: hosting-specific export from `FCVW/docs/` remains a release-process decision.

## [2026-05-29 13:00] audit | Root and snippets deprecation

- Source: user-requested framework structure review.
- Executed action: removed root `README.md`, removed root `docs/`, removed `FCVW/snippets/`, updated governance references, and created framework structure audit.
- Pages created:
  - `wiki/sessions/S003-2026-05-29-root-and-snippets-deprecation.md`
- Pages updated:
  - `wiki/index.md`
  - `wiki/log.md`
- Pages obsolete: none.
- Result: framework-owned docs now stay inside `FCVW/`; root is reserved for application instantiation.
- Gaps: `FCVW/pr_description.txt` remains obsolete; GitHub Pages publication from root `docs/` would need replacement config/export.

## [2026-05-29 12:00] synthesis | Governance state reconciliation

- Source: repository and governance structural audit.
- Executed action: restored root README content, aligned current-version fields to `V0.7.5`, created missing official directory baselines, corrected skill catalogs/links/triggers, created current-version changelog and troubleshooting record.
- Pages created:
  - `wiki/sessions/S002-2026-05-29-governance-state-reconciliation.md`
- Pages updated:
  - `wiki/index.md`
  - `wiki/log.md`
- Pages obsolete: none.
- Result: governance state reconciled with current repository tag and structural validation passed.
- Gaps: historical formal changelogs for `V0.7.0` through `V0.7.4` remain optional backfill.

## [2026-05-29 11:40] synthesis | README flowchart alignment

- Source: README flowchart review and correction request.
- Executed action: updated README flowchart, created plan, changelog fragment, and session synthesis.
- Pages created:
  - `wiki/sessions/S001-2026-05-29-readme-flowchart-alignment.md`
- Pages updated:
  - `README.md`
  - `wiki/index.md`
  - `wiki/log.md`
- Pages obsolete: none.
- Result: flowchart aligned with session routing, AICC step included, session recorded.
- Gaps: version mismatch between STACK.md and MANIFEST.md (out of scope).

## [YYYY-MM-DD HH:MM] init | LLM Wiki Initialization

- Source: creation of the initial structure of the `wiki/` folder.
- Executed action: creation of structural pages and starter templates.
- Pages created:
  - `wiki/README.md`
  - `wiki/schema.md`
  - `wiki/index.md`
  - `wiki/log.md`
- Pages updated: none.
- Pages obsolete: none.
- Result: clean baseline ready for first project-specific records.
- Gaps: fill the wiki with validated knowledge as evidence is produced.
