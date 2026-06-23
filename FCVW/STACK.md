# Tech Stack

## Application

- Name: `FrameCode VibeWork`
- Current version: `V0.11.0`
- Type: `framework / governance template`
- Target platform: `cross-platform (Windows / Linux / macOS)`
- Objective: `Document-based governance framework for AI-assisted application development with session context compression and on-demand skills engine.`

## Governance Layer

The primary "stack" of this framework is pure Markdown and Git. No runtime dependencies.

- Document format: `Markdown (.md)`
- Version control: `Git`
- Visualization (optional): `Obsidian` — graph view for wiki wikilinks
- Distribution: `GitHub template / git clone`
- ADR-0001: Pure Markdown Instruction Model — no automation scripts in the framework
- ADR-0002: Declarative Automation Contracts — hooks, watchers, daemons, and gates are Markdown-only contracts in Scenario 1

## Declarative Automation Contracts

The framework may describe hooks, watchers, daemons, maintenance loops, and governance gates as Markdown-only operational contracts.

These contracts do not introduce:

- executable scripts;
- installed Git hooks;
- background processes;
- package dependencies;
- CI/CD workflows;
- API-key integrations;
- provider SDKs;
- local command-execution loops.

They are executed manually or by AI agents following `AGENTS.md`, `AUTOMATION.md`, and the applicable governance skills.

This layer credits conceptual architectural inspiration from public SantanderAI repositories at `https://github.com/SantanderAI`, without copying source code.

## AI / LLM Integration

- Runtime / model server: `Model-agnostic — any LLM agent that can read and follow Markdown`
- Tested with: `Gemini Flash/Pro, Claude Sonnet/Haiku, GPT-4 class models`
- AI roles: `Plan author, implementer, wiki curator, session synthesizer, skill executor`
- Context compression: `AICC — AI Interaction Context Compression (wiki/sessions/S*.md)`
- Skills engine: `ASE — AI Skills Engine (skills/*.md, loaded JIT)`
- Continuous learning: `LLM Wiki Ingest/Query/Curate/Lint cycle (wiki/schema.md, skills/wiki-curator/SKILL.md)`
- Agent journals: `wiki/agents/<agent_name>_journal.md`

## Knowledge Base / Wiki

- Local directory: `wiki/`
- Format: `Markdown`
- Main structure: `schema.md, index.md, log.md, sessions/, patterns/, decisions/, failures/, releases/, templates/`
- Obsidian graph: `wikilinks [[page]] across all wiki/ and decisions/ files`

## Active Skills (ASE Catalog)

| Skill | Path | Trigger |
|---|---|---|
| `agent-aegis` | `skills/agent-aegis/SKILL.md` | security scan, vulnerability, harden, segurança, vazamento de dados |
| `agent-factory` | `skills/agent-factory/SKILL.md` | create skill, create agent, specialized agent |
| `agent-hephaestus` | `skills/agent-hephaestus/SKILL.md` | ux polish, accessibility, improve ui, interface, acessibilidade |
| `agent-hermes` | `skills/agent-hermes/SKILL.md` | performance, optimize, bottleneck, desempenho, lentidão |
| `agnix-linter` | `skills/agnix-linter/SKILL.md` | periodic maintenance, governance audit |
| `aicc-compact` | `skills/aicc-compact/SKILL.md` | shift close, compact session, close session |
| `anti-monolith-guard` | `skills/anti-monolith-guard/SKILL.md` | monolith, large file, new module, module boundary |
| `brainstorming-and-tdd` | `skills/brainstorming-and-tdd/SKILL.md` | starting a new feature, fixing a bug, implementing a plan |
| `code-hygiene-refactor` | `skills/code-hygiene-refactor/SKILL.md` | code hygiene, duplication, cleanup, dead code, higiene de código |
| `obsidian-markdown` | `skills/obsidian-markdown/SKILL.md` | wiki formatting, wikilinks, Obsidian notes |
| `git-conventional-commits` | `skills/git-conventional-commits/SKILL.md` | commit, tag, push, release notes |
| `governance-validator` | `skills/governance-validator/SKILL.md` | validate governance, verify filesystem, document integrity, plan state coherence |
| `memory-rotation` | `skills/memory-rotation/SKILL.md` | context bloat, clean sessions, rotate memory |
| `orchestrator` | `skills/orchestrator/SKILL.md` | large refactoring, complex plans, parallel tasks |
| `project-instantiation` | `skills/project-instantiation/SKILL.md` | bootstrap, new project, instantiate, initialize |
| `retroactive-instantiation` | `skills/retroactive-instantiation/SKILL.md` | retroactive instantiation, existing app, legacy app |
| `self-improvement` | `skills/self-improvement/SKILL.md` | improve skill, improve agent, skill failed, gatilho falhou |
| `wiki-curator` | `skills/wiki-curator/SKILL.md` | curate wiki, continuous learning, agrupar notas, frontmatter colors |
| `wiki-lint` | `skills/wiki-lint/SKILL.md` | lint, wiki audit, orphan pages |
| `release-checklist` | `skills/release-checklist/SKILL.md` | release, publish, version bump, changelog, publicar versão |
| `systematic-debugging` | `skills/systematic-debugging/SKILL.md` | debugging, fixing an error, tracking down a bug |

## Build and Execution

- Build script: `Not applicable — no compiled artifacts`
- Execution script: `Not applicable — open in Markdown editor or agent IDE`
- Main output: `Populated governance documents, wiki pages, and session syntheses`
- Public documentation site: `External to this framework baseline`
- Node package files: `Not applicable in the framework root`
- Application module docs: `Downstream application-owned docs/ generated from FCVW governance templates`
- Declarative automation: `Markdown-only contracts in AUTOMATION.md, HOOKS.md, WATCHERS.md, DAEMONS.md, and GOVERNANCE_GATES.md`

## Persistence and Logs

- Plans: `Plans/{pending,in_progress,completed,discontinued}/`
- Changelogs: `changelogs/unreleased/{plan-name}.md` fragments and formal `changelogs/Vx.y.z.md` releases
- Technical memory: `wiki/` (LLM Wiki format)
- Session context: `wiki/sessions/S{num}-{date}-{description}.md`
- Troubleshooting: `troubleshooting/YYYY-MM-DD-description.md`
- ADRs: `decisions/ADR-{num}-description.md`
- Writing strategy: `Append-first (wiki/log.md, changelogs); overwrite with version bump (MANIFEST.md)`
- Data ignored by Git: `*.env, local build artifacts, private paths (see .gitignore)`

## Document Governance

- Completed official documents: Markdown files at the root of the application.
- Reusable empty templates: `governance/` folder.
- Technical memory of governance: `wiki/` folder.
- Formal records: `Plans/`, `changelogs/`, `troubleshooting/`.
- Declarative automation records: `AUTOMATION.md`, `HOOKS.md`, `WATCHERS.md`, `DAEMONS.md`, and `GOVERNANCE_GATES.md`.
- Instantiation and renaming: `INSTANTIATION.md`.
- Versioning exclusions: `.gitignore`.
- Mandatory changelog: every change in a versioned file must be registered in `changelogs/Vx.y.z.md`.
