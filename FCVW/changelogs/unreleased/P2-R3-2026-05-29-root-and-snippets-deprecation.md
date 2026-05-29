# P2-R3-2026-05-29-root-and-snippets-deprecation

## Summary

Deprecated framework-owned root artifacts and removed the snippets library. The framework now keeps its own documentation under `FCVW/`, while the repository root is reserved for the application being instantiated.

## Related Plan

- `FCVW/Plans/completed/P2-R3-2026-05-29-root-and-snippets-deprecation.md`

## Items Removed

- `README.md`
- `docs/index.html`
- `FCVW/snippets/README.md`
- `FCVW/snippets/tokens.css`
- `FCVW/snippets/gallery.html`

## Items Modified

- `FCVW/README.md`
- `FCVW/DESIGN.md`
- `FCVW/SCOPE.md`
- `FCVW/INSTANTIATION.md`
- `FCVW/CONTEXT_MAP.md`
- `FCVW/FILESYSTEM.md`
- `FCVW/MANIFEST.md`
- `FCVW/AI.md`
- `FCVW/skills/project-instantiation/SKILL.md`
- `FCVW/wiki/index.md`
- `FCVW/wiki/log.md`

## Items Created

- `FCVW/audits/2026-05-29-framework-structure-audit.md`
- `FCVW/changelogs/unreleased/P2-R3-2026-05-29-root-and-snippets-deprecation.md`
- `FCVW/wiki/sessions/S003-2026-05-29-root-and-snippets-deprecation.md`

## Validation

- `git diff --check`
- Custom structural scan for removed paths, retained framework docs, Markdown links/tables/fences, and skill triggers.
- `git status --short`

## Risks

- If GitHub Pages currently serves from root `docs/`, publication settings must be adjusted or a release export step must be defined.
