---
title: "Visual Diff: <screen-or-module-name>"
type: "audit"
status: "draft"
confidence: "high"
last_reviewed: "YYYY-MM-DD"
sources:
  - "DESIGN.md"
  - "runtime screenshot or manually attached evidence"
  - "reference mockup, when the instantiated application owns one"
tags:
  - "visual-diff"
  - "pixel-perfect"
---

# Visual Diff: <Screen or Module Name>

## 1. Screen Reference Evidence

- **Design target:** `<describe token/spec/mockup source without linking to non-existent framework paths>`
- **Actual UI:** `<describe screenshot, browser capture, or manual observation>`
- **Evidence owner:** `<application path, issue, or artifact owner>`

---

## 2. Pixel Bounding Box Mapping and Comparison

| Element | Bounding Box in Design (px) | Bounding Box in Code (px) | Delta / Drift (px) | Status |
|---|---|---|---|---|
| `<Element Name 1>` | `Top: Ypx, W: Wpx` | `Top: Ypx, W: Wpx` | `0px` | OK |
| `<Element Name 2>` | `Padding: Ypx` | `Padding: Ypx` | `+Xpx` | Action Required |

---

## 3. Discrepancy and Action Checklist

Use the checklist below to execute precise visual fixes in the style source owned by the instantiated application:

- [ ] **`<Component-1> Adjustments`:**
  - Target: `<css-selector-1>`
  - Action: `<specific spacing/sizing adjustments in pixels>`
- [ ] **`<Component-2> Adjustments`:**
  - Target: `<css-selector-2>`
  - Action: `<specific spacing/sizing adjustments in pixels>`
