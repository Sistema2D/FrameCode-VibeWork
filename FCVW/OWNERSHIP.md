---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Artifact ownership and upgrades

Ownership determines what an FCVW upgrade may replace.

| Role | Meaning | Examples | Upgrade action |
|---|---|---|---|
| `framework_policy` | Generic operating rule | `PLANNING.md`, `RELEASE.md` | replace when compatible |
| `framework_lock` | Installed baseline | `FRAMEWORK_LOCK.md` | update through migration |
| `project_profile` | Application-specific truth | `PROJECT.md`, `SECURITY.md`, `DATA.md`, `APP_RULES.md` | preserve; merge deliberately |
| `template` | Reusable empty model | `governance/` | replace when schema-compatible |
| `record` | Historical evidence | plans, changelogs, ADRs, failures | preserve; never bulk-overwrite |
| `generated` | Derived navigation or metrics | disposable views and indexes in `.fcvw-cache/` | regenerate from current state |
| `example` | Non-authoritative sample | filled examples inside templates | replace; never instantiate as truth |

## Required metadata

Canonical documents and new records should declare:

- `schema`;
- `artifact_role`;
- `owner`;
- `upgrade_strategy`;
- status and dates when the artifact has a lifecycle.

Legacy documents without metadata remain readable but are validated as legacy until touched.

## Upgrade algorithm

1. Read `FRAMEWORK_LOCK.md` and the target migration note.
2. Inventory local roles before copying.
3. Back up project profiles and records.
4. Replace compatible framework policies and templates.
5. Merge project profiles section by section; never use global text replacement.
6. Preserve all records.
7. Regenerate generated artifacts.
8. Run the validator in `instantiated` profile.
9. Update `FRAMEWORK_LOCK.md` only after validation.

## Protected paths

The following are always project-owned after instantiation:

- `Plans/**`;
- `changelogs/**`;
- `audits/**`;
- `briefings/**`;
- `troubleshooting/**`;
- application-created `decisions/**`;
- application-created `wiki/**`;
- populated project profiles.

An upstream release must publish a file-role manifest or equivalent migration table so selective upgrade does not depend on guesswork.

## New operational surfaces

- `APP_RULES.md` is a preserved project profile and is never overwritten by a framework upgrade.
- The plan queue is derived from plan frontmatter; no queue file exists. Legacy `QUEUE.md` and `queue.d/` files are project-owned and are never deleted by an upgrade.
- No navigation catalog is versioned; records are reachable through their canonical directory (see [ADR-0011](https://github.com/Sistema2D/FrameCode-VibeWork/blob/main/FCVW/decisions/ADR-0011-record-reachability.md)).
- Context indexes are disposable generated artifacts and never replace their source documents.
- Knowledge graphs, stale-source reports, and aggregate queue views are disposable generated artifacts; their Markdown/frontmatter sources remain authoritative.
- `wiki/index.md` is a small preserved project profile; framework upgrades never replace its curated active links.
- Language-specific release variants contain the same ownership classes as the canonical source. A user downloads one variant; its framework policies and templates remain framework-owned, while populated project profiles and new project records become project-owned. FCVW does not install or own parallel language trees in the project.
- Release assets from V0.16.0 onward contain every framework filesystem path under the `FCVW/` root except `AGENTS.md` and the optional provider bridges `.cursorrules` and `.windsurfrules`, which only work at the repository root. Physical containment does not change ownership of populated profiles or records inside that directory; back them up before upgrading or removing.
- Removal may target only `FCVW/` as a directory plus a separate, explicit review of `AGENTS.md`, `.cursorrules`, and `.windsurfrules`. Never infer ownership of an application root `tools/`, `LICENSE`, `NOTICE`, or other ambiguous pre-V0.15.0 path, and never bulk-delete those paths.

## Filesystem layout

The physical tree is the source of truth; this section states only the rules and path classes, never a per-file inventory.

- **Installed release root:** `AGENTS.md`, `FCVW/`, and the optional provider bridges `.cursorrules` and `.windsurfrules`. Everything else of the framework, including `tools/`, `LICENSE` and `NOTICE`, lives under `FCVW/`. Deleting `FCVW/` removes the framework; `AGENTS.md` and the bridges are reviewed separately. The bridges are one-line legacy files that point older editor integrations to `AGENTS.md`; tools that read `AGENTS.md` directly do not need them, and no new bridge is added without a concrete demand.
- **Source checkout root:** the installed entries plus `README.md`, `TODO.md` (maintainer backlog), `.gitignore`, `.gitattributes`, `.github/` and the development `tools/`. `README.md`, `TODO.md` and `.gitignore` are source-only and never installed. Local `.obsidian/`, `.fcvw-cache/` and `.codex-test-tmp/` are disposable and excluded from inventories and payloads.
- **Path classes under `FCVW/`:** policies and project profiles `FCVW/*.md`; templates `FCVW/governance/*.md`; skills `FCVW/skills/*/SKILL.md` plus skill-local references; plans `FCVW/Plans/<status>/*.md`; records in `FCVW/{decisions,audits,troubleshooting,framework-releases,changelogs,briefings}/`; knowledge notes `FCVW/wiki/*.md`; installed tools `FCVW/tools/`.
- **Directories are created on demand** by the first real record; the clean template ships no empty or README-only scaffolding.
- **Disposable outputs** (context indexes, knowledge graphs, queue views, reports) go to `.fcvw-cache/` or another user-selected path and are never distributed.
- **Clean template:** no application plans, releases, audits, wiki history, credentials, screenshots or production-derived fixtures; root entries outside the source list above are rejected by the validator.
- **Language variants** exist only in external release staging: each `pt-BR`, `en-US`, `es` and `de` variant is a complete template; the user downloads one. Normal validation never creates or selects language directories.

A merge conflict in a generated surface is never merged by hand: regenerate it.

