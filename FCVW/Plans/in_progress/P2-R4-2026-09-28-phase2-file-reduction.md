---
schema: "fcvw/plan@2"
id: "P2-R4-2026-09-28-phase2-file-reduction"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "in_progress"
priority: "P2"
risk: "R4"
created_at: "2026-09-28"
updated_at: "2026-09-28"
current_version: "V0.19.1"
expected_version: "V0.20.0"
owner: "framework-maintainer"
regression_contract: "required"
category: "optimization"
context_files:
  - "FCVW/OWNERSHIP.md"
  - "FCVW/MIGRATIONS.md"
  - "FCVW/PLANNING.md"
  - "FCVW/REGRESSION_GUARDS.md"
  - "FCVW/TESTS.md"
  - "FCVW/CONTEXT_MAP.md"
depends_on: []
---

# Phase 2: file and folder reduction

## Description

Execute phase 2 of the source-only maintainer backlog (`TODO.md`, section J): remove empty and redundant files and folders, extract the inactive experimental layer from the core, and slim the validator, without losing any verifiable rule. The user approved the J-D recommendation and deferred V0.19.1 publication until this phase ends.

## Justification and objective

`FCVW/` has 228 files and 65 directories; 26 directories contain only a README, 11 profiles are placeholders and the templates are fragmented. The simulated target is at most 110 files and 30 directories (10 outside `skills/`).

## Scope

### Included

Work packages, each committed with a green suite. Executed order: WP1, WP3, WP4, WP5, WP6, WP7, WP2, WP8 — J-D (WP2) runs after the consolidations so that only the final set of policies, skills and templates is linked from the indexes.

1. WP1 — frozen rule-ID inventory test; upgrade `--prune` (A-08).
2. WP2 — J-D: records are reachable through canonical record directories; catalog READMEs, empty record directories and the versioned document graph are removed (J-08, J-11, J-14).
3. WP3 — the adaptive and loop experiment layer leaves the core (F-01). Framework history leaving the installed payload (F-05, J-13) moves after WP2, because the catalog READMEs removed there are what link to that history.
4. WP4 — flat wiki and single note template (J-01, J-02).
5. WP5 — queue derived from plan frontmatter; state READMEs removed (J-03, J-04).
6. WP6 — consolidated profiles, policies and templates (J-05, J-06, J-07, J-09, J-10, J-12).
7. WP7 — merged and renamed skills (J-15).
8. WP8 — lean validator and growth guards (E-01, E-02, E-04, F-04, B-05, J-G1 to J-G3).

### Excluded

Trigger heuristics (phase 3), the knowledge vault (phase 5), language variants and publication.

## Affected files or boundaries

Most of `FCVW/`, `tools/`, `AGENTS.md` and the source README. Ownership rules are preserved: framework policy and project-owned content never share a file.

## Implementation plan

See the work packages above; each records its evidence in the table below before the next starts.

## Proportionality gate

- Real problem: surface growth without matching executable rules (PLANNING.md "Framework proportionality").
- Necessary: approved by the user as the central objective.
- Existing solutions reused: current tools, frontmatter cache, release layout, upgrade tool.
- New code: only `--prune`, reachability by record directory and declarative record schemas; each removes more than it adds.
- Safeguards: frozen rule inventory, migration table, upgrade dry run, installed smoke test.

## Acceptance criteria

- [ ] `FCVW/` has at most 110 files and 30 directories (at most 10 outside `skills/`).
- [ ] Every rule ID of the frozen inventory still has an emitting rule, or its removal is justified here.
- [ ] A V0.19.0 installation migrates without losing records (digest comparison).
- [ ] Suite, governance, benchmark and installed smoke pass on Python 3.10 to 3.13.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

Validation rules, upgrade and packaging, retrieval routes and benchmark corpus, QA product checks, queue recommendation, document reachability, every path referenced by tests and policies.

### Regression contracts consulted

- [Ownership](../../OWNERSHIP.md) — replace versus preserve.
- [Migrations](../../MIGRATIONS.md) — downstream path moves.
- [Tests](../../TESTS.md) — structural suite.

### Regression checks required

