---
schema: "fcvw/automation@1"
id: "AUT-2026-09-22-local-validation"
artifact_role: "record"
record_scope: "framework"
upgrade_strategy: "preserve"
owner: "framework-maintainer"
kind: "governance_gate"
status: "active"
scenario: "2"
execution_mode: "scenario_2"
authorized_by: "User requested a free alternative to hosted Actions and continuation"
trigger: "Explicit local invocation before accepting a source change or publishing artifacts"
preconditions: "Trusted FCVW source/template and explicitly selected installed Python interpreters"
permissions: "Read local sources; execute trusted checks; write local logs and temporary fixtures; no service credentials"
actions: "Run tests, governance, labeled benchmark, installed-layout smoke and optional complete release verification"
evidence: "Local report.json, per-command logs, benchmark JSON, runtime identity and source digest"
failure_policy: "Any failed or timed-out command, missing interpreter, invalid asset set or changed source makes the command fail"
rollback: "Stop invoking the runner; individual validation commands remain available"
---

# Local validation contract

## Scope and authority

The optional local command implements [AUTOMATION.md](../AUTOMATION.md) Scenario 2 and [TESTS.md](../TESTS.md). It replaces the [retired hosted contract](CI_CONTRACT.md), with no hosted account, paid runner, scheduler, Git hook or background service. Run it only against trusted code and interpreters. Executed tests have the current user's permissions and are not sandboxed by this wrapper.

## Checks and evidence

Run source tests, clean-template governance, the labeled retrieval benchmark and a temporary installed-layout smoke test for every explicitly requested Python executable. A missing executable is an error, not a skipped matrix entry. Optional release verification requires exactly one version's four language ZIPs and its checksum file; the existing verifier compares installed Python tools to the selected trusted release source before executing them. No assets or interpreters are downloaded automatically.

Each invocation creates a distinct local report directory. JSON records the OS, interpreter version/path, command, return status, duration and log path, plus Git revision/dirty state when available and a digest of source files. Optional archive and checksum-file SHA-256 values are also recorded. Cache, Git/editor state and the generated role manifest are excluded from the source digest. Source or asset changes during execution invalidate the run. Reports are observations, not signed attestations or proof of independent CI. Missing OS coverage remains unverified.

## Failure, retention and rollback

Steps run sequentially; one failure cannot be hidden by a later success. The default timeout is 900 seconds per direct command and is configurable. A timeout fails the run; inspect any independently spawned child activity before retrying. Logs may contain local paths or test output; review before sharing. Reports stay local until the maintainer deletes or explicitly shares them. No credentials, account changes, branch protection changes, uploads or publication actions are built into the runner.

The maintainer runs the command before accepting changes. Automatic pull-request enforcement is not provided. Stop invoking or revert the wrapper to disable it; the underlying commands still work. To validate another OS, execute the same command on that OS and keep its separate report. See [release policy](../RELEASE.md).
