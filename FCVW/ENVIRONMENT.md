---
schema: "fcvw/project-environment@1"
artifact_role: "project_profile"
owner: "project"
upgrade_strategy: "preserve"
instantiation_status: "pending"
---

# Environment and deployment profile

## Environments

| Environment | Purpose | Data policy | Deployment owner | Promotion gate |
|---|---|---|---|---|
| Development | | | | |
| Test | | | | |
| Staging | | | | |
| Production | | | | |

Use only environments that exist. Document compensating controls when physical separation is unavailable.

## Configuration

- Commit safe examples; never commit live secrets.
- Record variable name, purpose, required/optional status, safe example, and validation.
- Define precedence among CLI, environment, profile files, and defaults.
- Fail closed when a required production setting is missing.

## Promotion

1. Build an immutable candidate.
2. Validate in the source environment.
3. Back up or establish rollback.
4. Promote without silently changing configuration.
5. Run health, authentication, data, and primary-flow smoke checks.
6. Record evidence and publish the release only after target validation.

## Runtime profile

- Start command:
- Stop command:
- Health endpoint/check:
- Readiness endpoint/check:
- Logs:
- Backup:
- Rollback:
- Supported host/port rules:

## Environment variables

| Name | Required | Secret | Safe example | Validation |
|---|---|---|---|---|
| | | | | |
