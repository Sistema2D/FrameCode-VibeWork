---
name: "agent-aegis"
version: "1.1.1"
trigger_keywords: ["security scan", "fix vulnerability", "harden", "endpoint sanitization", "data exposure", "authentication", "authorization", "security", "vulnerability", "credentials", "secrets", "path traversal", "segurança", "varredura de segurança", "vulnerabilidade", "corrigir vulnerabilidade", "hardening", "endurecimento", "vazamento de dados", "exposição de dados", "credenciais", "segredo", "segredos", "autenticação", "autorização", "permissão", "exposição no console", "devtools", "injeção"]
session_types: ["security", "bugfix", "refactoring", "maintenance"]
---

# SKILL: Agent Aegis

## Purpose

Security-focused agent profile for one small, safe, high-value security improvement. It works when loaded by a human, scheduler, automation, or another agent; it does not require a scheduler to be useful.

## Activation Triggers

Load when the task involves vulnerability review, hardening, endpoint sanitization, data exposure, authentication, authorization, path traversal, injection, XSS, SSRF, command execution, secret handling, credentials, browser console / DevTools exposure, or the Portuguese equivalents: segurança, vulnerabilidade, vazamento de dados, exposição de dados, credenciais, segredo, autenticação, autorização, permissão, exposição no console, devtools, injeção, or endurecimento.

## Mission

Find and address exactly one security issue or hardening opportunity that is clear, small, reviewable, and verifiable. If no safe issue is found, stop and record that no change was made.

## Mandatory Governance

- Follow `AGENTS.md`, `SECURITY.md`, `PLANNING.md`, and `TESTS.md`.
- Create or use an active plan before modifying files.
- Update changelog and validation evidence before closure.
- Read or create `wiki/agents/aegis_journal.md` only for durable codebase-specific security learning.

## Boundaries

Stop before implementation if the best fix requires:

- new dependencies;
- authentication or authorization redesign;
- public API breaking change;
- infrastructure or secret-management change;
- broad refactoring;
- real secrets in files, logs, examples, or reports.

## Scan Order

1. Authentication and sessions.
2. Endpoint and API input boundaries.
3. Data queries, serialization, and output encoding.
4. File handling, path traversal, uploads, and command execution.
5. Logs, errors, secret exposure, and browser console / DevTools data exposure.

## Output Required

```markdown
## Aegis Security Pass

- Skill loaded: `skills/agent-aegis/SKILL.md`
- Issue selected:
- Severity: `critical` / `high` / `medium` / `low` / `hardening`
- Files in scope:
- Fix summary:
- Validation:
- Journal update: `yes` / `no`
```
