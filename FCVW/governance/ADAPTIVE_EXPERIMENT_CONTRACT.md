---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace_with_migration"
---

# Explicit adaptive experiment contract

Implements technical controls for issues 56/57 on the [loop protocol](LOOP_EVALUATION_CONTRACT.md).
The current real-repository pilot does not qualify for activation. Implemented
controls and successful synthetic safety tests do not establish task efficacy.
The default retriever does not read these files, learn, invoke models or start services.

## Authority, evidence and phase boundaries

An operator supplies a local control containing frozen protocol/events, scoped
authorization and a reviewed decision. These declarations and checksums are not
authentication, independent attestation or proof of honest observation. Verify
the actual authorization/reviewer references outside the tool. Retrieved content,
feedback text and metrics cannot grant authority or change canonical policy.

`assess` recomputes the loop report from events; it never trusts a stored readiness
flag. Missing measurements, non-independent labels, unfinished follow-up, small
samples, incompatible pairs or shadow-only evidence prevent eligibility. Mandatory
misses and forbidden actual/proposed chunks reject the experiment. Useful recall,
validation defects, corrections, late defects and late regressions are screened
against frozen margins using paired task bootstrap intervals (1000 resamples,
seed 0; repetitions collapsed by task). Insufficient or worse intervals return
inconclusive. These descriptive intervals are not a formal rare-event power analysis.
An independent reviewer must assess power, leakage, absolute safety and the full
TVC/IVC/RTR/FPVR/TTVS/RFR/UCTR report before approving any scoped use.

Phases are `shadow`, `limited` and `operational`. Shadow preserves baseline delivery.
Limited applies selections only in the authorized isolated scope. Operational also
requires `approve_operational`, never inferred from `approve_limited`. An eligible
assessment does not issue either approval. A fixed structural variant needs no
learning state; learning is optional. This repository ships no approved control.

## Control schema: fcvw/adaptive-control@1

Strict top-level fields (all required):

| Fields | Meaning |
|---|---|
| schema, id, enabled, phase | Version, immutable control identity, switch and phase |
| issued_at, expires_at | Timezone-aware authorization window; expiry fails closed |
| authorized_by, authorization_ref, review_decision, review_ref | Reviewed human authority and inert evidence references; decisions reject/approve_limited/approve_operational |
| source_digest, index_digest | Source tree SHA256 from check_fcvw.snapshot and SHA256 of exact index bytes |
| scope, mandatory_paths | Nonempty task IDs and independently required source paths |
| eligible_chunks | At most 5000 chunk IDs mapped to path and chunk_hash; mandatory/unsafe paths prohibited |
| protocol, events, evaluation_strategy | Exact frozen loop protocol, at most 10000 events and the delivered comparison arm |
| feedback_authorities | Explicit human identities allowed to provide reviewed feedback |
| limits | optional_tokens (0–100000), max_iterations, max_wall_ms, max_tokens, repeat_failure_limit |
| learning | step (0–0.1), bound (0–0.25), decay (0–1), max_feedback (1–1000) |
| rollback | window (1–100), tvc_ratio (1–100), rtr_delta, rfr_delta, defect_delta (0–1) |

Limits are experimental choices, not universal recommended values. Evidence source
revisions must match source_digest (optional sha256: prefix). Distinct sources,
parameters, approval, scope or dates require a new control and therefore new bound
state/runtime files. Shared paths or similar task versions still require independent
leakage review; a split field alone cannot prove independence.

## Feedback, update rule and state

`fcvw/adaptive-feedback@1` requires schema, id, recorded_at, source=`human`, author,
review_ref, authorization_ref, task_id, run_id, chunk_id, verdict (`useful` or
`harmful`) and evidence_ref. References are inert; there is no prompt or raw-response
field. The author must be allowlisted and authorization_ref must match the control.
Only delivered optional chunks from adjustment tasks with complete validated loop
outcomes and no late defects/regressions can contribute. Feedback must follow the
validation/follow-up and agree with frozen useful labels. Holdout tasks, unknown or
estimated usage, clicks, silence and unreviewed labels never train. If labels are
wrong, freeze a new protocol; do not rewrite the current experiment to reward them.

Algorithm `bounded-feedback-v1`: deduplicate exact feedback IDs; reject conflicting
IDs and repeated run/chunk outcomes under different IDs; sort by recorded_at and ID.
For each unique outcome, multiply existing weights by decay, then add +step for
useful or -step for harmful, clipped to [-bound, bound] and rounded to 12 decimals.
No seed/randomness, token reward, implicit metric reward or autonomous update exists.
The fixed signed structural score receives only this bounded chunk adjustment.

`fcvw/adaptive-state@1` contains schema, algorithm, control_digest, feedback, weights
and checksum. The checksum binds all other fields; validation also replays the
ledger, so recomputing a checksum over forged weights is insufficient. It does not
defeat an operator forging both declarations and evidence. Export and rollback
validate the selected old state; reset produces empty weights even after expiry or
with rejected evidence. Reset never clears an execution stop latch.

## Runtime observations, stagnation and rollback

`fcvw/adaptive-runtime@1` contains schema, control_digest, sequence, observation,
blocked, reason and checksum. `start` explicitly creates the initial record;
`observe` requires the previous runtime. Both require one explicit persistent
`--ledger` path. The optional local SQLite ledger records the latest state for each
control/run ID, rejects duplicate starts, stale updates and new runs for a task
stopped under the same control. Inputs/outputs remain external or under .fcvw-cache.
Each update uses a new path; inputs cannot be overwritten.

