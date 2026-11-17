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
- Across several versions, apply the sections in order but skip what V0.20.0 retired: queue files (`QUEUE.md`, `queue.d/`), a versioned `DOCUMENT_GRAPH.md`, and regenerating `ROLE_MANIFEST.json` (the release ships it).

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
4. Review active `fcvw/plan@2` plans at risk `R3` or above that declare
   `regression_contract: not_applicable`: the combination is now invalid.
   Completed plans remain valid historical evidence.
5. Review `fcvw/plan@2` plans without a populated `Rollback` section, then run the validator.

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

A project that adopts or upgrades FCVW usually carries findings it cannot fix in the same change. Record them once, then let the gate fail only on new ones:

```powershell
python FCVW/tools/validate_fcvw.py --root . --write-baseline --baseline-owner <owner>
python FCVW/tools/validate_fcvw.py --root .
```

The first command writes `FCVW/audits/legacy-baseline.md` (`fcvw/legacy-baseline@1`, format in `governance/TEMPLATE_LEGACY_BASELINE.md`) with every current blocking finding, a review date (default 90 days, `--baseline-review-due`) and a justification (`--baseline-justification`). Run it again after fixing debt: reviewed rows keep their justification, fixed rows are dropped. The default `--profile auto` validates an instantiated project as `incremental` while that file exists; `--baseline <file>` names another one.

A row matches by path, rule and message, ignoring line numbers and successor hints, so moving text does not turn known debt into a new finding. A changed message, a new path, an expired or malformed baseline fails. Accepted findings are summarized by rule (`--show-baseline` lists them); stale rows are warnings. `strict` and `clean-template` accept no baseline. Never record a finding introduced by the change under review.

Before recording, remove the mechanical part of the debt: `--fix-moved-links` rewrites links and `context_files` whose target moved status directory or was renamed in git history (`MECHANICAL` in the summary counts them).

## V0.13.0 to V0.14.0

V0.14.0 introduces structured frontmatter validation, plan queues, application rules, document-graph integrity, optional lexical retrieval, proportionality governance, and language-specific release contracts.

Required migration:

1. Preserve project profiles and records.
2. Add `APP_RULES.md` as a preserved project profile and populate only confirmed rules.
3. Resolve new graph orphans rather than hiding them.
4. Validate first-level frontmatter lists and repair duplicate or unsupported YAML constructs in substantively touched files.
5. Keep optional context indexes outside normative records and rebuild them from sources.

Historical artifacts are not rewritten only to add retrieval metadata or new optional ownership fields. Language choice needs no downstream migration: a user downloads one variant, a normal monolingual tree. The release-production rules introduced here (external staging, lock and source revision) live in `RELEASE.md`.

## V0.14.0 to V0.15.0

V0.15.0 adds durable plan dependency evidence and additive typed/source-aware wiki metadata while preserving both canonical state queues, `fcvw/plan@2`, `fcvw/wiki@1`, BM25, JIT routing, and the document graph.

Required migration:

1. Preserve all project-owned plans and wiki records; do not rewrite completed history solely for optional fields.
2. For each active `fcvw/plan@2` whose queue row contains internal blocker IDs, add those IDs to `depends_on` and create one Dependency validation row per ID.
3. Keep pending or in-progress prerequisites as `pending`. Mark a dependency `satisfied` only after its prerequisite is completed and concrete evidence is recorded.
4. Treat a discontinued prerequisite as `invalidated`; keep the dependent plan blocked until it is explicitly replanned, replaced, or discontinued.
5. Existing wiki pages remain valid without maturity, typed relations, or source metadata. Add them only when the page is substantively reviewed and the semantics improve retrieval or impact analysis.
6. Replace any proposed tracked-source `content_hash` with `source_digest`; context chunks continue exposing `content_hash` as a compatibility alias plus `chunk_hash`.
7. Do not add `status: stale`. Generate stale-source and dependent-review findings, review affected knowledge, and update digests only after that review.
8. Keep generated knowledge graphs, stale reports, context indexes, and aggregate queue views in `.fcvw-cache/` or another disposable location.
9. Rebuild the context index before using new metadata filters or typed graph expansion. Graph expansion remains opt-in, relation-selected, one-hop, and bounded.
10. For a fresh V0.15.0 release installation, copy the two payload entries only: root `AGENTS.md` and `FCVW/`. Installed commands now use `FCVW/tools/`.
11. For an existing installation, back up populated profiles and records, merge the new `FCVW/` tree by ownership, and do not bulk-move or delete root `tools/`, `LICENSE`, `NOTICE`, `.cursorrules`, or `.windsurfrules`; those names may belong to the application.
12. Remove an older root framework file only after matching it to the prior release manifest and confirming that it has no application modification. Ambiguous files remain for manual reconciliation.
13. Run the complete validator and test suite after migration.
14. After a successful contained installation, framework removal consists of backing up any project-owned records, deleting `FCVW/`, then reviewing and optionally deleting the separately customized `AGENTS.md`.

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

