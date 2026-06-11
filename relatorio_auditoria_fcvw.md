# Relatório de melhorias para agentes, skills e governança do framework

## 0. Sumário executivo

Este relatório técnico apresenta recomendações de melhorias estruturais, de segurança e de governança para o FrameCode VibeWork (FCVW). Baseado na leitura sob demanda dos arquivos `AGENTS.md`, `SECURITY.md`, `skills/README.md`, `AI.md`, `AUDIT.md`, `VERSIONING.md` e `MANIFEST.md`, foram identificadas oportunidades de aprimoramento na sanitização da base de código, expansão das capacidades do agente Aegis (com foco em vazamento de dados no client-side), otimização de gatilhos de ativação, autoatualização do framework e regionalização de registros. As propostas mantêm o princípio de leitura sob demanda para eficiência de tokens e priorizam abordagens não destrutivas.

---

## 1. Sanitização periódica sob demanda

A tabela abaixo propõe regras de sanitização que podem ser executadas periodicamente, minimizando a leitura desnecessária e protegendo a janela de contexto da IA.

| Objetivo | Frequência Sugerida | Gatilho Recomendado | Arquivos ou Áreas Prováveis | Risco de Falso Positivo | Estratégia Segura | Evidência Mínima |
|---|---|---|---|---|---|---|
| **Limpeza de arquivos obsoletos** | A cada versionamento major | `clean up project`, `remove dead files` | `FCVW/Plans/`, `FCVW/troubleshooting/`, `FCVW/wiki/` | Médio (remover arquivos ainda referenciados) | Validar com `grep_search` se há referências antes de propor remoção. | Nenhuma referência encontrada no repositório + aprovação do usuário. |
| **Identificar código duplicado/abandonado** | Ao finalizar grandes refatorações ou a cada 50 iterações | `check for dead code`, `audit refactor` | Arquivos alterados em planos recentes (`FCVW/changelogs/`) | Alto (códigos parecidos podem ter contextos diferentes) | Usar ferramentas de análise estática (se disponíveis) ou comparar assinaturas de funções nos arquivos mapeados. | Funções idênticas sem referências de importação externas. |
| **Revisão de dependências não utilizadas** | A cada versionamento minor | `check dependencies`, `audit packages` | `package.json`, `requirements.txt` ou equivalentes | Baixo | Comparar lista de dependências com imports reais nos arquivos principais. | Relatório de ferramenta de análise ou ausência completa de imports no projeto. |
| **Revisão de documentos desatualizados** | A cada versionamento minor ou a cada 20 sessões (AICC) | `audit governance`, `check docs` | `AGENTS.md`, `FCVW/MANIFEST.md` | Baixo | Consultar `FCVW/AUDIT.md` e cruzar versões com `MANIFEST.md` e `STACK.md`. | Inconsistência de versão ou referência a arquivos deletados. |
| **Limpeza de artefatos temporários** | A cada 10 iterações da IA ou a cada fechamento de plano S3/S4 | `clean temp files`, `remove logs` | `logs/`, `.tmp/`, sobras de testes | Muito Baixo | Identificar pastas de cache e extensões de log (ex: `*.log`). Nunca excluir dados não versionados (`DATA.md`). | Confirmação visual de que os arquivos não são essenciais. |
| **Revisão de dívida técnica (TODO/FIXME)** | A cada versionamento patch ou a cada 15 iterações | `list tech debt`, `check TODOs` | Arquivos da base de código alvo da aplicação | Médio | Listar com `grep_search` marcadores `TODO`, `FIXME` e consolidá-los na wiki sob a tag `#tech-debt`. | Existência de comentários não vinculados a um plano ativo. |

---

## 2. Regras adicionais para o Aegis: vazamento de dados via navegador

O agente **Aegis** (`agent-aegis`) deve expandir sua análise de segurança para prevenir a exposição de dados sensíveis no front-end, complementando o documento `SECURITY.md`.

