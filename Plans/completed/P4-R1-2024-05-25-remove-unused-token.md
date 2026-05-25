---
type: plan
status: completed
priority: P4
risk: R1
context_files: ["snippets/tokens.css", "AGENTS.md", "VERSIONING.md"]
---

# Remove unused --radius-full CSS token

## Objective

Remove the unused CSS custom property `--radius-full` from `snippets/tokens.css` to improve code maintainability and remove dead code.

## Current Behavior

`snippets/tokens.css` defines `--radius-full: 9999px;` on line 35. A project-wide search confirms this variable is not referenced anywhere in the `snippets/tokens.css` or `snippets/gallery.html` files, nor in any other source file.

## Expected Behavior

`snippets/tokens.css` no longer contains the `--radius-full` variable. The visual appearance and functionality of the application remain completely unchanged.

## Implementation Plan

1. Remove line 35 (`--radius-full: 9999px;`) from `snippets/tokens.css`.
2. Ensure the file remains well-formatted.

## Acceptance Criteria

- The `--radius-full` variable is absent from `snippets/tokens.css`.
- The application (specifically any components relying on `tokens.css`) functions exactly as before.
- A changelog entry is created for this modification in `changelogs/V0.5.2.md`.

## Test Plan

- **Manual Validation:** Run a search to verify `--radius-full` is removed. Check `snippets/gallery.html` or other UI elements using the tokens (if testable) to ensure no visual regressions occur.
- **Linting:** Run CSS linters if available to ensure formatting is correct.
