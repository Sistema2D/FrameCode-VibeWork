# Template: formal audit record

Save the instantiated record under the application's `FCVW/audits/` directory and replace every placeholder.

```markdown
---
schema: "fcvw/audit@1"
id: "AUD-YYYYMMDD-<short-id>"
artifact_role: "record"
owner: "<accountable-owner>"
upgrade_strategy: "preserve"
record_scope: "<application | framework>"
retrieval_scope: "search_only"
status: "draft | completed | blocked"
created_at: "YYYY-MM-DD"
last_reviewed: "YYYY-MM-DD"
sources:
  - "<authoritative-plan-policy-or-evidence-path>"
---

# Audit: <scope>

## Scope

<Boundaries and exclusions.>

## Authoritative sources

- [Plan, policy, release, or evidence](<relative-path-to-authoritative-source.md>)

## Method

<Checks and limitations.>

## Findings

| Severity | Surface | Finding | Evidence | Owner |
|---|---|---|---|---|
| <R1-R5> | <area> | <finding> | <path or procedure> | <owner> |

## Validation

<Reproducible commands or review procedure.>

## Limitations and residual risk

<Known limits and owner.>

## Follow-up

- [Plan or governing record](<relative-path-to-follow-up.md>)
```
