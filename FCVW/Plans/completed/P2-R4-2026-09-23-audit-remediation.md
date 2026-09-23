---
schema: "fcvw/plan@2"
id: "P2-R4-2026-09-23-audit-remediation"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P2"
risk: "R4"
created_at: "2026-09-23"
updated_at: "2026-09-23"
current_version: "V0.18.0"
expected_version: "V0.19.0"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "FCVW/AI.md"
  - "FCVW/SECURITY.md"
  - "FCVW/PLANNING.md"
  - "FCVW/REGRESSION_GUARDS.md"
  - "FCVW/TESTS.md"
  - "FCVW/OWNERSHIP.md"
depends_on: []
---

# Remediate the repository-wide framework audit

## Description

Correct the observed cross-tool failures and implement proportionate routing, QA, adaptive-state, observability, evaluation, and documentation improvements identified by the September 23 audit.

## Justification and objective

The default local runner currently fails its own governance check; retrieval includes a temporary directory, QA cannot validate a blocked first-run inventory, and an adaptive stop can be restarted with the same run ID. The remaining audit findings concern deterministic routes, truthful evidence, and maintainable operation. Preserve the portable Markdown-first framework while making enforceable boundaries executable.

## Scope

### Included

- Fix objective bugs and symlink-safe upgrade boundaries.
- Clarify routing precedence, capabilities, checkpoints and claims; add focused machine-readable contracts where they close demonstrated gaps.
- Add regression tests, local evaluation evidence where genuinely obtainable, and update framework documentation and the V0.19.0 preparation record.

### Excluded

- Installing a universal agent runtime, paid service, or hosted CI; claiming provider token counts, independent labels, physical device coverage, or cross-OS validation that was not observed.
- Publishing a new release or modifying an application repository.

## Affected files or boundaries

Existing scripts under `tools/`, the affected `FCVW/` policies and skills, tests, templates, generated navigation, this plan, and the V0.19.0 preparation record.

## Implementation plan

1. Repair and test the confirmed runner, index, QA, benchmark, upgrade, and adaptive-runtime faults.
2. Add bounded structured routing, capability, decision, trace, and checkpoint interfaces using existing Python and Markdown surfaces when justified.
3. Simplify repeated policy and skill guidance, preserve precedence and security boundaries, and add cross-tool tests.
4. Measure what can be measured locally; keep empirical activation gates closed without real independent evidence.
5. Run focused and integrated validation, update generated surfaces and release record, and record limitations.

## Proportionality gate

- Real problem and root cause: reproduced cross-tool defects and unenforced or overbroad declarative boundaries.
- Necessary in current scope: yes, the user requested implementation of all listed corrections and improvements.
- Existing codebase solution checked: reuse current route parser, wiki checker, local runner, plan queue, loop evaluator and JSON contracts.
- Native platform capability checked: standard-library path resolution, atomic file writing, JSONL and monotonic counters.
- Installed dependency checked: no new dependency is needed.
- New code or complexity justified: only when a focused test demonstrates an operational gap; experimental host hooks remain opt-in.
- Minimum non-trivial behavior tests: negative boundary fixtures and actual cross-tool invocations.
- Deliberate simplification and limitations: no universal supervisor, adapter, cache or statistical efficacy claim without measured benefit.
- Condition for future evolution: independently labeled real tasks and provider usage for promotion; target hardware/OS available for broader QA.
- Mandatory safeguards preserved: security, privacy, traceability, validation, audit, data integrity, documentation and risk-required tests.

## Acceptance criteria

- [x] The default local runner passes and preserves its source snapshot.
- [x] Index, QA first-run, benchmark output and upgrade boundaries handle audited edge cases.
- [x] Adaptive stops cannot be silently cleared by reusing the same run identity through the supported CLI.
- [x] Routing, QA capability and evidence claims are precise and testable without adding mandatory broad context.
- [x] New regression tests and full available local checks pass; untestable empirical/OS claims stay explicit.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

- Clean-template rejection of application artifacts; no cache included in releases.
- Mandatory routing, retrieval exclusions and optional context ranking.
- QA pass/fail and divergence gating; release and selective upgrade boundaries.
- Adaptive rollback and stop persistence.

