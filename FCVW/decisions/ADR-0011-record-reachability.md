---
schema: "fcvw/adr@1"
id: "ADR-0011"
status: "accepted"
date: "2026-09-28"
artifact_role: "record"
owner: "framework"
upgrade_strategy: "preserve"
record_scope: "framework"
retrieval_scope: "routed"
language: "en-US"
---

# ADR-0011: Records are reachable through their canonical directory

## Context

Every governed Markdown file had to be reachable from an entrypoint. In practice that was satisfied by `FCVW/DOCUMENT_GRAPH.md`, a generated catalog that links every file by construction: removing it left 148 files, including policies, profiles, skills and templates, with no real incoming link. The reachability rule therefore verified nothing, while the 20 KB catalog and one README per record directory had to be regenerated and caused merge conflicts.

## Decision

- Policies, profiles, templates and skills must be linked from an entrypoint or from a catalog that an entrypoint links ([FCVW/README.md](../README.md), the skills catalog, the governance template catalog, the plans and wiki contracts).
- Records are reachable through their canonical directory: `Plans/`, `decisions/`, `audits/`, `troubleshooting/`, `framework-releases/`, `changelogs/`, `briefings/` and `wiki/`. They still need an outgoing link to their authoritative source (`document-source-link`).
- The document graph catalog is a disposable view written to `.fcvw-cache/` on demand. Links from any legacy `FCVW/DOCUMENT_GRAPH.md` are ignored for reachability, and the file is reported for deletion.
- Record directories carry no README; the rules for what goes in each one live in the owning policy.

## Alternatives and consequences

- Keep the generated catalog as the single catalog: rejected, because a catalog that links everything cannot detect an orphan.
- Consequence: 7 files removed (the catalog and six directory READMEs) and the reachability rule became meaningful. Obsidian's file explorer, graph view and backlinks provide the navigation the catalog offered.

## Compatibility, validation and rollback

Existing downstream records stay valid without edits. A downstream `FCVW/DOCUMENT_GRAPH.md` produces a warning. Rollback: regenerate a catalog into `FCVW/` and restore the removed READMEs from git history.

## Relationships

- [Phase 2 plan](../Plans/in_progress/P2-R4-2026-09-28-phase2-file-reduction.md).
- [Ownership and filesystem layout](../OWNERSHIP.md).
