---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Framework migrations

## Principles

- Migrate framework-owned surfaces; preserve project-owned truth and history.
- Never normalize all historical records merely to satisfy a new schema.
- Enforce the current schema on new or substantively edited records.
- Record legacy exceptions in a baseline and reduce them over time.
- Do not mark the framework lock as upgraded until validation passes.

## V0.12.0 to V0.13.0

### Reason

The V0.12.0 clean package reduced many operational documents, templates, refactoring guides, and skills to placeholders. Real-application evidence also showed that manual-only validation, sequential session IDs, mixed version namespaces, and destructive memory rotation did not scale.

### Required migration

1. Preserve project profiles and all record directories.
2. Restore operational framework policies and specialized templates.
3. Add `FRAMEWORK_LOCK.md`, `OWNERSHIP.md`, and `SCHEMAS.md`.
4. Move FCVW release history to `framework-releases/`; keep application releases in `changelogs/`.
5. Add schema metadata when records are created or substantively edited.
6. Replace destructive session deletion with archive and synthesis.
7. Use collision-resistant session IDs for new sessions.
8. Regenerate `FILESYSTEM.md` and run validation.
9. Remove production-derived comparison fixtures from the framework project after extracting only generic, reviewed contracts.
10. Adopt `fcvw/plan@2` for new and substantively reopened plans, including `regression_contract` and a completed Regression impact section.
11. Add `REGRESSION_GUARDS.md`, the Regression gate, watcher triggers, risk matrix, and `wiki/regressions/` template.

### Compatibility notes

- Historical plan filenames outside the current P1–P5/R1–R5 convention remain valid legacy evidence.
- Historical wiki pages without frontmatter are not rewritten automatically.
- Existing sequential session filenames remain readable; new pages require a unique `id`.
- Existing application changelogs stay in place. Only framework-release records move to the new namespace.
- Existing `fcvw/plan@1` records stay readable and are not rewritten solely for the Regression impact requirement.
- A confirmed regression may be promoted to `fcvw/regression@1`; do not fabricate records during migration.

## V0.15.0 to V0.16.0

V0.16.0 remediates the V0.15.0 audit. The migration is additive: no existing
artifact needs rewriting, and no existing schema was narrowed enough to
invalidate prior records.

Required migration:

1. Preserve project profiles and records.
2. Replace framework policies, templates, skills, and tools.
3. Move `.cursorrules` and `.windsurfrules` from `FCVW/` to the repository root
   if the previous installation has them. Inside `FCVW/` they have no effect.
4. Generate `FCVW/ROLE_MANIFEST.json` with
   `python FCVW/tools/role_manifest_fcvw.py --root . --write` immediately after
   replacing the framework files, and never again afterwards. Without it, the
   next upgrade cannot tell a locally edited policy from an untouched one.
5. Adopt fragmented queues when convenient: create `Plans/<state>/queue.d/` and
   move one `QUEUE.md` row at a time into an `fcvw/plan-queue-entry@1` fragment.
   While the directory does not exist, the legacy queue stays canonical and valid.
6. Review active `fcvw/plan@2` plans at risk `R3` or above that declare
   `regression_contract: not_applicable`: the combination is now invalid.
   Completed plans remain valid historical evidence.
7. Review `fcvw/plan@2` plans without a populated `Rollback` section.
8. Regenerate `DOCUMENT_GRAPH.md` and the queue views, then run the validator.

Compatibility notes:

- `fcvw/plan@1` and `fcvw/plan@2` remain readable without retroactive editing.
- The compact class `fcvw/plan-compact@1` is optional; no existing plan needs to
  migrate to it.
- Link resolution became lexical instead of syscall-based. A repository relying
  on symbolic links to resolve Markdown would see a difference; the packaging
  contract already forbade them.
- The six reproduced refactoring catalog pages were consolidated into
  `refactoring-guide/02-refactoring-catalog.md`. Old links must be redirected;
  the validator reports each one.

## Legacy baseline

The `incremental` profile accepts a project-specific baseline for pre-existing findings:

```powershell
python tools/validate_fcvw.py --root . --profile incremental --baseline path/to/legacy-baseline.md
```

Start from `governance/TEMPLATE_LEGACY_BASELINE.md`. The file and each row are time-bounded. Every entry must contain the exact path, rule identifier, existing message, justification, owner, and review date. Only the exact tuple `path + rule + message` becomes non-blocking; changed messages and new paths still fail. Expired or malformed baselines fail configuration, and entries that no longer match are reported as stale warnings so they can be removed.

Without `--baseline`, `incremental` blocks all applicable findings. `--baseline` is rejected under other profiles; `strict` always blocks all applicable findings.

## V0.13.0 to V0.14.0

V0.14.0 introduces structured frontmatter validation, plan queues, application rules, document-graph integrity, optional lexical retrieval, proportionality governance, and language-specific release contracts.

