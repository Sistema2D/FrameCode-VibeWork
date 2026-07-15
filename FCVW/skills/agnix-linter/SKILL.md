---
schema: "fcvw/skill@1"
name: "agnix-linter"
description: "Markdown and governance structure lint checklist."
version: "1.2.0"
trigger_keywords:
  - "governance lint"
  - "dead links"
  - "markdown audit"
  - "auditoria estrutural"
session_types:
  - "audit"
  - "release"
---

# Governance and Markdown linter

## Purpose

Detect structural defects, dead references, schema drift, and contradictory governance instructions without silently changing policy.

## Use conditions

Use during governance audits, framework maintenance, release closeout, or after moving and renaming documentation.

## Non-responsibilities

- deciding product policy or resolving a governance conflict without authorization;
- rewriting historical evidence to make validation pass;
- claiming semantic correctness from syntax checks alone;
- modifying versioned files without a plan and changelog.

## Inputs

`AGENTS.md`, the context map, schema and ownership documents, affected Markdown, skill catalog, record indexes, and any explicit legacy baseline.

## Procedure

1. Select clean-template, instantiated, incremental, or strict validation scope.
2. Check internal links, Markdown fences, required paths, schemas, IDs, lifecycle directories, and version namespaces.
3. Compare global instructions with narrower policies and skills for direct contradictions.
4. Distinguish new defects from accepted legacy debt.
5. Report exact file and rule for every finding.
6. Apply only authorized, plan-scoped corrections and rerun the same checks.

## Required output

Validation profile, checks executed, pass/fail result, actionable findings with paths, accepted baseline items, fixes made, and residual risks.

## Validation

Every reported path exists, each finding is reproducible, duplicate reports are consolidated, and the same lint scope passes after an authorized correction.

## Exit criteria

Exit when the chosen profile passes or each remaining finding has an explicit owner, reason, and follow-up path.
