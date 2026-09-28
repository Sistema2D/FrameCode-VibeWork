---
schema: "fcvw/adr@1"
id: "ADR-0010"
status: "accepted"
date: "2026-09-28"
artifact_role: "record"
owner: "framework"
upgrade_strategy: "preserve"
record_scope: "framework"
retrieval_scope: "routed"
language: "en-US"
---

# ADR-0010: Core reduction and removal of the inactive experiment layer

## Context

The structural shadow router ([ADR-0006](ADR-0006-adaptive-context-routing.md)), loop evaluation ([ADR-0008](ADR-0008-loop-evaluation.md)) and adaptive experiment controls ([ADR-0009](ADR-0009-adaptive-experiment-controls.md)) added about 1,400 lines of tools, 69 tests, two 13 KB contracts, a template and twelve JSON schemas. Their own activation gate stayed closed: the recorded pilot did not qualify and issues 55 to 57 closed with promotion criteria unmet. Every installation carried the layer, and every policy review paid for it, without any delivered behaviour depending on it.

## Decision

Remove from the core: `adaptive_control_fcvw.py`, `adaptive_learning_fcvw.py`, `adaptive_router_fcvw.py`, `adaptive_runtime_ledger_fcvw.py`, `loop_contract_fcvw.py`, `loop_metrics_fcvw.py`, their three test modules, the adaptive and loop contracts, the loop evaluation template, and the `--adaptive-*` and `--optional-token-budget` options of `retrieve_context.py`.

Keep `trace_fcvw.py` (used by the local runner and the retriever) and `benchmark_retrieval_fcvw.py` (retrieval regression check).

The complete layer remains in git history. The last revision that contains it is `0b3cb546062e154be169521fed50bec2f3b28383`. To restore it for a new experiment:

```sh
git checkout 0b3cb546062e154be169521fed50bec2f3b28383 -- \
  tools/adaptive_control_fcvw.py tools/adaptive_learning_fcvw.py tools/adaptive_router_fcvw.py \
  tools/adaptive_runtime_ledger_fcvw.py tools/loop_contract_fcvw.py tools/loop_metrics_fcvw.py \
  tools/test_adaptive_controls.py tools/test_adaptive_routing.py tools/test_loop_metrics.py \
  FCVW/governance/ADAPTIVE_EXPERIMENT_CONTRACT.md FCVW/governance/LOOP_EVALUATION_CONTRACT.md \
  FCVW/governance/TEMPLATE_LOOP_EVALUATION.md tools/retrieve_context.py
```

A maintainer may also tag that revision (for example `labs/adaptive-v0.19`) to keep it discoverable.

## Alternatives and consequences

- Keep the layer disabled in the core: rejected, because it kept the maintenance and review cost with no delivered behaviour.
- Move it to a `labs/` directory in the same repository: rejected, because its tests would stop running and the code would rot silently while still costing review time.
- Consequence: ADR-0006, ADR-0008 and ADR-0009 remain as history of the experiments; their tools are no longer installed. A future experiment starts from the revision above and must pass the same activation evidence before entering the core.

## Compatibility, validation and rollback

Default retrieval output is unchanged. Callers that passed `--adaptive-*` or `--optional-token-budget` now receive an argument error. The frozen rule inventory proves that no validator rule lived in the removed modules. Rollback: restore the files with the command above.

## Relationships

- [Phase 2 plan](../Plans/completed/P2-R4-2026-09-28-phase2-file-reduction.md).
- [AI governance](../AI.md).
