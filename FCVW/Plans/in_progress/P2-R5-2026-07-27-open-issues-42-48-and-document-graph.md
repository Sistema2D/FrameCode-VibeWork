---
schema: "fcvw/plan@2"
artifact_role: "record"
upgrade_strategy: "preserve"
id: "P2-R5-2026-07-27-open-issues-42-48-and-document-graph"
status: "in_progress"
priority: "P2"
risk: "R5"
created_at: "2026-07-27"
updated_at: "2026-07-27"
current_version: "V0.13.0"
expected_version: "V0.14.0"
owner: "Codex with explicit user approval for implementation and GitHub publication"
record_scope: "framework"
regression_contract: "required"
context_files:
  - "AGENTS.md"
  - "FCVW/CONTEXT_MAP.md"
  - "FCVW/PLANNING.md"
  - "FCVW/SCHEMAS.md"
  - "FCVW/OWNERSHIP.md"
  - "FCVW/REGRESSION_GUARDS.md"
  - "FCVW/TESTS.md"
  - "FCVW/AUDIT.md"
  - "FCVW/AI.md"
  - "FCVW/RELEASE.md"
  - "FCVW/VERSIONING.md"
  - "FCVW/FILESYSTEM.md"
---

# Implement open issues 42-48 and document-graph integrity

Reopened on 2026-07-27 after the pre-release adversarial audit demonstrated false-positive gates in graph relationships, schema validation, queues, retrieval classification, and language-release readiness.

## Description

Implement the seven open framework issues reviewed on 2026-07-27, including plan queues, language-specific release contracts, structured frontmatter, optional lexical retrieval, anti-monolith refinement, application rules, and proportionality checks. Add a cross-cutting document-graph contract so every governed Markdown artifact is reachable and no generated record is orphaned.

Language completeness is a release-production metric only. The source and every installed framework remain one monolingual conventional tree; users choose a language by downloading one independent empty-template variant, with no automatic selection or synchronization.

Implementation remained local while publication gates were blocking. On 2026-07-27 the user approved the four language adaptations and explicitly authorized all remaining steps through GitHub Release publication. Push, tag, Release publication, and related issue closeout are now in scope only after every local gate passes.

## Justification and objective

The current framework validates paths, selected reading routes, and schemas, but does not guarantee incoming links or reachability for every template and generated record. The open issues also expose real gaps in queue consistency, frontmatter parsing, application-rule routing, multilingual distribution, and proportionality governance.

The objective is a coherent published V0.14.0 release whose normative and generated Markdown artifacts form a validated, Obsidian-compatible graph.

## Scope

### Included

- Issues `#42` through `#48` as retrieved from `Sistema2D/FrameCode-VibeWork`.
- Comments on issues `#42` and `#43`.
- Portable Markdown-link graph and orphan detection.
- Optional standard-library tooling and deterministic tests.
- Local release candidate records and migration documentation.

### Excluded

- Force-push, history rewriting, destructive tag replacement, or silent removal of publication evidence.
- Installation of third-party dependencies.
- Claiming external publication or translation review by native speakers.

## Affected files or boundaries

- Root entrypoint, operational index, planning, schemas, ownership, release, filesystem, AI, tests, audit, and governance gates.
- Plan directories and queue files.
- Validator, unit tests, and optional indexing/retrieval tools.
- Existing skills `anti-monolith-guard` and `code-hygiene-refactor`.
- Framework release and migration records.
- External language-specific release staging, asset, and parity rules.

## Implementation plan

1. Establish structured frontmatter parsing and schema helpers.
2. Add document-graph extraction, reachability, backlink, catalog, and orphan validation.
3. Add plan queues and queue-aware planning/validation.
4. Add `APP_RULES.md`, routing, schema, instantiation, and validation.
5. Refine anti-monolith applicability and add proportionality checks without creating a redundant skill.
6. Add optional section indexer and lexical retriever that cannot replace mandatory context routes.
7. Add external language-release staging contracts, explicit variant validation, deterministic packaging, clean artifact rules, and no-runtime-migration documentation.
8. Update release/version surfaces and run R5 validation.



## Proportionality gate

