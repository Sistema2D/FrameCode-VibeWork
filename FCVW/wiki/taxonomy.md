---
title: "Wiki Taxonomy"
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
  - "taxonomy"
  - "continuous-learning"
theme: "knowledge-governance"
theme_color: "teal"
next_review: "2026-09-17"
review_cadence: "quarterly"
---

# Wiki Taxonomy

Canonical taxonomy for tags, themes, and frontmatter colors in the LLM Wiki.

## Primary Themes

| Theme | Color | Use for |
|---|---|---|
| `planning-governance` | `blue` | Plans, priority/risk gates, scope control, PR workflow |
| `release-governance` | `indigo` | Versions, changelogs, release syntheses, publication records |
| `knowledge-governance` | `teal` | Wiki schema, taxonomy, metrics, curation, Obsidian graph |
| `ai-operations` | `violet` | AICC, ASE, agents, prompts, model usage, context loading |
| `quality-validation` | `green` | Tests, audits, linting, validation evidence |
| `security-data` | `red` | Security, secrets, privacy, persistence, migrations |
| `design-ux` | `amber` | UI, accessibility, design system, visual decisions |
| `refactoring-hygiene` | `orange` | Refactoring, anti-monolith gates, duplication, stale files |
| `environment-deploy` | `slate` | Environment, deployment, promotion, rollback |
| `project-instantiation` | `cyan` | New project bootstrap, retroactive instantiation, templates |

## Canonical Tags

| Tag | Theme | Use for |
|---|---|---|
| `gold-pattern` | `quality-validation` | Validated reusable solutions |
| `failure-log` | `quality-validation` | Recurring failures and fixes |
| `arch-decision` | `planning-governance` | Architecture decisions and ADR-related notes |
| `tech-debt` | `refactoring-hygiene` | Debt, stale files, cleanup candidates |
| `refactor-plan` | `refactoring-hygiene` | Refactoring proposals and outcomes |
| `user-feedback` | `planning-governance` | Direct user requests that shape framework behavior |
| `continuous-learning` | `knowledge-governance` | Wiki learning loop, promotion, curation, synthesis |
| `wiki` | `knowledge-governance` | Wiki schema, index, log, taxonomy, and metrics |
| `release` | `release-governance` | Release notes and release syntheses |
| `skills` | `ai-operations` | ASE skills and agent procedures |
| `aicc` | `ai-operations` | Session compression and handoff memory |
| `validation` | `quality-validation` | Tests, audit evidence, lint results |

## Frontmatter Usage

Recommended fields for curated pages:

```yaml
theme: "knowledge-governance"
theme_color: "teal"
next_review: "YYYY-MM-DD"
review_cadence: "quarterly"
canonical_page: "wiki/<folder>/<page>.md"
supersedes:
  - "wiki/<folder>/<older-page>.md"
superseded_by: "wiki/<folder>/<newer-page>.md"
related_pages:
  - "wiki/<folder>/<related-page>.md"
```

Use these fields when they improve curation. Do not add metadata noise to short-lived raw or inbox records.
