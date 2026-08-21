---
schema: "fcvw/plan@2"
artifact_role: "record"
upgrade_strategy: "preserve"
record_scope: "framework"
id: "P2-R4-2026-08-21-single-folder-release-layout"
status: "completed"
priority: "P2"
risk: "R4"
created_at: "2026-08-21"
updated_at: "2026-08-21"
current_version: "V0.14.0"
expected_version: "V0.15.0"
owner: "Codex under the user's implementation authorization"
regression_contract: "required"
depends_on: []
context_files:
  - "AGENTS.md"
  - "FCVW/CONTEXT_MAP.md"
  - "FCVW/PLANNING.md"
  - "FCVW/REGRESSION_GUARDS.md"
  - "FCVW/OWNERSHIP.md"
  - "FCVW/FILESYSTEM.md"
  - "FCVW/RELEASE.md"
  - "FCVW/VERSIONING.md"
  - "FCVW/MIGRATIONS.md"
  - "FCVW/TESTS.md"
  - "FCVW/framework-releases/V0.15.0.md"
---

# Single-folder release layout

## Description

Implement GitHub issue #52 by making each FCVW release asset install all framework-owned filesystem content under `FCVW/`, with only `AGENTS.md` beside it at the application root.

## Justification and objective

The current release archive mirrors the source/staging tree and spreads framework files across `FCVW/`, `tools/`, root legal files, and editor adapters. Removal therefore requires path knowledge. The target layout makes removal mechanically understandable and prevents framework deletion from reaching unrelated application files.

## Scope

### Included

- Deterministic source-to-installed layout mapping during packaging.
- Root-shape, collision, forbidden-state, manifest, and safe-removal validation.
- Installed-layout support in the governance validator.
- Installed document-graph regeneration after relocation.
- Source-versus-installed command/path documentation, migration, rollback, tests, and V0.15.0 release evidence.

### Excluded

- Publishing assets, tags, commits, or releases.
- Automatic destructive uninstall.
- Moving Git repository infrastructure or changing the source checkout solely for cosmetic parity.
- Preserving root-only editor discovery behavior for `.cursorrules` or `.windsurfrules`; these become contained reference adapters in release assets.

## Affected files or boundaries

- Release packaging/layout tools and their tests.
- Clean-template validator required-path handling.
- Filesystem, release, installation, ownership, testing, migration, and root-entrypoint documentation.
- V0.15.0 release record and document graph.

## Implementation plan

1. Characterize the current archive manifest and define an explicit installed-layout mapper.
2. Materialize each variant into a temporary `AGENTS.md` + `FCVW/` tree, regenerate its graph, inspect it, and archive it deterministically.
3. Teach validation and documentation the source/installed path distinction.
4. Add positive, collision, extra-root, removal-residue, deterministic, and installed-validator tests.
5. Run R4 closeout, complete the plan, and close issue #52 with evidence.

## Proportionality gate

- Real problem: release files are physically scattered, making removal error-prone.
- Existing capability reused: language staging, deterministic ZIP writer, document graph, clean validator, and the existing `FCVW/` installation directory.
- Native capability: Python `pathlib`, `shutil`, `tempfile`, and `zipfile`; no dependency or installer is needed.
- Smallest viable solution: transform only release payloads and explicitly support their installed layout; keep repository-only landing and VCS files out of assets.
- Future evolution condition: add an uninstaller only if measured downstream upgrades/removals require state-aware preservation beyond deleting `FCVW/`.

## Acceptance criteria

- [x] Every archive has one conventional wrapper whose first-level payload is exactly `AGENTS.md` and `FCVW/`.
- [x] Tools, legal notices, adapters, policies, templates, and framework records reside under `FCVW/`.
- [x] Repository-only `README.md` and `.gitignore` do not leak into the installed root.
- [x] Manifest collisions and unexpected installed root entries fail deterministically.
- [x] Removing `FCVW/` leaves only the explicit framework entrypoint and does not target application paths.
- [x] The installed layout passes governance validation with a regenerated local document graph.
- [x] Source checkout behavior and language staging/parity remain supported.
- [x] Migration, rollback, documentation, tests, and V0.15.0 record agree.

## Regression impact

### Existing behaviors that may be affected

- Deterministic ZIP bytes, checksums, archive wrapper names, language parity, forbidden-state checks, source clean validation, document links, validator required paths, and commands copied by installed users.

### Regression contracts consulted

- `FCVW/RELEASE.md`, `FCVW/FILESYSTEM.md`, `FCVW/OWNERSHIP.md`, `FCVW/TESTS.md`, `FCVW/MIGRATIONS.md`, and `FCVW/REGRESSION_GUARDS.md`.

### Regression checks required

- [x] Existing archive determinism/checksum/replacement tests.
- [x] Existing locale and clean-source validation tests.
- [x] Negative collision, forbidden-state, root-entry, and unsafe-path tests.
- [x] Materialized-layout document graph and clean validator.
- [x] Full unit suite, AST, graph, queue, clean-template, and diff checks.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Pre-change unit suite | pass | 87 tests passed |
| Pre-change clean validator | pass | errors=0, findings=0 |
| Post-change checks | pass | 92 tests; source and installed validators 0/0; installed graph 198 nodes/0 findings |

