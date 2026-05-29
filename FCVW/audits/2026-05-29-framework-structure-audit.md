# Framework Structure Audit - 2026-05-29

## Status

`completed`

## Scope

Audit of root-owned artifacts, duplicate documentation folders, discontinued snippets, and remaining framework consistency risks after `P2-R3-2026-05-29-root-and-snippets-deprecation`.

## Decisions Applied

- Root `README.md` removed from the framework baseline. It must be generated for the target application during Phase 0.
- Root `docs/` removed because it duplicated `FCVW/docs/` byte-for-byte and occupied application-owned root space.
- `FCVW/docs/index.html` retained as the framework documentation site artifact.
- `FCVW/snippets/` removed. `FCVW/DESIGN.md` is the design-system source of truth.

## Validation Snapshot

- Root `README.md`: removed.
- Root `docs/`: removed.
- `FCVW/snippets/`: removed.
- `FCVW/docs/index.html`: retained.
- Markdown broken links: 0.
- Unclosed code fences: 0.
- Broken Markdown tables: 0.
- Skill files without activation triggers: 0.

## Follow-Up Status

| Severity | Finding | Evidence | Recommendation |
|---|---|---|---|
| P3 | Obsolete `FCVW/pr_description.txt` remained in the repository. | File referenced the removed `snippets/tokens.css` and `--shadow-sm`. | Resolved by `P3-R2-2026-05-29-audit-follow-up-cleanup`; stale artifact removed. |
| P3 | GitHub Pages publication path became a release decision, not an always-present root folder. | Root `docs/` was removed; `FCVW/docs/` remains. | Resolved by documenting `FCVW/docs/` publication rules in `FCVW/RELEASE.md`. |
| P4 | Historical records reference removed root README/docs/snippets artifacts. | Completed plans, older changelog fragments, and session syntheses mention those paths. | Preserved as historical evidence; no rewrite applied. |
| P4 | `FCVW/changelogs/V0.7.5.md` was reconstructed from Git history. | No original formal changelog existed for the tag at audit time. | Resolved by backfilling `V0.7.0` through `V0.7.4` changelogs from Git tag evidence. |

## Optimization Opportunities

| Priority | Opportunity | Rationale |
|---|---|---|
| P2 | Add a compact release-publishing rule for `FCVW/docs/`. | Applied in `FCVW/RELEASE.md`. |
| P3 | Remove or archive one-off transient files like `FCVW/pr_description.txt`. | Applied by removing `FCVW/pr_description.txt`. |
| P3 | Reduce duplicated structure declarations between `FCVW/MANIFEST.md`, `FCVW/FILESYSTEM.md`, and `FCVW/README.md`. | Applied by making `FCVW/FILESYSTEM.md` the detailed structural source of truth. |
| P4 | Add a short "root is application-owned" checklist to `FCVW/AUDIT.md`. | Applied in `FCVW/AUDIT.md`. |

## Result

The requested structural changes and follow-up corrections are applied. Historical evidence that mentions removed paths was intentionally preserved.
