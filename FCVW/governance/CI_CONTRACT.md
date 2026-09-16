---
schema: "fcvw/automation@1"
id: "AUT-2026-09-16-framework-ci"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
owner: "framework-maintainer"
kind: "governance_gate"
status: "active"
scenario: "3"
execution_mode: "scenario_3"
authorized_by: "Explicit user request for implementation and release on 2026-09-16"
trigger: "push main, pull_request, workflow_dispatch, release published"
preconditions: "GitHub Actions enabled; source checkout; Python available"
permissions: "contents read; no repository secrets; ephemeral runner writes"
actions: "Run regressions, governance, labeled benchmark and installed-payload verification"
evidence: "GitHub run logs and benchmark artifacts retained for 14 days"
failure_policy: "Fail the job and block maintainer release approval; no automatic repair"
rollback: "Disable or revert the source-only workflow; preserve project records"
---

# Framework CI contract

## Scope and execution

This repository-only gate implements [AUTOMATION.md](../AUTOMATION.md) and [TESTS.md](../TESTS.md). The user authorized implementation and publication. Four isolated jobs test Linux/Windows and Python 3.12/3.14. Actions are pinned to full commit IDs; checkout credentials are not persisted. No credentials or secrets are required beyond the read-only GitHub token for release downloads.

## Evidence and failure

Each job runs source regressions, governance, the synthetic labeled benchmark and installed-layout checks. A published-release event additionally downloads the assets and validates their checksums and source-bound installed tools before executing tests. Logs identify revision, runtime, inputs and failures. Benchmark artifacts expire after 14 days. A failed check exits nonzero; maintainers must resolve it before publishing. This workflow does not modify branch protection or publish assets.

## Bounds and rollback

Jobs time out after 15 minutes, have no automatic retry and use isolated ephemeral runners. Repeated runs do not modify the repository. Cancel a run or disable/revert the workflow to stop execution. The workflow is excluded from installed releases; this record grants no authority to enable downstream CI. See [release policy](../RELEASE.md).
