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
- `in_staging`: staged for pre-production validation (see `ENVIRONMENT.md §5`).
- `in_production`: deployed to production environment.
- `published`: finalized version and changelog released.
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

## External Documentation Publication

The framework baseline does not maintain a physical documentation site artifact.

Rules:

- Do not keep a permanent root `docs/` directory in the framework baseline.
- Do not keep a permanent `FCVW/docs/` directory in the framework baseline.
- Do not keep root Node/Jest package files only to test a removed documentation site.
- If GitHub Pages or another host is needed, publish the public page from another repository or from a deployment pipeline outside this framework baseline.
- Treat generated publication output as external release infrastructure, not as a canonical FCVW source.

## Deployment and Environment Promotion

A release is not complete until the changes are deployed and validated in the target environments. This section connects the release workflow to the environment promotion gates defined in `ENVIRONMENT.md §5`.

### Promotion Workflow

```text
Release prepared  →  Deploy to Staging  →  Validate  →  Deploy to Production  →  Changelog published
```

1. **Prepare release**: Execute the standard release workflow (plans completed, changelog assembled, audit passed).
2. **Deploy to Staging**: Deploy the release candidate to the staging environment per `ENVIRONMENT.md §5 — Promotion Gate: Development → Staging`.
3. **Validate in Staging**: Run integration tests, verify critical workflows, confirm no regressions. Record results.
4. **Obtain approval**: Human approval for production deployment, especially for R4+ changes.
5. **Deploy to Production**: Promote the release to the production environment per `ENVIRONMENT.md §5 — Promotion Gate: Staging → Production`.
6. **Verify in Production**: Confirm the application starts, main workflows function, and no critical errors appear.
7. **Publish changelog**: Set the changelog status to `published` after successful production deployment.

### Deploy Rollback

If a deployment to any environment causes critical failures:

1. **Revert immediately**: Restore the previous stable version in the affected environment.
2. **Record**: Create a troubleshooting record in `troubleshooting/` with symptoms, impact, and rollback actions taken.
3. **Assess**: Determine if the fix requires a patch release or can be included in the next planned release.
4. **Plan fix**: Create a plan to correct the issue. If the fix is urgent, classify as P1.
5. **Re-deploy**: After the fix is validated, repeat the promotion workflow from Staging.

The rollback procedure must be documented in the release plan before any R4+ deployment.

### Environments Without Physical Separation

Projects that do not maintain separate staging and production environments (e.g., solo developer deploying directly) should treat the promotion gates as sequential validation checkpoints:

1. **Development validation** = build + test + code review (same as before)
2. **Staging validation** = run the full release checklist and audit in a separate workspace or branch before deploying
3. **Production deployment** = deploy only after both validation stages pass

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
