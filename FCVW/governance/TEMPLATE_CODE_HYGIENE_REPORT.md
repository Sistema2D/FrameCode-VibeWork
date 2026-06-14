# Template: Code Hygiene Report

Save in the active plan, `audits/`, or `wiki/refactorings/` depending on scope. Use this before broad cleanup, retroactive instantiation cleanup, or refactoring of duplicated/monolithic areas.

```markdown
# Code Hygiene Report: <target area>

## Metadata

- **Date:** YYYY-MM-DD
- **Related plan:** `<Plans/...>`
- **Skill loaded:** `skills/code-hygiene-refactor/SKILL.md`
- **Scan level:** `local` / `module` / `systemic`
- **Target area:** `<folder, module, feature, service, or workflow>`
- **Behavior to preserve:** `<observable behavior>`

## Inventory

| Path | Role | Owner | Risk | Tests/validation | Notes |
|---|---|---|---|---|---|
| `<path>` | `<role>` | `<owner>` | `R1-R5` | `<tests>` | `<notes>` |

## Findings

| Finding | Path | Evidence | Action | Status |
|---|---|---|---|---|
| `duplicate` / `large-file` / `dead-code` / `stale-file` / `catch-all` | `<path>` | `<search/test/manual evidence>` | `<extract/remove/defer/split>` | `open` / `done` / `deferred` |

## Selected Cleanup Batch

- **Batch scope:** `<smallest reversible unit>`
- **Why this batch first:** `<impact and risk>`
- **Files changed:** `<paths>`
- **Rollback:** `<git revert or manual rollback>`

## Validation

| Check | Result | Evidence |
|---|---|---|
| `<check>` | `passed` / `failed` / `not run` | `<stdout, manual note, or limitation>` |

## Deferred Debt

- `<debt item, reason, follow-up plan or wiki card>`
```
