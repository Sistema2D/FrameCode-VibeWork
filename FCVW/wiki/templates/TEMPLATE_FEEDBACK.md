# Template: framework feedback note

Save as `wiki/feedback/FB-YYYYMMDD-<short-id>-<topic>.md`.

Write the `Suggestion` section **before** opening the earlier notes on the same
`topic`. Only then fill in `Assessment of prior notes`. The validator enforces
that order because reading another model's conclusion first tends to produce
agreement, and two independent readings are the reason this surface exists.

```markdown
---
schema: "fcvw/wiki@1"
id: "FB-YYYYMMDD-<short-id>"
artifact_role: "record"
owner: "project"
upgrade_strategy: "preserve"
record_scope: "application"
retrieval_scope: "search_only"
title: "<one-line summary of the suggestion>"
type: "feedback"
status: "draft"
confidence: "medium"
created_at: "YYYY-MM-DD"
last_reviewed: "YYYY-MM-DD"
authored_by_model: "<model-and-version>"
topic: "<kebab-case-topic>"
feedback_status: "open"
related_feedback: []
sources:
  - "<path or evidence that prompted this>"
tags:
  - "framework-feedback"
---

# <One-line summary of the suggestion>

## Evidence

<What was observed, where, and in which session or plan. Concrete beats general:
a path, a rule name, a command and its output.>

Source: [`FCVW/PLANNING.md`](../../PLANNING.md)

<Replace the link above with the document the note is actually about. A record
needs one navigable outgoing link to its authoritative source; the validator
refuses a note that only names its source in frontmatter.>

## Suggestion

<What should change in the framework, and why. State this before reading any
prior note on the same topic.>

## Cost and risk

<What the change would cost in surface, tokens, or migration, and what it would
break. A suggestion without a cost is a wish.>

## Assessment of prior notes

<Required only when `related_feedback` is non-empty. For each prior note: what
you agree with, what you disagree with, and why. Name the note and its model.
Omit this section entirely when yours is the first note on the topic.>

## Proposed disposition

<`open` for the maintainer to decide, or a concrete next step: a plan id, a
policy to change, a rule to add.>
```

## Fields

| Field | Required | Values |
|---|---|---|
| `authored_by_model` | yes | model and version that wrote the note |
| `topic` | yes | kebab-case key that groups notes from different models |
| `feedback_status` | yes | `open`, `accepted`, `declined`, `applied`, `superseded` |
| `related_feedback` | no | ids of the earlier notes this one assesses |
| `related_plan` | no | plan that acted on the note |

## Rules

See [`../feedback/README.md`](../feedback/README.md) for the complete rules,
including why a note never overwrites another model's note and why this directory
deliberately contradicts the rule in
[`../agents/README.md`](../agents/README.md).
