---
schema: "fcvw/adr@1"
id: "ADR-0013"
status: "accepted"
date: "2026-09-30"
artifact_role: "record"
owner: "framework"
upgrade_strategy: "preserve"
record_scope: "framework"
retrieval_scope: "routed"
language: "en-US"
---

# ADR-0013: Optional read-only MCP server instead of an own agent harness

## Context

FCVW governs agents only through instructions: an agent may skip the plan or the mandatory reading, and section ranges save tokens only when the agent actually calls the route tool. Building a complete agent harness (model calls, tool execution, permissions, sandbox, sessions) would contradict [ADR-0001](ADR-0001-pure-markdown-over-automation-scripts.md) and [ADR-0012](ADR-0012-optional-tooling-restored.md), repeat the experiment layer removed by [ADR-0010](ADR-0010-core-reduction.md) and compete with existing harnesses.

## Decision

Ship `tools/mcp_server_fcvw.py`, an optional Model Context Protocol server over stdio built on the standard library. It exposes five read-only tools (routes, section reads, validation, plan queue, digests) that wrap existing modules. The repository root is fixed at start, every path must resolve inside it (symlinks included), nothing is written, no git mutation or network call is made, and results carry the evidence-not-instruction notice. Harness-specific hooks are not shipped.

## Alternatives and consequences

- Complete own harness: rejected for scope, security surface and conflict with the Markdown-first decisions.
- Hooks for one harness in the core: deferred; they are provider-specific and their token and quality effect is unmeasured.
- Consequence: any MCP-capable harness can call FCVW checks; the manual flow is unchanged and the server is never required.

## Compatibility, validation and rollback

Additive tool; no existing command, schema or route changes. Protocol, tool and boundary tests cover handshake, errors, path escape and symlink escape. Rollback: unregister the server from the harness or delete the file.

## Relationships

- [AI governance](../AI.md#optional-mcp-server).
- [Plan](../Plans/completed/P2-R3-2026-09-30-optional-mcp-server.md).
