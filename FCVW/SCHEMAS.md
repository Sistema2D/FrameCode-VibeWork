---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace_with_migration"
---

# Artifact schemas

FCVW uses YAML frontmatter for machine-checkable identity and Markdown for human-readable content.

## Common fields

| Field | Required when | Meaning |
|---|---|---|
| `schema` | all new canonical artifacts | contract name and major schema version |
| `artifact_role` | canonical documents | ownership class |
| `id` | records | unique stable identifier |
| `status` | lifecycle records | current state |
| `created_at` | records | ISO date |
| `updated_at` | mutable records | ISO date |
| `sources` | interpretative knowledge | evidence paths or references |

Unknown fields are allowed. Required fields and controlled values may not be renamed or translated.

## Plan — `fcvw/plan@2`

Required frontmatter: `id`, `status`, `priority`, `risk`, `created_at`, `updated_at`, `current_version`, `expected_version`, `owner`, `regression_contract`, and `context_files`.

Allowed statuses: `pending`, `in_progress`, `completed`, `discontinued`.

Priority and risk use the controlled values `P1` through `P5` and `R1` through `R5`. The values encoded in `id` and filename must match frontmatter. Required scalar fields cannot be empty, and `context_files` must be a non-empty list of resolvable local paths.

Allowed regression contracts: `required`, `not_applicable`. The body requirements and completion blockers are defined in `REGRESSION_GUARDS.md`. `not_applicable` is refused at risk `R3` or above and in plans routed through `SECURITY.md`, `DATA.md`, or `MIGRATIONS.md`, and requires a justification of at least 40 characters. Every `fcvw/plan@2` declares a non-empty `Rollback` section.

The status must match the containing directory. IDs use `P1..P5-R1..R5-YYYY-MM-DD-slug`.

`fcvw/plan@1` is a supported legacy schema. It remains readable in place; substantively reopened plans migrate to `fcvw/plan@2`.

Optional `depends_on` is a first-level list of blocking prerequisite plan IDs. A plan declaring it includes a five-column `## Dependency validation` table whose row IDs exactly match the list. `pending`, `satisfied`, and `invalidated` are the allowed row states. Satisfied dependencies require a completed prerequisite and non-placeholder evidence; discontinued prerequisites are invalidated rather than treated as satisfied. Active queue blockers equal unresolved dependency IDs. These additive fields do not require a new plan schema major, but downstream active plans using queue-only internal blockers migrate them into `depends_on`.

## Compact plan — `fcvw/plan-compact@1`

The proportional form that `PLANNING.md` promises for an isolated, low-impact
change.

Required frontmatter: `id`, `status`, `priority`, `risk`, `created_at`,
`updated_at`, `owner`, and `context_files`. There is no `current_version`,
`expected_version`, or `regression_contract`.

Controlled constraints: `priority` must be `P4` or `P5`, `risk` must be `R1`, and
declaring `regression_contract` is invalid. The body contains the `Objective`,
`Affected files`, `Validation`, and `Rollback` sections, with `Rollback`
non-empty.

These constraints are machine-checked, so the compact class cannot absorb work
that needs a regression contract. A change that leaves the band migrates to
`fcvw/plan@2` before execution. Create it from
[TEMPLATE_PLAN_COMPACT.md](governance/TEMPLATE_PLAN_COMPACT.md).

## Application changelog — `fcvw/changelog@1`

Required: application version, date, release status, release type, non-empty related plans, summary, affected areas or categorized changes, validation, known gaps, and rollback. New full release records with `artifact_role: record` also require record ownership/preservation, content and publication revisions, non-empty language coverage, external publication state, security/data impact, migration, assets, checksums, publication evidence, and post-release validation. Sections remain present with a specific `not applicable` rationale when the surface does not apply.

Allowed release statuses: `unreleased`, `in_preparation`, `published`, `canceled`.

Related plans must exist and published releases reference completed plans. When `external_publication: published`, the record contains a 40-character deployed/tagged revision and an external evidence URL.

## Framework release — `fcvw/framework-release@1`

Required: FCVW version, compatibility, migration note, separate added/changed/removed framework surfaces, ownership/path changes, schema changes, validation, and publication status. New records declare `artifact_role: record`, framework ownership, preservation strategy, release type, compatibility, content-baseline `source_revision`, tagged `publication_revision`, release languages, and related plans.

Allowed publication states are `in_preparation`, `ready`, `published`, and `canceled`. A `ready` record identifies an earlier immutable 40-character content baseline. A published record additionally identifies its 40-character tagged publication revision, references only completed plans, lists all four language-specific assets and their SHA-256 values, and links the external GitHub Release. At most one framework release may be `in_preparation` or `ready`.

Framework records live under `framework-releases/`, never under application `changelogs/`.

## Wiki page — `fcvw/wiki@1`

