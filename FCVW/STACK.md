# Tech Stack

## Application

- Name: `FrameCode VibeWork`
- Current version: `V0.12.0`
- Type: `framework / governance template`
- Target platform: `cross-platform (Windows / Linux / macOS)`
- Objective: `Markdown-first governance framework for AI-assisted application development with context compression, on-demand skills, declarative automation contracts, and token-budget guidance.`

## Governance Layer

The primary stack of this framework is pure Markdown and Git. No runtime dependencies.

- Document format: `Markdown (.md)`
- Version control: `Git`
- Visualization: `Obsidian` optional
- Distribution: `GitHub template / git clone`
- ADR-0001: Pure Markdown instruction model
- ADR-0002: Declarative automation contracts over executable automation

## Token Economy Layer

- Input economy: `CONTEXT_MAP.md`, AICC session syntheses, and JIT skills.
- Output economy: `TOKEN_BUDGET.md`, with detailed evidence stored in plans, changelogs, audits, troubleshooting, release notes, and PR descriptions.

## Declarative Automation Contracts

The framework may describe hooks, watchers, daemons, maintenance loops, and governance gates as Markdown-only operational contracts.

These contracts do not introduce executable scripts, installed hooks, background processes, package dependencies, CI/CD workflows, API-key integrations, provider SDKs, or local command-execution loops.

## AI / LLM Integration

- Runtime/model server: `Model-agnostic — any LLM agent that can read and follow Markdown`
- Context compression: `AICC`
- Skills engine: `ASE — AI Skills Engine`
- Wiki memory: `LLM Wiki`

## Active Skills

Skills live under `skills/<name>/SKILL.md` and are loaded on demand. See `skills/README.md` for the current catalog.

## Build and Execution

- Build script: `Not applicable`
- Execution script: `Not applicable`
- Node package files: `Not applicable in the framework root`
- Main output: versioned governance documents, plans, changelogs, wiki pages, and session syntheses

## Persistence and Logs

- Plans: `Plans/{pending,in_progress,completed,discontinued}/`
- Changelogs: `changelogs/unreleased/` and formal `changelogs/Vx.y.z.md`
- Technical memory: `wiki/`
- Session context: `wiki/sessions/S*.md`
- Troubleshooting: `troubleshooting/`
- ADRs: `decisions/`
