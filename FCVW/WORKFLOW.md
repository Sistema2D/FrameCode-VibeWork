# WORKFLOW.md

Detailed operational document of the application.

> This is a template. Adapt the sections according to the actual architecture of the project. Remove or replace modules that do not exist.

This file describes the functional behavior of each module/screen/service of the application with focus on:

- concept and objective of each area;
- controls and components (buttons, fields, lists, modals, toggles, sliders);
- user events and effects on application state;
- integration between layers (frontend, backend, external services);
- local persistence and processing workflows;
- Mermaid flowcharts of the main paths.

## 1. Overview of Runtime Architecture

### 1.1 `<Layer 1 — e.g., Frontend>`

`<Describe the main process, responsibilities, and memory state.>`

### 1.2 `<Layer 2 — e.g., Backend>`

`<Describe the local/remote service, endpoints, and integrations.>`

### 1.3 Local Persistence

`<Describe configuration files, user data, and vault.>`

## 2. Application Lifecycle

### 2.1 Initialization

`<Describe boot steps: configuration loading, control creation, connection to services.>`

```mermaid
flowchart TD
    A["Start"] --> B["Load settings"]
    B --> C["Initialize services"]
    C --> D["Application ready"]
```

### 2.2 Shutdown

`<Describe shutdown steps: save state, close connections, release resources.>`

## 3. Global Navigation

`<Describe how the user navigates between screens or modules.>`

```mermaid
flowchart LR
    A["Module 1"] --> B["Module 2"]
    A --> C["Module 3"]
```

## 4. Module `<Module Name 1>`

### 4.1 Concept and Objective

`<Describe the purpose of the module.>`

### 4.2 Components

`<List relevant controls, fields, and visual elements.>`

### 4.3 Main Workflow

`<Describe the step-by-step workflow.>`

```mermaid
flowchart TD
    A["User action"] --> B["Validation"]
    B -- "Valid" --> C["Process"]
    B -- "Invalid" --> D["Error feedback"]
    C --> E["Result"]
```

## 5. Module `<Module Name 2>`

### 5.1 Concept and Objective

`<Describe the purpose of the module.>`

### 5.2 Components

`<List relevant controls, fields, and visual elements.>`

### 5.3 Main Workflow

`<Describe the step-by-step workflow.>`

## 6. Backend / Local Service

`<Remove if there is no separate backend.>`

### 6.1 Security and Middleware

`<Describe token, CORS, and authentication.>`

### 6.2 Main Endpoints

`<List endpoints with method, route, and purpose.>`

| Method | Route | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| `<method>` | `<route>` | `<description>` |

## 7. Integrated Workflow

`<Describe the workflow that connects all layers for the main use case.>`

```mermaid
flowchart TD
    A["User action"] --> B["Frontend"]
    B --> C["Backend"]
    C --> D["External service / AI / data"]
    D --> E["Response to user"]
```

## 8. Shortcuts and Cross-Cutting Behaviors

`<List keyboard shortcuts, gestures, or behaviors that apply to multiple modules.>`

## 9. Document Governance Workflow

The FrameCode VibeWork framework has its own operational workflow, separate from the application's runtime.

1. `AGENTS.md` guides the initial consultation and points to the applicable official documents.
2. `PLANNING.md` defines the methodology, and each change is recorded in `Plans/{status}`.
3. Priority and risk are evaluated before execution; priority drives triage and risk defines review, rollback, validation, blocking, and decomposition.
4. The implementation or document change updates the affected official documents.
5. Relevant downstream application module changes update the application-owned documentation defined in `APPLICATION_DOCUMENTATION.md`.
6. `VERSIONING.md` guides the expected version and the corresponding changelog in `changelogs/`.

```mermaid
flowchart TD
    A["AGENTS.md"] --> B["Applicable official documents"]
    B --> C["Plan in Plans/{status}"]
    C --> D["Priority/risk gates"]
    D --> E["Documented change"]
    E --> F["Changelog in changelogs/"]
```

## 10. Declarative Automation Workflow

Scenario 1 declarative automation is part of document governance, not application runtime.

1. Identify the event, operation, or recurring maintenance need.
2. Consult `AUTOMATION.md` to confirm Scenario 1 boundaries.
3. Apply the relevant contract:
   - `HOOKS.md` for pseudo-hook checklists;
   - `WATCHERS.md` for event/reaction rules;
   - `DAEMONS.md` for manual/agentic maintenance loops;
   - `GOVERNANCE_GATES.md` for gate trigger mapping.
4. Record findings and blocking conditions in the active plan.
5. Update changelog when any versioned file changes.
6. Stop if the action requires executable scripts, installed hooks, coded watchers, background daemons, CI/CD workflows, package manifests, API keys, provider SDKs, or command-execution loops.

```mermaid
flowchart TD
    A["Automation-related request"] --> B["AUTOMATION.md boundary check"]
    B --> C["Select contract: hooks / watchers / daemons / gates"]
    C --> D["Evaluate Markdown checklist"]
    D --> E{"Blocking condition?"}
    E -- "Yes" --> F["Stop and record in active plan"]
    E -- "No" --> G["Proceed within plan scope"]
    G --> H["Record evidence and changelog"]
```

## 11. Maintenance Observations

`<Record here known maintenance risks, critical dependencies, and areas requiring special attention when making changes.>`

- When evolving the behavior described here, keep this document synchronized within the same change plan/changelog.
- When changing pages, screens, components, flows, or business rules in a downstream application, keep the application-owned module documentation synchronized in the same plan.
- When evolving declarative automation contracts, preserve ADR-0001 and ADR-0002 boundaries: no executable automation in Scenario 1.
