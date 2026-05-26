# Architectural Decisions

Methodological document to register relevant technical decisions of the project using ADRs, Architecture Decision Records.

This file should be consulted before making changes that alter the architecture, stack, persistence, API contracts, module organization, runtime, security, distribution, AI integration, or the core flow of the application.

## Objective

Prevent important decisions from remaining implicit in conversations, commits, prompts, or code.

Each relevant architectural decision must be recorded so that humans and AI agents understand:

- the context of the decision;
- the alternatives considered;
- the decision made;
- the consequences;
- the risks;
- the relationship with plans, versions, and changelogs.

## Records Location

Decisions must be stored in:

```text
decisions/
```

Naming pattern:

```text
ADR-0001-short-description.md
ADR-0002-short-description.md
```

## When to Create an ADR

Create an ADR when the change involves:

- changing the tech stack;
- creating a new core module;
- modifying the frontend/backend architecture;
- changing the database or persistence format;
- altering API contracts;
- adopting a new AI runtime;
- changing RAG or memory strategies;
- making a relevant security change;
- changing build, packaging, or distribution processes;
- deciding to abandon an important technical alternative;
- rewriting a module;
- separating or merging services.

## When Not to Create an ADR

It is not necessary to create an ADR for:

- simple visual adjustments;
- text corrections;
- local bugs without architectural impact;
- small refactoring without change of responsibility;
- common documentation updates;
- local component improvements without impact on other modules.

## Allowed Statuses

- `proposed`: decision still under analysis;
- `accepted`: decision approved and in effect;
- `superseded`: decision replaced by a subsequent ADR;
- `rejected`: decision analyzed and not adopted;
- `deprecated`: decision no longer applies to the current state of the project.

## Relationship with Plans and Changelogs

- An ADR does not replace a plan in `Plans/`.
- A change that implements an ADR must have its own plan.
- A release that implements an ADR must cite the decision in the changelog.
- A superseded ADR must point to the new ADR.
- Pages in `wiki/decisions/` are syntheses of learning and do not replace the formal ADR.

---

## Models and Templates

To create new Architectural Decisions (ADRs), use the template in:
`governance/TEMPLATE_ADR.md`

## Checklist Before Accepting an ADR

- [ ] The problem was clearly described.
- [ ] Alternatives were considered.
- [ ] The decision does not contradict the approved scope.
- [ ] Impacts on security were evaluated.
- [ ] Impacts on data were evaluated.
- [ ] Impacts on tests were evaluated.
- [ ] Negative consequences were recorded.
- [ ] A plan exists to implement the decision, if necessary.