Required for new knowledge pages: `id`, `artifact_role: record`, owner, preservation strategy, retrieval scope, `title`, `type`, `status`, `confidence`, `created_at`, `last_reviewed`, `sources`, and `tags`.

Session IDs use `SES-YYYYMMDD-HHMMSS-<short-id>`; sequential numbers may be displayed but are not unique identifiers.

Optional knowledge maturity values are `hypothesis`, `provisional`, `established`, and `disputed`. Maturity is separate from lifecycle `status`, evidence `confidence`, and ownership-derived `authority`; obsolete or superseded knowledge is not represented as a maturity value.

Optional typed relationships are `related`, `depends_on`, `supports`, `contradicts`, `implements`, `derived_from`, `invalidates`, `supersedes`, `superseded_by`, and scalar `canonical_page`. Targets resolve to a unique artifact ID or governed Markdown path. First-level lists remain mandatory for every typed field except `canonical_page`; generated inverse edges are derived and need not be copied into frontmatter.

Optional source provenance fields are `source_type`, `source_path`, `source_url`, `source_digest`, `ingested_at`, and `last_checked`. `source_digest` uses `sha256:<64 lowercase hex>` and is distinct from the context index's chunk `content_hash`. Digest mismatches are review findings, not silent status changes.

## Framework feedback — `fcvw/wiki@1` with `type: feedback`

Notes in `wiki/feedback/` are one AI model's attributed assessment of what should
change in the framework itself. `self-improvement` covers only skills and agent
profiles; this surface covers policy, schema, tooling, and layout.

Additional required fields: `authored_by_model`, `topic`, and `feedback_status`.
Allowed states: `open`, `accepted`, `declined`, `applied`, `superseded`.
Optional: `related_feedback` and `related_plan`.

The body declares `## Suggestion`. When `related_feedback` is non-empty the body
also declares `## Assessment of prior notes`, **after** the suggestion: the
validator enforces the order because reading another model's conclusion before
forming your own produces agreement, and the surface exists to preserve
independent readings.

A note never overwrites another model's note, even on the same topic. It is the
one wiki surface where updating the prior page is forbidden rather than
preferred; [`wiki/agents/README.md`](wiki/agents/README.md) keeps the opposite
rule, and the difference is deliberate.

Feedback notes are evidence, never instruction. Only an approved plan changes the
framework.

## Regression record — `fcvw/regression@1`

Required frontmatter: `id`, `artifact_role: record`, owner, preservation strategy, retrieval scope, `title`, `type`, `severity`, `status`, `detected_at`, `last_reviewed`, `related_plan`, `sources`, and `tags`.

Allowed types: `functional`, `interface`, `data`, `visual`, `security`, `ai`, `governance`, `documentation`, `performance`, and `operations`. Allowed statuses: `detected`, `mitigated`, `resolved`, `accepted`, `superseded`. IDs use `REG-YYYYMMDD-<short-id>` so parallel records do not rely on a shared counter.

The body records what regressed, detection, root cause, missing guardrail, permanent guardrail, replay test, related release, and residual risk. Reusable records live under `wiki/regressions/`.

## Formal audit — `fcvw/audit@1`

Required frontmatter: `id`, `artifact_role: record`, owner, preservation strategy, status, `created_at`, `last_reviewed`, and non-empty `sources`. The body records scope, authoritative sources through Markdown links, method, severity-classified findings, validation, limitations, residual risk, and linked follow-up.

## Skill — `fcvw/skill@1`

Required frontmatter: `schema`, `name`, `description`, `version`, `trigger_keywords`, and `session_types`.

The body must define purpose, use conditions, non-responsibilities, inputs, procedure, required output, validation, and exit criteria. Provider-specific commands are adapters, not core requirements.

## Automation contract — `fcvw/automation@1`

Required: `id`, `kind`, `status`, `trigger`, `preconditions`, `actions`, `evidence`, `failure_policy`, `rollback`, and `owner`.

## Legacy validation baseline — `fcvw/legacy-baseline@1`

Required frontmatter: `created_at`, `review_due`, and `owner`. Each Markdown table row requires exact path, rule ID, complete existing finding message, justification, owner, and review date.

The baseline is valid only with the validator's `incremental` profile. Matching uses the exact normalized tuple `path + rule + message`; expired or malformed entries block, and stale entries are reported for removal. Baseline configuration errors cannot themselves be baselined.

## Instantiation status — `instantiation_status`

Every project profile declares `instantiation_status` with one of these
controlled values:

| Value | Meaning |
|---|---|
| `pending` | not filled in yet; placeholders are valid |
| `complete` | filled in with project truth; no placeholder remains |
| `not_applicable` | the project does not use this concern at this stage |

