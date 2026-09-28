# Template: application release

```markdown
---
schema: "fcvw/changelog@1"
version: "Vx.y.z"
artifact_role: "record"
owner: "project"
upgrade_strategy: "preserve"
record_scope: "application"
date: "YYYY-MM-DD"
release_status: "unreleased | in_preparation | published | canceled"
release_type: "patch | minor | major"
external_publication: "not_applicable | pending | published"
source_revision: "<40-character-content-baseline-revision-or-not_applicable>"
publication_revision: "<40-character-deployed-or-tagged-revision-or-UNPUBLISHED>"
release_languages:
  - "en-US"
  - "<additional-reviewed-locale>"
related_plans:
  - "P3-R2-YYYY-MM-DD-short-description"
---

# Application release Vx.y.z

## Summary
## Related plans

- [Change plan](<relative-path-to-plan.md>)

## Added
## Changed
## Fixed
## Removed
## Security and data impact
## Validation
## Known gaps
## Migration
## Rollback
## Assets and package contents
## Checksums
## Publication evidence
## Post-release validation
```

## Minimal unreleased fragment

The smallest valid fragment under `FCVW/changelogs/unreleased/` (the directory is created by the first fragment):

```markdown
---
schema: "fcvw/changelog@1"
version: "Vx.y.z"
date: "YYYY-MM-DD"
release_status: "unreleased"
release_type: "patch"
related_plans:
  - "P3-R1-YYYY-MM-DD-short-slug"
---

# Application Vx.y.z

## Summary

<User-visible outcome.>

## Affected areas

- `<path or module>` — <change>.

## Validation

- `<command>` — <observed result>.

## Known gaps

<None, or explicit gap.>

## Rollback

<Safe reversal procedure.>
```
