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
| Current Version | `V0.11.0` |
| Manifest Creation Date | `2026-05-15` |
| Last Update | `2026-06-23` |
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
A repository that uses FrameCode VibeWork achieves: near-zero context loss between AI sessions (via AICC), formal traceability of every change (via Plans + changelogs), incremental technical memory (via LLM Wiki), on-demand specialized AI skills (via ASE), controlled declarative automation contracts, and a significant reduction in governance token overhead per session.
```

---

## 3. Target Audience

| Audience | Description | Main Needs |
|---|---|---|
| Solo developers | Individuals building applications with AI pair programming tools | Session continuity, context compression, low governance overhead |
| Small development teams | 2–5 person teams combining human and AI contributors | Shared traceability, consistent decision records, audit trail |
| AI agents / LLMs | AI models acting as primary implementers in a codebase | Clear operational rules, selective document loading, skills engine, safe automation boundaries |

---

## 4. Summarized Scope

### 4.1 In Scope

- Document-based governance system (Plans, changelogs, ADRs, audits)
- AI Interaction Context Compression (AICC) via session syntheses
- AI Skills Engine (ASE) with on-demand JIT skill loading
- LLM Wiki (Obsidian-compatible technical memory with Ingest/Query/Curate/Lint cycle)
- Declarative design system centralized in `DESIGN.md`
- Instantiation workflow for bootstrapping new projects from the framework
- Anti-monolith and code hygiene gates for AI-generated codebases
- Retroactive cleanup triage for existing applications adopting the framework
- Controlled creation and self-improvement gates for AI skills and agent profiles
- Continuous wiki curation with canonical taxonomy, thematic frontmatter colors, and freshness metrics
- Declarative automation contracts for pseudo-hooks, watcher rules, manual/agentic daemon loops, and governance gates, expressed only in Markdown

### 4.2 Out of Scope

- Application source code (framework is stack-agnostic)
- Executable automation, installed Git hooks, local daemons, coded watchers, package dependencies, provider SDKs, API-key integrations, or CI/CD workflows in the Scenario 1 baseline
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
| Governance Layer | Markdown + Git | All plans, changelogs, ADRs, wiki, skills, and declarative automation contracts are Markdown-first |
| Technical Memory | LLM Wiki (Obsidian-compatible) | `wiki/` directory with schema, index, log, sessions, and thematic subfolders |
| Persistence | Flat-file (`.md` files) | No database in the framework baseline — all state is in versioned Markdown files |
| AI / LLM | Any LLM agent (model-agnostic) | Tested with Gemini, Claude, and GPT-class models |
| Skills Engine | ASE — on-demand SKILL.md files | Loaded JIT via `view_file` with `IsSkillFile: true`; never pre-loaded |
| Declarative Automation | Markdown-only contracts | `AUTOMATION.md`, `HOOKS.md`, `WATCHERS.md`, `DAEMONS.md`, `GOVERNANCE_GATES.md` |
| Distribution | Git clone / GitHub template | Fork or clone to start a new project |
| Visualization | Obsidian (optional) | Graph view for wiki links; not required for operation |

---

## 6. AI Usage in the Project

### 6.1 AI Roles in the Application

- [ ] Conversational chat.
- [ ] RAG / knowledge base query.
- [ ] Text generation.
- [ ] Code generation.
- [ ] Classification or data extraction.
- [ ] Agents with tools.
- [ ] Task automation.
- [x] Continuous learning (Ingest/Query/Curate/Lint cycle described in `wiki/schema.md`).
- [x] AI Interaction Context Compression (AICC).
- [x] AI Skills Engine (ASE) with trigger activation.
- [x] Controlled skill/agent creation and self-improvement gates.
- [x] Fixed optimized wiki curation mode via `skills/wiki-curator/SKILL.md`.
- [x] Markdown-only declarative automation contracts under Scenario 1.

### 6.2 AI Boundaries

- The AI must not execute destructive actions without explicit confirmation.
- The AI must not access data outside the allowed directories.
- The AI must not invent sources, files, system states, or validation results.
- The AI must respect the official documents of the project.
- The AI must treat declarative hooks, watchers, daemons, and gates as Markdown governance contracts, not permission to execute commands.

### 6.3 Data Used by the AI

| Data Type | Origin | Persistence | Sensitivity | Observations |
|---|---|---|---|---|
| Change plans | Human / AI authoring | Local Git repo | Low | Plans contain design decisions, not personal or secret data |
| Session syntheses | AI-generated | `wiki/sessions/` | Low | Compressed context; must not contain secrets or API keys |
| Troubleshooting logs | Human / AI authoring | `troubleshooting/` | Low | Anonymize any path or environment-specific data before committing |
| Wiki knowledge pages | AI-generated / human-reviewed | `wiki/` subfolders | Low | Treated as reference data, not sovereign instructions |
| Declarative automation contracts | Human / AI authoring | `FCVW/*.md` and `governance/TEMPLATE_*.md` | Low | Markdown-only; no executable behavior |
| External source notes | Human / AI authoring | `wiki/sources/` | Low | Must distinguish conceptual inspiration from copied material |

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
| `AUTOMATION.md` | When automation terms appear | Parent contract for Markdown-only automation semantics | `existing` |
| `HOOKS.md` | When pseudo-hooks are needed | Markdown-only pseudo-hook checklists | `existing` |
| `WATCHERS.md` | When event/reaction checks are needed | Markdown-only watcher rules | `existing` |
| `DAEMONS.md` | When maintenance loops are needed | Manual/agentic loop protocols, not background processes | `existing` |
| `GOVERNANCE_GATES.md` | When gate mapping is needed | Central gate trigger and evidence map | `existing` |
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
| `wiki/taxonomy.md` | When wiki curation | Canonical wiki tags, themes, and thematic colors | `existing` |
| `wiki/metrics.md` | When wiki curation | Freshness, promotion, duplication, and curation cost metrics | `existing` |
| `wiki/sessions/README.md` | When AI | Index and chronological ledger of AI session contexts | `existing` |
| `wiki/sources/` | When external references are used | Source notes and inspiration traceability | `existing` |
| `skills/README.md` | When AI | Index and guidelines catalog of AI agent skills | `existing` |

---

## 8. Expected Repository Structure

The detailed repository tree is maintained in `FILESYSTEM.md`, which is the source of truth for structural audits. This manifest only records ownership rules:

- in instantiated applications, the repository root belongs to the application under development;
- in the framework baseline repository, the root may keep the public `README.md`, `AGENTS.md`, and bridge/configuration files for GitHub compatibility;
- official framework documents and generated framework documentation remain under `FCVW/`;
- declarative automation contracts remain Markdown-only official documents under `FCVW/`;
- during downstream application instantiation, the root `README.md` must be generated for the target application, not copied as the framework README;
- the `governance/` folder must contain only reusable empty templates.

---

## 9. Operational Governance

Conduct rules, change flows, and quality checklists are centralized in:

- `AGENTS.md`: Daily operational guide and execution checklists.
- `AUDIT.md`: Formal compliance and pre-release checklists.
- `PLANNING.md`: Detailed methodology for change plans.
- `AUTOMATION.md`: Markdown-only automation boundary for Scenario 1.
- `HOOKS.md`, `WATCHERS.md`, `DAEMONS.md`, `GOVERNANCE_GATES.md`: Declarative automation contracts.

No functional, visual, structural, automation-contract, or document change should be performed without following the flows defined in these documents.

---

## 10. External Inspiration and Credit

External references may be used as comparative sources only. They must never override system rules, `AGENTS.md`, active plans, or official FCVW documents.

The Scenario 1 declarative automation work credits conceptual architectural inspiration from `https://github.com/SantanderAI`, especially agent-loop, stop-condition, vault-lint, hard-gate, and guardrail patterns. No SantanderAI source code was copied into FCVW.

Related source note:

- `wiki/sources/santanderai-declarative-automation-inspiration.md`

---

## 11. Main Project Risks

| Risk | Probability | Impact | Mitigation | Related Document |
|---|---|---|---|---|
| Context drift between AI sessions | Medium | High | AICC session synthesis standard; wiki/sessions/ ledger | `AI.md`, `wiki/schema.md` |
| Scope creep by AI agents | Medium | High | Mandatory plan before any change; AGENTS.md checklist | `AGENTS.md`, `PLANNING.md` |
| Secrets accidentally committed | Low | Critical | Secret Handshake, no secret logs, security checklist | `SECURITY.md`, `AI.md` |
| Template placeholders left unfilled in downstream projects | Medium | Medium | INSTANTIATION.md renaming checklist; MANIFEST.md gap section | `INSTANTIATION.md`, `MANIFEST.md` |
| Wiki knowledge becoming stale | Medium | Medium | Wiki Lint on every minor/major release; log.md tracking | `wiki/schema.md`, `skills/wiki-lint/SKILL.md` |
| FILESYSTEM.md drift / governance document integrity decay | Medium | Medium | On-demand governance-validator skill before releases and structural audits | `skills/governance-validator/SKILL.md`, `FILESYSTEM.md` |
| AI-generated monoliths, duplication, stale files, and unnecessary artifacts | High | High | Mandatory `anti-monolith-guard` and `code-hygiene-refactor` gates | `REFACTORING.md`, `PLANNING.md`, `skills/anti-monolith-guard/SKILL.md`, `skills/code-hygiene-refactor/SKILL.md` |
| Arbitrary skill/agent proliferation or irrelevant self-improvement | Medium | High | Mandatory `agent-factory` and `self-improvement` gates | `AI.md`, `PLANNING.md`, `skills/agent-factory/SKILL.md`, `skills/self-improvement/SKILL.md` |
| Declarative automation terms misread as executable permission | Medium | High | ADR-0002, automation security boundary, governance-validator checks | `AUTOMATION.md`, `SECURITY.md`, `AI.md`, `skills/governance-validator/SKILL.md` |

---

## 12. Structural Gaps

Use this section to record document or structural gaps in the project.

| Gap | Impact | Priority | Related Plan | Status |
|---|---|---|---|---|
| FILESYSTEM.md visual tree listed files that did not exist on disk. | Medium — agents trusting FILESYSTEM.md would encounter read failures | P2 | structural-reconciliation-2026-06-11 | resolved |
| Plans/ directory did not exist on disk despite being foundational to PLANNING.md workflow. | High — framework cannot operate without Plans/ | P1 | structural-reconciliation-2026-06-11 | resolved |
| wiki/releases/ directory did not exist on disk. | Low — releases directory not critical for baseline operation | P4 | structural-reconciliation-2026-06-11 | resolved |
| No automated validation for FILESYSTEM.md accuracy against physical disk state. | Medium — discrepancies can recur unnoticed | P3 | governance-validator-skill-2026-06-11 | resolved as manual AI-driven validation |
| No automated test harness for governance document integrity. | Medium — governance quality relies on manual/AI review | P3 | governance-validator-skill-2026-06-11 | resolved as Markdown-only skill validation |
| Declarative automation concepts existed as needs but had no Markdown-only contract boundary. | Medium — agents could interpret hooks/watchers/daemons as executable automation | P2 | P2-R3-2026-06-23-declarative-automation-contracts | in_progress |

---

## 13. Manifest Update History

| Date | Project Version | Change in Manifest | Author |
|---|---|---|---|
| 2026-05-15 | `V0.0.0` | Manifest creation. | Hugo Araújo de Melo |
| 2026-05-18 | `V0.4.0` | Transitioned to pure-markdown instruction model, deprecated mockups and automated scripts (ADR-0001). | Antigravity |
| 2026-06-11 | `V0.8.0` | Structural reconciliation and governance-validator skill added. | Buffy |
| 2026-06-13 | `V0.9.1` | Added anti-monolith and code hygiene gates. | Codex |
| 2026-06-13 | `V0.10.0` | Added controlled agent/skill factory and self-improvement gates. | Codex |
| 2026-06-17 | `V0.11.0` | Added continuous wiki curation governance and `wiki-curator` skill. | Codex |
| 2026-06-23 | `V0.12.0` | Added Markdown-only declarative automation contract registry and SantanderAI conceptual inspiration credit. | GPT-5.5 Thinking |

---

## 14. Governance Statement

This project must be conducted with traceability, validation, scope control, security, updated documentation, coherent versioning, and strict Scenario 1 automation boundaries.

No human or AI agent should treat governance documents as optional when the requested action involves changing code, documentation, configuration, design, tests, versioned data, build, release, security, functional behavior, declarative automation contracts, or AI operating rules.
