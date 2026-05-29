# Skills Engine Catalog & Guidelines

*Selecione o Idioma / Select Language:*
- [PortuguÃªs](#portuguÃªs)
- [English](#english)

---

## PortuguÃªs

A pasta `/skills/` atua como o **Motor de Habilidades (Skills Engine)** do framework. Ela armazena manuais de procedimentos tÃ©cnicos de alta densidade e checklists operacionais especializados para direcionar a execuÃ§Ã£o do agente de IA de forma eficiente e padronizada.

### Diretrizes de Uso

1. **AtivaÃ§Ã£o por Demanda (Token-Efficient)**: As skills **nunca** devem ser carregadas no prompt inicial da IA. O agente deve ler um arquivo de skill (com `view_file` e `IsSkillFile: true`) apenas quando a tarefa ativamente exigir a execuÃ§Ã£o daquele procedimento.
2. **Gatilhos Claros**: Cada skill deve declarar explicitamente seus gatilhos operacionais de ativaÃ§Ã£o.
3. **Estilo de Alta Densidade**: As skills devem usar checklists e comandos diretos, eliminando narrativa filler e conversas prolixas.
4. **Registro de Uso**: Quando uma skill Ã© ativada, ela deve ser listada na SÃ­ntese de SessÃ£o AICC correspondente em `wiki/sessions/S*.md`.

### CatÃ¡logo de Skills Ativas

| Skill | Arquivo | Gatilhos Principais | BenefÃ­cio |
|---|---|---|---|
| **obsidian-markdown** | [`skills/obsidian-markdown/SKILL.md`](obsidian-markdown/SKILL.md) | formataÃ§Ã£o wiki, wikilinks, frontmatter, notas Obsidian | Padroniza formataÃ§Ã£o e conexÃµes semÃ¢nticas da LLM Wiki |
| **git-conventional-commits** | [`skills/git-conventional-commits/SKILL.md`](git-conventional-commits/SKILL.md) | commit, tag, push, release notes, publicar versÃ£o | Padroniza mensagens de commit, tags semÃ¢nticas e notas de release |
| **wiki-lint** | [`skills/wiki-lint/SKILL.md`](wiki-lint/SKILL.md) | lint wiki, auditoria wiki, orphan pages, frontmatter invÃ¡lido | Valida integridade estrutural da wiki (substitui leitura de 335 linhas do schema.md Â§12) |
| **release-checklist** | [`skills/release-checklist/SKILL.md`](release-checklist/SKILL.md) | release, publish, version bump, publicar release | Checklist condensado de release (~2.700 tokens economizados vs. carregar RELEASE+VERSIONING+AUDIT) |
| **aicc-compact** | [`skills/aicc-compact/SKILL.md`](aicc-compact/SKILL.md) | shift close, compact session, concluir turno, finalizar sessão | Automatiza e compacta a síntese de sessão AICC para evitar inchaço de tokens |
| **project-instantiation** | [`skills/project-instantiation/SKILL.md`](project-instantiation/SKILL.md) | bootstrap, instantiate, inicializar projeto, novo projeto | Guia a IA no bootstrap e renomeação de novos projetos na Fase 0 |
| **agent-hermes** | [`skills/agent-hermes/SKILL.md`](agent-hermes/SKILL.md) | run perf agent, improve performance, optimize | Agente autônomo agendado para procurar e aplicar otimizações de performance. |
| **agent-hephaestus** | [`skills/agent-hephaestus/SKILL.md`](agent-hephaestus/SKILL.md) | ux polish, accessibility fix, improve ui | Agente autônomo agendado para encontrar e implementar melhorias de micro-UX e acessibilidade. |
| **agent-aegis** | [`skills/agent-aegis/SKILL.md`](agent-aegis/SKILL.md) | security scan, fix vulnerability, harden | Agente autônomo agendado para identificar e corrigir vulnerabilidades ou aplicar hardening. |
| **brainstorming-and-tdd** | [`skills/brainstorming-and-tdd/SKILL.md`](brainstorming-and-tdd/SKILL.md) | starting a new feature, fixing a bug, implementing a plan | Trava o agente no início para extrair especificações e obriga o uso de TDD (Red/Green). |
| **systematic-debugging** | [`skills/systematic-debugging/SKILL.md`](systematic-debugging/SKILL.md) | debugging, fixing an error, tracking down a bug, stack trace | Força a depuração estruturada baseada em hipóteses, eliminando a tentativa e erro. |
| **orchestrator** | [`skills/orchestrator/SKILL.md`](orchestrator/SKILL.md) | large refactoring, complex plans, parallel tasks | Habilita a IA a delegar tarefas em paralelo usando subagentes. |
| **agnix-linter** | [`skills/agnix-linter/SKILL.md`](agnix-linter/SKILL.md) | periodic maintenance, governance audit | Inspeciona e valida a formatação, dead-links e consistência da pasta `FCVW/`. |
| **memory-rotation** | [`skills/memory-rotation/SKILL.md`](memory-rotation/SKILL.md) | context bloat, clean sessions, rotate memory | Condensa sessões antigas do wiki em conceitos e remove excessos para proteger a janela de tokens. |

---

## English

The `/skills/` directory serves as the framework's **Skills Engine**. It houses high-density technical procedure manuals and specialized operational checklists to guide the AI agent's execution in an efficient and standardized manner.

### Usage Guidelines

1. **Demand-Driven Activation (Token-Efficient)**: Skills must **never** be loaded in the initial AI prompt. The agent must read a skill file (using `view_file` with `IsSkillFile: true`) only when the active task explicitly demands executing that procedure.
2. **Clear Triggers**: Each skill must explicitly state its operational activation triggers.
3. **High-Density Style**: Skills must utilize direct checklists and commands, eliminating filler narrative and verbose talk.
4. **Usage Registry**: When a skill is activated, it must be recorded in the corresponding AICC Session Synthesis inside `wiki/sessions/S*.md`.

### Active Skills Catalog

| Skill | File | Primary Triggers | Benefit |
|---|---|---|---|
| **obsidian-markdown** | [`skills/obsidian-markdown/SKILL.md`](obsidian-markdown/SKILL.md) | wiki formatting, wikilinks, frontmatter, Obsidian notes | Standardizes LLM Wiki formatting and semantic connections |
| **git-conventional-commits** | [`skills/git-conventional-commits/SKILL.md`](git-conventional-commits/SKILL.md) | commit, tag, push, release notes, publish version | Standardizes commit messages, semantic tags, and release notes |
| **wiki-lint** | [`skills/wiki-lint/SKILL.md`](wiki-lint/SKILL.md) | lint wiki, wiki audit, orphan pages, broken links, invalid frontmatter | Validates wiki structural integrity (replaces reading 335 lines of schema.md Â§12) |
| **release-checklist** | [`skills/release-checklist/SKILL.md`](release-checklist/SKILL.md) | release, publish, version bump, cut a release | Condensed release checklist (~2,700 tokens saved vs. loading RELEASE+VERSIONING+AUDIT) |
| **aicc-compact** | [`skills/aicc-compact/SKILL.md`](aicc-compact/SKILL.md) | shift close, compact session, close session, consolidate shift | Standardizes AICC context compression at session end to prevent token bleed |
| **project-instantiation** | [`skills/project-instantiation/SKILL.md`](project-instantiation/SKILL.md) | bootstrap, new project, instantiate, initialize, briefing | Steers the JIT bootstrap workflow for new downstream projects securely |
| **agent-hermes** | [`skills/agent-hermes/SKILL.md`](agent-hermes/SKILL.md) | run perf agent, improve performance, optimize | Autonomous scheduled agent to find and apply performance optimizations. |
| **agent-hephaestus** | [`skills/agent-hephaestus/SKILL.md`](agent-hephaestus/SKILL.md) | ux polish, accessibility fix, improve ui | Autonomous scheduled agent to find and implement micro-UX and accessibility improvements. |
| **agent-aegis** | [`skills/agent-aegis/SKILL.md`](agent-aegis/SKILL.md) | security scan, fix vulnerability, harden | Autonomous scheduled agent to identify and fix vulnerabilities or apply security hardening. |
| **brainstorming-and-tdd** | [`skills/brainstorming-and-tdd/SKILL.md`](brainstorming-and-tdd/SKILL.md) | starting a new feature, fixing a bug, implementing a plan | Halts the agent at the start to extract specs and enforces Red/Green TDD. |
| **systematic-debugging** | [`skills/systematic-debugging/SKILL.md`](systematic-debugging/SKILL.md) | debugging, fixing an error, tracking down a bug, stack trace | Enforces structured hypothesis-based debugging, eliminating guess and check. |
| **orchestrator** | [`skills/orchestrator/SKILL.md`](orchestrator/SKILL.md) | large refactoring, complex plans, parallel tasks | Enables the main AI to delegate tasks in parallel using subagents. |
| **agnix-linter** | [`skills/agnix-linter/SKILL.md`](agnix-linter/SKILL.md) | periodic maintenance, governance audit | Inspects and validates FCVW folder formatting, dead-links, and consistency. |
| **memory-rotation** | [`skills/memory-rotation/SKILL.md`](memory-rotation/SKILL.md) | context bloat, clean sessions, rotate memory | Condenses old wiki sessions into concepts and purges excess to protect the token window. |


