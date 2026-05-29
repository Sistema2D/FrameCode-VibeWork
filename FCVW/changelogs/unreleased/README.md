# Unreleased Changelog Fragments

This directory stores changelog fragments for completed plans that have not yet been consolidated into a formal release version (e.g., `V1.2.0.md`).

## Methodology

To avoid merge conflicts and data loss when multiple subagents execute tasks in parallel, **do not** directly edit a monolithic version changelog file during the `in_progress` to `completed` transition of a plan.

Instead:
1. When a plan is completed, create a new file in this directory: `FCVW/changelogs/unreleased/{plan-name}.md`.
2. Document the changes concisely in that fragment.

## Release Process

When a formal release is prepared (e.g., triggering the `release-checklist` skill), an agent or script must:
1. Read all fragments in this directory.
2. Consolidate them logically into the official version changelog (`FCVW/changelogs/Vx.y.z.md`).
3. Delete or archive the fragments in this directory.
