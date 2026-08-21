---
schema: "fcvw/plan@2"
artifact_role: "record"
upgrade_strategy: "preserve"
record_scope: "framework"
id: "P2-R4-2026-08-21-plan-dependencies-and-typed-knowledge"
status: "completed"
priority: "P2"
risk: "R4"
created_at: "2026-08-21"
updated_at: "2026-08-21"
current_version: "V0.14.0"
expected_version: "V0.15.0"
owner: "Codex under the user's implementation authorization"
regression_contract: "required"
context_files:
  - "AGENTS.md"
  - "FCVW/CONTEXT_MAP.md"
  - "FCVW/PLANNING.md"
  - "FCVW/SCHEMAS.md"
  - "FCVW/OWNERSHIP.md"
  - "FCVW/MIGRATIONS.md"
  - "FCVW/REGRESSION_GUARDS.md"
  - "FCVW/TESTS.md"
  - "FCVW/AI.md"
  - "FCVW/SECURITY.md"
  - "FCVW/AUDIT.md"
  - "FCVW/FILESYSTEM.md"
  - "FCVW/RELEASE.md"
  - "FCVW/VERSIONING.md"
  - "FCVW/wiki/schema.md"
  - "FCVW/MEMORY.md"
---

# Plan dependencies and typed knowledge

## Description

Implement the applicable outcomes of GitHub issues #49, #50, and #51: durable plan dependencies with evidence-backed unblocking, a bounded aggregate queue view, typed and source-aware wiki knowledge, a separate derived knowledge graph, deterministic stale-source findings, richer context metadata, bounded graph-aware retrieval, and optional review-only semantic lint.

## Justification and objective

The current queue can block work but does not preserve dependency rationale, criteria, or satisfaction evidence in the plan. The wiki already has strong routing, lexical retrieval, sources, and lifecycle controls, but its relationship model and provenance validation are less expressive. The objective is to close those gaps without replacing the two canonical queues, BM25, the document graph, JIT loading, or Markdown/Git authority.

## Scope

### Included

- Additive `fcvw/plan@2` dependency fields and a parseable dependency-validation section.
- Cycle, state, queue-parity, invalidation, and evidence validation.
- Optional aggregate queue output generated from the two canonical queues.
- Additive `fcvw/wiki@1` typed relationships, maturity, source provenance, and derived staleness.
- Separate disposable knowledge-graph generation and validation.
- Context-index metadata and bounded one-hop graph expansion after BM25.
- Optional source-bounded semantic review that never mutates canonical knowledge.
- Documentation, templates, skills, migration, release record, and deterministic tests.

### Excluded

- One canonical shared queue, symlinks, a `plan-queue@2` migration, embeddings, vector databases, autonomous knowledge mutation, committed cache files, broad wiki crawling, and release publication.

## Affected files or boundaries

- Planning, schemas, migration, memory, AI, tests, filesystem, ownership, and audit policies.
- Plan and wiki templates, `wiki-curator`, and `wiki-lint`.
- Queue, validation, context-index, retrieval, and new knowledge-graph/stale-review tools.
- Framework release and document-graph records.

## Implementation plan

1. Extend plan dependencies and queue validation while preserving the two state queues.
2. Add typed wiki relations, maturity, provenance metadata, stale detection, and a derived graph.
3. Extend indexing and retrieval with explicit metadata filters and bounded graph expansion.
4. Add optional semantic-review procedure and update affected skills.
5. Add migration/release records, tests, regenerated catalogs, and R4 validation.

## Proportionality gate

- Real problem and root cause: current queue blockers lose durable rationale/evidence; wiki frontmatter cannot express or validate semantic provenance edges.
- Necessary in current scope: yes, explicitly requested after issue analysis.
- Existing codebase solution checked: extend `plan_queue_fcvw.py`, `frontmatter_fcvw.py`, `build_context_index.py`, `retrieve_context.py`, and `validate_fcvw.py`; preserve both queues and the document graph.
- Native platform capability checked: Python standard library and flat YAML-compatible frontmatter are sufficient.
- Installed dependency checked: no third-party dependency is required.
- New code or complexity justified: one bounded knowledge-graph module owns semantic edges and stale checks so the document graph and main validator do not gain a second responsibility.
- Minimum non-trivial behavior tests: dependency cycles/evidence/invalidation; typed targets/inverses; stale source digest; metadata indexing/filtering; bounded graph expansion; injection-safe semantic review.
- Deliberate simplification and limitations: one-hop expansion, flat metadata, derived staleness, no shared canonical queue, no generated index tree, no embeddings, no automatic semantic decisions.
- Condition for future evolution: measured retrieval failures or real downstream scale demonstrating that bounded lexical/graph retrieval is insufficient.
- Mandatory safeguards preserved: instruction hierarchy, source traceability, deterministic release gates, project-owned record preservation, and token limits.

