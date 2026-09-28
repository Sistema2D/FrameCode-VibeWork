---
schema: "fcvw/skill@1"
name: "wiki-curator"
description: "Promote sourced reusable knowledge, merge duplicates, compact sessions and rotate memory. Use when adding, merging, reviewing or archiving wiki notes. Do not use for framework policy changes."
version: "2.0.1"
session_types:
  - "wiki_maintenance"
  - "handoff"
  - "maintenance"
---


# SKILL: Wiki Curator

Maintain the LLM Wiki as a continuously improving knowledge base while preserving FCVW's pillars: updates on demand, measurable freshness, and low token cost.

## Purpose

Promote sourced reusable knowledge into the smallest canonical wiki surface without duplicating records or loading the full archive by default.

## Activation Triggers

Load this skill when a task involves:

- creating, updating, merging, or reviewing wiki knowledge;
- promoting plans, changelogs, troubleshooting, audits, decisions, or sessions into reusable wiki pages;
- grouping related notes under the same topic;
- organizing tags, themes, or frontmatter colors;
- checking stale, duplicated, contradictory, or superseded wiki content;
- preparing minor or major releases that add reusable knowledge.

## Inputs

Changed source records, current canonical page candidates, `wiki/README.md`, taxonomy, metrics, active index/log, typed relationship findings, stale-source review candidates, and an explicit source-bounded search scope.

## Fixed Cost Mode

Always use the standard optimized mode. Do not ask the user to choose a cost mode.

Load only:

1. `AGENTS.md` checklist summary.
2. `CONTEXT_MAP.md` row for the active session type.
3. `wiki/index.md` and `wiki/README.md`.
4. the taxonomy in `wiki/README.md` when theme, tag, or freshness decisions are needed.
5. Source files that directly triggered the curation: changed plans, changelogs, troubleshooting records, audits, decisions, sessions, or specific wiki pages.

Do not read every wiki page unless `governance-validator` (wiki lint mode) reports an anomaly that requires it.

## Curation Loop

1. **Collect trigger sources**: identify new or changed source records and load only their summaries or relevant sections.
2. **Decide promotion**: promote only knowledge that meets `wiki/README.md` promotion criteria.
3. **Merge before create**: update an existing related page when the topic already exists; create a new page only for a distinct reusable concept.
4. **Cluster topics**: link related pages with Obsidian-style links and record canonical pages for superseded or overlapping notes.
5. **Refresh metadata**: set `last_reviewed`, `related_version`, `tags`, `theme`, `theme_color`, `maturity`, and `next_review` when applicable; do not require maturity for source, raw, or session records.
6. **Use typed relations deliberately**: prefer the narrowest meaningful relation, resolve every target, and rely on generated inverse edges instead of copying both directions.
7. **Review changed sources**: when a tracked `source_digest` changes, inspect only pages linked through `derived_from`; confirm, update, supersede, or invalidate them before refreshing the digest.
8. **Update metrics**: record freshness, promotion, duplication, source-impact, and taxonomy results in the active plan.
9. **Log curation**: summarize the curation in the active plan or session note; git history is the log.
10. **Validate**: run deterministic `governance-validator` (wiki lint mode) for minor/major releases or when three or more wiki pages changed; semantic review remains optional and source-bounded.

## Tag and Theme Rules

- Use canonical tags from the taxonomy in `wiki/README.md` before inventing new tags.
- Prefer one primary `theme` and one `theme_color` per page.
- Keep color names semantic and human-readable; do not store hex palettes unless a downstream renderer requires them.
- Use `superseded_by` or `canonical_page` instead of leaving duplicate notes active.

## Metrics

Record or verify these thresholds:

| Metric | Target |
|---|---|
| Freshness SLA | reviewed before each note's `next_review` date |
| Promotion precision | no trivial one-off notes promoted |
| Duplication | related notes linked or merged before release |
| Taxonomy coverage | curated pages have canonical tags and theme metadata |
| Source impact | changed tracked sources have explicit dependent-page decisions |
| Typed integrity | no broken, ambiguous, self, or redundant manually copied relation |
| Cost control | no broad wiki crawl without a lint finding or explicit request |

## Non-Responsibilities

