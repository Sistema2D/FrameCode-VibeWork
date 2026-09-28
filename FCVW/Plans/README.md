# Plans

Formal change plans, one file per plan, in a directory that matches its `status`: `pending/`, `in_progress/`, `completed/` or `discontinued/`. A state directory is created by the first plan that needs it. The method is in [PLANNING.md](../PLANNING.md).

## Queue

There is no queue file. Each active plan declares `category` (`correction`, `optimization`, `code_hygiene`, `visual` or `other`; default `other`), and optionally `blocked_external: <specific reason>` or, for a pending plan, `before_in_progress: <specific reason>`. Blockers also come from unresolved `depends_on`. The order is derived:

```sh
python FCVW/tools/plan_queue_fcvw.py --root . --recommend
```

Use `tools/` instead of `FCVW/tools/` in the framework source checkout. `--output .fcvw-cache/plan-queue.md` writes a disposable view.