The adaptive-experiment and loop-evaluation tools added here were removed in V0.20.0;
when continuing to V0.20.0 or later, skip their setup. External ledgers and evidence
stay yours; the last tools and the
[experiment contract](https://github.com/Sistema2D/FrameCode-VibeWork/blob/0b3cb546062e154be169521fed50bec2f3b28383/FCVW/governance/ADAPTIVE_EXPERIMENT_CONTRACT.md)
are at that revision.


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


## V0.20.0 to V0.21.0

Additive; no file moves and no schema major change.

1. New repository-wide rule `markdown-anchor`: every `#fragment` of a local
   Markdown link names a heading or an explicit `<a id>`. Fix renamed headings,
   or list existing debt in an incremental legacy baseline.
2. A broken link now names its successor. For a plan that changed status
   directory, `validate_fcvw.py --fix-moved-links` rewrites the link; for a
   removed framework path, the hint comes from the tables in this file.
3. Wiki pages may add `evidence_method`, `verified_by`, and a `#anchor` in a
   Markdown `source_path`. Existing pages stay valid; after narrowing a
   `source_path` to a section, refresh its digest with
   `knowledge_graph_fcvw.py --digest PATH#anchor`.
4. The route output of `retrieve_context.py` adds `ranges` and `context_bytes`;
   existing keys are unchanged.
5. The middle column of the `CONTEXT_MAP.md` selective-loading table now holds
   exact section headings. A project that edited that policy re-applies its
   notes when the upgrade reports a conflict.

## V0.21.0 to V0.22.0

Additive; nothing to migrate. The optional `FCVW/tools/mcp_server_fcvw.py`
lets an MCP-capable harness call routes, section reads, validation, the plan
queue and digests. Register it only if wanted; see `AI.md`.

Routes now add `FCVW/APP_RULES.md` when application files change in a project
whose rules are `complete`, as the context map already required. In
`PROJECT.md`, replace a governance-layer line that names a framework version
with a pointer to `FRAMEWORK_LOCK.md`.

## V0.22.0 to V0.23.0

Additive; nothing to migrate. `FCVW/tools/hook_fcvw.py` adds opt-in hooks for
Claude Code and Codex. To enable them, add the configuration from
`AUTOMATION.md` and record an `fcvw/automation@1` contract with
`scenario: "2"` and `authorized_by`; `FCVW_HOOKS=off` disables them.
The contract is the switch: it must name `implementation`, `hook_events` and
`harnesses` (see the ready template in `TEMPLATE_AUTOMATION_CONTRACT.md`), and
the hooks act only while it is `active`. The new `automation-binding` rule
reports configured hooks without such a contract, and the reverse.

## V0.23.0 to V0.24.0

Additive tools and rules; no file moves. Upgrade with `upgrade_fcvw.py`, then:

1. **Profile.** `validate_fcvw.py` without `--profile` now infers it: `project-instantiated` in `FRAMEWORK_LOCK.md` or `instantiation_status: complete` in `PROJECT.md` means `instantiated`. Commands that pass `--profile` behave as before; hooks and the MCP server default to `auto`.
2. **Debt.** The new rules below report findings in existing completed plans. Fix what is cheap, then record the rest with `--write-baseline` ([legacy baseline](#legacy-baseline)).
3. **Closeout.** `plan-acceptance`: a completed `fcvw/plan@2` or compact plan has no `[ ]` item, and `[~]` names `deferred: <plan-id>` or `waived: <reason>`. `plan-deferral`: the target plan carries a deferred criterion as `from: <origin-id>`. Legacy `fcvw/plan@1` records are not re-judged. Decide each open box: `[x]` with evidence, or `[~]` with an address or reason.
4. **`context_files`.** A bare entry is a repository path (as `retrieve_context.py` always read it); `./` and `../` stay plan-relative, and a bare path found only next to the plan is still accepted. A target deleted after a completed plan is a warning, not an error.
5. **Graph inventory.** Inside a git work tree the graph, catalog, knowledge graph and context index read git's view (`.gitignore` applies); transient trees and nested worktrees are skipped. Declare tracked Markdown that FCVW does not govern (vendored docs, mirrors) in `PROJECT.md` frontmatter `ungoverned_paths`. `document_graph_fcvw.py --write` no longer validates; add `--check`.
6. **Gates.** Optionally declare `PROJECT.md` Validation gates and run `gates_fcvw.py` before committing ([TESTS.md](TESTS.md#gate-selection-by-change-surface)).
7. **Removal.** A project that kept a local "requested removal" section in `REFACTORING.md` finds it upstream as section 26; the upgrade's conflict report shows any local wording to keep.
8. **Failures found during execution.** `PLANNING.md` now holds the "failure found, failure handled" rule; a project that kept it locally can point to it. Plans created for such failures declare `found_by`, and the finding plan names them (`plan-origin`); existing plans are not affected.
9. **Release guard.** Add `unreleased_limit: "5"` (or the project's number) to `PROJECT.md` to block a backlog of unreleased fragments (`release-backlog`); without it only the `release-unassembled` warning applies. A project that used a local release gate tool can retire it.
10. **Drafted plans.** `source` and `ai_review` are framework fields: a plan with `ai_review: pending` is blocked in the queue and invalid in `in_progress` or `completed` (`plan-review`).

Rollback: reinstall V0.23.0 by ownership. Its validator ignores the new `PROJECT.md` fields but reports `FCVW/audits/legacy-baseline.md` as `audit-schema`: move the file outside `audits/` and pass it with `--profile incremental --baseline`.
