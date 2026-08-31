---
schema: "fcvw/plan@2"
id: "P2-R4-2026-08-28-audit-remediation-and-scale-hardening"
artifact_role: "record"
owner: "framework-maintainer"
upgrade_strategy: "preserve"
record_scope: "framework"
retrieval_scope: "exact_only"
status: "completed"
priority: "P2"
risk: "R4"
created_at: "2026-08-28"
updated_at: "2026-08-28"
current_version: "V0.15.0"
expected_version: "V0.16.0"
regression_contract: "required"
context_files:
  - "FCVW/PLANNING.md"
  - "FCVW/REGRESSION_GUARDS.md"
  - "FCVW/SCHEMAS.md"
  - "FCVW/OWNERSHIP.md"
  - "FCVW/TESTS.md"
depends_on: []
---

# Remediate the V0.15.0 audit and harden the framework for scale

## Description

Fix the verified defects in the published V0.15.0 asset, close the contradictions
between policy and tooling, reduce the cost of operating in a large repository,
and make selective upgrade tool-assisted.

## Justification and objective

An independent audit of the published asset found defects that the framework own
gates should have blocked, and measured a validation cost that grows faster than
the repository. The objective is for the framework to remain operable in a large
project without governance becoming the bottleneck.

## Scope

### Included

- Content and contract defects in the published asset.
- Contradictions between `PLANNING.md`, `SCHEMAS.md`, and the validator.
- Performance and signal of the validation tools.
- Plan queue concurrency.
- Role manifest and assisted upgrade.
- Reduction of documentation surface reproduced from public literature.

### Excluded

- External publication of V0.16.0.
- Rewriting the derived surfaces into a single representation.
- Building release assets and checksums.

## Affected files or boundaries

- `AGENTS.md`, `FCVW/PLANNING.md`, `FCVW/SCHEMAS.md`, `FCVW/OWNERSHIP.md`,
  `FCVW/FILESYSTEM.md`, `FCVW/README.md`, `FCVW/TESTS.md`, `FCVW/AI.md`,
  `FCVW/MANIFEST.md`, `FCVW/FRAMEWORK_LOCK.md`, `FCVW/LANGUAGE_REVIEW.md`.
- `FCVW/tools/` — validator, graph, queues, locale, packaging, and three new modules.
- `FCVW/governance/` — compact plan template and CI workflow template.
- `FCVW/refactoring-guide/` — consolidation of the reproduced catalog.
- `FCVW/Plans/*/queue.d/` — queue fragments.

## Implementation plan

1. Fix the published asset defects and add the rule that detects them.
2. Introduce the compact plan class and bind risk to evidence.
3. Reduce tooling cost and noise.
4. Fragment the queues and publish the role manifest.
5. Add assisted upgrade and automation validation.
6. Consolidate the reproduced literature.

## Proportionality gate

- Real problem and root cause: gates declared in prose that no tool executed, and
  superlinear validation cost from repeated reads and syscall-based path resolution.
- Necessary in current scope: yes; the defects are in the published asset.
- Existing codebase solution checked: yes, the one-fragment-per-plan pattern
  already existed in `changelogs/unreleased/` and was reused for the queues.
- Native platform capability checked: yes, `os.path.normpath` replaces
  `Path.resolve()` without a syscall.
- Installed dependency checked: yes; no new dependency was added.
- New code or complexity justified: three new modules, each with a matching
  validator rule or an explicit `OWNERSHIP.md` contract.
- Minimum non-trivial behavior tests: the three structural suites plus the
  acceptance exercises recorded below.
- Deliberate simplification and limitations: the on-disk graph cache was refused
  on proportionality grounds; noise suppression solved the same problem without a
  new invalidation surface.
- Condition for future evolution: if validation again exceeds the accepted CI
  budget, revisit the graph cache with measurement.
- Mandatory safeguards preserved: security, privacy, accessibility, traceability,
  validation, audit, data integrity, documentation, and risk-required tests remain intact.

## Acceptance criteria

- [x] The three structural suites pass in the installed layout.
- [x] `validate_fcvw.py --profile clean-template` finishes with zero findings.
- [x] A compact plan as described by `PLANNING.md` validates.
- [x] A destructive `R5` plan with a waived contract is blocked.
- [x] No invisible character or damaged dash remains.
- [x] The language review record names the language it declares.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

- Validation of existing `fcvw/plan@1` and `fcvw/plan@2` plans.
- Reading legacy `QUEUE.md` queues in prior projects.
- Link and frontmatter relationship resolution.
- Machine-surface parity between language variants.
- The release package root contract.

### Regression contracts consulted

- [`REGRESSION_GUARDS.md`](../../REGRESSION_GUARDS.md) — blocking conditions.
- [`SCHEMAS.md`](../../SCHEMAS.md) — schema compatibility.
- [`OWNERSHIP.md`](../../OWNERSHIP.md) — ownership and removal boundary.

### Regression checks required

- [x] Full structural suites in the installed layout.
- [x] Clean validation before and after each tooling change.
- [x] A legacy `QUEUE.md` without `queue.d/` remains valid.
- [x] Lexical link resolution produces the same finding set.
- [x] Packaging still rejects an unexpected package root.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Structural suites | pass | `python -B FCVW/tools/test_validate_fcvw.py`, `test_open_issues.py`, `test_plan_dependencies_and_knowledge.py` |
| Clean validation | pass | `python FCVW/tools/validate_fcvw.py --root . --profile clean-template` |
| Legacy queue | pass | clean validation before `queue.d/` was created |
| Fragmented queue | pass | `plan_queue_fcvw.py --write-queues` plus `--recommend` |
| Package root | pass | `test_archive_inspection_rejects_extra_root_entry_even_when_manifest_matches` |
| Compact plan accepted | pass | a `P4-R1` plan validates without a regression section |
| `R5` plan blocked | pass | four independent findings against the destructive plan |

### Limitations and residual risk

- Lexical link resolution no longer follows symbolic links. The packaging
  contract already forbids them, but a project relying on them would see a
  behavior difference.
- Timing gains were measured on Windows and NTFS; the ratio should vary on other
  filesystems.
- Release assets were not built, so checksum and publication evidence remain
  outstanding for this candidate.

## Validation plan

- [x] Three structural suites.
- [x] Clean and instantiated validation.
- [x] Scale measurement before and after on corpora of 5,199 and 12,199 files.

## Rollback

Restore the published V0.15.0 asset, whose SHA-256 is recorded in
[`framework-releases/V0.15.0.md`](../../framework-releases/V0.15.0.md). No change
here touches project data, so the rollback is a tree replacement.

## Gates and approvals

- Regression gate: pass.
- Release gate: `in_preparation`; external publication is not claimed.
- Decomposition required: no.

## Related records

- Changelog/framework release: [`V0.16.0`](../../framework-releases/V0.16.0.md)
- Decision: [`ADR-0005`](../../decisions/ADR-0005-contained-release-filesystem.md)
- Policy: [`PLANNING.md`](../../PLANNING.md)

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| `test_validate_fcvw.py` | pass | 16 tests |
| `test_open_issues.py` | pass | 67 tests |
| `test_plan_dependencies_and_knowledge.py` | pass | 9 tests |
| Clean validation | pass | `errors=0 warnings=0 findings=0` |
| Scale at 12,199 files | pass | graph 11.83 s to 6.39 s; validation 35.05 s to 22.09 s |

## Gaps and residual risk

- The single representation for derived surfaces remains an open item.
- The mandatory reading route grew by roughly 7.5 percent.
