# Template: ADR (Architecture Decision Record)

Use this template to record technical decisions that affect the structure of the project. Save as `decisions/ADR-XXXX-<slug>.md`.

```markdown
---
schema: "fcvw/adr@1"
id: "ADR-XXXX"
status: "proposal | accepted | superseded | rejected | obsolete"
date: "YYYY-MM-DD"
artifact_role: "record"
owner: "<accountable-owner>"
upgrade_strategy: "preserve"
record_scope: "<application | framework>"
retrieval_scope: "routed"
---

# ADR-XXXX: <Decision Title>

## Context

<Describe the problem, constraint, or need that motivated the decision.>

## Decision

<Describe the decision made objectively.>

## Alternatives Considered

### Alternative 1
- Description:
- Advantages:
- Disadvantages:

### Alternative 2
- Description:
- Advantages:
- Disadvantages:

## Justification

<Explain why the decision was adopted over the others.>

## Positive Consequences
-

## Negative Consequences
-

## Risks
-

## Impact on Files or Modules
-

## Relationship with Documents
- `PROJECT.md` (identity and scope):
- `PROJECT.md` (stack):
- `PROJECT.md` (workflows):
- `DATA.md`:
- `SECURITY.md`:
- `AI.md`:

## Related Plan
- <Plan name in Plans/>

## Related Changelog
- <Vx.y.z>

## Related ADRs
- <ADR-XXXX>
```
