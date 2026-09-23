---
schema: "fcvw/adr@1"
id: "ADR-0009"
status: "accepted"
date: "2026-09-23"
artifact_role: "record"
owner: "framework"
upgrade_strategy: "preserve"
record_scope: "framework"
retrieval_scope: "routed"
language: "en-US"
---

# ADR-0009: Adaptive capability without automatic promotion

## Context

The user requested implementing and closing remaining issues 55, 56 and 57. The
issue-55 tools and initial pilot exist, but that pilot does not demonstrate causal
benefit or satisfy live activation requirements. Missing data cannot be supplied
by a synthetic safety test or inferred from issue closure.

## Decision

Implement small optional modules for evidence screening, explicit human feedback,
bounded replay, runtime stop latches and opt-in retrieval. Reuse loop metrics,
structural scoring and complete-chunk selection. Default and legacy shadow behavior
stay intact. Separate disabled, shadow, limited and operational authority; ship no
approved control, learned weights, application data or model executor.

Weights are a bounded chunk adjustment, not a neural network, rewritten edge graph,
policy update or automatic reward. Source/index digests and a replayed feedback
ledger constrain derived state. QA/safety stops remain blocking after rollback.
Explicit review and trusted operational handling are still required: hashes are
integrity checks, not signatures or proof of independent reviewers.

## Alternatives and consequences

Reject a second execution framework, always-on collection, paid model experiments
and automatic promotion. Pure documentation would not exercise recovery or selection
boundaries; the optional CLI makes them testable locally. Synthetic replay establishes
technical behavior only. Operational efficacy remains unproven, and current pilot
evidence continues to reject activation. Decline promotion rather than invent data.

Source hashing, evidence replay and structural scoring cost extra only when the
explicit experimental control is supplied. No default retrieval state scan is added.
Operators serialize runtime updates and own the latest-state pointer; no database,
distributed lock, tamper-proof audit service or authoritative identity provider exists.

## Compatibility, validation and rollback

Additive CLI flags and JSON contracts. Existing commands and schemas remain readable.
Use [the contract](../governance/ADAPTIVE_EXPERIMENT_CONTRACT.md) and
[implementation plan](../Plans/completed/P2-R4-2026-09-23-adaptive-controls.md)
for tests, negative pilot evidence and residual risks. Disable assistance, retain
stop evidence, and restore or reset explicit state. Revalidate before reactivation.

## Relationships

[ADR-0006](ADR-0006-adaptive-context-routing.md) describes the original shadow-only
baseline; this decision adds gated optional behavior rather than rewriting its history.
[ADR-0008](ADR-0008-loop-evaluation.md) owns metric/provenance semantics.
[V0.19.0](../framework-releases/V0.19.0.md) remains in preparation.
