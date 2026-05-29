# CONTEXT_MAP.md

Selective context loading map for AI agents and human contributors.

This document is designed to be the **first document read** in any session — before `AGENTS.md`. It provides a compact, scannable reference for which documents to load (and which to skip) based on session type, minimizing unnecessary token consumption.

> For full operational rules, always consult `AGENTS.md`. This map is a navigation shortcut, not a replacement.

---

## Session Type Reference Table

| Session Type | Load Immediately | Load On Demand | Skip Unless Crossing Domain |
|---|---|---|---|
| **Bugfix / Troubleshooting** | `AGENTS.md §checklist`, `TROUBLESHOOTING.md`, `PLANNING.md` | `troubleshooting/<record>`, `wiki/failures/` | `DESIGN.md`, `DATA.md`, `RELEASE.md` |
| **New Feature** | `AGENTS.md §checklist`, `SCOPE.md`, `PLANNING.md` | `DESIGN.md` (if UI), `AI.md` (if AI), `wiki/index.md` | `SECURITY.md`, `REFACTORING.md`, `RELEASE.md` |
| **UI / Components** | `AGENTS.md §checklist`, `DESIGN.md` | `wiki/patterns/` | `DATA.md`, `SECURITY.md`, `RELEASE.md` |
| **Refactoring** | `AGENTS.md §checklist`, `REFACTORING.md`, `PLANNING.md` | `wiki/refactorings/`, `TESTS.md` | `DESIGN.md`, `DATA.md`, `RELEASE.md` |
| **Release** | `AGENTS.md §checklist`, `skill:release-checklist` | `VERSIONING.md`, `AUDIT.md`, `RELEASE.md` | `DESIGN.md`, `REFACTORING.md` |
| **Briefing / Instantiation** | `AGENTS.md §checklist`, `INSTANTIATION.md`, `BRIEFING.md` | `skill:project-instantiation`, `MANIFEST.md`, `STACK.md` | `REFACTORING.md`, `RELEASE.md` |
| **Wiki / Knowledge** | `AGENTS.md §checklist`, `wiki/schema.md`, `wiki/index.md` | `skill:wiki-lint`, `wiki/log.md` | `DESIGN.md`, `DATA.md`, `SECURITY.md` |
| **Security / Data** | `AGENTS.md §checklist`, `SECURITY.md`, `DATA.md` | `AI.md`, `TESTS.md` | `DESIGN.md`, `REFACTORING.md` |
| **Document Audit** | `AGENTS.md §checklist`, `MANIFEST.md`, `AUDIT.md` | `wiki/index.md`, `changelogs/` | `DESIGN.md`, `DATA.md` |
| **Git / Commit / Tag** | `skill:git-conventional-commits` | `VERSIONING.md` | Most governance docs |

---

## Skills Quick Reference

| Skill | Trigger Keywords | Size Saved vs. Full Docs |
|---|---|---|
| `skills/agent-aegis/SKILL.md` | security scan, vulnerability, harden | Focused security-agent checklist |
| `skills/agent-hephaestus/SKILL.md` | ux polish, accessibility, improve ui | Focused UX/accessibility-agent checklist |
| `skills/agent-hermes/SKILL.md` | performance, optimize, bottleneck | Focused performance-agent checklist |
| `skills/agnix-linter/SKILL.md` | governance audit, AI instructions, dead links | Validates FCVW structural consistency |
| `skills/aicc-compact/SKILL.md` | shift close, compact session, close session, log sync | Reduces close turn overhead |
| `skills/brainstorming-and-tdd/SKILL.md` | new feature, fixing a bug, implementing a plan | Enforces specification and Red/Green workflow |
| `skills/git-conventional-commits/SKILL.md` | commit, tag, push, release notes | Replaces ad-hoc reinstructions |
| `skills/memory-rotation/SKILL.md` | context bloat, clean sessions, rotate memory | Keeps session memory bounded |
| `skills/obsidian-markdown/SKILL.md` | wikilink, frontmatter, Obsidian note | Replaces ad-hoc formatting instructions |
| `skills/orchestrator/SKILL.md` | large refactoring, complex plans, parallel tasks | Coordinates subagent-style task decomposition |
| `skills/project-instantiation/SKILL.md` | bootstrap, new project, instantiate, initialize | Safely sets up workspace |
| `skills/release-checklist/SKILL.md` | release, publish, version bump | ~2.7k tokens vs. RELEASE+VERSIONING+AUDIT |
| `skills/systematic-debugging/SKILL.md` | debugging, fixing an error, stack trace | Enforces hypothesis-based debugging |
| `skills/wiki-lint/SKILL.md` | lint, wiki audit, orphan pages | ~275 lines vs. reading schema.md §12 |

---

## AICC Session Ingestion Quick Steps

1. List `wiki/sessions/` → identify file with highest `S{num}`
2. Read that file only
3. Align with: completed tasks, active next steps, open risks
4. Confirm alignment to user before starting work

---

## Document Size Reference (V0.7.5)

> Use to make informed decisions about what to load. Larger files cost more tokens.

| Document | Size | Load Priority |
|---|---|---|
| `AGENTS.md` | ~12 KB | Always (first) |
| `REFACTORING.md` | ~14 KB | On demand |
| `AI.md` | ~11 KB | On demand (AI sessions) |
| `FCVW/README.md` | ~13 KB | Rarely (framework orientation only) |
| `wiki/schema.md` | ~9 KB | Use `skill:wiki-lint` instead |
| `SECURITY.md` | ~7 KB | On demand (security sessions) |
| `ENVIRONMENT.md` | ~6 KB | On demand (environment sessions) |
| `PERFORMANCE.md` | ~5 KB | On demand (performance sessions) |
| `DESIGN.md` | ~7 KB | On demand (UI sessions) |
| `TESTS.md` | ~7 KB | On demand |
| `MANIFEST.md` | ~11 KB | On demand (audit / identity) |
| `DATA.md` | ~9 KB | On demand (persistence sessions) |
| `SCOPE.md` | ~4 KB | On demand (new feature) |
| `PLANNING.md` | ~3 KB | Most sessions |
| `TROUBLESHOOTING.md` | ~5 KB | Bugfix sessions |
| `VERSIONING.md` | ~5 KB | Use `skill:release-checklist` instead |
| `RELEASE.md` | ~3 KB | Use `skill:release-checklist` instead |
| `AUDIT.md` | ~4 KB | Use `skill:release-checklist` instead |
| `CONTEXT_MAP.md` | ~3 KB | Always first (this file) |

---

## Related Documents

- `AGENTS.md` — full operational guide, checklists, and document index
- `AI.md §Token Efficiency` — detailed token optimization rules
- `skills/README.md` — skills catalog and usage guidelines
- `wiki/sessions/` — AICC session syntheses (latest = current context)
