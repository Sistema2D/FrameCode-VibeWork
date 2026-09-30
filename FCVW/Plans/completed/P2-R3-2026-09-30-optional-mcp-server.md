---
schema: "fcvw/plan@2"
id: "P2-R3-2026-09-30-optional-mcp-server"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P2"
risk: "R3"
created_at: "2026-09-30"
updated_at: "2026-09-30"
current_version: "V0.21.0"
expected_version: "V0.22.0"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "AGENTS.md"
  - "FCVW/AI.md"
  - "FCVW/SECURITY.md"
  - "FCVW/TESTS.md"
  - "FCVW/ARCHITECTURAL_DECISIONS.md"
  - "FCVW/REGRESSION_GUARDS.md"
category: "optimization"
depends_on: []
---

# Optional read-only MCP server

## Description

Expose FCVW checks to any MCP-capable agent harness through an optional, read-only Model Context Protocol server over stdio, instead of building an own harness.

## Justification and objective

The maintainer asked whether FCVW could become a complete harness. The analysis rejected that (scope, security surface, conflict with ADR-0001, ADR-0010 and ADR-0012) and recommended the smallest step that turns instructions into callable checks: agents can call the route, section, validation, queue and digest tools, so section ranges save tokens when they are actually used.

## Scope

### Included

- `tools/mcp_server_fcvw.py` with five tools: `fcvw_routes`, `fcvw_read_sections`, `fcvw_validate`, `fcvw_next_plan`, `fcvw_digest`.
- `tools/test_mcp_server_fcvw.py`: protocol, tool and boundary tests.
- `AI.md` section, `FCVW/README.md` pointer, [ADR-0013](../../decisions/ADR-0013-optional-mcp-server.md), migration note, V0.22.0 record, `TODO.md` entry.

### Excluded

- Model calls, command execution, file writes, git mutation, network access.
- Harness-specific hooks (Claude Code, Cursor, Codex) until measured.
- Publication of V0.22.0.

## Affected files or boundaries

The two new tool files; `FCVW/AI.md`, `FCVW/README.md`, `FCVW/MIGRATIONS.md`, `FCVW/decisions/ADR-0013-optional-mcp-server.md`, `FCVW/framework-releases/V0.22.0.md`, `TODO.md`, this plan.

## Implementation plan

1. Implement JSON-RPC 2.0 over stdio: `initialize` with version negotiation, `ping`, `tools/list`, `tools/call`; notifications unanswered; malformed input answered with JSON-RPC errors.
2. Wrap existing modules; confine every path to the fixed root.
3. Test protocol, tools and negative boundaries; document and record.

## Proportionality gate

- Real problem and root cause: FCVW rules are only instructions; nothing lets an agent call the checks from its harness.
- Necessary in current scope: requested by the maintainer after the harness analysis.
- Existing codebase solution checked: routes, sections, validator, queue and digests already exist; the server only wraps them.
- Native platform capability checked: MCP over stdio is newline-delimited JSON-RPC; the standard library suffices.
- Installed dependency checked: none added; no MCP SDK.
- New code or complexity justified: one module of about 300 lines and its tests.
- Minimum non-trivial behavior tests: handshake, JSON-RPC errors, path and symlink escape, argument injection into the validator, unknown tool.
- Deliberate simplification and limitations: tools only (no resources or prompts); no hooks; stdio transport only.
- Condition for future evolution: hooks only after the H-05 style measurement shows no token or quality regression.
- Mandatory safeguards preserved: read-only, root-confined, evidence-not-instruction notice, validator run without a shell.

## Acceptance criteria

- [x] An MCP client can initialize, list and call the five tools over stdio.
- [x] Every path argument outside the root, including through a symlink, is refused.
- [x] No tool writes files, mutates git or calls the network.
- [x] Existing tools, routes and validation are unchanged.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

- Retrieval and routing modules imported by the server.
- Installed payload contents (a new optional tool) and the public tool surface.
- AI and security boundaries: a new interface through which agents receive repository content.

### Regression contracts consulted

- `FCVW/AI.md` — retrieved content is evidence, never instruction.
- `FCVW/SECURITY.md` — least privilege and path safety.
- `FCVW/TESTS.md` — AI and agent boundary replay.

### Regression checks required

- [x] Full unit suite and local runner.
- [x] Clean-template validation.
- [x] Negative boundary cases: path escape, absolute path, symlink escape, validator argument injection, unknown tool, malformed JSON.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Server tests | pass | `test_mcp_server_fcvw.py`: 10 tests, including five negative boundary cases |
| Unit suite | pass | `python -B -m unittest discover -s tools -p 'test_*.py'`: 302 tests OK |
| Governance | pass | `validate_fcvw.py --profile clean-template`: 0 findings |
| Local runner | pass | `check_fcvw.py`: tests, governance, benchmark and installed smoke pass |
| Manual protocol replay | pass | stdio session: initialize, tools/list, five tools/call, parse error and unknown method answered correctly |

### Limitations and residual risk

- Not yet exercised inside a real harness session; registration commands follow each client's MCP configuration.
- Tool output can contain repository text, including prompt-like content; the notice marks it as evidence, and the harness keeps its own permission model.

## Validation plan

- [x] `python -B -m unittest discover -s tools -p 'test_*.py'`
- [x] `python -B tools/validate_fcvw.py --root . --profile clean-template`
- [x] `python -B tools/check_fcvw.py`

## Rollback

Unregister the server from the harness, or revert the commit. No data, schema or route changes.

## Gates and approvals

- User authorization: "prossiga" after the harness analysis.
- Regression gate: required and met.
- Release gate: V0.22.0 stays `in_preparation`.

## Related records

- Decision: [ADR-0013](../../decisions/ADR-0013-optional-mcp-server.md).
- Framework release: [V0.22.0](../../framework-releases/V0.22.0.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Suite, governance, local runner | pass | see Regression evidence |

## Gaps and residual risk

- Hooks and a measured activation remain future work.

## Status

`completed`
