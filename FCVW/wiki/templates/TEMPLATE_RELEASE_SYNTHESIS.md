# Template: release synthesis

```markdown
---
schema: "fcvw/wiki@1"
id: "REL-YYYYMMDD-<short-id>"
artifact_role: "record"
owner: "<accountable-owner>"
upgrade_strategy: "preserve"
record_scope: "<application | framework>"
retrieval_scope: "search_only"
title: "Release Synthesis <Vx.y.z>"
type: "release"
status: "draft"
confidence: "medium"
maturity: "provisional"
created_at: "YYYY-MM-DD"
last_reviewed: "YYYY-MM-DD"
next_review: "YYYY-MM-DD"
related_version: "Vx.y.z"
derived_from:
  - "<release-record-wiki-id-or-governed-path>"
sources:
  - "changelogs/Vx.y.z.md"
tags:
  - "release"
---

# Release Synthesis <Vx.y.z>

## Version Summary

<Objective version summary.>

## Main Changes

-

## Relevant Decisions

-

## Patterns Created or Reinforced

-

## Fixed Failures

-

## Refactorings Executed

-

## Related Audits

-

## Known Gaps / Open Items

-

## Reusable Learnings

-

## Next Recommendations

-

## Authoritative release and related records

- [Application changelog or framework release](<relative-path-to-release-record.md>)
```
