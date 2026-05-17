# Template: Data Schema Record

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

## Validation Rules

- <e.g., non-null fields, date format, etc.>

## Migrations

| Origin | Target | Description | Rollback |
|---|---|---|---|
| | | | |

## Sensitive Data

- <List if there are tokens, names, emails, or private data.>

## Observations

- <Additional notes on integrity or performance.>
```
