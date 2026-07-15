---
schema: "fcvw/skill@1"
name: "self-improvement"
description: "Improve an existing skill or agent from evidence while preserving scope."
version: "1.1.1"
trigger_keywords:
  - "improve skill"
  - "skill failed"
  - "trigger failed"
  - "melhorar skill"
session_types:
  - "ai_governance"
  - "maintenance"
---
# SKILL: Skill and Agent Self-Improvement

## Purpose

Control updates to existing skills and agent profiles so the framework improves from evidence without accumulating noise, redundant rules, or broader prompts. This skill is a Markdown-only refactoring gate for AI operational assets.

## Activation Triggers

Load this skill before changing any `skills/*/SKILL.md`, agent profile, skill catalog, trigger list, or agent-specific operating rule when:

- a skill or agent failed, was ambiguous, did not activate, or produced avoidable rework;
- two or more sessions repeated the same clarification or mistake;
- a validation gap allowed hallucination, duplication, monolith creation, unsafe cleanup, or context loss;
- a new framework rule makes an existing skill incomplete or contradictory;
- a proposed edit claims token savings, better triggers, or safer execution for existing assets;
- the task uses Portuguese equivalents such as melhorar skill, melhorar agente, ajuste de gatilho, gatilho falhou, skill não acionou, agente não acionou, auto melhoria, melhoria de prompt, or regra ambígua.

## Inputs

Concrete failure or drift evidence, owning canonical documents, current skill and catalog entry, overlapping skills, representative replay task, and active plan/change record.

## Improvement Gate

Improvement is allowed only when at least one evidence metric and all safety metrics pass:

| Metric | Pass threshold |
|---|---|
| Failure evidence | 2 independent failures/ambiguities, or 1 P1/P2 incident. |
| Rule drift | A canonical document changed and the skill now contradicts or misses it. |
| Validation gap | Existing exit criteria did not detect a real defect. |
| Token ROI | Expected skill or base-document reduction of at least 15%, or removes repeated clarifying prompts. |
| Scope preservation | The edit narrows or clarifies scope; it does not expand responsibility without `agent-factory`. |
| Backward compatibility | Existing valid triggers and outputs remain valid or have a migration note. |

## Block Conditions

Do not modify a skill or agent when:

- the change is only wording, tone, naming, or preference;
- the evidence is a single low-risk occurrence;
- expected token reduction is below 10% and no risk reduction exists;
- the edit broadens the skill into a catch-all procedure;
- another skill already owns the proposed responsibility;
- the change adds examples that should live in a template, plan, or wiki note;
- the edit changes triggers without checking `skills/README.md`, `CONTEXT_MAP.md`, and `STACK.md`.

## Safe Improvement Sequence

1. Identify the concrete failure, drift, or inefficiency.
2. Check the owning canonical documents and related skills.
3. Decide whether the fix belongs in the skill, a template, `AGENTS.md`, `AI.md`, or a wiki note.
4. Patch the smallest section that changes behavior.
5. Preserve trigger precision and explicit non-responsibilities.
6. Validate with the task that exposed the gap or a representative replay.
7. Update catalogs, indexes, changelog, plan, and session synthesis.

## Output Required

Create or fill `governance/TEMPLATE_SELF_IMPROVEMENT_REPORT.md` and record this compact block in the active plan:

```markdown
## Skill/Agent Self-Improvement Gate

- Skill loaded: `skills/self-improvement/SKILL.md`
- Asset changed:
- Evidence:
- Metric passed:
- Scope preserved:
- Token/risk ROI:
- Validation replay:
- Decision: `patch` / `defer` / `requires agent-factory`
```

## Exit Criteria

The improvement is complete only when the updated asset is more precise, no broader than before, cataloged consistently, validated against evidence, and documented with residual risk.
