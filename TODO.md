# TODO — Plano de correção, simplificação e otimização do FCVW

> Análise do branch `main` em V0.19.0 (commit `fdca53b`), feita em 2026-09-25 e revisada
> criticamente no mesmo dia (seção 13).
> Este arquivo é um backlog de trabalho, não uma política. **Cada caixa de seleção do
> roadmap (seção 11) é um pacote de trabalho e vira um plano** `fcvw/plan@2` (ou compacto,
> quando P4/P5-R1), conforme o [AGENTS.md](AGENTS.md). Um plano por item de ID geraria
> cerca de 90 planos, o que contradiz o objetivo de simplificar.

## 0. Linha de base e método

| Verificação | Resultado |
|---|---|
| Suíte `python -B -m unittest discover -s tools -p 'test_*.py'` | 305 testes **OK** no Linux com Python **3.10, 3.11, 3.12 e 3.13** (~11 s cada) |
| Versão mínima de Python (`vermin tools/`) | **3.10** |
| `python -B tools/validate_fcvw.py --root . --profile clean-template` | 0 findings (antes deste arquivo) |
| Repositório e issues | público; 0 issues abertas |
| Tamanho de `FCVW/` | 228 arquivos, 65 diretórios |

**Método:** leitura das políticas, das skills e das ferramentas em `tools/`, com
**reprodução em cópias descartáveis** dos itens marcados como *Confirmado*. Os itens
marcados como *Inspeção* vêm da leitura do código e ainda não foram reproduzidos. As
metas de redução da seção J foram **simuladas por script** sobre a árvore real.

**Efeito colateral deste arquivo:** o validador rejeita `TODO.md` na raiz, com duas
ocorrências: `clean-contamination`, por estar fora de `CLEAN_ROOT_ENTRIES`, e
`document-catalog-stale`, porque os `.md` da raiz entram no grafo. Além disso, o
empacotador copiaria o arquivo para `FCVW/TODO.md` no pacote instalado. Antes do merge,
escolha uma opção: (a) manter o backlog fora do `main` ou convertê-lo em planos em
`FCVW/Plans/pending/`; ou (b) adicionar `TODO.md` a `CLEAN_ROOT_ENTRIES`
(`tools/path_policy_fcvw.py`) e a `SOURCE_ONLY_ROOT_FILES`
(`tools/release_layout_fcvw.py`) e regenerar o `DOCUMENT_GRAPH`.

Legenda: **Prioridade** P1–P5 e **Risco** R1–R5 seguem o [PLANNING.md](FCVW/PLANNING.md).

---

## 1. Resumo executivo

| # | Tema | Itens ativos | Mais grave |
|---|---|---|---|
| A | Falhas (bugs) | 9 | A-01: o upgrade sobrescreve edições locais em silêncio |
| B | Gatilhos que podem **não** disparar | 8 (+2 resolvidos por G-03) | B-01: plano novo com `fcvw/plan@1` escapa de todo o controle de regressão |
| C | Gatilhos disparados **por engano** | 6 (+3 resolvidos por G-03/J) | C-01: editar um profile do projeto dispara `event:policy` (~110 KB de leitura obrigatória) |
| D | Contradições entre documentos | 7 (+3 absorvidos) | D-03: a ADR-0001 promete "sem runtime", mas o fluxo obrigatório exige Python |
| E | Redundâncias | 6 (+2 absorvidos) | E-01: validadores de registro quase idênticos (~390 linhas) |
| F | Overengineering | 6 (+2 em J, 1 removido) | F-01: ~1.400 LOC de camada adaptativa/loop desativada |
| G | Otimizações | 7 (+1 movido para J) | G-03: trocar heurísticas de roteamento por declaração explícita |
| **J** | **Redução de arquivos e pastas** (objetivo central) | 1 decisão + 15 + 3 guardas | simulação: **228 → 106 arquivos, 65 → 28 diretórios** |
| H | Vault Obsidian "supercérebro" (nova capacidade) | 12 | H-05: gate de ativação por tokens e qualidade |

**Ordem de execução:**

1. **Fase 1 — integridade:** bugs A e B críticos, mais a medição da linha de base.
2. **Fase 2 — redução:** J, F e E.
3. **Fase 3 — gatilhos:** B, C, G e D, já sobre a estrutura reduzida.
4. **Fase 4 — operação.**
5. **Fase 5 — vault H.**

A redução vem **antes** do ajuste de gatilhos porque o `CONTEXT_MAP` e as heurísticas citam arquivos que a seção J funde; na ordem inversa, o trabalho seria feito duas vezes. O balanço de complexidade está na seção 12.

---

## 2. A — Falhas confirmadas ou prováveis

### A-01 · `upgrade_fcvw.py` sobrescreve customizações locais sem conflito — P1-R5 · *Confirmado*

- **Evidência:** `tools/upgrade_fcvw.py:53-61` (`load_manifest`) reconstrói o manifesto a partir da árvore **atual** quando `FCVW/ROLE_MANIFEST.json` não existe. Com isso, o digest "instalado" é igual ao digest local e nenhuma edição é detectada. O [AGENTS.md:97](AGENTS.md) manda rodar `role_manifest_fcvw.py --write` "após adicionar, mover ou remover qualquer arquivo governado", o que regrava o baseline com os digests já modificados.
- **Reprodução:** instalação materializada → `role_manifest --write` → edição de `FCVW/PLANNING.md` → o upgrade reporta `CONFLICT` (correto). Depois de regenerar o manifesto como o AGENTS.md manda, reporta `REPLACE … safe to replace`. Sem manifesto, também reporta `REPLACE`.
- **Correção (a forma mais simples que resolve):**
  1. O manifesto **distribuído no pacote** é o baseline e **nunca é regenerado** no projeto. `role_manifest_fcvw.py --write` passa a recusar sobrescrever um manifesto existente quando o layout é instalado.
  2. Remover a instrução do AGENTS.md (incorpora o antigo D-01). Arquivos criados pelo projeto não precisam de papel no manifesto: o upgrade já os preserva quando estão ausentes no upstream.
  3. Sem baseline, o upgrade entra em **modo seguro**: todo arquivo substituível e divergente vira `conflict`, nunca `replace`.
  4. `--apply` copia o manifesto da versão aplicada, que passa a ser o novo baseline.
- **Aceite:** teste de regressão com os três cenários (manifesto original, manifesto regenerado e ausência de manifesto), todos exigindo `conflict`.

### A-02 · `validate_fcvw.py --since` esconde links quebrados e filas inconsistentes — P2-R3 · *Confirmado*

- **Evidência:** `REPOSITORY_WIDE_RULES` (`tools/validate_fcvw.py:942`) lista `queue` e `plan-queue`, mas as regras reais se chamam `plan-queue-stale`, `plan-queue-missing`, `plan-queue-entry` etc. Também ficam de fora `document-link`, `document-orphan`, `document-unreachable`, `knowledge-*`, `plan-dependency-*`, `framework-index` e `markdown-link`. Além disso, `validate_markdown` só lê os arquivos do escopo e não verifica links **para** arquivos removidos.
- **Reprodução:** remover `FCVW/troubleshooting/2026-07-27-…md` e regenerar o `DOCUMENT_GRAPH`. A validação completa dá **6 erros**; com `--since HEAD~2`, **0 erros** (`scoped_out=3`).
- **Correção:** marcar o escopo no próprio `Finding` (`scope="repository"|"file"`) em vez de manter uma lista de nomes. Sempre avaliar os links de entrada de arquivos removidos ou renomeados. Incluir no escopo os arquivos não rastreados (`git status --porcelain`).
- **Aceite:** testes com arquivo removido, renomeado, novo não rastreado e fila obsoleta, todos falhando com `--since`.

### A-03 · Chaves duplicadas em `LOCALIZED_TITLES` descartam aliases — P3-R2 · *Confirmado*

