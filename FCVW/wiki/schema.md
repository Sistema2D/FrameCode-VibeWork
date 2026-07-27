---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace_with_migration"
---

# Wiki schema

The wiki stores reusable, sourced knowledge. It does not replace code, project profiles, ADRs, plans, changelogs, or failure records.

## Page schema

New non-index pages use:

```yaml
---
schema: "fcvw/wiki@1"
id: "<collision-resistant-id>"
artifact_role: "record"
owner: "<accountable-owner>"
upgrade_strategy: "preserve"
retrieval_scope: "search_only"
title: "<title>"
type: "concept | decision | pattern | failure | regression | refactoring | audit | agent | release | session | component | prompt | question | synthesis | source | raw"
status: "draft | in_validation | validated | obsolete | superseded | contradictory"
confidence: "low | medium | high"
created_at: "YYYY-MM-DD"
last_reviewed: "YYYY-MM-DD"
sources:
  - "<path-or-reference>"
tags:
  - "<canonical-tag>"
---
```

Optional: `canonical_page`, `supersedes`, `superseded_by`, `related`, and `related_version`.

Every instantiated page contains at least one portable Markdown link to an authoritative source or related record. Frontmatter `sources` supports validation and retrieval, but does not by itself create an Obsidian backlink.

## IDs

- Session: `SES-YYYYMMDD-HHMMSS-<short-id>`.
- Regression: `REG-YYYYMMDD-<short-id>` using the specialized `fcvw/regression@1` schema.
- Other knowledge: stable slug or `TYPE-YYYYMMDD-<short-id>`.
- Filenames may be human-readable; uniqueness comes from `id`.

## Promotion

Promote only when knowledge is reusable, sourced, and not already canonical. Prefer updating an existing page. Link the plan, failure, decision, or session that supports the claim.

## Status and confidence

- `validated` requires medium/high confidence and evidence.
- conflicting evidence uses `contradictory`; do not silently select a winner.
- old behavior claims are reviewed or marked obsolete/superseded.
- sessions remain historical even when their conclusions become obsolete.

## Indexing and archives

- `index.md` links active canonical knowledge, not every file.
- `log.md` records curation/rotation events, not all development activity.
- old sessions move to `archive/YYYY/` under `MEMORY.md`.
- archives are searchable but not default context.

## Validation

Use `wiki-lint` in incremental mode by default. Legacy pages are preserved through exact baselines; new or changed pages must comply.

Confirmed reusable regressions live under `regressions/` and follow `templates/TEMPLATE_REGRESSION.md`. Do not create a regression record for an unverified suspicion or duplicate one when an existing canonical record can be updated.
