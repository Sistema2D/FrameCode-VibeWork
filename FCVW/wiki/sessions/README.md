# AI Session Syntheses & Compressed Contexts

This directory stores the chronologically-ordered compressed context records of AI agent interaction sessions.

## Purpose

To prevent token window bloat, reduce API costs, and guarantee flawless alignment and continuity between sessions, AI agents must not be forced to read extensive chat history or raw logs. Instead, they ingest the latest record in this folder to immediately understand:
1. What was accomplished in the last session.
2. The current logical and visual changes executed.
3. The exact git delta / status.
4. Next actions and immediate handoff tasks.

## Naming Convention

All files in this directory must be chronologically numbered and named using the following pattern:
```text
S{session_number}-{YYYY-MM-DD}-{short-description}.md
```

Examples:
- `S001-2026-05-18-context-compression-proposal.md`
- `S002-2026-05-18-refactoring-database-layer.md`

## Workflow

1. **At Session Start**: The AI agent must read the *latest* session file (highest `session_number`) to ingest the compressed system state.
2. **At Session Close**: Before finishing the turn, the AI agent must create a new session file, incrementing the `session_number` and filling the template based on the active session's progress.
3. **Index & Log**: Update `wiki/index.md` and `wiki/log.md` to reflect the new session synthesis.
