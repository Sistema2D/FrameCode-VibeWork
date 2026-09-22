---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Validated-completion evaluation

This optional local evaluator implements the measurement infrastructure of [issue 55](https://github.com/Sistema2D/FrameCode-VibeWork/issues/55). It reads deliberately supplied, sanitized evidence; it does not run models, monitor sessions, learn weights, change retrieval, or authorize issues 56/57. It complements the existing retrieval benchmark because execution runs, resumptions and quality follow-up have different units from retrieval cases.

## Freeze the experiment first

Copy the [protocol/run template](TEMPLATE_LOOP_EVALUATION.md) to an external evaluation directory. Define real tasks, acceptance and evidence references, independent labels, adjustment/evaluation split, configurations, repetition/order policy, initial-state isolation, limits, primary metric, quality margins and late-regression window before execution. Use a versioned analysis reference for the intended sample size and non-inferiority method. Changing scope or criteria requires a new protocol/digest and separate results.

Label required paths and useful/forbidden chunk IDs from requirements before querying retrieval. Record who labeled them and whether review was independent, by the implementation author, or synthetic. The tool checks declared identity/timing, not the reviewer's independence or the truth of the task's real-world origin. Keep source-derived author labels honest; they are not independent review. A task may be an agent execution, deterministic repository audit or retrieval replay; only the first supports claims about an agent's full development cycle.

Baseline and lexical-without-budget may be the same configuration: do not register duplicate arms. A shadow strategy names its unchanged delivered strategy. Its proposed chunks are scored separately and cannot establish execution benefit for undelivered context. Any active experiment needs its own authority and controls; this evaluator does not grant them.

## Input schemas

These JSON schemas are strict and separate from permissive Markdown frontmatter. Unknown fields, duplicate object keys, NaN/infinity, invalid booleans/counts, duplicate identifiers and inconsistent states fail. References are inert strings: no referenced file, command, URL or instruction is followed.

### `fcvw/loop-protocol@1`

Required top-level fields:

| Field | Contract |
|---|---|
| schema, id, frozen_at | Schema name, stable experiment identity, timezone-aware timestamp |
| registration | prospective or retrospective; retrospective evidence cannot establish preregistration |
| baseline, strategies | Baseline ID; distinct objects with id, mode (delivered/shadow), delivered_strategy and config_ref |
| repetitions, min_pairs | Planned repetitions 1–100; minimum independent paired tasks 2–10000 for descriptive intervals |
| limits | Positive max_iterations, max_wall_ms, max_tokens; report breaches, never silently truncate |
| margins | Predeclared nonnegative validation_defect_rate, human_correction_rate and useful_recall margins, each at most 1; assessed by the independent reviewer |
| followup_ms, primary_metric, analysis_ref | Nonnegative observation window, TVC/IVC/RTR/TTVS, and frozen analysis-plan reference |
| tasks | Objects with id, split (adjustment/evaluation), origin (real/synthetic), execution_kind (agent/deterministic_audit/retrieval_replay), domain, source_revision, acceptance_ref, labels_ref, labeler, label_basis (independent/author/synthetic), labeled_at, mandatory_paths, useful_chunks and forbidden_chunks |

The mandatory list is nonempty. Useful and forbidden labels cannot overlap. References should identify immutable revisions/digests rather than mutable filenames alone. State strategy configuration, model settings, seeds/order, environment, task leakage controls and annotation disagreements in the referenced protocol material. Do not load that material into default agent context.

### `fcvw/loop-run@1`: JSONL events

One iteration event is an objective/action/observation/adjustment cycle ending at a predeclared validation checkpoint, not a single tool call. Every started run gets an event, including a blocked first iteration. Shared fields are schema, kind, event_id, run_id and evidence_ref.

Iteration events require:

- kind = iteration; protocol_digest; task_id, strategy, repetition and consecutive iteration starting at 1;
- source_revision matching the task, initial_state_ref, operator, model and tokenizer (nullable), measurement_note;
- started_at and ended_at with timezone; sequential checkpoints cannot overlap, although work within one iteration may overlap;
- validation = pass/fail/not_run; state = running/validated/blocked/aborted/budget_exhausted; stop_reason is null only for running;
- acceptance_satisfied, nonnegative blockers, and qa counts divergences/asked/pending. Validated requires full acceptance, passing validation, no blockers, all divergences asked and no unanswered decision;
- failure_signature, null except for a failed checkpoint; a stable signature is a declared operational category, not inferred cause;
- usage_complete and context_complete attest whether the producer captured all relevant calls/deliveries. Unknown scope is false, not zero;
- human_corrected is true/false/null. False means explicitly observed absence, not missing data;
- calls, contexts and durations_ms as below.

Each call has unique call_id, input_tokens and output_tokens (nonnegative integers or null), token_source (provider/tokenizer/estimate/unavailable), and usage_ref. An unavailable source has null counts. Retries and delegated calls, when authorized, have their own IDs; do not double-count aggregate wrapper usage, cached input or reasoning tokens already included in provider totals. Optional cost/currency/cost_ref must appear together and refer to billing; currency uses three uppercase letters. No exchange-rate conversion or price inference occurs.

Each context delivery has unique delivery_id, mandatory_paths actually delivered/read, chunks, token_source (tokenizer/estimate/unavailable), evidence_ref and optional proposed_chunks for shadow evaluation. Each chunk contains chunk_id and nullable tokens. Reject duplicate chunks within one delivery; repeated delivery on different calls is counted again. A complete inventory includes at least one observation per model call. Merely listing a mandatory path in retriever output does not prove the agent read it: the producer must identify what was observed. Keep proposals separate from actual input.

durations_ms may contain retrieval, model, tools, validation and human_wait; each value is an observed wall duration or null. Categories may overlap and are never summed into total wall time. A category longer than its enclosing iteration is invalid; parallel CPU-time sums belong outside this contract.

Follow-up events require kind = followup, observed_until, defect and regression (true/false/null), plus the shared fields. They must reference a known run and cannot predate its end. Append new evidence without modifying earlier checkpoints. The declared observation window must be covered; a later false flag never erases an earlier true defect. Observation completeness remains a producer claim.

## Identity, resumption and privacy

Group by run_id, bound to one task/strategy/repetition and stable source/model/tokenizer/initial state. Exact duplicate events are ignored; conflicting duplicates, iteration gaps, execution after a terminal state, reused call/delivery IDs and two run IDs for the same planned repetition fail. Reordered files are sorted deterministically. Missing planned runs appear explicitly, and adjustment/evaluation cohorts stay separate.

Do not store prompts, responses, private user answers, secrets or production content in these files. Field allowlists reject accidental raw payloads but are not a secret detector: sanitize IDs/references/free text before supplying them. Input files are capped at 32 MiB each, events at 1 MiB and the combined input at 50000 records. Telemetry stays in a disposable cache or an explicit external directory, not canonical wiki records or clean distribution assets. Keep evidence needed for review under an explicit retention policy.

## Metrics and missingness

| Metric | Implementation |
|---|---|
| TVC | All provider input + output tokens through first validated completion. Incomplete call scope or non-provider/unknown counts yields null; separately expose known provider tokens as a lower bound |
| IVC | Consecutive iterations through validated completion; null for unfinished runs |
| RTR | Provider tokens in iterations after the first failed checkpoint / TVC; zero when fully measured and no validation failed, null when unknowable or an applicable denominator is zero. It is a proxy for rework |
| FPVR | Runs validated in iteration 1 / started runs in each declared cohort. Also show planned, started, validated and missing runs to expose selection bias |
| TTVS_ms | Last validated checkpoint end minus execution start; unfinished runs retain elapsed_ms but no fabricated completion time |
| RFR | Failed checkpoints repeating the immediately previous failed checkpoint's known signature / failed checkpoints with known signature. Report known-signature and failure counts; no signed failures means null |
| UCTR | Useful labeled optional tokens / delivered optional tokens, counted per delivery. No optional tokens means null; unknown/mixed counting bases are unavailable. Tokenizer and estimated cohort distributions remain separate |

Report observed mandatory recall minimum, useful recall, optional precision and forbidden hits over context deliveries. A mandatory miss or forbidden actual/proposed chunk is an invariant violation. Completeness gaps are inconclusive rather than proof of zero violations. No default route or retriever is modified by measurement.

Validation defect rate is the fraction of runs with any failed declared checkpoint among runs with known checkpoint outcomes. Expected negative-test success is pass. Human correction uses observed run-level flags; missing values remain null. Late defects/regressions are separate from first-pass success. Monetary totals require complete calls, billing evidence and a single currency; otherwise null.

Every metric distribution includes known/missing counts. Both UCTR distributions use the started cohort as denominator: a different or unknown counting basis is missing for that distribution. Protocol expansion is capped at 50000 planned executions before allocating missing-run records. Median/max are descriptive; p75 needs at least 4 observations and p95 at least 20. Token/completion distributions alone have survivor bias: retain incomplete runs, their measured accumulated cost, and completion rates. Never claim an improvement by discarding blocked or expensive runs. Human waiting remains part of total wall time; avoiding the mandatory QA question is not a performance benefit.

## Comparisons and review

Match evaluation task/repetition across baseline and candidate only when source, initial state, model and tokenizer identities agree. Collapse repeated deltas per task, then emit candidate-minus-baseline means and descriptive 95% percentile bootstrap intervals using 1000 task resamples and seed 0, only at min_pairs. Record this method in the frozen analysis plan. These small-sample intervals are not a statistical proof of non-inferiority, especially for rare safety events or zero observed defects. Task ordering, leakage, true independence and statistical power still require review.

Readiness is invariant_violation, inconclusive or ready_for_independent_review. The last means declared measurement prerequisites are present, not that quality passed. The independent reviewer compares all quality evidence against the frozen margins/method, including useful recall, human corrections and late regressions. Issues 56/57 always remain not_authorized_by_tool. Publish negative, neutral and inconclusive results and their limitations; no metric grants operational authority.

## CLI and rollback

Source checkout commands (installed releases use FCVW/tools):

```sh
python -B tools/loop_metrics_fcvw.py --protocol /external/protocol.json --show-protocol-digest
python -B tools/loop_metrics_fcvw.py --protocol /external/protocol.json --runs /external/runs.jsonl --runs /external/resumed.jsonl --output /external/report.json
python -B tools/loop_metrics_fcvw.py --protocol /external/protocol.json --runs /external/runs.jsonl --format markdown --output /external/report.md --check
```

Without --check, a valid report may be inconclusive. With --check, incomplete evidence/invariants return 1; invalid input returns 2. Inputs cannot be overwritten. Outputs inside the framework root are restricted to .fcvw-cache and are written atomically. No content is uploaded, model called or dependency installed. Stop invoking the tool to roll back; existing retrieval benchmarks and recorded evidence remain intact.
