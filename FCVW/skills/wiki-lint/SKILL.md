---
schema: "fcvw/skill@1"
name: "wiki-lint"
description: "Validate wiki schema, links, freshness, baselines, and index coverage."
version: "1.1.0"
trigger_keywords:
  - "wiki lint"
  - "orphan pages"
  - "wiki audit"
  - "lint wiki"
session_types:
  - "wiki_maintenance"
  - "audit"
  - "release"
---

# Wiki lint

## Purpose

Find structural and knowledge-quality problems without forcing bulk rewrites of historical evidence.

## Modes

- **Incremental:** fail new/changed pages that violate `fcvw/wiki@1`; report legacy findings separately.
- **Strict:** validate every non-exempt page.
- **Release:** incremental checks plus links and newly relevant release knowledge.

## Inputs

`MEMORY.md`, `wiki/schema.md`, `wiki/index.md`, changed pages, and optional legacy baseline.

## Checks

- required frontmatter and controlled values;
- unique IDs;
- source coverage and confidence consistency;
- broken Markdown links and wikilinks;
- duplicate/canonical/superseded relationships;
- stale validated claims;
- orphan pages that should be discoverable;
- active-session budget and archive index;
- unanswered questions beyond project threshold;
- reusable knowledge left only in completed plans or failures.

A release synthesis is created when a release introduces reusable knowledge, breaking migration, major incident learning, or an explicit project policy requires it. Patch releases do not require a duplicate synthesis by default.

## Non-responsibilities

- deleting old pages to reach a clean count;
- silently converting low-confidence notes to validated;
- treating sessions as canonical truth.

## Required output

Report mode, pages checked, new failures, legacy findings, fixes, waivers, and remaining review work.

## Validation and exit

New or changed pages comply, IDs are unique, links resolve, and every suppressed legacy finding has an exact path, rule, owner, and review date.
