# MANIFEST.md

Operational manifest of the project.

This file centralizes the identity, state, main rules, and official documents of the project. It must serve as a quick reference for humans and AI agents before any analysis, planning, implementation, refactoring, validation, or release publication.


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
| Current Version | `V0.7.6` |
| Manifest Creation Date | `2026-05-15` |
| Last Update | `2026-05-29` |
| Project Status | `development` |

---

## 2. Project Objective

FrameCode VibeWork is a document-based governance framework for AI-assisted application development. It provides a structured lifecycle for planning, implementing, validating, and documenting changes while maintaining technical memory across sessions through compressed AI context and a LLM Wiki.

### 2.1 Handled Problem

```text
AI-assisted development sessions suffer from context loss between sessions, lack of traceability, scope creep, and repeated failures. Without a formal governance layer, AI agents act inconsistently, regenerate already-solved decisions, and accumulate technical debt silently.
```

### 2.2 Expected Result

```text
A repository that uses FrameCode VibeWork achieves: near-zero context loss between AI sessions (via AICC), formal traceability of every change (via Plans + changelogs), incremental technical memory (via LLM Wiki), on-demand specialized AI skills (via ASE), and a 70–80% reduction in governance token overhead per session.
```

---

## 3. Target Audience

| Audience | Description | Main Needs |
|---|---|---|
| Solo developers | Individuals building applications with AI pair programming tools | Session continuity, context compression, low governance overhead |
| Small development teams | 2–5 person teams combining human and AI contributors | Shared traceability, consistent decision records, audit trail |
| AI agents / LLMs | AI models acting as primary implementers in a codebase | Clear operational rules, selective document loading, skills engine |

---

## 4. Summarized Scope

### 4.1 In Scope

- Document-based governance system (Plans, changelogs, ADRs, audits)
- AI Interaction Context Compression (AICC) via session syntheses
- AI Skills Engine (ASE) with on-demand JIT skill loading
- LLM Wiki (Obsidian-compatible technical memory with Ingest/Query/Lint cycle)
- Declarative design system centralized in `DESIGN.md`
- Instantiation workflow for bootstrapping new projects from the framework

### 4.2 Out of Scope

- Application source code (framework is stack-agnostic)
- Automated CI/CD pipelines or scripts (deprecated by ADR-0001)
- Cloud deployment or hosting infrastructure
- AI model fine-tuning or RAG embedding pipelines

### 4.3 Main Dependencies

- Git (version control and release tagging)
- Markdown-compatible editor (Obsidian recommended for wiki graph view)
- Any LLM agent or AI coding assistant that can read and follow Markdown instructions

---

## 5. Summarized Stack

| Layer | Technology / Tool | Observations |
|---|---|---|
| Governance Layer | Markdown + Git | All plans, changelogs, ADRs, wiki, and skills are pure Markdown (ADR-0001) |
| Technical Memory | LLM Wiki (Obsidian-compatible) | `wiki/` directory with schema, index, log, sessions, and thematic subfolders |
| Persistence | Flat-file (`.md` files) | No database — all state is in versioned Markdown files |
| AI / LLM | Any LLM agent (model-agnostic) | Tested with Gemini, Claude, and GPT-class models |
| Skills Engine | ASE — on-demand SKILL.md files | Loaded JIT via `view_file` with `IsSkillFile: true`; never pre-loaded |
| Distribution | Git clone / GitHub template | Fork or clone to start a new project |
| Visualization | Obsidian (optional) | Graph view for wiki links; not required for operation |

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
| Change plans | Human / AI authoring | Local Git repo | Low | Plans contain design decisions, not personal or secret data |
| Session syntheses | AI-generated | `wiki/sessions/` | Low | Compressed context; must not contain secrets or API keys |
| Troubleshooting logs | Human / AI authoring | `troubleshooting/` | Low | Anonymize any path or environment-specific data before committing |
| Wiki knowledge pages | AI-generated / human-reviewed | `wiki/` subfolders | Low | Treated as reference data, not sovereign instructions |

---

## 7. Official Project Documents

The documents below compose the project's governance. The absence of any document must be recorded as a gap.