| Padrão de Risco | Como Identificar | Arquivos/Termos a Verificar | Severidade | Recomendação de Correção | O que NÃO Fazer |
|---|---|---|---|---|---|
| **Credenciais/Segredos no Front-end** | Busca por variáveis com `SECRET`, `TOKEN`, `KEY` sendo enviadas no bundle público ou hardcoded. | `src/`, `public/`, `*.js`, `*.jsx`, `.env` | Crítica (S4) | Mover lógica para o backend/BFF ou usar variáveis `NEXT_PUBLIC_` apenas para dados seguros. | Não apagar credenciais automaticamente; acionar o protocolo "Secret Handshake". |
| **Lógica Crítica de Autorização no Client** | Verificação de permissões `isAdmin` ou roles sem validação correspondente nas chamadas à API. | Arquivos de rotas (`routes.js`), componentes de guarda (`AuthGuard.jsx`) | Alta (S3) | Alertar que a UI esconde componentes, mas a API deve validar a mesma flag. | Não tentar reescrever a API inteira; focar em alertar sobre a falsa segurança do client. |
| **Dados Sensíveis em Storage Local** | Referências a `localStorage.setItem` ou `sessionStorage.setItem` salvando senhas, tokens inteiros (não JWT seguros) ou PII. | Componentes de Auth, utilitários de storage | Alta (S3) | Usar cookies `HttpOnly` e `Secure` para tokens sensíveis em vez de Web Storage. | Não remover o código sem antes propor o plano de migração de storage. |
| **Source Maps em Produção** | Presença de source maps expondo código original de bibliotecas de segurança ou lógicas de negócio. | `webpack.config.js`, `vite.config.js`, `.env.production` | Moderada (S2) | Desativar a geração de source maps para o build de produção (`GENERATE_SOURCEMAP=false`). | Não desativar source maps em ambientes de desenvolvimento local. |
| **Endpoints Administrativos Expostos** | Rotas com `/admin`, `/internal` declaradas no roteador do front-end visíveis a usuários sem login. | Arquivos de rotas, sitemaps dinâmicos | Moderada (S2) | Implementar Code Splitting condicional para que o bundle admin não seja entregue a não administradores. | Não remover a rota admin; propor a separação de bundles. |
| **Logs Expondo Dados** | Uso de `console.log()` renderizando objetos inteiros que contêm senhas ou dados bancários. | Qualquer arquivo `*.js/ts` do front | Moderada (S2) | Remover ou comentar o `console.log()` ou implementar linter que barre isso em PRs. | Não quebrar o fluxo da aplicação; apenas intervir na camada de log. |

---

## 3. Gatilhos atuais de skills e agentes

Com base na análise de `FCVW/skills/README.md`, os seguintes gatilhos explícitos foram identificados:

*   **obsidian-markdown:** `wiki formatting, wikilinks, frontmatter, Obsidian notes`
*   **git-conventional-commits:** `commit, tag, push, release notes, publish version`
*   **wiki-lint:** `lint wiki, wiki audit, orphan pages, broken links, invalid frontmatter`
*   **release-checklist:** `release, publish, version bump, cut a release`
*   **aicc-compact:** `shift close, compact session, close session, consolidate shift`
*   **project-instantiation:** `bootstrap, new project, instantiate, initialize, briefing`
*   **retroactive-instantiation:** `retroactive instantiation, existing app, legacy app, framework migration`
*   **agent-hermes:** `run perf agent, improve performance, optimize`
*   **agent-hephaestus:** `ux polish, accessibility fix, improve ui`
*   **agent-aegis:** `security scan, fix vulnerability, harden`
*   **brainstorming-and-tdd:** `starting a new feature, fixing a bug, implementing a plan`
*   **systematic-debugging:** `debugging, fixing an error, tracking down a bug, stack trace`
*   **orchestrator:** `large refactoring, complex plans, parallel tasks`
*   **agnix-linter:** `periodic maintenance, governance audit`
*   **memory-rotation:** `context bloat, clean sessions, rotate memory`

A maioria dos gatilhos é explícita e manual. Eles dependem que o usuário invoque os termos-chave correspondentes para que a IA faça o `view_file` da skill apropriada.

---

## 4. GAPs nos gatilhos

A dependência exclusiva de ativação manual e certas sobreposições geram algumas lacunas:

