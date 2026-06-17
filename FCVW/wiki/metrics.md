---
title: "Wiki Metrics"
type: "synthesis"
status: "validated"
confidence: "high"
last_reviewed: "2026-06-17"
related_version: "V0.11.0"
sources:
  - "AI.md"
  - "wiki/schema.md"
  - "skills/wiki-curator/SKILL.md"
tags:
  - "wiki"
  - "validation"
  - "continuous-learning"
theme: "knowledge-governance"
theme_color: "teal"
next_review: "2026-09-17"
review_cadence: "quarterly"
---

# Wiki Metrics

Metrics used to keep the LLM Wiki current while controlling token cost.

## Freshness Targets

| Page Type | Review Cadence | Trigger |
|---|---|---|
| `decision` | 180 days | architecture, security, data, or API change |
| `pattern` | 180 days | new implementation validates or contradicts the pattern |
| `failure` | 90 days | recurring issue, bugfix, or troubleshooting closure |
| `refactoring` | 120 days | cleanup, module split, stale-file scan |
| `release` | each release | release publication or rollback |
| `synthesis` | 90 days | related pages changed or wiki-lint flags drift |
| `session` | no routine review | promoted only when reusable learning exists |

## Quality Metrics

| Metric | Target | Evidence |
|---|---|---|
| Promotion precision | no one-off notes promoted | active plan or wiki log |
| Source coverage | every interpretative page cites at least one source | frontmatter `sources` |
| Link coverage | every curated page has at least one related link or index entry | `wiki/index.md` or wikilink |
| Taxonomy coverage | curated pages use canonical tags and theme metadata | frontmatter |
| Duplication control | overlapping notes are merged or marked with `canonical_page` / `superseded_by` | page frontmatter |
| Release synthesis coverage | every published changelog has a release synthesis unless explicitly waived | `wiki/releases/` |
| Cost control | no full wiki crawl without lint finding or explicit request | plan validation notes |

## Standard Optimized Cost Mode

The wiki curator always uses one fixed optimized mode:

- load routing documents and indexes first;
- load source records only when they triggered curation;
- prefer updating an existing page over creating a duplicate;
- defer broad reads to `wiki-lint` findings or explicit user request;
- record remaining gaps instead of spending tokens to inspect unrelated domains.

No customizable cost mode is exposed by the framework.
