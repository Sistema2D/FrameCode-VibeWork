---
schema: "fcvw/plan@2"
id: "P2-R3-2026-07-15-v0130-github-publication"
status: "in_progress"
priority: "P2"
risk: "R3"
created_at: "2026-07-15"
updated_at: "2026-07-15"
current_version: "V0.12.0"
expected_version: "V0.13.0"
owner: "framework-maintainer"
regression_contract: "required"
record_scope: "framework"
context_files:
  - "AGENTS.md"
  - "FCVW/FRAMEWORK_LOCK.md"
  - "FCVW/MIGRATIONS.md"
  - "FCVW/OWNERSHIP.md"
  - "FCVW/RELEASE.md"
  - "FCVW/VERSIONING.md"
  - "FCVW/framework-releases/V0.13.0.md"
  - "FCVW/skills/release-checklist/SKILL.md"
---

# Publish FCVW V0.13.0 to GitHub

## Description

Apply the validated clean V0.13.0 framework baseline to `Sistema2D/FrameCode-VibeWork`, integrate it through a reviewed branch, and publish a GitHub tag and release with a clean template asset and SHA-256 evidence.

## Justification and objective

The remote default branch is at V0.12.0 while the locally validated framework contains the governed V0.13.0 reconstruction, regression guardrails, selective reading routes, richer README, migration contracts, and optional deterministic validator. Publication makes that coherent baseline available without carrying production-derived or legacy application-style records into the clean distribution.

## Scope

### Included

- Start from a clean clone of remote `main` at `a915dc8`.
- Replace framework-owned/template surfaces with the validated V0.13.0 baseline.
- Preserve `.github/` and Git history; remove only legacy working-tree records excluded by the clean-template contract.
- Validate tests, Markdown, clean boundaries, version namespace, and Git diff hygiene.
- Push a scoped branch, open and merge a PR, then publish tag/release `v0.13.0`.
- Attach a clean template ZIP and SHA-256 checksum file.

### Excluded

- Force-pushing `main` or rewriting Git history.
- Changing repository settings, branch protection, issues, or unrelated metadata.
- Publishing any application release or changing downstream application versions.
- Adding executable CI/provider automation beyond the optional standard-library validator.

## Affected files or boundaries

- Root framework entrypoints and optional provider bridges.
- `FCVW/` clean framework distribution, framework release namespace, and framework lock.
- `tools/validate_fcvw.py` and its regression suite.
- GitHub branch, PR, tag, release, ZIP asset, and checksum attachment.

## Implementation plan

1. Inspect live GitHub state, authentication, open PRs, latest tag/release, and clean default branch.
2. Import the already validated V0.13.0 clean baseline while preserving GitHub-owned infrastructure.
3. Validate structural integrity and review the complete deletion/addition boundary.
4. Synchronize release state, README, framework lock, and this publication record.
5. Commit and push an isolated branch; open and merge the PR after validation.
6. Build the clean artifact from the merged commit, compute SHA-256, publish `v0.13.0`, and verify remote evidence.

## Acceptance criteria

- [ ] Remote changes are based on current `origin/main`, not a stale local checkout.
- [ ] `.github/` and Git history remain untouched.
- [ ] V0.13.0 source contains no comparison fixture, application history, production data, or unexpected root entry.
- [ ] Validator tests and `clean-template` profile pass.
- [ ] Diff hygiene and version/release surfaces pass.
- [ ] PR is merged into `main` without force push.
- [ ] Tag and GitHub Release `v0.13.0` point to the merged release commit.
- [ ] Clean ZIP and `.sha256` assets are published and remotely verified.

## Regression impact

### Existing behaviors that may be affected

- Existing V0.12.0 consumers and migration path.
- GitHub source navigation and release download workflow.
- Historical framework-development records formerly stored in application namespaces.
- Provider bridge discovery and Scenario 1 Markdown-only automation behavior.

### Regression contracts consulted

- `OWNERSHIP.md` and `MIGRATIONS.md` for selective upgrade and legacy preservation.
- `REGRESSION_GUARDS.md` and `TESTS.md` for R3 evidence.
- `VERSIONING.md`, `RELEASE.md`, and `release-checklist` for namespace and publication.
- Remote `AGENTS.md` for branch/PR and record requirements before replacement.

### Regression checks required

- [ ] Compare imported baseline with the remote working tree and preserve `.github/`.
- [ ] Run all validator regression fixtures and the clean-template profile.
- [ ] Confirm Git history retains removed records and no working-tree application contamination remains.
- [ ] Validate clean artifact contents independently before upload.
- [ ] Verify release tag, merge commit, asset size, and SHA-256 after publication.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Remote baseline | pass | clean clone of `origin/main` at `a915dc8`; latest release `v0.12.0`; no open PRs |
| Imported framework | pass | 14 tests and clean-template validation: 0 errors, 0 findings |
| Git infrastructure preservation | pass | `.git/` and `.github/` excluded from replacement scope |
| Historical preservation | pass | removed working-tree records remain recoverable through Git history and published earlier tags |
| Publication transaction | in_progress | branch, PR, merge, tag, and release evidence to be verified before closeout |

### Limitations and residual risk

- The V0.13.0 migration is intentionally large because it removes legacy project history from the distributable baseline; downstream adopters must follow `MIGRATIONS.md` and preserve their project-owned records.
- GitHub publication is an external transaction. If merge, tag, or release creation fails, keep the release `in_preparation`, do not claim publication, and resume from the verified remote state.

## Validation plan

- `python -B tools/test_validate_fcvw.py`.
- `python -B tools/validate_fcvw.py --root . --profile clean-template`.
- `git diff --check`, scoped status/stat, and remote branch comparison.
- Independent validation inside the staged clean artifact.
- `gh pr checks`, merged-commit verification, and `gh release view` asset verification.

## Rollback

Before merge, close the PR and delete only the release branch. After merge but before release, revert the merge with a new commit. After publication, retain immutable evidence and publish a corrective patch release rather than rewriting `main` or an already consumed tag.

## Gates and approvals

- User publication authority: explicit request to apply to `Sistema2D/FrameCode-VibeWork` and publish a new release.
- Regression gate: required.
- Release gate: required.
- PR gate: required by the remote R3 workflow; owner-authorized merge after checks.
- External side effects: branch push, PR, merge, tag, release, and asset upload are in scope.

## Related records

- Framework release: `FCVW/framework-releases/V0.13.0.md`.
- Source plans: `P1-R4-2026-07-15-fcvw-clean-framework-reconstruction`, `P2-R4-2026-07-15-regression-guardrails-and-fixture-removal`, and `P2-R3-2026-07-15-final-integrity-reading-routes-and-readme`.

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| GitHub orientation | pass | authenticated as `Sistema2D`; public non-archived repo; default `main` |
| Remote release/PR state | pass | latest `v0.12.0`; no open PRs |
| Pre-publication imported baseline | pass | 14 tests; clean-template 0 errors and 0 findings |

## Gaps and residual risk

- External publication transaction remains in progress.
