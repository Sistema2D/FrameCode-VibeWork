---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Token and context budget

Token efficiency means loading the smallest evidence set that preserves correctness, safety, and scope.

## Default strategy

1. Read `AGENTS.md` and one `CONTEXT_MAP.md` row.
2. Add the active plan's `context_files` and every matching mandatory event trigger; these routes are cumulative.
3. Prefer current canonical documents over historical sessions.
4. Search archives before opening many files.
5. Load the relevant sections of long policies first, using the section routes in `CONTEXT_MAP.md`.
6. Load a JIT skill instead of several long documents when the skill fully covers the operation.
7. Put detailed evidence in repository records and keep user-facing updates compact.

## Context tiers

| Tier | Content | Default |
|---|---|---|
| Always | user request, AGENTS, context route | yes |
| Active | plan, changed files, directly affected policy | yes |
| Supporting | tests, failure record, decision, recent handoff | as needed |
| Archive | old plans, sessions, releases, logs | search only |

## Guardrails

- Never omit a mandatory event-triggered route—including security, data, AI, public interface, filesystem, automation, release, destructive-action, or approval context—to save tokens.
- Do not load all of `wiki/`, `Plans/`, or `changelogs/` by default.
- Avoid repeating full file contents in plans and session syntheses; link paths and retain decisive evidence.
- Rotate indexes and archive old sessions when active navigation becomes noisy.
- Ask only when missing information materially affects correctness, authority, safety, or product direction.

## Measurement

Token-saving claims must record the model/tokenizer or approximation method, compared context sets, date, and result. Do not publish unsupported percentage savings.

Useful repository metrics:

- bytes/estimated tokens in the default context route;
- number of files loaded per session type;
- archive versus active-memory size;
- repeated clarification count;
- validation defects caused by missing context.
