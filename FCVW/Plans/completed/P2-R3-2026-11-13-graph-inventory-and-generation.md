---
schema: "fcvw/plan@2"
id: "P2-R3-2026-11-13-graph-inventory-and-generation"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
retrieval_scope: "exact_only"
status: "completed"
priority: "P2"
risk: "R3"
created_at: "2026-11-13"
updated_at: "2026-11-13"
current_version: "V0.23.0"
expected_version: "V0.24.0"
owner: "framework-maintainer"
regression_contract: "required"
context_files:
  - "tools/path_policy_fcvw.py"
  - "tools/document_graph_fcvw.py"
  - "tools/knowledge_graph_fcvw.py"
  - "tools/build_context_index.py"
  - "FCVW/OWNERSHIP.md"
  - "FCVW/TESTS.md"
category: "correction"
depends_on: []
---

# One governed inventory; graph generation separate from validation

## Description

Give every tool that walks governed Markdown one immutable, git-aware inventory, and split the document graph command into generation and validation with their own exit states and an atomic write.

## Justification and objective

Field notes recorded that `document_graph_fcvw.py --write` updated the catalog and exited 1 in the same run, so the exit code did not say whether the catalog was produced; and that a run concurrent with the server tests indexed `.tmp-api-smoke/`, raising the graph from 1,847 to 1,951 nodes with 107 phantom entries. V0.23.0 still mixes both answers in one exit code and walks the whole root excluding only five names. Measured read-only on the same project, V0.23.0 indexes 22,336 Markdown files: 14,039 come from agent worktrees under `.claude/worktrees/`, 1,189 from `node_modules/`. The project's local V0.14.0 copy had patched an exclusion list that an upgrade would have overwritten.

## Scope

### Included

- `path_policy_fcvw.py`: `governed_markdown_inventory` (git's tracked plus untracked-unignored files inside a work tree; otherwise a walk that skips transient trees and nested repositories), transient names, repository globs, project `ungoverned_paths`.
- `document_graph_fcvw.py`: default validation; `--write` generates only; `--write --check` does both on the same inventory; exit 0, 1 (invalid) or 2 (not written); atomic replace.
- `knowledge_graph_fcvw.py` and `build_context_index.py` read the same inventory.
- `OWNERSHIP.md`, `TESTS.md`, `SCHEMAS.md`, `PROJECT.md` (`ungoverned_paths`), `AGENTS.md`, `FCVW/README.md`.

### Excluded

- An incremental graph mode: the validator's baseline already separates new graph findings from known ones.

## Affected files or boundaries

The tools and documents above and the inventory and command tests in `tools/test_validation_signal.py`.

## Implementation plan

1. Shared inventory with git and filesystem modes, contract exclusions and project globs.
2. Route the graph, catalog, knowledge graph and context index through it.
3. Separate command states; atomic write; tests for each exit state.

## Proportionality gate

- Real problem and root cause: each tool walked the tree itself with a short, divergent exclusion list.
- Necessary in current scope: required by the field notes and by any upgrade of the measured project.
- Existing codebase solution checked: extends `path_policy_fcvw.py`, already the shared path policy.
- Native platform capability checked: `git ls-files --cached --others --exclude-standard` applies the project's own ignore rules.
- Installed dependency checked: none.
- New code or complexity justified: about 120 lines.
- Minimum non-trivial behavior tests: transient and nested trees, git ignore, `ungoverned_paths`, glob semantics, three exit states, no partial file.
- Deliberate simplification and limitations: globs, not full gitignore syntax, for `ungoverned_paths`.
- Condition for future evolution: a project need that globs cannot express.
- Mandatory safeguards preserved: tracked files are always governed unless the project declares otherwise; the catalog stays disposable.

## Acceptance criteria

- [x] Transient trees, nested worktrees and git-ignored paths are not graph nodes.
- [x] `--write` reports `catalog_written` and never fails because of graph findings; `--write --check` reports both states.
- [x] An unwritable catalog exits 2 and leaves no partial file.
- [x] Graph, catalog, knowledge graph and context index read the same inventory.

## Dependency validation

None.

## Regression impact

### Existing behaviors that may be affected

- Callers that relied on `--write` failing on graph findings.
- Projects whose governed Markdown is ignored by git (it stops being indexed, as intended).

### Regression contracts consulted

- `FCVW/OWNERSHIP.md` — filesystem layout and disposable outputs.
- `FCVW/TESTS.md` — document graph and queue evidence.

### Regression checks required

- [x] Existing graph, knowledge and retrieval tests.
- [x] New inventory and command tests.
- [x] Read-only field run.

### Regression evidence

| Check | Result | Evidence |
|---|---|---|
| Full suite | pass | 372 tests, 2 skipped, on Python 3.11, 3.12 and 3.14 (Windows) |
| This repository | pass | `document_graph_fcvw.py --root .`: 135 nodes, 0 findings, before and after |
| Field run | pass | 22,336 to 3,510 nodes; graph 40 s to 6.6 s; validator errors 31,342 to 2,921, mostly phantom `document-unreachable` and `document-orphan` nodes |

### Limitations and residual risk

- Tracked application documentation is still governed; a project that does not want it in the graph declares `ungoverned_paths`.

## Validation plan

- [x] `python -B -m unittest discover -s tools -p "test_*.py"`
- [x] `python -B tools/document_graph_fcvw.py --root .` and `--write`

## Rollback

Revert the commit; the catalog is disposable and no project file changes format.

## Gates and approvals

- Regression gate: required and met.

## Related records

- Decision: [ADR-0015](../../decisions/ADR-0015-validation-signal-and-proportional-gates.md).
- Framework release: [V0.24.0](../../framework-releases/V0.24.0.md).

## Validation executed

| Check | Result | Evidence |
|---|---|---|
| Suite, graph, field run | pass | see Regression evidence |

## Gaps and residual risk

None beyond the limitation above.

## Status

`completed`
