---
context_files:
  - FCVW/REFACTORING.md
  - FCVW/FILESYSTEM.md
  - FCVW/CONTEXT_MAP.md
  - FCVW/skills/README.md
  - FCVW/governance/README_FRAMEWORK.md
  - FCVW/MANIFEST.md
  - FCVW/README.md
  - FCVW/Plans/completed/P3-R2-2026-06-04-integrate-refactoring-guide.md
  - FCVW/changelogs/V0.7.7.md
  - FCVW/refactoring-guide/README.md
  - FCVW/refactoring-guide/MANIFEST.md
  - FCVW/refactoring-guide/20-templates.md
  - FCVW/refactoring-guide/17-branch-and-pull-request-policy.md
  - FCVW/refactoring-guide/12-testing-strategy-before-refactoring.md
  - FCVW/refactoring-guide/11-refactoring-risk-matrix.md
  - FCVW/refactoring-guide/16-dependency-and-impact-map.md
  - FCVW/refactoring-guide/10-code-inventory-and-classification.md
  - FCVW/refactoring-guide/14-rollback-plan.md
  - FCVW/refactoring-guide/15-incremental-refactoring-plan.md
  - FCVW/governance/TEMPLATE_REFACTORING_OPENING.md
  - FCVW/governance/TEMPLATE_REFACTORING_MODULE_INVENTORY.md
  - FCVW/governance/TEMPLATE_REFACTORING_RISK_MATRIX.md
  - FCVW/governance/TEMPLATE_REFACTORING_CHARACTERIZATION_TEST_PLAN.md
  - FCVW/governance/TEMPLATE_REFACTORING_ROLLBACK_PLAN.md
  - FCVW/governance/TEMPLATE_REFACTORING_DEPENDENCY_MAP.md
  - FCVW/governance/TEMPLATE_REFACTORING_INCREMENTAL_PLAN.md
  - FCVW/governance/TEMPLATE_REFACTORING_PULL_REQUEST.md
  - FCVW/governance/TEMPLATE_REFACTORING_POST_VALIDATION_REPORT.md
---
# P3-R2-2026-06-04-integrate-refactoring-guide

- **Description:** Integrate the refactoring governance guide as an official FCVW module and promote applicable templates into `FCVW/governance/`.
- **Justification:** The refactoring guide is currently outside the framework scope; integrating it makes refactoring governance discoverable and standardized without inflating base context.
- **Objective:** A single official refactoring module under FCVW with centralized templates and updated references.
- **Scope:**
  - **Included:** move guide into `FCVW/refactoring-guide`, promote templates into `FCVW/governance`, update references/links, update governance docs and filesystem tree, add changelog evidence, create AICC synthesis.
  - **Excluded:** changes to code behavior, refactoring of application code, changes outside FCVW governance documents.
- **Affected files:**
  - FCVW/REFACTORING.md
  - FCVW/FILESYSTEM.md
  - FCVW/CONTEXT_MAP.md
  - FCVW/skills/README.md
  - FCVW/governance/README_FRAMEWORK.md
  - FCVW/MANIFEST.md
  - FCVW/README.md
  - FCVW/refactoring-guide/* (moved from GUIA REFATORACAO)
  - FCVW/governance/TEMPLATE_REFACTORING_*.md (new)
  - FCVW/changelogs/V0.7.7.md
  - FCVW/wiki/sessions/S{next}-2026-06-04-refactoring-guide-integration.md
  - FCVW/wiki/index.md
  - FCVW/wiki/log.md
- **Implementation plan:**
  1. Move GUIA REFATORACAO to FCVW/refactoring-guide and remove the original folder.
  2. Promote applicable templates to FCVW/governance with ASCII filenames; remove templates from the guide folder.
  3. Update guide references to point to FCVW/governance templates.
  4. Update REFACTORING.md and README to point to the refactoring-guide module.
  5. Update MANIFEST and FILESYSTEM to include the new module and templates.
  6. Create changelog evidence and AICC session synthesis; update wiki index and log.
- **Acceptance criteria:**
  - [x] Refactoring guide lives under FCVW/refactoring-guide with updated references.
  - [x] Applicable templates reside under FCVW/governance and are referenced by the guide.
  - [x] FILESYSTEM tree and MANIFEST reflect the new module.
  - [x] Changelog evidence and session synthesis are created.
- **Test plan:**
  - [x] Manual link spot-check of updated references.
  - [x] Manual verification of folder structure (FILESYSTEM alignment).
- **Priority:** `P3`
- **Risk:** `R2`
- **Current Version:** `V0.7.6`
- **Expected Version:** `V0.7.7`
- **Status:** `completed`
- **Creation Date:** 2026-06-04
- **Completion Date:** 2026-06-04.
- **Technical observations:**
  - `git status --short` fails in this workspace because .git is not present.

## Validation Executed (Fill on completion)

### Environment
- OS: Windows
- Backend/Runtime: Not applicable

### Tests
| Test | Result | Evidence |
|---|---|---|
| Manual link spot-check | Passed | Global link check reports `broken_links=0` after path normalization. |
| Folder structure verification | Passed | `FILESYSTEM.md` regenerated with the current `refactoring-guide/` tree. |

### Final Result
`approved`
