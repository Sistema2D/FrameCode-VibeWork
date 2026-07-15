---
schema: "fcvw/skill@1"
name: "governance-validator"
description: "Validate FCVW structure, schemas, ownership, states, and clean-template boundaries."
version: "1.2.0"
trigger_keywords:
  - "validate governance"
  - "verify filesystem"
  - "plan state"
  - "validar governança"
  - "context map"
  - "reading trigger"
  - "orphan policy"
  - "integridade do framework"
session_types:
  - "audit"
  - "release"
  - "framework_upgrade"
---

# Governance validator

## Purpose

Evaluate the human-readable FCVW invariants. The optional script automates deterministic checks; this skill owns interpretation and remediation decisions.

## Profiles

- `clean-template`: project-profile placeholders are allowed; application histories and contamination are forbidden.
- `instantiated`: required project profiles must be complete.
- `incremental`: new violations fail; exact legacy baseline findings are reported but do not block.
- `strict`: all applicable findings block.

## Inputs

- `SCHEMAS.md`, `OWNERSHIP.md`, `FRAMEWORK_LOCK.md`;
- physical filesystem;
- active plan and target release;
- optional legacy baseline.

## Checks

1. Canonical files and ownership metadata.
2. Plan status/directory coherence and unique IDs.
3. Skill metadata, catalog coverage, and provider-neutral core instructions.
4. Framework/application version namespace separation.
5. Markdown links and fence balance.
6. Wiki IDs, schema, index, freshness, and archive rules.
7. Placeholder policy by profile.
8. Clean-template contamination.
9. Framework lock, release record, and migration coherence.
10. `FILESYSTEM.md` canonical path/glob coverage.
11. Operational-index and reading-route coverage for every root framework policy, project profile, and declared skill session type.

## Optional execution

`python tools/validate_fcvw.py --root . --profile <profile>`

For controlled legacy debt:

`python tools/validate_fcvw.py --root . --profile incremental --baseline path/to/legacy-baseline.md`

Scripts do not auto-correct historical evidence. Review every proposed remediation and keep the report attached to the active plan or release.

## Non-responsibilities

- application runtime tests;
- legal approval;
- destructive cleanup without a plan;
- hiding legacy findings.

## Required output

List command/profile, passed checks, new failures, reading-route gaps, baseline findings, corrections, and residual risk.

## Validation and exit

Exit only when blocking findings are resolved or explicitly accepted by authorized scope, and no new debt is suppressed as legacy.
