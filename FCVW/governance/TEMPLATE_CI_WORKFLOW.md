# Template: continuous integration workflow

Reference workflow for Scenario 3 of [`AUTOMATION.md`](../AUTOMATION.md).

FCVW does **not** install this. `AUTOMATION.md` is explicit: Scenario 1 never
installs hooks or schedules work by implication, and external automation
requires project approval and documentation. Copy the block below into
`.github/workflows/fcvw.yml` only after recording the decision in a plan.

The workflow file is project-owned and lives outside `FCVW/`, so it is not part
of the framework removal boundary.

```yaml
name: FCVW governance

on:
  pull_request:
  push:
    branches: [main]

jobs:
  governance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      # Derived surfaces first: the validator compares the generated catalog
      # against the current filesystem, and a stale catalog is a failure.
      - name: Regenerate derived surfaces
        run: |
          python FCVW/tools/plan_queue_fcvw.py --root . --write-queues
          python FCVW/tools/document_graph_fcvw.py --root . --write
          python FCVW/tools/role_manifest_fcvw.py --root . --write

      - name: Fail when a derived surface was committed stale
        run: git diff --exit-code

      - name: Structural suites
        run: |
          python -B FCVW/tools/test_validate_fcvw.py
          python -B FCVW/tools/test_open_issues.py
          python -B FCVW/tools/test_plan_dependencies_and_knowledge.py

      - name: Validate governance
        run: >
          python FCVW/tools/validate_fcvw.py --root .
          --profile instantiated --format json --fail-on error
          | tee fcvw-validation.json

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: fcvw-validation
          path: fcvw-validation.json
```

## Scoped pull-request runs

In a large repository a full report is noisy on a small pull request. `--since`
keeps the repository-wide rules and restricts per-file findings to what changed:

```yaml
      - name: Validate changed governance only
        run: >
          python FCVW/tools/validate_fcvw.py --root .
          --profile instantiated --since origin/${{ github.base_ref }}
          --format json --fail-on error
```

`--since` affects signal, not runtime: repository-wide checks still run, so a
scoped run still fails when the tree as a whole is inconsistent.

## Adoption record

Record in the plan that authorizes this workflow:

- automation scenario: `3`;
- `authorized_by` and permission boundary;
- failure policy and disable procedure;
- evidence destination (`fcvw-validation.json`);
- rollback: remove the workflow file.

See [`GOVERNANCE_GATES.md`](../GOVERNANCE_GATES.md) for `pass`, `warn`, and
`block` handling.
