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


