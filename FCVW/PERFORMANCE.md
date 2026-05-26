---
title: "Performance Budget & Caching Governance"
type: "concept"
status: "validated"
confidence: "high"
last_reviewed: "2026-05-26"
related_version: "V0.6.0"
sources:
  - "STACK.md"
  - "DESIGN.md"
tags:
  - "performance"
  - "budget"
  - "caching"
---

# Performance Budget & Caching Governance

This document establishes official performance limits, network optimization protocols, bundle budget guidelines, and caching policies. It ensures that the application remains extremely fast, lightweight, and responsive.

---

## 1. Objective

Prevent performance degradation and bloated codebases by defining objective technical boundaries. Every human developer and AI agent must validate changes against these budgets before submitting changes.

---

## 2. Core Performance Budgets

The application must operate within these thresholds under realistic conditions (e.g., simulated mobile connections or mid-range machines):

| Metric | Target | Warning Limit | Maximum Budget |
|---|---|---|---|
| **Lighthouse Performance Score** | `> 90` | `< 85` | `80` (Critical) |
| **First Contentful Paint (FCP)** | `< 1.2s` | `> 1.8s` | `2.5s` |
| **Largest Contentful Paint (LCP)** | `< 2.0s` | `> 2.5s` | `3.0s` |
| **First Input Delay (FID)** | `< 50ms` | `> 80ms` | `100ms` |
| **Cumulative Layout Shift (CLS)** | `< 0.05` | `> 0.08` | `0.1` |
| **Total Bundle Size (Gzipped)** | `< 250 KB` | `> 400 KB` | `500 KB` |

---

## 3. UI Optimization Rules

To guarantee visual responsiveness and fluid animations (aligned with `DESIGN.md`):

1. **Lazy Loading:** All visual routes, heavy components, and off-screen images must be lazy-loaded by default.
2. **Layout Shift Protection:** Images and interactive items must declare exact aspect ratios or parent sizes to prevent sudden visual shifts during loading.
3. **No Unoptimized Assets:** Images must be compressed and formatted in modern containers (`.webp`, `.avif`, or vector-based `.svg`), and fonts must be subsetted or preloaded.

---

## 4. API & Caching Standards

To minimize server load and redundant networking:

- **State Caching:** Heavy queries must employ local memory caching, persisting results when applicable (e.g., via `localStorage`, index DBs, or key-value caches).
- **Stale-While-Revalidate (SWR):** Use caching layers that serve stale data instantly while fetching fresh data in the background.
- **Payload Minimization:** API requests and responses must contain only the fields necessary for the active view, avoiding over-fetching.

---

## 5. Build & CI Compliance

- Bundle size analysis must be part of pre-release audits (`AUDIT.md`).
- If a refactoring or feature pushes the bundle size beyond the Warning Limit, the plan must contain a justification and detail optimization steps (such as tree-shaking, code-splitting, or dynamic imports).

---

## 6. AI Agent Validation Checklist

When implementing features or modifying logic, the AI agent must verify:

- [ ] My implementation does not introduce redundant API calls.
- [ ] Visual elements are dynamic, lightweight, and lazy-loaded when off-screen.
- [ ] No heavy external libraries were added without verifying size impact.
- [ ] All elements are aligned with the budget thresholds in Section 2.
