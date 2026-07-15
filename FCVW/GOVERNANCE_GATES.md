---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Governance gates

| Gate | Trigger | Minimum evidence | Blocking condition |
|---|---|---|---|
| Plan | versioned change | active plan and scope | no plan or wrong state |
| Regression | functional, visual, data, AI, security, refactoring, workflow, interface, operation, or documentation change | Regression impact, consulted contracts, protected-behavior replay, limitations, residual risk, rollback status | missing/generic/pending evidence, insufficient risk coverage, hidden known regression, or unapproved rollback gap |
| Security | auth, secrets, sensitive data, permissions | threat/misuse analysis and tests | unmitigated critical risk |
| Data | schema, migration, import/export, deletion | rehearsal and reconciliation | no backup/rollback for R4/R5 |
| Refactoring | behavior-preserving structural work | characterization and regression tests | mixed rewrite/refactor without split |
| Skill creation | new reusable AI procedure | recurrence and ownership gap | existing skill already owns it |
| Skill improvement | existing AI procedure changes | evidence and replay | scope expansion without factory review |
| Release | version/publication | completed plans, validation, rollback | unresolved applicable P1/P2 |
| Framework upgrade | FCVW baseline change | ownership map, migration, clean validation | project history overwrite risk |

Outcomes are `pass`, `warn`, or `block`. A bypass records authority, justification, expiry, residual risk, and follow-up. Silence is not a pass.

Use `governance/TEMPLATE_GOVERNANCE_GATE_REPORT.md`.

The Regression gate is evaluated before plan completion. See `REGRESSION_GUARDS.md` for bypass requirements and confirmed-regression handling.
