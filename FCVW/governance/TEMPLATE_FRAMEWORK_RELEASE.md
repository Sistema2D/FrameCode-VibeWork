# Template: framework release

```markdown
---
schema: "fcvw/framework-release@1"
version: "Vx.y.z"
artifact_role: "record"
owner: "framework"
upgrade_strategy: "preserve"
record_scope: "framework"
date: "YYYY-MM-DD"
release_status: "in_preparation | ready | published | canceled"
release_type: "patch | minor | major"
compatibility: "backward_compatible | migration_required | breaking"
source_revision: "<40-character-content-baseline-revision-or-UNCOMMITTED_LOCAL_WORKTREE>"
publication_revision: "<40-character-tagged-revision-or-UNPUBLISHED>"
release_languages:
  - "pt-BR"
  - "en-US"
  - "es"
  - "de"
related_plans:
  - "P3-R2-YYYY-MM-DD-short-description"
---

# FCVW Vx.y.z

## Summary
## Related framework plans

- [Framework plan](<relative-path-to-plan.md>)

## Framework surfaces added
## Framework surfaces changed
## Framework surfaces removed
## Ownership and path changes
## Schema changes
## Migration
## Validation
## Downstream preservation rules
## Known gaps
## Rollback
## Language-variant parity and review evidence
## Clean assets and package contents
## Checksums
## Publication evidence
```
