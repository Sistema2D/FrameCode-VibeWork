# Skills Engine Catalog & Guidelines

*Selecione o Idioma / Select Language:*
- [Português](#português)
- [English](#english)

---

## Português

A pasta `/skills/` atua como o **Motor de Habilidades (Skills Engine)** do framework. Ela armazena manuais de procedimentos técnicos de alta densidade e checklists operacionais especializados para direcionar a execução do agente de IA de forma eficiente e padronizada.

### Diretrizes de Uso

1. **Ativação por Demanda (Token-Efficient)**: As skills **nunca** devem ser carregadas no prompt inicial da IA. O agente deve ler um arquivo de skill (com `view_file` e `IsSkillFile: true`) apenas quando a tarefa ativamente exigir a execução daquele procedimento.
2. **Gatilhos Claros**: Cada skill deve declarar explicitamente seus gatilhos operacionais de ativação, incluindo equivalentes PT-BR quando o uso esperado for bilíngue.
3. **Estilo de Alta Densidade**: As skills devem usar checklists e comandos diretos, eliminando narrativa filler e conversas prolixas.
4. **Registro de Uso**: Quando uma skill é ativada, ela deve ser listada na Síntese de Sessão AICC correspondente em `wiki/sessions/S*.md`.
5. **Crescimento Controlado**: novas skills e perfis de agente exigem `agent-factory`, métricas de recorrência/cobertura/ROI e validação. Ajustes em skills ou agentes exigem `self-improvement` e evidência de falha, drift ou economia relevante.

### Catálogo de Skills Ativas

| Skill | Arquivo | Gatilhos Principais | Benefício |
|---|---|---|---|
| **obsidian-markdown** | [`skills/obsidian-markdown/SKILL.md`](obsidian-markdown/SKILL.md) | formatação wiki, wikilinks, frontmatter, notas Obsidian | Padroniza formatação e conexões semânticas da LLM Wiki |
| **git-conventional-commits** | [`skills/git-conventional-commits/SKILL.md`](git-conventional-commits/SKILL.md) | commit, tag, push, release notes, publicar versão | Padroniza mensagens de commit, tags semânticas e notas de release |
| **wiki-lint** | [`skills/wiki-lint/SKILL.md`](wiki-lint/SKILL.md) | lint wiki, auditoria wiki, orphan pages, frontmatter inválido | Valida integridade estrutural da wiki |
| **release-checklist** | [`skills/release-checklist/SKILL.md`](release-checklist/SKILL.md) | release, publish, version bump, changelog, publicar versão, bump de versão, notas de versão | Checklist condensado de release |
| **aicc-compact** | [`skills/aicc-compact/SKILL.md`](aicc-compact/SKILL.md) | shift close, compact session, concluir turno, finalizar sessão | Automatiza e compacta a síntese de sessão AICC para evitar inchaço de tokens |
| **anti-monolith-guard** | [`skills/anti-monolith-guard/SKILL.md`](anti-monolith-guard/SKILL.md) | monolith, monolito, large file, new module, module boundary | Bloqueia arquivos e módulos com responsabilidades misturadas antes da edição |
| **code-hygiene-refactor** | [`skills/code-hygiene-refactor/SKILL.md`](code-hygiene-refactor/SKILL.md) | code hygiene, higiene de código, duplicação, limpeza, código morto, dívida técnica | Guia higienização ativa, deduplicação e refatoração segura sem scripts |
| **project-instantiation** | [`skills/project-instantiation/SKILL.md`](project-instantiation/SKILL.md) | bootstrap, instantiate, inicializar projeto, novo projeto | Guia a IA no bootstrap e renomeação de novos projetos na Fase 0 |
| **retroactive-instantiation** | [`skills/retroactive-instantiation/SKILL.md`](retroactive-instantiation/SKILL.md) | instanciação retroativa, aplicação existente, legado, migrar framework antigo | Guia adoção não destrutiva do FCVW em aplicações existentes ou parcialmente governadas |
| **agent-hermes** | [`skills/agent-hermes/SKILL.md`](agent-hermes/SKILL.md) | performance, desempenho, otimizar, lentidão, gargalo, latência | Perfil de agente sob demanda para uma melhoria de performance pequena, segura e validável |
| **agent-hephaestus** | [`skills/agent-hephaestus/SKILL.md`](agent-hephaestus/SKILL.md) | ux polish, UI, interface, acessibilidade, contraste, navegação por teclado | Perfil de agente sob demanda para uma melhoria pequena de UX, acessibilidade ou consistência visual |
| **agent-aegis** | [`skills/agent-aegis/SKILL.md`](agent-aegis/SKILL.md) | security scan, segurança, vulnerabilidade, vazamento de dados, credenciais, autenticação | Perfil de agente sob demanda para uma correção ou hardening de segurança pequeno e verificável |
| **agent-factory** | [`skills/agent-factory/SKILL.md`](agent-factory/SKILL.md) | create skill, create agent, specialized agent, criar skill | Gate mensurável para criar novas skills e perfis de agente sem proliferação arbitrária |
| **self-improvement** | [`skills/self-improvement/SKILL.md`](self-improvement/SKILL.md) | improve skill, improve agent, skill failed, gatilho falhou, skill não acionou, auto melhoria | Gate baseado em evidência para ajustar skills e agentes sem mudanças irrelevantes |
| **brainstorming-and-tdd** | [`skills/brainstorming-and-tdd/SKILL.md`](brainstorming-and-tdd/SKILL.md) | starting a new feature, fixing a bug, implementing a plan | Trava o agente no início para extrair especificações e obriga o uso de TDD |
| **systematic-debugging** | [`skills/systematic-debugging/SKILL.md`](systematic-debugging/SKILL.md) | debugging, fixing an error, tracking down a bug, stack trace | Força a depuração estruturada baseada em hipóteses |
| **orchestrator** | [`skills/orchestrator/SKILL.md`](orchestrator/SKILL.md) | large refactoring, complex plans, parallel tasks | Habilita a IA a coordenar tarefas complexas em modo delegado ou sequencial |
| **agnix-linter** | [`skills/agnix-linter/SKILL.md`](agnix-linter/SKILL.md) | periodic maintenance, governance audit, auditoria estrutural | Inspeciona e valida formatação, dead-links e consistência da pasta `FCVW/` |
| **memory-rotation** | [`skills/memory-rotation/SKILL.md`](memory-rotation/SKILL.md) | context bloat, clean sessions, rotate memory | Condensa sessões antigas do wiki em conceitos e remove excessos para proteger a janela de tokens |
| **governance-validator** | [`skills/governance-validator/SKILL.md`](governance-validator/SKILL.md) | validar governança, verificar filesystem, integridade documental, plan state coherence | Checklist para validar acurácia do FILESYSTEM.md, integridade documental e coerência de status dos planos |

---

## English

The `/skills/` directory serves as the framework's **Skills Engine**. It houses high-density technical procedure manuals and specialized operational checklists to guide the AI agent's execution in an efficient and standardized manner.

### Usage Guidelines

1. **Demand-Driven Activation (Token-Efficient)**: Skills must **never** be loaded in the initial AI prompt. The agent must read a skill file (using `view_file` with `IsSkillFile: true`) only when the active task explicitly demands executing that procedure.
2. **Clear Triggers**: Each skill must explicitly state its operational activation triggers, including PT-BR equivalents when bilingual usage is expected.
3. **High-Density Style**: Skills must utilize direct checklists and commands, eliminating filler narrative and verbose talk.
4. **Usage Registry**: When a skill is activated, it must be recorded in the corresponding AICC Session Synthesis inside `wiki/sessions/S*.md`.
5. **Controlled Growth**: new skills and agent profiles require `agent-factory`, recurrence/coverage/ROI metrics, and validation. Changes to skills or agents require `self-improvement` and evidence of failure, drift, or meaningful savings.

### Active Skills Catalog

| Skill | File | Primary Triggers | Benefit |
|---|---|---|---|
| **obsidian-markdown** | [`skills/obsidian-markdown/SKILL.md`](obsidian-markdown/SKILL.md) | wiki formatting, wikilinks, frontmatter, Obsidian notes | Standardizes LLM Wiki formatting and semantic connections |
| **git-conventional-commits** | [`skills/git-conventional-commits/SKILL.md`](git-conventional-commits/SKILL.md) | commit, tag, push, release notes, publish version | Standardizes commit messages, semantic tags, and release notes |
| **wiki-lint** | [`skills/wiki-lint/SKILL.md`](wiki-lint/SKILL.md) | lint wiki, wiki audit, orphan pages, broken links, invalid frontmatter | Validates wiki structural integrity |
| **release-checklist** | [`skills/release-checklist/SKILL.md`](release-checklist/SKILL.md) | release, publish, version bump, changelog, publicar versão | Condensed release checklist |
| **aicc-compact** | [`skills/aicc-compact/SKILL.md`](aicc-compact/SKILL.md) | shift close, compact session, close session, consolidate shift | Standardizes AICC context compression |
| **anti-monolith-guard** | [`skills/anti-monolith-guard/SKILL.md`](anti-monolith-guard/SKILL.md) | monolith, large file, new module, module boundary | Blocks mixed-responsibility artifacts before implementation |
| **code-hygiene-refactor** | [`skills/code-hygiene-refactor/SKILL.md`](code-hygiene-refactor/SKILL.md) | code hygiene, duplication, cleanup, dead code, higiene de código | Guides active cleanup, deduplication, and safe refactoring without scripts |
| **project-instantiation** | [`skills/project-instantiation/SKILL.md`](project-instantiation/SKILL.md) | bootstrap, new project, instantiate, initialize, briefing | Steers the JIT bootstrap workflow for new downstream projects securely |
| **retroactive-instantiation** | [`skills/retroactive-instantiation/SKILL.md`](retroactive-instantiation/SKILL.md) | retroactive instantiation, existing app, legacy app, framework migration | Guides non-destructive FCVW adoption |
| **agent-hermes** | [`skills/agent-hermes/SKILL.md`](agent-hermes/SKILL.md) | performance, optimize, bottleneck, desempenho, lentidão | On-demand agent profile for validated performance improvement |
| **agent-hephaestus** | [`skills/agent-hephaestus/SKILL.md`](agent-hephaestus/SKILL.md) | ux polish, accessibility, improve ui, interface, acessibilidade | On-demand agent profile for UX/accessibility improvements |
| **agent-aegis** | [`skills/agent-aegis/SKILL.md`](agent-aegis/SKILL.md) | security scan, vulnerability, harden, segurança, vazamento de dados | On-demand agent profile for security fixes or hardening |
| **agent-factory** | [`skills/agent-factory/SKILL.md`](agent-factory/SKILL.md) | create skill, create agent, specialized agent, criar skill | Measurable gate for creating new skills and agent profiles |
| **self-improvement** | [`skills/self-improvement/SKILL.md`](self-improvement/SKILL.md) | improve skill, improve agent, skill failed, gatilho falhou | Evidence-based gate for adjusting skills and agents |
| **brainstorming-and-tdd** | [`skills/brainstorming-and-tdd/SKILL.md`](brainstorming-and-tdd/SKILL.md) | starting a new feature, fixing a bug, implementing a plan | Halts the agent at the start to extract specs and enforces Red/Green TDD |
| **systematic-debugging** | [`skills/systematic-debugging/SKILL.md`](systematic-debugging/SKILL.md) | debugging, fixing an error, tracking down a bug, stack trace | Enforces structured hypothesis-based debugging |
| **orchestrator** | [`skills/orchestrator/SKILL.md`](orchestrator/SKILL.md) | large refactoring, complex plans, parallel tasks | Coordinates complex task decomposition |
| **agnix-linter** | [`skills/agnix-linter/SKILL.md`](agnix-linter/SKILL.md) | periodic maintenance, governance audit | Inspects FCVW formatting, dead-links, and consistency |
| **memory-rotation** | [`skills/memory-rotation/SKILL.md`](memory-rotation/SKILL.md) | context bloat, clean sessions, rotate memory | Condenses old wiki sessions into concepts |
| **governance-validator** | [`skills/governance-validator/SKILL.md`](governance-validator/SKILL.md) | validate governance, verify filesystem, document integrity, plan state coherence | Validates FILESYSTEM.md accuracy, governance integrity, and plan state consistency |