- Real problem and root cause: seven related governance gaps plus the user's explicit no-orphan objective required one coherent compatibility batch.
- Necessary in current scope: yes; the user authorized local implementation after reviewing the open issues.
- Existing codebase solution checked: the validator, context map, planning gates, release templates, and two existing skills were extended instead of replaced.
- Native platform capability checked: Python standard-library parsing, hashing, BM25 math, filesystem traversal, and Markdown links were sufficient.
- Installed dependency checked: no third-party dependency was needed.
- New code or complexity justified: seven small single-purpose modules isolate frontmatter, graph, queue, locale, packaging, indexing, and retrieval concerns without a service or database.
- Minimum non-trivial behavior tests: 62 focused feature/adversarial tests plus 16 validator regressions.
- Deliberate simplification and limitations: no embeddings, vector database, background automation, third-party archive dependency, automatic language selection, or remote publication.
- Condition for future evolution: measured lexical-recall gaps, approved language reviews, or repeated workflow evidence.
- Mandatory safeguards preserved: security, privacy, accessibility, traceability, validation, audit, integrity, documentation, and risk-proportional regression checks remain blocking.

## Acceptance criteria

- [x] Both plan queues exist, follow the issue-comment priority order, and are validator-enforced.
- [x] Frontmatter supports scalars and first-level lists while rejecting duplicate keys and unsupported YAML structures.
- [x] New/touched governed records have coherent ownership, lifecycle, and retrieval metadata.
- [x] Optional lexical retrieval preserves mandatory context, source traceability, and untrusted-content boundaries.
- [x] Anti-monolith size thresholds do not automatically block ordinary documentation.
- [x] Proportionality checks reuse existing gates and do not create a new skill without evidence.
- [x] `FCVW/APP_RULES.md` is routed, preserved, indexed, and validated.
- [x] Language-specific release contracts cover independent `pt-BR`, `en-US`, `es`, and `de` empty-template variants without changing the source or runtime layout.
- [x] Complete external `pt-BR`, `en-US`, `es`, and `de` release folders, candidate archives, and source-bound checksums are present locally.
- [x] Accountable language review is approved for all four variants.
- [x] Every governed Markdown artifact is reachable from an official entrypoint or explicit catalog.
- [x] Every generated record category has an incoming catalog/relationship link and outgoing authoritative relationship, unless a validated schema-based exception applies.
- [x] Standard Markdown links remain portable and create Obsidian backlinks.
- [x] Clean-template validation, adversarial fixtures, and all unit tests pass after correction.
- [x] No remote mutation occurred.

## Regression impact

### Existing behaviors that may be affected

- Plan status/directory validation and clean-template contamination checks.
- Frontmatter interpretation for plans, skills, wiki pages, releases, and canonical documents.
- Reading-route discovery and Markdown link validation.
- Anti-monolith activation and existing skill outputs.
- Root filesystem allowlist, framework release namespace, and downstream installation paths.
- Token and source boundaries for AI retrieval.

### Regression contracts consulted

- `AGENTS.md` — required change flow and closeout.
- `FCVW/SCHEMAS.md` — compatibility and legacy preservation.
- `FCVW/OWNERSHIP.md` — replacement and preservation boundaries.
- `FCVW/REGRESSION_GUARDS.md` — blocking conditions and R5 evidence.
- `FCVW/TESTS.md` — filesystem, AI, governance, and release evidence.
- `FCVW/AI.md` — instruction hierarchy and retrieved-content trust boundary.
- `FCVW/RELEASE.md` — clean artifacts and publication truth.
- `FCVW/FILESYSTEM.md` — source-of-truth paths.

### Regression checks required

- [x] All 16 validator regression tests.
- [x] Structured-frontmatter positive and negative fixtures.
- [x] Queue missing, stale, duplicate, wrong-state, and valid fixtures.
- [x] Link graph valid, broken, orphan, unreachable, self-only, wikilink, and catalog fixtures.
- [x] APP_RULES duplicate/malformed/valid fixtures.
- [x] Anti-monolith documentation and code scenarios.
- [x] Retrieval route precedence, exclusion, source, and prompt-injection fixtures.
- [x] Language-variant structure/parity, source decoupling, and clean-package fixtures.
- [x] Full clean-template validator and local file/status review.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Existing clean-template validator | pass | Pre-change: `errors=0 findings=0` |
| Existing unit suite | pass | Pre-change: 14 tests passed |
| Post-change validation | pass | 16 validator + 62 feature/adversarial tests; source clean validator 0/0; source graph 191/3/0; every candidate graph 192/3/0 |
| Pre-publication boundary | pass | Candidate revisions remained local through approval; no external state was claimed before authorization and blocker-free validation |

