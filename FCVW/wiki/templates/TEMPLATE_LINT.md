# Template: wiki lint report

```markdown
---
schema: "fcvw/wiki@1"
id: "LINT-YYYYMMDD-<short-id>"
artifact_role: "record"
owner: "<accountable-owner>"
upgrade_strategy: "preserve"
record_scope: "<application | framework>"
retrieval_scope: "search_only"
title: "LLM Wiki Lint Report"
type: "audit"
status: "draft"
confidence: "low"
created_at: "YYYY-MM-DD"
last_reviewed: "YYYY-MM-DD"
related_version: "V0.0.0"
sources:
  - "wiki/schema.md"
tags:
  - "wiki-lint"
---

# LLM Wiki Lint Report

## Date

YYYY-MM-DD

## Scope

<Describe the scope of the lint.>

## Trigger

<Describe why the lint was executed.>

## Checks

- [ ] Orphan pages.
- [ ] Broken links.
- [ ] Cited concepts without a page.
- [ ] Resolved failures without a synthesis.
- [ ] Completed plans without extracted learning.
- [ ] Changelogs without a release synthesis.
- [ ] ADRs without a page in `decisions/`.
- [ ] Obsolete pages without marking.
- [ ] Contradictions between sources.
- [ ] `index.md` updated.
- [ ] `log.md` updated.

## Findings

-

## Actions Executed

-

## Gaps / Open Items

-

## Result

`approved` / `approved with reservations` / `rejected`

## Authoritative sources and follow-up

- [Wiki schema, source record, or follow-up plan](<relative-path-to-authoritative-source.md>)
```
