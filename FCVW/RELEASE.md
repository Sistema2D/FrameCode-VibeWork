---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Release and publication

## States

Application records use `unreleased` → `in_preparation` → `published`. Framework records use `in_preparation` → `ready` → `published`. Both allow `canceled` as an explicit terminal state.

Publication status for a changelog and external tag/release status are separate fields.

## Application release

1. Select completed plans and unreleased fragments.
2. Decide the semantic version.
3. Assemble `changelogs/Vx.y.z.md`.
4. Confirm version source coherence.
5. Run risk-proportional tests and governance validation.
6. Prepare backup, migration, deployment, and rollback when applicable.
7. Deploy/promote and validate the target environment.
8. Mark published only after target validation.
9. When externally published, record the deployed/tagged revision, asset/checksum state, and evidence URL.
10. Create a wiki synthesis only when the release adds reusable knowledge.

## Framework release

1. Use a framework plan and `framework-releases/Vx.y.z.md`.
2. Classify each path by ownership and upgrade action.
3. Document schema and compatibility changes in `MIGRATIONS.md`.
4. Validate both the framework source and a clean-template fixture.
5. Verify the clean artifact excludes downstream/application histories, credentials, app licenses, comparison examples, caches, and local editor state such as `.obsidian/`. Governed records of the framework's own development may remain because they carry version, migration, and regression traceability.
6. Commit the immutable content baseline and record that earlier commit in `source_revision`; this field is not the hash of the commit that contains itself.
7. Complete language reviews against that content baseline and run all release gates.
8. Mark the release and `FRAMEWORK_LOCK.md` as `ready`, commit that state, and use this second revision for the tag and exact asset input.
9. Build assets from the ready revision, generate the external checksum file, and publish the tag/assets only with explicit authority.
10. In a post-publication evidence commit, mark the release and lock `published`, store the tagged revision in `publication_revision`, and record the external URL/checksums. Checksums are not embedded before asset creation, avoiding an archive that contains its own hash.

## Required gates

- No active P1/P2 blocker relevant to the release.
- Plans and directories agree.
- Acceptance criteria and validation evidence exist.
- Links, schemas, placeholders, skills, and versions pass validation.
- Known gaps and rollback are explicit.
- Destructive or irreversible migrations have approval and rehearsal.
- External tag/release is never claimed without evidence.

## Post-release

Monitor primary workflows, security/authentication, data integrity, logs, and rollback signals. Record failures in `troubleshooting/`; do not rewrite published evidence to hide a regression.

## Language-specific GitHub release contract

Framework releases publish independent clean empty-template variants for `pt-BR`, `en-US`, `es`, and `de`. Each artifact is self-contained after extraction, excludes downstream/application-generated history, passes clean-template validation, and has an external SHA-256 entry. Governed framework history follows the same clean-baseline rule as the source.

Recommended asset names are `FrameCode-VibeWork-Vx.y.z-pt-BR.zip`, `-en-US.zip`, `-es.zip`, and `-de.zip`, plus `SHA256SUMS.txt`. GitHub-generated source archives are source snapshots and must not be described as clean templates.

The user chooses the framework language by downloading one asset. A downloaded variant contains no automatic language selector, fallback, synchronization process, or dependency on the other variants. The four-language requirement measures release completeness; it is not a runtime feature. Starting with V0.15.0, it does change the installed package boundary: the template root contains only `AGENTS.md` and `FCVW/`, while the governed source and pre-package staging remain conventional development trees.

Every V0.15.0-or-later ZIP must have one conventional archive wrapper whose first-level payload is exactly `AGENTS.md` and `FCVW/`. The packager relocates root tools, legal notices, and provider bridges under `FCVW/`, excludes repository-only root `README.md` and `.gitignore`, rejects path collisions or additional root entries, regenerates the local document graph, and preserves deterministic bytes/checksums. Removing `FCVW/` is the bounded filesystem uninstall; `AGENTS.md` requires a separate review because downstream users may customize it.

Application and framework GitHub release notes use the same sections: summary, included plans, added/changed/fixed/removed behavior, compatibility, migration, validation, known gaps, rollback, assets, checksums, and publication evidence.

Machine identifiers, schema fields, enums, paths, commands, code, API names, and checksums are not translated. Human prose is language-adapted and requires review evidence before publication.

