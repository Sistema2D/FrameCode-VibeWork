---
schema: "fcvw/plan@2"
id: "P2-R3-2026-09-28-phase3-triggers-and-documents"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P2"
risk: "R3"
created_at: "2026-09-28"
updated_at: "2026-09-28"
current_version: "V0.19.0"
expected_version: "V0.20.0"
owner: "framework-maintainer"
regression_contract: "required"
category: "correction"
context_files:
  - "FCVW/CONTEXT_MAP.md"
  - "FCVW/AI.md"
  - "FCVW/SCHEMAS.md"
  - "FCVW/PLANNING.md"
  - "FCVW/REGRESSION_GUARDS.md"
  - "FCVW/TESTS.md"
depends_on: []
---

# Phase 3: triggers and documents

## Description

Execute phase 3 of the source-only maintainer backlog (`TODO.md`, section 11) on the reduced structure: fix triggers that do not fire or fire by mistake, make skill triggers descriptive, validate ADRs, and align the documents. The maintainer asked for this phase before publishing, so it ships in V0.20.0 instead of a separate V0.21.0.

## Justification and objective

Routing guesses semantic events from application file names: `auth_service.py` never loads `SECURITY.md`, while `src/skills/` or `.github/FUNDING.yml` load unrelated policies. Discovery by substring accepts `XAI.md` for `AI.md`. `trigger_keywords` are required but read by no tool. The root README is 745 lines with per-version sections.

## Scope

### Included

1. Routing: G-03 (no semantic guessing for application paths; a warning when code changes declare no semantic event), B-06, B-07, C-03, C-04, and G-02 (`--routes-only`).
2. Validator: B-04 (exact discovery), B-10 (ADR schema check), C-05 and C-06 (`trigger_keywords` optional, trigger in `description`), C-08.
3. Documents: F-02, F-08, D-02, D-03, D-05, D-06, D-08, D-09, E-05, E-08 and the G-01 re-measurement.

### Excluded

F-04 and F-03 (need the release variant pipeline), G-05 (hosted CI needs a new maintainer decision), the knowledge vault (phase 5).

## Affected files or boundaries

`tools/context_routing_fcvw.py`, `tools/retrieve_context.py`, `tools/validate_fcvw.py`, their tests, `AGENTS.md`, the root `README.md`, `FCVW/README.md`, `CONTEXT_MAP.md`, `AI.md`, `SCHEMAS.md`, `PLANNING.md`, skills frontmatter.

## Implementation plan

Routing, then validator, then documents; each batch keeps the suite green.

## Proportionality gate

- Real problem: false negatives and false positives in mandatory reads, measured in bytes per route.
- Existing solutions reused: role-based routing from phase 1, the document graph link extraction, the declarative record table.
- New code: a warning list in the route result and one ADR record specification; heuristics are removed rather than extended.

## Acceptance criteria

- [x] A path-to-events case table (framework and typical application paths) is tested: 23 cases in both layouts.
- [ ] A project profile edit reads at most 40 KB of mandatory context; no route reads more than the phase 1 baseline. **Partly met:** a `PROJECT.md` edit reads 22 KB. Summed over the 34 routes, section-first reading fell from 563 to 526 KB against V0.19.0 (the phase 1 tree is equivalent for routes), but 10 routes grew by 0.1 to 2.3 KB, mainly because one `PROJECT.md` (preamble plus its largest section) replaced near-empty placeholder profiles.
- [x] Every rule of the frozen inventory still emits; new rules are added to it (`adr-schema`, 117 IDs).
- [x] Suite, governance, benchmark and installed smoke pass on Python 3.10 to 3.13.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

Mandatory context routes, the retrieval CLI, skill validation, ADR records, agent instructions in `AGENTS.md`.

### Regression contracts consulted

- [Context map](../../CONTEXT_MAP.md) — event table.
- [AI](../../AI.md) — retrieval boundary.
- [Tests](../../TESTS.md) — boundary cases.

### Regression checks required

