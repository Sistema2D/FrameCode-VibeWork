---
schema: "fcvw/adr@1"
id: "ADR-0008"
status: "accepted"
date: "2026-09-22"
artifact_role: "record"
owner: "framework"
upgrade_strategy: "preserve"
record_scope: "framework"
retrieval_scope: "routed"
language: "en-US"
---

# ADR-0008: Explicit local loop evidence

## Context

Issue 55 expands retrieval evaluation to validated task completion. The existing
benchmark has one caller-supplied outcome per case; it cannot represent distinct
repetitions, resumed checkpoints, partial token usage or later regression evidence.
The user requested implementation and creation of an initial dataset because none
was supplied. That instruction does not make author labels independent review or
turn deterministic tests into measured model executions.

## Decision and alternatives

Keep the retrieval benchmark unchanged. Add an opt-in standard-library aggregator,
a small strict input-contract module, and a frozen protocol/run template. Reuse
retrieval scoring rather than creating another ranking system. A background
collector, provider SDK, model runner or learning subsystem is unnecessary and would
expand cost/privacy boundaries. Generated reports are evidence, never policy.

Deduplicate exact resumed events and reject conflicting evidence. Preserve all
started/planned runs, incomplete outcomes, source identities, QA decision gates and
the distinction between shadow proposals and actual delivery. Provider counts,
tokenizer counts and estimates remain separate. Input references are inert and
unknown raw-payload fields fail. Outputs are external or disposable cache.

## Consequences and limits

The tool can establish structural consistency and compute declared metrics, not
attest truth, reviewer independence or causal efficacy. It does not promote a
strategy. Descriptive paired task intervals support independent review but do not
prove non-inferiority. Author-created real-repository audit pilots must retain their
measurement and experimental limitations. A failed or inconclusive pilot is a valid
result and cannot enable issues 56/57 automatically.

## Validation, migration and rollback

See the [implementation plan](../Plans/completed/P2-R4-2026-09-22-loop-evaluation.md),
[contract](../governance/LOOP_EVALUATION_CONTRACT.md), [schemas](../SCHEMAS.md) and
[V0.19.0 preparation](../framework-releases/V0.19.0.md). New JSON contracts do not
modify prior benchmark input or output. Stop invoking the evaluator to roll back;
retain external evidence and preserve application-owned data.
