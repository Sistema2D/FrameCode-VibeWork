# FrameCode VibeWork Framework

Current framework version: `V0.10.2`

*Select Language / Selecione o Idioma:*
- [Português](#português)
- [English](#english)

---

## Português

**FrameCode VibeWork** é um framework de governança documental e técnica para desenvolvimento de aplicações assistido por IA. Ele reduz perda de contexto entre sessões ao combinar planos formais, changelogs, auditorias, troubleshooting, decisões arquiteturais, design system declarativo e uma LLM Wiki mantida em Markdown.

### Como Funciona

O framework usa um ciclo de vida explícito para garantir que mudanças sejam justificadas, planejadas, implementadas, validadas e registradas.

```mermaid
graph TD
    A["Fase 0: Briefing"] -->|"Definição de escopo"| B["Manifesto e Escopo"]
    B -->|"Solicitação de mudança"| C["Plano de alteração"]
    C -->|"Execução assistida por IA"| D["Implementação"]
    D -->|"Rastreabilidade"| E["Changelog e versionamento"]
    E -->|"Validação"| F["Auditoria e release"]
    F -->|"Aprendizado"| G["Wiki / memória técnica"]
    G -->|"Publicacao externa opcional"| H["Site/documentacao fora do framework"]
    H -->|"Contexto acumulado"| C
```

### Fluxo de Sessão com Carregamento Sob Demanda

O framework organiza o trabalho em **cenários de sessão** — cada um define quais documentos carregar imediatamente, quais carregar sob demanda e quais pular. O diagrama abaixo mapeia os 17 cenários com base no `CONTEXT_MAP.md`:

```mermaid
graph TD
    Start["Início da Sessão"] --> ReadCM["Ler CONTEXT_MAP.md\ne AGENTS.md §checklist"]
    ReadCM --> IdentifyType["Identificar tipo de sessão"]

    IdentifyType -->|Bugfix / Troubleshooting| Bugfix["Imediato: TROUBLESHOOTING.md\n+ PLANNING.md\nSob demanda: troubleshooting/, wiki/failures/"]
    IdentifyType -->|New Feature| Feature["Imediato: SCOPE.md + PLANNING.md\nSob demanda: DESIGN.md (se UI),\nAI.md (se AI), wiki/index.md"]
    IdentifyType -->|App Module Docs| AppDocs["Imediato: APPLICATION_DOCUMENTATION.md\n+ PLANNING.md\nSob demanda: TEMPLATE_MODULE_DOCUMENTATION.md,\nTEMPLATE_FLOW_DOCUMENTATION.md"]
    IdentifyType -->|UI / Components| UI["Imediato: DESIGN.md\nSob demanda: wiki/patterns/"]
    IdentifyType -->|Refactoring| Refact["Imediato: REFACTORING.md\n+ PLANNING.md\nSob demanda: wiki/refactorings/, TESTS.md"]
    IdentifyType -->|Agent / Skill Creation| AssetCreate["Imediato: AI.md + PLANNING.md\n+ skill:agent-factory\nSob demanda: proposal template"]
    IdentifyType -->|Skill / Agent Self-Improvement| AssetImprove["Imediato: AI.md + PLANNING.md\n+ skill:self-improvement\nSob demanda: AUDIT.md, report template"]
    IdentifyType -->|Release| Release["Imediato: skill:release-checklist\nSob demanda: VERSIONING.md,\nAUDIT.md, RELEASE.md"]
    IdentifyType -->|Briefing / Instanciação| Briefing["Imediato: INSTANTIATION.md\n+ BRIEFING.md\nSob demanda: skill:project-instantiation,\nMANIFEST.md, STACK.md"]
    IdentifyType -->|Retroactive Inst.| Retro["Imediato: RETROACTIVE_INSTANTIATION.md\n+ INSTANTIATION.md\nSob demanda: CONTEXT_MAP.md"]
    IdentifyType -->|Wiki / Knowledge| Wiki["Imediato: wiki/schema.md\n+ wiki/index.md\nSob demanda: skill:wiki-lint, wiki/log.md"]
    IdentifyType -->|Security / Data| Security["Imediato: SECURITY.md + DATA.md\nSob demanda: AI.md, TESTS.md"]
    IdentifyType -->|Document Audit| Audit["Imediato: MANIFEST.md + AUDIT.md\nSob demanda: skill:governance-validator,\nwiki/index.md, changelogs/"]
    IdentifyType -->|PR / Code Review| PR["Imediato: AGENTS.md §Code Review\nSob demanda: refactoring-guide/17,\nPLANNING.md (risk gates)"]
    IdentifyType -->|Deploy / Environment| Deploy["Imediato: ENVIRONMENT.md §5\nSob demanda: RELEASE.md §Deployment,\nskill:release-checklist"]
    IdentifyType -->|Multi-Agent / Collab.| Multi["Imediato: AGENTS.md §Multi-Agent\nSob demanda: Plans/in_progress/,\nwiki/agents/ (journals)"]
    IdentifyType -->|Git / Commit / Tag| Git["Imediato: skill:git-conventional-commits\nSob demanda: VERSIONING.md"]

    Bugfix --> Execute["Executar escopo\n+ registrar em changelog"]
    Feature --> Execute
    AppDocs --> Execute
    UI --> Execute
    Refact --> Execute
    AssetCreate --> Execute
    AssetImprove --> Execute
    Release --> Execute
    Briefing --> Execute
    Retro --> Execute
    Wiki --> Execute
    Security --> Execute
    Audit --> Execute
    PR --> Execute
    Deploy --> Execute
    Multi --> Execute
    Git --> Execute

    Execute --> Validate["Validar:\ngovernance-validator\nou testes"]
    Validate --> Close["Fechar sessão:\nAICC session synthesis"]
```

### Pilares

#### 1. Governança por planos

Nenhuma alteração funcional, visual, estrutural ou documental deve ser aplicada sem plano correspondente em `Plans/`.

#### 2. Rastreabilidade por versão

Toda alteração em arquivo versionado deve ser registrada em `changelogs/Vx.y.z.md`, com plano relacionado, arquivos afetados, validação e riscos residuais.

#### 3. Memória técnica incremental

A pasta `wiki/` segue o padrão LLM Wiki: fontes brutas, páginas sintetizadas, índice, log, links internos, estados de confiança e lint periódico.

> **Portabilidade e Reuso:** O conhecimento acumulado na `wiki/` (padrões, decisões, troubleshooting) pode e deve ser portado e reutilizado em novos projetos para acelerar o desenvolvimento assistido por IA e manter a consistência técnica entre diferentes aplicações.

#### 4. Design system declarativo

O arquivo `DESIGN.md` centraliza tokens, regras visuais, contratos de componentes e critérios de experiência. A antiga pasta `snippets/` foi descontinuada; exemplos físicos devem ser gerados na aplicação instanciada quando necessários.

#### 5. Separação entre framework e projeto

A pasta `governance/` preserva templates genéricos. Os documentos preenchidos do projeto ficam na raiz da aplicação instanciada, não na raiz do framework-base. A instanciação e as regras de renomeação estão em `INSTANTIATION.md`.

#### 6. Motor de Habilidades (ASE)

A pasta `skills/` armazena procedimentos técnicos de alta densidade carregados sob demanda pelo agente de IA — nunca pré-carregados no prompt. Isso preserva a janela de contexto enquanto disponibiliza checklists especializados quando necessários.

#### 7. Criação e melhoria controlada de skills/agentes

Novas skills e perfis de agente só podem ser criados via `agent-factory`, com métricas de recorrência, cobertura, ROI de tokens/risco, escopo estreito e validação. Ajustes em skills ou agentes existentes exigem `self-improvement` com evidência de falha, drift ou economia relevante.

#### 8. Documentacao de modulos da aplicacao

`APPLICATION_DOCUMENTATION.md` define como a aplicacao instanciada deve manter documentacao propria de modulos, telas, componentes e fluxos em `docs/`, usando templates de `governance/`.

#### 9. Journals de agentes

Journals de agentes devem usar `wiki/agents/<agent_name>_journal.md` para manter a memoria operacional centralizada.

Habilidades ativas: `agent-aegis`, `agent-factory`, `agent-hephaestus`, `agent-hermes`, `agnix-linter`, `aicc-compact`, `anti-monolith-guard`, `brainstorming-and-tdd`, `code-hygiene-refactor`, `git-conventional-commits`, `governance-validator`, `memory-rotation`, `obsidian-markdown`, `orchestrator`, `project-instantiation`, `release-checklist`, `retroactive-instantiation`, `self-improvement`, `systematic-debugging`, `wiki-lint`.

### Estrutura De Diretórios

A estrutura detalhada e auditável do framework é mantida em `FILESYSTEM.md`. Este README registra apenas o mapa operacional resumido:

- raiz do repositório: pertence à aplicação em desenvolvimento; mantém `AGENTS.md` e arquivos ponte/configuração.
- `FCVW/`: fonte canônica dos documentos, governança, memória, planos, changelogs e habilidades do framework.
- site/documentacao publica: nao faz parte do baseline fisico do framework; quando necessario, publique em repositorio ou pipeline externo.
- `FCVW/FILESYSTEM.md`: fonte de verdade para a árvore completa e para o estado esperado dos diretórios.
- `FCVW/CONTEXT_MAP.md`: mapa compacto de carregamento seletivo por tipo de sessão.
- `APPLICATION_DOCUMENTATION.md`: regras de documentacao de modulos da aplicacao.

### Consumo de Tokens por Cenário

Para maximizar a transparência de custos de chamadas de APIs de LLMs, o framework mapeia estimativas de planejamento para cada cenário de desenvolvimento com base em suas políticas ativas:

| Cenário Mapeado | Documentos Ingeridos | Custo Inicial (Sem AICC) | Custo por Turno com AICC | Economia com AICC |
| :--- | :--- | :---: | :---: | :---: |
| **Bugfix / Troubleshooting** | `AGENTS.md` + `TROUBLESHOOTING.md` + `PLANNING.md` | ~5.000 tokens | **~1.200 tokens** | **-76%** |
| **Nova Funcionalidade** | `AGENTS.md` + `SCOPE.md` + `PLANNING.md` + `DESIGN.md` | ~7.000 tokens | **~1.500 tokens** | **-78%** |
| **App Module Docs** | `AGENTS.md` + `APPLICATION_DOCUMENTATION.md` + `PLANNING.md` | ~5.000 tokens | **~1.200 tokens** | **-76%** |
| **Componentes / UI** | `AGENTS.md` + `DESIGN.md` | ~4.000 tokens | **~900 tokens** | **-77%** |
| **Refatoração** | `AGENTS.md` + `REFACTORING.md` + `PLANNING.md` | ~8.000 tokens | **~1.800 tokens** | **-77%** |
| **Criação de Skill/Agente** | `AGENTS.md` + `AI.md` + `PLANNING.md` + `skill:agent-factory` | ~5.500 tokens | **~1.200 tokens** | **-78%** |
| **Self-Improvement de Skill/Agente** | `AGENTS.md` + `AI.md` + `PLANNING.md` + `skill:self-improvement` | ~5.500 tokens | **~1.200 tokens** | **-78%** |
| **Release** | `CONTEXT_MAP.md` + `skill:release-checklist` (JIT) | ~2.500 tokens | **~600 tokens** | **-76%** |
| **Briefing / Instanciação** | `AGENTS.md` + `INSTANTIATION.md` + `BRIEFING.md` + `MANIFEST.md` | ~8.500 tokens | **~2.000 tokens** | **-76%** |
| **Wiki / Knowledge** | `AGENTS.md` + `wiki/schema.md` + `wiki/index.md` | ~5.500 tokens | **~1.300 tokens** | **-76%** |
| **Security / Data** | `AGENTS.md` + `SECURITY.md` + `DATA.md` | ~6.000 tokens | **~1.400 tokens** | **-77%** |
| **Document Audit** | `AGENTS.md` + `MANIFEST.md` + `AUDIT.md` | ~6.000 tokens | **~1.400 tokens** | **-77%** |
| **PR / Code Review** | `AGENTS.md §Code Review` + (se refatoração) `refactoring-guide/17` | ~4.000 tokens | **~1.000 tokens** | **-75%** |
| **Deploy / Environment** | `AGENTS.md` + `ENVIRONMENT.md §5` + `RELEASE.md §Deployment` | ~5.000 tokens | **~1.200 tokens** | **-76%** |
| **Multi-Agent / Collaboration** | `AGENTS.md §Multi-Agent` + `Plans/in_progress/` | ~3.500 tokens | **~800 tokens** | **-77%** |
| **Git / Commit / Tag** | `skill:git-conventional-commits` (JIT) | ~1.500 tokens | **~400 tokens** | **-73%** |

*Nota: As estimativas são valores de referência para planejamento, não medições recalibradas automaticamente após cada mudança documental. Recalibre-as após crescimento material dos documentos de governança. 1 token ≈ 4 caracteres em inglês ou ~3 caracteres em português.*

### Como Usar

#### 1. Copiar ou clonar

Use este repositório como base para um novo projeto ou mantenha-o como framework central.

```bash
git clone https://github.com/Sistema2D/FrameCode-VibeWork.git meu-projeto
cd meu-projeto
```

#### 2. Instanciar

Leia `AGENTS.md` e `INSTANTIATION.md`. A instanciação não depende de script automático: renomeações e substituições devem ser feitas explicitamente, preservando templates em `governance/` e `wiki/templates/`.

#### 3. Executar Fase 0

Preencha `BRIEFING.md`, atualize `MANIFEST.md`, `STACK.md`, `SCOPE.md` e gere o `README.md` da aplicação na raiz, registrando a alteração por plano e changelog.

#### 4. Trabalhar com IA

Ao solicitar mudanças, peça para o agente seguir `AGENTS.md`. Para consultas, análise e revisão sem edição de arquivos, plano não é obrigatório. Para qualquer alteração, o fluxo de plano e changelog é obrigatório.

---

## English

**FrameCode VibeWork** is a technical and document-based governance framework for AI-assisted application development. It reduces context loss between sessions by combining formal plans, changelogs, audits, troubleshooting, architectural decisions, a declarative design system, and an LLM Wiki maintained in Markdown.

### How It Works

The framework uses an explicit lifecycle to ensure that changes are justified, planned, implemented, validated, and recorded.

```mermaid
graph TD
    A["Phase 0: Briefing"] -->|"Scope definition"| B["Manifest and Scope"]
    B -->|"Change request"| C["Change plan"]
    C -->|"AI-assisted execution"| D["Implementation"]
    D -->|"Traceability"| E["Changelog and versioning"]
    E -->|"Validation"| F["Audit and release"]
    F -->|"Learning"| G["Wiki / technical memory"]
    G -->|"Optional external publishing"| H["Site/documentation outside the framework"]
    H -->|"Accumulated context"| C
```

### Session Flow with On-Demand Loading

The framework organizes work into **session scenarios** — each defines which documents to load immediately, which to load on demand, and which to skip. The diagram below maps the 17 scenarios based on `CONTEXT_MAP.md`:

```mermaid
graph TD
    Start["Session Start"] --> ReadCM["Read CONTEXT_MAP.md\nand AGENTS.md §checklist"]
    ReadCM --> IdentifyType["Identify session type"]

    IdentifyType -->|Bugfix / Troubleshooting| Bugfix["Immediate: TROUBLESHOOTING.md\n+ PLANNING.md\nOn demand: troubleshooting/, wiki/failures/"]
    IdentifyType -->|New Feature| Feature["Immediate: SCOPE.md + PLANNING.md\nOn demand: DESIGN.md (if UI),\nAI.md (if AI), wiki/index.md"]
    IdentifyType -->|App Module Docs| AppDocs["Immediate: APPLICATION_DOCUMENTATION.md\n+ PLANNING.md\nOn demand: TEMPLATE_MODULE_DOCUMENTATION.md,\nTEMPLATE_FLOW_DOCUMENTATION.md"]
    IdentifyType -->|UI / Components| UI["Immediate: DESIGN.md\nOn demand: wiki/patterns/"]
    IdentifyType -->|Refactoring| Refact["Immediate: REFACTORING.md\n+ PLANNING.md\nOn demand: wiki/refactorings/, TESTS.md"]
    IdentifyType -->|Agent / Skill Creation| AssetCreate["Immediate: AI.md + PLANNING.md\n+ skill:agent-factory\nOn demand: proposal template"]
    IdentifyType -->|Skill / Agent Self-Improvement| AssetImprove["Immediate: AI.md + PLANNING.md\n+ skill:self-improvement\nOn demand: AUDIT.md, report template"]
    IdentifyType -->|Release| Release["Immediate: skill:release-checklist\nOn demand: VERSIONING.md,\nAUDIT.md, RELEASE.md"]
    IdentifyType -->|Briefing / Instantiation| Briefing["Immediate: INSTANTIATION.md\n+ BRIEFING.md\nOn demand: skill:project-instantiation,\nMANIFEST.md, STACK.md"]
    IdentifyType -->|Retroactive Inst.| Retro["Immediate: RETROACTIVE_INSTANTIATION.md\n+ INSTANTIATION.md\nOn demand: CONTEXT_MAP.md"]
    IdentifyType -->|Wiki / Knowledge| Wiki["Immediate: wiki/schema.md\n+ wiki/index.md\nOn demand: skill:wiki-lint, wiki/log.md"]
    IdentifyType -->|Security / Data| Security["Immediate: SECURITY.md + DATA.md\nOn demand: AI.md, TESTS.md"]
    IdentifyType -->|Document Audit| Audit["Immediate: MANIFEST.md + AUDIT.md\nOn demand: skill:governance-validator,\nwiki/index.md, changelogs/"]
    IdentifyType -->|PR / Code Review| PR["Immediate: AGENTS.md §Code Review\nOn demand: refactoring-guide/17,\nPLANNING.md (risk gates)"]
    IdentifyType -->|Deploy / Environment| Deploy["Immediate: ENVIRONMENT.md §5\nOn demand: RELEASE.md §Deployment,\nskill:release-checklist"]
    IdentifyType -->|Multi-Agent / Collab.| Multi["Immediate: AGENTS.md §Multi-Agent\nOn demand: Plans/in_progress/,\nwiki/agents/ (journals)"]
    IdentifyType -->|Git / Commit / Tag| Git["Immediate: skill:git-conventional-commits\nOn demand: VERSIONING.md"]

    Bugfix --> Execute["Execute scope\n+ record in changelog"]
    Feature --> Execute
    AppDocs --> Execute
    UI --> Execute
    Refact --> Execute
    AssetCreate --> Execute
    AssetImprove --> Execute
    Release --> Execute
    Briefing --> Execute
    Retro --> Execute
    Wiki --> Execute
    Security --> Execute
    Audit --> Execute
    PR --> Execute
    Deploy --> Execute
    Multi --> Execute
    Git --> Execute

    Execute --> Validate["Validate:\ngovernance-validator\nor tests"]
    Validate --> Close["Close session:\nAICC session synthesis"]
```

### Pillars

#### 1. Governance by Plans

No functional, visual, structural, or document change should be applied without a corresponding plan in `Plans/`.

#### 2. Version Traceability

Every change in a versioned file must be recorded in `changelogs/Vx.y.z.md`, with related plans, affected files, validation, and residual risks.

#### 3. Incremental Technical Memory

The `wiki/` folder follows the LLM Wiki standard: raw sources, synthesized pages, index, log, internal links, confidence states, and periodic linting.

> **Portability and Reuse:** The knowledge accumulated in the `wiki/` (patterns, decisions, troubleshooting) can and should be ported and reused in new projects to accelerate AI-assisted development and maintain technical consistency across different applications.

#### 4. Declarative Design System

`DESIGN.md` centralizes tokens, visual rules, component contracts, and experience criteria. The former `snippets/` folder is discontinued; physical examples should be generated inside the instantiated application when needed.

#### 5. Framework and Project Separation

The `governance/` folder preserves generic templates. Filled project documents reside at the instantiated application root, not at the framework-baseline root. Instantiation and renaming rules are in `INSTANTIATION.md`.

#### 6. AI Skills Engine (ASE)

The `skills/` folder stores high-density technical procedures loaded on-demand by the AI agent — never pre-loaded into the prompt. This preserves the context window while making specialized checklists available when needed.

#### 7. Controlled Skill/Agent Creation and Improvement

New skills and agent profiles can only be created through `agent-factory`, with recurrence, coverage, token/risk ROI, narrow-scope, and validation metrics. Changes to existing skills or agents require `self-improvement` with failure, drift, or meaningful-savings evidence.

#### 8. Application Module Documentation

`APPLICATION_DOCUMENTATION.md` defines how the instantiated application should keep its own module, screen, component, and flow documentation in `docs/`, using templates from `governance/`.

#### 9. Agent Journals

Agent journals must use `wiki/agents/<agent_name>_journal.md` to keep operational memory centralized.

Active skills: `agent-aegis`, `agent-factory`, `agent-hephaestus`, `agent-hermes`, `agnix-linter`, `aicc-compact`, `anti-monolith-guard`, `brainstorming-and-tdd`, `code-hygiene-refactor`, `git-conventional-commits`, `governance-validator`, `memory-rotation`, `obsidian-markdown`, `orchestrator`, `project-instantiation`, `release-checklist`, `retroactive-instantiation`, `self-improvement`, `systematic-debugging`, `wiki-lint`.

### Directory Structure

The detailed and auditable framework structure is maintained in `FILESYSTEM.md`. This README records only the operational summary:

- repository root: owned by the application under development; keeps `AGENTS.md` and bridge/configuration files.
- `FCVW/`: canonical source for framework documents, governance, memory, plans, changelogs, and skills.
- public site/documentation: not part of the framework physical baseline; publish it in an external repository or pipeline when needed.
- `FCVW/FILESYSTEM.md`: source of truth for the complete tree and expected directory state.
- `FCVW/CONTEXT_MAP.md`: compact selective loading map by session type.
- `APPLICATION_DOCUMENTATION.md`: application module documentation rules.

### Token Consumption by Scenario

To maximize transparency and API call cost-efficiency with LLMs, the framework maps planning estimates for each development scenario based on its active policies:

| Mapped Scenario | Ingested Documents | Initial Load (No AICC) | Continuous Turn Cost (With AICC) | Savings with AICC |
| :--- | :--- | :---: | :---: | :---: |
| **Bugfix / Troubleshooting** | `AGENTS.md` + `TROUBLESHOOTING.md` + `PLANNING.md` | ~5,000 tokens | **~1,200 tokens** | **-76%** |
| **New Feature** | `AGENTS.md` + `SCOPE.md` + `PLANNING.md` + `DESIGN.md` | ~7,000 tokens | **~1,500 tokens** | **-78%** |
| **App Module Docs** | `AGENTS.md` + `APPLICATION_DOCUMENTATION.md` + `PLANNING.md` | ~5,000 tokens | **~1,200 tokens** | **-76%** |
| **UI / Components** | `AGENTS.md` + `DESIGN.md` | ~4,000 tokens | **~900 tokens** | **-77%** |
| **Refactoring** | `AGENTS.md` + `REFACTORING.md` + `PLANNING.md` | ~8,000 tokens | **~1,800 tokens** | **-77%** |
| **Skill/Agent Creation** | `AGENTS.md` + `AI.md` + `PLANNING.md` + `skill:agent-factory` | ~5,500 tokens | **~1,200 tokens** | **-78%** |
| **Skill/Agent Self-Improvement** | `AGENTS.md` + `AI.md` + `PLANNING.md` + `skill:self-improvement` | ~5,500 tokens | **~1,200 tokens** | **-78%** |
| **Release** | `CONTEXT_MAP.md` + `skill:release-checklist` (JIT) | ~2,500 tokens | **~600 tokens** | **-76%** |
| **Briefing / Instantiation** | `AGENTS.md` + `INSTANTIATION.md` + `BRIEFING.md` + `MANIFEST.md` | ~8,500 tokens | **~2,000 tokens** | **-76%** |
| **Wiki / Knowledge** | `AGENTS.md` + `wiki/schema.md` + `wiki/index.md` | ~5,500 tokens | **~1,300 tokens** | **-76%** |
| **Security / Data** | `AGENTS.md` + `SECURITY.md` + `DATA.md` | ~6,000 tokens | **~1,400 tokens** | **-77%** |
| **Document Audit** | `AGENTS.md` + `MANIFEST.md` + `AUDIT.md` | ~6,000 tokens | **~1,400 tokens** | **-77%** |
| **PR / Code Review** | `AGENTS.md §Code Review` + (if refactoring) `refactoring-guide/17` | ~4,000 tokens | **~1,000 tokens** | **-75%** |
| **Deploy / Environment** | `AGENTS.md` + `ENVIRONMENT.md §5` + `RELEASE.md §Deployment` | ~5,000 tokens | **~1,200 tokens** | **-76%** |
| **Multi-Agent / Collaboration** | `AGENTS.md §Multi-Agent` + `Plans/in_progress/` | ~3,500 tokens | **~800 tokens** | **-77%** |
| **Git / Commit / Tag** | `skill:git-conventional-commits` (JIT) | ~1,500 tokens | **~400 tokens** | **-73%** |

*Note: Estimates are planning reference values, not measurements automatically recalibrated after every documentation change. Recalibrate them after material growth in the governance documents. 1 token ≈ 4 characters in English or ~3 characters in Portuguese.*

### How to Use

#### 1. Copy or Clone

Use this repository as a base for a new project or keep it as a central framework.

```bash
git clone https://github.com/Sistema2D/FrameCode-VibeWork.git my-project
cd my-project
```

#### 2. Instantiate

Read `AGENTS.md` and `INSTANTIATION.md`. Instantiation does not rely on automatic scripts: renaming and replacements must be done explicitly, preserving templates in `governance/` and `wiki/templates/`.

#### 3. Execute Phase 0

Fill out `BRIEFING.md`, update `MANIFEST.md`, `STACK.md`, `SCOPE.md`, generate the application root `README.md`, and record the change via plan and changelog.

#### 4. Work with AI

When requesting changes, ask the agent to follow `AGENTS.md`. For queries, analysis, and reviews without file editing, a plan is not mandatory. For any modification, the plan and changelog workflow is mandatory.

---

## Obsidian

Abra a pasta raiz como um vault no Obsidian para visualizar links entre decisões, falhas, padrões, auditorias, releases e sínteses da wiki. / Open the root folder as a vault in Obsidian to visualize links between decisions, failures, patterns, audits, releases, and wiki syntheses.

## Créditos / Credits

O conceito de LLM Wiki usado como inspiração para a memória técnica incremental deste framework é creditado a Andrej Karpathy, autor do gist [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). / The LLM Wiki concept used as inspiration for the incremental technical memory of this framework is credited to Andrej Karpathy, author of the [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) gist.

Se este framework for útil para o seu trabalho, você pode apoiar o desenvolvimento pelo Buy Me a Coffee: / If this framework is useful for your work, you can support development via Buy Me a Coffee:

[Support development on Buy Me a Coffee](https://www.buymeacoffee.com/hugomelovek)

## Licença / License

Este projeto está licenciado sob a licença MIT. Veja `LICENSE`. / This project is licensed under the MIT license. See `LICENSE`.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Sistema2D/FrameCode-VibeWork&type=Date)](https://star-history.com/#Sistema2D/FrameCode-VibeWork&Date)
