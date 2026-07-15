---
schema: "fcvw/plan@2"
id: "P3-R2-2026-07-15-bilingual-readme-navigation-and-badges"
status: "in_progress"
priority: "P3"
risk: "R2"
created_at: "2026-07-15"
updated_at: "2026-07-15"
current_version: "V0.13.0"
expected_version: "V0.13.1"
owner: "framework-maintainer"
regression_contract: "required"
record_scope: "framework"
context_files:
  - "AGENTS.md"
  - "README.md"
  - "FCVW/PLANNING.md"
  - "FCVW/REGRESSION_GUARDS.md"
  - "FCVW/VERSIONING.md"
  - "FCVW/RELEASE.md"
  - "FCVW/framework-releases/V0.13.1.md"
---

# Bilingual README navigation and restored badges

## Description

Make the root README fully bilingual and navigable in Brazilian Portuguese and United States English, restore the public identity badges present before V0.13.0, and publish the documentation patch to the GitHub repository.

## Justification and objective

V0.13.0 substantially improved the Portuguese adoption guide but reduced English coverage to a short orientation and removed the Buy Me a Coffee, Apache 2.0, LinkedIn, and release badges. The README should offer equivalent discovery paths in both languages without weakening the current governance explanations.

## Scope

### Included

- Restore Buy Me a Coffee, Apache 2.0, LinkedIn, and stable-release badges with their prior destinations.
- Add explicit, stable PT-BR and ENG-US anchors and language switching.
- Provide equivalent section coverage, commands, tables, limitations, and repository navigation in both languages.
- Preserve V0.13.0 as the latest published release and prepare V0.13.1 as an unpublished documentation patch.
- Apply the same governed files locally and to `Sistema2D/FrameCode-VibeWork` through a branch and PR.

### Excluded

- Publishing V0.13.1, creating a tag, or rebuilding release assets.
- Changing framework behavior, schemas, skills, validation rules, or GitHub repository settings.
- Altering destinations or ownership of the restored public profile/support links.

## Affected files or boundaries

- Root `README.md`.
- `FCVW/FRAMEWORK_LOCK.md` and `FCVW/framework-releases/V0.13.1.md`.
- This plan and GitHub PR metadata.

## Implementation plan

1. Recover the exact badge destinations and content structure from the remote pre-V0.13 README.
2. Define explicit top, PT-BR, ENG-US, and section anchors.
3. Rewrite the README with semantically equivalent bilingual sections.
4. Register V0.13.1 as `in_preparation` without changing the published V0.13.0 release.
5. Validate Markdown links, language parity, governance, and diff hygiene.
6. Publish through an isolated branch and PR; synchronize local and remote state.

## Acceptance criteria

- [ ] Buy Me a Coffee, Apache 2.0, LinkedIn, and v0.13.0 release badges are visible and link to the intended destinations.
- [ ] The top language selector uses explicit PT-BR and ENG-US anchors.
- [ ] Each language has a local table of contents, stable section anchors, language switching, and back-to-top navigation.
- [ ] PT-BR and ENG-US cover the same major concepts, workflows, validation profiles, paths, limitations, and release state.
- [ ] All relative Markdown links resolve.
- [ ] V0.13.0 remains published and unchanged; V0.13.1 remains `in_preparation`.
- [ ] Validator tests, clean-template validation, and Git diff hygiene pass.
- [ ] Local and remote README contents match after merge.

## Regression impact

### Existing behaviors that may be affected

- README anchors and external badge destinations.
- Existing Portuguese navigation and adoption instructions.
- Accurate representation of stable versus in-preparation framework versions.
- Markdown rendering on GitHub and portable readers.

### Regression contracts consulted

- `REGRESSION_GUARDS.md` for documentation and interface preservation.
- `VERSIONING.md` and `RELEASE.md` for published versus in-preparation state.
- Pre-V0.13 remote README for badge destinations.
- Current V0.13 README for the richer canonical content that must be preserved.

### Regression checks required

- [ ] Check all local README paths through the validator.
- [ ] Compare PT-BR and ENG-US section inventories.
- [ ] Verify four badge destinations and explicit language anchors.
- [ ] Confirm stable release remains v0.13.0 and no release/tag is created.
- [ ] Confirm GitHub main matches the validated local README after merge.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Original badge recovery | pass | remote commit `a915dc8`: support, license, LinkedIn, and release destinations |
| Current rich content baseline | pass | published V0.13.0 local and remote README |
| Language parity | pending | final heading/section inventory |
| Markdown navigation | pending | validator and explicit-anchor scan |
| Local/remote parity | pending | post-merge blob/hash comparison |

### Limitations and residual risk

- GitHub and other Markdown renderers may style badges or Mermaid diagrams differently; explicit HTML anchors preserve navigation independently of automatic heading slugs.
- V0.13.1 is only prepared by this change and must not be described as published.

## Validation plan

- `python -B tools/test_validate_fcvw.py`.
- `python -B tools/validate_fcvw.py --root . --profile clean-template`.
- Explicit PT/EN anchor and section parity inventory.
- Badge destination check.
- `git diff --check` and remote README blob comparison.

## Rollback

Restore the published V0.13.0 README from tag `v0.13.0`, remove the unpublished V0.13.1 record, and revert the framework lock through a new commit. Do not rewrite the v0.13.0 tag or release.

## Gates and approvals

- User authorization: explicit request to change the README locally and remotely.
- Regression gate: required.
- Release gate: no new release publication; V0.13.1 remains in preparation.
- PR gate: publish through a scoped branch and merge after validation.

## Related records

- Published baseline: `FCVW/framework-releases/V0.13.0.md`.
- Documentation patch: `FCVW/framework-releases/V0.13.1.md`.

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Remote orientation | pass | latest release v0.13.0; main available; no open PRs |
| Historical README inspection | pass | four original badge destinations recovered from `a915dc8` |

## Gaps and residual risk

- Implementation and publication are in progress.
