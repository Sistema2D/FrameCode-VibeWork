---
title: "🧹 Remove unused CSS variable"
priority: P4
risk: R1
current_version: V0.5.1
expected_version: V0.5.1
status: completed
context_files:
  - "docs/index.html"
---

## Description
Remove unused CSS variable `--chip-translucent` from `docs/index.html` to improve code health and maintainability.

## Implementation Plan
1. Open `docs/index.html`.
2. Delete line 28 containing `--chip-translucent`.

## Acceptance Criteria
- `--chip-translucent` is removed from `docs/index.html`.
- No regressions or layout issues.

## Test Plan
- Visually verify layout of `docs/index.html`.
