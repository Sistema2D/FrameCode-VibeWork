---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace_with_migration"
---

# Artifact schemas

FCVW uses YAML frontmatter for machine-checkable identity and Markdown for human-readable content.

## Common fields

| Field | Required when | Meaning |
|---|---|---|
| `schema` | all new canonical artifacts | contract name and major schema version |
| `artifact_role` | canonical documents | ownership class |
| `id` | records | unique stable identifier |
| `status` | lifecycle records | current state |
| `created_at` | records | ISO date |
| `updated_at` | mutable records | ISO date |
| `sources` | interpretative knowledge | evidence paths or references |

Unknown fields are allowed. Required fields and controlled values may not be renamed or translated.

## Plan — `fcvw/plan@2`

Required frontmatter: `id`, `status`, `priority`, `risk`, `created_at`, `updated_at`, `current_version`, `expected_version`, `owner`, `regression_contract`, and `context_files`.

Allowed statuses: `pending`, `in_progress`, `completed`, `discontinued`.

Allowed regression contracts: `required`, `not_applicable`. The body requirements and completion blockers are defined in `REGRESSION_GUARDS.md`.

The status must match the containing directory. IDs use `P1..P5-R1..R5-YYYY-MM-DD-slug`.

`fcvw/plan@1` is a supported legacy schema. It remains readable in place; substantively reopened plans migrate to `fcvw/plan@2`.

## Application changelog — `fcvw/changelog@1`

Required: application version, date, release status, release type, related plans, summary, affected areas, validation, known gaps, and rollback.

Allowed release statuses: `unreleased`, `in_preparation`, `published`, `canceled`.

## Framework release — `fcvw/framework-release@1`

Required: FCVW version, compatibility, migration note, created/modified/removed framework surfaces, schema changes, validation, and publication status.

Framework records live under `framework-releases/`, never under application `changelogs/`.

## Wiki page — `fcvw/wiki@1`

Required for new knowledge pages: `id`, `title`, `type`, `status`, `confidence`, `created_at`, `last_reviewed`, `sources`, and `tags`.

Session IDs use `SES-YYYYMMDD-HHMMSS-<short-id>`; sequential numbers may be displayed but are not unique identifiers.

## Regression record — `fcvw/regression@1`

Required frontmatter: `id`, `title`, `type`, `severity`, `status`, `detected_at`, `last_reviewed`, `related_plan`, `sources`, and `tags`.

Allowed types: `functional`, `interface`, `data`, `visual`, `security`, `ai`, `governance`, `documentation`, `performance`, and `operations`. Allowed statuses: `detected`, `mitigated`, `resolved`, `accepted`, `superseded`. IDs use `REG-YYYYMMDD-<short-id>` so parallel records do not rely on a shared counter.

The body records what regressed, detection, root cause, missing guardrail, permanent guardrail, replay test, related release, and residual risk. Reusable records live under `wiki/regressions/`.

## Skill — `fcvw/skill@1`

Required frontmatter: `schema`, `name`, `description`, `version`, `trigger_keywords`, and `session_types`.

The body must define purpose, use conditions, non-responsibilities, inputs, procedure, required output, validation, and exit criteria. Provider-specific commands are adapters, not core requirements.

## Automation contract — `fcvw/automation@1`

Required: `id`, `kind`, `status`, `trigger`, `preconditions`, `actions`, `evidence`, `failure_policy`, `rollback`, and `owner`.

## Legacy validation baseline — `fcvw/legacy-baseline@1`

Required frontmatter: `created_at`, `review_due`, and `owner`. Each Markdown table row requires exact path, rule ID, complete existing finding message, justification, owner, and review date.

The baseline is valid only with the validator's `incremental` profile. Matching uses the exact normalized tuple `path + rule + message`; expired or malformed entries block, and stale entries are reported for removal. Baseline configuration errors cannot themselves be baselined.

## Compatibility

- Schema major changes require a migration note.
- New optional fields are backward compatible.
- Renaming a required field or changing its meaning is breaking. `fcvw/plan@2` is therefore explicit rather than silently tightening `fcvw/plan@1`.
- Legacy records are preserved and validated against an explicit baseline.
- New changes must not expand legacy debt.
