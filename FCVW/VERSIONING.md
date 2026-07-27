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

`FRAMEWORK_LOCK.md` identifies the installed published baseline or a fully validated `ready` candidate. Keep it on the last published version while a framework release is `in_preparation`. Advance it to `ready` only after the candidate, migration, language-specific assets, checksums, and release gates pass; change it to `published` in the post-publication evidence commit.

`source_revision` is the earlier immutable content baseline reviewed for every language variant. `publication_revision` is the later revision tagged and used to build release assets. Keeping them separate avoids an impossible requirement for a file to contain the hash of its own commit.

## Language-variant parity

All language-specific artifacts for one release share the same framework version, schema versions, functional file-role manifest, and machine contracts. A translation-only correction is a patch when it changes no normative meaning. Divergent operational meaning is a compatibility defect, not a language-specific feature.

Language publication does not migrate repository paths or add a runtime mode. Users select one monolingual variant at download time, so release compatibility is evaluated against the conventional single-tree package contract.
