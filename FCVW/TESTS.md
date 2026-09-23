---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Testing and validation

## Purpose

Define risk-proportional evidence for new behavior, protected existing behavior, failure handling, and rollback. Each plan selects the applicable checks; this policy does not invent application-specific commands.

## General rules

- Validate both the requested outcome and the protected behaviors listed in the plan's Regression impact section.
- Prefer reproducible automated checks for stable contracts; record manual evidence when automation is unavailable or unsuitable.
- A test name or suite size is not evidence by itself: record command or procedure, result, protected contract, and limitation.
- Use representative synthetic or sanitized fixtures instead of private production data.
- A reproducible failure receives a troubleshooting record when diagnosis or recurrence value justifies it.
- Published changes carry concise validation evidence in their plan and changelog or framework release record.
- Missing tooling does not silently lower risk; it becomes a limitation, residual risk, and completion decision.

## Minimum regression evidence by risk

| Risk | Minimum evidence |
|---|---|
| R1 | Focused review or replay of the changed contract, structural checks when applicable, and changelog/release evidence |
| R2 | Direct component or document-contract test plus one relevant existing-behavior replay |
| R3 | Full build or equivalent integrity check, primary workflow, alternate/error workflow, and related-boundary regression |
| R4 | R3 plus dependent workflows, compatibility or recovery evidence, documented rollback, and explicit residual-risk review |
| R5 | Expanded regression across affected boundaries, security/data review when applicable, rollback rehearsal, and explicit human approval before completion |

An additional independent critic/reviewer is selective: use one when a high-risk
change has unresolved ambiguity, repeated prior defects or an unverified boundary
that a second perspective can actually inspect. Record its question, findings,
validation impact and added calls/time. Do not dispatch a second agent solely
because a plan is R3+ or because a tool is available.

Authentication, authorization, persistent data, public APIs or file formats, agent instructions, memory, filesystem, automation, migrations, destructive behavior, and releases are not R1 by default. An R1 classification for one of these surfaces requires a concrete blast-radius and reversibility rationale.

## Evidence matrix by change surface

| Surface | Required considerations |
|---|---|
| Documentation/governance | links, schema, ownership, instruction conflicts, lifecycle, generated summaries, negative structural fixture |
| UI/accessibility | supported viewport/state matrix, keyboard/focus, contrast, error/empty/loading states, primary and adjacent navigation |
| Frontend/client | focused tests, build, affected journey, navigation/state persistence, error and offline/dependency behavior |
| Backend/API | syntax/compile, contract tests, valid/invalid input, authorization, dependency failure, idempotency where required |
| Data/filesystem | CRUD or equivalent lifecycle, old-data compatibility, migration idempotency, reconciliation, backup and recovery |
| AI/agent/RAG | allowed and denied actions, untrusted-content handling, context/source traceability, unavailable model, memory boundaries |
| Security/privacy | authentication, authorization denial, secrets/logs, path boundaries, destructive confirmation, misuse cases |
| Refactoring | characterization baseline, before/after behavior, public contract, focused and dependent regressions |
| Performance/operations | measured baseline, representative load, startup/deploy/recovery, resource and failure thresholds |
| Release/build | clean artifact, version surfaces, primary smoke, migration/rollback, changelog, known gaps |

Release tests also cover state transitions, content-versus-publication revisions, completed related plans, copyable template completeness, language-variant asset/checksum evidence, and external publication URLs.

## Regression test design

1. Name the protected behavior and its authoritative contract.
2. Choose the narrowest check that can detect the unwanted change.
3. Capture a baseline before modification when the result is comparative.
4. Include negative, invalid, denied, empty, or recovery cases when relevant.
5. Confirm a new guardrail would fail on the known regressed state when practical.
6. Run focused checks first and broaden by risk and dependency radius.
7. Record nondeterminism, environment differences, skipped paths, and residual uncertainty.

## AI and agent boundary replay

