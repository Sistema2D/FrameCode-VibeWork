---
title: "AICC Session Compression Pattern"
type: "pattern"
status: "validated"
confidence: "high"
last_reviewed: "2026-05-22"
related_version: "V0.5.0"
sources:
  - "wiki/sessions/S001-2026-05-18-ai-context-compression-implementation.md"
  - "wiki/sessions/S002-2026-05-18-integrate-token-estimations.md"
  - "wiki/sessions/S003-2026-05-18-implement-skills-engine.md"
  - "wiki/sessions/S004-2026-05-18-align-readme-directory-trees.md"
  - "wiki/sessions/S006-2026-05-18-discontinue-mockups-and-automation-scripts.md"
  - "AI.md"
  - "changelogs/V0.2.0.md"
tags:
  - "#gold-pattern"
  - "#aicc"
  - "#token-optimization"
  - "#session-compression"
---

# AICC Session Compression Pattern

## Summary

The AI Interaction Context Compression (AICC) pattern reduces token consumption by ~77% between sessions by replacing raw chat history re-ingestion with a dense, telegraphic session synthesis document.

## Problem

AI agents lose context between sessions. Re-reading all previous chat history or all governance documents at the start of each session is prohibitively expensive (5,000–8,500 tokens per session type) and error-prone.

## Solution

At the end of each working session, the AI agent creates a compressed synthesis file in `wiki/sessions/S{num}-{date}-{description}.md`. At the start of the next session, the agent reads only the latest synthesis (typically 600–1,200 tokens) instead of re-reading full history.

## Structure

Each synthesis file (`S{num}`) must contain:

1. **Session Metadata** — date, agent identity, objective, workspace version
2. **Compressed Context & Changes** — telegraphic list of files read, modified, created; diff summary
3. **Acquired Technical Memory** — patterns, failures, decisions discovered (`#gold-pattern`, `#failure-log`, `#arch-decision`)
4. **Current Workspace Status** — git delta, tests executed, open risks
5. **Next Steps / Agent Handoff** — checklist of immediate next actions

## Frontmatter Requirements

All session synthesis files must have valid YAML frontmatter at the top of the file (before any Markdown content):

```yaml
---
title: "Session Synthesis: <title>"
type: "synthesis"
status: "validated"
confidence: "high"
last_reviewed: "YYYY-MM-DD"
related_version: "Vx.y.z"
session_number: <integer>
tags:
  - "#session-synthesis"
---
```

> `session_number` must be a sequential integer. Never skip numbers — if a session was aborted, still create a synthesis marked `status: obsolete`.

## Naming Convention

```
S{session_num:03d}-{YYYY-MM-DD}-{kebab-case-description}.md
```

Example: `S007-2026-05-22-framework-optimization-and-ase-expansion.md`

## Token Impact (Measured, V0.2.0–V0.5.0)

| Scenario | Without AICC | With AICC | Savings |
|---|---|---|---|
| Bugfix / Troubleshooting | ~5,000 tokens | ~1,200 tokens | **-76%** |
| New Feature | ~7,000 tokens | ~1,500 tokens | **-78%** |
| UI / Components | ~4,500 tokens | ~1,000 tokens | **-77%** |
| Refactoring | ~8,000 tokens | ~1,800 tokens | **-77%** |

## Writing Style Rules

- Telegraphic, high-density bullet points — no conversational padding
- Use absolute file URIs for all referenced files
- Record `skills_invoked` when skills were loaded during the session
- Prioritize next steps with checkboxes (`- [ ]`) so the next agent can immediately orient

## Related Patterns

- [[patterns/ase-jit-skill-loading]] — complementary JIT skill loading pattern
- [[decisions/adr-0001-pure-markdown]] — architectural decision that underpins this pattern

## Applicable Documents

- `AI.md §AICC` — authoritative specification
- `governance/TEMPLATE_AI_SESSION_SYNTHESIS.md` — canonical template
- `wiki/templates/TEMPLATE_SESSION_SYNTHESIS.md` — wiki copy of the template
