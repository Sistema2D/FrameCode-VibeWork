# App

Esta é a raiz do repositório da aplicação sob desenvolvimento. O código-fonte principal, ativos públicos e configurações de build pertencem inteiramente a esta pasta.

---

> [!NOTE]
> ### 🛠️ Governança Assistida por IA (FrameCode VibeWork)
> Este projeto é regido pelo framework de governança documental e memória técnica **FrameCode VibeWork (FCVW)**, localizado integralmente na pasta `/FCVW`.
>
> Quando trabalhar com assistentes de IA (como Cursor, Windsurf ou agentes agentizados):
> * O agente lerá automaticamente o arquivo `./AGENTS.md` na raiz.
> * O agente utilizará a governança, planos e base de conhecimento dentro de `./FCVW/`.

---

## Estrutura do Repositório

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
    └── 📂 snippets/         # Biblioteca de componentes visuais reutilizáveis
```

---

## Como Começar

### 1. Requisitos
* [Adicione os requisitos do seu sistema aqui, ex: Node.js >= 20.0]

### 2. Instalação e Execução
```bash
# Instale as dependências da aplicação
npm install

# Inicie o servidor de desenvolvimento
npm run dev
```

---

## Gestão de Conhecimento e Obsidian

Para visualizar os gráficos de decisão, o histórico de versões formais, relatórios de troubleshooting e padrões arquiteturais do seu projeto:
1. Abra o aplicativo **Obsidian**.
2. Escolha **"Open folder as vault"** (Abrir pasta como cofre).
3. Selecione a subpasta `/FCVW` na raiz deste projeto.
4. Agora você pode navegar pelos planos, conceitos e conexões em um gráfico interativo completo!

---
*Este repositório foi organizado com amor usando o ecossistema assistido do FrameCode VibeWork.*
