---
schema: "fcvw/adr@1"
id: "ADR-0005"
status: "accepted"
date: "2026-08-21"
artifact_role: "record"
owner: "framework"
upgrade_strategy: "preserve"
record_scope: "framework"
retrieval_scope: "routed"
language: "en-US"
---

# ADR-0005: Contained release filesystem

## Context

GitHub issue [#52](https://github.com/Sistema2D/FrameCode-VibeWork/issues/52) identifies that release assets scatter framework-owned files across the application root. A later removal must know every historical path and may collide with an application's own `tools/`, license, notice, or provider configuration.

## Alternatives considered

1. Preserve the mirrored source-tree layout in every asset.
2. Add an executable uninstaller that tracks individual files.
3. Introduce another wrapper directory alongside the existing `FCVW/` directory.
4. Keep `AGENTS.md` as the root entrypoint and contain every other installed framework file under the existing `FCVW/` directory.

## Decision

Adopt option 4 for V0.15.0-or-later release assets.

- The source checkout and pre-package language staging keep their development layout.
- The packager deterministically maps each variant to a template root containing exactly `AGENTS.md` and `FCVW/`.
- Existing `FCVW/**` paths remain stable; root `tools/**`, legal notices, and provider bridges move under `FCVW/`.
- Repository-only root `README.md` and `.gitignore` are not installed payload files.
- Path collisions, symlinks, forbidden state, or a third root entry block packaging.
- The installed document graph is regenerated after mapping.
- Deleting `FCVW/` is the physical removal boundary. `AGENTS.md` is reviewed separately because downstream customization is allowed.
- Migration from older layouts is manifest-based and never bulk-deletes ambiguous application-root paths.

## Justification

The existing `FCVW/` directory already owns the framework namespace. Reusing it minimizes path churn, requires no dependency or background installer, and makes the deletion boundary visible while preserving project-owned content rules.

## Consequences

- Fresh assets are mechanically removable and cannot scatter new framework files through the application root.
- Installed tool commands use `FCVW/tools/`; source-development commands continue using `tools/`.
- Root-discovered optional provider files no longer activate automatically from the release payload and become contained reference adapters.
- Older installations need cautious reconciliation because same-named root paths may have become application-owned.

## Risks and mitigations

- Risk: accidental loss of project records stored inside `FCVW/`. Mitigation: ownership policy requires backup before removal and never describes containment as ownership replacement.
- Risk: source and installed paths drift. Mitigation: one shared mapper, installed validator support, deterministic package tests, and migration documentation.
- Risk: archive looks correct but links target the staging layout. Mitigation: regenerate and validate the installed document graph after mapping.

## Relationships

- Implementation plan: [single-folder release layout](../Plans/completed/P2-R4-2026-08-21-single-folder-release-layout.md).
- Governing policies: [Filesystem](../FILESYSTEM.md), [Ownership](../OWNERSHIP.md), [Release](../RELEASE.md), and [Migrations](../MIGRATIONS.md).
- Related decision: [ADR-0004](ADR-0004-multilingual-source-and-release-model.md).
- Framework release: [V0.15.0](../framework-releases/V0.15.0.md).
