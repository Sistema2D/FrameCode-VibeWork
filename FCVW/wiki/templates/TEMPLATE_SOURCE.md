# Template: tracked source

```markdown
---
schema: "fcvw/wiki@1"
id: "SRC-YYYYMMDD-<short-id>"
artifact_role: "record"
owner: "<accountable-owner>"
upgrade_strategy: "preserve"
record_scope: "<application | framework>"
retrieval_scope: "search_only"
title: "<source title>"
type: "source"
status: "draft"
confidence: "medium"
created_at: "YYYY-MM-DD"
last_reviewed: "YYYY-MM-DD"
next_review: "YYYY-MM-DD"
source_type: "repository_file"
source_path: "<repository-relative-or-page-relative-path>"
source_digest: "sha256:<64-lowercase-hex>"
ingested_at: "YYYY-MM-DD"
last_checked: "YYYY-MM-DD"
sources:
  - "<source-path-or-url>"
tags:
  - "source"
---

# <Source Title>

## Origin and scope

<Describe the source, owner, relevant boundary, and why explicit tracking adds value.>

## Evidence represented

<Describe what this source can and cannot support.>

## Review and digest procedure

<Describe how the digest is recomputed and which dependent knowledge must be reviewed after a change.>

## Authoritative source

- [Tracked source or governing artifact](<relative-path-to-authoritative-source.md>)
```