- [ ] Frozen rule inventory reviewed at every package.
- [ ] Full suite and local runner on four interpreters at the end.
- [ ] Migration rehearsal on a materialized V0.19.0 installation.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| WP2b framework history out of the payload (F-05, J-13) | pass | `payload_mapping` skips framework-scoped plans, audits, troubleshooting records, ADRs and every framework release record; shipped policies link to them by absolute repository URL; an installed validator no longer requires the release record. Installed payload measured from `fdca53b` (V0.19.0) to now: 273 to 108 files, 66 to 24 directories, 1,457 to 994 KB (Markdown 815 to 467 KB). Old installations see the dropped history as `obsolete` and can remove it with `--prune` |
| WP2 J-D record reachability (J-08, J-11, J-14) | pass | [ADR-0011](../../decisions/ADR-0011-record-reachability.md). Finding: without the generated catalog, 148 files had no real incoming link, so the old reachability rule was vacuous. Now records are reachable through their canonical directory, other documents through real links from `FCVW/README.md`, the skills and template catalogs; legacy `FCVW/DOCUMENT_GRAPH.md` edges are ignored and the file is warned. Removed the versioned catalog and six directory READMEs; packager and smoke no longer write a catalog. A text scan for removed file names found stale mentions (including a `CONTEXT_MAP.md` row an aborted WP6c script had not updated); all fixed. 265 tests; governance 0 findings; benchmark pass |
| WP7 skills (J-15), self-improvement gate | pass, partial | Merged `agnix-linter` and `wiki-lint` into `governance-validator` 2.0.0, and `aicc-compact` and `memory-rotation` into `wiki-curator` 2.0.0, each as a named mode with the union of triggers and session types. Gate: rule drift passes (the merged skills cited `MEMORY.md`, `wiki/schema.md` and `wiki/log.md`, removed in WP4/WP6c); scope preservation and backward compatibility pass (old names remain as trigger keywords and mode titles); token ROI **not met** (17,848 to 17,461 bytes, about 2%), so the benefit claimed is fewer files and one owner per concern, not tokens. The renames of `agent-aegis`, `agent-hephaestus` and `agent-hermes` were **blocked** by the gate's naming-only rule and not applied. 264 tests; governance 0 findings |
| WP6 consolidated documents (J-05, J-06, J-07, J-09, J-10, J-12) | pass | 6a: guide (18 files) becomes `REFACTORING_GUIDE.md` loaded by section, 12 refactoring/hygiene/monolith templates become `TEMPLATE_REFACTORING.md`, 6 application-doc templates become `TEMPLATE_APP_DOC.md`, 2 skill templates become `TEMPLATE_SKILL_CHANGE.md`, retired CI contract and workflow removed (links pinned). 6b: HOOKS, WATCHERS, DAEMONS, GOVERNANCE_GATES merged into `AUTOMATION.md`; 4 kind templates merged into `TEMPLATE_AUTOMATION_CONTRACT.md`, whose envelope now carries the fields the validator requires (it previously declared `kind: gate` and omitted six required fields); a missing regression surface is now reported (B-03). 6c: VERSIONING, RETROACTIVE_INSTANTIATION, MEMORY, TOKEN_BUDGET and FILESYSTEM merged into their owners. 6d: seven profiles merged into `PROJECT.md` with per-section waivers; `profile-legacy` warning keeps populated downstream profiles validated; briefing questionnaire moved to the instantiation skill. 6e: examples folded into the plan and release templates; the example-plan regression marker is dropped because the plan template carries the same marker. 264 tests; benchmark and governance pass |
| WP5 derived queue (J-03, J-04) | pass | queue derived from plan frontmatter (`category`, `depends_on`, `blocked_external`, `before_in_progress`); 2 `QUEUE.md`, 2 `queue.d/` and 4 state READMEs removed; `plan_queue_fcvw.py` 501 to about 190 lines. Rule inventory: 12 `plan-queue-*` IDs retired because the queue/plan parity they protected no longer exists (status versus directory remains `plan-state`); `plan-queue-legacy` (warning) added for downstream migration; 6 new derived-queue tests |
| WP4 flat wiki (J-01, J-02) | pass | 20 scaffolding READMEs, `schema.md`, `taxonomy.md`, `log.md`, `metrics.md` and 12 wiki templates removed; rules merged into [the wiki contract](../../wiki/README.md) and [TEMPLATE_NOTE](../../governance/TEMPLATE_NOTE.md); product guide and 3 templates moved to `skills/QA/`; feedback selected by `type`; historical references to moved files updated; 260 tests; governance 0 findings |
| WP3 experiment layer removed (F-01) | pass | 6 tools, 3 test modules (69 tests), 2 contracts and 1 template removed; `retrieve_context.py` without `--adaptive-*`/`--optional-token-budget`; frozen rule inventory unchanged; historical links pinned to revision `0b3cb54`; [ADR-0010](../../decisions/ADR-0010-core-reduction.md); 260 tests; governance 0 findings |
| WP1 rule inventory and `--prune` | pass | 115 rule IDs frozen in `StaticIntegrityTests`; 4 prune tests (unmodified removed, modified kept, later prune, no baseline keeps); 329 tests |

### Limitations and residual risk

- Recorded at closeout.

## Validation plan

Per package: focused tests, full suite, governance. At the end: local runner on four interpreters and the migration rehearsal.

## Rollback

Revert the package commits in reverse order; the migration note keeps the old-to-new path table so moved records can be restored.

## Gates and approvals

- Regression gate: evidence per package.
- Release gate: V0.20.0 record in preparation; no publication.
- Decomposition: eight work packages, one commit each.

## Related records

- Framework release: to be recorded with V0.20.0.
- Previous phase: [V0.19.1](../../framework-releases/V0.19.1.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Closeout | in progress | recorded at completion |

## Gaps and residual risk

Recorded at closeout.
