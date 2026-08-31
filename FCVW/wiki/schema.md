---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace_with_migration"
---

# Wiki schema

The wiki stores reusable, sourced knowledge. It does not replace code, project profiles, ADRs, plans, changelogs, failure records, or their authority.

## Knowledge and evidence

- Knowledge pages state reusable understanding, decisions, patterns, questions, or syntheses.
- `type: source` pages describe selected evidence whose provenance or change impact is worth tracking.
- `type: raw` pages preserve imported material when preservation is necessary; they are not validated knowledge.
- Project state remains in plans, profiles, ADRs, code, data, releases, and troubleshooting records.
- Context indexes and knowledge graphs are derived caches, never canonical pages.

Do not create one source page per repository file. Track a source only when explicit provenance, digest comparison, or impact analysis improves reviewability.

## Page schema

New non-index pages use:

```yaml
---
schema: "fcvw/wiki@1"
id: "<collision-resistant-id>"
artifact_role: "record"
owner: "<accountable-owner>"
upgrade_strategy: "preserve"
record_scope: "application | framework"
retrieval_scope: "search_only"
title: "<title>"
type: "concept | feedback | decision | pattern | failure | regression | refactoring | audit | agent | release | session | component | prompt | question | synthesis | source | raw"
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

Claim-bearing pages may add:

```yaml
maturity: "hypothesis | provisional | established | disputed"
next_review: "YYYY-MM-DD"
domain:
  - "<bounded-domain>"
```

`maturity` is not required for `source`, `raw`, or `session` pages. Deprecation remains a lifecycle concern expressed by `status: obsolete | superseded`; it is not a maturity value.

## Typed relationships

Optional flat relationship fields are:

```yaml
related:
  - "<wiki-id-or-governed-markdown-path>"
depends_on:
  - "<wiki-id-or-governed-markdown-path>"
supports:
  - "<wiki-id-or-governed-markdown-path>"
contradicts:
  - "<wiki-id-or-governed-markdown-path>"
implements:
  - "<wiki-id-or-governed-markdown-path>"
derived_from:
  - "<wiki-id-or-governed-markdown-path>"
invalidates:
  - "<wiki-id-or-governed-markdown-path>"
supersedes:
  - "<wiki-id-or-governed-markdown-path>"
superseded_by:
  - "<wiki-id-or-governed-markdown-path>"
canonical_page: "<wiki-id-or-governed-markdown-path>"
```

| Relation | Meaning |
|---|---|
| `related` | Symmetric contextual association with no stronger claim. |
| `depends_on` | The source claim requires the target knowledge to remain valid. |
| `supports` | The source contributes evidence or reasoning in favor of the target. |
| `contradicts` | The source and target contain materially incompatible claims requiring review. |
| `implements` | The source operationalizes the target decision, pattern, or contract. |
| `derived_from` | The source knowledge was derived from the target evidence or artifact. |
| `invalidates` | The source makes the target claim no longer reliable. |
| `supersedes` | The source replaces the target while preserving history. |
| `superseded_by` | Compatibility field for an explicitly recorded replacement. Prefer recording `supersedes` on the newer page. |
| `canonical_page` | The target is the preferred knowledge page for the topic. |

Targets resolve to a unique wiki ID or an existing governed Markdown path inside the repository. External URLs belong in `sources` or `source_url`, not typed relationships. Typed fields other than `canonical_page` use first-level lists. Do not duplicate inverse edges merely for navigation: the derived knowledge graph emits `required_by`, `supported_by`, `implemented_by`, `source_for`, `invalidated_by`, canonical, symmetric, and supersession inverses.

Frontmatter relations remain machine metadata. Every instantiated page still contains at least one portable Markdown link to an authoritative source or related record so Obsidian backlinks and the document graph remain navigable.

## Source provenance

A selectively tracked `type: source` page may add:

```yaml
source_type: "repository_file | web | document | dataset | issue | api | conversation | other"
source_path: "<repository-relative-or-page-relative-path>"
source_url: "https://example.test/source"
source_digest: "sha256:<64-lowercase-hex>"
ingested_at: "YYYY-MM-DD"
last_checked: "YYYY-MM-DD"
```

Use `source_digest`, not `content_hash`: the context index already uses `content_hash` as a legacy alias for the indexed chunk hash and exposes the unambiguous `chunk_hash`. A digest mismatch is a derived stale finding. It never rewrites the stored digest, page status, or dependent knowledge.

Knowledge that must be reconsidered when a tracked source changes declares `derived_from` to the source page. The knowledge-graph validator then reports review candidates. Review confirms, updates, supersedes, or invalidates the knowledge and only then refreshes the stored digest and review dates.

## IDs

- Session: `SES-YYYYMMDD-HHMMSS-<short-id>`.
- Regression: `REG-YYYYMMDD-<short-id>` using the specialized `fcvw/regression@1` schema.
- Other knowledge: stable slug or `TYPE-YYYYMMDD-<short-id>`.
- Filenames may be human-readable; uniqueness comes from `id`.

## Promotion

Promote only when knowledge is reusable, sourced, and not already canonical. Prefer updating an existing page. Link the plan, failure, decision, source, or session that supports the claim.

## Status, confidence, maturity, and authority

- `status` is page lifecycle.
- `confidence` is strength of current evidence.
- `maturity` is consolidation of a claim.
- `authority` is determined by artifact ownership and cannot be elevated by a wiki record.
- `validated` requires medium/high confidence and evidence.
- conflicting evidence uses `contradictory` and, when useful, a typed `contradicts` edge; do not silently select a winner.
- old behavior claims are reviewed or marked obsolete/superseded.
- sessions remain historical even when their conclusions become obsolete.

## Derived graphs, indexing, and archives

- `tools/document_graph_fcvw.py` remains the navigation and reachability graph.
- `tools/knowledge_graph_fcvw.py` emits a separate semantic graph reconstructed from frontmatter.
- Graphs, stale-review reports, and context indexes use `.fcvw-cache/` or another user-selected disposable path.
- `index.md` is a small preserved project profile linking active canonical knowledge rather than every derived category.
- Do not commit a hierarchy of generated wiki indexes until measured downstream scale proves it useful.
- `log.md` records curation/rotation events, not all development activity.
- old sessions move to `archive/YYYY/` under `MEMORY.md`.
- archives are searchable but not default context.

## Validation

Use `wiki-lint` in incremental mode by default. Deterministic validation owns schema, relationships, digests, cycles, conflicts, and review dates. Optional semantic review is source-bounded, produces reviewable findings, never mutates canonical knowledge, and is not a release gate without measured precision and cost evidence.

Legacy pages are preserved through exact baselines; new or changed pages must comply. Confirmed reusable regressions live under `regressions/` and follow `templates/TEMPLATE_REGRESSION.md`; do not create a record for an unverified suspicion or duplicate an existing canonical record.