Changes to `AGENTS.md`, AI policies, skills, prompts, memory, retrieval, or automation must replay representative allowed, denied, ambiguous, unavailable-runtime, and prompt-injection cases. Mature projects may automate evaluations in their chosen runtime, but FCVW does not require a particular vendor or test package.

## Visual evidence

Visual changes identify supported viewports and states before testing. Compare relevant before/after states; verify keyboard focus, zoom or scaling when applicable, long content, empty/error/loading states, disabled and destructive actions. Store only non-sensitive captures in project-owned paths.

## Data and rollback evidence

Schema, format, migration, retention, import/export, or destructive changes use representative prior-version data. Validate reconciliation, idempotency, backup, recovery, and rollback—or record why rollback is irreversible and who approved that risk.

## Completion checklist

- [ ] Requested behavior has evidence.
- [ ] Regression impact identifies protected behavior and source contracts.
- [ ] Applicable focused and dependent checks have final results.
- [ ] Invalid, denied, error, and recovery paths were considered.
- [ ] Compatibility and rollback were validated when applicable.
- [ ] Security, data, AI, visual, or operational gates ran when triggered.
- [ ] No pending regression result remains.
- [ ] Limitations, residual risks, and known gaps are explicit.
- [ ] Plan and changelog or framework release record contain reproducible evidence.

Use `governance/TEMPLATE_PLAN.md` to record change-specific validation and `REGRESSION_GUARDS.md` for blocking rules.

## Document graph and queue evidence

Structural changes must test valid and negative cases for incoming links, entrypoint reachability, broken/ambiguous targets, self-only links, inline-code examples, source-relative destinations, spaces in paths, queue absence, duplicate/stale IDs, exact state-directory targets, status mismatch, category and P1-P5 order, blocker lifecycle, and justified cross-state override.

Plan-dependency changes additionally test flat-list enforcement, missing/ambiguous/self references, duplicate IDs, cycles, queue parity, completed prerequisites without evidence, satisfied evidence, discontinued invalidation, and completed dependent plans with unresolved prerequisites. Aggregate queue output must be derived from both canonical queues and remain disposable.

An index that merely contains a path does not prove a meaningful record relationship. Generated plans, audits, troubleshooting records, releases, regressions, and session syntheses also link their authoritative parent or source.

## Frontmatter and retrieval evidence

Frontmatter changes test scalars, first-level lists, non-empty required values, ID/priority/risk coherence, duplicate keys, invalid ISO dates, unsupported nesting, invalid enums, relationship-path existence, and legacy preservation. Retrieval changes test role-based default scope and authority, mandatory-route recall, missing-context failure status, out-of-root plans, source traceability, retrieval priority, freshness, active-plan relation, excluded content, obsolete-content penalties, explicit declared-language filtering, empty results, token bounds, and prompt-injection handling.

Typed-knowledge changes test ID/path target resolution, generated inverses, self/conflicting relations, supersession cycles, maturity values, source-digest syntax and change detection, dependent review candidates, document-graph independence, chunk/source hash distinction, metadata filters, one-hop relation selection, graph seed/candidate limits, and deterministic behavior without a semantic model. Semantic review tests source bounds, review-only output, unavailable-runtime handling, and prohibition of silent mutation.

Language-specific release tests use an external authoritative clean source and immutable revision. They test missing `pt-BR`, `en-US`, `es`, and `de` variants, source-manifest divergence, authoritative clean validation without executing candidate validators, reviewer-revision mismatch, machine-surface drift, local graph integrity, and the prohibition against treating unreviewed translations as approved.

Normal source validation must pass without language directories and must not invoke the release-variant validator. Release fixtures also prove that staging needs no language-selection index and that each downloadable variant is independently valid and internally linked.

Local `.obsidian/` state may be recreated by the editor and is ignored by source validation, but clean release-asset inspection must prove it was not packaged.

Release packaging tests cover deterministic ZIP bytes, exact per-language archive roots, manifest inspection, SHA-256 binding, refusal to package forbidden editor/repository/cache state or symlinks, safe replacement boundaries, and the rule that candidate mode tolerates only an `in_review` approval blocker. V0.15.0 layout tests additionally cover source-only exclusions, path collisions, the exact `AGENTS.md` + `FCVW/` payload root, installed required paths, local graph regeneration, extra-root rejection, and proof that removing `FCVW/` preserves an unrelated application file.

