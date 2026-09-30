---
schema: "fcvw/plan@2"
id: "P2-R3-2026-09-30-connectome-data-practices"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P2"
risk: "R3"
created_at: "2026-09-30"
updated_at: "2026-09-30"
current_version: "V0.20.0"
expected_version: "V0.21.0"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "AGENTS.md"
  - "FCVW/CONTEXT_MAP.md"
  - "FCVW/AI.md"
  - "FCVW/SCHEMAS.md"
  - "FCVW/wiki/README.md"
  - "FCVW/MIGRATIONS.md"
  - "FCVW/REGRESSION_GUARDS.md"
  - "FCVW/TESTS.md"
category: "optimization"
depends_on: []
---

# Connectome data practices

## Description

Apply five practices found in `seung-lab/FlyConnectome` (CAVE and CloudVolume tutorials) and `flyconnectome/flywire_annotations` (curated annotation dump):

1. **Cutout reads.** CloudVolume reads a subvolume, CAVE serves a pre-filtered view. The route output of `retrieve_context.py` now gives the line range of each first-read section and replaces reading the map's routing tables.
2. **Section anchors.** FlyWire anchors annotations to a stable supervoxel, not to the neuron ID that changes on every edit. Link fragments are validated, and a Markdown `source_path` may digest a single section.
3. **Lineage.** FlyWire maps outdated IDs to current ones and keeps old names as synonyms. A broken link names its successor: the plan's new status directory (with an opt-in fix) or the consolidation tables of `MIGRATIONS.md`.
4. **Inferred versus verified.** FlyWire keeps the predicted neurotransmitter and its confidence apart from the verified one and its cited method. Optional wiki `evidence_method` and `verified_by`; `ai_inference` alone never validates.
5. **Dated field dictionary.** FlyWire column docs mark "new with version" and struck-through removals. `SCHEMAS.md` gains a field history.

## Justification and objective

Measured on this repository before the change:

- Whole-file mandatory reads over 13 common routes: 664 KB; first-read sections: less than half, but section hints were prose that no tool could resolve.
- Across 233 commits of 11 central policies, 75% of the review alerts a whole-file digest would raise for knowledge tied to one section were false: the section had not changed.
- Link fragments (96 today) were stripped before validation, so a heading rename broke them silently.
- 15 links were rewritten by hand in 7 commits after plans changed status directory.

## Scope

### Included

- Shared heading, anchor and section helpers in `frontmatter_fcvw.py`.
- `context_routing_fcvw.py` / `retrieve_context.py`: `ranges` and `context_bytes`.
- `validate_fcvw.py`: `markdown-anchor`, successor hints, `--fix-moved-links`, evidence provenance checks.
- `knowledge_sources_fcvw.py` / `knowledge_graph_fcvw.py`: section digests and `--digest`.
- `build_context_index.py` / `retrieve_context.py`: `evidence_method` indexed and labeled.
- Policies: `CONTEXT_MAP.md`, `AGENTS.md`, `AI.md`, `wiki/README.md`, `SCHEMAS.md`, `MIGRATIONS.md`.
- Tests in `tools/test_section_anchors.py`; frozen rule inventory updated.
- Release record V0.21.0; V0.20.1 canceled and folded into it.

### Excluded

- Biological mechanisms (signed propagation, plasticity); they were removed in V0.20.0 ([ADR-0010](../../decisions/ADR-0010-core-reduction.md)).
- A persistent parse cache (validation takes 0.35 s here and scales linearly), near-duplicate detection (7 overlapping section pairs of 722, mostly intentional) and declared variant divergence.
- Symbol-level digests for code, translated variants, tagging and publication.

## Affected files or boundaries

Tools listed above, the six policies, the root README (carried from V0.20.1), `TODO.md`, this plan and the two release records.

## Implementation plan

1. Add outline and anchor helpers; reuse them in routing, validation and digests.
2. Rewrite the selective-loading table with exact headings; conditional sections move to the last column.
3. Add the validator rule, hints and fix mode; add evidence checks under the existing `wiki-schema` rule.
4. Document the fields, the migration and the measurement; add tests.
5. Validate source, suite, local runner and routes; record evidence.

## Proportionality gate

