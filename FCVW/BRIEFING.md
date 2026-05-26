# Initial Project Briefing

Methodological document to conduct **Phase 0 — Discovery and Briefing** before the development or restructuring of an application.

This file defines the questions, minimum criteria, and completion rules to be used by humans and AI agents to collect the necessary information before generating or updating `SCOPE.md`, `STACK.md`, `DESIGN.md`, `WORKFLOW.md`, `PLANNING.md`, `VERSIONING.md`, `SECURITY.md`, `DATA.md`, `AI.md`, and other official project documents.

## Objective

Ensure that the start of development is guided, traceable, and free of critical gaps.

Phase 0 must produce a completed file in:

```text
briefings/INITIAL_BRIEFING.md
```

This file will serve as the initial source of project understanding. After the official documents are created, it ceases to be the main normative source but remains as a historical record of the project's conception.

## Relationship with Other Documents

- `AGENTS.md`: triggers this process when the user requests the creation or restructuring of an application.
- `SCOPE.md`: filled out based on the answers about objective, audience, boundaries, and features.
- `STACK.md`: filled out based on technical decisions.
- `DESIGN.md`: filled out based on visual preferences and UX criteria.
- `WORKFLOW.md`: filled out based on flows, screens, modules, and events.
- `SECURITY.md`: filled out based on risks, permissions, sensitive data, and integrations.
- `DATA.md`: filled out based on persistence, files, database, retention, and migration.
- `AI.md`: filled out based on the role of AI, models, context, memory, RAG, and boundaries of action.
- `PLANNING.md`: guides subsequent plans.
- `VERSIONING.md`: guides the initial version and future releases.

## Mandatory Activation Rule

When the user requests the start of a new application, a reconstruction from scratch, a broad migration, or the adaptation of this framework to another project, the AI agent must:

1. Check if `briefings/INITIAL_BRIEFING.md` already exists.
2. If it does not exist, start the guided interview.
3. Record the answers in the briefing file.
4. Consult `INSTANTIATION.md` and manually apply the renaming, placeholder, and canonical vs. template document separation rules.
5. Mark unknown fields as `To be defined`.
6. List critical gaps before generating official documents.
7. Do not start code implementation while there are critical gaps without an explicit decision from the user.

## Gap Levels

### Critical Gap

Prevents the safe start of development.

Examples:

- undefined application objective;
- undefined target audience;
- undefined target platform;
- undefined use of AI;
- unknown handled data;
- unevaluated security requirements;
- undefined mandatory stack or technical constraints;
- unprioritized mandatory features.

### Relevant Gap

Does not prevent prototyping but must be resolved before stable development.

Examples:

- visual identity not yet approved;
- final name undefined;
- future integrations not yet detailed;
- pending backup policy;
- generic acceptance criteria.

### Tolerable Gap

Can remain open during initial versions.

Examples:

- slogan;
- final icon;
- public documentation;
- optional resources;
- future internationalization.

## Mandatory Questionnaire

### 1. Project Identification

- Temporary name:
- Final name, if any:
- Type of application:
- Target platform:
- Target operating system:
- Target audience:
- Problem the application solves:
- Main objective:
- Product success criterion:

### 2. Context of Use

- Who will use the application?
- In what environment will the application be used?
- Will the application be used for personal, internal, corporate, or public purposes?
- Does the application need to work offline?
- Does the application need to work on a local network?
- Will the application have multiple users?
- Are there any hardware or performance constraints?

### 3. Functional Scope

- Mandatory features:
- Desirable features:
- Explicitly out of scope features:
- Main user flow:
- Planned screens or modules:
- Critical user actions:
- Destructive actions requiring confirmation:
- Necessary integrations:
- Required reports, exports, or imports:

### 4. Use of AI

- Will the application use local, online, or hybrid AI?
- What runtime, provider, or model is planned?
- Will AI be used for chat, automation, analysis, RAG, content generation, classification, agents, or another use?
- Will AI be able to execute actions or only respond?
- Will there be memory, history, or a knowledge base?
- Will there be embeddings or vector search?
- Will there be continuous learning?
- What information should the AI not access?
- What actions should the AI never execute automatically?

### 5. Data and Persistence

- What data will be stored?
- Where will they be stored?
- Will there be a database?
- Will there be local files?
- Will there be sensitive data?
- Will there be logs?
- Will there be backups?
- Will there be export or import features?
- Will there be migration between versions?
- What data should be ignored by Git?

### 6. Security and Privacy

- Will the application require authentication?
- Will there be roles or permissions?
- Will there be tokens, keys, or secrets?
- Will there be local command execution?
- Will there be filesystem access?
- Will there be communication with external APIs?
- What initial threats are predictable?
- How will private or sensitive data be handled?

### 7. Design and Experience

- Desired visual style:
- Light, dark theme, or both:
- Interface density:
- Visual references:
- Desired palette:
- Desired typography:
- Main components:
- Accessibility requirements:
- Layout constraints:
- Behavior on small screens or resized windows:

### 8. Technical Stack

- Main language:
- Frontend framework:
- Backend framework:
- Database:
- AI runtime:
- Build tools:
- External dependencies:
- Packaging standard:
- Mandatory constraints:
- Prohibited technologies:

### 9. Quality, Testing, and Validation

- How will the project be tested?
- Which flows require mandatory manual testing?
- Will there be automated tests?
- Will there be a release checklist?
- What criteria define that a version is ready?
- What regressions would be unacceptable?

### 10. Versioning and Governance

- Initial version:
- Versioning strategy:
- Changelog standard:
- Plans standard:
- Criteria for minor version:
- Criteria for patch version:
- Criteria for major version:
- Responsible for approving scope changes:
- Responsible for approving visual changes:

---

## Models and Templates

To perform the initial survey of a new project, use the template in:
`governance/TEMPLATE_BRIEFING.md`

## Phase 0 Closure Rule

Phase 0 can only be marked as completed when:

- the initial briefing exists;
- critical gaps are resolved or formally accepted by the user;
- the agent has indicated which official documents will be created or updated;
- the user has approved the minimum starting scope;
- any assumed premise is recorded.