| Descrição do Problema | Impacto Prático | Agente/Skill Afetado | Proposta de Melhoria | Texto Sugerido para Nova Regra | Prioridade |
|---|---|---|---|---|---|
| **Auditoria de segurança opcional** | Vulnerabilidades introduzidas sem aviso prévio. | `agent-aegis` / `SECURITY.md` | Ativação preventiva antes de fechamento de `S3/S4 plans`. | "Se o plano classificado como S3 ou S4 estiver na fase de validação, acione o gatilho `security scan` antes de movê-lo para concluído." | Alta |
| **Limpeza de código pós-refatoração** | Acúmulo de código morto que as skills de TDD ou Orchestrator deixam para trás. | `orchestrator`, novas skills | Incluir rotina de higienização ao final de `large refactoring`. | "Sempre que finalizar um `large refactoring`, invoque um `code cleanup` para varrer referências órfãs afetadas." | Média |
| **Ambiguidade entre Linters** | `wiki-lint` foca na wiki e `agnix-linter` foca em `FCVW/`. Falta linter para a aplicação base. | Linters | Definir melhor as fronteiras ou sugerir skill para a *codebase* alvo. | "Use `agnix-linter` estritamente para auditoria de framework FCVW, e não para análise de código da aplicação cliente." | Média |
| **Auto-compaction esquecido** | Fim de sessão dependente da memória do usuário em pedir `close session`. | `aicc-compact` | Instruir a IA a sugerir o AICC compact se a janela de contexto estiver muito carregada. | "Se a interação envolver múltiplos arquivos modificados e uma pausa for sugerida, oferte proativamente: 'Deseja consolidar a sessão (aicc-compact)?'" | Baixa |

---

## 5. Higienização de código: novo agente, skill ou incorporação

### Comparação de Alternativas

*   **Criar novo agente (`agent-janitor`):** Especializado, atua de forma autônoma. Risco: pode ser destrutivo se atuar sem supervisão.
*   **Incorporar ao Aegis:** Inadequado. Aegis tem foco em segurança, higienização é manutenção e manutenibilidade.
*   **Incorporar ao `agnix-linter`:** `agnix-linter` analisa formatação da pasta `FCVW/`, misturar com limpeza de código de aplicação polui seu escopo.
*   **Nova skill de higienização (`code-sanitization`):** Otimizada para tokens (acionada sob demanda), ativada pelo usuário ou como follow-up após refatorações.

**Recomendação Final:** **Nova Skill (`code-sanitization`)** que pode ser utilizada pelo agente principal ou orquestrador. Isso evita o consumo de recursos de um subagente contínuo e garante intervenção manual aprovativa (o princípio de nunca apagar nada sem plano e confirmação).

### Rascunho da Skill `code-sanitization`

*   **Missão:** Reduzir débito técnico passivo (código duplicado, morto, órfão) preservando funcionalidades e o histórico.
*   **Escopo:** Mapeamento de imports não utilizados, funções não chamadas, arquivos obsoletos em diretórios alvo, limpeza de logs/testes esquecidos.
*   **Fora de escopo:** Refatorações arquiteturais, mudança de lógica de negócio, atualizações de dependência.
*   **Gatilhos:** `code cleanup`, `sanitize codebase`, `remove dead code`.
*   **Checklist Obrigatório:**
    1. Usar `grep_search` para rastrear qualquer uso da função/arquivo.
    2. Verificar referências dinâmicas no código.
    3. Documentar a remoção no `changelog` vigente.
*   **Critérios para Não Alterar:** Funções de API públicas (mesmo sem uso interno), código atrelado a features flagadas como inativas, esquemas de banco de dados comentados como backup.
*   **Relatório e PR:** Elaborar "Plano de Remoção" curto, justificando os ganhos; só prosseguir após o usuário confirmar "OK para remover".

---

## 6. Checagem de versão e autoatualização aprovada pelo usuário

O fluxo de atualização do framework deve ser seguro e documentado, preferencialmente descrito em `FCVW/VERSIONING.md` e `FCVW/RELEASE.md`.

**Fluxo Seguro Proposto:**

1.  **Detectar versão atual:** A IA lê o `Current Version` no arquivo local `FCVW/MANIFEST.md`.
2.  **Consultar release mais recente:** A IA faz uma chamada de leitura (fetch) à API do GitHub: `https://api.github.com/repos/Sistema2D/Planner-Simples-Editado/releases/latest`.
    *   *Fallback 1:* Caso não existam releases formais, buscar pelas `tags`.