- **Evidência:** `tools/validate_fcvw.py:405`. As chaves `"validation"` e `"rollback"` aparecem duas vezes; o Python mantém só a última. Somem `validation plan`, `plano de validacao`, `rueckabwicklung`, `zuruckrollen` e `reversion`.
- **Correção imediata:** mesclar os conjuntos e adicionar um teste com stdlib (`ast`) que proíba chaves duplicadas em literais (ver G-04). A correção definitiva é a remoção desses dicionários do código-fonte (B-05/F-04).

### A-04 · Falso positivo "completed plan has pending regression evidence" — P3-R2 · *Inspeção*

- **Evidência:** `tools/validate_fcvw.py:1133` usa `re.search(r"\bpending\b", section)` em toda a seção *Regression impact*. Citar `Plans/pending/` ou "no pending items" bloqueia a conclusão.
- **Correção:** procurar apenas valores de resultado (células de tabela ou `result: pending`), ignorando código inline.

### A-05 · `FILESYSTEM.md` diz ser "generated", mas não existe gerador — P3-R2 · *Inspeção*

- **Evidência:** `artifact_role: generated` e `upgrade_strategy: regenerate`, mas nenhuma ferramenta o gera. A lista é manual e já está incompleta (falta `tools/test_trace_fcvw.py`, por exemplo).
- **Correção:** **não** criar um gerador. Fundir as regras e os globs no `OWNERSHIP.md` e eliminar a lista de arquivos (J-09).

### A-06 · O backup `.local` do upgrade é sobrescrito sem aviso — P3-R3 · *Inspeção*

- `tools/upgrade_fcvw.py:156`: um segundo `--accept-conflicts` sobrescreve o `.local` anterior. **Correção:** recusar quando o `.local` já existe.

### A-07 · A saída JSON do upgrade sempre informa `"applied": false` — P4-R1 · *Inspeção*

- `tools/upgrade_fcvw.py:194`: o JSON é impresso antes do apply. **Correção:** emitir o JSON depois do apply, com os valores reais.

### A-08 · Arquivos removidos no upstream nunca são removidos nem sinalizados como bloqueio — P3-R3 · *Inspeção*

- O verdict `removed` é ignorado pelo `apply_upgrade`. Políticas obsoletas continuam instaladas, roteadas e validadas. **Correção:** exigir `--prune`, que remove apenas os arquivos cujo digest ainda é igual ao do baseline e reporta os demais como `conflict`. Essa correção é necessária para que a redução J chegue às instalações existentes.

### A-09 · Os templates de plano falham na validação do próprio framework — P4-R1 · *Inspeção*

- **Evidência:** nem `TEMPLATE_PLAN.md` nem `TEMPLATE_PLAN_COMPACT.md` trazem `record_scope`. No repositório do framework, `validate_clean_template` exige `record_scope: framework`, então um plano copiado do template gera `clean-contamination`. Em projetos de aplicação, que usam o perfil `instantiated`, o problema não ocorre.
- **Correção:** incluir `record_scope: "<application|framework>"` nos dois templates.

---

## 3. B — Gatilhos que podem **não** disparar (falsos negativos)

### B-01 · Plano novo com `fcvw/plan@1` escapa de todo o controle — P1-R4 · *Confirmado*

- **Evidência:** `PLAN_SCHEMAS` aceita `fcvw/plan@1` (`validate_fcvw.py:131`), e as regras de regressão e de risco retornam cedo para qualquer schema diferente de `plan@2` (linhas 1097 e 1156).
- **Reprodução:** um plano **P1-R5** em `pending/` com `context_files: [FCVW/SECURITY.md]`, sem corpo, sem *Regression impact* e sem *Rollback*, recebe **0 findings**.
- **Correção:** aceitar `plan@1` somente com `status` `completed` ou `discontinued` (os 3 registros históricos). Em `pending/` e `in_progress/`, exigir `plan@2` ou `plan-compact@1`.

### B-02 · Registro de troubleshooting sem `schema` não é validado — P2-R3 · *Confirmado*

- `validate_fcvw.py:1641` (`if not schema: continue`). No perfil `instantiated`, onde a checagem de contaminação não roda, um registro sem frontmatter passa limpo. **Correção:** todo `.md` em `troubleshooting/` exige `fcvw/troubleshooting@1` ou uma entrada no baseline legado.

### B-03 · `regression-surface` ignora arquivos ausentes em silêncio — P4-R1 · *Confirmado, com mitigação*

- **Evidência:** `validate_fcvw.py:1869` faz `continue` quando o arquivo não existe. **Na prática,** remover `WATCHERS.md` ainda gera 3 erros indiretos (links e `context_files` quebrados), então a detecção depende de referências incidentais.
- **Correção:** tornar a ausência um finding explícito, usando a lista única de caminhos obrigatórios (E-04).

### B-04 · A descoberta de políticas e skills usa *substring* — P3-R2 · *Inspeção*

- `path.name not in fcvw_index` (linha 1350), `name not in catalog` (linha 1318) e `` f"`{session_type}`" not in context ``: `AI.md` casa com `XAI.md`, a skill `QA` casa com qualquer "QA" do texto, e um tipo de sessão pode aparecer só na prosa. **Correção:** extrair os links e as células de tabela (o `document_graph_fcvw` já faz isso) e comparar de forma exata.

### B-05 · O contrato de corpo das skills é permissivo demais — P3-R2 · *Inspeção*

- **Evidência:** `heading.startswith(marker)` (linha 1329) com **46 aliases em inglês e 126 traduções**, várias de tradução automática sem sentido (`## schecks`, `## puertas duras`, `## schopfungstor`). `## Modifications` satisfaz "use conditions" através do prefixo `## modi`.
- **Correção (junto com F-04):** no código-fonte, **um cabeçalho canônico em inglês por conceito**, com igualdade exata. As variantes traduzidas recebem os aliases gerados pelo empacotador a partir da tradução revisada (ver F-04).

### B-06 · `event:filesystem` não dispara para arquivos não-Markdown — P2-R3 · *Inspeção*

- `tools/context_routing_fcvw.py:68` só adiciona `filesystem` para `.md`. Adicionar ou remover `.py`, JSON, imagens ou `.cursorrules` não carrega `OWNERSHIP.md`, embora a tabela diga *"Add, move, rename, generate, or delete a file/directory"*. **Correção:** qualquer `add|delete|move|rename` dispara `filesystem`.

### B-07 · Instruções de IA não disparam `event:ai` — P2-R3 · *Inspeção*

- `AGENTS.md` dispara só `policy`, e `.cursorrules` e `.windsurfrules` não disparam nada. **Correção:** incluir esses três arquivos em `ai` e em `policy`.

### B-08 · Heurísticas de `security` e `data` quase nunca casam em código real — *resolvido por G-03*

- Exigem nome **exatamente** igual a `auth`, `security`, `permissions`, `migrations` ou `database`; não casam `auth_service.py`, `oauth.py`, `.env*`, `db/`, `*.sql` nem `alembic/`. Em vez de ampliar a lista (o que aumenta o risco de falso positivo e a complexidade), G-03 remove a adivinhação semântica.

### B-09 · `public_interface` nunca dispara para código de aplicação — *resolvido por G-03*

- A regra só olha `.py` sob `tools/`. O mesmo raciocínio de B-08 se aplica: `public_interface` passa a ser um evento declarado.

### B-10 · As ADRs (`fcvw/adr@1`) não têm schema documentado nem validação — P3-R2 · *Inspeção*

- 9 ADRs usam `fcvw/adr@1`, mas `SCHEMAS.md` não tem essa seção e o validador só checa `record_scope`. O título da ADR-0001 diverge entre o arquivo, o H1 e o catálogo. **Correção:** documentar o schema (validado pela tabela declarativa de E-01) e alinhar os títulos.

---

## 4. C — Gatilhos disparados **por engano** (falsos positivos)

