# Versioning and Changelogs

This document defines the versioning, release, and changelog rules of the application.

The goal is to ensure traceability between plans, applied changes, modified files, justifications, executed validations, and published versions.

## Base Version and Current Version

The formal base version of the documented versioning process is:

```text
V0.0.0
```

The current version of the application must be consulted jointly in:

- application source code (constant or version file);
- `STACK.md`, `Current version` field;
- `MANIFEST.md`, `Current version` field;
- corresponding `changelogs/Vx.y.z.md`.

As long as the version is not centralized in a single release file, the version references in code and documentation must remain coherent with each other.

## Relationship with Release

`RELEASE.md` describes the operational workflow to prepare, validate, and publish a release. This `VERSIONING.md` is the normative source for version, increment, changelog status, and publication criteria.

The changelog in `changelogs/Vx.y.z.md` is the formal source of the published version or the version in preparation. Syntheses in `wiki/releases/` may record reusable learnings, but do not replace the changelog.

## Version Format

```text
Vx.y.z
```

Where:

- `x`: major version;
- `y`: minor version;
- `z`: patch version.

## Increment Criteria

### Major Version (`x`)

Increment when the change:

- modifies core architecture;
- alters main API contracts;
- requires relevant structural migration;
- breaks backward compatibility with old persisted data;
- alters the main workflow in a way incompatible with previous versions;
- introduces a broad product or distribution change.

### Minor Version (`y`)

Increment when the change:

- adds relevant functionality;
- creates a new screen, module, or usage flow;
- expands capabilities without breaking compatibility;
- adds significant integration or functional improvement.

### Patch Version (`z`)

Increment when the change:

- fixes a bug;
- adjusts existing behavior without changing the contract;
- improves documentation;
- updates process, planning, troubleshooting, or design;
- fixes a localized visual issue;
- applies a small refactoring with no relevant functional impact.

## Mandatory Changelog Rule

Every functional, visual, structural, documental, build, process, or versioned data change must have a corresponding Markdown file in `changelogs/`.

The file must be created or updated before closing the plan.

No version should be considered completed without a corresponding changelog.

## Naming Pattern

```text
changelogs/Vx.y.z.md
```

The filename must correspond exactly to the version recorded in the changelog content.

## Mandatory Changelog Structure

```markdown
# Changelog Vx.y.z

## Version

`Vx.y.z`

## Date

YYYY-MM-DD

## Release Status

`in_preparation`

## Release Type

`major` / `minor` / `patch`

## Summary

-

## Related Plans

-

## Items Created

-

## Items Modified

-

## Items Removed

-

## Justifications

-

## Affected Files

-

## Functional Impact

-

## Visual Impact

-

## Technical Impact

-

## Evaluated Risks and Regressions

-

## Validation Executed

-

## Known Gaps

-

## Rollback Observations

-
```

## Allowed Statuses for Release

- `in_preparation`: release in assembly, still subject to changes.
- `in_validation`: changes completed, validation in progress.
- `published`: release completed and recorded as official version.
- `canceled`: release planned, but not published.

## Release Types

- `major`: increment of `x`.
- `minor`: increment of `y`.
- `patch`: increment of `z`.

## Relationship with Plans

Each relevant changelog item must point to one or more plans in `Plans/`.

- Completed plans must be cited by filename.
- In-progress plans must not be treated as completed.
- Discontinued plans only enter the changelog if they affected decisions, files, or scope.

## Criteria to Publish a Version

A version can only be marked as `published` when:

- all included plans are in `Plans/completed/`;
- the changelog exists and lists created, modified, and removed items;
- the validation defined in the plans has been executed or the limitation is documented;
- version references in code, documentation, and build are coherent;
- known gaps are recorded;
- there is no temporary file used as a source of truth.

## Rollback

When a release alters code, persisted data, build, migration, or API contracts, the changelog must indicate the rollback procedure or justify why rollback does not apply.

## Minimum Audit Before Closing a Release

- Does the `changelogs/Vx.y.z.md` file exist?
- Does the filename correspond to the **Version** field?
- Do all cited plans exist and reside in `Plans/completed/`?
- Were created, modified, and removed files listed?
- Were justifications and validations recorded?
- Are known gaps explicit?
