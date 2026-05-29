# Release and Publication

Operational document to prepare, validate, and publish versions of the application.

This file complements `VERSIONING.md`. While `VERSIONING.md` defines versioning and changelog rules, this document describes the practical workflow of preparing a release.

The changelog in `changelogs/Vx.y.z.md` is the formal source of the release. This document does not create a parallel version source.

## Objective

Standardize the closure of versions, preventing publication with incomplete plans, inconsistent versions, incomplete changelogs, missing tests, or unknown gaps.

## States of a Release

- `planned`: expected version, with no completed changes yet.
- `in_preparation`: changes being grouped and documented.
- `in_validation`: implementation completed, tests in progress.
- `published`: finalized version.
- `canceled`: planned version that will not be published.

## Recommended Workflow

1. Identify plans that compose the release.
2. Confirm expected version.
3. Ensure each plan has the correct status.
4. Update the version's changelog.
5. Execute tests as per `TESTS.md`.
6. Execute audit as per `AUDIT.md`.
7. Confirm version coherence in code, `STACK.md`, and changelog.
8. Record known gaps.
9. Record rollback procedures when applicable.
10. Mark changelog as `published`.
11. Evaluate if the release generated reusable learning for `wiki/releases/`.

## Minimum Criteria to Publish

- All included plans are completed or explicitly removed from the release.
- Changelog exists and is complete.
- Version displayed in the application is coherent.
- Version in `STACK.md` is coherent.
- Minimum tests were executed.
- Known gaps were recorded.
- Residual risks were recorded.
- Rollback was described or justified as not applicable.

## Pre-Release Checklist

- [ ] The expected version follows `Vx.y.z`.
- [ ] The type of release was defined.
- [ ] Related plans were listed.
- [ ] Changelog was created.
- [ ] Affected files were listed.
- [ ] Tests were defined.
- [ ] Validation was executed or limitation was recorded.
- [ ] Known gaps were recorded.
- [ ] Rollback was recorded when applicable.
- [ ] Document audit was executed.

## Publication Checklist

- [ ] Final build executed.
- [ ] Application starts.
- [ ] Main workflow works.
- [ ] Displayed version matches.
- [ ] Changelog is set to `published`.
- [ ] Plans are in `Plans/completed`.
- [ ] There are no temporary files as source of truth.
- [ ] Build artifacts were not improperly versioned.

## Framework Documentation Publication

The framework documentation site artifact lives in `FCVW/docs/`.

Rules:

- Do not keep a permanent root `docs/` directory in the framework baseline.
- If a host requires root `docs/` for publication, generate or export it as a release/deployment artifact from `FCVW/docs/`.
- Do not treat the generated root export as the source of truth.
- After publication, verify that `FCVW/docs/index.html` remains the canonical maintained file and that generated deployment artifacts are not confused with application-owned root files.

## Post-Release Checklist

- [ ] Next gaps were registered in future plans, if applicable.
- [ ] Recurring issues were reviewed.
- [ ] Official documents remain coherent.
- [ ] Residual risks were communicated.
- [ ] Following version was not started without a plan.

---

## Models and Templates

To create release notes or executive summaries, use the template in:
`governance/TEMPLATE_RELEASE.md`
