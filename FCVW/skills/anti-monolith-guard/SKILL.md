---
name: "anti-monolith-guard"
version: "1.0.0"
trigger_keywords: ["monolith", "monolito", "large file", "large module", "new module", "new component", "new service", "module boundary", "mixed responsibilities", "oversized file"]
session_types: ["new_feature", "refactoring", "retroactive_instantiation", "application_module_docs"]
---

# SKILL: Anti-Monolith Guard

## Purpose

Prevent AI agents from creating or expanding monolithic files, components, routes, services, prompts, or modules. This is a Markdown-only gate: it blocks unsafe structure through explicit checklist decisions, not scripts.

## Activation Triggers

Load this skill before implementation when any condition is true:

- creating a new feature, page, route, service, component, model, prompt pack, worker, or module;
- editing a file already considered large or mixed-responsibility;
- adding a second responsibility to an existing file;
- copying a similar block because "it is faster";
- retroactive instantiation finds a large application file without clear ownership;
- the plan uses vague scope such as "implement dashboard", "build backend", "create full app", or "add whole flow".

## Hard Gates

Stop and split the work before editing if any gate fails:

| Gate | Pass condition | If it fails |
|---|---|---|
| Single responsibility | The file has one primary reason to change. | Split into module, service, component, adapter, or utility. |
| Boundary named | Inputs, outputs, owner, and public contract are stated. | Create a module boundary note using `governance/TEMPLATE_MONOLITH_GATE.md`. |
| Size budget | Planned file growth is small and reviewable. | Split the plan or create extraction task first. |
| Duplication check | Similar code was searched and reused or centralized. | Load `code-hygiene-refactor` before adding code. |
| Test/validation path | There is a specific validation for the new boundary. | Do not proceed beyond planning. |
| No catch-all file | Names like `utils`, `helpers`, `manager`, `service`, or `index` have a precise scoped role. | Rename or split by capability. |

## Recommended Size Budgets

These are governance thresholds, not universal language rules. A project may override them in `STACK.md` or `APPLICATION_DOCUMENTATION.md`.

| Artifact | Warning | Block unless justified |
|---|---:|---:|
| Function / method | 40 lines | 80 lines |
| UI component / screen section | 180 lines | 300 lines |
| Route / controller / handler | 120 lines | 220 lines |
| Service / use case | 180 lines | 300 lines |
| Prompt or agent instruction file | 180 lines | 300 lines |
| General module file | 250 lines | 400 lines |

If a file crosses the warning threshold, record the reason in the plan. If it crosses the block threshold, split first or document why a temporary exception is safer.

## Boundary Pattern

Every new non-trivial module must answer in the active plan:

- **Responsibility:** one sentence.
- **Owns:** data, state, UI, side effects, or external calls it owns.
- **Does not own:** responsibilities explicitly excluded.
- **Inputs:** public inputs, events, parameters, messages, files, or context.
- **Outputs:** return values, rendered UI, emitted events, written files, or API responses.
- **Collaborators:** direct dependencies only.
- **Validation:** exact tests, checks, or manual evidence.

## Allowed Splits

Prefer the smallest split that removes real coupling:

- UI shell vs. presentational component.
- Route/controller vs. domain use case.
- Domain rule vs. adapter/integration.
- Data schema vs. persistence implementation.
- Prompt system rules vs. retrieved context vs. examples.
- Parsing/validation vs. side effect.
- Shared utility vs. project-specific rule.

## Forbidden Patterns

- One file that owns UI, state, validation, persistence, API calls, and formatting.
- "Temporary" duplication without a `#tech-debt` record.
- Adding unrelated helpers to a generic catch-all file.
- Creating a new abstraction before two real call sites prove it.
- Moving many files only to make a tree look cleaner.
- Refactoring and feature behavior changes in the same batch without explicit plan scope.

## Output Required

Record this compact block in the active plan before editing:

```markdown
## Anti-Monolith Gate

- Skill loaded: `skills/anti-monolith-guard/SKILL.md`
- Target artifact:
- Primary responsibility:
- Explicit non-responsibilities:
- Size budget:
- Similar code checked:
- Split decision: `proceed` / `split first` / `temporary exception`
- Validation:
```

## Exit Criteria

Proceed only when the plan proves the next edit is small, named, bounded, reusable where needed, and validated.