### C-01 · Qualquer `FCVW/*.md` dispara `event:policy`, inclusive profiles do projeto — P2-R2 · *Confirmado*

- **Evidência:** `context_routing_fcvw.py:70` (`path.count("/") == 1`). Um typo corrigido em `FCVW/SECURITY.md` numa sessão `documentation` gera 11 leituras obrigatórias, **~110 KB (~27 mil tokens estimados)**, incluindo `SCHEMAS.md` (25 KB) e `AUDIT.md`.
- **Correção:** decidir pelo `artifact_role` do frontmatter (`framework_policy` e `template` disparam `policy`; `project_profile` dispara só o evento do seu domínio). Essa correção independe da reorganização da seção J e pode ser antecipada para a Fase 1.

### C-02 · `SCHEMAS.md` dispara `event:data` — P3-R2 · *Inspeção*

- O stem `schemas` está na lista de `data` e carrega `DATA.md`, que no template limpo é placeholder. **Correção:** remover o stem (fica coberto pelo mapeamento por papel de C-01).

### C-03 · Qualquer arquivo em `.github/` dispara `event:automation` — P4-R1 · *Inspeção*

- `FUNDING.yml` carrega `AUTOMATION.md` e todos os contratos. **Correção:** disparar somente em `.github/workflows/**`.

### C-04 · `skills` e `memory` em código de aplicação disparam `event:ai` — *resolvido por G-03*

- `src/skills/` ou `memory.py` de um app carregam `AI.md` e `SECURITY.md`. A heurística fica restrita a `FCVW/skills/**` e às pontes de IA.

### C-05 · `trigger_keywords` ambíguos nas skills — P3-R2 · *Inspeção*

| Skill | Palavra-chave | Colisão |
|---|---|---|
| `git-conventional-commits` | `tag` | tags de frontmatter e da wiki |
| `project-instantiation` | `bootstrap` | o framework CSS Bootstrap |
| `agent-hephaestus` | `interface` | "public interface" (API) |
| `agent-hermes` | `optimize` | qualquer pedido de otimização |
| `obsidian-markdown` | `frontmatter` | toda edição de plano ou registro |
| `release-checklist` | `release` | leitura de release notes, `release_status` |
| `QA` | `QA` | sigla curta, casa com texto incidental |

- **Correção:** ver C-06.

### C-06 · `trigger_keywords` não são consumidos por nenhuma ferramenta — P3-R2 · *Inspeção*

- O campo é apenas exigido pelo validador; nenhuma ferramenta o lê. **Correção (simplificação):** torná-lo **opcional e depreciado** e fazer o `description` de cada skill carregar o gatilho no formato "Use quando… / Não use quando…", o mesmo usado pelos formatos de skill dos agentes. Isso dispensa um teste de colisão e adaptadores no core. Renomear as skills de nome mitológico (J-15) ajuda o disparo por nome.

### C-07 · "Declarative automation" carrega todos os contratos de automação — *resolvido por J-06*

- Com `HOOKS`, `WATCHERS`, `DAEMONS` e `GOVERNANCE_GATES` fundidos num `AUTOMATION.md` de ~8 KB, um único arquivo passa a ser lido e a regra "exactly one of" deixa de existir.

### C-08 · `MANGLED_DASH` pode acusar texto legítimo — P5-R1 · *Inspeção*

- `(?<=\w)\s\?\s(?=\w)` sinaliza "A ? B". **Correção:** ignorar código inline ou aplicar a checagem só a pacotes traduzidos.

### C-09 · `documentation` exige `FILESYSTEM.md` mesmo em uma edição simples — *resolvido por J-09*

- Com o `FILESYSTEM.md` fundido no `OWNERSHIP.md`, a linha passa a exigir só o `OWNERSHIP.md`, e apenas em movimentação de arquivo (via `event:filesystem`).

---

## 5. D — Contradições e deriva documental

| ID | Contradição | Evidência | Correção | P/R |
|---|---|---|---|---|
| D-01 | *Incorporado ao A-01* (instrução de regenerar o `ROLE_MANIFEST`) | — | — | — |
| D-02 | `wiki/index.md` é "generated" no `FCVW/README.md`, mas "preserved project profile" no `OWNERSHIP.md` e no frontmatter | `FCVW/README.md:55`, `OWNERSHIP.md:68` | Tirar da lista de gerados; continua project-owned (ver J-01) | P3-R2 |
| D-03 | A ADR-0001 promete "no required runtime dependency", mas o fluxo obrigatório exige Python para regenerar `QUEUE.md`, `DOCUMENT_GRAPH.md` e o manifesto | ADR-0001, AGENTS.md | **Resolvido pela redução:** J-03 (fila derivada), J-14 (sem catálogo versionado) e A-01 (sem regeneração do manifesto) tornam o validador de novo opcional. Registrar isso numa ADR curta | P2-R3 |
| D-04 | `FILESYSTEM.md` diz "No database", mas `adaptive_runtime_ledger_fcvw.py` usa `sqlite3` | `FILESYSTEM.md:164` | Some com F-01 e J-09 | P5-R1 |
| D-05 | O AGENTS.md alterna entre `FCVW/tools/` e `tools/` | AGENTS.md, seção final | Um único parágrafo sobre o prefixo; sem wrapper novo | P4-R1 |
| D-06 | A versão mínima de Python não é declarada | README, CI_CONTRACT | Declarar **3.10** (confirmado por `vermin` e pela suíte) | P4-R1 |
| D-07 | Fragmentos de fila com `artifact_role: project_profile` | `queue.d/README.md` | *Some com J-03* | — |
| D-08 | `CI_CONTRACT.md` foi aposentado, mas `TEMPLATE_CI_WORKFLOW.md` segue em `REQUIRED_PATHS` | `validate_fcvw.py:25` | Remover os dois; o histórico fica no git (J-12), salvo decisão contrária em G-05 | P3-R2 |
| D-09 | As pontes de provedor são uma linha genérica, e `.cursorrules` e `.windsurfrules` podem estar em formatos legados | `.cursorrules` | Verificar os formatos atuais; **não** criar pontes novas no core sem demanda real (redução) | P5-R1 |
| D-10 | O guia de refatoração pula de `02-` para `08-` | `refactoring-guide/` | *Some com J-07* | — |

---

## 6. E — Redundâncias

- **E-01 · Validadores de registro duplicados:** wiki, regressão, auditoria, troubleshooting e releases de aplicação somam ~390 linhas no mesmo padrão (campos, listas, enums, seções). **Proposta:** uma tabela declarativa `RECORD_SCHEMAS` em Python com um executor único (~150 linhas), mais um teste que confere se o `SCHEMAS.md` cita cada schema e campo. Não gerar a tabela a partir da prosa do `SCHEMAS.md`, porque esse parse seria frágil. — P3-R3
- **E-02 · Parser de *code fences* repetido:** aparece em `outside_code_fences`, `validate_markdown`, `level_two_section` e `document_graph_fcvw._outside_fences`, e a leitura da versão do `FRAMEWORK_LOCK` existe em dois lugares. **Proposta:** consolidar em `frontmatter_fcvw.py` ou `document_graph_fcvw.py`, sem criar módulo novo. — P3-R2
- **E-03 · Skills sobrepostas:** detalhado em **J-15**.
- **E-04 · Listas de caminhos obrigatórios em quatro lugares:** `REQUIRED_PATHS`, `REQUIRED_INSTALLED_PATHS`, `FILESYSTEM.md` e `required_content`. **Proposta:** uma lista única no arquivo existente `tools/path_policy_fcvw.py`, com os dois layouts. — P3-R2
- **E-05 · README raiz inchado e bilíngue à mão (745 linhas):** 6 seções "V0.1x — …" acumuladas no fim e o conteúdo duplicado em PT e EN sem checagem de paridade. **Proposta:** mover as novidades para `framework-releases/` e manter só o estado atual, nas duas línguas, no mesmo arquivo (sem criar `README.pt-BR.md`). A meta é chegar a menos de 350 linhas. Aplicar o mesmo corte às seções por versão do `FCVW/README.md`. — P3-R2
- **E-06 · *Incorporado a E-05.***
- **E-07 · `--optional-token-budget` e `--context-budget`** coexistem em `retrieve_context.py` com semânticas diferentes. **Proposta:** um único orçamento. — P4-R2
- **E-08 · Registros de contrato dentro de `governance/` (diretório de templates):** `CI_CONTRACT` é removido (D-08), `ADAPTIVE` e `LOOP` saem com F-01, e fica apenas `LOCAL_VALIDATION_CONTRACT.md`, aceito ali como exceção documentada. — P4-R1

