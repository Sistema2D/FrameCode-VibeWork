# Agent-specific knowledge

This directory stores durable, sourced, project-specific learning produced through specialized agent procedures. Routine narration, raw chat, and per-run status do not belong here.

Rules:

- Use `fcvw/wiki@1` with `type: agent` and a collision-resistant ID.
- This consolidation rule does not apply to `../feedback/`, where a note never overwrites another model's note: consolidated knowledge converges, attributed assessment preserves disagreement.
- Prefer updating an existing canonical page when the learning has the same responsibility and sources.
- Never coordinate parallel writers through one shared fixed journal filename.
- Record sources, confidence, review date, affected boundary, and related plan.
- Do not store secrets, tokens, private logs, or unnecessary personal data.
- Promote cross-agent patterns to the appropriate canonical theme and link the source page.

Suggested filename: `AGENT-YYYYMMDD-<short-id>-<topic>.md`. The filename aids browsing; the frontmatter `id` owns uniqueness.
