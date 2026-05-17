---
title: "Visual Diff: <screen-or-module-name>"
type: "audit"
status: "draft"
confidence: "high"
last_reviewed: "YYYY-MM-DD"
sources:
  - "mockups/design/<screen-name>.webp"
  - "mockups/actual/<screen-name>.webp"
  - "DESIGN.md"
tags:
  - "visual-diff"
  - "pixel-perfect"
---

# Visual Diff: <Screen or Module Name>

## 1. Screen Reference Maps

- **Design Mockup (Goal):** ![Mockup Target](/mockups/design/<screen-name>.webp)
- **Actual UI (Current):** ![Actual UI](/mockups/actual/<screen-name>.webp)

---

## 2. Pixel Bounding Box Mapping & Comparison

| Element | Bounding Box in Design (px) | Bounding Box in Code (px) | Delta / Drift (px) | Status |
|---|---|---|---|---|
| `<Element Name 1>` | `Top: Ypx, W: Wpx` | `Top: Ypx, W: Wpx` | `0px` |  OK |
| `<Element Name 2>` | `Padding: Ypx` | `Padding: Ypx` | `+Xpx` | ❌ Action Required |

---

## 3. Discrepancy & Action Checklist

Use the checklist below to execute the precise pixel-perfect fixes in the styles file (`tokens.css` or component files):

- [ ] **`<Component-1> Adjustments`:**
  * Target: `<css-selector-1>`
  * Action: `<specific spacing/sizing adjustments in pixels>`
- [ ] **`<Component-2> Adjustments`:**
  * Target: `<css-selector-2>`
  * Action: `<specific spacing/sizing adjustments in pixels>`
