# Template: legacy validation baseline

```markdown
---
schema: "fcvw/legacy-baseline@1"
created_at: "YYYY-MM-DD"
review_due: "YYYY-MM-DD"
owner: "<owner>"
---

# Legacy validation baseline

| Exact path | Rule ID | Existing finding | Justification | Owner | Review due |
|---|---|---|---|---|---|
| | | | | | |
```

A baseline makes only an exact pre-existing finding non-blocking under `--profile incremental --baseline <file>`. Exact means the normalized path, rule ID, and complete finding message all match. It never hides a new path, changed violation, expired review, or malformed entry. Remove rows reported as stale.
