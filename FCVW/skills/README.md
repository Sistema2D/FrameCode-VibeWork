---
schema: "fcvw/skill-catalog@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Skills catalog

Skills are provider-neutral, just-in-time procedures using `fcvw/skill@1`. Load only when the trigger and task scope match.

| Skill | Responsibility |
|---|---|
| `agent-aegis` | security and privacy review |
| `agent-factory` | gate for creating a skill or agent |
| `agent-hephaestus` | UI and accessibility review |
| `agent-hermes` | measured performance investigation |
| `agnix-linter` | Markdown/governance lint |
| `aicc-compact` | collision-resistant session handoff |
| `anti-monolith-guard` | responsibility and size boundaries |
| `brainstorming-and-tdd` | specification and test-first workflow |
| `code-hygiene-refactor` | bounded cleanup/refactoring |
| `git-conventional-commits` | commit, tag, and release message preparation |
| `governance-validator` | FCVW conformance, reading-route coverage, and clean-template validation |
| `memory-rotation` | safe archive and knowledge promotion |
| `obsidian-markdown` | portable Markdown/Obsidian formatting |
| `orchestrator` | explicitly authorized parallel coordination |
| `project-instantiation` | clean project instantiation |
| `release-checklist` | application or framework release |
| `retroactive-instantiation` | non-destructive adoption |
| `self-improvement` | evidence-based existing-skill change |
| `systematic-debugging` | hypothesis-driven diagnosis |
| `wiki-curator` | sourced promotion, typed relations, and stale-source review |
| `wiki-lint` | deterministic wiki integrity plus optional bounded semantic review |

## Rules

- A directory and catalog row must exist for every skill.
- Core procedures may describe capabilities, not vendor-specific tool names.
- Provider adapters may translate commands without changing responsibility or exit criteria.
- New skills use `agent-factory`; existing skills use `self-improvement`.
- Trigger overlap is reviewed against the narrowest owning skill.
