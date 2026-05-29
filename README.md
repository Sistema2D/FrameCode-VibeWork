*Selecione o Idioma / Select Language:*
- [Português](#português)
- [English](#english)

---

## Português

[![Buy me a coffee](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20coffee&emoji=&slug=hugomelovek&button_colour=BD5FFF&font_colour=ffffff&font_family=Cookie&outline_colour=000000&coffee_colour=FFDD00)](https://www.buymeacoffee.com/hugomelovek)

> [!NOTE]
> ### 🛠️ Governança Assistida por IA (FrameCode VibeWork)
> Este projeto é regido pelo framework de governança documental e memória técnica **FrameCode VibeWork (FCVW)**, localizado integralmente na pasta `/FCVW`.
>
> Quando trabalhar com assistentes de IA (como Cursor, Windsurf ou agentes agentizados):
> * O agente lerá automaticamente o arquivo `./AGENTS.md` na raiz.
> * O agente utilizará a governança, planos e base de conhecimento dentro de `./FCVW/`.

### Estrutura do Repositório

```text
[project-root]/
├── 📁 src/                  # Código-fonte principal da sua aplicação (React, Node, Python, etc.)
├── 📁 public/               # Ativos estáticos públicos do seu sistema
├── 📄 package.json          # Configuração de pacotes e scripts da sua aplicação
├── 📄 .gitignore            # Filtros de versionamento do Git
├── 📄 README.md             # Este arquivo (descreve a sua aplicação)
├── 📄 AGENTS.md             # Ponte de instrução e regras para os agentes de IA
├── 📄 .cursorrules          # Regras operacionais para o Cursor IDE
├── 📄 .windsurfrules        # Regras operacionais para o Windsurf IDE
└── 📂 FCVW/                 # Subpasta contendo o motor do framework VibeWork
    ├── 📄 README.md         # Documentação original do framework VibeWork
    ├── 📄 STACK.md          # Arquitetura técnica e stack do projeto
    ├── 📄 SCOPE.md          # Limites funcionais e escopo do produto
    ├── 📄 ENVIRONMENT.md    # Governança de ambiente e segredos
    ├── 📄 PERFORMANCE.md    # Governança e orçamentos de desempenho
    ├── 📂 Plans/            # Planos de alteração e ciclo de vida
    ├── 📂 wiki/             # Memória técnica incremental do projeto (LLM Wiki)
    └── 📂 skills/           # Motor de habilidades avançadas e agentes autônomos
```

### Correlação e Cenários de Governança

```mermaid
graph TD
    classDef root fill:#8b5cf6,stroke:#fff,stroke-width:2px,color:#fff
    classDef core fill:#1a1d24,stroke:#8b5cf6,stroke-width:2px,color:#fff
    classDef node fill:#20232b,stroke:#3a3c42,stroke-width:1px,color:#d1d5db
    classDef folder fill:#10b981,stroke:#fff,stroke-width:1px,color:#fff

    A[AGENTS.md<br/>Root Entrypoint]:::root --> B(FCVW/CONTEXT_MAP.md<br/>Router):::core
    
    subgraph "Fase 0: Instanciação"
    B --> C1(INSTANTIATION.md)
    C1 --> C2(BRIEFING.md)
    C1 --> C3(MANIFEST.md)
    end
    
    subgraph "Fase 1: Workflow de Modificação"
    B --> P1(PLANNING.md)
    P1 --> P2[[Plans/]]:::folder
    P1 --> P3[[changelogs/]]:::folder
    end
    
    subgraph "Fase 2: Arquitetura Core"
    B --> A1(STACK.md)
    A1 --> A2(SCOPE.md)
    A1 --> A3(DATA.md)
    A1 --> A4(ENVIRONMENT.md)
    end
    
    subgraph "Fase 3: Motor de Inteligência"
    B --> M1(AI.md)
    M1 --> M2[[skills/]]:::folder
    M1 --> M3[[wiki/]]:::folder
    end
    
    subgraph "Fase 4: UX & Resiliência"
    B --> T1(TESTS.md)
    T1 --> T2(TROUBLESHOOTING.md)
    B --> D1(DESIGN.md)
    end
    
    subgraph "Fase 5: Entrega & Segurança"
    B --> R1(VERSIONING.md)
    R1 --> R2(RELEASE.md)
    R1 --> R3(SECURITY.md)
    R1 --> R4(AUDIT.md)
    R1 --> R5(PERFORMANCE.md)
    end

    class C1,C2,C3,P1,A1,A2,A3,A4,T1,T2,D1,M1,R1,R2,R3,R4,R5 node
```

### Como Começar

#### 1. Requisitos
* Um editor de código moderno com suporte a assistentes de IA (ex: Cursor, Windsurf, VS Code).
* Copiar o arquivo `AGENTS.md` para a raiz do seu projeto.
* Manter o diretório `/FCVW` íntegro na estrutura de pastas.

#### 2. Fluxo Inicial de Uso
1. **Defina o Contexto:** Descreva as metas e restrições iniciais em `FCVW/BRIEFING.md`.
2. **Configure as Regras:** Personalize o `FCVW/MANIFEST.md` com os princípios e arquitetura inegociáveis do seu projeto.
3. **Inicie o Desenvolvimento:** Oriente seu assistente de IA a ler `AGENTS.md` e seguir estritamente o ciclo de governança do framework.


### Gestão de Conhecimento e Obsidian

Para visualizar os gráficos de decisão, o histórico de versões formais, relatórios de troubleshooting e padrões arquiteturais do seu projeto:
1. Abra o aplicativo **Obsidian**.
2. Escolha **"Open folder as vault"** (Abrir pasta como cofre).
3. Selecione a subpasta `/FCVW` na raiz deste projeto.
4. Agora você pode navegar pelos planos, conceitos e conexões em um gráfico interativo completo!

*Este repositório foi organizado com amor usando o ecossistema assistido do FrameCode VibeWork.*

---

## English

[![Buy me a coffee](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20coffee&emoji=&slug=hugomelovek&button_colour=BD5FFF&font_colour=ffffff&font_family=Cookie&outline_colour=000000&coffee_colour=FFDD00)](https://www.buymeacoffee.com/hugomelovek)

> [!NOTE]
> ### 🛠️ AI-Assisted Governance (FrameCode VibeWork)
> This project is governed by the **FrameCode VibeWork (FCVW)** document governance and technical memory framework, located entirely in the `/FCVW` folder.
>
> When working with AI assistants (such as Cursor, Windsurf, or agentic workflows):
> * The agent will automatically read the `./AGENTS.md` file at the root.
> * The agent will utilize the governance, plans, and knowledge base within `./FCVW/`.

### Repository Structure

```text
[project-root]/
├── 📁 src/                  # Main source code of your application (React, Node, Python, etc.)
├── 📁 public/               # Public static assets of your system
├── 📄 package.json          # Package and scripts configuration for your app
├── 📄 .gitignore            # Git versioning filters
├── 📄 README.md             # This file (describes your application)
├── 📄 AGENTS.md             # Instruction bridge and rules for AI agents
├── 📄 .cursorrules          # Operational rules for the Cursor IDE
├── 📄 .windsurfrules        # Operational rules for the Windsurf IDE
└── 📂 FCVW/                 # Subfolder containing the VibeWork framework engine
    ├── 📄 README.md         # Original VibeWork framework documentation
    ├── 📄 STACK.md          # Technical architecture and project stack
    ├── 📄 SCOPE.md          # Functional boundaries and product scope
    ├── 📄 ENVIRONMENT.md    # Environment and secrets governance
    ├── 📄 PERFORMANCE.md    # Performance budgets and governance
    ├── 📂 Plans/            # Change plans and lifecycle management
    ├── 📂 wiki/             # Incremental technical memory of the project (LLM Wiki)
    └── 📂 skills/           # Advanced skills engine and autonomous agents
```

### Correlation and Governance Scenarios

```mermaid
graph TD
    classDef root fill:#8b5cf6,stroke:#fff,stroke-width:2px,color:#fff
    classDef core fill:#1a1d24,stroke:#8b5cf6,stroke-width:2px,color:#fff
    classDef node fill:#20232b,stroke:#3a3c42,stroke-width:1px,color:#d1d5db
    classDef folder fill:#10b981,stroke:#fff,stroke-width:1px,color:#fff

    A[AGENTS.md<br/>Root Entrypoint]:::root --> B(FCVW/CONTEXT_MAP.md<br/>Router):::core
    
    subgraph "Phase 0: Instantiation"
    B --> C1(INSTANTIATION.md)
    C1 --> C2(BRIEFING.md)
    C1 --> C3(MANIFEST.md)
    end
    
    subgraph "Phase 1: Modification Workflow"
    B --> P1(PLANNING.md)
    P1 --> P2[[Plans/]]:::folder
    P1 --> P3[[changelogs/]]:::folder
    end
    
    subgraph "Phase 2: Core Architecture"
    B --> A1(STACK.md)
    A1 --> A2(SCOPE.md)
    A1 --> A3(DATA.md)
    A1 --> A4(ENVIRONMENT.md)
    end
    
    subgraph "Phase 3: Intelligence Engine"
    B --> M1(AI.md)
    M1 --> M2[[skills/]]:::folder
    M1 --> M3[[wiki/]]:::folder
    end
    
    subgraph "Phase 4: UX & Resilience"
    B --> T1(TESTS.md)
    T1 --> T2(TROUBLESHOOTING.md)
    B --> D1(DESIGN.md)
    end
    
    subgraph "Phase 5: Delivery & Security"
    B --> R1(VERSIONING.md)
    R1 --> R2(RELEASE.md)
    R1 --> R3(SECURITY.md)
    R1 --> R4(AUDIT.md)
    R1 --> R5(PERFORMANCE.md)
    end

    class C1,C2,C3,P1,A1,A2,A3,A4,T1,T2,D1,M1,R1,R2,R3,R4,R5 node
```

### Getting Started

#### 1. Requirements
* A modern code editor with support for AI assistants (e.g., Cursor, Windsurf, VS Code).
* Copy the `AGENTS.md` file to the root of your project.
* Maintain the integrity of the `/FCVW` directory in your project's folder structure.

#### 2. Initial Workflow
1. **Define the Context:** Write down the initial goals and constraints in `FCVW/BRIEFING.md`.
2. **Configure the Rules:** Customize `FCVW/MANIFEST.md` with the non-negotiable principles and architecture of your project.
3. **Start Developing:** Instruct your AI assistant to read `AGENTS.md` and strictly follow the framework's governance cycle.


### Knowledge Management and Obsidian

To visualize decision graphs, formal version history, troubleshooting reports, and architectural patterns of your project:
1. Open the **Obsidian** app.
2. Choose **"Open folder as vault"**.
3. Select the `/FCVW` subfolder at the root of this project.
4. You can now navigate through plans, concepts, and connections in a fully interactive graph!

*This repository was lovingly organized using the FrameCode VibeWork assisted ecosystem.*

---

### Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Sistema2D/FrameCode-VibeWork&type=Date)](https://star-history.com/#Sistema2D/FrameCode-VibeWork&Date)

