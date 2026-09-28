# Template: wiki note

Save as `wiki/<ID>-<topic>.md`. One envelope serves every `fcvw/wiki@1` note; choose the body block for the note's `type`. Confirmed regressions use [TEMPLATE_REGRESSION.md](TEMPLATE_REGRESSION.md); product pages and QA runs use the templates in [the QA skill](../skills/QA/PRODUCT_WIKI.md). Types, ID prefixes and rules are in the [wiki contract](../wiki/README.md).

## Envelope

```markdown
---
schema: "fcvw/wiki@1"
id: "<PREFIX>-YYYYMMDD-<short-id>"
artifact_role: "record"
owner: "<accountable-owner>"
upgrade_strategy: "preserve"
record_scope: "<application | framework>"
retrieval_scope: "search_only"
title: "<title>"
type: "<concept | component | pattern | decision | failure | refactoring | audit | agent | feedback | release | session | prompt | question | synthesis | source | raw>"
status: "draft"
confidence: "low"
maturity: "provisional"          # claim-bearing notes only; omit for source, raw and session
created_at: "YYYY-MM-DD"
last_reviewed: "YYYY-MM-DD"
next_review: "YYYY-MM-DD"
derived_from:
  - "<source-wiki-id-or-governed-path>"
related:
  - "<related-wiki-id-or-governed-path>"
sources:
  - "<plan, changelog, code, audit, issue or evidence>"
tags:
  - "<canonical-tag>"
---

# <Title>

<Body block for the type, below.>

## Relations

- [Authoritative source or related record](<relative-path-to-authoritative-source.md>)
```

A note needs at least one navigable outgoing link to its authoritative source; naming the source only in frontmatter is not enough.

## Body blocks by type

| `type` | Sections |
|---|---|
| default (`concept`, `component`, `refactoring`, `agent`, `prompt`, `synthesis`) | Summary; Context; Content; Sources and evidence; Limitations |
| `pattern` | Problem it solves; Recommended solution; When to use; When not to use; Application example; Validation evidence; Risks |
| `decision` | Context; Alternatives considered; Decision made; Justification; Positive consequences; Trade-offs; Conditions for review |
| `failure` | Symptoms; Context; Probable root cause; Unsuccessful attempts; Validated solution; Validation executed; Prevention |
| `question` | Question; Why it matters; Context; Hypotheses; Existing evidence; Next steps; Resolution |
| `release` | Version summary; Main changes; Relevant decisions; Patterns; Fixed failures; Known gaps; Reusable learnings; Next recommendations |
| `session` (`SES-YYYYMMDD-HHMMSS-<short-id>`) | Objective and scope; Completed state; Active or blocked state; Files changed; Validation; Decisions and reusable learning; Risks and next authorized step |
| technical debt (`type: concept`, `DEBT-` prefix) | Context and location; Classification and impact; Remediation plan; Follow-up |
| wiki lint report (`type: audit`, `LINT-` prefix) | Date; Scope; Trigger; Checks; Findings; Actions executed; Open items; Result |
| `source` | Origin and scope; Evidence represented; Review and digest procedure; Authoritative source |
| `feedback` | Evidence; **Suggestion**; Cost and risk; Assessment of prior notes (only with `related_feedback`, and after Suggestion); Proposed disposition |

## Extra fields by type

- `source`: `source_type` (`repository_file | web | document | dataset | issue | api | conversation | other`), `source_path`, `source_url`, `source_digest: "sha256:<64-lowercase-hex>"`, `ingested_at`, `last_checked`.
- `feedback`: `authored_by_model`, `topic` (kebab-case), `feedback_status` (`open | accepted | declined | applied | superseded`), optional `related_feedback` and `related_plan`. Write **Suggestion** before reading earlier notes on the same topic; the validator enforces the order.