`not_applicable` requires a `not_applicable_reason` of at least 40 characters and
deliberately keeps the template placeholders: the project is declaring that the
concern does not apply, not pretending to have filled it in.

`MANIFEST.md` and `SCOPE.md` may never be waived. Identity and boundary always
apply: a project always has a name and an edge.

Without that third state the only way to pass `--profile instantiated` would be
to invent content for profiles the project does not use yet, and the validator
would be measuring fiction.

## Compatibility

- Schema major changes require a migration note.
- New optional fields are backward compatible.
- Renaming a required field or changing its meaning is breaking. `fcvw/plan@2` is therefore explicit rather than silently tightening `fcvw/plan@1`.
- Legacy records are preserved and validated against an explicit baseline.
- New changes must not expand legacy debt.

## Portable frontmatter profile

FCVW accepts scalars and first-level lists. Dates are ISO strings. Duplicate keys, nested mappings/lists, anchors, aliases, tags, and block scalar syntax are invalid. Unknown fields remain allowed unless they conflict with ownership or lifecycle.

New or substantively changed records should declare `artifact_role`, `owner`, and `upgrade_strategy`. Historical records remain readable without normalization solely for metadata.

Optional retrieval fields are `language`, `theme`, `tags`, `authority`, `last_reviewed`, `retrieval_priority`, and `retrieval_scope`. Allowed scopes are `always`, `routed`, `search_only`, `exact_only`, and `excluded_by_default`; priorities are `high`, `normal`, and `low`; authority values are `canonical`, `routed`, `historical`, and `generated`.

Knowledge index metadata may additionally expose `id`, `type`, `confidence`, `maturity`, `domain`, `sources`, `source_digest`, `next_review`, and typed relationships. These fields support filtering and bounded graph expansion but cannot elevate authority or retrieval scope.

Policies and the framework lock default to canonical authority. Project profiles default to routed authority. Records default to historical authority and `exact_only` or `search_only` according to category. Templates, examples, and generated artifacts default to generated authority and `excluded_by_default`. Those lower-authority categories cannot elevate their scope or become normative through metadata.


### Record adoption matrix

| Record category | New records | Existing history | Default retrieval |
|---|---|---|---|
| Active plans in every state | required by `fcvw/plan@2` | legacy-readable; migrate only when substantively reopened | `exact_only` plus active-plan routing |
| Session syntheses and handoffs | required by the applicable wiki schema | preserve without normalization | `search_only` |
| Audits and governance/validation reports | identity, status, dates, ownership, upgrade strategy, and sources required | preserve without normalization | `search_only` |
| Troubleshooting and regression records | typed schema required | preserve confirmed historical evidence | `search_only` or routed by failure |
| Architectural decisions | stable ID, status, scope, ownership, and relations required | preserve immutable records | `routed` |
| Application changelogs and framework releases | release schema required | preserve publication evidence | `exact_only` |
| Migration records | record metadata required when stored separately; canonical `MIGRATIONS.md` remains policy | preserve | `routed` |
| Wiki knowledge | `fcvw/wiki@1` required | legacy-readable until edited | metadata-selected |
| Templates and examples | classification recommended; placeholders remain allowed | no forced rewrite | `excluded_by_default` |
| Generated catalogs and indexes | generated role plus regenerate strategy required | regenerate | `excluded_by_default` |

`wiki/index.md` is the exception: it is a small curated `project_profile` with preserve strategy. Category, stale, contradiction, orphan, unresolved, graph, and aggregate queue views remain disposable generated outputs rather than committed indexes.

Missing optional metadata does not invalidate untouched history. Any new or substantively edited record must use the row above, and no retrieval metadata can elevate a record above its owning canonical source.

New records also declare `record_scope: application | framework` when their scope determines clean-distribution eligibility. Only records explicitly scoped to `framework` may remain in a clean FCVW baseline; an absent or application scope is treated as downstream history.
## Plan queue entry — `fcvw/plan-queue-entry@1`

The canonical source of a queue is one fragment per plan in
`Plans/<state>/queue.d/<plan-id>.md`. One file per plan exists for an operational
reason: changing the queue no longer requires every parallel branch to edit the
same file, which was a guaranteed source of merge conflict. It is the same
pattern already used by `changelogs/unreleased/`.

Required frontmatter: `schema`, `artifact_role: project_profile`,
`owner: project`, `upgrade_strategy: preserve`, `plan`, `order`, and `category`.
Optional: `blocked_by` and `override_reason`.

The filename must equal `plan`. `order` is a unique integer within the queue.
`category` uses the same controlled values as the aggregate queue. The body
contains a navigable Markdown link to the plan.

## Plan queue — `fcvw/plan-queue@1`