## Structural suite

In an installed release the tools live under `FCVW/tools/`; in the framework source checkout they live under the root `tools/`. Use the matching prefix.

```powershell
python -B FCVW/tools/test_validate_fcvw.py
python -B FCVW/tools/test_open_issues.py
python -B FCVW/tools/test_plan_dependencies_and_knowledge.py
python -B FCVW/tools/document_graph_fcvw.py --root .
python -B FCVW/tools/knowledge_graph_fcvw.py --root .
python -B FCVW/tools/role_manifest_fcvw.py --root . --write
python -B FCVW/tools/plan_queue_fcvw.py --root . --recommend
python -B FCVW/tools/validate_fcvw.py --root . --profile clean-template
```

`--since` narrows the per-file rules to the changed files and skips reading the rest; repository-wide rules — graph, queues, identifier uniqueness, release surfaces — keep reading the whole tree, so a scoped run still fails when the tree as a whole is inconsistent.

The language gate is separate and runs only against prepared release artifacts:

```powershell
python -B tools/locale_fcvw.py --root <release-staging-root> --require-complete --source-root <clean-source-root> --source-revision <40-character-commit>
python -B tools/package_release_fcvw.py --root <release-staging-root> --source-root <clean-source-root> --source-revision <40-character-commit> --version <Vx.y.z> --output <asset-directory>
```

## Structural shadow routing

Run `python -B FCVW/tools/test_adaptive_routing.py` in an installed package, or
use the source checkout tool prefix. Replay mandatory immunity, disabled and
shadow CLI equivalence, cumulative explicit routes, missing mandatory failure,
excluded/exact-only content, injection, invalid graph/schema/hash/weights, cycles,
budget bounds and fallback. Synthetic fixtures verify invariants, not task quality.

## Retrieval quality and installed archives

Run the following from a source checkout; installed tools use the FCVW tools directory.

```sh
python -B -m unittest discover -s tools -p 'test_*.py'
python -B tools/benchmark_retrieval_fcvw.py --root . --check
python -B tools/verify_release_fcvw.py --source-root . --smoke --run-tests
python -B tools/verify_release_fcvw.py --source-root . --archive /path/FrameCode-VibeWork-V0.18.0-en-US.zip --checksums /path/SHA256SUMS.txt --run-tests
```

The benchmark contains 12 labeled synthetic cases, including eight session families, exact-only history, injection evidence and cumulative boundaries. Supply `--cases` and `--index` together for external labeled JSONL. The check fails on missing required files, required recall below one, forbidden hits or useful recall below the unbudgeted baseline. Precision and cost remain measured reports, not universal thresholds. Timings exclude route resolution and graph reconstruction.

