# Template: compact change plan

Save as `Plans/pending/P{4,5}-R1-YYYY-MM-DD-<slug>.md` and replace every
placeholder before execution.

Use this form only for an isolated, low-impact change: text, metadata, a label,
a link, a typographic fix, or a local cleanup with no consumer. If the change
touches behavior, data, permission, a public interface, automation, or AI
boundaries, it is not compact — use
[`TEMPLATE_PLAN.md`](TEMPLATE_PLAN.md).

The validator enforces that boundary: a compact plan accepts only `P4` or `P5`
with `R1`, and may not declare `regression_contract`. A plan that needs to waive
a regression contract must argue that waiver in `fcvw/plan@2`.

```markdown
---
schema: "fcvw/plan-compact@1"
id: "P4-R1-YYYY-MM-DD-short-description"
artifact_role: "record"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "pending"
priority: "P4"
risk: "R1"
created_at: "YYYY-MM-DD"
updated_at: "YYYY-MM-DD"
owner: "<human-or-agent-role>"
context_files:
  - "path/to/file"
---

# Short change title

## Objective

<Observable result in one or two sentences.>

## Affected files

- <Exact path.>

## Validation

- [ ] <Command or procedure and expected result.>

## Rollback

<Concrete revert procedure.>

## Related records

- Changelog/framework release: <link>
```

## Escalation rule

If, during execution, the change starts touching existing behavior, a consumer,
persisted data, or a public surface, stop and convert the plan to `fcvw/plan@2`
with a complete regression impact section. Do not widen scope inside the compact
form.

See [`PLANNING.md`](../PLANNING.md) for the plan classes and
[`REGRESSION_GUARDS.md`](../REGRESSION_GUARDS.md) for the blocking conditions.
