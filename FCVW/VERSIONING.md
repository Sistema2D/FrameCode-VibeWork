---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace_with_migration"
---

# Versioning and changelog namespaces

## Two independent versions

- **Application version:** owned by the application and recorded in its single runtime/manifest source.
- **Framework version:** owned by FCVW and recorded in `FRAMEWORK_LOCK.md`.

An FCVW documentation upgrade does not bump the application version unless it changes application behavior or the project's release policy explicitly says otherwise.

## Locations

- Application release: `changelogs/Vx.y.z.md`.
- Application unreleased fragment: `changelogs/unreleased/<plan-id>.md`.
- Framework release: `framework-releases/Vx.y.z.md`.
- Framework baseline in a project: `FRAMEWORK_LOCK.md`.

Never store framework release history in application `changelogs/`.

## Semantic versioning

| Change | Bump |
|---|---|
| Backward-compatible correction | patch |
| New backward-compatible capability | minor |
| Breaking schema, path, or behavior | major |

Pre-1.0 minor versions may contain breaking changes only when the framework release record and migration note make them explicit.

## Application changelog

Use schema `fcvw/changelog@1` and include:

- version, date, release type and status;
- summary and related plans;
- created, modified, and removed behavior;
- affected files/areas;
- functional, visual, technical, security, and data impact as applicable;
- validation, known gaps, and rollback;
- external publication status when relevant.

One logical change batch creates one unreleased fragment. Release assembly may combine several fragments into one version.

## Framework release

Use schema `fcvw/framework-release@1`. Record compatibility, ownership/path changes, schema changes, migrations, validation, and the clean-template asset state.

## Source of truth

Do not manually duplicate the current version across README, stack, manifest, code, and changelogs. Choose one application source and derive or link other surfaces. The framework version is always read from `FRAMEWORK_LOCK.md`.
