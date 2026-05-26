---
context_files:
  - "FCVW/MANIFEST.md"
  - "FCVW/CONTEXT_MAP.md"
  - "FCVW/skills/README.md"
  - "FCVW/FILESYSTEM.md"
  - "FCVW/README.md"
  - "README.md"
  - "AGENTS.md"
  - "FCVW/REFACTORING.md"
---
# P3-R2-2026-05-26-expand-governance-and-ase-v0-6-0

- **Description:** Adicionar novas diretrizes de governança (ambiente, segredos e performance), novas skills JIT (ASE) de bootstrapping e de compactação AICC, e o Technical Debt Ledger acoplado ao REFACTORING.md e à Wiki.
- **Justification:** O framework necessita de mecanismos estruturados para lidar de forma pure-markdown com chaves de API/segredos, budgets de performance de UI/API e processos repetitivos de IA (Compactação AICC e Bootstrapping de novos projetos), além de centralizar e auditar débitos técnicos.
- **Objective:** Expansão robusta do ecossistema de governança FrameCode VibeWork com portabilidade absoluta (sem scripts de automação ou dependências externas), atingindo a versão V0.6.0.
- **Scope:**
  - **Incluído:**
    - Criação de `FCVW/ENVIRONMENT.md` e `FCVW/governance/TEMPLATE_ENV.md`.
    - Criação de `FCVW/PERFORMANCE.md` e `FCVW/governance/TEMPLATE_API_SPEC.md`.
    - Criação das novas Skills JIT em `FCVW/skills/aicc-compact/SKILL.md` e `FCVW/skills/project-instantiation/SKILL.md`.
    - Criação de `FCVW/wiki/templates/TEMPLATE_TECH_DEBT.md`.
    - Modificação em `FCVW/REFACTORING.md` para incluir a seção 24 (Technical Debt & Refactoring Ledger).
    - Atualização dos arquivos de índice: `MANIFEST.md`, `CONTEXT_MAP.md`, `skills/README.md`, `FILESYSTEM.md`, `FCVW/README.md`, `README.md` da raiz e `AGENTS.md` da raiz.
    - Criação do changelog `FCVW/changelogs/V0.6.0.md`.
  - **Excluído:**
    - Escrita de código-fonte de aplicação (src/) ou qualquer script ativo (.py/.ps1).
- **Affected files:**
  - `FCVW/ENVIRONMENT.md` [NEW]
  - `FCVW/governance/TEMPLATE_ENV.md` [NEW]
  - `FCVW/PERFORMANCE.md` [NEW]
  - `FCVW/governance/TEMPLATE_API_SPEC.md` [NEW]
  - `FCVW/skills/aicc-compact/SKILL.md` [NEW]
  - `FCVW/skills/project-instantiation/SKILL.md` [NEW]
  - `FCVW/wiki/templates/TEMPLATE_TECH_DEBT.md` [NEW]
  - `FCVW/REFACTORING.md` [MODIFY]
  - `FCVW/MANIFEST.md` [MODIFY]
  - `FCVW/CONTEXT_MAP.md` [MODIFY]
  - `FCVW/skills/README.md` [MODIFY]
  - `FCVW/FILESYSTEM.md` [MODIFY]
  - `FCVW/README.md` [MODIFY]
  - `README.md` [MODIFY]
  - `AGENTS.md` [MODIFY]
  - `FCVW/docs/index.html` [MODIFY]
- **Implementation plan:**
  1. Criar os quatro novos arquivos de governança e templates (`ENVIRONMENT.md`, `TEMPLATE_ENV.md`, `PERFORMANCE.md`, `TEMPLATE_API_SPEC.md`).
  2. Implementar as novas skills em `FCVW/skills/`.
  3. Modificar `FCVW/REFACTORING.md` e criar `TEMPLATE_TECH_DEBT.md`.
  4. Sincronizar todos os arquivos de mapeamento e índice (`MANIFEST.md`, `CONTEXT_MAP.md`, `skills/README.md`, `FILESYSTEM.md`, `README.md`s e `AGENTS.md`).
  5. Criar changelog `changelogs/V0.6.0.md`.
  6. Finalizar o plano e mover para `completed/`.
- **Acceptance criteria:**
  - [x] Todos os novos arquivos Markdown descritos foram criados nas pastas corretas.
  - [x] Os caminhos relativos entre os arquivos e os índices funcionam perfeitamente.
  - [x] Não há códigos executáveis ou dependências ativas adicionadas.
  - [x] O changelog de versão V0.6.0 está devidamente registrado.
- **Test plan:**
  - [x] Verificar integridade física dos links internos em Markdown.
  - [x] Validar a leitura e parsing do cabeçalho YAML para Obsidian nas novas notas da wiki.
  - [x] Confirmar compatibilidade total de caminhos na raiz da aplicação.
- **Priority:** `P3` (Medium)
- **Risk:** `R2` (Low)
- **Current Version:** `V0.5.2`
- **Expected Version:** `V0.6.0`
- **Status:** `completed`
- **Creation Date:** 2026-05-26
- **Completion Date:** 2026-05-26
- **Technical observations:**
  - Execução estritamente em conformidade com o ADR-0001.

## Validation Executed (Fill on completion)

### Environment
- OS: Windows 11
- Backend/Runtime: AI Agent (Antigravity)

### Tests
| Test | Result | Evidence |
|---|---|---|
| Mapeamento de Arquivos | Sucesso | Todos os novos arquivos (ENVIRONMENT.md, PERFORMANCE.md, etc.) criados nos caminhos corretos e mapeados nos índices. |
| Skills JIT | Sucesso | Novas skills (aicc-compact, project-instantiation) escritas de forma densa e catalogadas no skills/README.md. |
| Débitos Técnicos | Sucesso | Seção de Debt Ledger adicionada ao REFACTORING.md e template oficial criado em wiki/templates/. |
| Integridade de Links | Sucesso | Auditoria manual de caminhos relativos confirmou zero quebras de links. |
| Docs index.html | Sucesso | Página de documentação atualizada em todas as 4 línguas com os novos módulos e selo V0.6.0. |

### Final Result
`approved`