### Limitations and residual risk

- The repository owner explicitly approved every language adaptation; this establishes accountable acceptance but does not claim professional certification or native-speaker review.
- No multilingual filesystem migration exists: the source and installed tree stay monolingual, while the four external release candidates remain independent.
- Obsidian behavior is validated through portable link semantics and graph rules, not through automating the Obsidian desktop application.

## Validation plan

- [x] `python -B tools/test_validate_fcvw.py`
- [x] `python -B tools/validate_fcvw.py --root . --profile clean-template`
- [x] Compile optional Python tools without writing bytecode.
- [x] Inspect document graph report for zero blocking orphans.
- [x] Run explicit language-release staging gates and verify package, revision, and review blockers without coupling them to normal source validation.
- [x] Confirm `git status` contains only planned local changes.

## Rollback

Before publication, stop without creating external state if a gate fails. After publication, preserve the release evidence and correct defects through a follow-up patch release or an explicit revert commit from restoration source `16ea5c2`. Removing a published Release or tag, rewriting history, or performing a destructive reset requires separate explicit authorization.

## Gates and approvals

- Regression gate: required, R5.
- Security/data/refactoring/skill/release gate: AI, filesystem, skill self-improvement, release, and migration gates apply.
- Decomposition required: implementation is phased with validation after each foundational boundary.
- Human approval: the user explicitly authorized local implementation, approved all four language adaptations, and authorized every remaining step through GitHub Release publication on 2026-07-27.

## Anti-Monolith Gate

- Skill loaded: `skills/anti-monolith-guard/SKILL.md`
- Target artifact: framework policies, validator, and optional tools.
- Artifact class: source modules, operational instructions, canonical documentation, and generated records were classified separately.
- Numeric threshold applicability: applicable to Python modules, warning-only for operational skills, and not applicable to cohesive policies/records/templates.
- Primary responsibility: each executable module owns one bounded parsing, validation, indexing, or retrieval concern.
- Explicit non-responsibilities: no provider integration, background service, vector database, or automatic publication.
- Size budget: split parser, graph, indexer, and retriever rather than expanding the existing validator into a catch-all.
- Similar code checked: existing validator helpers and skills were reviewed.
- Split decision: `proceed`.
- Validation: focused unit modules plus full governance validation.

## Skill/Agent Self-Improvement Gate

- Skill loaded: `skills/self-improvement/SKILL.md`
- Asset changed: `anti-monolith-guard` and `code-hygiene-refactor`.
- Evidence: issue #46 identifies false-positive scope; issue #48 identifies overlapping proportionality coverage.
- Metric passed: canonical-rule drift and scope clarification.
- Scope preserved: thresholds are narrowed to applicable artifacts; no new catch-all responsibility is added.
- Token/risk ROI: removes repeated exceptions for ordinary documentation and avoids a redundant new skill.
- Validation replay: pass in `test_proportionality_and_document_classification_are_contractual` plus full skill-contract validation.
- Decision: `patch`.

## Agent/Skill Creation Gate

- Skill loaded: `skills/agent-factory/SKILL.md`
- Proposed asset: anti-overengineering skill.
- Asset type: `inline checklist`.
- Evidence of recurrence: one open issue; existing policies cover most of the decision process.
- Existing coverage checked: planning, refactoring, anti-monolith, code hygiene, governance gates.
- Token ROI: a new skill would duplicate existing context.
- Risk ROI: existing gates can cover the gap.
- Scope boundary: proportionality only when new technical complexity is introduced.
- Validation task: representative plan/gate fixtures.
- Decision: `patch existing`.

## Related records