Archive verification checks SHA-256, paths, size limits, containment and version, then binds installed Python tools to the trusted source before optional execution. Local smoke exercises the installation layout without manufacturing language-review evidence. The [local validation contract](governance/LOCAL_VALIDATION_CONTRACT.md) orchestrates these checks on explicitly selected local interpreters; coverage is limited to the actual host OS. Real-task evaluation is tracked in [issue 55](https://github.com/Sistema2D/FrameCode-VibeWork/issues/55).


## Local validation without hosted services

Available in the source checkout; use the installed tool prefix only in a package that includes this command. V0.18.0 assets remain immutable and do not contain the new runner.

```sh
python -B tools/check_fcvw.py --root .
```

This uses the current interpreter and writes a unique run under `.fcvw-cache/local-checks/`. The report includes every command/log, actual Python and OS, source revision and dirty state, content digest, and pass/fail status. `--output` may select an external directory; inside the source tree only the cache directory is allowed. No logs are uploaded. A nonzero exit blocks acceptance; the tool never silently substitutes an unavailable interpreter or claims Linux coverage from a Windows run.

For two already-installed Windows runtimes:

```powershell
$fcvwPython312 = py -3.12 -c "import sys; print(sys.executable)"
$fcvwPython314 = py -3.14 -c "import sys; print(sys.executable)"
python -B tools/check_fcvw.py --root . --python "$fcvwPython312" --python "$fcvwPython314"
```

Repeat `--python` with executable paths on any supported host. On Linux use an installed Python interpreter and keep the resulting Linux report separately; a local run does not test other operating systems. `--timeout` controls the maximum seconds per direct command, default 900. The runner executes trusted repository code with the user's permissions.

For existing release assets add `--release-dir` pointing to a directory containing exactly four language ZIPs of one version and SHA256SUMS.txt. For older archives, also supply `--release-source` pointing to a trusted checkout of their release tag. This preserves source-code binding rather than skipping it. The runner verifies existing assets; translation review, locale parity and reproducible package construction remain separate release gates. See [the execution contract](governance/LOCAL_VALIDATION_CONTRACT.md).

## Live product QA and wiki integrity

QA must question the user for every expected/actual divergence. Require 100%
consultation coverage and zero pending decisions before acting on a discrepancy;
otherwise checkpoint the affected work and continue only independent tests. The
selected-run checker infers unasked/pending decisions from failed cases even if
their Divergences rows are missing. A decision never changes a historical verdict.

[QA](skills/QA/SKILL.md) first maps the accessible application, then tests and maintains only affected [product surfaces](wiki/product/README.md). Test reports separate approved expected behavior from actual observations and preserve failures. Initial discovery can end in a resumable checkpoint; neither a partial inventory nor source inspection proves live coverage.

Run the optional selected-page checker after writing contracts/runs. It checks stable IDs, element-to-case coverage, complete inventory claims, run contract hashes, missing/duplicate results and evidence fields. It rejects passes for unknown/provisional expectations and stale contracts. It does not browse, authenticate, infer requirements or prove evidence truth. Keep the normal application tests and relevant wiki validation. Missing target execution capability is a blocked result, not an alternative definition of pass. Follow [target guidance](skills/QA/TARGETS.md) for native UI, CLI, APIs, compiled libraries, services and firmware; identify simulation separately from physical hardware coverage.

## Validated-completion evaluation

The optional [loop evaluator](governance/LOOP_EVALUATION_CONTRACT.md) calculates
cost, iterations, rework, timing and quality from explicit external events. Use
`python -B tools/loop_metrics_fcvw.py --protocol /external/protocol.json --runs /external/runs.jsonl --check`
in source, or the installed tools prefix. Missing provider counts remain unknown;
synthetic fixtures and deterministic repository audits do not prove agent efficacy.
The test suite covers exact metrics, resumption/conflicting duplicates, partial
measurements, unknown/unfinished runs, shadow attribution, QA decisions, frozen
identity, output containment and delayed quality. No automatic evaluation is
added to ordinary retrieval or project execution.

## Adaptive control boundary replay

Test [adaptive controls](governance/ADAPTIVE_EXPERIMENT_CONTRACT.md) with synthetic
positive evidence and negative real pilot reassessment. Protect default delivery,
source/index identity, independent evidence, holdout separation, strict feedback
authority, bounded/decayed updates, duplicate/conflict rejection, state replay,
export/reset/rollback, expiry, budgets, stagnation, QA/safety latches and CLI fallback.
These tests establish implementation behavior, not causal efficacy or human authority.
Real provider usage, independent label review, paired execution and follow-up are
still required before interpreting full-cycle savings or non-inferiority.

Cross-tool regressions cover the default local runner's disposable cache,
temporary-file index exclusion, blocked first-run QA inventory, output-directory
creation, known file operations, adaptive ledger restart/stale-state denial and
content-free decision tracing. A filesystem-link upgrade denial test runs on hosts
that permit link creation and is explicitly skipped otherwise. These checks
exercise implementation boundaries; they do not provide real-task efficacy or
cross-operating-system coverage.
