# Template: decision knowledge

```markdown
---
schema: "fcvw/wiki@1"
id: "DEC-YYYYMMDD-<short-id>"
artifact_role: "record"
owner: "<accountable-owner>"
upgrade_strategy: "preserve"
record_scope: "<application | framework>"
retrieval_scope: "search_only"
title: "<decision>"
type: "decision"
status: "draft"
confidence: "low"
maturity: "provisional"
created_at: "YYYY-MM-DD"
last_reviewed: "YYYY-MM-DD"
next_review: "YYYY-MM-DD"
related_version: "V0.0.0"
derived_from:
  - "<source-wiki-id-or-governed-path>"
sources:
  - "decisions/<ADR>.md"
tags:
  - "decision"
---

# <Decision>

## Context

<Explain the context of the decision.>

## Alternatives Considered

1.
2.
3.

## Decision Made

<Describe the decision.>

## Justification

<Explain why this decision was made.>

## Positive Consequences

-

## Negative Consequences or Trade-Offs

-

## Conditions for Review

-

## Relations

- [Architectural decision or source record](<relative-path-to-authoritative-source.md>)
```
