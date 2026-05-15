# MANIFESTO.md

Manifesto operacional do projeto.

Este arquivo centraliza a identidade, o estado, as regras principais e os documentos oficiais do projeto. Ele deve funcionar como referência rápida para humanos e agentes de IA antes de qualquer análise, planejamento, implementação, refatoração, validação ou publicação de versão.

> Este é um modelo. Substitua os campos entre `<...>` pelas informações reais do projeto.

---

## 1. Identificação do projeto

| Campo | Informação |
|---|---|
| Nome do projeto | `<nome-do-projeto>` |
| Nome curto / codinome | `<nome-curto>` |
| Tipo de aplicação | `<web / desktop / mobile / CLI / API / biblioteca / híbrida>` |
| Plataforma alvo | `<Windows / Linux / macOS / Web / Android / iOS / multiplataforma>` |
| Responsável principal | `<nome>` |
| Repositório | `<URL ou caminho local>` |
| Versão atual | `V0.0.0` |
| Data de criação do manifesto | `AAAA-MM-DD` |
| Última atualização | `AAAA-MM-DD` |
| Status do projeto | `conceito / planejamento / desenvolvimento / validação / publicado / suspenso / descontinuado` |

---

## 2. Objetivo do projeto

Descrever, em poucas linhas, o objetivo principal da aplicação.

```text
<Descreva aqui o problema que a aplicação resolve, para quem ela é destinada e qual valor ela entrega.>
```

### 2.1 Problema tratado

```text
<Descreva o problema, limitação, necessidade ou oportunidade que motivou o projeto.>
```

### 2.2 Resultado esperado

```text
<Descreva o resultado prático esperado quando a aplicação estiver funcional.>
```

---

## 3. Público-alvo

| Público | Descrição | Necessidades principais |
|---|---|---|
| `<grupo 1>` | `<descrição>` | `<necessidades>` |
| `<grupo 2>` | `<descrição>` | `<necessidades>` |

---

## 4. Escopo resumido

### 4.1 Dentro do escopo

- `<funcionalidade ou responsabilidade 1>`
- `<funcionalidade ou responsabilidade 2>`
- `<funcionalidade ou responsabilidade 3>`

### 4.2 Fora do escopo

- `<item explicitamente fora do escopo 1>`
- `<item explicitamente fora do escopo 2>`
- `<item explicitamente fora do escopo 3>`

### 4.3 Dependências principais

- `<dependência técnica, operacional ou externa 1>`
- `<dependência técnica, operacional ou externa 2>`
- `<dependência técnica, operacional ou externa 3>`

---

## 5. Stack resumida

| Camada | Tecnologia / Ferramenta | Observações |
|---|---|---|
| Frontend | `<tecnologia>` | `<observações>` |
| Backend | `<tecnologia>` | `<observações>` |
| Banco de dados / persistência | `<tecnologia>` | `<observações>` |
| IA / LLM | `<modelo, runtime ou provedor>` | `<observações>` |
| Build | `<ferramenta>` | `<observações>` |
| Testes | `<ferramenta>` | `<observações>` |
| Distribuição | `<formato>` | `<observações>` |

---

## 6. Uso de IA no projeto

### 6.1 Funções da IA na aplicação

Marque ou descreva as funções previstas:

- [ ] Chat conversacional.
  - [ ] RAG / consulta a base de conhecimento.
  - [ ] Geração de texto.
  - [ ] Geração de código.
  - [ ] Classificação ou extração de dados.
  - [ ] Agentes com ferramentas.
  - [ ] Automação de tarefas.
  - [ ] Aprendizado contínuo (ciclo Ingest/Query/Lint descrito em `wiki/schema.md`).
  - [ ] Outro: `<descrever>`.

### 6.2 Limites da IA

- A IA não deve executar ações destrutivas sem confirmação explícita.
- A IA não deve acessar dados fora dos diretórios permitidos.
- A IA não deve inventar fontes, arquivos, estados de sistema ou resultados de validação.
- A IA deve informar limitações quando não conseguir validar uma informação.
- A IA deve respeitar os documentos oficiais do projeto.

### 6.3 Dados usados pela IA

| Tipo de dado | Origem | Persistência | Sensibilidade | Observações |
|---|---|---|---|---|
| `<tipo>` | `<origem>` | `<local>` | `<baixa/média/alta>` | `<observações>` |

---

## 7. Documentos oficiais do projeto

Os documentos abaixo compõem a governança do projeto. A ausência de algum documento deve ser registrada como pendência.