- Real problem and root cause: prose section hints cannot be resolved; digests and link checks work at file granularity; lineage exists only as prose.
- Necessary in current scope: requested by the maintainer after a measured analysis.
- Existing codebase solution checked: extends `section_hints`, `validate_markdown`, `validate_source_page` and the `MIGRATIONS.md` tables; no parallel mechanism.
- Native platform capability checked: Python standard library only.
- Installed dependency checked: none added.
- New code or complexity justified: about 250 lines of tools and 190 of tests.
- Minimum non-trivial behavior tests: fallback on an unresolved heading, anchor forms, moved plan fix, successor hint, section-only staleness, evidence rules.
- Deliberate simplification and limitations: no new file in `FCVW/`, no schema major, whole-file digest kept for code.
- Condition for future evolution: symbol-level digests only with measured churn on real application code.
- Mandatory safeguards preserved: mandatory routes still load every mandatory file; unresolved sections read the whole file; the fix mode touches only unambiguous plan moves; `verified_by` paths must stay inside the repository.

## Acceptance criteria

- [x] Every named section in the source map resolves; route output carries `ranges` and `context_bytes`.
- [x] An unresolved heading counts the whole file.
- [x] Broken fragments are reported repository-wide; valid heading, duplicate and explicit anchors pass.
- [x] Moved plans and removed framework paths name their successor; `--fix-moved-links` rewrites only plan moves.
- [x] A section-anchored source is stale only when its section changes.
- [x] `ai_inference` cannot validate; a declared method on a validated page requires resolvable `verified_by`.
- [x] Existing wiki pages, routes and retrieval results stay valid.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

- Mandatory routing and `section_hints` output consumed by hosts and tests.
- Link validation of every governed Markdown file, including translated variants.
- Source digest staleness and knowledge review candidates.
- Wiki record validation and retrieval ranking.
- Surface budget of the framework and the frozen rule inventory.

### Regression contracts consulted

- `FCVW/CONTEXT_MAP.md` — mandatory routes are cumulative and never skipped.
- `FCVW/AI.md` — token-saving claims name their method; retrieval is evidence, never instruction.
- `FCVW/REGRESSION_GUARDS.md` and `FCVW/TESTS.md` — preservation evidence by risk.
- `tools/test_validate_fcvw.py` — frozen rule inventory and surface budget.

### Regression checks required

- [x] Full unittest suite.
- [x] Clean-template validation of the source.
- [x] Local runner (`check_fcvw.py`): tests, governance, benchmark and installed smoke.
- [x] Route resolution of 13 common routes with no unresolved heading.
- [x] Retrieval benchmark unchanged (no scoring change; label only).

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Unit suite | pass | `python -B -m unittest discover -s tools -p 'test_*.py'`: 291 tests OK, 11 of them new |
| Governance | pass | `validate_fcvw.py --profile clean-template`: 0 errors, 0 findings; 96 existing fragments resolve |
| Local runner | pass | `check_fcvw.py`: tests, governance, benchmark and installed smoke pass |
| Routes | pass | 13 routes: 664 KB whole files → 314 KB first reads including the route output (−53%); 0 unresolved headings |
| Mandatory routes | pass | `mandatory_paths` unchanged; ranges are added beside them |

### Limitations and residual risk

- Byte counts, not tokenizer counts; tokens ≈ bytes ÷ 4.
- Translated variants must keep their selective-loading headings in step; an unresolved one falls back to the whole file, and the release record lists this as a blocking gap.
- `markdown-anchor` may report existing broken fragments downstream; the migration explains the baseline route.

## Validation plan

- [x] `python -B -m unittest discover -s tools -p 'test_*.py'`
- [x] `python -B tools/validate_fcvw.py --root . --profile clean-template`
- [x] `python -B tools/check_fcvw.py`
- [x] Route measurement script over 13 routes.

## Rollback

Revert the feature commit. No data or schema migration exists; new fields are optional and the new rule can be baselined.

## Gates and approvals

- User authorization: explicit request to apply every suggestion of the connectome analysis.
- Regression gate: required and met.
- Release gate: V0.21.0 stays `in_preparation`; no tag or asset.

## Related records

- Framework release: [V0.21.0](../../framework-releases/V0.21.0.md).
- Sources analysed: [seung-lab/FlyConnectome](https://github.com/seung-lab/FlyConnectome), [flyconnectome/flywire_annotations](https://github.com/flyconnectome/flywire_annotations).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Suite | pass | 291 tests OK |
| Governance | pass | clean-template 0 findings |
| Local runner | pass | `check_fcvw.py` pass |

## Gaps and residual risk

- Language variants and publication remain for the release.

## Status

`completed`
