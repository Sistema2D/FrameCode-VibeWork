---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Technical memory lifecycle

## Layers

| Layer | Location | Purpose | Default loading |
|---|---|---|---|
| Active handoff | `wiki/sessions/` | recent session continuity | latest relevant only |
| Curated knowledge | concepts, patterns, failures, decisions | reusable current understanding | search/on demand |
| Archive | `wiki/archive/YYYY/` | historical evidence | search only |
| Canonical truth | project profiles, ADRs, source code/data | authoritative current state | when applicable |

Sessions never override canonical documents.

## Session identity

New session pages use `id: SES-YYYYMMDD-HHMMSS-<short-id>`. Human-readable sequence numbers are optional and may not be used as the uniqueness mechanism.

## Rotation trigger

Rotate when active sessions exceed either:

- 10 files;
- 100 KB;
- the default context budget defined by the project.

## Safe rotation

1. Select sessions outside the active window.
2. Extract validated reusable knowledge and link sources.
3. Update existing canonical wiki pages before creating duplicates.
4. Create an archive index with date range and source list.
5. Move old sessions to `wiki/archive/YYYY/`; do not delete audit evidence.
6. Keep the latest 3–10 relevant sessions active according to project cadence.
7. Run wiki lint and record unresolved conflicts.

Deletion requires an explicit retention policy, approval, and evidence that no legal, audit, security, or recovery need remains.

Resolved feedback notes (`applied`, `declined`, or `superseded`) follow this same rotation; `open` notes stay active until the maintainer decides.

## Freshness

Knowledge pages declare confidence, sources, last review date, and supersession links. Stale information is reviewed or marked obsolete; it is not silently treated as current.

Tracked source pages may store `source_digest` and knowledge may declare `derived_from`. A digest mismatch is a derived review condition: report the source and dependent pages, then require a reviewer to confirm, update, supersede, or invalidate the knowledge. Do not add a lifecycle `stale` status or silently refresh the stored digest.

Claim-bearing pages may use maturity independently from lifecycle, confidence, and authority. Source, raw, and session records do not require maturity.

The document graph owns navigation and reachability. The disposable knowledge graph owns typed semantic relations; neither graph is canonical truth.
