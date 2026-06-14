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
| **Application Module Docs** | `AGENTS.md checklist`, `APPLICATION_DOCUMENTATION.md`, `PLANNING.md` | `governance/TEMPLATE_MODULE_DOCUMENTATION.md`, `governance/TEMPLATE_FLOW_DOCUMENTATION.md` | `DESIGN.md`, `DATA.md`, `RELEASE.md` |
| **UI / Components** | `AGENTS.md §checklist`, `DESIGN.md` | `wiki/patterns/` | `DATA.md`, `SECURITY.md`, `RELEASE.md` |
| **Refactoring** | `AGENTS.md §checklist`, `REFACTORING.md`, `PLANNING.md` | `wiki/refactorings/`, `TESTS.md` | `DESIGN.md`, `DATA.md`, `RELEASE.md` |
| **Code Hygiene / Anti-Monolith** | `AGENTS.md §checklist`, `REFACTORING.md`, `PLANNING.md`, `skill:anti-monolith-guard`, `skill:code-hygiene-refactor` | `TESTS.md`, `APPLICATION_DOCUMENTATION.md`, `wiki/refactorings/` | `DESIGN.md`, `DATA.md`, `RELEASE.md` |
| **Agent / Skill Creation** | `AGENTS.md §checklist`, `AI.md §AI Skills Engine`, `PLANNING.md`, `skill:agent-factory` | `governance/TEMPLATE_AGENT_OR_SKILL_PROPOSAL.md`, `skills/README.md`, `STACK.md` | Unrelated domain docs, release docs |
| **Skill / Agent Self-Improvement** | `AGENTS.md §checklist`, `AI.md §AI Skills Engine`, `PLANNING.md`, `skill:self-improvement` | `AUDIT.md`, `governance/TEMPLATE_SELF_IMPROVEMENT_REPORT.md`, `skills/README.md`, `STACK.md` | Unrelated feature docs |
| **Release** | `AGENTS.md §checklist`, `skill:release-checklist` | `VERSIONING.md`, `AUDIT.md`, `RELEASE.md` | `DESIGN.md`, `REFACTORING.md` |
| **Briefing / Instantiation** | `AGENTS.md §checklist`, `INSTANTIATION.md`, `BRIEFING.md` | `skill:project-instantiation`, `MANIFEST.md`, `STACK.md` | `REFACTORING.md`, `RELEASE.md` |
| **Retroactive Instantiation / Migration** | `AGENTS.md §checklist`, `RETROACTIVE_INSTANTIATION.md`, `INSTANTIATION.md` | `CONTEXT_MAP.md`, `skill:retroactive-instantiation`, `MANIFEST.md`, `STACK.md` | `DESIGN.md`, `REFACTORING.md`, `RELEASE.md` |
| **Wiki / Knowledge** | `AGENTS.md §checklist`, `wiki/schema.md`, `wiki/index.md` | `skill:wiki-lint`, `wiki/log.md` | `DESIGN.md`, `DATA.md`, `SECURITY.md` |
| **Security / Data** | `AGENTS.md §checklist`, `SECURITY.md`, `DATA.md` | `AI.md`, `TESTS.md` | `DESIGN.md`, `REFACTORING.md` |
| **Document Audit** | `AGENTS.md §checklist`, `MANIFEST.md`, `AUDIT.md` | `skill:governance-validator`, `wiki/index.md`, `changelogs/` | `DESIGN.md`, `DATA.md` |
| **Pull Request / Code Review** | `AGENTS.md §Code Review and Pull Requests` | `FCVW/refactoring-guide/17-branch-and-pull-request-policy.md` (if refactoring PR), `PLANNING.md` (risk gates) | Most governance docs |
| **Deploy / Environment Promotion** | `AGENTS.md §checklist`, `ENVIRONMENT.md §5` | `RELEASE.md §Deployment and Environment Promotion`, `skill:release-checklist` (if release) | `DESIGN.md`, `REFACTORING.md`, `AI.md` |
| **Multi-Agent / Collaboration** | `AGENTS.md §Multi-Agent Concurrency` | `FCVW/Plans/in_progress/` (check active plans), `wiki/agents/` (agent journals) | Most governance docs unless crossing domain |
| **Git / Commit / Tag** | `skill:git-conventional-commits` | `VERSIONING.md` | Most governance docs |

