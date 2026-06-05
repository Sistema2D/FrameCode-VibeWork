# Agent Journals

This folder stores agent-specific journals.

Official path pattern:

```text
FCVW/wiki/agents/<agent_name>_journal.md
```

Rules:

- Each agent uses one predictable journal file derived from the agent name.
- Journals record durable, codebase-specific learnings, not routine narration.
- Append new entries; do not overwrite previous journal content.
- Do not store secrets, tokens, private logs, or unnecessary personal data.
- Use concise dated entries.
- Journal files should use wiki frontmatter with `type: "agent"` when they are created.
- When a journal entry becomes reusable across agents, promote it to the appropriate wiki folder and link back to the journal entry.

Examples:

```text
FCVW/wiki/agents/aegis_journal.md
FCVW/wiki/agents/hephaestus_journal.md
FCVW/wiki/agents/hermes_journal.md
```