---

## 7. F — Overengineering

| ID | Situação | Evidência | Proposta | P/R |
|---|---|---|---|---|
| F-01 | Camada adaptativa e de loop **desativada** ("current pilot does not qualify"): ~1.400 LOC de ferramentas (`adaptive_*`, `loop_*`, `trace`, `benchmark`), ~860 LOC de testes, 2 contratos de 13 KB, 1 template, 3 ADRs e 12 schemas `adaptive-*` / `loop-*` | `tools/`, `governance/`, ADR-0006/8/9 | Mover para um **repositório ou branch separado** e deixar no core apenas o roteamento determinístico. Antes, desacoplar `retrieve_context.py`, que tem flags `--adaptive-*`. As ADRs ficam como histórico, com uma ADR de supersessão | P2-R4 |
| F-02 | **55 schemas** `fcvw/*@N` distintos em uso, vários só para JSON descartável em cache | `SCHEMAS.md` | Documentar em `SCHEMAS.md` apenas os artefatos versionados (cerca de 20 após J); schemas de saída descartável vão para docstrings | P3-R3 |
| F-03 | `validate_fcvw.py` com **2.675 linhas / 113 KB** num framework que tem `anti-monolith-guard` | `tools/validate_fcvw.py` | **Primeiro reduzir** (E-01, F-04, B-05); dividir em módulos só se, depois disso, ainda passar de ~1.200 linhas. Dividir antes apenas espalharia a complexidade | P3-R3 |
| F-04 | Dicionários de tradução embutidos no validador: ~270 traduções mais 46 aliases em inglês nas linhas 229–540, parte deles de tradução automática | `validate_fcvw.py` | O **código-fonte valida só os cabeçalhos canônicos em inglês**. O empacotador, que já traduz as variantes, gera para cada variante um arquivo de aliases a partir da tradução revisada. São ~310 linhas a menos no core e nenhum arquivo novo no repositório | P3-R3 |
| F-05 | O histórico de desenvolvimento do framework (16 planos, ~160 KB, audits e 8 releases) é **distribuído no payload instalado** e se mistura aos planos da aplicação | `release_layout_fcvw.py`, `framework_history` | Excluir `record_scope: framework` do pacote, mantendo só a release note da versão atual (J-13) | P2-R3 |
| F-06 | Subdiretórios da wiki com README apenas | — | *Detalhado em J-01/J-02* | — |
| F-07 | 43 templates e 4 contratos em `governance/` | — | *Detalhado em J-06/J-07/J-12* | — |
| F-08 | Cerimônia desproporcional para mudanças triviais: plano, fila, changelog ou release record e ~110 KB de leitura | AGENTS.md "Required change flow" | Caminho "trivial" sem plano, com critérios estritos: apenas prosa, sem mexer em frontmatter, links, tabelas, código ou políticas `framework_policy`, e registrado no commit convencional. O compacto continua para o resto. Exige atualizar o AGENTS.md (R3) | P2-R3 |
| F-09 | ~~A suíte executa o pipeline completo aninhado~~ **Removido: afirmação incorreta.** As linhas repetidas vinham de passos simulados (`patch('check_fcvw.run_step')`) que imprimem no stdout; não há execução recursiva | — | Nenhuma ação | — |

---

## 8. G — Otimizações

- **G-01 · Orçamento de contexto medido:** registrar na Fase 1 a **linha de base** (bytes por rota de sessão e evento, com o método de estimativa), repetir a medição após as Fases 2 e 3 e publicar o resultado no `TOKEN_BUDGET` (que J-09 funde em `AI.md`). Teto de teste: edição de profile do projeto ≤ 40 KB. — P2-R2
- **G-02 · Rotas sem índice BM25:** hoje `retrieve_context.py` exige `--index` e `--query` mesmo para obter só as rotas obrigatórias. Tornar os dois opcionais (modo `--routes-only`) **no próprio arquivo**, sem criar uma ferramenta nova. — P3-R2
- **G-03 · Trocar heurísticas semânticas por declaração explícita (simplificação):** o CLI deixa de adivinhar `security`, `data`, `public_interface` e `ai` a partir de nomes de arquivos da aplicação. Mantém só o que é inequívoco: operações de arquivo (`filesystem`) e caminhos do próprio framework, classificados pelo `artifact_role` (C-01). Quando `--versioned-change` recebe arquivos de código sem nenhum evento semântico declarado, o CLI **avisa** e lista os eventos a considerar. Isso resolve B-08, B-09 e C-04 **removendo** código em vez de criar um motor de padrões configuráveis. — P2-R3
- **G-04 · Checagem estática sem dependência:** um teste com stdlib (`ast`) para chaves duplicadas, nomes não usados e imports mortos, que teria pegado o A-03. Usar `ruff` apenas como opção local, respeitando a ADR-0001 (zero dependência). — P4-R1
- **G-05 · CI hospedado (decisão do mantenedor):** o repositório é público, então os runners padrão do GitHub Actions são gratuitos. Porém, o `LOCAL_VALIDATION_CONTRACT` registra a decisão explícita de substituir o CI hospedado. **Não reativar sem nova autorização.** Se autorizado: um workflow mínimo (Linux/Windows/macOS × Python 3.10 e o mais recente) rodando `check_fcvw.py`, com actions fixadas por SHA e `contents: read`. — P3-R3
- **G-06 · Hook opcional de validação incremental** (`validate_fcvw.py --since HEAD`), documentado no `AUTOMATION.md` e **não versionado no core**. Depende de A-02. — P5-R2
- **G-07 · Evidência de plataforma:** registrar no próximo release record o que esta análise executou (Linux com Python 3.10 a 3.13, suíte OK) e reduzir os *Known gaps*; macOS continua não verificado. — P5-R1
- **G-08 · *Movido para J-14.***

---

## 9. H — Vault Obsidian indexado por YAML ("supercérebro" do projeto)

**Objetivo:** transformar a wiki, os registros de troubleshooting, as regras de negócio,
os fluxos de autenticação e o conhecimento sobre UI e código da aplicação num **vault
Obsidian único, indexado por frontmatter YAML**, que a IA consulta de forma seletiva e
mantém atualizado. Isso vale **somente se o consumo de tokens e a qualidade não
piorarem** (H-05).

**Princípios de desenho:**

1. Reaproveitar o que já existe, sem sistema paralelo.
2. O mínimo de schema novo.
3. **Nenhuma pasta ou arquivo novo no template limpo** além de um template de nota (coerente com J).

| Já existe | Papel no vault |
|---|---|
| `fcvw/wiki@1` com relações tipadas, `source_path`, `source_digest`, `derived_from` e o tipo `component` | Envelope YAML e notas de código (`type: component`) |
| Wiki de produto e skill [QA](FCVW/skills/QA/SKILL.md) (inventário e superfícies) | Notas de **UI**, sem tipo novo |
| `APP_RULES.md` (`APP-RULE-NNN`) | **Regras de negócio**, indexadas por âncora, sem duplicar |
| `troubleshooting/` (`fcvw/troubleshooting@1`, `type: failure`) | Falhas, que passam a participar do índice |
| `knowledge_graph_fcvw.py`, `build_context_index.py` e `retrieve_context.py` (BM25) | Grafo, índice e busca |
| Seções de validação dos planos | Evidência para o gate H-05, sem ferramenta nova |