Required migration:

1. Preserve project profiles and records.
2. Add `APP_RULES.md` as a preserved project profile and populate only confirmed rules.
3. Add active plans to their exact `QUEUE.md`; completed and discontinued records remain historical.
4. Regenerate `DOCUMENT_GRAPH.md` and resolve new orphans rather than hiding them.
5. Validate first-level frontmatter lists and repair duplicate or unsupported YAML constructs in substantively touched files.
6. Keep optional context indexes outside normative records and rebuild them from sources.
7. Do not migrate the repository or an installed framework to a multilingual layout. Prepare `pt-BR`, `en-US`, `es`, and `de` as independent empty-template variants in external release staging.
8. Keep `FRAMEWORK_LOCK.md` on the published installed baseline while V0.14.0 is `in_preparation`; advance it with the release record only at the `ready` gate.
9. Bind complete language-variant validation to an external clean source root and immutable source revision; do not validate a staged variant against itself.
10. Record the reviewed content baseline separately from the later tagged publication revision to avoid a self-referential commit hash.

Historical artifacts are not rewritten only to add retrieval metadata or new optional ownership fields.

Language choice requires no downstream migration. A user selects one language by downloading that release variant, and the resulting framework behaves as a normal monolingual tree without automatic detection, fallback, or synchronization.

## V0.14.0 to V0.15.0

V0.15.0 adds durable plan dependency evidence and additive typed/source-aware wiki metadata while preserving both canonical state queues, `fcvw/plan@2`, `fcvw/wiki@1`, BM25, JIT routing, and the document graph.

Required migration:

1. Preserve all project-owned plans and wiki records; do not rewrite completed history solely for optional fields.
2. For each active `fcvw/plan@2` whose queue row contains internal blocker IDs, add those IDs to `depends_on` and create one Dependency validation row per ID.
3. Keep pending or in-progress prerequisites as `pending`. Mark a dependency `satisfied` only after its prerequisite is completed and concrete evidence is recorded.
4. Treat a discontinued prerequisite as `invalidated`; keep the dependent plan blocked until it is explicitly replanned, replaced, or discontinued.
5. Retain `Plans/in_progress/QUEUE.md` and `Plans/pending/QUEUE.md` as canonical. Delete or ignore any manually maintained aggregate queue; regenerate disposable views from the tool.
6. Existing wiki pages remain valid without maturity, typed relations, or source metadata. Add them only when the page is substantively reviewed and the semantics improve retrieval or impact analysis.
7. Replace any proposed tracked-source `content_hash` with `source_digest`; context chunks continue exposing `content_hash` as a compatibility alias plus `chunk_hash`.
8. Do not add `status: stale`. Generate stale-source and dependent-review findings, review affected knowledge, and update digests only after that review.
9. Keep generated knowledge graphs, stale reports, context indexes, and aggregate queue views in `.fcvw-cache/` or another disposable location.
10. Rebuild the context index before using new metadata filters or typed graph expansion. Graph expansion remains opt-in, relation-selected, one-hop, and bounded.
11. Regenerate `DOCUMENT_GRAPH.md` and run the complete validator/test suite.
12. For a fresh V0.15.0 release installation, copy the two payload entries only: root `AGENTS.md` and `FCVW/`. Installed commands now use `FCVW/tools/`.
13. For an existing installation, back up populated profiles and records, merge the new `FCVW/` tree by ownership, and do not bulk-move or delete root `tools/`, `LICENSE`, `NOTICE`, `.cursorrules`, or `.windsurfrules`; those names may belong to the application.
14. Remove an older root framework file only after matching it to the prior release manifest and confirming that it has no application modification. Ambiguous files remain for manual reconciliation.
15. Regenerate the graph with `python FCVW/tools/document_graph_fcvw.py --root . --write` and validate with `python FCVW/tools/validate_fcvw.py --root . --profile instantiated` after migration.
16. After a successful contained installation, framework removal consists of backing up any project-owned records, deleting `FCVW/`, then reviewing and optionally deleting the separately customized `AGENTS.md`.

Compatibility notes:

- Optional plan and wiki fields are additive within the existing major schemas.
- Active queue-only dependencies require migration because operational parity is now deterministic; historical terminal plans without `depends_on` remain readable.
- No embeddings, new runtime dependency, database, background service, shared canonical queue, or committed generated-index tree is introduced.
- Optional semantic wiki review remains non-blocking and cannot mutate canonical knowledge.
- The source checkout and pre-package language staging retain root `tools/` for development. Release assets relocate those tools under `FCVW/tools/` and omit repository-only root `README.md` and `.gitignore`.
- The single-folder removal shortcut applies directly to fresh V0.15.0-or-later assets. Older installations require the manifest-based reconciliation above; no migration may assume that same-named root files are framework-owned.

