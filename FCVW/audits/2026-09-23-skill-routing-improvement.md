---
schema: "fcvw/audit@1"
id: "AUD-20260923-skill-routing-improvement"
artifact_role: "record"
record_scope: "framework"
owner: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "search_only"
status: "completed"
created_at: "2026-09-23"
last_reviewed: "2026-09-23"
sources:
  - "FCVW/CONTEXT_MAP.md"
  - "FCVW/skills/QA/SKILL.md"
  - "FCVW/skills/orchestrator/SKILL.md"
  - "FCVW/Plans/completed/P2-R4-2026-09-23-audit-remediation.md"
---

# Skill and agent self-improvement: QA and orchestrator

## Scope

- Assets: [QA](../skills/QA/SKILL.md), [orchestrator](../skills/orchestrator/SKILL.md) and the [context map](../CONTEXT_MAP.md).
- The [audit remediation plan](../Plans/completed/P2-R4-2026-09-23-audit-remediation.md) records a blocked initial QA inventory rejected by the optional checker, mixed QA/UI/wiki trigger ambiguity and an orchestrator trigger that included any multi-domain or R3+ plan.
- Severity: medium; the QA checkpoint defect was directly reproduced.

## Authoritative sources

- [QA skill](../skills/QA/SKILL.md), [orchestrator skill](../skills/orchestrator/SKILL.md), [context map](../CONTEXT_MAP.md), and the [remediation plan](../Plans/completed/P2-R4-2026-09-23-audit-remediation.md).

## Method

Reproduced the initial QA checkpoint failure, inspected routing rules, changed the checker and skill triggers, and replayed focused regressions. Claims about actual host execution require separate evidence.

## Findings

| Metric | Evidence | Decision |
|---|---|---|
| Validation gap | All-blocked first-run inventory raised `ValueError` despite the skill requiring an in-progress checkpoint. | fixed |
| Scope preservation | QA remains product-behavior owner; the orchestrator now delegates only independent authorized scopes. | retained |
| Backward compatibility | Existing QA targets and explicit multi-agent triggers remain valid; no mandatory new adapter. | retained |
| Token ROI | Fewer adjacent skills and delegated work packages should load for mixed requests; no numeric savings claimed. | unmeasured |

## Validation

The integrated Windows/Python 3.14 runner passed 305 source tests (one symlink test skipped), clean-template governance, the labeled retrieval benchmark and installed smoke tests; its source snapshot was unchanged. Focused QA and routing regressions are included in that suite.

## Limitations and residual risk

Actual agent activation, product-host coverage, and token savings have not been measured. The checker only verifies the structure and provenance of submitted QA records.

## Follow-up

The [skills catalog](../skills/README.md) retains the existing responsibilities; the [context map](../CONTEXT_MAP.md) resolves mixed-task precedence. The plan and [V0.19.0 preparation record](../framework-releases/V0.19.0.md) track validation and remaining limits.
