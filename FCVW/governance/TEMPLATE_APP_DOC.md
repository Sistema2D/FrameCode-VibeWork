# Template: application documentation

Sections for application-owned documentation under the rules of [APPLICATION_DOCUMENTATION.md](../APPLICATION_DOCUMENTATION.md): the docs folder README, a module, a flow, an API, a data schema and an AI feature. Copy only the section that matches the document being written.

## Application Documentation

This folder contains documentation for the application modules, screens, pages, components, and flows.

It is application-owned. The FCVW framework defines the rules in `FCVW/APPLICATION_DOCUMENTATION.md`, but filled documents in this folder describe this specific application.

### Structure

```text
docs/
|-- README.md
|-- modules/
|   |-- TEMPLATE_MODULE.md
|   \-- <module-name>.md
\-- flows/
    |-- TEMPLATE_FLOW.md
    \-- <flow-name>.md
```

### Required Practice

- Create one module document for each relevant page, screen, module, or major component.
- Create flow documents for cross-module workflows.
- Use Mermaid diagrams when they clarify behavior, dependencies, or state transitions.
- Keep documentation changes in the same FCVW plan and changelog as the implementation change.

### Module Index

| Module | Document | Owner | Last Updated |
|---|---|---|---|
| | | | |

### Flow Index

| Flow | Document | Owner | Last Updated |
|---|---|---|---|
| | | | |

## Module: <module name>

### Objective

<Describe the module purpose and user value.>

### Related Files

| Path | Role |
|---|---|
| | |

### Related Pages / Components / Services

-

### Inputs

| Input | Source | Validation |
|---|---|---|
| | | |

### Outputs

| Output | Destination | Notes |
|---|---|---|
| | | |

### Business Rules

-

### Internal Dependencies

-

### External Dependencies

-

### User Events and Actions

| Event / Action | Expected Result |
|---|---|
| | |

### States

| State | Description | Trigger |
|---|---|---|
| Initial | | |
| Loading | | |
| Empty | | |
| Error | | |
| Success | | |

### Validation Criteria

-

### Known Risks

-

### Operating Flow

```mermaid
flowchart TD
    A["User enters module"] --> B["Module loads required state"]
    B --> C{"Required data available?"}
    C -- "Yes" --> D["Render primary state"]
    C -- "No" --> E["Render empty or error state"]
```

### Change History

| Date | Version / Plan | Change |
|---|---|---|
| | | |

## Flow: <flow name>

### Objective

<Describe what this flow accomplishes and why it matters.>

### Entry Points

-

### Actors

-

### Related Modules

| Module | Documentation |
|---|---|
| | |

### Related Files

| Path | Role |
|---|---|
| | |

### Main Flow

```mermaid
flowchart TD
    A["Start"] --> B["Step 1"]
    B --> C{"Decision"}
    C -- "Path A" --> D["Outcome A"]
    C -- "Path B" --> E["Outcome B"]
```

### Alternative Flows

| Condition | Flow | Expected Outcome |
|---|---|---|
| | | |

### Error and Recovery Paths

| Error / Failure | Recovery | User Feedback |
|---|---|---|
| | | |

### Data and State Transitions

| State Before | Event | State After |
|---|---|---|
| | | |

### Validation Criteria

-

### Known Risks

-

### Change History

| Date | Version / Plan | Change |
|---|---|---|
| | | |

## API Endpoint Contract Specification

Use this template to document the physical contract of any new or modified API route in the application before writing implementation logic.

---

### 1. Route Summary

*   **Path:** `/api/v1/resource`
*   **Method:** `GET` / `POST` / `PUT` / `DELETE`
*   **Authentication Required:** Yes / No (Role: `user` / `admin`)
*   **Version:** `v1`

---

### 2. Request Contract

#### 2.1 URL Parameters (if any)
| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | UUID / Integer | Yes | Unique identifier of the target resource |

#### 2.2 Query Parameters (if any)
| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `page` | Integer | No | `1` | Pagination offset index |
| `limit` | Integer | No | `20` | Max entries to return |

#### 2.3 Body Payload (JSON format)
```json
{
  "name": "Required string field",
  "category": "Optional string matching allowed enum values",
  "tags": ["Array of string labels"]
}
```

---

### 3. Response Contract

#### 3.1 Success Response (`200 OK` or `201 Created`)
```json
{
  "success": true,
  "data": {
    "id": "uuid-string",
    "name": "Resource Name",
    "category": "default",
    "tags": [],
    "created_at": "YYYY-MM-DDTHH:MM:SSZ"
  }
}
```

#### 3.2 Error Responses
*   `400 Bad Request` — Validation failed:
    ```json
    {
      "success": false,
      "error": "validation_error",
      "message": "Field 'name' is required."
    }
    ```
*   `401 Unauthorized` — Expired or invalid token.
*   `404 Not Found` — Resource ID does not exist.

## Template: Data Schema Record

Copy this content when defining a new persistence format (JSON, database, CSV, etc.).

```markdown
# Schema: <Data Name>

## Schema Version

`1`

## File or Table

- Path/Table: `<path>`

## Purpose

- <Describe what this data is used for.>

## Fields

| Field | Type | Required | Default Value | Description |
|---|---|---|---|---|
| | | | | |

## SQL DDL Blueprint

*Use this standard SQLite DDL code to generate or reset the physical table:*

```sql
CREATE TABLE IF NOT EXISTS <table_name> (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- Define columns here...
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

## Migration Script Mapping

- **Init Migration:** `data/migrations/V1__init_<table_name>.sql`
- **Upgrades Mapping:**
  | Target Version | Migration Script | Rollback Script | Description |
  |---|---|---|---|
  | `2` | `data/migrations/V2__upgrade.sql` | `data/migrations/V2__rollback.sql` | |

## Validation Rules

- <e.g., non-null fields, date format, etc.>

## Sensitive Data

- <List if there are tokens, names, emails, or private data.>

## Observations

- <Additional notes on integrity or performance.>
```

## Template: AI Feature Specification

Copy this content to a new file or inside a plan when defining a new AI feature.

```markdown
# AI Feature: <Name>

## Objective

- <Describe the practical goal of the feature.>

## Usage Type

`simple chat` / `chat with context` / `RAG` / `continuous learning` / `agent with tools`

## Inputs

- <Describe what the user sends or what is captured from the system.>

## Outputs

- <Describe the expected format of the response (text, JSON, action).>

## Model/Runtime

- <Provider/runtime and exact model identifier, or selection policy.>

## Context Used

- <Which files, history, or databases are sent to the model.>

## Sources Displayed

- <How the user will know the origin of the information.>

## Action Boundaries

- <What the feature CANNOT do (e.g., delete without confirmation).>

## Risks

- <Hallucination, cost, latency, context leakage.>

## Minimum Tests

- <Mandatory test cases for this feature.>
```