### H-01 · Definir o vault e a estrutura — P3-R3

- A raiz do vault é `FCVW/`, porque `.obsidian/` já está no `.gitignore`. Registrar isso numa ADR curta.
- **Estrutura plana, sem pastas por tipo.** O tipo fica no YAML e no prefixo do `id`; o Obsidian filtra por propriedade.

  ```text
  FCVW/wiki/README.md      política da wiki: MEMORY + schema + taxonomia (framework, substituído no upgrade)
  FCVW/wiki/index.md       índice curado (project-owned, preservado)
  FCVW/wiki/<id>.md        notas: COMP-* (código), FLOW-* (fluxos, inclusive auth), conceitos, decisões, padrões…
  FCVW/troubleshooting/    falhas (local e schema atuais)
  .fcvw-cache/vault/       catálogos, métricas e índice gerados — descartáveis, não versionados
  ```

- A política (framework) e o índice (projeto) **ficam em arquivos separados** para não quebrar o modelo de upgrade (substituir × preservar).
- Uma subpasta só é criada se um tipo passar de ~50 notas, e sempre sem README.
- **Links:** o link Markdown relativo continua canônico; wikilinks são opcionais e nunca duplicam uma relação.

### H-02 · Extensão mínima do schema — P2-R3

- **Um tipo novo:** `flow` (fluxo ponta a ponta: UI → API → dados, inclusive autenticação e autorização). Código usa o tipo existente `component`, UI usa as páginas de produto do QA, e regras ficam no `APP_RULES`.
- **Três campos opcionais novos:** `summary` (até 280 caracteres), `symbols` (âncoras estáveis como `Classe.metodo`; nunca números de linha) e `sensitivity` (`public|internal|restricted`). O `source_path` e o `source_digest` já existentes passam a ser aceitos em `component` e `flow`.

```yaml
---
schema: "fcvw/wiki@1"
id: "COMP-billing-invoice-service"        # slug estável, permitido pela seção IDs do wiki/schema
type: "component"
title: "InvoiceService — emissão e cancelamento de faturas"
summary: "Emite, cancela e reemite faturas; valida o limite de crédito (APP-RULE-012) antes de emitir."
status: "validated"
confidence: "high"
sensitivity: "internal"
record_scope: "application"
retrieval_scope: "search_only"
source_path: "src/billing/invoice_service.py"
symbols: ["InvoiceService.issue", "InvoiceService.cancel"]
source_digest: "sha256:<digest do arquivo>"
last_checked: "2026-09-25"
implements: ["FCVW/APP_RULES.md#APP-RULE-012"]
depends_on: ["FLOW-billing-auth"]
tags: ["billing", "invoice"]
created_at: "2026-09-25"
last_reviewed: "2026-09-25"
sources: ["src/billing/invoice_service.py"]
---
```

- **Corpo curto:** *Propósito*, *Comportamento*, *Regras e permissões*, *Erros*, *Armadilhas*, *Links*.
- **Validador (pela tabela de E-01):** `summary` com até 280 caracteres, `source_path` existente, `symbols` encontrados no arquivo por busca textual e, em links para `APP_RULES.md#APP-RULE-NNN`, o ID existente no arquivo. Hoje o validador de relações descarta o fragmento `#…`, então ele precisa passar a conferi-lo.

### H-03 · Migrar a wiki e o troubleshooting existentes — P3-R2

- Os registros de troubleshooting ganham `summary` e passam a ser indexados pelo mesmo grafo e índice. Uma falha resolvida aparece quando alguém mexe no código ligado a ela.
- Script de migração **não destrutivo** (`--dry-run` por padrão, sem reescrever corpo), executado pelo mesmo mecanismo de migração da seção J, **sem ferramenta nova**.
- **Regras de negócio com uma única fonte:** o `APP_RULES.md` continua sendo o arquivo das regras e o vault apenas o indexa por âncora `APP-RULE-NNN`, e as notas apontam para a regra com `implements: ["FCVW/APP_RULES.md#APP-RULE-NNN"]`. Converter regras em notas separadas só se passarem de ~30 regras, e nunca manter as duas formas.
- Depende de B-02 e D-02.

### H-04 · Índice e catálogos gerados — P3-R2

- Estender `knowledge_graph_fcvw.py` e `build_context_index.py` para emitir, **em `.fcvw-cache/vault/` (não versionado)**, o catálogo por tipo (`id`, `title`, `summary`, `status`, desatualização) e a lista de notas desatualizadas.
- Opcional e versionado: **um** arquivo do Obsidian Bases (`.base`) com uma visão por tipo. Verificar o formato atual do Obsidian antes.
- O BM25 passa a pesar `title`, `summary`, `tags` e `symbols` acima do corpo.
- **Aceite:** geração determinística; nenhum arquivo gerado versionado, exceto o `.base` opcional.

### H-05 · Gate de ativação: tokens e qualidade não podem piorar — P1-R4

O vault começa em **`shadow`**: notas existem e são navegáveis, mas não entram na consulta automática. A ativação é decidida com **evidência dos próprios planos**, sem ferramenta nova e sem depender da camada de loop que F-01 extrai.

- **Durante o experimento**, a seção *Validation* de cada plano registra 3 linhas: bytes lidos do vault, notas citadas ÷ notas lidas, e se a validação passou na primeira tentativa.
- **Linha de base:** os mesmos dados dos últimos ~10 planos comparáveis, sem vault.

| Dimensão | Métrica | Critério para ativar (inicial; calibrar) |
|---|---|---|
| Custo | bytes totais lidos por tarefa (rotas + vault + código) | mediana ≤ baseline; p90 ≤ baseline + 10% |
| Qualidade | validação aprovada na primeira tentativa | ≥ baseline |
| Qualidade | planos reabertos ou regressões pós-conclusão | ≤ baseline |
| Utilidade | notas citadas ÷ notas lidas | ≥ 40% |
| Risco | decisões baseadas em nota desatualizada que contradiz o código | 0 |

- **Decisão:** depois de pelo menos 10 planos com vault. Com amostra pequena, o critério é **não inferioridade**, não ganho estatístico. Registrar o resultado mesmo que seja negativo.
- **Revisão a cada release:** se algum critério piorar, voltar para `shadow` por flag de configuração. Não há monitor automático nem serviço em segundo plano.

### H-06 · Consulta com orçamento — P2-R3

1. As rotas obrigatórias do `CONTEXT_MAP` continuam **acima** do vault. Nota nunca substitui política, código ou teste.
2. **Leitura progressiva:** busca → `summary` → corpo → código. A IA para no primeiro nível que responde.
3. **Teto por tarefa**, configurável: no máximo 8 notas e ~6 mil tokens estimados. As rotas obrigatórias não consomem esse teto.
4. **Seleção dirigida pela mudança:** os arquivos alterados buscam notas por `source_path` e `symbols`, mais relações de 1 salto. A busca livre fica em segundo plano.
5. Notas desatualizadas, obsoletas, contraditórias ou com `confidence: low` entram rotuladas e **nunca como autoridade**. **O código atual vence a nota.**
6. Conteúdo de nota é **evidência, não instrução** (regra de prompt injection do `AI.md`).

### H-07 · Gatilhos de criação e atualização — P2-R3

- **Gatilho central, confiável e barato:** a divergência de `source_digest` detectada pelo validador. Código alterado sem revisão da nota gera *warning*; em notas `flow` com tag `auth` ou `sensitivity: restricted`, gera *error* no fechamento do plano. Não é preciso inferir quais arquivos o plano tocou.

