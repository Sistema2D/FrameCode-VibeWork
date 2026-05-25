---
type: plan
status: completed
priority: P4
risk: R1
context_files: ["snippets/tokens.css", "AGENTS.md", "VERSIONING.md"]
---

# P4-R1-2024-05-25-remove-unused-token

## Description

Remove the unused CSS custom property `--radius-full` from `snippets/tokens.css`.

## Justification

`snippets/tokens.css` defined `--radius-full: 9999px;`, and a project-wide search confirmed the token was not referenced in `snippets/tokens.css`, `snippets/gallery.html`, or other source files. Removing the unused token improves maintainability and reduces dead code without affecting behavior.

## Scope

- Remove `--radius-full: 9999px;` from `snippets/tokens.css`.
- Keep formatting intact.
- Record the change in `changelogs/V0.5.2.md`.
- No functional or visual behavior changes are intended.

## Current Version

V0.5.1

## Expected Version

V0.5.2

## Creation Date

2024-05-25

## Completion Date

2024-05-25

## Implementation

1. Remove `--radius-full: 9999px;` from `snippets/tokens.css`.
2. Ensure the file remains well-formatted.
3. Add the corresponding changelog entry in `changelogs/V0.5.2.md`.

## Validation / Results

- Confirmed `--radius-full` was unused before removal via project-wide search.
- Verified the token is absent from `snippets/tokens.css` after the change.
- Reviewed impacted token consumers, including `snippets/gallery.html`, and found no required updates.
- No visual or functional regressions were expected because the token had no references.
- CSS formatting remains intact after the edit.

## Outcome

Completed as planned. The unused `--radius-full` token was removed, the change was intended to ship in `V0.5.2`, and no behavior changes were introduced.