### Regression contracts consulted

- [Regression guardrails](../../REGRESSION_GUARDS.md) — protected behavior and evidence.
- [AI policy](../../AI.md) — retrieval and agent trust boundary.
- [Security profile](../../SECURITY.md) — denial and path containment.
- [Local validation](../../governance/LOCAL_VALIDATION_CONTRACT.md) — offline check semantics.

### Regression checks required

- [x] Focused boundary tests for each concrete failure.
- [x] All source unit tests, clean-template validation, graph/queue checks, benchmark and installed smoke tests.
- [x] Default local runner and repository clean-state check.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Confirmed bug reproductions | pass | September 23 audit: runner cache failure, temporary-index inclusion, blocked QA checkpoint, adaptive restart. Negative tests now cover each boundary. |
| Focused and full checks | pass | `python -B tools/check_fcvw.py --root . --timeout 300` passed source tests, governance, benchmark and installed smoke on Windows/Python 3.14; source snapshot unchanged. |

### Limitations and residual risk

- Real provider usage, independent labels, Linux/macOS, downstream applications and firmware remain unavailable unless observed during implementation; no corresponding promotion is authorized by this plan.

## Validation plan

- [x] Run focused regression tests and all source unit tests.
- [x] Run local runner from the default output location, clean-template validator, document graph and plan queue checks.
- [x] Inspect versioned diff, role manifest and V0.19.0 record consistency.

## Rollback

Revert this plan's implementation commit or affected files while preserving reports outside the distributed payload; verify previous mandatory routes and installed layout after rollback.

## Gates and approvals

- Regression gate: required, assessed using the checks above.
- Security/data/refactoring/skill/release gate: review path containment, skill self-improvement and release checklist as applicable.
- Decomposition required: no new runtime or mandatory dependency; split opt-in experiments from bug fixes in validation.

## Related records

- Framework release: [V0.19.0 preparation](../../framework-releases/V0.19.0.md).
- Audit evidence: user-requested September 23 repository-wide review.
- Skill review: [QA and orchestrator improvement](../../audits/2026-09-23-skill-routing-improvement.md).

## Skill/Agent Self-Improvement Gate

- Skill loaded: `skills/self-improvement/SKILL.md`
- Asset changed: `skills/QA/SKILL.md` and `skills/orchestrator/SKILL.md`.
- Evidence: A3, B3 and D1/D2 from the repository audit.
- Metric passed: validation gap and observed trigger ambiguity.
- Scope preserved: targeted clarification only.
- Token/risk ROI: fewer irrelevant skill loads and truthful blocked QA coverage.
- Validation replay: focused routing and QA tests.
- Decision: patch only affected assets.

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Baseline source tests | pass | `python -B -m unittest discover -s tools -p 'test_*.py'`: 295 tests. |
| Baseline default local runner | fail | Governance rejected runner-created `.fcvw-cache` as clean contamination. |
| Remediated integrated runner | pass | Windows/Python 3.14: 305 tests (one Windows symlink test skipped), governance, labeled retrieval benchmark and installed smoke; source snapshot unchanged. Report: `.fcvw-cache/local-checks/20260923T110356Z-a46b5b7b/report.json`. |
| Corpus retrieval timing | descriptive | 1,684 chunks; 32 BM25 queries median 92.63 ms, p95 101.38 ms. No persistent cache added without a measured bottleneck. |

## Gaps and residual risk

- Runtime ledger is trusted local state, not adversarial authentication. Explicit CLI routes enforce it; direct Python calls and files modified by a hostile local actor are outside this boundary.
- Host activation, actual product interaction, provider token usage, independent real-task labeling and Linux/macOS or physical-device QA were unavailable. No statistical improvement or universal-agent claim follows from the synthetic fixtures and local tests.
- The opt-in trace records metadata and nullable provider tokens; it does not attest that a user was consulted. QA records mark declared-only consultation separately from witnessed evidence.
- The existing 24-audit pilot rejects live adaptive promotion. The activation gate remains closed. Additional cache, universal adapters and supervisor machinery were omitted because the measured local path and current usage do not justify their cost.
