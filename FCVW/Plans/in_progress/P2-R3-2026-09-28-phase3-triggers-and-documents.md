---
schema: "fcvw/plan@2"
id: "P2-R3-2026-09-28-phase3-triggers-and-documents"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "in_progress"
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

- [ ] A path-to-events case table (framework and typical application paths) is tested.
- [ ] A project profile edit reads at most 40 KB of mandatory context; no route reads more than the phase 1 baseline.
- [ ] Every rule of the frozen inventory still emits; new rules are added to it.
- [ ] Suite, governance, benchmark and installed smoke pass on Python 3.10 to 3.13.

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

- [ ] Route case table and byte measurement against the phase 1 baseline.
- [ ] Allowed, denied and ambiguous boundary cases for routing.
- [ ] Full local runner on four interpreters.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Routing (G-03, B-06, B-07, C-03, C-04, G-02) | pass | `changed_file_events` derives only facts: any add, delete, move or rename implies `filesystem` (B-06); `.github/workflows/` alone implies `automation` (C-03); `AGENTS.md`, `.cursorrules` and `.windsurfrules` imply `policy` and `ai` (B-07); application paths imply no semantic event (G-03, closing B-08, B-09 and C-04) and a versioned application change without one returns a `warnings` entry. A 23-case path table covers framework and application paths in both layouts. `retrieve_context.py` resolves routes without `--index`/`--query` (G-02). The section-hint parser now accepts nested paths, which also activated the existing `BRIEFING.md` row; a `wiki/README.md` row was added. Local runner pass |

### Limitations and residual risk

- Recorded at closeout.

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
| Closeout | in progress | recorded at completion |

## Gaps and residual risk

Recorded at closeout.
