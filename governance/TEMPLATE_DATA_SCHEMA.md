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
