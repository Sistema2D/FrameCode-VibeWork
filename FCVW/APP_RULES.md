---
schema: "fcvw/app-rules@1"
artifact_role: "project_profile"
owner: "project"
upgrade_strategy: "preserve"
instantiation_status: "pending"
retrieval_scope: "always"
---

# Application-specific rules

This project-owned profile records cross-cutting business rules, operational constraints, permissions, synchronization requirements, and deliberate application exceptions. It complements framework policy and does not replace scope, architecture, plans, ADRs, API documentation, tests, or necessary code comments.

## Consultation rule

Consult this file before changing observable application behavior, workflows, data, permissions, interface conventions, or dependencies between modules. Add or update a rule when implementation or audit evidence reveals a durable application-specific constraint.

## Rule index

No application rules have been instantiated.

## Rule template

Copy this structure only when a real rule is known:

```markdown
## APP-RULE-001 — Short title

### Status

active | deprecated | superseded

### Rule

Observable requirement or constraint.

### Affected components

- [Affected module](../path/to/module)

### Rationale and expected behavior

Why the rule exists and what must remain true.

### Exceptions

Known exception, authority, and expiry; or `None`.

### Related records

- [Plan](Plans/in_progress/example.md)
- [Decision](decisions/example.md)
```

## Maintenance

- IDs are unique and stable.
- Changed rules retain traceability through related plans or decisions.
- Removed rules become `deprecated` or `superseded`; do not erase historical evidence silently.
- If growth or merge conflicts justify decomposition, this file remains the canonical index and links domain-specific rule files.
