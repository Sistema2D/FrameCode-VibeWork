---
name: "aicc-compact"
version: "1.0.0"
trigger_keywords: ["shift close", "compact session", "aicc compact", "close session", "consolidate session", "concluir turno", "finalizar sessao", "sintese de sessao"]
session_types: ["wiki_maintenance", "release", "document_audit", "refactoring", "new_feature", "bugfix"]
---

# SKILL: AICC Session Compaction

High-density procedural checklist for performing AI Interaction Context Compression (AICC) at the end of a developmental session or shift. Condenses the handoff workflow to ensure zero context drift between AI runs while minimizing token bloat.

## Activation Triggers

Load this skill (with `view_file` and `IsSkillFile: true`) when:
- The user declares "concluir turno", "finalizar sessão", "close session", "consolidate shift", or similar.
- The active plan reaches completion and is ready to be closed.
- The developer changes IDE contexts or shuts down a coding session.

---

## 1. Context Collection

Before generating the session synthesis, execute these investigative commands or verify manually:
1. Check the git status to retrieve the exact list of modified files.
2. Review all files read or modified during the session.
3. Locate the previous session synthesis in `wiki/sessions/` (e.g. `S005...`) to check outstanding next steps.

---

## 2. Compaction Execution Checklist

### 2.1 File Generation
1. Identify the incremented session number: `S{num}` (e.g., if the last was `S005`, this is `S006`).
2. Create the file in `FCVW/wiki/sessions/S{num}-{description}.md`.
3. Copy [`governance/TEMPLATE_AI_SESSION_SYNTHESIS.md`](../../governance/TEMPLATE_AI_SESSION_SYNTHESIS.md) or [`wiki/templates/TEMPLATE_SESSION_SYNTHESIS.md`](../../wiki/templates/TEMPLATE_SESSION_SYNTHESIS.md) as the starting base.

### 2.2 Text Densification Rules
- **Telegraphic Style:** Write using short, incomplete sentences. Eliminate adjectives, prepositions, polite conversational padding, and verbose descriptions. Let paths and codes speak.
- **Paths as URIs:** Specify relative links for every single file touched (e.g. `[AGENTS.md](../../../AGENTS.md)`).
- **Exact Commits/Tags:** Record the final Git tag, commits, or versions.

### 2.3 Semantic Tags Registration
If the session produced reusable learnings, tag them explicitly:
- `#gold-pattern` -> For validated architectural solutions.
- `#failure-log` -> For troubleshooting logs.
- `#arch-decision` -> For ADR updates.
- `#tech-debt` -> For any technical shortcuts taken that need remediation.

---

## 3. Index and Log Synchronization

- [ ] Add a brief index record in `FCVW/wiki/index.md` pointing to the newly generated `S{num}` page.
- [ ] Add a log entry in `FCVW/wiki/log.md` with format:
  ```markdown
  ## [YYYY-MM-DD HH:MM] shift | Session S{num} Compacted
  - Source: AI Agent Handoff
  - Description: Shift closed. Next steps mapped.
  - Active Plan: <P*-R*-description>
  - Files modified: <list>
  ```

---

## 4. Synthesis Output Format (Telegraphic Standard)

```markdown
---
session: "S{num}"
date: "YYYY-MM-DD"
author: "AI Agent"
active_plan: "Plan-Path"
skills_invoked:
  - "skills/aicc-compact/SKILL.md"
---

# AICC Synthesis: S{num}

## 1. Active State & Focus
- Focus was [Core focus of the shift].
- Previous steps in [S{prev}] were fully resolved.

## 2. Physical Deltas
- **Modified:** [Relative links to modified files]
- **Created:** [Relative links to created files]

## 3. Logical Deltas
- Installed and calibrated [system feature].
- Refactored [module] reducing complexity.

## 4. Technical Memory Tags
- `#gold-pattern` -> [Link to wiki page of the pattern]

## 5. Precise Handoff for Next Session
- [ ] Target task 1.
- [ ] Target task 2.
```
