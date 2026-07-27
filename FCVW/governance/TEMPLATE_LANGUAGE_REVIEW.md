# Template: language-specific release review

Save one completed copy as `FCVW/LANGUAGE_REVIEW.md` inside each staged release variant. This is accountable release evidence, not a runtime language selector.

```markdown
---
schema: "fcvw/language-review@1"
artifact_role: "record"
owner: "<accountable-language-reviewer>"
upgrade_strategy: "preserve"
record_scope: "framework"
retrieval_scope: "exact_only"
language: "pt-BR | en-US | es | de"
status: "draft | in_review | approved | rejected"
reviewer: "<reviewer-name-or-accountable-team>"
reviewed_at: "YYYY-MM-DD"
source_revision: "<40-character-content-baseline-revision>"
sources:
  - "FCVW/RELEASE.md"
  - "FCVW/SCHEMAS.md"
---

# Language-specific release review: <language>

## Scope

<Variant, source revision, reviewed surfaces, and explicit exclusions.>

## Authoritative sources

- [Release contract](RELEASE.md)
- [Schema contract](SCHEMAS.md)

## Review evidence

<Reviewer procedure, samples, automated parity checks, and human-language adaptation evidence.>

## Findings and disposition

<Blocking findings, corrections, or an explicit statement that none remain.>

## Limitations

<Residual language, legal, cultural, or accessibility limitations and accountable owner.>
```

Governed by the [language-specific release contract](../RELEASE.md) and [language-review schema](../SCHEMAS.md).