### Limitations and residual risk

- Existing applications are not rearranged automatically; migration is explicit to avoid overwriting project-owned content.
- Removing `FCVW/` intentionally leaves `AGENTS.md`, which the user may delete separately after reviewing any local customization.

## Validation plan

- [x] Focused release-layout/package tests.
- [x] Full unit discovery.
- [x] Materialize the current clean source as an installed-layout fixture and run the authoritative clean validator.
- [x] Document/knowledge graphs, queue validator, Python AST, and `git diff --check`.

## Rollback

Restore direct staging-tree archiving and the source-layout validator contract. Existing source/staging trees remain unchanged, so rollback requires no downstream data rewrite. Do not delete application paths.

## Gates and approvals

- Regression/release/filesystem/migration gates: required, R4.
- External issue creation and closing: explicitly authorized by the user.
- Commit, push, tag, asset publication, and GitHub Release: not authorized.

## Anti-Monolith Gate

- Skill loaded: `skills/anti-monolith-guard/SKILL.md`
- Target artifact: release layout mapper plus existing packager/validator adapters.
- Primary responsibility: map and validate the installed release filesystem.
- Artifact class: `source`.
- Numeric threshold applicability: `applicable`.
- Explicit non-responsibilities: translation, publication, installation mutation, or application cleanup.
- Size budget: keep the mapper below 250 lines and patch packager/validator only at their existing boundaries.
- Similar code checked: `package_release_fcvw.py`, `locale_fcvw.py`, `document_graph_fcvw.py`, and clean-root validation.
- Split decision: `proceed` with a focused `release_layout_fcvw.py` module shared by packaging and validation.
- Validation: focused contract tests and full governance replay.

## Code Hygiene Scan

- Skill loaded: `skills/code-hygiene-refactor/SKILL.md`
- Scan level: `module`.
- Duplicate candidates: payload-path/root-layout checks in package inspection and clean validation.
- Large/monolithic candidates: do not expand the existing 2,040-line validator with mapping logic.
- Dead/stale candidates: root `README.md` and `.gitignore` are source-only, not installed payload files.
- Cleanup batch selected: centralize layout semantics and reuse them in both consumers.
- Behavior preservation evidence: determinism, locale, clean-source, and installed-layout tests.
- Deferred debt: broader validator decomposition remains outside this issue.

## Code Hygiene Report

### Inventory and findings

- `release_layout_fcvw.py`: 107 lines, single responsibility, used by packaging and installed-layout validation.
- `package_release_fcvw.py`: 250 lines, remains bounded to release validation/materialization/archive production.
- `validate_fcvw.py`: 2,058 lines, pre-existing catch-all; only layout detection, required-path mapping, compatibility alias, and contained-license exception were added.
- `test_open_issues.py`: 1,565 lines, pre-existing historical aggregation; focused layout cases were added beside existing package tests.

### Cleanup selected

- Centralized source-to-installed mapping, collision detection, root-shape validation, and removal residue in one focused module instead of duplicating them in package and governance code.
- Kept source-only exclusions explicit and small; no installer, registry, manifest database, symlink, or second framework wrapper was introduced.
- Reused `FCVW/`, temporary directories, document-graph generation, and deterministic ZIP infrastructure.

### Behavior preservation and deferred debt

- Deterministic archive/checksum, replacement boundaries, forbidden state, locale staging, source validation, and graph behavior are covered by the 92-test suite and both layout smokes.
- The validator and historical test aggregation remain decomposition candidates; splitting them is outside this release-layout behavior change.

## Skill/Agent Self-Improvement Gate

- Skill loaded: `skills/self-improvement/SKILL.md`
- Asset changed: `governance-validator`.
- Evidence: its only documented command referenced source-root `tools/`, which is absent from the contained installed release layout.
- Metric passed: canonical rule drift and validation gap.
- Scope preserved: validation responsibility and triggers are unchanged; only physical command selection is clarified.
- Token/risk ROI: prevents a guaranteed installed-command failure with a short two-layout distinction.
- Validation replay: source and materialized installed validators plus skill-contract validation.
- Decision: `patch`.

## Related records

- GitHub issue: [#52](https://github.com/Sistema2D/FrameCode-VibeWork/issues/52).
- Framework release: [V0.15.0](../../framework-releases/V0.15.0.md).
- Architectural decision: [ADR-0005](../../decisions/ADR-0005-contained-release-filesystem.md).
- Self-improvement report: [installed validator command](../../audits/2026-08-21-installed-validator-skill-self-improvement.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Focused package/layout suite | pass | 67 tests passed |
| Full unit suite | pass | 92 tests passed |
| Source clean validator | pass | errors=0, findings=0, baseline=0 |
| Installed layout shape | pass | first-level entries exactly `AGENTS.md` and `FCVW/` |
| Installed document graph | pass | nodes=198, findings=0 |
| Installed clean validator | pass | executed from `FCVW/tools/`, errors=0, findings=0 |
| Syntax and diff | pass | all Python ASTs valid; no diff whitespace errors |

## Gaps and residual risk

- Published language-specific assets remain intentionally absent because publication was not authorized; deterministic fixtures validate the new layout contract.
- Pre-V0.15.0 applications require manifest-based reconciliation before claiming single-folder removability.
