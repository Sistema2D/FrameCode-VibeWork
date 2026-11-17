---
schema: "fcvw/plan@2"
id: "P3-R2-2026-11-17-local-root-entries"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P3"
risk: "R2"
created_at: "2026-11-17"
updated_at: "2026-11-17"
current_version: "V0.23.0"
expected_version: "V0.24.0"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "FCVW/OWNERSHIP.md"
  - "tools/path_policy_fcvw.py"
  - "tools/validate_fcvw.py"
  - "tools/release_layout_fcvw.py"
category: "correction"
depends_on: []
---

# Ignored root entries are local state

## Description

The maintainer classified a product under development inside the source checkout as a separate, parallel project and asked for V0.24.0 to be published without mentions of other projects or sensitive data. The inventory, the validator and the packager named that product's folder. Replace the special case with a general rule: a root entry that the checkout's git ignores is local state. Records of the framework's own development refer to the downstream application only as "the field project".

## Justification and objective

A framework release must not depend on, or advertise, a project that is not part of it. A hard-coded folder name also failed for any other local folder a maintainer keeps beside the source. Git ignore rules already decide what the governed inventory contains, so the clean-root check now follows the same rule.

## Scope

### Included

- `path_policy_fcvw.py`: `git_ignored_root_entries`; the product folder leaves `CLEAN_ROOT_ENTRIES` and the transient rule.
- `validate_fcvw.py`: the clean-root check skips ignored entries.
- `release_layout_fcvw.py`: no product exception in the installed-path mapping.
- `verify_release_fcvw.py`: the source smoke skips ignored root entries.
- `OWNERSHIP.md` source-root and clean-template rows; `InventoryTests`.
- Release record, backlog section 15 and two completed plans without project names.

### Excluded

- The parallel project itself and its records, which stay outside the published tree.

## Affected files or boundaries

The files above and `FCVW/framework-releases/V0.24.0.md`, `TODO.md`.

## Implementation plan

1. Ask git which root entries it ignores (`check-ignore --stdin`), only when the root is a work tree's top level.
2. Use that set in the clean-root check; remove the folder-specific code and its test.
3. Remove project names from the publishable records.

## Proportionality gate

- Real problem and root cause: a product-specific exception in framework code.
- Necessary in current scope: requested by the maintainer for this release.
- Existing codebase solution checked: reuses the work-tree test of the git-aware inventory.
- Native platform capability checked: `git check-ignore`.
- Installed dependency checked: none.
- New code or complexity justified: about 25 lines, replacing the special case.
- Minimum non-trivial behavior tests: the same folder is contamination before it is ignored and local state after.
- Deliberate simplification and limitations: outside a git work tree (release variants, extracted assets) every unexpected root entry is still rejected.
- Condition for future evolution: none.
- Mandatory safeguards preserved: forbidden fixtures are rejected even when ignored; packaging still reads only a clean export.

## Acceptance criteria

- [x] No framework file names the parallel project or the field project.
- [x] An ignored root entry is neither contamination nor governed Markdown; the same entry not ignored is contamination.
- [x] Release variants and installed payloads keep the strict root check.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

- Clean-template validation of the source checkout and of release variants.
- Release packaging (installed-path mapping).

### Regression contracts consulted

- `FCVW/OWNERSHIP.md` — filesystem layout and clean template.
- `FCVW/RELEASE.md` — assets are built from a clean export.

### Regression checks required

- [x] Inventory, clean-template and packaging tests; full runner.
- [x] Source validation with the local folders present and ignored.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Inventory and clean root | pass | `test_a_git_ignored_root_entry_is_local_state`; `InventoryTests`: 5 tests OK |
| Source validation | pass | `validate_fcvw.py --root .` with two ignored local folders at the root: no `clean-contamination` |
| Full runner | pass | see Validation executed |
| Name search | pass | no project name in tracked or publishable files |

### Limitations and residual risk

- A maintainer who ignores a folder accepts that it is invisible to governance in that checkout.

## Validation plan

- [x] `python -B tools/check_fcvw.py --root .` on two interpreters.

## Rollback

Revert the commit.

## Gates and approvals

- Maintainer request (2026-11-17): disregard the parallel project and publish the version clean of mentions of other projects and of sensitive data.

## Related records

- Framework release: [V0.24.0](../../framework-releases/V0.24.0.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Runner | pass | `check_fcvw.py --root .` on Python 3.11.15, 3.12.10 and 3.14.2: 374 tests (2 skipped), governance, benchmark and installed smoke; source unchanged |
| Failure found: the installed smoke copied the ignored local folders into the payload (277 findings) | fixed | `smoke_source` skips ignored root entries; installed smoke passes |
| Failure found: the new `OWNERSHIP.md` sentence put the surface 57 bytes over budget | fixed | sentence shortened; `test_framework_surface_stays_within_budget` passes |

## Gaps and residual risk

None beyond the limitation above.

## Status

`completed`
