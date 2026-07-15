---
schema: "fcvw/filesystem@1"
artifact_role: "generated"
owner: "framework"
upgrade_strategy: "regenerate"
last_reviewed: "2026-07-15"
---

# Filesystem contract

The physical filesystem is the source of truth. This document summarizes canonical paths and uses globs for historical record collections; it must not become a thousand-line manual mirror.

## Root

- `AGENTS.md`
- `README.md`
- `LICENSE`
- `NOTICE`
- `.gitignore`
- optional provider bridges `.cursorrules` and `.windsurfrules` (when distributed)
- `FCVW/`
- `tools/validate_fcvw.py`
- `tools/test_validate_fcvw.py`

## Canonical FCVW surfaces

- Policies and project profiles: `FCVW/*.md`
- Reusable templates: `FCVW/governance/*.md`
- Illustrative fixtures: `FCVW/examples/**/*.md`
- JIT skills: `FCVW/skills/*/SKILL.md`
- Refactoring guidance: `FCVW/refactoring-guide/*.md`
- Framework releases: `FCVW/framework-releases/*.md`
- Plans: `FCVW/Plans/{pending,in_progress,completed,discontinued}/*.md`
- Application changelogs: `FCVW/changelogs/*.md` and `unreleased/*.md`
- Decisions: `FCVW/decisions/*.md`
- Audits: `FCVW/audits/*.md`
- Troubleshooting: `FCVW/troubleshooting/*.md`
- Wiki: `FCVW/wiki/**/*.md`
- Confirmed regression knowledge: `FCVW/wiki/regressions/*.md`

## Clean-template expectations

- Record directories contain README files only, except the framework's active development records.
- No application runtime data, credentials, screenshots, application histories, or application license files occur under `FCVW/`.
- Production-derived comparison fixtures are absent from the project root and clean distribution.
- Root entries outside the documented clean-package allowlist are rejected; Git metadata and repository-owned `.github/` configuration are allowed when present.
- `FCVW/wiki/regressions/` contains only its README until a real, sourced regression is confirmed.
- Every root framework policy is cataloged in `FCVW/README.md` and discoverable from `AGENTS.md`, `CONTEXT_MAP.md`, or that index; every project profile is cataloged and every skill session type is mapped in `CONTEXT_MAP.md`.

Run the optional validator to verify the current tree instead of manually expanding every historical filename.