## V0.16.0 to V0.17.0

Replace framework-owned tools and policies using the role manifest; preserve all
project profiles and records. The optional router is disabled by default and has
no persistent state or required dependency. Existing retrieval arguments and output
remain compatible. Rebuild disposable indexes after source changes. To roll back,
omit the shadow flag or reinstall V0.16.0 using ownership-aware replacement.

## V0.17.0 to V0.18.0

Replace framework-owned tools and policies through the role manifest and preserve project records. Rebuild disposable indexes to obtain complete bounded chunks and updated identities. Exact-only matching intentionally rejects accidental substring matches. Structured routes and budget selection are optional; CLI metadata is additive. Shadow proposals now use a larger eligible pool and may change, while delivered lexical results remain independent of shadow scoring. Repository CI is source-only and is not installed into downstream projects. To roll back, omit the new flags or restore V0.17.0 by ownership and rebuild its index.

## V0.18.0 to V0.19.0

Adaptive experiments add opt-in controls and strict external JSON contracts.
Existing default/shadow invocations remain valid. No state is migrated or loaded
implicitly. Before using assist, obtain reviewed evidence and prepare a source-bound
control/runtime; changing control requires revalidated state and a new scoped run.
The V0.19.0 experimental `start`/`observe` commands require an
explicit trusted `--ledger` SQLite path, and controlled retrieval requires the
same `--adaptive-ledger` path. Create a fresh external ledger; manually created
runtime JSON is not accepted for assist until registered through `start`. Keep
the ledger outside the release payload or under disposable `.fcvw-cache`, back it
up with runtime files when continuing an experiment, and restrict write access.
Reset/export/rollback operate on external derived files and preserve QA/safety stops.
The current pilot does not satisfy activation. See the
[experiment contract](https://github.com/Sistema2D/FrameCode-VibeWork/blob/0b3cb546062e154be169521fed50bec2f3b28383/FCVW/governance/ADAPTIVE_EXPERIMENT_CONTRACT.md).


Loop evaluation adds optional external JSON schemas and tools; no existing benchmark,
application record or retrieval invocation is migrated. Create a separately frozen
protocol for new evaluations. Do not infer loop events from old benchmark outcomes
or backfill missing usage with estimates labeled as provider measurements. Retain
external evidence and rebuild reports explicitly; no collector runs by default.


QA 1.1.0 requires user consultation for every behavior divergence. The optional
selected-run report adds divergence metrics, pending cases and user_decision_gate.
Existing runs remain readable; failing historical cases without question/response
evidence have a blocked decision gate. Preserve their original results and append
dated decision evidence when reviewed; never fabricate or backdate user answers.
Passing runs without divergences need no new table. No background scan is added.

The optional local validation runner reuses existing checks and preserves project records. No persistent state migration is required. The source repository removes the hosted workflow and retires its contract; no hook, service or runner is installed. Published V0.18.0 assets remain unchanged. After V0.19.0 installation, run its tools from `FCVW/tools/`.

QA adds optional product inventory, surface and execution templates within the existing wiki schema. Preserve populated product pages and QA audits as application records during upgrades; preserve their index as a project profile. Link existing approved specifications instead of duplicating or replacing them. The runtime field describes actual execution on any target; a browser is not mandatory. No adapters, browsers, simulators, board tooling or background service are installed. Invoke QA explicitly; first use maps the reachable application scope, then subsequent runs are selective.

## V0.19.0 to V0.20.0

V0.20.0 includes the integrity fixes prepared as V0.19.1, which was never
published, and the file reduction. Apply both parts in order.

### Integrity

1. Do not regenerate `FCVW/ROLE_MANIFEST.json`. It is the installation baseline;
   `role_manifest_fcvw.py --write` now refuses to overwrite it in an installed
   layout. If it was regenerated after local edits, compare each framework file
   with the release you installed before upgrading; the upgrade tool now reports
   every unverifiable difference as a conflict instead of replacing it.
2. Convert any `fcvw/plan@1` plan in `pending/` or `in_progress/` to
   `fcvw/plan@2` with a Regression impact and Rollback section. Completed and
   discontinued legacy plans stay valid without edits.
3. Add `schema: "fcvw/troubleshooting@1"` and its required fields to troubleshooting
   records that lack a schema, or list them in an incremental legacy baseline.
4. `--since` now keeps cross-file findings (links, graph, queues, knowledge,
   dependencies) from unchanged files; expect them in scoped runs.

### File reduction

Upgrade with the release's own tool, dry run first:

```sh
python <release>/FCVW/tools/upgrade_fcvw.py --root . --release <release>
python <release>/FCVW/tools/upgrade_fcvw.py --root . --release <release> --apply --prune
```

`--prune` deletes only framework-owned files the release no longer ships whose
bytes still equal the installation baseline: scaffolding READMEs, retired
policies and templates, the experiment tools, and the framework's own history
(plans, ADRs, audits and troubleshooting records with `record_scope: framework`).
Project profiles and application records are never pruned. A framework file you
edited is reported as `review` (dropped upstream, kept) or `conflict` (replaced
upstream; `--accept-conflicts` keeps a `.local` backup).

Then complete these manual steps; the validator reports each one until done:

1. **Project profiles.** Merge each legacy profile into the matching section of
   the new `FCVW/PROJECT.md`, then delete it. Until deleted, each one reports
   `profile-legacy` plus orphan findings.

   | Legacy file | `PROJECT.md` section |
   |---|---|
   | `MANIFEST.md`, `SCOPE.md` | Identity and scope |
   | `STACK.md` | Stack |
   | `ENVIRONMENT.md` | Environment |
   | `DESIGN.md` | Design |
   | `PERFORMANCE.md` | Performance |
   | `WORKFLOW.md` | Workflows |

   A section the project does not use goes into `not_applicable_sections`.
   A filled `BRIEFING.md` is a record: move it to `briefings/INITIAL_BRIEFING.md`.
   The questionnaire now lives in `skills/project-instantiation/BRIEFING.md`.
2. **Wiki index.** `wiki/index.md` is project-owned and keeps its links; replace
   links to `schema.md`, `taxonomy.md`, `log.md` or `metrics.md` with
   `README.md` (the wiki contract). Notes may stay in subfolders; new notes are
   flat under `wiki/` and are typed by `type`, not by folder.
3. **Plan queue.** Delete `Plans/*/QUEUE.md` and `Plans/*/queue.d/`. Move each
   plan's queue data into its frontmatter as `category`, and optionally
   `blocked_external` or `before_in_progress`; the queue is derived from the
   plans. Until then the old files report `plan-queue-legacy`.
4. **Document graph.** Delete `FCVW/DOCUMENT_GRAPH.md` if it survived the
   upgrade. Records are reachable through their record directory; generate a
   view on demand into `.fcvw-cache/`.
5. **Edited dropped policies.** For each `review` path, move local notes into
   the consolidating policy, then delete the file:

   | Removed | Consolidated into |
   |---|---|
   | `HOOKS.md`, `WATCHERS.md`, `DAEMONS.md`, `GOVERNANCE_GATES.md` | `AUTOMATION.md` |
   | `VERSIONING.md` | `RELEASE.md` |
   | `RETROACTIVE_INSTANTIATION.md` | `INSTANTIATION.md` |
   | `TOKEN_BUDGET.md` | `AI.md` |
   | `MEMORY.md`, `wiki/schema.md`, `wiki/taxonomy.md` | `wiki/README.md` |
   | `FILESYSTEM.md` | `OWNERSHIP.md` (filesystem layout) |
   | `refactoring-guide/` | `REFACTORING_GUIDE.md` |
   | `wiki/templates/`, most `governance/TEMPLATE_*` | `governance/TEMPLATE_NOTE.md`, `TEMPLATE_REFACTORING.md`, `TEMPLATE_APP_DOC.md`, `TEMPLATE_SKILL_CHANGE.md`, `TEMPLATE_AUTOMATION_CONTRACT.md` |
   | product and QA templates | `skills/QA/` |
   | skills `agnix-linter`, `wiki-lint` | `governance-validator` 2.0.0 |
   | skills `aicc-compact`, `memory-rotation` | `wiki-curator` 2.0.0 |

6. **Experiments.** `--adaptive-*` and `--optional-token-budget` are removed
   from `retrieve_context.py`, and the adaptive and loop tools are gone.
   External ledgers remain yours; the last tools that read them are at the
   revision linked in the V0.18.0 to V0.19.0 section.

Rehearsed on a V0.19.0 installation carrying application records, filled and
pending profiles, and two locally edited framework policies: every
project-owned file kept its SHA-256 digest.

### Triggers and records

1. **Declare semantic events.** Routing no longer guesses security, data,
   interface or AI impact from application file names. Pass the matching
   `--event` for application changes; the route result lists a warning when a
   versioned application change declares none. Adding, moving, renaming or
   deleting any file now implies `event:filesystem`.
2. **ADRs.** Decision records are validated as `fcvw/adr@1`. An ADR without the
   envelope is a warning, not an error: add the envelope from `TEMPLATE_ADR.md`
   when you next edit it. A superseded ADR names its replacement in
   `superseded_by`.
3. **Custom skills.** `trigger_keywords` is optional; move its intent into the
   `description` as "Use when …" and "Do not use when …".
4. **References.** The operational index, skill catalog and session routes must
   name a document or skill through a Markdown link or inline code; a bare prose
   mention no longer counts.

