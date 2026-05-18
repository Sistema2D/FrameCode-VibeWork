# MANIFEST.md

Operational manifest of the project.

This file centralizes the identity, state, main rules, and official documents of the project. It must serve as a quick reference for humans and AI agents before any analysis, planning, implementation, refactoring, validation, or release publication.

> This is a template. Replace the fields between `<...>` with the actual information of the project.

---

## 1. Project Identification

| Field | Information |
|---|---|
| Project Name | `<project-name>` |
| Short Name / Codename | `<short-name>` |
| Application Type | `<web / desktop / mobile / CLI / API / library / hybrid>` |
| Target Platform | `<Windows / Linux / macOS / Web / Android / iOS / cross-platform>` |
| Main Lead | `<name>` |
| Repository | `<URL or local path>` |
| Current Version | `V0.3.1` |
| Manifest Creation Date | `YYYY-MM-DD` |
| Last Update | `2026-05-18` |
| Project Status | `concept / planning / development / validation / published / suspended / discontinued` |

---

## 2. Project Objective

Describe, in a few lines, the main objective of the application.

```text
<Describe here the problem the application solves, who it is intended for, and what value it delivers.>
```

### 2.1 Handled Problem

```text
<Describe the problem, limitation, need, or opportunity that motivated the project.>
```

### 2.2 Expected Result

```text
<Describe the practical result expected when the application is functional.>
```

---

## 3. Target Audience

| Audience | Description | Main Needs |
|---|---|---|
| `<group 1>` | `<description>` | `<main needs>` |
| `<group 2>` | `<description>` | `<main needs>` |

---

## 4. Summarized Scope

### 4.1 In Scope

- `<feature or responsibility 1>`
- `<feature or responsibility 2>`
- `<feature or responsibility 3>`

### 4.2 Out of Scope

- `<item explicitly out of scope 1>`
- `<item explicitly out of scope 2>`
- `<item explicitly out of scope 3>`

### 4.3 Main Dependencies

- `<technical, operational, or external dependency 1>`
- `<technical, operational, or external dependency 2>`
- `<technical, operational, or external dependency 3>`

---

## 5. Summarized Stack

| Layer | Technology / Tool | Observations |
|---|---|---|
| Frontend | `<technology>` | `<observations>` |
| Backend | `<technology>` | `<observations>` |
| Database / Persistence | `<technology>` | `<observations>` |
| AI / LLM | `<model, runtime, or provider>` | `<observations>` |
| Build | `<tool>` | `<observations>` |
| Tests | `<tool>` | `<observations>` |
| Distribution | `<format>` | `<observations>` |

---

## 6. AI Usage in the Project

### 6.1 AI Roles in the Application

Mark or describe the planned roles:

- [ ] Conversational chat.
  - [ ] RAG / knowledge base query.
  - [ ] Text generation.
  - [ ] Code generation.
  - [ ] Classification or data extraction.
  - [ ] Agents with tools.
  - [ ] Task automation.
  - [x] Continuous learning (Ingest/Query/Lint cycle described in `wiki/schema.md`).
  - [x] AI Interaction Context Compression (AICC).
  - [x] AI Skills Engine (ASE) with trigger activation.
  - [ ] Other: `<describe>`.

### 6.2 AI Boundaries

- The AI must not execute destructive actions without explicit confirmation.
- The AI must not access data outside the allowed directories.
- The AI must not invent sources, files, system states, or validation results.
- The AI must report limitations when it cannot validate information.
- The AI must respect the official documents of the project.

### 6.3 Data Used by the AI

| Data Type | Origin | Persistence | Sensitivity | Observations |
|---|---|---|---|---|
| `<type>` | `<origin>` | `<local>` | `<low/medium/high>` | `<observations>` |

---

## 7. Official Project Documents

The documents below compose the project's governance. The absence of any document must be recorded as a gap.

| Document | Mandatory | Role | Status |
|---|---:|---|---|
| `AGENTS.md` | Yes | Operational guide for AI agents and humans | `<existing/pending>` |
| `README.md` | Yes | Presentation, installation, execution, and usage | `<existing/pending>` |
| `INSTANTIATION.md` | Phase 0 | Framework instantiation, renaming, and placeholders | `<existing/pending/not applicable>` |
| `SCOPE.md` | Yes | Functional scope and project boundaries | `<existing/pending>` |
| `STACK.md` | Yes | Technical stack, dependencies, and environment | `<existing/pending>` |
| `FILESYSTEM.md` | Yes | Physical folder structure blueprint and self-healing rules | `<existing>` |
| `DESIGN.md` | When UI | Visual guidelines and UX | `<existing/pending/not applicable>` |
| `WORKFLOW.md` | Yes | Functional flows, screens, events, and integrations | `<existing/pending>` |
| `PLANNING.md` | Yes | Method for change plans | `<existing/pending>` |
| `VERSIONING.md` | Yes | Versioning rules and changelogs | `<existing/pending>` |
| `TROUBLESHOOTING.md` | Yes | Issue recording and handling | `<existing/pending>` |
| `TESTS.md` | Yes | Testing and validation rules | `<existing/pending>` |
| `SECURITY.md` | Yes | Security and privacy rules | `<existing/pending>` |
| `DATA.md` | When persistence | Data, storage, migration, and backup | `<existing/pending/not applicable>` |
| `AI.md` | When AI | AI usage, boundaries, and governance | `<existing/pending/not applicable>` |
| `REFACTORING.md` | Yes | Criteria and metrics for refactoring | `<existing/pending>` |
| `RELEASE.md` | Yes | Operational publication procedure | `<existing/pending>` |
| `AUDIT.md` | Yes | Document and technical compliance checklists | `<existing/pending>` |
| `ARCHITECTURAL_DECISIONS.md` | Recommended | Registry of architectural decisions | `<existing/pending>` |
| `BRIEFING.md` | Phase 0 | Discovery and initial project briefing | `<existing/pending/not applicable>` |
| `wiki/schema.md` | When vault/RAG | Operational rules of the wiki in LLM Wiki standard | `<existing/pending/not applicable>` |
| `wiki/sessions/README.md` | When AI | Index and chronological ledger of AI session contexts | `existing` |
| `skills/README.md` | When AI | Index and guidelines catalog of AI agent skills | `existing` |

