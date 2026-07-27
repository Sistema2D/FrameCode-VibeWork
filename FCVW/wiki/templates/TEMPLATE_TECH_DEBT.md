# Template: technical-debt knowledge

```markdown
---
schema: "fcvw/wiki@1"
id: "DEBT-YYYYMMDD-<short-id>"
artifact_role: "record"
owner: "<accountable-owner>"
upgrade_strategy: "preserve"
record_scope: "<application | framework>"
retrieval_scope: "search_only"
title: "Technical Debt card: [Short Description]"
type: "concept"
status: "draft"
confidence: "medium"
created_at: "YYYY-MM-DD"
last_reviewed: "YYYY-MM-DD"
related_version: "Vx.y.z"
sources:
  - "[File link or task where debt was introduced]"
tags:
  - "tech-debt"
---

# Technical Debt: [Description]

## 1. Context & Location
*   **Affected Module/File:** `[Link to code base file]`
*   **Introduction Date:** YYYY-MM-DD
*   **Introduced In Version:** `Vx.y.z`

---

## 2. Debt Classification & Impact

| Severity | Category | Remediation Priority |
|---|---|---|
| `High` / `Medium` / `Low` | `Code smell` / `Architecture` / `Test gap` / `Security` | `P1` (Immediate) to `P5` (Optional) |

### 2.1 Why was this debt introduced?
*   [Provide business justification, time constraints, or design shortcuts taken.]

### 2.2 Expected Impact / Symptoms if Left Unsolved
*   [e.g., Increased fragility in module X, performance hit under high loads.]

---

## 3. Remediation Plan

### 3.1 Proposed Technical Solution
*   [Outline the code or architecture changes required to pay down the debt.]

### 3.2 Refactoring Complexity
*   **Expected Complexity Score:** Low / Moderate / High
*   **Validation Plan:** [Describe how to test the refactoring, e.g., regression check on workflow Y.]

## 4. Authoritative source and follow-up

- [Code, plan, decision, or issue that owns this debt](<relative-path-to-authoritative-source.md>)
```
