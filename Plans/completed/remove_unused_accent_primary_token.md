---
status: completed
priority: P4
risk: R4
context_files:
  - snippets/tokens.css
current_version: "V0.5.1"
expected_version: "V0.5.1"
---

# Plan: Remove Unused `--accent-primary` Token

## Scope
Remove the unused CSS variable `--accent-primary` from `snippets/tokens.css`.

## Acceptance Criteria
- `--accent-primary` is no longer in `snippets/tokens.css`.
- The token is not referenced in the project.

## Test Plan
- Run `grep -r "--accent-primary" snippets/` to ensure no usages exist.

## Validation
- `grep -r -e "--accent-primary" snippets/` returned no results.
- `snippets/tokens.css` was manually inspected.
- The framework is a document-based governance framework. No automated tests exist to run.
