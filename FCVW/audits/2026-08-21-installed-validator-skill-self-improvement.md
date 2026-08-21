---
schema: "fcvw/audit@1"
id: "AUD-20260821-installed-validator-skill"
artifact_role: "record"
owner: "framework"
upgrade_strategy: "preserve"
record_scope: "framework"
retrieval_scope: "search_only"
status: "completed"
created_at: "2026-08-21"
last_reviewed: "2026-08-21"
sources:
  - "FCVW/FILESYSTEM.md"
  - "FCVW/skills/governance-validator/SKILL.md"
  - "FCVW/Plans/completed/P2-R4-2026-08-21-single-folder-release-layout.md"
---

# Skill or Agent Self-Improvement: installed governance validator command

## Scope

Patch only the command-location guidance in the existing `governance-validator` skill after release assets moved executable tools under `FCVW/tools/`.

## Authoritative sources

- [Filesystem contract](../FILESYSTEM.md)
- [Release contract](../RELEASE.md)
- [Completed implementation plan](../Plans/completed/P2-R4-2026-08-21-single-folder-release-layout.md)

## Method

Apply `self-improvement` using canonical rule drift, preserve triggers and responsibilities, add the installed command first, retain the source-checkout alternative, and replay both layouts.

## Findings

- Evidence: the prior skill exposed only `python tools/validate_fcvw.py`, which is absent from the contained installed layout.
- Metric passed: rule drift and validation gap.
- Scope preservation: command selection remains inside the same validator responsibility; no trigger or provider dependency changes.
- Backward compatibility: the source-checkout command remains documented.

## Validation

Both commands were replayed: the source validator and the materialized installed validator each reported errors=0/findings=0. The skill contract passed in the full 92-test suite, and the installed document graph reported zero findings.

## Limitations and residual risk

Historical releases still use root `tools/`; the skill therefore documents both physical layouts instead of inferring one command universally.

## Follow-up

Revisit only if another supported distribution layout is introduced.