## Acceptance criteria

- [x] Plans can declare blocking prerequisites without conflating non-blocking relations.
- [x] Dependency cycles, missing IDs, discontinued prerequisites, and evidence-free unblocking fail deterministically.
- [x] Queue blockers agree with unresolved plan dependencies.
- [x] In-progress work remains preferred and an aggregate view is disposable, not canonical.
- [x] Wiki pages can express and validate typed relations to wiki IDs or governed Markdown paths.
- [x] Maturity remains separate from status, confidence, and authority.
- [x] Source pages can track provenance and digests without colliding with chunk hashes.
- [x] Changed tracked sources produce review findings without modifying knowledge.
- [x] A separate reconstructible knowledge graph is available outside canonical data.
- [x] Context chunks expose relevant knowledge metadata.
- [x] Retrieval can filter metadata and expand selected relations by at most one bounded hop.
- [x] Semantic lint is optional, source-bounded, review-only, and never a deterministic gate.
- [x] Existing routing, BM25, authority, freshness, document graph, and queue behavior remain protected.
- [x] Skills and templates agree with canonical contracts.
- [x] Migration, release, graph, tests, and clean-template validation pass.

## Regression impact

### Existing behaviors that may be affected

- Queue parsing, recommendation order, blocker lifecycle, and legacy plans without dependencies.
- Wiki schema validation, relationship path resolution, source hashes, and downstream preserved records.
- Context index shape, BM25 ranking, excerpt limits, mandatory routing, and untrusted-content handling.
- Clean-template filesystem allowlist, document reachability, and skill contracts.

### Regression contracts consulted

- [Planning](../../PLANNING.md) — plan lifecycle, queues, and compatibility.
- [Schemas](../../SCHEMAS.md) — flat frontmatter, additive fields, and preserved history.
- [Regression guards](../../REGRESSION_GUARDS.md) — R4 completion evidence.
- [AI](../../AI.md) — retrieval, instruction hierarchy, and memory boundaries.
- [Tests](../../TESTS.md) — structural, AI, and negative fixtures.
- [Ownership](../../OWNERSHIP.md) — project-owned plan/wiki records and disposable outputs.

### Regression checks required

- [x] Existing queue and recommendation fixtures.
- [x] Existing frontmatter, wiki, graph, and clean-template fixtures.
- [x] Existing BM25 authority/freshness/active-plan behavior and output bounds.
- [x] New negative fixtures for cycles, invalidation, stale source, relation targets, and graph bounds.
- [x] Full unit suite, clean-template validator, document graph, syntax, and diff checks.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Pre-change clean validator | pass | `python tools/validate_fcvw.py --root . --profile clean-template`: 0/0 |
| Pre-change unit suite | pass | 78 tests passed |
| Post-change checks | pass | 87 tests; clean validator 0/0; document and knowledge graphs clean; AST and diff checks pass |

### Limitations and residual risk

- Real downstream knowledge volume is absent from the clean baseline; graph-retrieval utility will be validated structurally, not claimed from production recall metrics.

## Validation plan

- [x] `python -m unittest discover -s tools -p 'test_*.py'`
- [x] `python tools/validate_fcvw.py --root . --profile clean-template`
- [x] `python tools/document_graph_fcvw.py --root . --write`
- [x] Python AST/syntax validation for every tool.
- [x] `git diff --check` and scoped status review.

## Rollback

Revert the bounded local change set before publication. Preserve downstream project-owned plans and wiki pages; remove only new framework-owned policies/tools/templates and restore the V0.14.0 contracts. No tag, push, release, or external issue mutation is authorized.

## Gates and approvals

- Regression gate: required, R4.
- Security/data/refactoring/skill/release gate: AI, filesystem, schema/migration, self-improvement, anti-monolith, governance-validator, and framework-release preparation apply.
- Decomposition required: bounded modules and phased validation; no monolithic validator expansion.

## Anti-Monolith Gate

- Skill loaded: `skills/anti-monolith-guard/SKILL.md`
- Target artifact: plan dependency logic, knowledge graph/stale checks, context index, and retrieval.
- Primary responsibility: keep operational plan ordering, semantic knowledge edges, indexing, and retrieval as separate capabilities.
- Artifact class: `source` and `operational instruction`.
- Numeric threshold applicability: applicable to Python modules; warning only to skills.
- Explicit non-responsibilities: no vector search, background service, autonomous curation, or canonical aggregate queue.
- Size budget: prefer one new semantic-graph module below the general 400-line block threshold; patch existing focused modules only in their owned boundary.
- Similar code checked: document graph, queue validator, frontmatter parser, context indexer, and retriever.
- Split decision: `proceed`.
- Validation: focused unit fixtures plus full governance validation.

