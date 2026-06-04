---
status: completed
priority: P3
risk: R2
current_version: "V0.7.6"
expected_version: "V0.7.7"
---

# P3-R2-2026-06-04-translate-refactoring-guide

## Status
`completed`

## Goal
Translate all 23 markdown files inside `FCVW/refactoring-guide/` from Portuguese to English to match the framework's internationalization standard. Standardize file names and content using Martin Fowler's "Refactoring" terminology.

## Execution
- Delegated the workload to 5 concurrent AI subagents to translate files in batches.
- Subagents outputted files to a temporary workspace.
- Replaced the official `FCVW/refactoring-guide/` directory with the 23 fully translated English files.

## Changes
- Renamed and translated `00-governanca-geral.md` to `00-general-governance.md`
- Renamed and translated `01-guia-decisao.md` to `01-decision-guide.md`
- ... and 21 other files.
- Replaced the directory wholesale.

## Acceptance Criteria
- Refactoring guide filenames and content use English consistently.
- Internal links point to the current English filenames.
- Tables, headers, and lists remain valid Markdown.

## Test Plan / Validation
- Manual verification of directory contents. All 23 files are present and contain English markdown.
- Formatting, headers, lists, and tables preserved.
