# MANIFEST.md

Operational manifest of the project.

---

## 1. Project Identification

| Field | Information |
|---|---|
| Project Name | `FrameCode VibeWork` |
| Short Name / Codename | `FCVW` |
| Application Type | `framework / governance template` |
| Target Platform | `cross-platform (Windows / Linux / macOS)` |
| Main Lead | `Hugo Araújo de Melo` |
| Repository | `https://github.com/Sistema2D/FrameCode-VibeWork` |
| Current Version | `V0.12.0` |
| Manifest Creation Date | `2026-05-15` |
| Last Update | `2026-06-23` |
| Project Status | `development` |

---

## 2. Project Objective

FrameCode VibeWork is a Markdown-first governance framework for AI-assisted software development. It provides traceable planning, versioned changelogs, audits, troubleshooting, decisions, technical memory, on-demand skills, declarative automation contracts, and token-budget guidance.

## 3. Summarized Scope

### 3.1 In Scope

- Document-based governance system.
- Plans, changelogs, ADRs, audits, troubleshooting, and releases.
- AICC session context compression.
- AI Skills Engine with JIT skill loading.
- LLM Wiki technical memory.
- Declarative automation contracts in Markdown.
- Output-token economy guidance through `TOKEN_BUDGET.md`.
- New and retroactive project instantiation.
- Governed refactoring and anti-monolith gates.

### 3.2 Out of Scope

- Application source code.
- Executable automation in the Scenario 1 baseline.
- Installed Git hooks, coded watchers, background daemons, package dependencies, provider SDKs, API-key integrations, or CI/CD workflows.
- Cloud deployment or hosting infrastructure.
- AI fine-tuning or embedding pipelines.

## 4. Summarized Stack

| Layer | Technology / Tool | Observations |
|---|---|---|
| Governance | Markdown + Git | Canonical source of truth |
| Technical Memory | LLM Wiki | `wiki/` with index, log, sessions, releases, and source notes |
| Skills | ASE | JIT skill loading from `skills/` |
| Token Economy | AICC + Token Budget | Input and output token optimization |
| Declarative Automation | Markdown-only contracts | `AUTOMATION`, `HOOKS`, `WATCHERS`, `DAEMONS`, `GOVERNANCE_GATES` |

## 5. Official Project Documents

| Document | Role |
|---|---|
| `AGENTS.md` | Operational guide for humans and agents |
| `FCVW/README.md` | Framework README |
| `FCVW/MANIFEST.md` | Identity, scope, and operational state |
| `FCVW/STACK.md` | Stack and dependency posture |
| `FCVW/FILESYSTEM.md` | Physical tree source of truth |
| `FCVW/CONTEXT_MAP.md` | Selective context loading map |
| `FCVW/PLANNING.md` | Change planning methodology |
| `FCVW/TOKEN_BUDGET.md` | Output-token economy guidance |
| `FCVW/AUTOMATION.md` | Declarative automation parent contract |
| `FCVW/HOOKS.md` | Pseudo-hook checklists |
| `FCVW/WATCHERS.md` | Event/reaction watcher rules |
| `FCVW/DAEMONS.md` | Manual/agentic maintenance loops |
| `FCVW/GOVERNANCE_GATES.md` | Governance gate mapping |
| `FCVW/AI.md` | AI usage and boundaries |
| `FCVW/SECURITY.md` | Security and privacy boundaries |
| `FCVW/VERSIONING.md` | Version and changelog rules |
| `FCVW/RELEASE.md` | Release procedure |
| `FCVW/wiki/` | Technical memory |
| `FCVW/skills/` | On-demand AI skills |

## 6. External Inspiration and Credit

Scenario 1 declarative automation credits conceptual inspiration from `https://github.com/SantanderAI`. No SantanderAI source code was copied into FCVW.

## 7. Main Project Risks

| Risk | Mitigation |
|---|---|
| Context drift | AICC and wiki session syntheses |
| Scope creep | Mandatory plans and risk gates |
| Excessive token use | `CONTEXT_MAP.md`, JIT skills, AICC, and `TOKEN_BUDGET.md` |
| Automation terms misread as runtime permission | ADR-0002 and Markdown-only contracts |
| Secrets committed | `SECURITY.md` and Secret Handshake |
| Skill proliferation | `agent-factory` and `self-improvement` gates |

## 8. Manifest Update History

| Date | Project Version | Change in Manifest | Author |
|---|---|---|---|
| 2026-05-15 | `V0.0.0` | Manifest creation. | Hugo Araújo de Melo |
| 2026-05-18 | `V0.4.0` | Pure Markdown instruction model and ADR-0001. | Antigravity |
| 2026-06-11 | `V0.8.0` | Structural reconciliation and governance validator. | Buffy |
| 2026-06-13 | `V0.10.0` | Controlled skill/agent factory and self-improvement gates. | Codex |
| 2026-06-17 | `V0.11.0` | Continuous wiki curation governance. | Codex |
| 2026-06-23 | `V0.12.0` | Declarative automation contracts, token budget guidance, and bilingual README refresh. | GPT-5.5 Thinking |

## 9. Governance Statement

FCVW changes must preserve traceability, validation, scope control, security, version coherence, Markdown-first portability, and token-aware operation.