| Document | Mandatory | Role | Status |
|---|---:|---|---|
| `AGENTS.md` | Yes | Operational guide for AI agents and humans | `existing` |
| `FCVW/README.md` | Yes | Framework presentation, installation, execution, and usage | `existing` |
| `INSTANTIATION.md` | Phase 0 | Framework instantiation, renaming, and placeholders | `existing` |
| `SCOPE.md` | Yes | Functional scope and project boundaries | `existing` |
| `STACK.md` | Yes | Technical stack, dependencies, and environment | `existing` |
| `FILESYSTEM.md` | Yes | Physical folder structure blueprint and self-healing rules | `existing` |
| `DESIGN.md` | When UI | Visual guidelines and UX | `existing` |
| `WORKFLOW.md` | Yes | Functional flows, screens, events, and integrations | `existing` |
| `PLANNING.md` | Yes | Method for change plans | `existing` |
| `VERSIONING.md` | Yes | Versioning rules and changelogs | `existing` |
| `TROUBLESHOOTING.md` | Yes | Issue recording and handling | `existing` |
| `TESTS.md` | Yes | Testing and validation rules | `existing` |
| `SECURITY.md` | Yes | Security and privacy rules | `existing` |
| `DATA.md` | When persistence | Data, storage, migration, and backup | `existing` |
| `ENVIRONMENT.md` | Yes | Environment configurations and secrets governance | `existing` |
| `PERFORMANCE.md` | Yes | Performance budgets and network caching governance | `existing` |
| `AI.md` | When AI | AI usage, boundaries, and governance | `existing` |
| `REFACTORING.md` | Yes | Criteria and metrics for refactoring | `existing` |
| `RELEASE.md` | Yes | Operational publication procedure | `existing` |
| `AUDIT.md` | Yes | Document and technical compliance checklists | `existing` |
| `ARCHITECTURAL_DECISIONS.md` | Recommended | Registry of architectural decisions | `existing` |
| `BRIEFING.md` | Phase 0 | Discovery and initial project briefing | `existing` |
| `CONTEXT_MAP.md` | When AI | Selective context loading map by session type | `existing` |
| `wiki/schema.md` | When vault/RAG | Operational rules of the wiki in LLM Wiki standard | `existing` |
| `wiki/sessions/README.md` | When AI | Index and chronological ledger of AI session contexts | `existing` |
| `skills/README.md` | When AI | Index and guidelines catalog of AI agent skills | `existing` |

---

## 8. Expected Repository Structure

The detailed repository tree is maintained in `FILESYSTEM.md`, which is the source of truth for structural audits. This manifest only records the ownership rule:

- the repository root belongs to the application under development;
- `AGENTS.md` and bridge/configuration files may remain at the root;
- official framework documents and generated framework documentation remain under `FCVW/`;
- the root `README.md`, when present, must describe the target application, not the framework.

The framework baseline keeps official framework documents inside `FCVW/`, with `AGENTS.md` at the root as the bridge entrypoint. During application instantiation, the root `README.md` must be generated for the target application. The `governance/` folder must contain only reusable empty templates.

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
| Context drift between AI sessions | Medium | High | AICC session synthesis standard; wiki/sessions/ ledger | `AI.md`, `wiki/schema.md` |
| Scope creep by AI agents | Medium | High | Mandatory plan before any change; AGENTS.md checklist | `AGENTS.md`, `PLANNING.md` |
| Secrets accidentally committed | Low | Critical | No automation scripts; AI.md data rules; manual review | `SECURITY.md`, `AI.md` |
| Template placeholders left unfilled in downstream projects | Medium | Medium | INSTANTIATION.md renaming checklist; MANIFEST.md gap section | `INSTANTIATION.md`, `MANIFEST.md` |
| Wiki knowledge becoming stale | Medium | Medium | Wiki Lint on every minor/major release; log.md tracking | `wiki/schema.md`, `skills/wiki-lint/SKILL.md` |

---

## 13. Structural Gaps

Use this section to record document or structural gaps in the project.

| Gap | Impact | Priority | Related Plan | Status |
|---|---|---|---|---|
| No structural gaps identified at V0.5.0. | — | — | — | — |

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
| 2026-05-18 | `V0.4.0` | Transitioned to pure-markdown instruction model, deprecated mockups and automated scripts (ADR-0001). | Antigravity |
| 2026-05-22 | `V0.5.0` | Filled all placeholder fields; expanded ASE with 3 new skills; added CONTEXT_MAP.md; populated wiki; consolidated AICC templates; added TEMPLATE_TROUBLESHOOTING.md. | Antigravity |
| 2026-05-25 | `V0.5.2` | Clean up unused css variable. | Jules |
| 2026-05-26 | `V0.6.0` | Expanded framework: added ENVIRONMENT.md, PERFORMANCE.md, project-instantiation & aicc-compact skills, and integrated technical debt ledger. | Antigravity |
| 2026-05-29 | `V0.7.0` | Released modern internationalized `docs/index.html` and sanitized repository to zero-state distribution. | Sistema2D |
| 2026-05-29 | `V0.7.1` | Corrected root README getting-started flow to match the framework lifecycle. | Sistema2D |
| 2026-05-29 | `V0.7.2` | Copied `FCVW/docs/index.html` to root `docs/index.html` for GitHub Pages compatibility. | Sistema2D |
| 2026-05-29 | `V0.7.3` | Added Star History and Buy Me a Coffee references to the public README. | Sistema2D |
| 2026-05-29 | `V0.7.4` | Expanded root README with operational routing flowcharts. | Sistema2D |
| 2026-05-29 | `V0.7.5` | Fixed Mermaid syntax in root README routing flowcharts. | Sistema2D |
| 2026-05-29 | `V0.7.5` | Reconciled governance metadata, mandatory troubleshooting structure, and current-version documentation. | Codex |
| 2026-05-29 | `V0.7.5` | Deprecated framework-owned root README, root docs duplicate, and `FCVW/snippets/`; centralized design rules in `DESIGN.md`. | Codex |

---

## 15. Governance Statement

This project must be conducted with traceability, validation, scope control, security, updated documentation, and coherent versioning.

No human or AI agent should treat governance documents as optional when the requested action involves changing code, documentation, configuration, design, tests, versioned data, build, release, security, or functional behavior.