| Documento | Obrigatório | Função | Status |
|---|---:|---|---|
| `AGENTS.md` | Sim | Guia operacional para agentes de IA e humanos | `<existente/pendente>` |
| `README.md` | Sim | Apresentação, instalação, execução e uso | `<existente/pendente>` |
| `INSTANCIACAO.md` | Fase 0 | Instanciação do framework, renomeação e placeholders | `<existente/pendente/não aplicável>` |
| `ESCOPO.md` | Sim | Escopo funcional e limites do projeto | `<existente/pendente>` |
| `STACK.md` | Sim | Stack técnica, dependências e ambiente | `<existente/pendente>` |
| `DESIGN.md` | Quando houver UI | Diretrizes visuais e UX | `<existente/pendente/não aplicável>` |
| `WORKFLOW.md` | Sim | Fluxos funcionais, telas, eventos e integrações | `<existente/pendente>` |
| `PLANEJAMENTO.md` | Sim | Método para planos de alteração | `<existente/pendente>` |
| `VERSIONAMENTO.md` | Sim | Regras de versão e changelog | `<existente/pendente>` |
| `TROUBLESHOOTING.md` | Sim | Registro e tratativa de falhas | `<existente/pendente>` |
| `TESTES.md` | Sim | Regras de teste e validação | `<existente/pendente>` |
| `SEGURANCA.md` | Sim | Regras de segurança e privacidade | `<existente/pendente>` |
| `DADOS.md` | Quando houver persistência | Dados, armazenamento, migração e backup | `<existente/pendente/não aplicável>` |
| `IA.md` | Quando houver IA | Uso, limites e governança de IA | `<existente/pendente/não aplicável>` |
| `REFATORACAO.md` | Sim | Critérios e métricas para refatoração | `<existente/pendente>` |
| `RELEASE.md` | Sim | Procedimento operacional de publicação | `<existente/pendente>` |
| `AUDITORIA.md` | Sim | Checklists de conformidade documental e técnica | `<existente/pendente>` |
| `DECISOES_ARQUITETURAIS.md` | Recomendado | Registro de decisões arquiteturais | `<existente/pendente>` |
| `BRIEFING.md` | Fase 0 | Descoberta e briefing inicial do projeto | `<existente/pendente/não aplicável>` |
| `wiki/schema.md` | Quando houver vault/RAG | Regras operacionais da wiki no padrão LLM Wiki | `<existente/pendente/não aplicável>` |

---

## 8. Estrutura esperada do repositório

```text
.
├── AGENTS.md
├── MANIFESTO.md
├── README.md
├── INSTANCIACAO.md
├── ESCOPO.md
├── STACK.md
├── DESIGN.md
├── WORKFLOW.md
├── PLANEJAMENTO.md
├── VERSIONAMENTO.md
├── TROUBLESHOOTING.md
├── TESTES.md
├── SEGURANCA.md
├── DADOS.md
├── IA.md
├── REFATORACAO.md
├── RELEASE.md
├── AUDITORIA.md
├── DECISOES_ARQUITETURAIS.md
├── Planos/
│   ├── pendente/
│   ├── em andamento/
│   ├── concluído/
│   └── descontinuado/
├── changelogs/
├── troubleshooting/
├── decisoes/
├── auditorias/
├── briefings/
├── wiki/
├── governança/
├── .gitignore
├── src/
├── tests/
└── build/
```

Adapte esta estrutura conforme a stack real do projeto.

Os documentos preenchidos do projeto devem ficar na raiz. A pasta `governança/`, quando mantida no repositório, deve conter apenas modelos vazios reutilizáveis.

---

---

## 9. Governança Operacional

As regras de conduta, fluxos de alteração e checklists de qualidade estão centralizados no:

- `AGENTS.md`: Guia operacional diário e checklists de execução.
- `AUDITORIA.md`: Checklists formais de conformidade e pré-release.
- `PLANEJAMENTO.md`: Metodologia detalhada de planos de alteração.

Nenhuma alteração funcional, visual ou estrutural deve ser realizada sem seguir os fluxos definidos nestes documentos.

---

## 12. Riscos principais do projeto

| Risco | Probabilidade | Impacto | Mitigação | Documento relacionado |
|---|---|---|---|---|
| `<risco 1>` | `<baixa/média/alta>` | `<baixo/médio/alto>` | `<ação>` | `<documento>` |
| `<risco 2>` | `<baixa/média/alta>` | `<baixo/médio/alto>` | `<ação>` | `<documento>` |

---

## 13. Pendências estruturais

Use esta seção para registrar lacunas documentais ou estruturais do projeto.

| Pendência | Impacto | Prioridade | Plano relacionado | Status |
|---|---|---|---|---|
| `<pendência>` | `<impacto>` | `<P1-P5>` | `<arquivo em Planos/>` | `<status>` |

---

## 14. Histórico de atualização do manifesto

| Data | Versão do projeto | Alteração no manifesto | Responsável |
|---|---|---|---|
| `AAAA-MM-DD` | `V0.0.0` | `Criação do manifesto.` | `<nome>` |

---

## 15. Declaração de governança

Este projeto deve ser conduzido com rastreabilidade, validação, controle de escopo, segurança, documentação atualizada e versionamento coerente.

Nenhum agente humano ou de IA deve tratar os documentos de governança como opcionais quando a ação solicitada envolver alteração de código, documentação, configuração, design, testes, dados versionados, build, release, segurança ou comportamento funcional.