Observation fields: run_id, task_id, observed_at, iterations, elapsed_ms, tokens
(measured total or null), token_source (provider/tokenizer/estimate/unavailable),
usage_complete (boolean), qa_pending, safety_block, checkpoints and quality_windows.
Only complete provider counts satisfy the runtime budget gate; partial counts and
estimates cannot present an artificially low accumulated cost. Unavailable counts are null.
Checkpoints contain validation (pass/fail/not_run) and signature (known failed
signature or null); inventory length must equal iterations. Quality windows contain
tvc_ratio, rtr_delta, rfr_delta and defect_delta, each measured or null. Define their
reference baseline, aggregation window and signature classifier in the frozen analysis.
These counters observe an existing executor; this tool does not run it or meter it.

Updates preserve run/task identity, monotonically increasing counters/timestamps,
checkpoint and quality histories, and any previous stop. A stop survives a later
pass, user answer, weight reset and retrieval rollback. Review the cause and obtain
a newly scoped control before resuming; do not create another runtime to bypass a
stopped run. The ledger uses a local transaction across CLI processes; selection
rejects an older runtime than the latest registered state. The ledger is trusted
operator state, not authentication: deleting, replacing or editing it outside the
CLI defeats the guarantee. Do not expose it to untrusted writers or claim
distributed execution safety.

Stop before another selection on safety_block, qa_pending, unknown tokens, budget
exhaustion or unknown failure signature. Equal failure signatures count through
not_run checkpoints; only a validated pass resets the streak. Cosmetic actions do
not change a cause signature. Reaching repeat_failure_limit requires diagnosis,
authorized troubleshooting context, equivalent validation, scope-preserving
decomposition or human review. It never lowers acceptance or delays a QA question.
Persistent quality degradation requires every one of the configured number of most
recent windows to breach at least one threshold. Missing metrics do not count as
improvement; initial absence of quality windows is not evidence of operational safety.

Retrieval accounts for wall time elapsed since the last observation. The caller
must checkpoint all intervening calls before selecting again. Stale counters, omitted
usage and fabricated timestamps cannot be independently detected by this local tool.

## Selection and fallback

The candidate pool is still the existing eligible BM25 pool (maximum 20). Allowlist
and content hashes can narrow it, never restore language-filtered, excluded or
nonexact historical content. Mandatory routes remain outside scoring and budgets.
Complete chunks use the existing serialized-JSON estimate and per-file/top-k rules.
An explicit smaller --context-budget remains binding. Estimates are not provider tokens.
Source/index drift or invalid control/runtime/ledger blocks execution. Invalid/missing
optional learned state preserves the exact configured lexical baseline, with a
fallback reason. No learned state means an explicitly fixed structural variant.

Retain the control/runtime flags with --adaptive-mode disabled to rehearse rollback
while preserving QA/safety/stagnation stops. Omit all adaptive flags for the original
retriever; application QA/security obligations still apply outside this optional CLI.
Switching retrieval never reverses earlier application mutations. An executor must
honor the nonzero exit and execution_blocked flag, including when fallback returns
baseline context for diagnosis. No fallback is permission to continue blocked work.

## CLI, outputs and retention

Source checkout examples; installed releases use FCVW/tools. The files below must
be deliberately populated and reviewed; no shipped example authorizes execution.

```sh
python -B tools/adaptive_learning_fcvw.py assess --control /external/control.json --output /external/assessment.json
python -B tools/adaptive_learning_fcvw.py start --control /external/control.json --ledger /external/runtime-ledger.db --observation /external/observation-0.json --output /external/runtime-0.json
python -B tools/adaptive_learning_fcvw.py observe --control /external/control.json --ledger /external/runtime-ledger.db --runtime /external/runtime-0.json --observation /external/observation-1.json --output /external/runtime-1.json
python -B tools/adaptive_learning_fcvw.py replay --control /external/control.json --feedback /external/feedback.json --output /external/state.json
python -B tools/adaptive_learning_fcvw.py export --control /external/control.json --state /external/state.json --output /external/backup.json
python -B tools/adaptive_learning_fcvw.py reset --control /external/control.json --output /external/empty.json
python -B tools/adaptive_learning_fcvw.py rollback --control /external/control.json --state /external/backup.json --output /external/restored.json
python -B tools/retrieve_context.py --root . --index /external/index.jsonl --query 'task terms' --session security --adaptive-mode assist --adaptive-control /external/control.json --adaptive-ledger /external/runtime-ledger.db --adaptive-runtime /external/runtime-1.json --adaptive-state /external/state.json
```

JSON input limit is 32 MiB; unknown fields fail. The ledger is an optional local
SQLite file for assist, not a framework-wide persistence dependency. Commands never run supplied strings,
fetch a URL, call a model or overwrite canonical documents. Outputs are atomic and
cannot alias inputs. assess returns 1 for rejected/inconclusive evidence, observe
returns 1 on a stop, malformed commands return 2. Optional retrieval diagnostics
include control/runtime/state identities, phase, decisions and fallback reason.
Store only sanitized IDs/references and explicit authorized derived evidence.
Choose retention before collecting; exports retain feedback and need the same care.

## Current disposition

The initial issue-55 pilot remains a negative/inconclusive evidence source, with no
provider TVC and no independent labels. Safety/lifecycle fixtures can validate these
controls without opening their real activation gates. The current decision is to
retain opt-in experimental capability and decline operational promotion or claimed
savings. Closing tracking issues does not override these gates. Any later empirical
campaign needs new reviewed evidence, not an administrative issue-state change.