- [x] Route case table and byte measurement against the phase 1 baseline.
- [x] Allowed, denied and ambiguous boundary cases for routing (application path with and without a declared event, framework path, unknown operation, path escape).
- [x] Full local runner on four interpreters.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Migration rehearsal rerun (V0.19.0 to this tree) | pass | All 20 project-owned files keep their SHA-256 digests after `--apply --prune`; the only new finding versus phase 2 is the documented warning for a legacy ADR without an envelope. Found before it shipped: the validator would have made every pre-V0.20.0 application ADR an error, because the old template had no frontmatter and used `—` in the title; schema-less ADRs are now warnings and both title separators are accepted |
| Documents (F-08, D-03, D-05, D-06, D-09, E-05, G-01; D-02, D-08, E-07, E-08 already resolved in phase 2) | pass | F-08: `AGENTS.md` and `PLANNING.md` define a trivial prose fix that needs no plan (no frontmatter, link, table, heading, code or `framework_policy` file; conventional commit). D-03: [ADR-0012](../../decisions/ADR-0012-optional-tooling-restored.md) records that no versioned artifact is tool-generated any more. D-05: one statement on the `FCVW/tools/` versus `tools/` prefix. D-06: Python 3.10 or later in `TESTS.md` and the README. D-09: `OWNERSHIP.md` calls the bridges legacy and forbids new ones without demand. E-05: root README 690 to 249 lines, current state only, stale facts corrected (skill count, roles, validation commands); per-version section removed from `FCVW/README.md` along with the stale claim that empty record directories keep a README. Found while measuring: the merged skills had garbled "formerly" headings, now fixed. G-01: section rows added for `MIGRATIONS.md`, `OWNERSHIP.md`, `INSTANTIATION.md` and `governance-validator`; `AGENTS.md` trimmed below its V0.19.0 size; result published in `AI.md` |
| Validator (B-04, B-10, C-05, C-06, C-08, F-02) and skill triggers | pass | B-04: the index, catalog and session-route checks compare exact link-target parts and inline-code tokens; fixtures prove `XAI.md` no longer indexes `AI.md` and prose or `qa-extended` no longer list skill `qa`. B-10: `fcvw/adr@1` joins the declarative record table with new rule `adr-schema` (inventory 117 IDs): id format, status enum, filename and H1 match the id, and a superseded ADR names `superseded_by`. This marked ADR-0006, 0008 and 0009 as superseded by ADR-0010, which removed their layers. C-06/C-05: `trigger_keywords` is optional and deprecated; all 18 skill descriptions now state what the skill does plus "Use when" and "Do not use when" with the neighbouring skill, and each skill's patch version is bumped. Self-improvement gate: failure evidence passes (7 colliding keywords, an unread field); rule drift passes (the schema required a field no tool consumed); scope is preserved (bodies, session types and outputs unchanged). C-08: inline code is not scanned for damaged dashes. F-02: `SCHEMAS.md` keeps only versioned artifacts; disposable outputs are documented in their tools' docstrings (22.3 to 21.1 KB). Local runner pass |
| Routing (G-03, B-06, B-07, C-03, C-04, G-02) | pass | `changed_file_events` derives only facts: any add, delete, move or rename implies `filesystem` (B-06); `.github/workflows/` alone implies `automation` (C-03); `AGENTS.md`, `.cursorrules` and `.windsurfrules` imply `policy` and `ai` (B-07); application paths imply no semantic event (G-03, closing B-08, B-09 and C-04) and a versioned application change without one returns a `warnings` entry. A 23-case path table covers framework and application paths in both layouts. `retrieve_context.py` resolves routes without `--index`/`--query` (G-02). The section-hint parser now accepts nested paths, which also activated the existing `BRIEFING.md` row; a `wiki/README.md` row was added. Local runner pass |

### Limitations and residual risk

- Removing name-based guessing means an application change routes semantic policies only when the host declares the event; the warning makes the omission visible but cannot detect it semantically.
- Ten routes are slightly larger than in V0.19.0; see the acceptance criteria.
- Skill triggers in `description` are prose and are translated in language variants; no tool matches them.
- F-04 and F-03 remain deferred.

## Validation plan

Focused tests per batch, full suite, governance and the local runner on four interpreters at the end.

## Rollback

Revert the phase commits; no schema major changes and no downstream data migration.

## Gates and approvals

- Regression gate: route case table and byte measurement.
- Release gate: ships in the V0.20.0 candidate.

## Related records

- Framework release: [V0.20.0](../../framework-releases/V0.20.0.md).
- Previous phase: [phase 2](../completed/P2-R4-2026-09-28-phase2-file-reduction.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Local runner, Python 3.10, 3.11, 3.12 and 3.13 (Linux) | pass | `check_fcvw.py` report `20260928T130027Z-c5517848` on the closeout worktree: 280 tests, clean-template governance with 0 findings, labeled retrieval benchmark and installed smoke all pass on each interpreter |

## Gaps and residual risk

See *Limitations and residual risk*. Hosted CI (G-05) still needs a maintainer decision; the knowledge vault is phase 5.
