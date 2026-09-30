---
schema: "fcvw/plan@2"
id: "P3-R2-2026-09-30-simplify-root-readme"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P3"
risk: "R2"
created_at: "2026-09-30"
updated_at: "2026-09-30"
current_version: "V0.20.0"
expected_version: "V0.20.1"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "AGENTS.md"
  - "README.md"
  - "FCVW/PLANNING.md"
  - "FCVW/REGRESSION_GUARDS.md"
  - "FCVW/RELEASE.md"
  - "FCVW/framework-releases/V0.20.1.md"
---

# Simplify the root README

## Description

Rewrite the root README shown on GitHub so it is shorter, simpler and more direct, keeping the header and the PT-BR and ENG-US versions.

## Justification and objective

The README duplicated detail that already lives in canonical policies (ownership roles, change flow, routing, repository map, release layout). A first-time visitor needs what FCVW is, what it solves, how to start and where to read more.

## Scope

### Included

- Keep the header unchanged: title, tagline, four badges, stable release line and PT-BR/ENG-US selector.
- Replace each language section with: summary, problems solved, three-step usage, optional validation commands, links to canonical documents and the non-goal statement.
- Keep explicit `top`, `pt-br` and `en-us` anchors and language switching.
- Record an unpublished V0.20.1 documentation candidate.

### Excluded

- Changes to policies, tools, templates, skills, schemas or `FRAMEWORK_LOCK.md`.
- Tagging, publishing or building release assets.

## Affected files or boundaries

- `README.md`.
- `FCVW/framework-releases/V0.20.1.md`.
- This plan.

## Implementation plan

1. Keep the header block byte-identical.
2. Rewrite both language sections with equivalent content.
3. Add the V0.20.1 `in_preparation` record; keep the lock on published V0.20.0.
4. Validate links, anchors, version surface and governance.

## Acceptance criteria

- [x] Header block identical to V0.20.0.
- [x] PT-BR and ENG-US sections are equivalent and each is linked from the selector.
- [x] README is substantially shorter (249 → 99 lines).
- [x] All relative links and fragments resolve; README still references V0.20.0.
- [x] Clean-template validation and tool tests pass.

## Regression impact

### Existing behaviors that may be affected

- `#top`, `#pt-br` and `#en-us` anchors used by the header and external links.
- Removed sub-anchors (`#pt-visao-geral`, `#en-overview`, etc.) that external pages might link to.
- Framework version surface checked by `validate_fcvw.py` (README must reference the installed version).
- Discoverability of canonical policies from the root README.

### Regression contracts consulted

- `REGRESSION_GUARDS.md` for documentation and public interface preservation.
- `RELEASE.md` for the `in_preparation` state and the lock rule.
- `AGENTS.md` link-reachability rule: policies remain reachable through `AGENTS.md` and `FCVW/README.md`, both linked from the README.

### Regression checks required

- [x] Header diff against V0.20.0.
- [x] Anchor and fragment resolution.
- [x] Clean-template validation (links, version, graph reachability).
- [x] Tool test suite.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Header preserved | pass | lines 1–21 identical to `git show HEAD:README.md` |
| Anchors | pass | `top`, `pt-br`, `en-us` defined; all internal fragments resolve |
| Governance | pass | `validate_fcvw.py --profile clean-template`: see Validation executed |
| Tool tests | pass | `check_fcvw.py`: see Validation executed |

### Limitations and residual risk

- Sub-section anchors of the old README no longer exist; external deep links fall back to the top of the page. Section content remains available in the linked canonical documents.

## Validation plan

- `python -B tools/validate_fcvw.py --root . --profile clean-template`.
- `python -B tools/check_fcvw.py`.
- Anchor/fragment inventory and `git diff --check`.

## Rollback

Restore `README.md` from tag `v0.20.0` and mark V0.20.1 as `canceled` through a new commit.

## Gates and approvals

- User authorization: explicit request to simplify the README.
- Regression gate: required.
- Release gate: none; V0.20.1 remains `in_preparation`.

## Related records

- Framework release: [V0.20.1](../../framework-releases/V0.20.1.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Clean-template validation | pass | 0 errors, 0 findings |
| Tool suite | pass | `check_fcvw.py` exit 0 |
| Anchors and fragments | pass | 3 anchors, all fragments resolve |
| Diff hygiene | pass | `git diff --check` clean |

## Gaps and residual risk

- V0.20.1 is not published; no tag or asset exists.

## Status

`completed`
