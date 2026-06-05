# Change Planning

## Objective

Define the mandatory methodology for planning changes before any modification to code, documentation, configuration, build, tests, or versioned data.

Individual plans reside in `Plans/{status}`. This file is a methodology, not a task list.

## Mandatory Rule

No change should be applied without a corresponding plan in `Plans/`.

Mandatory sequence before any change:

1. Identify the required change.
2. Create a plan file in `Plans/pending/`.
3. Classify priority (`P1`-`P5`) and risk (`R1`-`R5`).
4. Record operational score, review gate, rollback requirement, and decomposition requirement.
5. Record current version and expected version.
6. Describe implementation plan, acceptance criteria, and test plan.
7. List exact files needed for execution in the `context_files` frontmatter array (Token Optimization).
8. Move to `Plans/in_progress/` upon starting.
9. Apply only the scope of the plan.
10. Create a changelog fragment in `changelogs/unreleased/{plan-name}.md`.
11. Validate acceptance criteria (execute tests via terminal and paste the stdout inside the plan as physical evidence).
12. Update the plan with results and move to `Plans/completed/` or `Plans/discontinued/`.

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

## Operational Use of Priority and Risk

Priority and risk are operational controls, not only labels.

- Priority (`P1` to `P5`) represents impact, urgency, and execution value.
- Risk (`R1` to `R5`) represents regression probability, complexity, technical impact, and required control.
- Priority is the primary triage criterion.
- Risk defines containment, validation, rollback, review, and decomposition gates.

### Operational Score

Plans must record an operational score in this format:

```text
P{n}-R{n} => impact_weight {6 - P} x risk_weight {R} = {score}
```

Example:

```text
P2-R3 => impact_weight 4 x risk_weight 3 = 12
```

The score helps triage and compare pending plans, but it must not be used as the only ordering rule. A high-risk, low-priority plan must not jump ahead only because its score is high.

### Decision Rules

| Classification | Required handling |
|---|---|
| `P1-R1` / `P1-R2` | Execute with high priority and proportional validation. |
| `P1-R4` / `P1-R5` | Triage immediately; require rollback, expanded validation, and possible human review before execution. |
| `P2-R3` | Execute after active `P1` work or with explicit justification; run compatible regression validation. |
| `P3-R5` | Do not execute automatically; evaluate decomposition, preparatory plan, or human review. |
| `P4-R1` / `P5-R1` | Low priority; execute only when no more relevant plan is pending or when bundled with approved maintenance. |
| `P5-R4` / `P5-R5` | Usually postpone, discontinue, or reclassify unless there is explicit justification. |

### Mandatory Gates

- Plans `R4` and `R5` must include rollback observations before execution.
- Plans `R4` and `R5` must include expanded validation evidence before completion.
- Plans `R5` require explicit human approval before being considered completed.
- Plans with high risk and low priority (`P4/P5-R4/R5`) must document why they are not postponed, decomposed, or discontinued.
- If risk comes from broad scope, split the work into smaller plans unless a single plan has a clearer validation path.

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
