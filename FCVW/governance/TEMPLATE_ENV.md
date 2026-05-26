# Template: Project Environment & Secrets Configuration

Save a completed copy of this document as your project's local configurations if applicable.

---

## 1. Required Variables Reference

Document all variables needed for local operation here.

| Variable Name | Role | Expected Value Format | Default Value | Notes |
|---|---|---|---|---|
| `PORT` | Local server port | Integer (e.g., 3000) | `3000` | — |
| `DB_CONNECTION` | Database connection string | URI string | `postgresql://localhost:5432` | Local dev DB |
| `USE_MOCKS` | Flag for sandbox mock data | Boolean (`true`/`false`) | `true` | Set true for AI agents |
| `API_GATEWAY_URL` | Microservices entry | URL | `https://dev.api.internal` | Local fallback available |

---

## 2. Secrets Insertion Procedures

Provide precise instructions on how developers and CI/CD pipelines should retrieve and inject active secrets:

### 2.1 Local Workspace Injection
1. Copy `.env.example` to `.env` in the project root.
2. Request a developer sandbox account from the Lead Developer.
3. Replace the placeholder tokens in `.env` with your sandbox credentials.
4. **Never commit the `.env` file.**

### 2.2 CI/CD Integration
* In your CI/CD platform (e.g., GitHub Actions, GitLab CI), navigate to Repository Settings -> Secrets.
* Inject all variables required by tests and builds using their exact names listed in the table above.
