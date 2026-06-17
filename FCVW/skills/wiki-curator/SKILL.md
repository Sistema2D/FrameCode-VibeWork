---
name: "wiki-curator"
version: "1.0.0"
trigger_keywords: ["wiki curator", "curate wiki", "continuous learning", "knowledge promotion", "wiki learning loop", "organizar wiki", "curadoria wiki", "agrupar notas", "frontmatter colors", "taxonomia", "metricas da wiki"]
session_types: ["wiki_maintenance", "ai_governance", "document_audit", "release"]
---

# SKILL: Wiki Curator

Maintain the LLM Wiki as a continuously improving knowledge base while preserving FCVW's pillars: updates on demand, measurable freshness, and low token cost.

## Activation Triggers

Load this skill when a task involves:

- creating, updating, merging, or reviewing wiki knowledge;
- promoting plans, changelogs, troubleshooting, audits, decisions, or sessions into reusable wiki pages;
- grouping related notes under the same topic;
- organizing tags, themes, or frontmatter colors;
- checking stale, duplicated, contradictory, or superseded wiki content;
- preparing minor or major releases that add reusable knowledge.

## Fixed Cost Mode

Always use the standard optimized mode. Do not ask the user to choose a cost mode.

Load only:

1. `AGENTS.md` checklist summary.
2. `CONTEXT_MAP.md` row for the active session type.
3. `wiki/index.md`, `wiki/log.md`, `wiki/schema.md`.
4. `wiki/taxonomy.md` and `wiki/metrics.md` when theme, color, tag, or freshness decisions are needed.
5. Source files that directly triggered the curation: changed plans, changelogs, troubleshooting records, audits, decisions, sessions, or specific wiki pages.

Do not read every wiki page unless `wiki-lint` reports an anomaly that requires it.

## Curation Loop

1. **Collect trigger sources**: identify new or changed source records and load only their summaries or relevant sections.
2. **Decide promotion**: promote only knowledge that meets `wiki/schema.md` promotion criteria.
3. **Merge before create**: update an existing related page when the topic already exists; create a new page only for a distinct reusable concept.
4. **Cluster topics**: link related pages with Obsidian-style links and record canonical pages for superseded or overlapping notes.
5. **Refresh metadata**: set `last_reviewed`, `related_version`, `tags`, `theme`, `theme_color`, and `next_review` when applicable.
6. **Update metrics**: record freshness, promotion, duplication, and taxonomy results in `wiki/metrics.md` or the active plan.
7. **Log curation**: append a compact event to `wiki/log.md`.
8. **Validate**: run `wiki-lint` for minor/major releases or when three or more wiki pages changed.

## Tag and Theme Rules

- Use canonical tags from `wiki/taxonomy.md` before inventing new tags.
- Prefer one primary `theme` and one `theme_color` per page.
- Keep color names semantic and human-readable; do not store hex palettes unless a downstream renderer requires them.
- Use `superseded_by` or `canonical_page` instead of leaving duplicate notes active.

## Metrics

Record or verify these thresholds:

| Metric | Target |
|---|---|
| Freshness SLA | reviewed within the cadence in `wiki/metrics.md` |
| Promotion precision | no trivial one-off notes promoted |
| Duplication | related notes linked or merged before release |
| Taxonomy coverage | curated pages have canonical tags and theme metadata |
| Cost control | no broad wiki crawl without a lint finding or explicit request |

## Non-Responsibilities

- Do not rewrite official governance documents unless the active plan includes them.
- Do not delete raw sources.
- Do not mark knowledge as validated without source evidence.
- Do not change release, versioning, or planning rules without `release-checklist` and an active plan.

## Exit Criteria

- Relevant pages are created or updated, not duplicated.
- `wiki/index.md` and `wiki/log.md` are synchronized.
- Theme/tag metadata follows `wiki/taxonomy.md`.
- Metrics or validation evidence are recorded.
- Residual gaps are explicit.
