---
schema: "fcvw/adr@1"
id: "ADR-0014"
status: "accepted"
date: "2026-09-30"
artifact_role: "record"
owner: "framework"
upgrade_strategy: "preserve"
record_scope: "framework"
retrieval_scope: "routed"
language: "en-US"
---

# ADR-0014: Opt-in harness hooks for Claude Code and Codex

## Context

[ADR-0013](ADR-0013-optional-mcp-server.md) shipped callable checks but deferred hooks until measured. Claude Code and Codex share the hook protocol parts FCVW needs: JSON on stdin, `additionalContext` on SessionStart, `permissionDecision: "deny"` on PreToolUse, and exit code 2 with stderr to keep a Stop from ending. Codex names file edits `apply_patch` and passes the patch text as `tool_input.command`.

## Decision

Ship `tools/hook_fcvw.py` with three hooks (session start status, pre-edit plan check, stop validation) and document the configuration of both harnesses in [AUTOMATION.md](../AUTOMATION.md#agent-harness-hooks-optional-scenario-2). The hooks are Scenario 2: a project enables them by adding the configuration and an `fcvw/automation@1` contract with `authorized_by`. They are never enabled by installing FCVW.

## Evidence

Headless Claude Code on an instantiated test project, two runs per condition. A first version blocked closeout edits after the plan moved to `completed/`; allowing plans completed in uncommitted work removed every denial. With the task naming FCVW, cost matched runs without hooks (US$0.39 against US$0.37). Without naming it, hooks kept the plan before the code in 2 of 2 runs against 1 of 2, for about 27% more cost. Every final state passed tests and validation.

## Alternatives and consequences

- Enable by default: rejected; cost rises when the agent would otherwise skip governance, and the sample is small.
- Inspect shell commands: rejected; parsing arbitrary shells is unreliable, so shell edits escape `pre-edit` (documented).
- Consequence: projects that want enforcement opt in; the manual flow and the MCP server are unchanged.

## Compatibility, validation and rollback

Additive tool. Tests cover Claude Code and Codex payloads, ignored and outside paths, closeout edits, the disable switch and the stop cycle. Rollback: `FCVW_HOOKS=off`, remove the harness configuration, or retire the contract.

## Relationships

- [Plan](../Plans/completed/P2-R3-2026-09-30-harness-hooks.md).
- [Declarative automation](../AUTOMATION.md).
