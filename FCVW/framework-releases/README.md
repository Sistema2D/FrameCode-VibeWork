---
schema: "fcvw/framework-release-index@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Framework releases

This directory is the changelog namespace for FCVW itself. Application releases belong in `FCVW/changelogs/`.

## Release records

- [V0.13.0](V0.13.0.md)
- [V0.13.1](V0.13.1.md)
- [V0.14.0](V0.14.0.md)

Each `Vx.y.z.md` record must identify compatibility, migration, changed framework surfaces, validation, publication state, known gaps, and rollback. A release marked `in_preparation` is not a published artifact.