## Code Hygiene Scan

- Skill loaded: `skills/code-hygiene-refactor/SKILL.md`
- Scan level: `systemic` within the affected framework tooling.
- Duplicate candidates: relationship target resolution and queue dependency state derivation.
- Large/monolithic candidates: `validate_fcvw.py` is already large; semantic graph logic must remain outside it.
- Dead/stale candidates: redundant canonical aggregate queue and committed hierarchical indexes are deliberately excluded.
- Cleanup batch selected: reuse frontmatter helpers and centralize semantic graph/stale logic in one bounded module.
- Behavior preservation evidence: existing tests plus new compatibility fixtures.
- Deferred debt: repository-wide validator decomposition is audit-only and outside this functional batch.

## Code Hygiene Report

### Scope and inventory

- Systemic scan of affected Python tooling, tests, governed Markdown contracts, templates, and generated catalogs.
- Largest Python artifacts after the change: `validate_fcvw.py` (2,040 lines), `test_open_issues.py` (1,458), `locale_fcvw.py` (545), `plan_queue_fcvw.py` (365), and `knowledge_graph_fcvw.py` (347).

### Findings and cleanup selected

- Plan dependency parsing and state evaluation were extracted to `plan_dependencies_fcvw.py`; `plan_queue_fcvw.py` retains queue ownership only.
- Tracked-source digest and review logic were extracted to `knowledge_sources_fcvw.py`; `knowledge_graph_fcvw.py` remains below the 400-line source warning threshold.
- The aggregate queue is generated from the two canonical queues, eliminating a third writable source of truth.
- Knowledge metadata is additive and its graph is disposable, avoiding parallel canonical stores or a schema-major rewrite.
- Semantic lint is contract-tested as source-bounded, non-mutating, optional, and non-gating.

### Behavior preservation evidence

- Baseline: clean validator 0/0 and 78 tests.
- Closeout: 87 tests, clean validator 0/0, zero knowledge/document graph findings, all Python ASTs valid, and no diff whitespace errors.

### Deferred debt

- `validate_fcvw.py` is a 2,040-line catch-all validator and should be decomposed by contract domain behind characterization tests.
- `test_open_issues.py` is a 1,458-line historical test aggregation and should be split into domain suites without losing regression names.
- Path/reference policy is spread across document, validation, and knowledge modules; a narrow shared resolver may reduce drift after characterization coverage exists.
- `wiki/metrics.md` is marked generated but has no deterministic generator; either add a bounded generator or reclassify it as a preserved project profile.
- The clean baseline has no populated knowledge corpus, so recall gains and semantic-review precision remain unmeasured rather than assumed.

## Skill/Agent Self-Improvement Gate

- Skill loaded: `skills/self-improvement/SKILL.md`
- Asset changed: `wiki-curator` and `wiki-lint`.
- Evidence: canonical wiki contracts gain typed relations, source digests, derived staleness, and optional semantic review that the existing skills do not cover.
- Metric passed: rule drift and validation gap.
- Scope preserved: curation remains source-bounded and lint remains review-only; no new skill is created.
- Token/risk ROI: prevents broad wiki crawling and silent stale/semantic mutation while reusing existing skills.
- Validation replay: skill-contract validation plus focused policy assertions.
- Decision: `patch`.

## Related records

- Framework release: [V0.15.0](../../framework-releases/V0.15.0.md).
- Self-improvement report: [typed wiki skills update](../../audits/2026-08-21-typed-wiki-skills-self-improvement.md).
- GitHub issues: [#49](https://github.com/Sistema2D/FrameCode-VibeWork/issues/49), [#50](https://github.com/Sistema2D/FrameCode-VibeWork/issues/50), and [#51](https://github.com/Sistema2D/FrameCode-VibeWork/issues/51).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Unit suite | pass | 87 tests passed |
| Knowledge graph | pass | nodes=0, edges=0, errors=0, findings=0 on the clean baseline |
| Document graph | pass | generated catalog reports zero findings |
| Queue/dependencies | pass | canonical queues and dependency parity report zero findings |
| Clean validator | pass | profile `clean-template`, errors=0, findings=0, baseline=0 |
| Syntax and diff | pass | 14 Python ASTs valid; `git diff --check` has no whitespace errors |

## Gaps and residual risk

- No blocking implementation or validation gap remains.
- Production-corpus retrieval recall, semantic precision, and token cost require downstream measurement.
- Deferred code-hygiene findings are recorded above and do not change current behavior.
