---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Maintenance-loop contracts

A daemon contract describes recurring maintenance but does not authorize a background service.

Define:

- objective and owner;
- cadence or trigger;
- bounded input set;
- one iteration's actions;
- maximum duration/work items;
- checkpoint and evidence;
- stop, pause, and failure conditions;
- concurrency lock;
- resource and permission limits;
- rollback/cleanup.

Scenario 1 executes at most one explicitly requested iteration. Persistent scheduling belongs to Scenario 3 and requires separate authorization.

Use `governance/TEMPLATE_DAEMON_LOOP.md`.