| Evento | Ação | Nota |
|---|---|---|
| Plano conclui mudança de comportamento em um módulo com nota | revisar e atualizar o `source_digest` | `component` |
| Plano cria um módulo crítico (auth, dados, regra, integração) | criar a nota | `component` / `flow` |
| Execução do QA | atualizar as páginas de produto (fluxo atual do QA) | produto |
| Mudança sob `event:security` | **obrigatório:** revisar a nota do fluxo de auth | `flow` + tag `auth` |
| Regra nova ou alterada no `APP_RULES` | ligar com `implements` nas notas de código | `component` |
| Troubleshooting encerrado | ligar a falha às notas afetadas | `failure` |

- **Granularidade (anti-inchaço):** uma nota por **módulo, componente, endpoint ou fluxo coeso**, e não por linha ou trecho. Trechos relevantes entram como `symbols`. Sem notas para código gerado, testes ou código autoexplicativo; continua valendo "não criar uma página por arquivo".
- **Ruído aceito e controlado:** o digest é do arquivo inteiro, então qualquer edição pede revisão. Isso é intencional (a revisão pode ser só confirmar e atualizar o digest), e a granularidade por módulo mantém o volume baixo.
- **Closeout:** o checklist do `AUDIT.md` ganha uma linha: "notas afetadas revisadas ou marcadas".

### H-08 · Segurança e privacidade do vault — P1-R4

- Notas de auth descrevem **fluxo, papéis, pontos de verificação e riscos**, e **nunca** segredos, tokens, senhas, chaves, URLs internas sensíveis ou dados pessoais.
- Varredura de padrões de segredo (chaves de API, JWT, `password=`, chaves privadas) em **todo Markdown governado**, não só no vault. Qualquer ocorrência bloqueia.
- `sensitivity: restricted` fica fora da consulta automática e só é lida com rota explícita (`event:security`).
- Nada é enviado a serviços externos; não há embeddings remotos.

### H-09 · Métricas de saúde (geradas em `.fcvw-cache/vault/metrics.json`) — P3-R2

Só métricas cujo denominador **já existe**, sem exigir novas declarações do projeto:

| Métrica | Definição | Alvo inicial |
|---|---|---|
| Frescor | notas com `source_digest` coerente ÷ notas com `source_path` | ≥ 95% |
| Cobertura de UI | superfícies do inventário do QA com página validada | ≥ 80% no escopo declarado |
| Cobertura de regras | `APP-RULE-NNN` referenciadas por pelo menos um `implements: …APP_RULES.md#APP-RULE-NNN` ÷ total de regras | ≥ 90% |
| Candidatos por churn (informativo) | arquivos mais alterados nos últimos 90 dias (`git log`) sem nota | lista, sem meta |
| Tamanho | p90 de bytes por nota | ≤ 6 KB |
| Utilidade | citadas ÷ lidas (H-05) e notas nunca lidas em 90 dias (candidatas a arquivamento) | tendência ascendente |

- Cobertura sem utilidade é sinal de inchaço e **não** justifica criar notas em massa.

### H-10 · Ciclo de vida e poda — P3-R2

- A skill de memória consolidada (J-15) desduplica por `source_path` e `symbols`, arquiva notas nunca lidas, consolida notas pequenas demais e resolve `contradicts`.
- Código removido torna a nota `obsolete`, com `superseded_by` quando houver substituto. Nenhuma nota é apagada sem registro.

### H-11 · Obsidian sem dependência obrigatória — P4-R2

- Tudo funciona em Markdown puro com YAML de primeiro nível (o parser do FCVW não aceita aninhamento). Dataview e outros plugins de terceiros ficam **fora** do core.
- A skill `obsidian-markdown` documenta as propriedades do vault: listas como listas e datas ISO.

### H-12 · Entrega incremental — P2-R3

1. **V0:** ADR, extensão do schema (H-02) e varredura de segredos (H-08).
2. **V1:** migração (H-03), catálogos (H-04) e métricas (H-09).
3. **V2:** gatilhos por digest (H-07) em modo *warning*.
4. **V3:** consulta em `shadow` com orçamento (H-06) e coleta do gate (H-05).
5. **V4:** ativação somente se o gate passar; senão, o vault continua como documentação navegável e o resultado é registrado.

**Rollback:** flag de volta para `shadow`, preservando as notas. Os campos novos são opcionais e retrocompatíveis.

---

## 10. J — Redução de arquivos e pastas vazios ou redundantes (objetivo central)

**Situação medida em `FCVW/`: 228 arquivos e 65 diretórios.**

- **26 diretórios contêm apenas um `README.md`** (a maioria entre 200 e 500 bytes, dizendo só "guarde X aqui").
- **11 profiles** estão só com placeholders (`instantiation_status: pending`).
- `governance/` tem **43 templates e 4 contratos**, dos quais 11 templates são de refatoração e 5 de automação.
- O guia de refatoração tem 18 arquivos.

**Meta (simulada por script sobre a árvore real):**

- **≤ 110 arquivos** (simulação: 106) e **≤ 30 diretórios** (simulação: 28).
- Destes, **≤ 10 diretórios fora de `skills/`**. Cada skill mantém o seu diretório (`skills/<nome>/SKILL.md`) por compatibilidade com o formato de skills dos agentes.
- **Nenhuma regra verificável pode ser perdida.**

**Regra geral:** diretório nasce **sob demanda**, na primeira escrita de um registro real, nunca com um README de scaffolding. O "o que guardar aqui" mora na política dona do assunto.

### J-D · Decisão prévia: como registros ficam navegáveis sem READMEs de catálogo — P2-R3

Hoje a regra do AGENTS.md exige que todo Markdown governado seja alcançável a partir de um ponto de entrada ou de um catálogo. Os READMEs de diretório e o `DOCUMENT_GRAPH.md` (20 KB, gerado e fonte de conflitos de merge) existem para cumprir essa regra. **Proposta:**

- Políticas e templates continuam exigindo link a partir de um ponto de entrada.
- **Registros** (planos, ADRs, auditorias, troubleshooting, releases, notas) passam a cumprir a regra por **estarem num diretório canônico de registros** e por terem **link de saída** para a fonte autoritativa, que já é exigido.
- O validador calcula a alcançabilidade diretamente, sem catálogo versionado. O Obsidian oferece explorador, grafo e backlinks.

J-08, J-11 e J-14 dependem desta decisão. Sem ela, a alternativa é manter o `DOCUMENT_GRAPH.md` gerado como único catálogo (−1 item de economia, porém ainda eliminando todos os READMEs).

