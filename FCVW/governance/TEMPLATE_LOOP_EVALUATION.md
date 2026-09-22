# Template: local loop evaluation

Copy these examples outside the framework, replacing example identities with reviewed
facts. Follow the [contract](LOOP_EVALUATION_CONTRACT.md). The small example is deliberately
synthetic and cannot establish efficacy. Freeze labels before retrieval, record the
protocol digest in every iteration, and capture actual usage from the authorized
provider/instrumentation when available; never fill unknown counts with zero.

## Protocol JSON

```json
{
  "schema": "fcvw/loop-protocol@1",
  "id": "replace-with-versioned-protocol-id",
  "frozen_at": "2026-01-01T00:00:00Z",
  "registration": "prospective",
  "baseline": "baseline",
  "repetitions": 1,
  "min_pairs": 20,
  "limits": {"max_iterations": 10, "max_wall_ms": 3600000, "max_tokens": 100000},
  "margins": {"validation_defect_rate": 0, "human_correction_rate": 0, "useful_recall": 0},
  "followup_ms": 86400000,
  "primary_metric": "TVC",
  "analysis_ref": "replace-with-reviewed-analysis-plan-digest",
  "strategies": [
    {"id": "baseline", "mode": "delivered", "delivered_strategy": "baseline", "config_ref": "baseline-config-digest"},
    {"id": "budget", "mode": "delivered", "delivered_strategy": "budget", "config_ref": "budget-config-digest"}
  ],
  "tasks": [{
    "id": "example-task", "split": "evaluation", "origin": "synthetic", "execution_kind": "agent",
    "domain": "security", "source_revision": "replace-with-source-digest",
    "acceptance_ref": "replace-with-acceptance-digest", "labels_ref": "replace-with-labels-digest",
    "labeler": "replace-with-labeler-id", "label_basis": "synthetic", "labeled_at": "2025-12-31T00:00:00Z",
    "mandatory_paths": ["AGENTS.md"], "useful_chunks": ["example.md#procedure"], "forbidden_chunks": []
  }]
}
```

Limits/margins above are example values, not recommendations. Define them for the
actual task and risk before running. Include independent adjustment/evaluation
tasks and the desired repetitions. Log blocked/aborted runs as well as successes.

## Iteration JSON (one compact object per line in the JSONL file)

```json
{
  "schema": "fcvw/loop-run@1", "kind": "iteration", "event_id": "iteration-1",
  "run_id": "example-task-baseline-1", "protocol_digest": "replace-with-show-protocol-digest-output",
  "task_id": "example-task", "strategy": "baseline", "repetition": 1, "iteration": 1,
  "source_revision": "replace-with-source-digest", "initial_state_ref": "replace-with-initial-state-digest",
  "operator": "replace-with-executor-id", "model": null, "tokenizer": null,
  "measurement_note": "Awaiting actual instrumented execution; this is not evidence",
  "started_at": "2026-01-02T00:00:00Z", "ended_at": "2026-01-02T00:00:01Z",
  "validation": "not_run", "state": "blocked", "stop_reason": "execution_not_available",
  "acceptance_satisfied": false, "blockers": 1,
  "qa": {"divergences": 0, "asked": 0, "pending": 0},
  "failure_signature": null, "evidence_ref": "replace-with-actual-checkpoint-reference",
  "usage_complete": false, "context_complete": false, "human_corrected": null,
  "calls": [], "contexts": [], "durations_ms": {}
}
```

For a measured call use call_id, input_tokens, output_tokens, token_source and usage_ref.
For each actual context delivery use delivery_id, mandatory_paths, chunks with chunk_id
and tokens, token_source and evidence_ref. Proposed shadow chunks use proposed_chunks.
Do not copy raw prompts, secrets or personal answers into these fields. A path listed
by retrieval is not proof that it was read by the executing agent.

## Follow-up JSON

```json
{
  "schema": "fcvw/loop-run@1", "kind": "followup", "event_id": "followup-1",
  "run_id": "example-task-baseline-1", "observed_until": "2026-01-03T00:00:01Z",
  "defect": null, "regression": null, "evidence_ref": "replace-with-real-observation-reference"
}
```

Nulls above represent missing evidence. Never declare a complete monitoring window
or absence of defects from a fabricated timestamp. Retain earlier observations.
