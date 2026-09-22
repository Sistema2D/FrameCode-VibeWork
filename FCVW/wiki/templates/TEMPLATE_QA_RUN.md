# Template: QA execution

Follow the [product contract](../product/README.md).

Use one unique application-owned run per bounded execution. Existing passing evidence must not be relabeled after the behavior contract changes.

```markdown
---
schema: "fcvw/wiki@1"
id: "QA-YYYYMMDD-unique"
artifact_role: "record"
record_scope: "application"
owner: "QA"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
title: "<bounded QA run>"
type: "audit"
qa_run: "true"
status: "draft"
confidence: "medium"
created_at: "YYYY-MM-DD"
last_reviewed: "YYYY-MM-DD"
app_revision: "<tested build or commit>"
environment: "<authorized URL/environment without secrets>"
runtime: "<OS, execution tool/harness and version; browser or board/simulator when applicable>"
roles: "<roles tested>"
observed_at: "YYYY-MM-DDTHH:MM:SS+00:00"
sources:
  - "<selected surface page>"
tags:
  - "quality-validation"
---

# QA run

## Scope and conditions

Record target, roles, target platform, applicable viewport/device conditions, test data, allowed side effects, tool capabilities, case boundaries and cleanup. Report unavailable tools/access; never substitute source inspection for live execution. Identify simulation, mocks and physical execution separately, including untested boundaries.

## Contracts

| surface_id | sha256 |
|---|---|
| UI-profile | <hash returned by the selected-page checker> |

## Results

| surface_id | case_id | result | observed | evidence |
|---|---|---|---|---|
| UI-profile | save-valid | not_run | Application not accessed yet | - |

## Evidence and discrepancies

Link replay steps, screenshots or traces sufficient to support observed results. Redact sensitive data. Results may be pass, fail, blocked or not_run. Unknown/provisional expectations cannot pass. Add a reproducible defect with expected/actual difference and affected case; product repairs require a separate authorized plan.

## Coverage and handoff

List tested, failed, blocked, not-run and undiscovered scope separately. Identify follow-up owner and exact next step. Link relevant product pages and the inventory. No claim of universal coverage follows from a passing selected subset.
```