- Do not rewrite official governance documents unless the active plan includes them.
- Do not delete raw sources.
- Do not mark knowledge as validated without source evidence.
- Do not refresh a changed source digest before dependent knowledge has been reviewed.
- Do not treat graph edges, stale reports, or semantic findings as canonical truth.
- Do not change release, versioning, or planning rules without `release-checklist` and an active plan.

## Required output

Pages created, updated, merged, superseded, or deferred; sources and confidence; index/log changes; metric impact; and residual review work.

## Exit Criteria

- Relevant pages are created or updated, not duplicated.
- `wiki/index.md` links the current canonical pages.
- Theme/tag metadata follows the taxonomy in `wiki/README.md`.
- Metrics or validation evidence are recorded.
- Residual gaps are explicit.


## Product knowledge handoff

For [product pages](../QA/PRODUCT_WIKI.md), preserve the distinction between sourced expected behavior, observed behavior and exact QA runs. [QA](../QA/SKILL.md) owns first-run live mapping and functional replay; curator owns deduplication, source review and lifecycle. Do not promote an observed defect into approved intent, refresh a changed behavior hash to reuse an old pass, or claim browser execution from document review. Review only affected product pages; preserve earlier runs and unresolved expectations.

## Mode: Session compaction (formerly `aicc-compact`)

Create a bounded session handoff with collision-resistant identity.

### Purpose

Capture only the state required to continue work without replaying the full conversation.

### Use when

- an active governed batch is handed to another session or agent;
- work stops with meaningful unresolved state;
- a completed batch produced reusable operational context.

Do not create a session file for a trivial read-only exchange or duplicate information already canonical elsewhere.

### Identity

Use `id: SES-YYYYMMDD-HHMMSS-<short-id>`. The short ID may be a commit prefix or random hexadecimal token. Never derive uniqueness only from “highest session number + 1”.

Suggested filename: `YYYYMMDD-HHMMSS-<short-id>-<slug>.md`.

### Inputs

- active plan and its current state;
- actual modified files;
- validation evidence;
- open risks and next authorized action.

### Non-responsibilities

- copying full files or chat transcripts into the handoff;
- inventing commit, test, publication, or completion evidence;
- treating the newest or highest sequence as relevant without checking scope;
- deleting older sessions as part of compaction.

### Procedure

1. Verify actual workspace and plan state.
2. Create the page from `governance/TEMPLATE_NOTE.md` (session block).
3. Link canonical files rather than copying their contents.
4. Record decisions, failures, validation, unresolved risks, and next step.
5. Add index/log entry only when the session is useful for future retrieval.
6. Check ID uniqueness.

### Required output

A concise, sourced handoff that distinguishes completed work, active work, blocked work, and optional next steps.

### Validation and exit

- unique ID;
- no secrets or private runtime data;
- links resolve;
- plan/status matches disk state;
- no unsupported claim of commit, tag, test, or publication.

## Mode: Memory rotation (formerly `memory-rotation`)

Archive and curate old sessions without destroying audit evidence.

### Purpose

Keep active session context bounded while preserving historical evidence and promoting sourced reusable knowledge.

### Use when

- active sessions exceed 10 files, 100 KB, or the project's context budget;
- duplicated or stale session summaries impair retrieval;
- the user requests archive, rotation, or memory consolidation.

### Do not use for

- deleting evidence to make validation appear clean;
- rewriting published history;
- replacing canonical project documents with session narrative.

### Inputs

- `wiki/README.md`;
- active and archived session indexes;
- retention/legal requirements.

### Procedure

1. Inventory active sessions and choose a bounded archive range.
2. Identify decisions, patterns, failures, and unresolved conflicts.
3. Promote only sourced, reusable knowledge; update an existing canonical page before creating a duplicate.
4. Create `wiki/archive/YYYY/README.md` with range, sources, destination paths, and unresolved items.
5. Move selected sessions to `wiki/archive/YYYY/`.
6. Keep the latest 3–10 relevant sessions active.
7. Update index, log, metrics, and backlinks.
8. Run wiki lint in incremental mode.

### Required output

Record files moved, knowledge promoted, duplicates merged, unresolved conflicts, retention decision, and validation.

### Validation and exit

- no source session is lost;
- archive links resolve;
- active session IDs remain unique;
- promoted claims cite sources;
- active memory is within the configured budget.
