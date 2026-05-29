---
name: Memory Rotation (Garbage Collection)
description: Analyzes the FCVW/wiki/sessions/ directory. If there are more than 10 sessions, it condenses learnings into FCVW/wiki/concepts/ and deletes older raw sessions to prevent context bloat.
---

# 🧠 Memory Rotation & Garbage Collection

## Context
When working with AI agents continuously, the `FCVW/wiki/sessions/` folder acts as the active short-term memory (compressed chronological session synthesis). If this folder accumulates dozens of files, reading the latest context or indexing it becomes excessively costly (Context Bloat), degrading AI inference capabilities and increasing latency/costs.

## When to Use
This skill MUST be executed when you detect that the `FCVW/wiki/sessions/` directory contains more than **10 files**.

## Routine / Execution Steps

1. **Audit Active Memory**:
   - List all files in `FCVW/wiki/sessions/` using your file listing tools.
   - Sort them chronologically (usually by filename numbering `S001`, `S002`, etc.).

2. **Extract Deep Learnings**:
   - Read the old sessions (from the oldest up to the 4th most recent).
   - Identify critical "Deep Learnings": architectural decisions made, persistent bugs fixed, or overarching design changes.
   - Consolidate these learnings.

3. **Transfer to Long-Term Memory**:
   - Inject the consolidated learnings into the appropriate documents inside `FCVW/wiki/concepts/`, `FCVW/wiki/components/`, or update `FCVW/ARCHITECTURAL_DECISIONS.md`.
   - Add back-links if using Obsidian graph view.

4. **Purge (Garbage Collection)**:
   - Delete all the old session files that you just processed.
   - **Keep ONLY the 3 most recent sessions** in `FCVW/wiki/sessions/`. This ensures the next agent starting a task only reads immediate relevant history.
   - Log the garbage collection event in `FCVW/wiki/log.md`.

5. **Report**:
   - Notify the user of how many files were deleted and what major concepts were transferred to long-term memory.
