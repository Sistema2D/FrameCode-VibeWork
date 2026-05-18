# Skills Engine Catalog & Guidelines

*Selecione o Idioma / Select Language:*
- [Português](#português)
- [English](#english)

---

## Português

A pasta `/skills/` atua como o **Motor de Habilidades (Skills Engine)** do framework. Ela armazena manuais de procedimentos técnicos de alta densidade e checklists operacionais especializados para direcionar a execução do agente de IA de forma eficiente e padronizada.

### Diretrizes de Uso

1. **Ativação por Demanda (Token-Efficient)**: As skills **nunca** devem ser carregadas no prompt inicial da IA. O agente deve ler um arquivo de skill (com `view_file` e `IsSkillFile: true`) apenas quando a tarefa ativamente exigir a execução daquele procedimento.
2. **Gatilhos Claros**: Cada skill deve declarar explicitamente seus gatilhos operacionais de ativação.
3. **Estilo de Alta Densidade**: As skills devem usar checklists e comandos diretos, eliminando narrativa filler e conversas prolixas.
4. **Registro de Uso**: Quando uma skill é ativada, ela deve ser listada na Síntese de Sessão AICC correspondente em `wiki/sessions/S*.md`.

### Catálogo de Skills Ativas

- **[`obsidian-markdown`](file:///c:/Users/meloha/Desktop/FCVW/skills/obsidian-markdown/SKILL.md)**: Especializada em padronizar a formatação, propriedades, callouts e conexões semânticas bidirecionais (wikilinks) em notas da LLM Wiki.

---

## English

The `/skills/` directory serves as the framework's **Skills Engine**. It houses high-density technical procedure manuals and specialized operational checklists to guide the AI agent's execution in an efficient and standardized manner.

### Usage Guidelines

1. **Demand-Driven Activation (Token-Efficient)**: Skills must **never** be loaded in the initial AI prompt. The agent must read a skill file (using `view_file` with `IsSkillFile: true`) only when the active task explicitly demands executing that procedure.
2. **Clear Triggers**: Each skill must explicitly state its operational activation triggers.
3. **High-Density Style**: Skills must utilize direct checklists and commands, eliminating filler narrative and verbose talk.
4. **Usage Registry**: When a skill is activated, it must be recorded in the corresponding AICC Session Synthesis inside `wiki/sessions/S*.md`.

### Active Skills Catalog

- **[`obsidian-markdown`](file:///c:/Users/meloha/Desktop/FCVW/skills/obsidian-markdown/SKILL.md)**: Specialized in standardizing formatting, properties, callouts, and internal bidirectional semantic connections (wikilinks) in LLM Wiki notes.
