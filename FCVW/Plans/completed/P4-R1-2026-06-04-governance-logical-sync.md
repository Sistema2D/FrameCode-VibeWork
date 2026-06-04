---
title: "P4-R1 Governance Logical Sync"
type: "plan"
status: "completed"
priority: "P4"
risk: "R1"
date: "2026-06-04"
current_version: "V0.7.6"
expected_version: "V0.7.7"
context_files:
  - "FCVW/VERSIONING.md"
  - "FCVW/MANIFEST.md"
  - "FCVW/REFACTORING.md"
  - "FCVW/FILESYSTEM.md"
  - "FCVW/governance/TEMPLATE_VISUAL_DIFF.md"
---

# Plan: Governance Logical Sync

## 1. Motivation
Global analysis V5 identified 4 chronic logical divergences within the governance texts:
1. `VERSIONING.md` ignored the `unreleased/` changelog fragment flow.
2. `VERSIONING.md` lacked the `planned` release state defined in `RELEASE.md`.
3. `TEMPLATE_VISUAL_DIFF.md` survived despite `ADR-0001` deprecating mockups.
4. `MANIFEST.md` and `REFACTORING.md` were blind to the newly integrated modular 20-file `refactoring-guide/`.

## 2. Preserved External Behavior
This is purely a documentation logic fix. There is no change to UI, functional logic, API contracts, or application building.

## 3. Implementation Steps
- Update `VERSIONING.md` to officially require the `unreleased/` fragment and include the `planned` status.
- Update `MANIFEST.md` to list `refactoring-guide/`.
- Update `REFACTORING.md` to point to `refactoring-guide/` and the new 10 templates.
- Delete `governance/TEMPLATE_VISUAL_DIFF.md`.
- Remove `TEMPLATE_VISUAL_DIFF.md` from `FILESYSTEM.md`.

## 4. Acceptance Criteria
- All documents agree on the changelog and release state logic.
- Zombified visual diff template is physically gone.
- Refactoring guide is properly linked in all official meta-docs.

## 5. Rollback Plan
Since this is R1 (pure markdown documentation), rollback consists of reversing the git commit or restoring the old markdown text.

## 6. Test Plan / Validations
- `FILESYSTEM.md` must accurately reflect the deletion.
- Markdown texts must not have broken links.
