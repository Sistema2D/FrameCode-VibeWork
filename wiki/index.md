# LLM Wiki Index

This file is the navigable index of the project's wiki.

It must be updated whenever new pages are created, obsoleted, replaced, or validated.

---

## Core Pages

- [[schema]] â€” Structural and operational rules of the wiki.
- [[log]] â€” Chronological log of wiki events.
- [[sessions/README]] â€” Index and chronological ledger of AI Session Syntheses.
- [[README]] â€” Overview of the `wiki/` folder.

## Preferred Formal Sources

- `AGENTS.md`
- `CONTEXT_MAP.md`
- `INSTANTIATION.md`
- `MANIFEST.md`
- `FILESYSTEM.md`
- `PLANNING.md`
- `VERSIONING.md`
- `TROUBLESHOOTING.md`
- `Plans/completed/`
- `changelogs/`
- `troubleshooting/`
- `decisions/`
- `audits/`

---

## Validated Technical Patterns

- [[patterns/aicc-session-compression|AICC Session Compression Pattern]] â€” `#gold-pattern` Â· Validated context compression achieving ~77% token reduction across all session types.
- [[patterns/ase-jit-skill-loading|ASE JIT Skill Loading Pattern]] â€” `#gold-pattern` Â· On-demand skill loading strategy to reduce prompt bloat and preserve active context window.

---

## Known Failures and Learnings

> Record here recurring failures, root causes, and validated solutions.

- No consolidated failures so far.

---

## Consolidated Decisions

- [[decisions/adr-0001-pure-markdown|ADR-0001: Pure Markdown Over Automation Scripts]] â€” `#arch-decision` Â· Architectural pivot adopted in V0.4.0; mandates pure Markdown instruction model for all framework tooling.

---

## Components and Modules

> Record here pages about modules, screens, services, components, or project layers.

- No components recorded so far.

---

- No consolidated refactoring pages recorded so far.

---

## Audits

> Record here pages about formal audits executed in the project.

- No consolidated audits so far.

---

## Releases

- [[releases/v0-5-0|V0.5.0 â€” ASE Expansion and Context Optimization]] â€” Expanded ASE to 4 skills, added CONTEXT_MAP, promoted wiki knowledge, and finalized portability/consistency fixes.
- [[releases/v0-4-0|V0.4.0 â€” Pure Markdown Instruction Model]] â€” Strategic architectural pivot; removed scripts and mockups; expanded DESIGN.md and FILESYSTEM.md.

---

## Useful Prompts

> Record here reusable and validated prompts.

- No prompts recorded so far.

---

## Open Questions

> Record here important questions that may guide future decisions.

- No open questions recorded so far.

---

## Cross-Cutting Syntheses

> Record here syntheses that connect multiple sources, decisions, failures, or patterns.

- [[syntheses/S005-framework-optimization-analysis|Framework Optimization & Architectural Analysis]] â€” In-depth architectural audit proposing 5 major pillars of automation and safety improvements.
- [[sessions/S009-2026-05-22-github-pages-bilingual-application-page|Session S009 - GitHub Pages Bilingual Application Guide]] â€” Documentation-focused synthesis for the bilingual public page.
- [[sessions/S010-2026-05-22-local-model-guidelines-pages-wiki-and-readme-flow-update|Session S010 - Local Model Guidelines + Pages/Wiki/README Alignment]] â€” Added local-model sizing guidance and synchronized lifecycle/public documentation flow.
- [[sessions/S011-2026-05-22-pages-header-language-expansion-and-outline-renumbering|Session S011 - Pages Header UX + 4-Language Expansion]] â€” Reworked header controls, hierarchical numbering, and multilingual coverage (PT-BR, EN, ES, DE).
- [[sessions/S012-2026-05-22-pages-accordion-quickstart-flowchart-and-es-de-parity|Session S012 - Pages Accordion Navigation + AGENTS-First Quick Start]] â€” Simplified public instructions, added single-open nav accordions, and upgraded ES/DE sections to full topic parity.
- [[sessions/S013-2026-05-22-pages-apple-design-system-adoption|Session S013 - Apple DESIGN.md Adoption for Pages]] â€” Replaced GitHub Pages visual system with Apple tokens/components from `VoltAgent/awesome-design-md`.

---

## Obsolete or Replaced Pages

> Record here pages that should no longer be used as a primary source.

- No obsolete pages recorded so far.