| ID | Consolidação | Arquivos | Dirs | P/R |
|---|---|---|---|---|
| J-01 | **Wiki plana:** remover os 20 subdiretórios que só contêm README. O conteúdo real de `feedback/` (regras append-only), `agents/`, `qa/`, `sources/` e `regressions/` vai para `wiki/README.md`, e **o validador passa a selecionar pelo `type`, não pela pasta** (hoje `validate_feedback_notes` lê `wiki/feedback/`). `schema.md` e `taxonomy.md` também vão para `wiki/README.md`; `log.md` sai (o `git log` é o log); `metrics.md` vai para o cache; `product/README.md` (8 KB) vai para `skills/QA/`. O `index.md` **continua separado** porque é project-owned | −24 (+1 movido) | −21 | P2-R3 |
| J-02 | **Templates de wiki:** 15 → 1 `governance/TEMPLATE_NOTE.md` com o envelope YAML e blocos opcionais por `type`. Os 3 templates de produto vão para `skills/QA/` | −12 | −1 | P3-R2 |
| J-03 | **Fila derivada:** `category`, `order`, `blocked_by` e `override_reason` vão para o frontmatter do plano (cada plano continua sendo um arquivo, então não há conflito de merge). A fila é calculada por `plan_queue_fcvw.py`, ou manualmente, lendo o frontmatter dos planos em `in_progress/` e `pending/`. Remove os 2 `queue.d/`, os 2 `QUEUE.md` e a classe inteira de erros "fila obsoleta" | −4 | −2 | P2-R4 |
| J-04 | **READMEs de estado de plano:** 4 → 0 (o `PLANNING.md` já descreve os estados). `pending/`, `in_progress/` e `discontinued/` são criados sob demanda | −4 | −3 | P3-R3 |
| J-05 | **Profiles:** `MANIFEST`, `SCOPE`, `STACK`, `ENVIRONMENT`, `DESIGN`, `PERFORMANCE`, `WORKFLOW` e as respostas do `BRIEFING` → **`PROJECT.md`**. O questionário vai para a skill `project-instantiation`. **`SECURITY.md`, `DATA.md` e `APP_RULES.md` continuam separados:** são alvos de gatilhos obrigatórios e da regra `SENSITIVE_CONTEXT_FILES`, e fundi-los aumentaria os tokens de toda rota de segurança ou dados. O status por seção usa listas de primeiro nível (`complete_sections: […]`, `not_applicable_sections: […]`), já que o parser não aceita aninhamento. As rotas passam a apontar para seções (`section_hints` já existe) | −7 | 0 | P2-R4 |
| J-06 | **Automação:** `AUTOMATION`, `HOOKS`, `WATCHERS`, `DAEMONS` e `GOVERNANCE_GATES` (~8,8 KB no total) → `AUTOMATION.md` com uma seção por `kind`, e os 4 templates específicos → o template de contrato existente. Custo: +3 a 5 KB apenas em tarefas de automação, que são raras | −8 | 0 | P3-R3 |
| J-07 | **Refatoração:** `refactoring-guide/` (18 arquivos, com a lacuna 03–07) e os 10 `TEMPLATE_REFACTORING_*` → seções do `REFACTORING.md` + o `TEMPLATE_REFACTORING.md` existente | −28 | −1 | P3-R2 |
| J-08 | **READMEs de catálogo** de `decisions/`, `troubleshooting/`, `audits/` e `framework-releases/`. Não fundir as listas nas políticas: o `ARCHITECTURAL_DECISIONS.md` é framework-owned, e links adicionados pelo projeto seriam sobrescritos no upgrade (depende de J-D) | −4 | 0 | P3-R2 |
| J-09 | **Políticas sobrepostas:** `VERSIONING` → `RELEASE` (sempre lidos juntos); `RETROACTIVE_INSTANTIATION` → `INSTANTIATION` (dois modos); `FILESYSTEM` → `OWNERSHIP` (lidos juntos em `event:filesystem`; resolve A-05); `MEMORY` → `wiki/README.md`; `TOKEN_BUDGET` → seção do `AI.md`, **não** do `CONTEXT_MAP`, que é lido em toda sessão e cresceria para todo mundo | −5 | 0 | P3-R3 |
| J-10 | **Exemplos:** `examples/` (4 arquivos) → um bloco "exemplo preenchido" dentro dos templates de plano | −4 | −2 | P4-R2 |
| J-11 | **Diretórios de registro vazios:** `briefings/` e `changelogs/unreleased/` são criados pela primeira escrita (as ferramentas fazem `mkdir -p`) | −2 | −3 | P4-R2 |
| J-12 | **Templates restantes:** os 5 de documentação de aplicação → `TEMPLATE_APP_DOC.md`; proposta de skill + relatório de self-improvement → 1; `AI_RESOURCE` e `AI_SESSION_SYNTHESIS` → tipos do `TEMPLATE_NOTE`; `CODE_HYGIENE_REPORT` e `MONOLITH_GATE` → seções do template de refatoração; `BRIEFING` → skill; `CI_WORKFLOW` e `CI_CONTRACT` são removidos (D-08) | −12 (+2 novos) | 0 | P3-R2 |
| J-13 | **Fora do payload instalado:** histórico do framework (F-05) e camada adaptativa/loop (F-01). Afeta o **pacote**, não a contagem da fonte | ~−40 no pacote | — | P2-R4 |
| J-14 | **`DOCUMENT_GRAPH.md` fora do versionamento** (antigo G-08), gerado em `.fcvw-cache/` quando alguém quiser. Depende de J-D | −1 | 0 | P3-R3 |
| J-15 | **Skills (antigo E-03):** `agnix-linter` + `wiki-lint` → `governance-validator`; `aicc-compact` + `memory-rotation` → `wiki-curator`. Renomear as skills de nome opaco: `agent-aegis` → `security-review`, `agent-hephaestus` → `ui-review`, `agent-hermes` → `performance-review` (feito via `self-improvement` e `agent-factory`) | −4 | −4 | P3-R3 |
| F-01 | Contratos e template adaptativos/loop saem de `governance/` | −3 | 0 | P2-R4 |

**Guardas contra o recrescimento** (instaladas ao fim da Fase 2, quando já passam):

- **J-G1:** no perfil `clean-template`, diretório sob `FCVW/` que contém só `README.md` vira finding.
- **J-G2:** o release record registra arquivos, diretórios e bytes de `FCVW/`. Um teste falha se o total crescer mais de 5% sem justificativa no plano, transformando em regra a pergunta "What is removed in exchange?" do `PLANNING.md`.
- **J-G3:** cada `schema` versionado tem no máximo um template, e cada template tem um schema; o validador cruza os dois.

**Cuidados obrigatórios:**

- **Nenhum registro é apagado:** em projetos instalados, o upgrade (com `--prune`, A-08) **move** notas e registros para os novos caminhos, a partir de uma tabela caminho antigo → novo em `MIGRATIONS.md`, sempre com `--dry-run` primeiro. Por isso a Fase 1 (A-01 e A-08) precede a Fase 2.
- **Prova de que nenhuma regra se perdeu:** antes da Fase 2, inventariar os IDs de regra emitidos pelo validador (mais de 80) e garantir uma fixture negativa por regra. Depois da redução, cada ID continua com fixture que falha, ou foi removido com justificativa no plano. Isso é necessário porque boa parte dos 305 testes referencia caminhos que vão mudar e precisará ser reescrita.
- Atualizar juntos: `REQUIRED_PATHS` (na lista única de E-04), rotas do `CONTEXT_MAP.md`, inferência de papéis do `role_manifest_fcvw.py`, empacotamento das 4 variantes de idioma e links.
- **Uma consolidação por plano**, sempre com a suíte verde antes da próxima.

---

## 11. Roadmap

### Fase 1 — Integridade e linha de base (patch V0.19.1)

- [ ] Medir a linha de base: arquivos, diretórios e bytes de `FCVW/`, bytes por rota (G-01) e inventário de IDs de regra com fixtures
- [ ] A-01 + A-08 Upgrade: manifesto distribuído como baseline, modo seguro e `--prune` (**P1-R5**, plano expandido, rollback ensaiado)
- [ ] B-01 + B-02 Plano `plan@1` só em histórico; troubleshooting sem schema vira finding
- [ ] A-02 Escopo de `--since`
- [ ] A-03 + G-04 Chaves duplicadas e teste estático com stdlib
- [ ] C-01 Roteamento de `FCVW/*.md` por `artifact_role` (economia imediata de tokens)
- [ ] A-04, A-06, A-07, A-09 Correções pontuais

**Aceite:** cada bug tem um teste que falha no estado atual e passa após a correção; suíte e validador verdes.

### Fase 2 — Redução (minor V0.20.0; exige migração)

- [ ] J-D Decisão sobre navegabilidade de registros (ADR)
- [ ] F-01 + F-05/J-13 Camada adaptativa/loop e histórico do framework fora do core e do pacote
- [ ] J-01 + J-02 Wiki plana e template único de nota
- [ ] J-03 + J-04 Fila derivada do frontmatter; READMEs de estado removidos
- [ ] J-05 `PROJECT.md` (mantendo `SECURITY`, `DATA` e `APP_RULES` separados)
- [ ] J-06 + J-07 + J-12 Templates e políticas de automação e refatoração consolidados
- [ ] J-08 + J-09 + J-10 + J-11 + J-14 READMEs de catálogo, políticas sobrepostas, exemplos, diretórios vazios e `DOCUMENT_GRAPH`
- [ ] J-15 Skills fundidas e renomeadas
- [ ] E-01 + E-02 + E-04 + F-04 + B-05 Validador enxuto (tabela declarativa, aliases fora do código-fonte, lista única de caminhos); F-03 só se ainda necessário
- [ ] F-02 `SCHEMAS.md` restrito aos artefatos versionados (D-04 some junto com F-01 e J-09)
- [ ] J-G1 + J-G2 + J-G3 Guardas contra o recrescimento

