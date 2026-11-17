---
schema: "fcvw/adr@1"
id: "ADR-0015"
status: "accepted"
date: "2026-11-13"
artifact_role: "record"
owner: "framework"
upgrade_strategy: "preserve"
record_scope: "framework"
retrieval_scope: "routed"
language: "en-US"
---

# ADR-0015: A validation signal that separates new defects from known debt

## Context

Notes from real use of FCVW in an application (V0.14.0 installed, measured again against V0.23.0) showed a gate that was always red and therefore ignored: the default profile was wrong for instantiated projects, the legacy baseline had no generator and broke when line numbers moved, the graph indexed agent worktrees and `node_modules/` (22,336 nodes instead of 3,510), and `--write` mixed "catalog written" with "repository valid". The same notes showed that `completed` did not mean "criteria met" (171 open boxes), that a criterion deferred in prose was lost by the plan that should have carried it, that a documentation-only commit ran the full product gate set, and that a requested removal left its code behind unless the owner asked twice.

## Alternatives considered

1. Keep the tools and document workarounds (explicit `--profile`, ad hoc scoping scripts, manual baselines).
2. A differential mode that validates the previous git revision and reports only the difference.
3. Make the defaults trustworthy: infer the profile, generate a stable baseline, read one git-aware inventory, define closeout as data, and select gates from the diff.

## Decision

Option 3.

- `--profile auto` is the default. `project-instantiated` in the lock or `instantiation_status: complete` in `PROJECT.md` means `instantiated`; with `FCVW/audits/legacy-baseline.md` it means `incremental`. The reason is printed.
- The baseline is generated (`--write-baseline`), keeps reviewed rows, drops fixed ones, compares messages without line numbers or successor hints, and is summarized by rule instead of listed.
- `context_files` are repository paths, as the consumer always read them. Git's rename history names a proven successor that `--fix-moved-links` applies; a target deleted after a completed plan is history (warning), not a defect.
- One inventory, git-aware, feeds the graph, catalog, knowledge graph and context index. Graph generation and validation have separate states and exit codes; the write is atomic.
- Completed means decided: `[x]`, or `[~]` with `deferred: <plan-id>` carried by the target as `from: <origin-id>`, or `waived: <reason>`.
- Gates are selected from surfaces the project declares; anything undeclared, R4/R5 or a release runs `full`. The tool prints; it does not run.
- A requested removal includes sanitizing the item's exclusive code (`REFACTORING.md` section 26).

## Justification

Option 1 keeps the failure: a gate people learn to ignore. Option 2 hides debt without recording it, doubles the run time and needs a full checkout of the old revision to avoid masking deleted files. Option 3 reuses the existing baseline schema, plan grammar and git's own rename and ignore rules, adds no schema and no runtime, and every new rule has negative fixtures.

## Consequences

- The default command's exit code means "this change introduced a defect"; known debt stays visible as a count with owners and review dates.
- Downstream projects see new `plan-acceptance` findings in completed plans; the baseline absorbs them until reconciled, and new plans cannot repeat them.
- The framework surface grows by about 11 KB of policy text, each paragraph backed by an executable rule; superseded migration steps were removed in exchange.

## Conditions for review

- Baselines prove too costly to maintain compared with a differential mode.
- Real removals close with residue despite a filled sanitization record.
- Declared gate surfaces drift from the code layout often enough to make `full` the usual outcome.

## Relationships

- Plans: [validation signal](../Plans/completed/P2-R3-2026-11-13-validation-signal-and-closeout.md), [graph inventory](../Plans/completed/P2-R3-2026-11-13-graph-inventory-and-generation.md), [gates](../Plans/completed/P3-R2-2026-11-13-proportional-gates.md), [removal](../Plans/completed/P3-R2-2026-11-13-requested-removal-sanitization.md).
- Policies: [Planning](../PLANNING.md#completion), [Tests](../TESTS.md#gate-selection-by-change-surface), [Migrations](../MIGRATIONS.md#legacy-baseline), [Refactoring](../REFACTORING.md).