- Changelog/framework release: [V0.14.0](../../framework-releases/V0.14.0.md).
- Decisions: [ADR-0003](../../decisions/ADR-0003-proportionality-and-contextual-anti-monolith-gates.md) and [ADR-0004](../../decisions/ADR-0004-multilingual-source-and-release-model.md).
- Failure/regression: none at plan start.
- Other plan: none.

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Pre-change clean validator | pass | 0 errors, 0 findings |
| Pre-change unit suite | pass | 14/14 |
| Validator regression suite | pass | `python -B tools/test_validate_fcvw.py`: 16/16 |
| Feature/adversarial suite | pass | `python -B tools/test_open_issues.py`: 62/62 |
| Python syntax | pass | 10 tool/test modules parsed through `ast` without bytecode |
| Document graph | pass | 191 nodes, 3 entrypoints, 0 findings |
| Plan queues | pass | reopened correction is the first valid `in_progress` recommendation |
| Language-release staging | pass | Four complete independent folders; 206 source files and 207 files per candidate; schema, machine surface, heading/list/table/quote structure, links, and language metadata are parity-checked |
| Language-release gate | pass | Repository-owner approval recorded in all four `LANGUAGE_REVIEW.md` files; explicit release validator reports 0 errors and 0 findings |
| Approved-package preflight | pass | Four approved ZIPs plus external `SHA256SUMS.txt` generated without `--allow-in-review`; final assets will be rebuilt from the tagged ready revision |
| Candidate packages | pass | Four deterministic pre-approval ZIPs plus external `SHA256SUMS.txt`; two builds were byte-identical |
| Extracted packages | pass | Every exact-root archive extracted to 207 files and passed clean-template 0/0 plus graph 192/3/0 |
| Clean-template validator | pass | 0 errors, 0 findings |
| Patch integrity | pass | `git diff --check` exit 0; only line-ending conversion notices |
| Local Obsidian state | pass | `.obsidian/` absent, ignored if recreated locally, excluded by release-tree validation |
| Local-only boundary | pass | Local candidate baseline `c9ac95c`; origin remains unmodified; no tag or remote mutation |
| Pre-release adversarial audit | fail | False-positive graph, queue, schema, retrieval, locale, and release-readiness cases reproduced; plan reopened |
| Second adversarial audit | pass after correction | Candidate-validator execution, unbounded retrieval, absent mandatory sources, unenforced wiki/audit/application schemas, self-referential release revisions, lock-state circularity, and truncated application-release template were reproduced and corrected |
| Third adversarial audit | pass after correction | Automatic language-layout coupling, inferred document language, non-failing missing context, duplicate chunk IDs, repository/editor package leakage, non-Markdown drift, checksum/asset decoupling, unscoped clean history, weak troubleshooting records, nested-fence parsing, fenced release headings, and non-portable Markdown links were reproduced and corrected |

### Superseded pre-approval candidate checksum evidence

- `FrameCode-VibeWork-V0.14.0-de.zip`: `554de70c4cb5ee2bab67e4b609eb0829a084d887e7094ec7f4417329746205f3`
- `FrameCode-VibeWork-V0.14.0-en-US.zip`: `196a8fd1a3d1b2f5ce2936c7b1ee07441e4ddb023987d04bdcf01440f3c2fd03`
- `FrameCode-VibeWork-V0.14.0-es.zip`: `c65cae0c34e397fb18b7eb73164f58d50eaca56c333325f5a110113cd9fcddc0`
- `FrameCode-VibeWork-V0.14.0-pt-BR.zip`: `681943409829edbe14523157a667b4c9450bc7782d69e99cae84349e1446bd26`

The former candidate `SHA256SUMS.txt` contained the same values and was reproduced byte-for-byte in a second build. These hashes are historical pre-approval evidence and are not the final release checksums.

## Gaps and residual risk

- External `pt-BR`, `en-US`, `es`, and `de` empty-template folders and approved preflight ZIPs exist locally; no language or content blocker remains.
- The final deterministic archives and checksums must be rebuilt from the tagged `ready` revision before publication.
- Obsidian desktop itself was not automated; compatibility is established through portable relative links, incoming-link validation, reachability, zero graph findings, ignored local `.obsidian/` state, and a release-tree exclusion check.
- The adversarial fixtures and approved-language gate pass. The only remaining lifecycle work is final ready-revision packaging, external publication, remote issue closeout, and post-publication evidence.