Prepare the four complete variants under an external or disposable staging root and validate them against an authoritative clean source outside that staging root:

```powershell
python tools/locale_fcvw.py --root <release-staging-root> --require-complete --source-root <clean-source-root> --source-revision <40-character-commit>
```

The `en-US` functional manifest must exactly match that source; release-only review evidence is compared across variants but is not required in the source baseline. The authoritative validator that launches the release check validates the source and every pre-package variant; candidate copies of `tools/validate_fcvw.py` are compared for parity but are not executed before trust is established. Packaging then validates the mapped installed layout independently. Every approved `LANGUAGE_REVIEW.md` must name the same immutable revision. Each installed variant contains a regenerated local `DOCUMENT_GRAPH.md`; links cannot escape to another language variant to mask missing adapted content.

After the gate passes, create and inspect deterministic assets:

```powershell
python tools/package_release_fcvw.py --root <release-staging-root> --source-root <clean-source-root> --source-revision <40-character-commit> --version <Vx.y.z> --output <asset-directory>
```

`--allow-in-review` is permitted only for local candidate ZIPs. It tolerates exactly the `in_review` publication blocker, labels the output as a candidate, and does not authorize a tag, GitHub Release, or published release record.

Normal `validate_fcvw.py` runs do not look for language directories. Language parity is evaluated only when `locale_fcvw.py` is invoked explicitly for release preparation.

An `in_preparation` framework record may describe the contract while variants are absent, but it must list the missing assets and review evidence as blocking gaps. A `ready` record has no blocking gap and contains an immutable content baseline revision; it may be tagged and used to build assets, but it does not claim that the external GitHub Release already exists or embed checksums that do not yet exist.

## Versioning

### Two independent versions

- **Application version:** owned by the application and recorded in its single runtime/manifest source.
- **Framework version:** owned by FCVW and recorded in `FRAMEWORK_LOCK.md`.

An FCVW documentation upgrade does not bump the application version unless it changes application behavior or the project's release policy explicitly says otherwise.

### Locations

- Application release: `changelogs/Vx.y.z.md`.
- Application unreleased fragment: `changelogs/unreleased/<plan-id>.md`.
- Framework release: `framework-releases/Vx.y.z.md`.
- Framework baseline in a project: `FRAMEWORK_LOCK.md`.

Never store framework release history in application `changelogs/`.

### Semantic versioning

| Change | Bump |
|---|---|
| Backward-compatible correction | patch |
| New backward-compatible capability | minor |
| Breaking schema, path, or behavior | major |

Pre-1.0 minor versions may contain breaking changes only when the framework release record and migration note make them explicit.

### Application changelog

Use schema `fcvw/changelog@1` and include:

- version, date, release type and status;
- summary and related plans;
- created, modified, and removed behavior;
- affected files/areas;
- functional, visual, technical, security, and data impact as applicable;
- validation, known gaps, and rollback;
- external publication status when relevant.

One logical change batch creates one unreleased fragment. Release assembly may combine several fragments into one version.

### Framework release

Use schema `fcvw/framework-release@1`. Record compatibility, ownership/path changes, schema changes, migrations, validation, and the clean-template asset state.

### Source of truth

Do not manually duplicate the current version across README, stack, manifest, code, and changelogs. Choose one application source and derive or link other surfaces. The framework version is always read from `FRAMEWORK_LOCK.md`.

`FRAMEWORK_LOCK.md` identifies the installed published baseline or a fully validated `ready` candidate. Keep it on the last published version while a framework release is `in_preparation`. Advance it to `ready` only after the candidate, migration, language-specific assets, checksums, and release gates pass; change it to `published` in the post-publication evidence commit.

`source_revision` is the earlier immutable content baseline reviewed for every language variant. `publication_revision` is the later revision tagged and used to build release assets. Keeping them separate avoids an impossible requirement for a file to contain the hash of its own commit.

### Language-variant parity

All language-specific artifacts for one release share the same framework version, schema versions, functional file-role manifest, and machine contracts. A translation-only correction is a patch when it changes no normative meaning. Divergent operational meaning is a compatibility defect, not a language-specific feature.

Language publication does not migrate repository paths or add a runtime mode. Users select one monolingual variant at download time, so release compatibility is evaluated against the conventional single-tree package contract.
