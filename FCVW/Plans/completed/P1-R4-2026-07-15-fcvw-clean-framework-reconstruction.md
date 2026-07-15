---
schema: "fcvw/plan@1"
id: "P1-R4-2026-07-15-fcvw-clean-framework-reconstruction"
status: "completed"
priority: "P1"
risk: "R4"
created_at: "2026-07-15"
updated_at: "2026-07-15"
current_version: "V0.12.0"
expected_version: "V0.13.0"
owner: "framework-maintainer"
record_scope: "framework"
context_files:
  - "AGENTS.md"
  - "FCVW/CONTEXT_MAP.md"
  - "FCVW/PLANNING.md"
  - "FCVW/INSTANTIATION.md"
  - "FCVW/skills/self-improvement/SKILL.md"
---

# Reconstruct the clean FCVW framework

## Description

Restore the main `FCVW/` directory as a clean, reusable framework; recover proven generic contracts from the real-application example; remove application-owned history from the clean baseline; and add schemas, ownership, upgrade, validation, memory, automation, and release rules.

## Objective

Deliver a coherent `V0.13.0` clean framework whose documentation is operational rather than placeholder-only, while keeping `FCVW - Exemplo retirado de aplicação real/` unchanged as comparison evidence.

## Scope

### Included

- Clean-baseline recovery and removal of copied application records from `FCVW/`.
- Framework/application ownership boundaries and selective-upgrade policy.
- Operational core documents, templates, skills, wiki lifecycle, and declarative automation contracts.
- Canonical artifact schemas and optional zero-dependency validation.
- Framework/application version namespace separation.
- Version, changelog, filesystem, and release-preparation synchronization.

### Excluded

- Changes inside the real-application example.
- Publishing a Git tag, GitHub Release, or remote changes.
- Normalizing the application example's historical records.

## Affected files

- Root framework entrypoints and license metadata.
- `FCVW/*.md` canonical documents.
- `FCVW/governance/`, `FCVW/skills/`, `FCVW/refactoring-guide/`, and `FCVW/wiki/`.
- Clean record directories under `FCVW/`.
- Optional validator under `tools/`.

## Implementation plan

1. Inventory and remove copied application-owned records from the clean `FCVW/` tree.
2. Rebuild generic framework-owned documents from proven example content without application-owned data.
3. Add ownership, lock, schema-version, migration, memory-retention, and version-namespace rules.
4. Normalize templates and skills; add optional portable validation.
5. Validate structure, links, schemas, placeholders, state coherence, and version surfaces.
6. Record `V0.13.0`, finish this plan, and keep publication status explicit.

## Acceptance criteria

- [x] The example directory is unchanged.
- [x] No application plans, changelogs, troubleshooting records, sessions, or app-specific binary/license artifacts remain in the clean baseline.
- [x] Core documents contain actionable rules, not one-line placeholders.
- [x] Plan, changelog, wiki, ADR, troubleshooting, automation, and skill contracts are versioned and internally coherent.
- [x] Framework and application versions have separate namespaces.
- [x] Skills use one portable metadata schema and avoid vendor-specific core commands.
- [x] Memory is archived, not destructively purged.
- [x] Optional validation passes on the clean baseline.
- [x] `FILESYSTEM.md`, version surfaces, changelog, and release status are synchronized.

## Validation plan

- Run the optional FCVW validator in strict clean-template mode.
- Scan for application-specific identifiers and copied historical records.
- Check Markdown links, code-fence balance, plan state, skill metadata, version coherence, and placeholder policy.
- Compare hashes under the example directory before and after implementation.
- Run `git diff --check` if a valid Git worktree becomes available; otherwise record the limitation.

## Rollback notes

Restore the `FCVW/` directory from the pre-change clean `V0.12.0` snapshot and leave the example directory untouched. Because the current `.git` marker is not a valid repository, rollback must use a verified backup or release artifact rather than Git commands.

## Skill/Agent Self-Improvement Gate

- Skill loaded: `skills/self-improvement/SKILL.md`
- Asset changed: all existing FCVW skills and their catalog.
- Evidence: clean skills are identical placeholders; the real application shows inconsistent metadata, vendor-specific commands, and unenforced exit criteria.
- Metric passed: rule drift and validation gap.
- Scope preserved: each skill retains its named responsibility; shared metadata and exit rules are standardized.
- Token/risk ROI: JIT skills replace repeated loading of large base documents and reduce ambiguous activation.
- Validation replay: catalog/schema validator plus representative trigger and output checks.
- Decision: `patch`

## Completion evidence

- Removed 956 application-owned files that had been copied into the clean framework baseline; retained only framework policies, templates, clean directory markers, and framework-scoped records.
- Added ownership, lock, schemas, migration, memory, clean-example, and separate framework-release surfaces.
- Rebuilt operational policies and restored substantive reusable templates and refactoring guidance from the comparison example without importing its application history.
- Normalized 21 skills to `fcvw/skill@1`; rewrote unsafe or vendor-bound debugging, linting, TDD, memory rotation, compaction, release, instantiation, and validation contracts.
- `python -m py_compile tools/validate_fcvw.py`: passed.
- `python tools/validate_fcvw.py --root . --profile clean-template`: passed with 0 errors and 0 findings.
- Clean `FCVW/`: 171 Markdown files, 0 application changelogs, and 0 application wiki records.
- Comparison example: 1,099 files and aggregate SHA-256 `0E06BEB4FDA4B54B0352965A703B1D85D9C0649CB7CD27AA4FE599A05E9C7FEC`, equal to the pre-change snapshot.
- Git validation unavailable: the workspace has no valid Git worktree; no commit, tag, push, or release publication was attempted.

## Status

`completed`
