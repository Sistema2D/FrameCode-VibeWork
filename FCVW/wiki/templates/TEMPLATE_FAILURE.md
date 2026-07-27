# Template: failure knowledge

```markdown
---
schema: "fcvw/wiki@1"
id: "FAIL-YYYYMMDD-<short-id>"
artifact_role: "record"
owner: "<accountable-owner>"
upgrade_strategy: "preserve"
record_scope: "<application | framework>"
retrieval_scope: "search_only"
title: "<failure>"
type: "failure"
status: "draft"
confidence: "low"
created_at: "YYYY-MM-DD"
last_reviewed: "YYYY-MM-DD"
related_version: "V0.0.0"
sources:
  - "troubleshooting/<file>.md"
tags:
  - "failure"
---

# <Failure>

## Symptoms

-

## Context

<When does the failure occur?>

## Probable Root Cause

<Describe the root cause or main hypothesis.>

## Unsuccessful Attempts

-

## Validated Solution

-

## Validation Executed

-

## Prevention

-

## Relations

- [Troubleshooting source, plan, or related component](<relative-path-to-authoritative-source.md>)
```
