---
schema: "fcvw/skill@1"
name: "memory-rotation"
description: "Archive and curate old sessions without destroying audit evidence."
version: "1.1.0"
trigger_keywords:
  - "rotate memory"
  - "context bloat"
  - "archive sessions"
  - "rotacionar memória"
session_types:
  - "wiki_maintenance"
  - "handoff"
---

# Memory rotation

## Purpose

Keep active session context bounded while preserving historical evidence and promoting sourced reusable knowledge.

## Use when

- active sessions exceed 10 files, 100 KB, or the project's context budget;
- duplicated or stale session summaries impair retrieval;
- the user requests archive, rotation, or memory consolidation.

## Do not use for

- deleting evidence to make validation appear clean;
- rewriting published history;
- replacing canonical project documents with session narrative.

## Inputs

- `MEMORY.md`;
- `wiki/schema.md`;
- active and archived session indexes;
- retention/legal requirements.

## Procedure

1. Inventory active sessions and choose a bounded archive range.
2. Identify decisions, patterns, failures, and unresolved conflicts.
3. Promote only sourced, reusable knowledge; update an existing canonical page before creating a duplicate.
4. Create `wiki/archive/YYYY/README.md` with range, sources, destination paths, and unresolved items.
5. Move selected sessions to `wiki/archive/YYYY/`.
6. Keep the latest 3–10 relevant sessions active.
7. Update index, log, metrics, and backlinks.
8. Run wiki lint in incremental mode.

## Required output

Record files moved, knowledge promoted, duplicates merged, unresolved conflicts, retention decision, and validation.

## Validation and exit

- no source session is lost;
- archive links resolve;
- active session IDs remain unique;
- promoted claims cite sources;
- active memory is within the configured budget.
