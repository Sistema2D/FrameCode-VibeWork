# Project Governance Wiki

This folder stores the cumulative technical memory of the project's governance in Markdown format.

The wiki does not replace the official documents of the repository, such as `AGENTS.md`, `PLANNING.md`, `VERSIONING.md`, `TROUBLESHOOTING.md`, `AUDIT.md`, `REFACTORING.md`, `AI.md`, or `DESIGN.md`.

It works as a continuous learning layer: it records validated patterns, recurring failures, consolidated decisions, refactorings, audits, releases, components, useful prompts, open questions, and reusable syntheses.

When the project also has a user/runtime wiki or vault, explicitly differentiate that structure from this governance wiki.

## Principles

1. Raw sources must be preserved.
2. Syntheses must point to their sources.
3. Reusable knowledge must be promoted to its own pages.
4. Hypotheses must not be treated as truths.
5. Obsolete content must be marked as such, not deleted without justification.
6. The wiki must be consulted before making relevant changes.
7. The wiki must be updated after changes that generate reusable learning.
8. The wiki must not store secrets, tokens, private logs, or unnecessary personal data.

## Main Files

- `schema.md`: structural rules of the wiki.
- `index.md`: navigable index of knowledge.
- `log.md`: chronological log of ingestions, syntheses, audits, and linting.
- `inbox/`: unprocessed inputs.
- `raw/`: immutable raw sources.
- `sources/`: normalized or described sources.
- `concepts/`: technical and product concepts.
- `decisions/`: consolidated architectural decisions.
- `patterns/`: approved technical patterns.
- `failures/`: learnings about failures.
- `refactorings/`: refactoring learnings and opportunities.
- `audits/`: recurring audit findings.
- `releases/`: syntheses of published versions.
- `components/`: components, modules, and responsibilities.
- `prompts/`: useful and validated prompts.
- `questions/`: open questions.
- `syntheses/`: cross-cutting syntheses.
- `templates/`: wiki page templates.

## Formal Sources

Preferred formal sources:

- `Plans/completed/`
- `changelogs/`
- `troubleshooting/`
- `decisions/`
- `audits/`
- Root official documents
- Code snippets or documentation used as evidence
