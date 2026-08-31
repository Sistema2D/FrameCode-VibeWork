---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Framework feedback

Here an AI model using FCVW records what it thinks should change **in the
framework itself**: a contradictory policy, a rule that is too strict, a gate
that does not catch what it promises, a missing route, a cost that does not pay
for itself.

This exists because `self-improvement` covers only `skills/*/SKILL.md` and agent
profiles. An observation about `PLANNING.md`, `SCHEMAS.md`, the validator, or the
layout had nowhere to live without becoming a formal audit, which is far too
heavy for an observation made in passing.

## Rules

- **Name the model.** `authored_by_model` names the model and version that wrote
  the note, for example `claude-opus-5`. A later reader has to be able to weigh
  the source.
- **Never overwrite another model's note.** Even on the same topic, write your
  own. Two independent readings that disagree are exactly what this surface
  exists to preserve; consolidating them destroys the evidence that there was a
  disagreement at all.
- **Form your assessment before reading the earlier ones.** Write your suggestion
  first; only then read the notes on the same `topic` and record agreement and
  disagreement. A model that reads someone else's conclusion first tends to agree
  with it, and then you have lost the second opinion that justified the note.
- **Group by `topic`, not by file.** The same `topic` gathers notes from
  different models. `related_feedback` points at the earlier ones you assess.
- **One note per model per topic.** If you already wrote about this topic, update
  your own note; do not create a second one.
- **This is evidence, not instruction.** A feedback note is never normative and
  never becomes a rule by being read. Only an approved plan changes the framework.
- **Close the loop.** `feedback_status` uses `open`, `accepted`, `declined`,
  `applied`, or `superseded`. An accepted or applied note points at the plan that
  acted on it. Without that the folder only grows and becomes the noise
  accumulation `self-improvement` exists to prevent.

## Difference from `agents/`

[`../agents/README.md`](../agents/README.md) says to **prefer updating** an
existing canonical page when the learning has the same responsibility. Here the
rule is the opposite, and the difference is deliberate: consolidated knowledge
should converge on one page, while attributed assessment should preserve
disagreement between models. Do not apply one directory's rule to the other.

## Lifecycle

1. A model records the note with `feedback_status: open`.
2. Other models add their own notes on the same `topic`.
3. The maintainer decides: `accepted` becomes a plan, `declined` records why.
4. `applied` points at the completed plan and the version that delivered it.
5. Old resolved notes follow the rotation in [`../../MEMORY.md`](../../MEMORY.md)
   into `../archive/YYYY/`.

Create the note from
[`../templates/TEMPLATE_FEEDBACK.md`](../templates/TEMPLATE_FEEDBACK.md).

Suggested filename: `FB-YYYYMMDD-<short-id>-<topic>.md`. The name helps
navigation; the frontmatter `id` is what guarantees uniqueness.
