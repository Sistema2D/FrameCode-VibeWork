---
title: "Environment and Secrets Governance"
type: "concept"
status: "validated"
confidence: "high"
last_reviewed: "2026-05-26"
related_version: "V0.6.0"
sources:
  - "SECURITY.md"
  - "DATA.md"
tags:
  - "environment"
  - "secrets"
  - "governance"
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

## 5. Security & Secret Rotation

In the event of a credential leak (detected or suspected):

1. **Immediate Revocation:** The administrator must immediately revoke the leaked credential at the provider.
2. **Log the Incident:** Record the occurrence in `troubleshooting/` detailing the impact window and containment steps, but excluding the leaked value.
3. **Clean Git History:** If committed, run a history scrub (e.g., using `git-filter-repo` or BFG Repo-Cleaner) to purge the secret from all branches.

---

## 6. AI Agent Checklist

Before completing any task related to environment variables, the AI agent must verify:

- [ ] I have not written or committed any raw keys, tokens, or credentials.
- [ ] Any new configuration key is documented in `FCVW/ENVIRONMENT.md` or the project `.env.example`.
- [ ] **Active Environment Warning**: If I modified `.env.example`, I MUST immediately output a `> [!WARNING]` markdown alert in the chat instructing the human user to manually replicate the new key in their local `.env` file to prevent silent application crashes.
- [ ] The `.gitignore` file includes strict overrides for all active runtime configuration files.
- [ ] Local development configurations fallback safely to mocks or sandbox environments.
