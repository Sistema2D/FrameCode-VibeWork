---
schema: "fcvw/skill@1"
name: "code-hygiene-refactor"
description: "Select a bounded, behavior-preserving code-hygiene batch."
version: "1.1.1"
trigger_keywords:
  - "code hygiene"
  - "duplication"
  - "dead code"
  - "higiene de código"
session_types:
  - "refactoring"
  - "audit"
---
# SKILL: Code Hygiene Refactor

## Purpose

Drive active cleanup of duplication, stale files, unnecessary code, oversized modules, and retroactive technical debt while preserving behavior. This skill is a Markdown-only operational tool: it tells the agent what to inspect, what to block, and what evidence to record.

## Activation Triggers

Load this skill when:

- a user reports duplication, monoliths, repeated snippets, stale files, unnecessary files, dead code, technical debt, cleanup, or the Portuguese equivalents: higiene de código, limpeza, duplicação, código duplicado, arquivo obsoleto, arquivo morto, código morto, refatoração, dívida técnica, monolito, or sobras de implementação;
- retroactive instantiation is applied to an existing project;
- a file is large, low-cohesion, or repeatedly changed;
- a plan touches code with known `#tech-debt`;
- an agent is tempted to copy/paste similar code;
- a cleanup/refactoring plan is opened.

## Inputs

Active plan and scope, changed-path and ownership evidence, similar-code search, dependency/consumer references, focused behavior checks, and rollback or restoration source for removals.

## Non-Negotiable Rules

- Preserve observable behavior unless a separate functional plan exists.
- Do not remove dead code without evidence from search, tests, owners, routes, or build behavior.
- Do not combine broad cleanup with a feature delivery unless the cleanup is required to keep the feature small.
- Do not introduce new dependencies for cleanup without explicit research and plan approval.
- Prefer extracting existing repeated logic over inventing generic abstractions.
- Keep each cleanup batch reviewable and reversible.

## Hygiene Scan

Use the smallest scan compatible with the risk:

| Scan | Use when | Evidence |
|---|---|---|
| Local | One file or one function is changing. | Similar-code search, direct callers, before/after behavior. |
| Module | A component, route, service, prompt pack, or folder is changing. | Inventory table, imports/callers, tests, duplication candidates. |
| Systemic | Multiple modules, legacy migration, or retroactive adoption. | Dependency/impact map, phased plan, rollback, characterization tests. |

## Findings Matrix

Classify each finding before editing:

| Finding | Required action |
|---|---|
| Duplicate code | Extract only when the shared rule is truly identical; otherwise document intentional variation. |
| Large file | Load `anti-monolith-guard`; split by responsibility before adding behavior. |
| Dead code | Mark `CANDIDATE_FOR_REMOVAL`; remove only after validation. |
| Stale file | Mark authoritative source and obsolete copy; remove only inside a plan. |
| Catch-all utility | Split by domain capability or keep scoped with explicit owner. |
| Repeated prompt | Move stable prompt rule to versioned AI/resource doc; keep context examples separate. |
| Missing tests | Add characterization or manual validation before structural change. |
| Hidden dependency | Make dependency explicit or document order/contract before moving code. |

## Cleanup Sequence

1. Inventory the target area.
2. Identify duplicates, large files, stale files, dead code, and catch-all modules.
3. Rank findings by risk and user impact.
4. Choose one small cleanup batch.
5. Characterize current behavior.
6. Apply the smallest extraction, deletion, move, or rename.
7. Validate behavior.
8. Record result in plan, changelog, and wiki if reusable.

## Output Required

Create or fill a report using `governance/TEMPLATE_CODE_HYGIENE_REPORT.md` when the scan is module-level or systemic. For local scans, add this compact block to the active plan:

```markdown
## Code Hygiene Scan

- Skill loaded: `skills/code-hygiene-refactor/SKILL.md`
- Scan level: `local` / `module` / `systemic`
- Duplicate candidates:
- Large/monolithic candidates:
- Dead/stale candidates:
- Cleanup batch selected:
- Behavior preservation evidence:
- Deferred debt:
```

## Exit Criteria

The cleanup is complete only when duplication, monolith risk, stale files, or dead code were reduced or explicitly deferred with evidence and a follow-up plan.
