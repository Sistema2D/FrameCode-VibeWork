---
schema: "fcvw/adr@1"
id: "ADR-0006"
status: "accepted"
date: "2026-09-16"
artifact_role: "record"
owner: "framework"
upgrade_strategy: "preserve"
record_scope: "framework"
retrieval_scope: "routed"
language: "en-US"
---

# ADR-0006: Connectome-inspired structural shadow routing

## Context

The supplied Connectome Implementation Package contains a revised report and six
proposed plans, not executable implementation. V0.16.0 already has BM25, typed
knowledge, mandatory path reporting and document graphs. Biological analogies
motivate experiments; they do not establish software performance benefits.

## Alternatives considered

Keep BM25 alone; extend the existing retriever; add a parallel router; introduce
embeddings or a spiking neural network. Choose a small optional extension using
the Python standard library and the existing graph builders.

## Decision

Deliver deterministic build, analyze, shadow and compare. Canonical path references
and document links provide structural evidence; wiki relations add signed edges.
No path reference infers a mandatory event automatically. No source authority is
changed. Propagation stays within the already eligible result pool, at most 20
candidates and three hops, with degree normalization and attenuation. Negative
signals terminate rather than flipping sign on later hops. Mandatory paths are
never scored. A structural hash binds source bytes and topology; no cache is loaded.
Default disabled mode and shadow both preserve actual delivered context.

## Feasibility of the supplied concepts

| Concept or proposed phase | Decision and evidence boundary |
|---|---|
| Baseline, contracts, authority separation | Implemented; synthetic route fixtures and comparison metrics. |
| Sparse graph, local activation, excitation/inhibition | Implemented for optional candidates; explicit supersedes/invalidates inhibit, contradictions stay visible. |
| Bounded recurrence, structural prior, topology | Implemented; hop traces, degrees, components and reciprocal pairs. No rich-club statistical claim. |
| Sparse task representations | Existing lexical ranking reused; no learned fingerprint model. |
| Plasticity, eligibility traces, rewards | Technically feasible; deferred pending independently labeled outcomes and causal evaluation. |
| Homeostasis and automatic budget tuning | Fixed experimental excerpt budget implemented; adaptive tuning deferred. |
| Circuit discovery and modular multi-agent routing | Feasible research; needs repeated task traces, holdout validation and explicit ownership. No scheduler added. |
| Assist rollout and governed promotion | Conditional on quality non-inferiority and safety evidence; no autonomous promotion. |
| SNN and biological connectome import | Research only; no demonstrated net benefit for this framework, no runtime dependency or dataset copied. |

## CLI and interpretation

Source checkout examples (installed packages use `FCVW/tools/`):

```bash
python tools/build_context_index.py --root . --output /external/context.jsonl
python tools/adaptive_router_fcvw.py build --root .
python tools/adaptive_router_fcvw.py analyze --root .
python tools/retrieve_context.py --root . --index /external/context.jsonl --query security --mandatory FCVW/SECURITY.md --adaptive-mode shadow
python tools/adaptive_router_fcvw.py compare --baseline /external/baseline.json --proposed /external/proposed.json --mandatory AGENTS.md --useful FCVW/SECURITY.md
```

Comparison files are JSON arrays of relative paths. Resolve every applicable
mandatory trigger before invocation. Add repeated mandatory arguments or an active
plan. Optional token budget estimates excerpts only. Independent expected mandatory
and useful-path labels can be supplied to compare. No query or raw excerpt is
persisted automatically. Printed traces may expose project paths; retain locally
under the project's own data policy. Omit the shadow flag for immediate rollback.

## Consequences and limits

No production quality or token-saving claim follows from synthetic tests. The
clean template has little typed knowledge; downstream enrichment remains governed.
Analysis describes the selected structural subgraph, not complete semantic reachability.
Malformed graph inputs fail closed to baseline; missing mandatory files still fail
the CLI. Learning, feedback schemas, production assist, automatic policy changes,
statistical rich-club analysis and full motif discovery remain unimplemented.

## Relationships

- [AI contract](../AI.md), [token budget](../TOKEN_BUDGET.md), [schemas](../SCHEMAS.md).
- [Release V0.17.0](../framework-releases/V0.17.0.md).

Later extension: [ADR-0009](ADR-0009-adaptive-experiment-controls.md) adds gated
optional feedback and assistance. The original default and shadow-only command
remain unchanged; this historical feasibility assessment is not promotion evidence.