3.  **Comparar versões:** Se a versão online for maior (ex: `v0.9.0` vs `v0.8.0`), ativar fluxo de sugestão.
4.  **Apresentar resumo e riscos:** Extrair as "Release Notes" do GitHub e exibir ao usuário os ganhos e os *breaking changes*.
5.  **Pedir aprovação:** Perguntar explicitamente: *"Deseja iniciar o plano de atualização para o framework FCVW? Isso pode modificar seus arquivos em `FCVW/governance`."*
6.  **Criar Plano:** Abrir um plano em `FCVW/Plans/pending` para executar o pull/fetch.
7.  **Atualizar e Registrar:** Fazer a mesclagem cuidadosa (preservando configurações do usuário em `AGENTS.md`), criar o `changelog/Vx.y.z.md` e atualizar o `MANIFEST.md` local.

**Onde Documentar:** Uma nova seção "Self-Update Procedures" deve ser incluída no `FCVW/MANIFEST.md` e `FCVW/VERSIONING.md`.

---

## 7. Regionalização dos registros

Apesar do projeto estrutural (framework) estar em inglês internacional (`MANIFEST.md`), as interações do usuário brasileiro devem preservar a sintaxe local para os registros gerados pela IA, a fim de manter legibilidade da equipe.

**Regras Propostas (A serem adicionadas em `FCVW/AI.md` e `FCVW/wiki/schema.md`):**

*   **Detecção de Idioma:** A IA deve analisar o idioma majoritário do *prompt* do usuário. Se o usuário fornecer instruções em PT-BR, a IA **deve redigir o conteúdo documental** (Changelogs, ADRs, Plans, Wiki, Session Syntheses) em **Português do Brasil**, a menos que o projeto especifique outro idioma nativo de negócio.
*   **Termos Técnicos Preservados:** Manter no original inglês (ex: `changelog`, `pull request`, `frontmatter`, `release`, `bugfix`, `deploy`, nomes de pastas `FCVW/Plans/`). Não traduzir para "registro de mudanças" ou "pedido de puxar".
*   **Idomas de Arquivos e Identificadores:** Nomes de arquivos (`TEMPLATE_*.md`), variáveis de ambiente, nomes de funções e chaves de JSON devem permanecer rigorosamente em inglês.
*   **Fallback de Ambiguidade:** Se o usuário falar de modo genérico, o idioma de registros deverá ser o mesmo idioma declarado em "Language" dentro do `MANIFEST.md` da aplicação-alvo.

---

## 8. Instruções “DE/PARA” para implementação futura

| DE | PARA | Justificativa | Arquivo Provável |
|---|---|---|---|
| Ativação de Aegis apenas explícita por usuário | Ativação explícita **E** sugerida antes de fechamento de `S3/S4 plans` | Prevê riscos antes que a versão seja liberada. | `FCVW/skills/README.md` / `FCVW/SECURITY.md` |
| Sem política clara de limpeza de código alvo | Adição do gatilho e skill `code-sanitization` | Reduz débito técnico sem poluir os linters de governança. | `FCVW/skills/README.md` |
| Registros gerados em idioma padrão da IA | Regionalização baseada na entrada do usuário (PT-BR) preservando termos técnicos | Alinha a documentação gerada à linguagem de negócios da equipe local. | `FCVW/AI.md` (Memory and History) |
| Ignorância sobre versões upstream | Fluxo de `self-update` lendo releases do GitHub Sistema2D | Facilita a adoção de melhorias contínuas do framework e evita bifurcações mortas. | `FCVW/MANIFEST.md` / `FCVW/VERSIONING.md` |
| Aegis apenas foca em backend / genérico | Adição de detecção de segredos em *client-side bundles* e *Web Storage* | Bloqueia a ilusão de segurança (credentials no front end). | `FCVW/skills/agent-aegis/SKILL.md` (quando existir) |

---

## 9. Métricas Antirregressão e Gestão de Riscos

As regras atuais de mitigação foram endurecidas para incluir métricas consolidadas e portões de validação (gates) inegociáveis. Para evitar regressões no framework ou na aplicação cliente, as seguintes métricas são obrigatórias:

*   **Tolerância Zero para Remoção Cega (Sanitização):** Nenhuma exclusão de arquivo ou bloco de código pode ocorrer sem que o `grep_search` indique exatamente `0 referências ativas` em todo o escopo do projeto (ignorando apenas pastas de dependências). Deleções exigem o status de "aprovação humana pendente" (bloqueio "hard").
*   **Métrica de Integridade da Wiki (Zero Broken Links):** Sempre que a governança do framework for autoatualizada ou ocorrer rotação de memória, o gatilho `wiki-lint` é acionado automaticamente. A métrica de sucesso exige o retorno inegociável de `0 links quebrados` e `0 páginas órfãs` causadas pela alteração atual.
*   **Proteção de Overwrite na Autoatualização (Diff Mandatório):** O framework jamais substituirá de forma forçada arquivos que o usuário naturalmente edita (como `AGENTS.md`, `FCVW/SCOPE.md`, `FCVW/DESIGN.md`). A métrica exige que, para esses arquivos, a autoatualização apresente obrigatoriamente um "Diff Review" para o usuário aprovar cada fragmento. O overwrite autônomo é tolerado *apenas* em arquivos de template genéricos dentro de `FCVW/governance/`.
*   **Prevenção Estrita de Token Bloat:** Para evitar que a sanitização desestabilize o agente consumindo a janela de tokens, ferramentas de busca (`grep_search`, linters) recebem uma métrica de recusa: se a leitura incluir automaticamente pastas como `node_modules`, `.next`, `.git` ou `dist`, a ação de sanitização deve falhar no ato (fail-fast) para poupar tokens.
*   **Preservação das Tags AICC:** Toda e qualquer alteração documental gerada pela autoatualização ou por scripts de higienização deve preservar intocáveis as tags do modelo de Technical Memory (ex: `#gold-pattern`, `#tech-debt`, `#arch-decision`).

---

## 10. Próximos passos recomendados

Para a implementação destas melhorias, siga a ordem:

1.  **Baixo risco:** Atualizar o `FCVW/AI.md` adicionando as regras de Regionalização dos Registros.
2.  **Média prioridade e baixo risco:** Criar a nova skill file `FCVW/skills/code-sanitization/SKILL.md` contendo as diretrizes aprovadas.
3.  **Segurança e Expansão:** Atualizar a documentação e a skill do `agent-aegis` incluindo os padrões de risco no navegador.
4.  **Autoatualização (Maior complexidade):** Documentar e aprovar um plano estruturado (S3) para implementar o script/módulo de checagem contra a API do GitHub.

---

## 11. Plano para Inclusão de Diffs nos Changelogs (Análise de Viabilidade)

A proposta de incluir as *diffs* literais de código por arquivo diretamente nos `changelogs/Vx.y.z.md` foi analisada quanto à sua viabilidade técnica frente à mecânica do framework (especialmente em relação à janela de tokens da IA).

### Viabilidade e Riscos
*   **Token Bloat (Risco Crítico):** Changelogs são frequentemente lidos pelas ferramentas de `memory-rotation` e na preparação de auditorias. Inserir linhas de código (`+` / `-`) causaria imediato esgotamento da janela de contexto e perda de memória nas sessões subsequentes.
*   **Poluição Visual:** Arquivos Markdown com linhas de *diffs* tornam a leitura humana árdua, contrariando o princípio do FCVW de ser amigável e legível.

### Plano de Implementação Seguro (Aprovado)
Devido ao alto risco de poluição e perda de contexto, a inclusão de linhas de código literais no changelog fica **terminantemente proibida**. A rastreabilidade será garantida através do extrato estatístico:

1.  **Adoção Exclusiva do `Diff Stat`:** A seção do changelog deve registrar o extrato gerado pelo comando `git diff --stat` (ou sumarização similar da IA), listando unicamente os arquivos afetados e o respectivo saldo numérico de inserções/deleções.
2.  **Referências de Commit:** Para auditoria do código real que foi alterado, a IA deve registrar no changelog apenas o hash do commit correspondente (`[Commit a1b2c3d](...)`) ou o link do histórico. Nenhuma linha de código deve ser transcrita no arquivo Markdown.

**O que deve ser alterado no Framework:** A seção "Mandatory Changelog Structure" dentro de `FCVW/VERSIONING.md` precisará ser atualizada, convertendo a atual lista simples de "Affected Files" em uma nova subseção governada chamada "Affected Files & Stats", registrando a proibição formal de *diffs* literais.
