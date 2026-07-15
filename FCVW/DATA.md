---
schema: "fcvw/project-data@1"
artifact_role: "project_profile"
owner: "project"
upgrade_strategy: "preserve"
instantiation_status: "pending"
---

# Data, persistence, and migration

## Data inventory

| Data class | Source of truth | Sensitivity | Retention | Backup | Owner |
|---|---|---|---|---|---|
| | | | | | |

Generated documents, exports, caches, and reports must remain downstream of structured source data.

## Persistence contract

- Primary store: `<store>`
- Schema source: `<path>`
- Migration mechanism: `<mechanism>`
- Transaction/atomicity boundary:
- Concurrency model:
- Integrity constraints:

## Import and export

- Validate format and schema version before mutation.
- Use explicit conflict and duplicate policies.
- Never silently coerce unknown values.
- Preserve provenance and produce a reconciliation result.
- Treat imports, backups, and exports as untrusted input.

## Migration gate

R4/R5 data changes require:

1. inventory and dependency map;
2. forward migration;
3. rollback or restore plan;
4. disposable-environment rehearsal;
5. record-count and semantic reconciliation;
6. backup/restore evidence;
7. explicit approval for irreversible loss.

## Recovery objectives

- Recovery point objective:
- Recovery time objective:
- Backup schedule:
- Restore drill cadence:
- Last verified restore:

## Privacy and deletion

Document lawful purpose, access, retention, export, deletion, and log-redaction rules for each sensitive class. Do not place secrets or personal production data in FCVW records.
