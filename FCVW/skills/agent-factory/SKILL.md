---
schema: "fcvw/skill@1"
name: "agent-factory"
description: "Evidence-based gate for creating a new skill or agent profile."
version: "1.1.1"
trigger_keywords:
  - "create skill"
  - "create agent"
  - "new skill"
  - "nova skill"
  - "criar agente"
session_types:
  - "ai_governance"
  - "planning"
---
# SKILL: Agent and Skill Factory

## Purpose

Govern the creation of new skills and specialized agent profiles without allowing uncontrolled proliferation. This skill is a Markdown-only gate: it decides whether a recurring problem deserves a reusable procedural asset, a small checklist inside an existing document, or no new asset.

## Activation Triggers

Load this skill before creating any new file under `skills/` or any new agent profile when:

- a user asks to create a new agent, skill, specialist, persona, command pack, or operational procedure;
- the same task pattern appears repeatedly in plans, sessions, troubleshooting records, or changelogs;
- an existing skill is too broad, too vague, or missing a repeatable procedure for a high-risk task;
- a proposed solution would otherwise add long instructions to `AGENTS.md`, `AI.md`, or another base-loaded document;
- an agent proposes a new role to solve a specific recurring problem.

## Inputs

Recurring task evidence, existing skill/catalog coverage, trigger and responsibility boundary, expected consumers, validation task, maintenance owner, and token/risk ROI estimate.

## Decision Ladder

Use the smallest reusable asset that solves the problem:

| Level | Use when | Output |
|---|---|---|
| Inline checklist | One-off or low-risk clarification. | Add 3-7 bullets to the existing canonical document. |
| Template | Repeated output format is needed, but execution logic is simple. | Add a `governance/TEMPLATE_*.md` file. |
| Skill | A repeatable procedure has clear triggers, gates, validation, and exit criteria. | Add `skills/<name>/SKILL.md`. |
| Agent profile | A bounded role must execute a specialized loop with tools, journals, or handoff. | Add or update a focused `agent-*` skill/profile. |

## Creation Gate

Creation is allowed only when all required metrics pass:

| Metric | Pass threshold |
|---|---|
| Recurrence | At least 2 independent occurrences, or 1 P1/P2 high-risk blocker. |
| Coverage gap | Existing docs/skills cover less than 70% of the needed procedure. |
| Token ROI | Expected initial-context reduction of at least 20%, or avoids adding 500+ words to base-loaded docs. |
| Risk ROI | Reduces a recurrent failure class, compliance risk, data risk, monolith risk, or validation gap. |
| Scope narrowness | One trigger family, one responsibility, one primary output, and one validation path. |
| Validation path | The new asset can be tested against at least one real plan/session/task. |

If any metric fails, do not create a new skill or agent. Patch an existing document or defer with evidence.

## Agent vs Skill Criteria

Create a **skill** when the asset is a procedure any agent can execute.

Create an **agent profile** only when all extra criteria pass:

- the work needs a persistent role boundary, not only a checklist;
- the role has a narrow objective and explicit non-responsibilities;
- the role can produce a measurable artifact or decision;
- the role does not duplicate `orchestrator`, `agent-aegis`, `agent-hermes`, or `agent-hephaestus`;
- the role has a journal or handoff rule when it can run independently.

Do not create persona-only agents, motivational roles, vague "expert" agents, or agents whose only difference is tone.

## Block Conditions

Stop creation when any condition is true:

- the problem is a one-off request with no P1/P2 risk;
- the proposed asset overlaps more than 50% with an existing skill;
- the trigger cannot be stated in concrete keywords or session types;
- the asset has no validation method;
- the asset would encourage broad "do everything" execution;
- the content is mostly style, branding, naming, or personality;
- the proposed instructions should instead be a template field or a plan checklist.

## Output Required

For every allowed creation, create or fill `governance/TEMPLATE_AGENT_OR_SKILL_PROPOSAL.md` and record the compact block below in the active plan:

```markdown
## Agent/Skill Creation Gate

- Skill loaded: `skills/agent-factory/SKILL.md`
- Proposed asset:
- Asset type: `inline checklist` / `template` / `skill` / `agent profile`
- Evidence of recurrence:
- Existing coverage checked:
- Token ROI:
- Risk ROI:
- Scope boundary:
- Validation task:
- Decision: `create` / `patch existing` / `defer`
```

## Exit Criteria

Creation is complete only when the asset has triggers, non-responsibilities, validation criteria, catalog/index updates, changelog entry, and at least one recorded use case.