---

## 8. Expected Repository Structure

```text
.
├── AGENTS.md
├── MANIFEST.md
├── README.md
├── INSTANTIATION.md
├── SCOPE.md
├── STACK.md
├── FILESYSTEM.md
├── DESIGN.md
├── WORKFLOW.md
├── PLANNING.md
├── VERSIONING.md
├── TROUBLESHOOTING.md
├── TESTS.md
├── SECURITY.md
├── DATA.md
├── AI.md
├── REFACTORING.md
├── RELEASE.md
├── AUDIT.md
├── ARCHITECTURAL_DECISIONS.md
├── Plans/
│   ├── pending/
│   ├── in_progress/
│   ├── completed/
│   └── discontinued/
├── changelogs/
├── troubleshooting/
├── decisions/
├── audits/
├── briefings/
├── wiki/
│   ├── README.md
│   ├── index.md
│   ├── log.md
│   ├── schema.md
│   ├── templates/
│   │   └── TEMPLATE_SESSION_SYNTHESIS.md
│   └── sessions/
│       └── README.md
├── governance/
│   ├── README_FRAMEWORK.md
│   ├── TEMPLATE_AI_SESSION_SYNTHESIS.md
│   └── TEMPLATE_PLAN.md
├── skills/
│   ├── README.md
│   └── obsidian-markdown/
│       └── SKILL.md
├── mockups/
├── .gitignore
├── src/
├── tests/
└── build/
```

Adapt this structure according to the actual tech stack of the project.

The completed project documents must reside at the root. The `governance/` folder, when kept in the repository, should contain only reusable empty templates.

---

---

## 9. Operational Governance

Conduct rules, change flows, and quality checklists are centralized in:

- `AGENTS.md`: Daily operational guide and execution checklists.
- `AUDIT.md`: Formal compliance and pre-release checklists.
- `PLANNING.md`: Detailed methodology for change plans.

No functional, visual, or structural change should be performed without following the flows defined in these documents.

---

## 12. Main Project Risks

| Risk | Probability | Impact | Mitigation | Related Document |
|---|---|---|---|---|
| `<risk 1>` | `<low/medium/high>` | `<low/medium/high>` | `<action>` | `<document>` |
| `<risk 2>` | `<low/medium/high>` | `<low/medium/high>` | `<action>` | `<document>` |

---

## 13. Structural Gaps

Use this section to record document or structural gaps in the project.

| Gap | Impact | Priority | Related Plan | Status |
|---|---|---|---|---|
| `<gap>` | `<impact>` | `<P1-P5>` | `<file in Plans/>` | `<status>` |

---

## 14. Manifest Update History

| Date | Project Version | Change in Manifest | Author |
|---|---|---|---|
| 2026-05-15 | `V0.0.0` | Manifest creation. | Hugo Araújo de Melo |
| 2026-05-15 | `V0.0.1` | Added Star History to README. | Antigravity |
| 2026-05-17 | `V0.1.0` | Repository internationalization: translated all files and structures to English. | Antigravity |
| 2026-05-17 | `V0.1.1` | Implemented FILESYSTEM.md and sync-filesystem.ps1 script. | Antigravity |
| 2026-05-17 | `V0.1.2` | Implemented mockup calibration system and TEMPLATE_VISUAL_DIFF.md. | Antigravity |
| 2026-05-17 | `V0.1.3` | Implemented database schema update protocols and token optimization. | Antigravity |
| 2026-05-18 | `V0.2.0` | Implemented AI Interaction Context Compression (AICC) system. | Antigravity |
| 2026-05-18 | `V0.2.1` | Added bilingual token consumption estimates to README.md and AI.md. | Antigravity |
| 2026-05-18 | `V0.3.0` | Implemented AI Skills Engine (ASE) and integrated obsidian-markdown skill. | Antigravity |
| 2026-05-18 | `V0.3.1` | Aligned README.md visual directory trees with physical filesystem tree. | Antigravity |

---

## 15. Governance Statement

This project must be conducted with traceability, validation, scope control, security, updated documentation, and coherent versioning.

No human or AI agent should treat governance documents as optional when the requested action involves changing code, documentation, configuration, design, tests, versioned data, build, release, security, or functional behavior.