**Aceite:** `FCVW/` com ≤ 110 arquivos e ≤ 30 diretórios (≤ 10 fora de `skills/`); cada ID de regra do inventário continua com fixture que falha, ou foi removido com justificativa; uma instalação V0.19.0 migrada sem perda (digests dos registros conferidos).

### Fase 3 — Gatilhos e documentos, sobre a nova estrutura (minor V0.21.0)

- [ ] G-03 Remover a adivinhação semântica e avisar quando faltar evento (resolve B-08, B-09 e C-04)
- [ ] B-06 + B-07 + C-02 + C-03 + C-08 Correções pontuais de roteamento
- [ ] B-04 + B-03 Comparação exata e superfícies obrigatórias explícitas
- [ ] C-05 + C-06 `trigger_keywords` opcional; gatilho no `description`
- [ ] B-10 Schema de ADR
- [ ] G-01 + G-02 Medir de novo contra a linha de base; modo `--routes-only`
- [ ] F-08 Caminho trivial sem plano (atualiza o AGENTS.md)
- [ ] D-02, D-03 (ADR), D-05, D-06, D-08, D-09 + E-05, E-07, E-08 Alinhamento documental e READMEs enxutos

**Aceite:** tabela de casos caminho → eventos (framework e app típico) testada; edição de profile do projeto ≤ 40 KB de leitura obrigatória; bytes por rota **menores ou iguais** à linha de base da Fase 1 em todas as rotas.

### Fase 4 — Operação contínua

- [ ] G-05 CI hospedado somente com nova autorização do mantenedor
- [ ] G-06 Hook opcional (não versionado no core)
- [ ] G-07 Evidência de plataforma no release record

### Fase 5 — Vault "supercérebro" (depois da Fase 2, já na estrutura plana)

- [ ] H-01 + H-02 + H-08 ADR, extensão mínima do schema e varredura de segredos
- [ ] H-03 + H-04 + H-09 Migração, catálogos em cache e métricas
- [ ] H-07 + H-10 + H-11 Gatilhos por digest, poda e propriedades Obsidian
- [ ] H-06 + H-05 Consulta em `shadow` com orçamento e coleta do gate nos planos
- [ ] H-12 Ativação condicionada ao gate

**Aceite:** gate H-05 registrado com os números brutos; ativação só se todos os critérios passarem; rollback para `shadow` testado.

---

## 12. Balanço de complexidade (o plano de fato simplifica?)

Estimativas, a confirmar pelas medições das Fases 1 a 3:

| Área | Remove | Adiciona | Resultado esperado |
|---|---|---|---|
| Arquivos em `FCVW/` (J, simulado) | −130 | +8 (fusões e movimentações) | **228 → 106** |
| Diretórios em `FCVW/` (J, simulado) | −37 | 0 | **65 → 28** (10 fora de `skills/`) |
| Pacote instalado (J-13) | ~−40 arquivos, ~−300 KB de histórico e experimentos | — | instalação menor e sem histórico alheio |
| Ferramentas: camada adaptativa/loop (F-01) | ~−1.400 LOC + ~860 LOC de testes | — | core menor |
| Validador: aliases de tradução (F-04/B-05) | ~−310 linhas | ~+50 no empacotador | |
| Validador: registros declarativos (E-01) | ~−390 linhas | ~+150 | |
| Roteamento (G-03) | heurísticas semânticas | aviso de evento ausente | menos falsos positivos e negativos |
| Correções A/B | — | ~+250 LOC + testes | integridade |
| Vault (H) | — | 1 tipo, 3 campos, varredura de segredos, métricas: ~+300 LOC; 1 template | capacidade nova, **em `shadow` até o gate** |
| Artefatos gerados versionados | `DOCUMENT_GRAPH`, 2 `QUEUE.md`, `wiki/log`, `wiki/metrics`, `FILESYSTEM` | — | menos conflitos de merge; a ADR-0001 volta a valer |
| Leitura obrigatória (edição de profile) | ~110 KB | — | meta ≤ 40 KB |

**Saldo estimado nas ferramentas:** cerca de −1.500 a −2.000 LOC (sem contar os testes da camada extraída). A única área que cresce é o vault, que é opcional, fica em `shadow` e depende de um gate medido.

---

## 13. Riscos, cuidados e histórico de revisão

- A-01, A-08, J-03, J-05 e F-05 mexem no upgrade e no conteúdo instalado: exigem plano **expandido**, backup e ensaio de rollback numa instalação real anterior.
- Mudanças em `CONTEXT_MAP.md`, `AGENTS.md` e skills disparam `event:ai` e `event:policy`: reexecutar os casos de fronteira (permitido, negado, ambíguo, injeção) de [TESTS.md](FCVW/TESTS.md).
- Consolidar documentos traduzidos exige regenerar e revisar as 4 variantes de idioma. Planeje a Fase 2 junto com a revisão linguística.
- O vault (H) é o item com maior risco de **piorar** tokens e qualidade (inchaço, nota desatualizada tratada como verdade, vazamento de dados de auth). Por isso nasce em `shadow`, com teto de orçamento, código acima da nota e gate medido.
- Nenhum item autoriza, por si só, a implementação: cada pacote passa pelo fluxo de plano do [AGENTS.md](AGENTS.md).

**Revisão crítica aplicada (2026-09-25):**

- **Corrigido (erros factuais):**
  - F-09 removido: não havia execução aninhada da suíte.
  - Números de F-01 corrigidos (~1.400 LOC, e não 2.700), além de F-02, F-04 e da contagem de templates.
  - B-03 rebaixado: a remoção é detectada indiretamente.
  - A-09 ampliado aos dois templates de plano.
  - D-06 confirmado (3.10).
  - Meta de diretórios de J corrigida (≤ 20 era inviável com 22 skills; a simulação dá 28).
- **Corrigido (incoerências internas):**
  - J-01 fundia uma política do framework com o índice do projeto no mesmo arquivo, o que quebraria o upgrade.
  - J-08 mandava fundir catálogos em políticas substituíveis no upgrade.
  - J-09 aumentava o `CONTEXT_MAP`, que é lido em toda sessão.
  - J-05 fundia `SECURITY` e `DATA`, alvos de gatilhos obrigatórios.
  - G-08 e J brigavam pela navegação; agora a decisão fica em J-D.
  - H-05 dependia da camada que F-01 extrai.
  - D-01 duplicava A-01.
  - As fases ajustavam os gatilhos antes de reorganizar os arquivos.
- **Simplificado (propostas que adicionavam complexidade):**
  - Heurísticas configuráveis viraram declaração explícita (G-03).
  - Teste de colisão de keywords virou campo depreciado (C-06).
  - A ferramenta nova de rotas virou uma flag (G-02).
  - O gerador de `FILESYSTEM` virou fusão com o `OWNERSHIP` (A-05).
  - O `ruff` virou um teste com stdlib (G-04).
  - Os 6 tipos novos do vault viraram 1 tipo e 3 campos (H-02).
  - As pastas por tipo e os catálogos versionados do vault viraram estrutura plana e cache (H-01/H-04).
  - O monitor automático do gate virou revisão por release (H-05).
  - A obrigação de um plano por item virou um plano por pacote do roadmap.
- **Condicionado a decisão do mantenedor:** CI hospedado (G-05), porque contraria uma decisão registrada.
