---
schema: "fcvw/filesystem@1"
artifact_role: "generated"
owner: "framework"
upgrade_strategy: "regenerate"
last_reviewed: "2026-08-21"
---

# Filesystem contract

The physical filesystem is the source of truth. This document summarizes canonical paths and uses globs for historical record collections; it must not become a thousand-line manual mirror.

## Source checkout root

- `AGENTS.md`
- `README.md`
- `LICENSE`
- `NOTICE`
- `.gitignore`
- local-only `.obsidian/` may be recreated by Obsidian and is ignored; it is never required or distributed
- optional provider bridges `.cursorrules` and `.windsurfrules` (when distributed)
- `FCVW/`
- `tools/validate_fcvw.py`
- `tools/test_open_issues.py`
- `tools/test_plan_dependencies_and_knowledge.py`
- `tools/frontmatter_fcvw.py`
- `tools/document_graph_fcvw.py`
- `tools/knowledge_graph_fcvw.py`
- `tools/knowledge_sources_fcvw.py`
- `tools/plan_dependencies_fcvw.py`
- `tools/plan_queue_fcvw.py`
- `tools/locale_fcvw.py`
- `tools/package_release_fcvw.py`
- `tools/release_layout_fcvw.py`
- optional context tools `tools/build_context_index.py` and `tools/retrieve_context.py`
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

- Record directories may contain governed framework history; application/downstream plans, releases, audits, sessions, wiki history, and comparison evidence are excluded.
- No application runtime data, credentials, screenshots, application histories, or application license files occur under `FCVW/`.
- Production-derived comparison fixtures are absent from the project root and clean distribution.
- Root entries outside the documented source allowlist are rejected; Git metadata, repository-owned `.github/` configuration, and ignored local `.obsidian/` state are allowed when present.
- Clean distribution assets exclude `.git/`, `.github/`, `.obsidian/`, caches, workspaces, and other repository/editor state unless a release contract explicitly requires an infrastructure file.
- `FCVW/wiki/regressions/` contains only its README until a real, sourced regression is confirmed.
- Every root framework policy is cataloged in `FCVW/README.md` and discoverable from `AGENTS.md`, `CONTEXT_MAP.md`, or that index; every project profile is cataloged and every skill session type is mapped in `CONTEXT_MAP.md`.

Run the optional validator to verify the current tree instead of manually expanding every historical filename.

## Graph, queues, and application rules

- Application-specific cross-cutting rules: `FCVW/APP_RULES.md`.
- Generated Obsidian-compatible catalog: `FCVW/DOCUMENT_GRAPH.md`.
- Active priority queues: `FCVW/Plans/{pending,in_progress}/QUEUE.md`.
- Optional disposable context indexes: user-selected output path; never a normative source or distributable record.
- Optional disposable knowledge graphs, source-review reports, and aggregate queue views: `.fcvw-cache/` or another user-selected output path; never normative or distributable records.

Every governed Markdown file is linked from an official entrypoint, a domain catalog, a queue, or `DOCUMENT_GRAPH.md`. File movement requires link-graph regeneration and validation.

## Installed release root

Starting with V0.15.0 assets, the template root contains exactly:

```text
AGENTS.md
FCVW/
```

`FCVW/` contains policies, profiles, records, `tools/`, `LICENSE`, `NOTICE`, and optional provider bridges. Root `README.md`, `.gitignore`, `.github/`, and Git/editor/cache state are source or staging infrastructure and are not installed payload files. This containment is a release-package contract; application-owned root files may coexist after installation but are never included in the framework removal boundary.

Deleting `FCVW/` removes the contained framework filesystem. `AGENTS.md` is reviewed separately because it is the root entrypoint and may have been customized. Upgrades or removal never bulk-delete an application root `tools/`, license, notice, rules file, or other ambiguous pre-V0.15.0 path.

## Language-specific release staging

The governed source keeps its conventional development tree. Downloaded V0.15.0-or-later templates use the contained installed root above. FCVW has no multilingual runtime layout and does not create, discover, select, or synchronize language directories during normal validation, instantiation, or use.

Release preparation may create an external or disposable staging directory with independent `pt-BR/`, `en-US/`, `es/`, and `de/` variants. Each variant is a complete empty template whose own root exposes `AGENTS.md`, `README.md`, `FCVW/`, and `tools/`. This staging directory is not part of the source contract and must not be copied wholesale into an installed framework.

The user chooses the language by downloading exactly one variant. Each variant owns its own `FCVW/DOCUMENT_GRAPH.md`, must be internally reachable, and must not depend on links to another language. The four-variant parity requirement is a release gate only.

`tools/package_release_fcvw.py` validates the external staging tree, materializes each variant through `tools/release_layout_fcvw.py`, regenerates the installed document graph, creates deterministic language-specific ZIPs, inspects the two-entry payload root, and writes `SHA256SUMS.txt`. Its explicit `--allow-in-review` mode creates local candidate assets without weakening or satisfying the publication review gate.

## Relationships

Regenerate this inventory under the [document graph contract](DOCUMENT_GRAPH.md) and interpret ownership through [OWNERSHIP.md](OWNERSHIP.md).
