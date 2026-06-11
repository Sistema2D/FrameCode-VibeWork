---
title: "Environment and Secrets Governance"
type: "concept"
status: "validated"
confidence: "high"
last_reviewed: "2026-06-11"
related_version: "V0.8.0"
sources:
  - "SECURITY.md"
  - "DATA.md"
tags:
  - "environment"
  - "secrets"
  - "governance"
  - "deployment"
---

# Environment and Secrets Governance

This document establishes the official policies for managing environment variables, configurations, mock endpoints, and sensitive credentials in a FrameCode VibeWork project. It ensures that the application remains secure, portable, and easily deployable across environments without risking the accidental exposure of private data.

---

## 1. The Golden Rules of Secrets

To prevent high-risk vulnerabilities, every human developer and AI agent must strictly enforce these five principles:

1. **No Credentials in Code:** Never commit passwords, tokens, API keys, certificates, or personal identifiers to version control.
2. **Mandatory Gitignore Filtering:** All files containing active runtime environment values (such as `.env`, `.env.local`, `config.json`) must be strictly filtered in `.gitignore`.
3. **Canonical Example Standard:** Every environment file must have a matching `.env.example` in version control, detailing all key names, types, and descriptive instructions, but containing only safe placeholders.
4. **Agent Sandbox Isolation:** The AI agent must never read or extract active production secret files during development or debugging sessions.
5. **Fail-Safe Defaults:** The codebase must employ default values for local development that do not require valid production integrations, falling back gracefully to mock servers.

---

## 2. Environment Segmentation

The project recognizes three major environments, each with its own operational rules:

| Environment | Scope | Access Controls | Persistence Type |
|---|---|---|---|
| **Development** | Local workspace, debugging | Developer local variables, sandbox credentials | Local storage, file-based database |
| **Staging** | Pre-production testing, auditing | Protected credentials, isolated database systems | Dedicated testing database instances |
| **Production** | Live system serving end-users | High-security credentials, production vault storage | Secure, encrypted relational databases |

---

## 3. The `.env.example` Structural Standard

Any change that introduces a new configuration variable must immediately update `.env.example`. The template follows this semantic format:

```text
# ==============================================================================
# PROJECT ENVIRONMENT VARIABLES TEMPLATE (.env.example)
# Application: [Name]
# Version: V[x.y.z]
# ==============================================================================

# --- DATABASE CONFIGURATION ---
# Database host address. (Default: localhost)
DB_HOST=localhost
# Database port number. (Default: 5432)
DB_PORT=5432
# Database name.
DB_NAME=my_app_dev
# DO NOT include DB_USER or DB_PASSWORD here. Document them in instructions.

# --- THIRD-PARTY INTEGRATIONS ---
# API key for the payment gateway. (Placeholder: Insert sandbox token)
PAYMENT_GATEWAY_KEY=PLACEHOLDER_SANDBOX_TOKEN
# Base URL for the weather microservice. (Default: Mock URL)
WEATHER_SERVICE_URL=https://mock.weather.local/api
```

---

## 4. Mock APIs and Offline Execution

To ensure portability and token efficiency for AI agents:

- The system must provide a flag or variable (e.g., `USE_MOCKS=true`) that intercepts HTTP queries and redirects them to local mock data.
- This allows the agent to run and validate components in sandboxes without possessing active developer accounts or external network keys.
- Mock handlers must reside under `src/mocks/` or a similar folder and mirror the exact payloads of external APIs.

---

## 5. Environment Promotion Workflow

This section defines how changes and releases flow across the three environments (Development → Staging → Production). The goal is to ensure every change is validated in progressively more production-like conditions before reaching end users.

### Environment Roles

| Environment | Role | Access | Data | Validation Required |
|---|---|---|---|---|
| **Development** | Active development, debugging, and local testing | Developer local machine | Mock or anonymized data | Build + local tests + plan validation |
| **Staging** | Pre-production validation, integration testing, audit | Protected team access | Sanitized or synthetic dataset | All development validation + integration tests + audit (`AUDIT.md`) |
| **Production** | Live end-user service | Restricted ops access | Real user data | All staging validation + rollback plan + human approval |

### Promotion Gate: Development → Staging

A change moves from Development to Staging when:

1. The plan is complete and located in `Plans/completed/`.
2. All acceptance criteria from the plan are validated.
3. The change compiles/builds without errors.
4. Local tests pass (or limitations are documented).
5. Code review is complete per the risk level (see `AGENTS.md §Code Review and Pull Requests`).
6. The PR is merged into the main development branch.

The staging deployment can be triggered by the merge event or scheduled — the framework does not prescribe the mechanism, but the validation evidence must exist before considering the promotion complete.

### Promotion Gate: Staging → Production

A change moves from Staging to Production when:

1. The release is prepared and documented per `RELEASE.md`.
2. The audit per `AUDIT.md` passes.
3. Staging validation confirms all critical workflows function correctly.
4. Rollback procedure is documented.
5. Known gaps are recorded.
6. Human approval is obtained for the deployment.

### Rollback During Promotion

If a deployed change fails validation in the target environment:

1. **Immediate rollback**: Revert the deployment to the previous stable version in that environment.
2. **Record the failure**: Create a troubleshooting record in `troubleshooting/` detailing symptoms, impact, and rollback actions.
3. **Investigate**: Use `skill:systematic-debugging` to determine root cause.
4. **Plan correction**: Create a new plan to fix the issue, referencing the troubleshooting record.
5. **Re-promote**: After fix validation, repeat the promotion flow.

### Promotion Without an Environment

Projects with a single environment (e.g., solo developer, no staging) can treat the promotion gates as validation checkpoints: Development gates validate before merge, and Production gates validate before considering the change delivered. The environment column becomes a validation stage rather than a physical deployment target.

---

## 6. Security & Secret Rotation

In the event of a credential leak (detected or suspected):

1. **Immediate Revocation:** The administrator must immediately revoke the leaked credential at the provider.
2. **Log the Incident:** Record the occurrence in `troubleshooting/` detailing the impact window and containment steps, but excluding the leaked value.
3. **Clean Git History:** If committed, run a history scrub (e.g., using `git-filter-repo` or BFG Repo-Cleaner) to purge the secret from all branches.

---

## 7. AI Agent Checklist

Before completing any task related to environment variables, the AI agent must verify:

- [ ] I have not written or committed any raw keys, tokens, or credentials.
- [ ] Any new configuration key is documented in `FCVW/ENVIRONMENT.md` or the project `.env.example`.
- [ ] **Active Environment Warning**: If I modified `.env.example`, I MUST immediately output a `> [!WARNING]` markdown alert in the chat instructing the human user to manually replicate the new key in their local `.env` file to prevent silent application crashes.
- [ ] The `.gitignore` file includes strict overrides for all active runtime configuration files.
- [ ] Local development configurations fallback safely to mocks or sandbox environments.
- [ ] For promotion between environments, follow the workflow in `FCVW/ENVIRONMENT.md §5`.
