---
schema: "fcvw/plan@2"
id: "P3-R2-2026-09-30-mcp-field-test-fixes"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P3"
risk: "R2"
created_at: "2026-09-30"
updated_at: "2026-09-30"
current_version: "V0.21.0"
expected_version: "V0.22.0"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "FCVW/CONTEXT_MAP.md"
  - "FCVW/AI.md"
  - "FCVW/PROJECT.md"
  - "FCVW/REGRESSION_GUARDS.md"
category: "correction"
depends_on: []
---

# Fixes from the first MCP field test

## Description

Correct four problems found when a real Claude Code session used the MCP server on a freshly instantiated project.

## Justification and objective

In the field test the agent spent two failed calls on `fcvw_routes` (a versioned change needs an event; it guessed `public-interface`), received repeated text from `fcvw_read_sections` when it asked for a section and its subsections, reached `APP_RULES.md` only by reading the map's cross-cutting section, and the project template still named V0.13.0.

## Scope

### Included

- `fcvw_routes` schema lists the session and event names from `CONTEXT_MAP.md` and states that a versioned change needs an event.
- `fcvw_read_sections` skips a requested section already inside another requested one.
- Routes add `FCVW/APP_RULES.md` when application files change and the rules are `complete`; `CONTEXT_MAP.md` says so.
- `PROJECT.md` governance layer points to `FRAMEWORK_LOCK.md` instead of a stale version.

### Excluded

- Hooks and further tools.

## Affected files or boundaries

`tools/mcp_server_fcvw.py`, `tools/context_routing_fcvw.py`, `tools/test_mcp_server_fcvw.py`, `FCVW/CONTEXT_MAP.md`, `FCVW/PROJECT.md`, `FCVW/MIGRATIONS.md`, the V0.22.0 record and this plan.

## Implementation plan

1. Build the tool list per repository from `route_tables`.
2. Deduplicate nested sections.
3. Add the rules route for instantiated application changes.
4. Fix the template line; test; rerun the field session.

## Proportionality gate

Not applicable — four local corrections inside existing modules; no new dependency or abstraction.

## Acceptance criteria

- [x] `tools/list` shows accepted sessions and events for `fcvw_routes`.
- [x] Nested sections appear once.
- [x] `APP_RULES.md` joins the route only for application files in a project whose rules are `complete`.
- [x] The template no longer names a framework version.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

- Mandatory routes for application changes in instantiated projects (one more file, by design).
- Tool schemas seen by MCP clients.
- Section reads.

### Regression contracts consulted

- `FCVW/CONTEXT_MAP.md` — cross-cutting application-rule trigger; mandatory routes are cumulative.
- `FCVW/REGRESSION_GUARDS.md` — preservation evidence.

### Regression checks required

- [x] Clean-template routes unchanged (rules still `pending`).
- [x] Full suite and local runner.
- [x] Field session rerun on the test project.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| New tests | pass | `test_mcp_server_fcvw.py`: 13 tests (enum list, nested sections, rules route pending/complete/framework-only) |
| Full suite and local runner | pass | `check_fcvw.py`: tests, governance, benchmark and installed smoke pass |
| Field session | pass | see Validation executed |

### Limitations and residual risk

- One field session is anecdotal evidence, not the measured gate of TODO H-05.

## Validation plan

- [x] `python -B tools/check_fcvw.py`
- [x] Rerun the same headless Claude Code session on the test project.

## Rollback

Revert the commit; routes and schemas return to V0.22.0-before-fix behaviour.

## Gates and approvals

- User authorization: request to fix the four findings and rerun the session.

## Related records

- Framework release: [V0.22.0](../../framework-releases/V0.22.0.md).
- Server plan: [optional MCP server](P2-R3-2026-09-30-optional-mcp-server.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Suite, governance, local runner | pass | see Regression evidence |
| Field session rerun | pass | Same headless Claude Code prompt on the same test project, before → after: failed tool calls 2 → 0; FCVW tool calls 12 → 9; turns 14 → 11; tool output 25.5 → 21.5 KB; cost US$0.19 → US$0.11. `APP_RULES.md` came from the route; the agent did not reopen `CONTEXT_MAP.md`. One run each: indicative, not the H-05 gate |

## Gaps and residual risk

None beyond the limitation above.

## Status

`completed`
