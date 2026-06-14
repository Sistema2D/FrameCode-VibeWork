---
name: "orchestrator"
version: "1.1.0"
trigger_keywords: ["large refactoring", "complex plans", "parallel tasks", "dispatching agents", "multi-agent", "orchestrate"]
session_types: ["refactoring", "maintenance", "document_audit", "multi_agent"]
---

# SKILL: Orchestrator

## Purpose

Coordinate complex plans without pretending unavailable tools exist. The orchestrator is functional in two modes:

- **Delegated mode:** use subagent tools only when the current environment explicitly provides them.
- **Sequential mode:** if no subagent tool exists, split the work into bounded task blocks and execute them one at a time under the active plan.

## Activation Triggers

Load this skill when a plan spans multiple domains, has R3+ risk, mentions parallel work, or requires coordination between security, UX, performance, refactoring, docs, tests, and release.

## Hard Rules

- Do not invent tool names such as `invoke_subagent` if the environment does not expose them.
- Do not open parallel edits against the same soft-locked files.
- Every delegated or sequential task must cite the active plan and affected files.
- Domain agents must load their own `SKILL.md` before acting.
- The main agent remains responsible for review, validation, changelog, and plan closure.

## Workflow

1. Read the active plan and identify independent work packages.
2. Check `Plans/in_progress/` for scope collisions.
3. Select execution mode:
   - delegated mode when subagent tools are available;
   - sequential mode otherwise.
4. For each work package, define:
   - exact files in scope;
   - required skill;
   - behavior to preserve;
   - validation evidence;
   - rollback note.
5. Execute or delegate the smallest safe package first.
6. Review each result against the plan acceptance criteria.
7. Do not close the plan until all packages are validated or explicitly deferred.

## Output Required

Add this block to the active plan:

```markdown
## Orchestration

- Skill loaded: `skills/orchestrator/SKILL.md`
- Execution mode: `delegated` / `sequential`
- Work packages:
  - `<package>`: `<skill>`, `<files>`, `<validation>`
- Collision check:
- Deferred packages:
```
