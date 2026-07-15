---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Framework migrations

## Principles

- Migrate framework-owned surfaces; preserve project-owned truth and history.
- Never normalize all historical records merely to satisfy a new schema.
- Enforce the current schema on new or substantively edited records.
- Record legacy exceptions in a baseline and reduce them over time.
- Do not mark the framework lock as upgraded until validation passes.

## V0.12.0 to V0.13.0

### Reason

The V0.12.0 clean package reduced many operational documents, templates, refactoring guides, and skills to placeholders. Real-application evidence also showed that manual-only validation, sequential session IDs, mixed version namespaces, and destructive memory rotation did not scale.

### Required migration

1. Preserve project profiles and all record directories.
2. Restore operational framework policies and specialized templates.
3. Add `FRAMEWORK_LOCK.md`, `OWNERSHIP.md`, and `SCHEMAS.md`.
4. Move FCVW release history to `framework-releases/`; keep application releases in `changelogs/`.
5. Add schema metadata when records are created or substantively edited.
6. Replace destructive session deletion with archive and synthesis.
7. Use collision-resistant session IDs for new sessions.
8. Regenerate `FILESYSTEM.md` and run validation.
9. Remove production-derived comparison fixtures from the framework project after extracting only generic, reviewed contracts.
10. Adopt `fcvw/plan@2` for new and substantively reopened plans, including `regression_contract` and a completed Regression impact section.
11. Add `REGRESSION_GUARDS.md`, the Regression gate, watcher triggers, risk matrix, and `wiki/regressions/` template.

### Compatibility notes

- Historical plan filenames outside the current P1–P5/R1–R5 convention remain valid legacy evidence.
- Historical wiki pages without frontmatter are not rewritten automatically.
- Existing sequential session filenames remain readable; new pages require a unique `id`.
- Existing application changelogs stay in place. Only framework-release records move to the new namespace.
- Existing `fcvw/plan@1` records stay readable and are not rewritten solely for the Regression impact requirement.
- A confirmed regression may be promoted to `fcvw/regression@1`; do not fabricate records during migration.

## Legacy baseline

The `incremental` profile accepts a project-specific baseline for pre-existing findings:

```powershell
python tools/validate_fcvw.py --root . --profile incremental --baseline path/to/legacy-baseline.md
```

Start from `governance/TEMPLATE_LEGACY_BASELINE.md`. The file and each row are time-bounded. Every entry must contain the exact path, rule identifier, existing message, justification, owner, and review date. Only the exact tuple `path + rule + message` becomes non-blocking; changed messages and new paths still fail. Expired or malformed baselines fail configuration, and entries that no longer match are reported as stale warnings so they can be removed.

Without `--baseline`, `incremental` blocks all applicable findings. `--baseline` is rejected under other profiles; `strict` always blocks all applicable findings.
