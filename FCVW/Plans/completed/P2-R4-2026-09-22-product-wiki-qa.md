---
schema: "fcvw/plan@2"
id: "P2-R4-2026-09-22-product-wiki-qa"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P2"
risk: "R4"
created_at: "2026-09-22"
updated_at: "2026-09-22"
current_version: "V0.18.0"
expected_version: "V0.19.0"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "FCVW/APPLICATION_DOCUMENTATION.md"
  - "FCVW/AI.md"
  - "FCVW/SECURITY.md"
  - "FCVW/TESTS.md"
  - "FCVW/wiki/schema.md"
  - "FCVW/skills/agent-factory/SKILL.md"
  - "FCVW/skills/self-improvement/SKILL.md"
depends_on: []
---

# Product wiki and QA

## Description

Centralize sourced application behavior knowledge in the wiki and implement the explicitly requested agent named QA. Its first run maps screens, buttons, modals, fields and states before incremental maintenance. User follow-up requires multidisciplinary execution for web, C++, firmware, native Windows/Linux and other targets; map non-GUI interfaces instead of inventing UI.

## Justification and objective

Existing module docs and wiki curation lack a bounded live-application QA loop and a distinction between inventory coverage, approved expectations and observed results. Avoid teaching an agent that a defect is intended behavior.

## Scope

On-demand QA profile, application-owned product inventory and surface/run templates, selective routing, deterministic coverage checking, documentation integration and fixture replay. No runtime dependency, background crawler, invented product knowledge, automatic production mutation or new release publication.

## Affected files or boundaries

Application documentation, wiki contracts/templates, QA skill, curator handoff, context/skill catalogs, optional verification tool, tests, inventories and V0.19.0 preparation record.

## Implementation plan

1. Define initial discovery and resumable inventory, then incremental testing/maintenance.
2. Separate expected source-backed behavior from actual UI observations and unresolved expectations.
3. Implement selected-page coverage checks without an automatic global wiki scan.
4. Exercise browser discovery and a deliberate defect in an isolated fixture, plus an executed non-GUI harness and structural coverage across target kinds. Physical/native-platform execution requires capabilities and is not implied.
5. Run structural and regression checks, measure validation overhead, and record limits.

## Proportionality gate

- Real problem: no unified surface knowledge and live QA evidence loop.
- Necessary scope: expressly requested by user, including first-run mapping and name QA.
- Reuse: existing wiki schema, source provenance, retrieval, lint and browser capabilities.
- Native capability: Markdown and Python standard library; optional browser tools supplied by the host.
- Dependencies: none added.
- Complexity: a bounded agent procedure, reusable templates and optional selected-page verifier.
- Tests: unknown expectations, missing/duplicate coverage, fabricated passes, unsafe paths and bootstrap scope.
- Simplification: no visual crawler service, embedding database or continuous agent process.
- Evolution: actual downstream applications and measured coverage/cost evidence.
- Safeguards: source authority, explicit execution scope, privacy, preserved evidence and reversible docs changes.

## Agent/Skill Creation Gate

- Skill loaded: `skills/agent-factory/SKILL.md`.
- Proposed asset: `skills/QA/SKILL.md`; agent profile named QA.
- Evidence of recurrence: not established; creation follows the explicit user instruction rather than an invented recurrence count.
- Existing coverage checked: Hephaestus owns focused UI fixes; wiki-curator owns generic curation; neither owns live functional coverage plus initial product mapping.
- Token ROI: keep the full procedure out of AGENTS and default sessions; no numerical savings claim.
- Risk ROI: prevent false functional claims and undocumented UI gaps.
- Scope boundary: observe/test bounded product surfaces and maintain their knowledge; no product-code fixes or generic wiki sweeps.
- Validation task: this implementation plus a controlled live fixture; no supplied downstream application is claimed as tested.
- Decision: create under explicit user authorization; record proposal in the decision record.

## Skill/Agent Self-Improvement Gate

- Skill loaded: `skills/self-improvement/SKILL.md`.
- Asset changed: wiki-curator handoff.
- Evidence: new product-knowledge contract needs explicit expected/observed separation.
- Metric passed: canonical rule drift; avoid conflicting curation authority.
- Scope preserved: curator still deduplicates and reviews sources, without becoming a browser tester.
- Token/risk ROI: precise handoff replaces duplicate rules; no measured token claim.
- Validation replay: fixture divergence is retained, not promoted to expected behavior.
- Decision: patch; compact improvement report in the decision record.

