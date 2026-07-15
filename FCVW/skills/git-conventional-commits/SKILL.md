---
schema: "fcvw/skill@1"
name: "git-conventional-commits"
description: "Prepare scoped conventional commits, tags, and release messages."
version: "1.2.0"
trigger_keywords:
  - "commit"
  - "tag"
  - "push"
  - "conventional commit"
session_types:
  - "git"
  - "release"
---

# Git conventional commits

## Purpose

Prepare or execute a reviewable Git commit, annotated version tag, push, or release message while preserving scope, version namespaces, and external-action authority.

## Use conditions

Use when the user requests commit-message preparation, staging/commit, tag creation, push, or release-message generation. Load `release-checklist` as well when a version or publication is involved.

## Non-responsibilities

- inferring authority to commit, tag, push, publish, merge, or rewrite history;
- staging unrelated worktree changes;
- choosing an application release record for an FCVW release, or the reverse;
- creating mandatory wiki/session records when no reusable knowledge or policy requires them;
- exposing secrets through diffs, messages, tags, or release notes.

## Inputs

Valid Git worktree, status and diff, active/completed plans, application changelog or framework release record, target branch/remote, target version, validation evidence, and explicit authority for each external mutation.

## Commit format

```text
<type>(<scope>): <short imperative summary>

<optional body describing why and impact>

<optional issue, plan, or BREAKING CHANGE footer>
```

Common types: `feat`, `fix`, `docs`, `refactor`, `test`, `perf`, `build`, `ci`, `chore`, and `revert`. Scope names the smallest stable responsibility, not an agent or temporary filename.

A breaking footer describes the actual compatibility impact and migration, for example:

```text
feat(schema)!: require regression contract in new plans

BREAKING CHANGE: new plans use fcvw/plan@2; plan@1 remains legacy-readable.
```

## Procedure

1. Confirm the directory is a valid Git worktree and inspect branch, remotes, status, staged diff, and unstaged diff.
2. Identify user-owned pre-existing changes and exclude them unless explicitly included.
3. Confirm plan, regression evidence, and application changelog or framework release record are coherent.
4. Scan the intended diff for secrets, generated noise, unresolved conflicts, and out-of-scope paths.
5. Select type/scope and draft a concise imperative summary; add compatibility and issue/plan references only when useful.
6. Stage and commit only when authorized, then verify the resulting commit content and worktree state.
7. For a version tag, confirm semantic version, namespace, release record, target commit, and publication state; create an annotated tag only when authorized.
8. Push branch, tag, or release only with explicit authority and record actual remote evidence separately.

## Required output

Action requested, files included/excluded, commit message, commit identifier when created, tag/version when created, remote action and evidence when performed, validation status, and remaining worktree state.

## Validation

- Commit diff contains only intended paths.
- Message matches the actual change and flags breaking compatibility correctly.
- Application and framework release namespaces are not mixed.
- Tag points to the intended commit and version record.
- External publication is never claimed from a local command alone.

## Exit criteria

Exit when the authorized Git action is verified and residual worktree changes are reported, or when the missing worktree, authority, validation, or release evidence is stated without performing the blocked action.
