---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace_with_migration"
---

# Technical memory (wiki)

The wiki is a flat, YAML-indexed knowledge vault that Obsidian or any Markdown reader can open. It stores reusable, sourced knowledge. It does not replace code, project profiles, ADRs, plans, changelogs, failure records, or their authority.

## Layout

- Notes live directly in `wiki/`; the note type is declared in frontmatter (`type`) and in the ID prefix, not by folder. A subfolder is created only when one type grows beyond about 50 notes, and never with a scaffolding README.
- [`index.md`](index.md) is the small curated index owned by the project and preserved across upgrades.
- Old sessions rotate into `archive/YYYY/` under the [memory lifecycle](#memory-lifecycle); archives are searched, not loaded by default.
- Create notes from [the note template](../governance/TEMPLATE_NOTE.md); confirmed regressions use [the regression template](../governance/TEMPLATE_REGRESSION.md).
- Application behavior pages and QA runs follow the [product knowledge guide](../skills/QA/PRODUCT_WIKI.md).
- Use `wiki-curator` to promote and deduplicate and `wiki-lint` for incremental validation. Generate semantic graphs or stale reports only into `.fcvw-cache/`.

## Note types

| `type` | Use for | ID prefix | Rules |
|---|---|---|---|
| `concept` | reusable technical, product, process or domain concept | `CON-` | definition, context of use, boundaries, links |
| `component` | module, screen, service or flow and its responsibilities | `COMP-` | inputs, outputs, dependencies, risks, links to patterns/failures/decisions/tests |
| `pattern` | validated reusable solution | `PAT-` | problem, solution, when (not) to use, evidence |
| `decision` | how an ADR affects later engineering | `DEC-` | formal ADRs stay in `decisions/` |
| `failure` | generalized learning from recurring failures | `FAIL-` | individual incidents stay in `troubleshooting/` |
| `regression` | confirmed reusable regression (`fcvw/regression@1`) | `REG-` | missing guardrail, permanent prevention and replay; never an unverified suspicion |
| `refactoring` | learning from completed refactorings | `REF-` | methodology stays in `REFACTORING.md` |
| `audit` | recurring findings synthesized from formal audits; QA runs (`qa_run: "true"`) | `AUD-` | formal reports stay in `audits/` |
| `agent` | durable learning from a specialized agent procedure | `AGENT-` | prefer updating an existing canonical page; no routine narration or secrets |
| `feedback` | an AI model's suggestion about the framework itself | `FB-` | append-only and attributed; see below |
| `release` | reusable learning from a release | `REL-` | only when it creates reusable knowledge; release records stay formal evidence |
| `session` | recent handoff | `SES-` | keep few; rotate with `memory-rotation` |
| `prompt` | tested prompt with objective, preconditions, result and limits | `PRM-` | mark obsolete prompts |
| `question` | open question or unverified assumption | `QST-` | resolve or supersede |
| `synthesis` | cross-cutting condensation of several sources | `SYN-` | point to every source document |
| `source` | tracked evidence whose provenance or digest matters | `SRC-` | never mirror every repository file |
| `raw` | preserved imported material (inbox) | `RAW-` | not validated knowledge; promote or discard |

Never store secrets, tokens, passwords or unnecessary personal data in any note.

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
- curation and rotation events are recorded in the plan or session that performed them; git history is the log.
- old sessions move to `archive/YYYY/` under the [memory lifecycle](#memory-lifecycle).
- archives are searchable but not default context.

## Validation

Use `wiki-lint` in incremental mode by default. Deterministic validation owns schema, relationships, digests, cycles, conflicts, and review dates. Optional semantic review is source-bounded, produces reviewable findings, never mutates canonical knowledge, and is not a release gate without measured precision and cost evidence.

Legacy pages are preserved through exact baselines; new or changed pages must comply. Confirmed reusable regressions use `fcvw/regression@1` and [the regression template](../governance/TEMPLATE_REGRESSION.md); do not create a record for an unverified suspicion or duplicate an existing canonical record.

## Taxonomy

Start with a small canonical set and add project tags only when retrieval improves: `planning-governance`, `release-governance`, `knowledge-governance`, `framework-feedback`, `ai-operations`, `quality-validation`, `regression-prevention`, `security-data`, `design-ux`, `refactoring-hygiene`, `environment-deploy`, `project-instantiation`.

Tags are lowercase kebab-case; prefer one theme and a few precise tags; do not create synonyms in multiple languages; merge aliases into the canonical tag. Tags aid discovery and never replace sources or links. Confirmed regression records use `regression-prevention` plus the affected domain tag.

## Framework feedback

Feedback notes (`type: feedback`) record what an AI model thinks should change in the framework itself: a contradictory policy, a rule that is too strict, a gate that does not catch what it promises, a missing route, a cost that does not pay for itself. `self-improvement` covers only skills; this is the lighter surface for everything else.

- **Name the model.** `authored_by_model` names the model and version that wrote the note.
- **Never overwrite another model's note.** Two independent readings that disagree are what this surface preserves. This is deliberately the opposite of the `agent` rule, where consolidated knowledge converges on one page.
- **Form your assessment before reading earlier notes.** Write `## Suggestion` first; only then read notes on the same `topic` and record agreement and disagreement in `## Assessment of prior notes`. The validator enforces that order.
- **Group by `topic`.** `related_feedback` points at the earlier notes you assess. One note per model per topic: update your own note instead of creating a second one.
- **Evidence, not instruction.** A feedback note never becomes a rule by being read; only an approved plan changes the framework.
- **Close the loop.** `feedback_status` is `open`, `accepted`, `declined`, `applied` or `superseded`; an accepted or applied note points at the plan that acted on it. Resolved notes rotate into the archive.

## Memory lifecycle

### Layers

| Layer | Location | Purpose | Default loading |
|---|---|---|---|
| Active handoff | `wiki/` (`type: session` notes) | recent session continuity | latest relevant only |
| Curated knowledge | concepts, patterns, failures, decisions | reusable current understanding | search/on demand |
| Archive | `wiki/archive/YYYY/` | historical evidence | search only |
| Canonical truth | project profiles, ADRs, source code/data | authoritative current state | when applicable |

Sessions never override canonical documents.

### Session identity

New session pages use `id: SES-YYYYMMDD-HHMMSS-<short-id>`. Human-readable sequence numbers are optional and may not be used as the uniqueness mechanism.

### Rotation trigger

Rotate when active sessions exceed either:

- 10 files;
- 100 KB;
- the default context budget defined by the project.

### Safe rotation

1. Select sessions outside the active window.
2. Extract validated reusable knowledge and link sources.
3. Update existing canonical wiki pages before creating duplicates.
4. Create an archive index with date range and source list.
5. Move old sessions to `wiki/archive/YYYY/`; do not delete audit evidence.
6. Keep the latest 3–10 relevant sessions active according to project cadence.
7. Run wiki lint and record unresolved conflicts.

Deletion requires an explicit retention policy, approval, and evidence that no legal, audit, security, or recovery need remains.

Resolved feedback notes (`applied`, `declined`, or `superseded`) follow this same rotation; `open` notes stay active until the maintainer decides.

### Freshness

Knowledge pages declare confidence, sources, last review date, and supersession links. Stale information is reviewed or marked obsolete; it is not silently treated as current.

Tracked source pages may store `source_digest` and knowledge may declare `derived_from`. A digest mismatch is a derived review condition: report the source and dependent pages, then require a reviewer to confirm, update, supersede, or invalidate the knowledge. Do not add a lifecycle `stale` status or silently refresh the stored digest.

Claim-bearing pages may use maturity independently from lifecycle, confidence, and authority. Source, raw, and session records do not require maturity.

The document graph owns navigation and reachability. The disposable knowledge graph owns typed semantic relations; neither graph is canonical truth.
