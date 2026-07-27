---
schema: "fcvw/skill@1"
name: "anti-monolith-guard"
description: "Prevent mixed-responsibility modules and uncontrolled file growth."
version: "1.2.0"
trigger_keywords:
  - "monolith"
  - "large file"
  - "module boundary"
  - "anti-monólito"
session_types:
  - "planning"
  - "refactoring"
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

## Inputs

Active plan, target artifact, responsibility map, similar-code search, dependency/consumer evidence, current size or complexity indicators, and the checks that protect behavior during a split.

## Applicability Classification

Classify the target before applying numeric thresholds:

| Artifact class | Automatic size enforcement | Review focus |
|---|---|---|
| Source code, query, executable configuration, or runtime prompt | Yes, using the closest project-adjusted budget | responsibility, coupling, side effects, test boundary |
| Operational AI instruction or procedural skill | Warning by default; block only when mixed responsibilities or unsafe context loading are demonstrated | instruction hierarchy, retrieval cost, cohesion, provider neutrality |
| Canonical documentation, specification, report, plan, decision, or release record | No numeric block | cohesion, discoverability, ownership, document-graph relationships |
| Template, example, generated catalog, or historical record | No numeric block | schema correctness, generation source, reachability, preservation |

Markdown is not automatically documentary: classify it by responsibility. A Markdown prompt that controls runtime behavior may be operational, while a long technical specification may remain one cohesive document.

If the target is not source code or an operational instruction, record `not numerically applicable` and use document-graph and schema validation instead. Do not split prose merely to satisfy a line count.

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

These are code-oriented governance defaults, not universal rules. Apply them only after the applicability classification. A project may resize them in `STACK.md` or `APPLICATION_DOCUMENTATION.md` when architecture, security, integrity, or performance evidence requires a different budget.

| Artifact | Warning | Block unless justified |
|---|---:|---:|
| Function / method | 40 lines | 80 lines |
| UI component / screen section | 180 lines | 300 lines |
| Route / controller / handler | 120 lines | 220 lines |
| Service / use case | 180 lines | 300 lines |
| Prompt or agent instruction file | 180 lines | 300 lines |
| General module file | 250 lines | 400 lines |

If a file crosses the warning threshold, record the reason in the plan. If it crosses the block threshold, split first or document why a temporary exception is safer.

## Exceptions and Threshold Reassessment

An exception may pass only when the plan records:

- the concrete regression, security, architecture, integrity, performance, or cognitive-load harm that a split could cause;
- why a smaller boundary, extraction, or existing module is insufficient;
- the project-adjusted warning and block thresholds;
- validation that protects the critical attribute; and
- an owner and revisit condition.

Line count alone never proves a monolith, and splitting into many low-value files can itself fail this gate. Exceptions cannot waive mandatory security, privacy, accessibility, data-integrity, audit, or regression controls.

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
- Artifact class: `source` / `operational instruction` / `documentation` / `record/template/generated`
- Numeric threshold applicability: `applicable` / `warning only` / `not applicable`
- Explicit non-responsibilities:
- Size budget:
- Similar code checked:
- Split decision: `proceed` / `split first` / `temporary exception`
- Validation:
```

## Exit Criteria

Proceed only when the plan proves the next edit is small, named, bounded, reusable where needed, and validated.