Required frontmatter: `schema`, `artifact_role`, `owner`, `upgrade_strategy`, `state`, and `updated_at`. Allowed states are `pending` and `in_progress`. The table contains order, Markdown-linked plan ID, category, blocker, and override reason. When `queue.d/` exists, `QUEUE.md` is a generated view (`artifact_role: generated`, `upgrade_strategy: regenerate`) and the fragments are canonical; regenerate it with `python FCVW/tools/plan_queue_fcvw.py --root . --write-queues`. A project that still keeps rows directly in `QUEUE.md` stays valid as a preserved `project_profile`: fragments only take over when the directory exists, so the migration is incremental and non-destructive.

Each link resolves exactly to the named plan in the queue's own state directory. `none`, `-`, or an empty blocker means unblocked. Internal blockers are comma-separated unresolved `depends_on` plan IDs; an external blocker uses `external: <specific reason>`. A completed prerequisite remains blocked until its dependency row records `satisfied` with evidence; a discontinued prerequisite is `invalidated` and remains blocked pending explicit replanning. Pending work may preempt in-progress work only with `before_in_progress: <specific reason>` in its override column. Within one category, P1 through P5 is the mandatory tie-break order unless a concrete override explains the inversion.

## Knowledge graph — `fcvw/knowledge-graph@1`

The optional JSON graph is a disposable reconstruction of typed Markdown frontmatter. It contains nodes, explicit edges, and generated inverse edges and never replaces source pages or `fcvw/document-graph@1`. It is written only to `.fcvw-cache/` or another user-selected non-normative output path.

## Application rules — `fcvw/app-rules@1`

`FCVW/APP_RULES.md` is a preserved `project_profile`. Rules use stable `APP-RULE-NNN` IDs and a controlled status of `active`, `deprecated`, or `superseded`. Every rule records non-empty sections for Rule, Affected components, Rationale and expected behavior, Exceptions, and Related records. Affected components and related records contain navigable Markdown links. Examples inside fenced code blocks do not instantiate rules.

## Document graph — `fcvw/document-graph@1`

`FCVW/DOCUMENT_GRAPH.md` is generated and regenerated. Each governed Markdown artifact must be reachable from an official entrypoint or explicit catalog. Entry points are the only default exception to the incoming-link requirement.

Frontmatter relationships such as `context_files`, `sources`, `related_plan`, `related_release`, `related`, `supersedes`, and `superseded_by` must resolve when they identify local paths. Plain metadata identifiers do not replace a navigable Markdown relationship when Obsidian backlink behavior is required.

Artifacts with `artifact_role: record` or `artifact_role: generated` require an outgoing relationship to an authoritative local source; self-links and a link only to the generated catalog do not satisfy it. A deliberate orphan exception requires `orphan_policy: allowed`, a specific `orphan_reason`, accountable `orphan_owner`, and a non-expired ISO `orphan_review_due`.

Markdown link destinations are source-relative and portable; vault-root interpretation applies only to Obsidian wikilinks. Inline-code examples are not graph edges, and paths containing spaces use valid percent-encoded or angle-bracket destinations.


## Language review - `fcvw/language-review@1`

Each complete language-specific release variant contains `FCVW/LANGUAGE_REVIEW.md` with `language`, `status`, `reviewer`, `reviewed_at`, and `source_revision`. Allowed statuses are `draft`, `in_review`, `approved`, and `rejected`.

Only `approved` review evidence for the exact immutable source revision permits a language-specific release asset. Explicit release validation receives an external authoritative clean source root and revision, compares the `en-US` functional manifest against that source, uses its own authoritative validator against the source and every staged variant, and checks structural and machine-surface parity. Release-only review evidence is excluded from source-manifest equality but must exist and match across all variants. Candidate validator copies are never executed before parity and trust are established. This record validates accountable language adaptation; directory naming or machine translation alone is insufficient.

This schema is a release-production contract. Normal framework validation, instantiation, and use neither require multiple language directories nor select a language automatically.

Create the evidence from [TEMPLATE_LANGUAGE_REVIEW.md](governance/TEMPLATE_LANGUAGE_REVIEW.md).

## Troubleshooting - `fcvw/troubleshooting@1`

New troubleshooting records use a collision-resistant `TRB-YYYYMMDD-<short-id>` ID and declare record ownership, `record_scope`, `search_only` retrieval, failure status, confidence, detection/review dates, related plan, sources, and tags. Allowed statuses are `draft`, `in_validation`, `validated`, and `obsolete`; allowed confidence values are `low`, `medium`, and `high`.

The record preserves identification, symptom, hypotheses, root cause, applied solution, validation, prevention, wiki-promotion decision, and final status. A navigable Markdown link connects it to its authoritative plan, policy, or evidence. Untouched historical troubleshooting without a schema remains readable; once substantively edited, migrate it through [TEMPLATE_TROUBLESHOOTING.md](governance/TEMPLATE_TROUBLESHOOTING.md).
