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
