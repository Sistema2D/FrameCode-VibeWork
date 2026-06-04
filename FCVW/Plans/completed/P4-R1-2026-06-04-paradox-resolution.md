---
title: "P4-R1 Paradox Resolution"
type: "plan"
status: "completed"
priority: "P4"
risk: "R1"
date: "2026-06-04"
current_version: "V0.7.6"
expected_version: "V0.7.7"
context_files:
  - "FCVW/AUDIT.md"
  - "FCVW/AI.md"
  - "FCVW/FILESYSTEM.md"
  - "FCVW/wiki/templates/TEMPLATE_SESSION_SYNTHESIS.md"
---

# Plan: Paradox Resolution

## 1. Motivation
Global analysis V6 identified 3 new logical paradoxes in the repository:
1. `AUDIT.md` instructed audits to be placed at the application root, contradicting the `FCVW/` isolation rule.
2. `AI.md` offered two competing templates for session synthesis (one in governance, one in wiki).
3. `FILESYSTEM.md` and `DATA.md` needed to clarify that database folders are downstream-project concerns, not baseline framework state.

## 2. Preserved External Behavior
This is a purely documentary and structural integrity fix. The core application logic and public API remain untouched.

## 3. Implementation Steps
- Update `AUDIT.md` to point audits to `FCVW/audits/`.
- Update `AI.md` to point strictly to `wiki/templates/TEMPLATE_SESSION_SYNTHESIS.md`.
- Delete the redundant `FCVW/governance/TEMPLATE_AI_SESSION_SYNTHESIS.md`.
- Update the filesystem/data documentation to avoid declaring a baseline `FCVW/data/` subtree.

## 4. Acceptance Criteria
- Contradictory instructions removed.
- Physical single source of truth for templates.
- Filesystem accurately reflects the framework baseline without a runtime data layer.

## 5. Rollback Plan
Since this is R1 (pure markdown documentation), rollback consists of reversing the git commit or restoring the old markdown text.

## 6. Test Plan / Validations
- `FILESYSTEM.md` must accurately reflect the baseline structure and removed redundant template.
- Markdown texts must not have broken links.
