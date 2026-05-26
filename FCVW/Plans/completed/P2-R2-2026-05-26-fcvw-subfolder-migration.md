---
context_files:
  - "AGENTS.md"
  - ".cursorrules"
  - ".windsurfrules"
  - "FILESYSTEM.md"
  - "INSTANTIATION.md"
---
# P2-R2-2026-05-26-fcvw-subfolder-migration

- **Description:** Mover toda a estrutura do framework FrameCode VibeWork para uma pasta dedicada chamada `FCVW/`, mantendo apenas o arquivo `AGENTS.md` e as regras de editores (`.cursorrules` / `.windsurfrules`) na raiz do repositório, que agora abrigará um novo `README.md` específico para a aplicação em desenvolvimento.
- **Justification:** O acúmulo de arquivos do framework e da aplicação na mesma pasta raiz causa poluição visual e conflitos de contexto. Isolar o framework melhora a separação de responsabilidades, limpa a raiz para a aplicação, permite um README focado no produto final e preserva a integridade documental do framework em uma pasta isolada que pode ser facilmente aberta como um Obsidian Vault.
- **Objective:** Obter uma separação física completa entre o framework FCVW e a aplicação sob desenvolvimento, garantindo que o agente de IA continue operando perfeitamente ao ler a raiz.
- **Scope:**
  - **Incluído:**
    - Criação da pasta `FCVW/`.
    - Movimentação de todos os 20+ arquivos markdown de governança (exceto `AGENTS.md` da raiz) para `FCVW/`.
    - Movimentação das pastas `Plans/`, `changelogs/`, `wiki/`, `skills/`, `snippets/`, `governance/`, `decisions/`, `troubleshooting/` para dentro de `FCVW/`.
    - Atualização do `AGENTS.md` na raiz para redirecionar os caminhos para `FCVW/`.
    - Atualização das regras `.cursorrules` e `.windsurfrules` na raiz.
    - Atualização interna de `FCVW/FILESYSTEM.md` e `FCVW/INSTANTIATION.md`.
    - Inicialização de um novo `README.md` na raiz focado na aplicação em desenvolvimento.
  - **Excluído:**
    - Criação de código-fonte de aplicação (src/) ou alteração de lógicas externas.
- **Affected files:**
  - `AGENTS.md` (Modificar na raiz)
  - `.cursorrules` (Modificar na raiz)
  - `.windsurfrules` (Modificar na raiz)
  - `README.md` (Mover o original para `FCVW/README.md` e criar novo na raiz)
  - `FILESYSTEM.md` (Mover para `FCVW/FILESYSTEM.md` e modificar)
  - `INSTANTIATION.md` (Mover para `FCVW/INSTANTIATION.md` e modificar)
  - Todos os outros arquivos e diretórios de governança (Mapeados na movimentação física para `FCVW/`)
- **Implementation plan:**
  1. Criar a pasta física `FCVW/`.
  2. Mover o `README.md` original do framework para `FCVW/README.md`.
  3. Mover todos os outros arquivos de governança da raiz para `FCVW/` (ex: `AI.md`, `STACK.md`, `SCOPE.md`, `DESIGN.md`, etc.).
  4. Mover todas as pastas de governança para `FCVW/` (incluindo este plano, que passará a residir em `FCVW/Plans/completed/`).
  5. Ajustar o arquivo `AGENTS.md` que permanece na raiz para atuar como ponte, updating todos os links para a pasta `FCVW/`.
  6. Modificar `.cursorrules` e `.windsurfrules` na raiz para apontar para `FCVW/`.
  7. Modificar `FCVW/FILESYSTEM.md` para atualizar o mapa físico e documentar a estrutura `/FCVW/`.
  8. Criar o novo `README.md` na raiz da aplicação.
- **Acceptance criteria:**
  - [x] A raiz possui apenas `AGENTS.md`, `.cursorrules`, `.windsurfrules`, `.gitignore` e o novo `README.md` do app.
  - [x] Todos os arquivos e diretórios originais do framework residem dentro de `FCVW/`.
  - [x] O `AGENTS.md` na raiz contém links relativos funcionais apontando para `FCVW/`.
  - [x] As regras do Cursor/Windsurf apontam a IA corretamente para `AGENTS.md` raiz e `FCVW/Plans/`.
- **Test plan:**
  - [x] Validar a leitura e parsing do `AGENTS.md` raiz pelo agente de IA.
  - [x] Validar que nenhum link relativo interno no `AGENTS.md` está quebrado.
  - [x] Validar que a abertura da pasta `FCVW/` como vault isolado no Obsidian mantém o gráfico de conexões funcional.
- **Priority:** `P2` (High)
- **Risk:** `R2` (Low)
- **Current Version:** `V0.4.0`
- **Expected Version:** `V0.5.0`
- **Status:** `completed`
- **Creation Date:** 2026-05-26
- **Completion Date:** 2026-05-26
- **Technical observations:**
  - A reestruturação de subpastas foi executada com absoluto sucesso, resultando em uma raiz de projeto limpa e totalmente voltada à aplicação sob desenvolvimento.

## Validation Executed (Fill on completion)

### Environment
- OS: Windows 11 / PowerShell
- Backend/Runtime: AI Agent (Antigravity)

### Tests
| Test | Result | Evidence |
|---|---|---|
| Integridade física da raiz | Sucesso | Apenas arquivos de ponte e README raiz mantidos. Todos os outros em `/FCVW`. |
| Ponte `AGENTS.md` | Sucesso | Todos os caminhos internos adaptados com prefixo `FCVW/`. |
| Regras de editores | Sucesso | `.cursorrules` e `.windsurfrules` modificados apontando para `./FCVW/`. |
| Novo README raiz | Sucesso | Documento limpo focado na aplicação inicializado. |
| Obsidian Vault Nesting | Sucesso | Cofre isolado aberto em `/FCVW/` testado sem links quebrados. |

### Final Result
`approved`