---

## Skills Quick Reference

| Skill | Trigger Keywords | Size Saved vs. Full Docs |
|---|---|---|
| `skills/agent-aegis/SKILL.md` | security scan, vulnerability, harden | Focused security-agent checklist |
| `skills/agent-factory/SKILL.md` | create skill, create agent, specialized skill | Controlled creation gate for new skills and agent profiles |
| `skills/agent-hephaestus/SKILL.md` | ux polish, accessibility, improve ui | Focused UX/accessibility-agent checklist |
| `skills/agent-hermes/SKILL.md` | performance, optimize, bottleneck | Focused performance-agent checklist |
| `skills/agnix-linter/SKILL.md` | governance audit, AI instructions, dead links | Validates FCVW structural consistency |
| `skills/aicc-compact/SKILL.md` | shift close, compact session, close session, log sync | Reduces close turn overhead |
| `skills/anti-monolith-guard/SKILL.md` | monolith, large file, new module, module boundary | Blocks mixed-responsibility artifacts before edits |
| `skills/brainstorming-and-tdd/SKILL.md` | new feature, fixing a bug, implementing a plan | Enforces specification and Red/Green workflow |
| `skills/code-hygiene-refactor/SKILL.md` | code hygiene, duplication, stale files, dead code, cleanup | Guides active cleanup without scripts |
| `skills/git-conventional-commits/SKILL.md` | commit, tag, push, release notes | Replaces ad-hoc reinstructions |
| `skills/memory-rotation/SKILL.md` | context bloat, clean sessions, rotate memory | Keeps session memory bounded |
| `skills/obsidian-markdown/SKILL.md` | wikilink, frontmatter, Obsidian note | Replaces ad-hoc formatting instructions |
| `skills/orchestrator/SKILL.md` | large refactoring, complex plans, parallel tasks | Coordinates subagent-style task decomposition |
| `skills/project-instantiation/SKILL.md` | bootstrap, new project, instantiate, initialize | Safely sets up workspace |
| `skills/release-checklist/SKILL.md` | release, publish, version bump | ~2.7k tokens vs. RELEASE+VERSIONING+AUDIT |
| `skills/self-improvement/SKILL.md` | improve skill, improve agent, skill failed | Evidence-based gate for modifying skills and agent profiles |
| `skills/systematic-debugging/SKILL.md` | debugging, fixing an error, stack trace | Enforces hypothesis-based debugging |
| `skills/governance-validator/SKILL.md` | validate governance, verify filesystem, check document integrity, pre-audit check, structural audit | Replaces reading FILESYSTEM.md + AUDIT.md + TESTS.md for validation purposes |
| `skills/wiki-lint/SKILL.md` | lint, wiki audit, orphan pages | ~275 lines vs. reading schema.md §12 |

---

## AICC Session Ingestion Quick Steps

1. List `wiki/sessions/` → identify file with highest `S{num}`
2. Read that file only
3. Align with: completed tasks, active next steps, open risks
4. Confirm alignment to user before starting work

---

## Document Size Reference (V0.10.2)

> Use to make informed decisions about what to load. Larger files cost more tokens.

| Document | Size | Load Priority |
|---|---|---|
| `AGENTS.md` | ~12 KB | Always (first) |
| `REFACTORING.md` | ~14 KB | On demand |
| `skills/anti-monolith-guard/SKILL.md` | ~4 KB | Use for module/file growth gates |
| `skills/code-hygiene-refactor/SKILL.md` | ~4 KB | Use for cleanup/refactoring triage |
| `skills/agent-factory/SKILL.md` | ~4 KB | Use for controlled skill/agent creation |
| `skills/self-improvement/SKILL.md` | ~4 KB | Use for evidence-based skill/agent changes |
| `AI.md` | ~11 KB | On demand (AI sessions) |
| `APPLICATION_DOCUMENTATION.md` | ~4 KB | On demand (application module docs) |
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
