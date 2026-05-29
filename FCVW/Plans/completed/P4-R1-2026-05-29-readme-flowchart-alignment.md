---
context_files:
  - README.md
  - FCVW/CONTEXT_MAP.md
  - FCVW/PLANNING.md
  - FCVW/VERSIONING.md
  - FCVW/governance/TEMPLATE_PLAN.md
  - FCVW/changelogs/unreleased/README.md
  - FCVW/wiki/sessions/README.md
  - FCVW/wiki/templates/TEMPLATE_SESSION_SYNTHESIS.md
  - FCVW/wiki/index.md
  - FCVW/wiki/log.md
  - FCVW/MANIFEST.md
  - FCVW/STACK.md
---
# P4-R1-2026-05-29-readme-flowchart-alignment

- **Description:** Atualizar o fluxograma do README para cobrir todos os tipos de sessao do CONTEXT_MAP, incluir AICC quando aplicavel e manter AGENTS.md como primeiro passo. Gerar registros de changelog e sessao.
- **Justification:** O diagrama atual nao cobre todos os cenarios oficiais e nao explicita o passo AICC.
- **Objective:** Fluxograma alinhado ao fluxo real do framework, com validacao Mermaid e rastreabilidade documental.
- **Scope:**
  - Inclusao de todos os tipos de sessao do CONTEXT_MAP.
  - Passo de leitura AICC quando aplicavel.
  - Decisao principal focada em alteracao de codigo, com desvio para mudancas documentais.
  - Atualizacao do README (PT/EN), changelog fragment e sessao AICC.
- **Affected files:**
  - README.md
  - FCVW/changelogs/unreleased/P4-R1-2026-05-29-readme-flowchart-alignment.md
  - FCVW/wiki/sessions/S001-2026-05-29-readme-flowchart-alignment.md
  - FCVW/wiki/index.md
  - FCVW/wiki/log.md
- **Implementation plan:**
  1. Atualizar o diagrama Mermaid no README (PT/EN) conforme o fluxo aprovado.
  2. Validar o diagrama com o Mermaid validator e gerar preview.
  3. Criar fragmento de changelog em unreleased.
  4. Criar sintese de sessao AICC e registrar em wiki/index.md e wiki/log.md.
  5. Atualizar o plano com validacao e mover para completed.
- **Acceptance criteria:**
  - [x] Diagrama do README inclui todos os tipos de sessao e o passo AICC.
  - [x] AGENTS.md permanece como primeira leitura do fluxo.
  - [x] Decisao principal trata alteracao de codigo e contempla mudancas documentais.
  - [x] Mermaid validator executado sem erros e preview gerado.
  - [x] Fragmento de changelog criado em unreleased.
  - [x] Sessao AICC criada e registrada em wiki/index.md e wiki/log.md.
- **Test plan:**
  - [x] Mermaid diagram validator.
  - [x] Mermaid diagram preview.
- **Priority:** `P4`
- **Risk:** `R1`
- **Current Version:** `V0.6.0`
- **Expected Version:** `V0.6.0`
- **Status:** `completed`
- **Creation Date:** 2026-05-29
- **Completion Date:** 2026-05-29
- **Technical observations:**
  - STACK.md indica versao V0.5.2 enquanto MANIFEST.md indica V0.6.0; fora do escopo deste plano.

## Validation Executed (Fill on completion)

### Environment
- OS: Windows
- Backend/Runtime: Not applicable

### Tests
| Test | Result | Evidence |
|---|---|---|
| Mermaid diagram validator | pass | Mermaid diagram syntax is valid. |
| Mermaid diagram preview | pass | Mermaid diagram preview opened successfully. |

### Final Result
`approved`
