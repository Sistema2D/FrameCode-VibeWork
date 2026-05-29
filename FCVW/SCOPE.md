# SCOPE.md

General scope of the FrameCode VibeWork framework according to its current state.

This document describes the purpose, boundaries, modules, and main components of the framework. It does not replace `FCVW/README.md`, `STACK.md`, `DESIGN.md`, or `PLANNING.md`; its role is to consolidate the functional scope view to guide future analysis, planning, and evolution.

## Overview

FrameCode VibeWork (FCVW) is a stack-agnostic, document-based governance framework for AI-assisted application development. It runs entirely in Markdown and Git, requiring no runtime dependencies or automation scripts. It is designed to be forked, cloned, or used as a template for any new software project that uses AI agents as primary implementers.

## General Objective

Provide a structured, traceable, and token-efficient lifecycle for AI-assisted development — from initial briefing through planning, implementation, validation, release, and incremental knowledge accumulation.

## Specific Objectives

- Eliminate context loss between AI sessions through compressed session syntheses (AICC)
- Enforce traceability of every change through a mandatory Plans → Changelog workflow
- Accumulate reusable technical memory in a structured LLM Wiki (Obsidian-compatible)
- Reduce AI governance token overhead by 70–80% via selective document loading and JIT skills
- Provide a clear instantiation path for bootstrapping new projects from the framework

## Limits of Current Scope

- FCVW does not include application source code — it is stack-agnostic infrastructure
- Automation scripts are out of scope (deprecated by ADR-0001; pure markdown model adopted)
- Cloud deployment, CI/CD pipelines, and hosting infrastructure are not part of the framework
- AI model fine-tuning, RAG embedding pipelines, and vector databases are out of scope

## High-Level Architecture

### Governance Layer

The core of the framework. `AGENTS.md` remains at the repository root as the agent entrypoint; official framework documents reside inside `FCVW/` and define the rules, methodology, and boundaries for any change. Plans in `Plans/{status}` govern the lifecycle of every modification. Changelogs in `changelogs/` track formal version history.

### AI Skills Engine (ASE)

The `skills/` directory hosts SKILL.md files — high-density procedural checklists loaded JIT by AI agents via `view_file` with `IsSkillFile: true`. Skills are never pre-loaded; they are activated only when the active task explicitly triggers their condition. This keeps the base token window lean.

The authoritative skill catalog is `FCVW/skills/README.md`. `FCVW/STACK.md` records the current active inventory for quick technical reference.

### LLM Wiki (Technical Memory)

The `wiki/` directory implements the LLM Wiki standard (inspired by Andrej Karpathy's concept). It contains: raw sources, synthesized knowledge pages, an index, a chronological log, AICC session syntheses, and thematic subfolders (patterns, decisions, failures, releases, etc.).

**Key operational cycle:** Ingest → Query → Lint (defined in `wiki/schema.md`)

### AI Interaction Context Compression (AICC)

Session syntheses stored in `wiki/sessions/S{num}-{date}-{description}.md` compress each working session into a dense, telegraphic handoff document. At the start of each new session, the agent reads the latest synthesis to restore context without rereading all history.

**Estimated token savings:** ~77% reduction vs. raw chat history ingestion.

### Design System

`DESIGN.md` is the source of truth for visual rules, tokens, component contracts, and interaction standards. Framework-level snippet/sample storage is discontinued; downstream applications generate physical UI assets from `DESIGN.md` when needed.

### Governance Templates

The `governance/` directory preserves generic, empty templates for all operational processes: plans, ADRs, session syntheses, briefings, data schemas, refactoring records, and release notes. These templates are never filled with project-specific data — they serve as canonical blanks for instantiation.

## Modules and Components

### Root Documents (Governance Layer)

Objective: Define rules, methodology, and identity for the project using this framework.

Content and features:
- `AGENTS.md` — master operational guide and index; loaded first in every session
- `MANIFEST.md` — identity, state, scope, stack, risks, gaps, and governance statement
- `CONTEXT_MAP.md` — session-type selective loading table (token optimization)
- `PLANNING.md` — mandatory plan methodology (P/R scale, naming, lifecycle)
- `AI.md` — AICC and ASE operational standards, token efficiency rules
- `DESIGN.md` — visual rules for projects with UI (HSL palette, glassmorphism, VDA)
- `VERSIONING.md`, `RELEASE.md`, `AUDIT.md` — release and version lifecycle

### Plans Workflow

Objective: Govern every change with a formal, traceable plan.

Content and features:
- `Plans/pending/` — approved plans not yet started
- `Plans/in_progress/` — plans actively being executed
- `Plans/completed/` — validated and closed plans
- `Plans/discontinued/` — canceled plans with justification
- Naming convention: `P{priority}-R{risk}-{date}-{description}.md`

### LLM Wiki

Objective: Accumulate and maintain reusable technical knowledge across sessions.

Content and features:
- `wiki/schema.md` — structural and operational rules (Ingest/Query/Lint cycle)
- `wiki/index.md` — navigable map of all knowledge pages
- `wiki/log.md` — chronological event log
- `wiki/sessions/` — AICC session syntheses
- Thematic subfolders: `patterns/`, `decisions/`, `failures/`, `releases/`, `components/`, `prompts/`, `questions/`, `syntheses/`

### Cross-Cutting Components

### Navigation

Users navigate between documents via Markdown hyperlinks and Obsidian-style wikilinks. The `CONTEXT_MAP.md` provides a quick reference for which documents to load in each session type.

### Local Persistence

All state is persisted as Markdown files in Git. No database or binary format is used. Session state is compressed into `wiki/sessions/S{num}.md` files.

### Local Security

No secrets, API keys, or personal data should be stored in the repository. See `SECURITY.md`. The `AI.md` data rules require anonymization of any sensitive path or environment data before committing to `troubleshooting/` or `wiki/`.

### Build and Execution

No build step required. Clone the repository, open in a Markdown editor (Obsidian recommended for graph view), and begin using the framework with an AI agent following `AGENTS.md`.

### Document Governance

The framework maintains a versioned document layer to guide planning, implementation, validation, release, and continuous learning.

Main components:
- official framework documents in `FCVW/`, with `AGENTS.md` at the repository root as the bridge entrypoint;
- plans in `Plans/{status}`;
- changelogs in `changelogs/`;
- issue records in `troubleshooting/`;
- governance wiki in `wiki/`;
- reusable empty templates in `governance/`.

## Related Documents

- `FCVW/README.md`: overview, requirements, build, execution, and troubleshooting for the framework.
- `STACK.md`: technical stack and architecture.
- `DESIGN.md`: visual and experience rules.
- `PLANNING.md`: mandatory methodology for changes.
- `AGENTS.md`: operational guide for humans and agents.
- `TROUBLESHOOTING.md`: failure registration and handling process.
- `VERSIONING.md`: version, release, and changelog rules.
- `MANIFEST.md`: identity and governance synthesis of the project.
- `CONTEXT_MAP.md`: selective loading map by session type.
