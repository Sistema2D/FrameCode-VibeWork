# Plan: Mandatory Third-Party Service Research Before Recommendation

## Status

`completed`

## Priority / Risk

`P1-R4` => impact_weight 5 x risk_weight 4 = 20

## Gates

- **Review gate**: Required (R4) — passed
- **Rollback required**: No (documentation changes only)
- **Decomposition required**: No (single logical change)

## Current Version

`V0.8.0`

## Expected Version

`V0.8.0` (patch — documentation only)

## Motivation

**GAP-1.3 identified in hypothesis test**: The framework had no rule requiring AI agents to research third-party developer services before recommending or integrating them.

## Scope

- `AGENTS.md` — add operational rule
- `FCVW/AI.md` — add new section "Third-Party Service Research"

## Acceptance Criteria

1. ✅ `AGENTS.md` contains an operational rule stating that third-party services must be researched before recommendation.
2. ✅ `FCVW/AI.md` contains a section defining research requirements, prohibited behaviors, integration protocol, and exceptions.
3. ✅ All existing references are consistent with the new rule.

## Implementation Summary

- `AGENTS.md`: Added "Third-Party Services" operational rule + Initial Checklist item
- `FCVW/AI.md`: Added "Third-Party Service Research" section (mandatory research, prohibited behaviors, integration protocol, exceptions)

## Validation

- Code review: passed (3 review cycles, all issues resolved)
- Consistency: AGENTS.md → AI.md cross-reference verified
- Changelog: `changelogs/unreleased/P1-R4-2026-06-11-service-research-mandate.md` created

## Stale Files

Stale copies exist at: `FCVW/Plans/pending/P1-R4-2026-06-11-service-research-mandate.md`, `FCVW/Plans/in_progress/P1-R4-2026-06-11-service-research-mandate.md`. This file is the authoritative completed version.
