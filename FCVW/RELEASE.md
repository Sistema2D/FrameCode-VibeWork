---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Release and publication

## States

`unreleased` → `in_preparation` → `published`, with `canceled` as an explicit terminal state.

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
9. Create a wiki synthesis only when the release adds reusable knowledge.

## Framework release

1. Use a framework plan and `framework-releases/Vx.y.z.md`.
2. Classify each path by ownership and upgrade action.
3. Document schema and compatibility changes in `MIGRATIONS.md`.
4. Validate both the framework source and a clean-template fixture.
5. Verify the clean artifact excludes project histories, credentials, app licenses, and comparison examples.
6. Record asset checksum and publication evidence.
7. Update `FRAMEWORK_LOCK.md` only when the release is ready.

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