## Acceptance criteria

- [x] QA chooses target-specific execution and maps GUI or non-GUI surfaces.
- [x] QA performs initial mapping and leaves explicit resumable gaps.
- [x] Wiki distinguishes approved, provisional and unknown expectations from observations.
- [x] Tests cover every declared element/case within explicit scope, not inferred global coverage.
- [x] Maintenance is selective; optional tools do not enter default validation or retrieval loops.
- [x] Live fixture and deterministic checks demonstrate pass, failure and incomplete coverage behavior.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

Wiki ownership/authority, source freshness, skill activation, retrieval boundaries, browser action scope and existing module documentation.

### Regression contracts consulted

- [Application documentation](../../APPLICATION_DOCUMENTATION.md), [wiki schema](../../wiki/schema.md), [tests](../../TESTS.md), [AI](../../AI.md).

### Regression checks required

Selected-page negative fixtures, preservation of default routes, full local validation and live browser fixture with a known expected/observed mismatch.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Baseline validation | pass | Five local runs: median 438.012 ms; 228 existing tests from preceding change. |
| Source and installed regressions | pass | 242 tests each on Windows Python 3.12.10 and 3.14.2; governance and labeled benchmark pass in both runtimes. |
| Live target replay | pass for QA detection | Browser and CLI fixtures: 2 surfaces, 10 elements, 6 cases; 5 passed and 1 deliberate browser defect correctly retained as failure. Checker CLI returned 1 as required. |
| Multidisciplinary contract | pass | Seven non-GUI target kinds accepted without browser metadata; unknown/stale passes, missing evidence, incomplete discovery and unfilled thresholds rejected. |
| Context preservation | pass | AGENTS unchanged; explicit product_qa route only, unrelated security route unchanged. No QA execution or scan added to core validation/retrieval. |
| Local cost sample | measured | Five clean validations median 449.111 ms versus baseline 438.012 ms (+2.53%); optional two-surface check median 1.518 ms in-process. Small local samples include timing noise, not a zero-overhead or statistical guarantee. |

### Limitations and residual risk

Semantic correctness and hidden UI completeness require actual application access and review. Structural checks cannot prove that an agent really clicked a control. Initial mapping is bounded by available roles and time; unknown requirements remain unresolved.

## Validation plan

Measure the same clean-template command, run full tests/local runner, inspect prompt growth and replay real interactions in an isolated fixture outside the clean source.

## Rollback

Stop invoking QA and revert the optional tools/contracts. Existing module docs and wiki workflows remain usable. Preserve application inventory and QA evidence; never remove downstream data as part of rollback.

## Gates and approvals

User explicitly authorized implementation if viable and specified initial discovery and name QA. Source-only records/templates contain no real application data. The controlled fixture uses synthetic local data. Actual project tests require a known target, authorized environment and supplied capabilities; blocked access is reported.

## Related records

- [Design and proposal](../../decisions/ADR-0007-product-wiki-qa.md).
- [Next release](../../framework-releases/V0.19.0.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Full local runner | pass | External report outputs/product-qa-validation/20260922T161719Z-dc1070d4/report.json; source identity unchanged during the run. 242 tests in source and installed layouts per interpreter. |
| Live mapping and evidence | pass | External outputs/product-qa-replay contains inventory, surface pages, exact run, browser transcript, CLI streams, fixture hashes, coverage and performance JSON. Synthetic data only. |
| Failure correction | resolved | Initial full run 20260922T161433Z-1e9f5852 retained: legacy template test assumed every wiki template was a historical record. It now requires the index to be a preserved project profile while retaining record rules for other templates; all new templates have portable contract links. |
| Numeric embedded requirements | pass | Approved comparisons such as response time < 5 ms are accepted; unfilled threshold placeholders remain rejected. |
| Closeout | pass | Plan moved, active queue removed, graph/role manifest regenerated and final clean-template validation performed after documentation-only closeout. |

## Gaps and residual risk

No downstream target was provided. Actual native desktop, C++ toolchain, Linux, mobile and physical firmware execution were not performed; the profile selects available project/host capabilities and records blocked gaps. Simulation cannot establish physical board behavior. Fixture execution proves the procedure, not universal application coverage or zero total runtime cost. Language packaging remains a future release gate.
