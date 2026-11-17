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

Generate it instead of copying this form: `validate_fcvw.py --root . --write-baseline --baseline-owner <owner>` writes `FCVW/audits/legacy-baseline.md`, which `--profile auto` then applies. A baseline makes only an exact pre-existing finding non-blocking. Exact means the normalized path, rule ID, and finding message match, ignoring `line N:` prefixes and successor hints. It never hides a new path, changed violation, expired review, or malformed entry. Rerun `--write-baseline` to drop fixed rows; reviewed justifications are kept.
