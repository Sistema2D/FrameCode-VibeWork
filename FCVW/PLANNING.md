# Change Planning

## Objective

Define the mandatory methodology for planning changes before any modification to code, documentation, configuration, build, tests, or versioned data.

Individual plans reside in `Plans/{status}`. This file is a methodology, not a task list.

## Mandatory Rule

No change should be applied without a corresponding plan in `Plans/`.

Mandatory sequence before any change:

1. Identify the required change.
2. Create a plan file in `Plans/pending/`.
3. Classify priority (`P1`–`P5`) and risk (`R1`–`R5`).
4. Record current version and expected version.
5. Describe implementation plan, acceptance criteria, and test plan.
6. List exact files needed for execution in the `context_files` frontmatter array (Token Optimization).
7. Move to `Plans/in_progress/` upon starting.
8. Apply only the scope of the plan.
9. Create a changelog fragment in `changelogs/unreleased/{plan-name}.md`.
10. Validate acceptance criteria (execute tests via terminal and paste the stdout inside the plan as physical evidence).
11. Update the plan with results and move to `Plans/completed/` or `Plans/discontinued/`.

---

## Models and Templates

To create new change plans, use the template in:
`governance/TEMPLATE_PLAN.md`

When applicable, also include: security analysis (`SECURITY.md`), data and migration (`DATA.md`), AI impact (`AI.md`), architectural decisions (`ARCHITECTURAL_DECISIONS.md`), and expected updates to the `wiki/`.

## Naming Pattern

```text
P{priority}-R{risk}-{date}-{short-description}.md
```

Examples:

```text
P1-R4-2026-05-13-data-persistence-correction.md
P3-R2-2026-05-13-dashboard-interface-adjustment.md
```

## Priority Scale

| Priority | Name | Use when |
|---|---|---|
| P1 | Critical | security, data integrity, failures that prevent usage |
| P2 | High | main workflow, stability, relevant features |
| P3 | Medium | functional improvements, organization, usability |
| P4 | Low | visual adjustments, texts, small refactoring |
| P5 | Optional | future ideas, experimental improvements |

## Risk Scale

| Risk | Name | Use when |
|---|---|---|
| R1 | Very low | only texts, styles, no logic or data |
| R2 | Low | isolated component, simple logic, localized tests |
| R3 | Moderate | shared logic, major workflows, possible regression |
| R4 | High | persistence, global states, integrations, relevant refactoring |
| R5 | Critical | security, architecture, authentication, migration, risk of data loss |

## Folders Organization

```text
Plans/
├── pending/
├── in_progress/
├── completed/
└── discontinued/
```

Each file must be in the folder corresponding to the plan's **Status** field. When changing the status, move the file to the correct subfolder.

## Relationship with Document Governance

Changes in the root official documents and in templates of `governance/` follow the same methodology.

When a change modifies the structure of an official document, evaluate if the corresponding empty template in `governance/` needs to be updated with the same structure, without project-specific data.

The `wiki/` can be updated when the change generates reusable learning. This update does not replace plans, changelogs, troubleshooting, or official documents.
