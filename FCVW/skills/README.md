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
| [`QA`](QA/SKILL.md) | first-run application mapping, live functional testing and product-wiki maintenance |
| [`agent-aegis`](agent-aegis/SKILL.md) | security and privacy review |
| [`agent-factory`](agent-factory/SKILL.md) | gate for creating a skill or agent |
| [`agent-hephaestus`](agent-hephaestus/SKILL.md) | UI and accessibility review |
| [`agent-hermes`](agent-hermes/SKILL.md) | measured performance investigation |
| [`anti-monolith-guard`](anti-monolith-guard/SKILL.md) | responsibility and size boundaries |
| [`brainstorming-and-tdd`](brainstorming-and-tdd/SKILL.md) | specification and test-first workflow |
| [`code-hygiene-refactor`](code-hygiene-refactor/SKILL.md) | bounded cleanup/refactoring |
| [`git-conventional-commits`](git-conventional-commits/SKILL.md) | commit, tag, and release message preparation |
| [`governance-validator`](governance-validator/SKILL.md) | FCVW conformance, reading-route coverage, clean-template validation, Markdown lint and wiki lint |
| [`obsidian-markdown`](obsidian-markdown/SKILL.md) | portable Markdown/Obsidian formatting |
| [`orchestrator`](orchestrator/SKILL.md) | explicitly authorized parallel coordination |
| [`project-instantiation`](project-instantiation/SKILL.md) | clean project instantiation |
| [`release-checklist`](release-checklist/SKILL.md) | application or framework release |
| [`retroactive-instantiation`](retroactive-instantiation/SKILL.md) | non-destructive adoption |
| [`self-improvement`](self-improvement/SKILL.md) | evidence-based existing-skill change |
| [`systematic-debugging`](systematic-debugging/SKILL.md) | hypothesis-driven diagnosis |
| [`wiki-curator`](wiki-curator/SKILL.md) | sourced promotion, typed relations, stale-source review, session compaction and memory rotation |

## Rules

- A directory and catalog row must exist for every skill.
- Core procedures may describe capabilities, not vendor-specific tool names.
- Provider adapters may translate commands without changing responsibility or exit criteria.
- New skills use `agent-factory`; existing skills use `self-improvement`.
- Trigger overlap is reviewed against the narrowest owning skill.
