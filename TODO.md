# TODO — Plano de correção, simplificação e otimização do FCVW

> Análise do branch `main` em V0.19.0 (commit `fdca53b`), feita em 2026-09-25.
> Este arquivo é um backlog de trabalho, não uma política. Cada item deve virar um
> plano `fcvw/plan@2` (ou compacto, quando P4/P5-R1) antes de ser implementado,
> conforme [AGENTS.md](AGENTS.md).

## 0. Linha de base e método

| Verificação | Resultado |
|---|---|
| `python -B -m unittest discover -s tools -p 'test_*.py'` | 305 testes, **OK** (Linux, Python 3.11.15, ~11 s) |
| `python -B tools/validate_fcvw.py --root . --profile clean-template` | 0 findings (antes deste arquivo) |
| Issues abertas no GitHub | 0 |

Método: leitura de `AGENTS.md`, `CONTEXT_MAP.md`, `PLANNING.md`, `OWNERSHIP.md`,
`FILESYSTEM.md`, `TESTS.md`, `REGRESSION_GUARDS.md`, `TOKEN_BUDGET.md`, das skills e
das ferramentas em `tools/`, com **reprodução em cópias descartáveis** dos defeitos
marcados como *Confirmado*. Os demais itens foram obtidos por inspeção do código ou dos
documentos e estão marcados como *Inspeção*.

Observação: o Linux não constava como plataforma testada nos *Known gaps* da V0.19.0.
A suíte passou aqui, então esse gap pode ser reduzido (ver G-07).

**Efeito colateral deste arquivo:** o validador rejeita `TODO.md` na raiz, com duas
ocorrências: `clean-contamination`, por estar fora da allowlist `CLEAN_ROOT_ENTRIES`, e
`document-catalog-stale`, porque os `.md` da raiz entram no grafo. Além disso, o
empacotador copiaria o arquivo para `FCVW/TODO.md` no pacote instalado. Antes de fazer
merge, escolha uma das opções: (a) manter o backlog fora do `main` ou convertê-lo em
planos em `FCVW/Plans/pending/`; ou (b) adicionar `TODO.md` a `CLEAN_ROOT_ENTRIES`
(`tools/path_policy_fcvw.py`) e a `SOURCE_ONLY_ROOT_FILES`
(`tools/release_layout_fcvw.py`) e regenerar o `DOCUMENT_GRAPH`.

Legenda: **Prioridade** P1–P5 e **Risco** R1–R5 seguem o [PLANNING.md](FCVW/PLANNING.md).

---

## 1. Resumo executivo

| # | Tema | Itens | Mais grave |
|---|---|---|---|
| A | Falhas (bugs) | 9 | A-01: o upgrade sobrescreve edições locais em silêncio |
| B | Gatilhos que podem **não** disparar | 10 | B-01: plano novo com `fcvw/plan@1` escapa de todo o controle de regressão |
| C | Gatilhos disparados **por engano** | 9 | C-01: editar um profile do projeto dispara `event:policy` (~110 KB de leitura obrigatória) |
| D | Contradições entre documentos | 10 | D-01: AGENTS.md manda regenerar um arquivo que está no `.gitignore` |
| E | Redundâncias | 8 | E-01: três validadores de registro quase idênticos |
| F | Overengineering | 9 | F-01: ~2.700 LOC de camada adaptativa/loop que está desativada |
| G | Otimizações | 8 | G-01: custo de contexto obrigatório para mudanças triviais |
| H | Vault Obsidian "supercérebro" (nova capacidade) | 12 | H-05: gate de ativação por tokens e qualidade |
| J | **Redução de arquivos e pastas vazios ou redundantes** | 13 + 3 guardas | J-01: 20 pastas da wiki que só contêm um README |

Ordem sugerida de execução: **Fase 1 (A + B críticos) → Fase 2 (C + D) → Fase 3 (J + E + F) → Fase 4 (G) → Fase 5 (H, vault)**. O vault vem **depois** da redução J, para nascer já na estrutura plana. Detalhes na seção 11.

---

## 2. A — Falhas confirmadas ou prováveis

### A-01 · `upgrade_fcvw.py` sobrescreve customizações locais sem conflito — P1-R5 · *Confirmado*

- **Evidência:** `tools/upgrade_fcvw.py:53-61` (`load_manifest`) reconstrói o manifesto a partir da árvore **atual** quando `FCVW/ROLE_MANIFEST.json` não existe. Com isso, o digest "instalado" é igual ao digest local e nenhuma edição local é detectada. O [AGENTS.md:97](AGENTS.md) manda rodar `role_manifest_fcvw.py --write` "após adicionar, mover ou remover qualquer arquivo governado", o que regrava o baseline com os digests já modificados.
- **Reprodução:** instalação materializada → `role_manifest --write` → edição de `FCVW/PLANNING.md` → o upgrade reporta `CONFLICT` (correto). Depois de regenerar o manifesto como o AGENTS.md manda, o mesmo upgrade reporta `REPLACE … safe to replace`. Sem manifesto, também reporta `REPLACE`.
- **Correção:**
  1. Separar o **baseline de instalação** (digests do pacote, imutável, gravado só pelo instalador/upgrade) do **inventário de papéis** (regenerável). Exemplo: `FCVW/ROLE_MANIFEST.json` com `installed_digest` preservado e `current_digest` recalculado.
  2. Sem baseline, `upgrade` deve cair em modo seguro: todo arquivo substituível e divergente vira `conflict`, nunca `replace`.
  3. `--apply` deve regravar o baseline com os digests da versão aplicada (hoje não regrava, e o upgrade seguinte vê conflitos falsos).
  4. Remover a instrução do AGENTS.md ou trocá-la por "atualize apenas os papéis; nunca o baseline".
- **Aceite:** teste de regressão que cobre os três cenários (com manifesto, manifesto regenerado, sem manifesto) exigindo `conflict`.

### A-02 · `validate_fcvw.py --since` esconde links quebrados e filas inconsistentes — P2-R3 · *Confirmado*

- **Evidência:** `REPOSITORY_WIDE_RULES` (`tools/validate_fcvw.py:942`) contém `queue` e `plan-queue`, mas as regras reais se chamam `plan-queue-stale`, `plan-queue-missing`, `plan-queue-entry` etc. Também ficam de fora `document-link`, `document-orphan`, `document-unreachable`, `knowledge-*`, `plan-dependency-*`, `framework-index` e `markdown-link`. Além disso, `validate_markdown` só lê os arquivos do escopo, então não verifica links **para** um arquivo removido.
- **Reprodução:** remover `FCVW/troubleshooting/2026-07-27-…md` e regenerar o `DOCUMENT_GRAPH`. A validação completa dá **6 erros**; `--since HEAD~2` dá **0 erros** (`scoped_out=3`).
- **Correção:** trocar a lista de nomes por um atributo `scope="repository"|"file"` no próprio `Finding`, ou por prefixos (`plan-queue-`, `document-`, `knowledge-`, `plan-dependency-`). Sempre avaliar links de entrada dos arquivos removidos ou renomeados. Incluir arquivos não rastreados (`git status --porcelain`) e não-Markdown no escopo.
- **Aceite:** teste com arquivo removido, arquivo renomeado, arquivo novo não rastreado e fila obsoleta, todos falhando com `--since`.

### A-03 · Chaves duplicadas em `LOCALIZED_TITLES` descartam aliases — P3-R2 · *Confirmado*

- **Evidência:** `tools/validate_fcvw.py:405`. As chaves `"validation"` e `"rollback"` aparecem duas vezes; o Python mantém só a última. Somem `validation plan`, `plano de validacao`, `rueckabwicklung`, `zuruckrollen` e `reversion`.
- **Efeito:** um plano compacto com `## Validation plan` ou `## Plano de validação` é rejeitado, e um plano alemão com `## Rückabwicklung` também.
- **Correção:** mesclar os conjuntos. Adicionar um teste (ou `ruff` com a regra `F601`) que detecte chaves duplicadas em literais.

### A-04 · Falso positivo "completed plan has pending regression evidence" — P3-R2 · *Inspeção*

- **Evidência:** `tools/validate_fcvw.py:1133` usa `re.search(r"\bpending\b", section)` em toda a seção *Regression impact*. Citar `Plans/pending/`, `release_status: pending` ou "no pending items" bloqueia a conclusão.
- **Correção:** procurar apenas valores de resultado, como células de tabela ou marcadores `result: pending` / `| pending |`, fora de código inline.

### A-05 · `FILESYSTEM.md` diz ser "generated", mas não existe gerador — P3-R2 · *Inspeção*

- **Evidência:** `artifact_role: generated` e `upgrade_strategy: regenerate`, mas nenhuma ferramenta o gera. A lista é manual, cresce por seção de versão e já está incompleta (falta, por exemplo, `tools/test_trace_fcvw.py`). `last_reviewed: 2026-08-21`.
- **Correção:** criar um gerador (derivado do `ROLE_MANIFEST`) **ou** reclassificar como `framework_policy` e reduzir o conteúdo a regras e globs, sem lista de arquivos.

### A-06 · O backup `.local` do upgrade é sobrescrito sem aviso — P3-R3 · *Inspeção*

- **Evidência:** `tools/upgrade_fcvw.py:156`. Um segundo `--accept-conflicts` sobrescreve o `.local` anterior, e a customização original se perde.
- **Correção:** usar backup com timestamp ou recusar quando o `.local` já existe. Excluir `*.local` do manifesto e do grafo.

### A-07 · A saída JSON do upgrade sempre informa `"applied": false` — P4-R1 · *Inspeção*

- **Evidência:** `tools/upgrade_fcvw.py:194`. O JSON é impresso antes do apply e nunca é atualizado.
- **Correção:** emitir o JSON depois do apply, com `applied` e `files_applied` reais.

### A-08 · Arquivos removidos no upstream nunca são removidos nem sinalizados como bloqueio — P3-R3 · *Inspeção*

- **Evidência:** o verdict `removed` é ignorado pelo `apply_upgrade`. Políticas e ferramentas obsoletas continuam instaladas e ainda são validadas e roteadas.
- **Correção:** mover para `FCVW/.retired/<versão>/` (ou exigir `--prune`) e registrar isso no relatório do upgrade.

### A-09 · O template compacto falha na validação do próprio framework — P4-R1 · *Inspeção*

- **Evidência:** `FCVW/governance/TEMPLATE_PLAN_COMPACT.md` não traz `record_scope`. No repositório do framework, `validate_clean_template` exige `record_scope: framework` em todo plano, então um plano copiado do template gera `clean-contamination`.
- **Correção:** incluir `record_scope: "<application|framework>"` no template e documentar o campo em `SCHEMAS.md`.

---

## 3. B — Gatilhos que podem **não** disparar (falsos negativos)

### B-01 · Plano novo com `fcvw/plan@1` escapa de todo o controle — P1-R4 · *Confirmado*

- **Evidência:** `PLAN_SCHEMAS` aceita `fcvw/plan@1` (`validate_fcvw.py:131`). `validate_plan_regression` e `validate_plan_risk_binding` retornam cedo quando o schema não é `plan@2` (linhas 1097 e 1156).
- **Reprodução:** um plano **P1-R5** em `pending/` com `context_files: [FCVW/SECURITY.md]`, sem corpo, sem *Regression impact* e sem *Rollback*, recebe **0 findings**.
- **Correção:** aceitar `plan@1` apenas em `completed/` e `discontinued/` e com `created_at` anterior à data de corte da V0.13; em `pending/` e `in_progress/`, exigir `plan@2` ou `plan-compact@1`.

### B-02 · Registro de troubleshooting sem `schema` não é validado — P2-R3 · *Confirmado*

- **Evidência:** `validate_fcvw.py:1641` (`if not schema: continue`). No perfil `instantiated`, onde a checagem de contaminação não roda, um registro sem frontmatter passa limpo.
- **Correção:** todo `.md` em `troubleshooting/` (exceto o README) exige `fcvw/troubleshooting@1`, ou um baseline legado explícito.

### B-03 · `regression-surface` ignora arquivos ausentes — P2-R3 · *Inspeção*

- **Evidência:** `validate_fcvw.py:1869` (`if not path.is_file(): continue`). `TESTS.md`, `GOVERNANCE_GATES.md` e `WATCHERS.md` não estão em `REQUIRED_PATHS`. Remover um deles elimina a própria verificação.
- **Correção:** um arquivo ausente vira finding, e a lista de `REQUIRED_PATHS` deve ser derivada do `ROLE_MANIFEST` (ver E-04).

### B-04 · A descoberta de políticas e skills usa *substring* — P3-R2 · *Inspeção*

- **Evidência:** `path.name not in fcvw_index` (linha 1350), `name not in catalog` (linha 1318) e `` f"`{session_type}`" not in context ``. `AI.md` casa com qualquer `XAI.md`, e a skill `QA` casa com qualquer "QA" do catálogo. O tipo de sessão pode estar só na prosa, fora das tabelas.
- **Correção:** extrair links e células de tabela (o `document_graph_fcvw` já faz isso) e comparar caminhos e identificadores exatos.

### B-05 · O contrato de corpo das skills é permissivo demais — P3-R2 · *Inspeção*

- **Evidência:** `heading.startswith(marker)` (linha 1329) com mais de 150 aliases, vários de tradução automática sem sentido (`## schecks`, `## puertas duras`, `## schopfungstor`, `## bestellung prufen`). `## modi` satisfaz "use conditions", e `## Modifications` também passa.
- **Correção:** um cabeçalho canônico por conceito **em inglês**, mais uma tradução revisada por idioma, com igualdade exata. Remover os aliases de tradução automática.

### B-06 · `event:filesystem` não dispara para arquivos não-Markdown — P2-R3 · *Inspeção*

- **Evidência:** `tools/context_routing_fcvw.py:68` só adiciona `filesystem` para `.md`. Adicionar ou remover `tools/*.py`, imagens, JSON ou `.cursorrules` não dispara a leitura de `OWNERSHIP.md` e `FILESYSTEM.md`, embora a tabela diga *"Add, move, rename, generate, or delete a file/directory"*.
- **Correção:** qualquer `add|delete|move|rename` dispara `filesystem`, independentemente da extensão.

### B-07 · Instruções de IA não disparam `event:ai` — P2-R3 · *Inspeção*

- **Evidência:** `AGENTS.md`, `.cursorrules` e `.windsurfrules` só disparam `policy` (ou nada). A tabela diz que `event:ai` cobre *"AI instruction, prompt, skill, agent…"*.
- **Correção:** incluir as pontes de provedor e o `AGENTS.md` na heurística de `ai`. Os mesmos arquivos devem disparar `policy`.

### B-08 · Heurísticas de `security` e `data` quase nunca casam em código real — P2-R3 · *Inspeção*

- **Evidência:** exige diretório ou stem **exatamente** igual a `auth`, `security`, `permissions`, `migrations`, `database`. Não casam `auth_service.py`, `login/`, `oauth.py`, `rbac.py`, `secrets.*`, `.env*`, `migration/`, `db/`, `*.sql`, `alembic/`, `prisma/schema.prisma` nem `models.py`.
- **Correção:** trocar por padrões configuráveis, com tokens em qualquer parte do nome e uma lista de extensões, declarados num bloco do `CONTEXT_MAP.md` (e não hard-coded) para o projeto instanciado ajustar. Manter o aviso de que a heurística é conservadora e o host deve declarar o evento semântico.

### B-09 · `public_interface` nunca dispara para código de aplicação — P3-R2 · *Inspeção*

- **Evidência:** a regra só olha `.py` sob um diretório `tools`. APIs (`openapi.*`, `routes/`, `api/`, `*.proto`, `schema.graphql`, `cli.*`) nunca disparam.
- **Correção:** separar as heurísticas do framework (`tools/*_fcvw.py`) das heurísticas de aplicação, com padrões configuráveis como em B-08.

### B-10 · As ADRs (`fcvw/adr@1`) não têm schema documentado nem validação — P3-R2 · *Inspeção*

- **Evidência:** 9 ADRs usam `fcvw/adr@1`, mas `SCHEMAS.md` não tem essa seção e o validador só checa `record_scope`. A ADR-0001 também diverge no título: arquivo "pure-markdown-over-automation-scripts", H1 "Markdown-first baseline", catálogo "Pure Markdown over automation scripts".
- **Correção:** documentar `fcvw/adr@1` e validar `id`, `status` (`proposed|accepted|superseded|deprecated`), `date` e as seções mínimas. Alinhar os títulos.

---

## 4. C — Gatilhos disparados **por engano** (falsos positivos)

### C-01 · Qualquer `FCVW/*.md` dispara `event:policy`, inclusive profiles do projeto — P2-R2 · *Confirmado*

- **Evidência:** `context_routing_fcvw.py:70` (`path.count("/") == 1`). Corrigir um typo em `FCVW/SECURITY.md` numa sessão `documentation` gera 11 leituras obrigatórias, **~110 KB (~27 mil tokens estimados)**, incluindo `SCHEMAS.md` (25 KB) e `AUDIT.md`.
- **Correção:** decidir pelo `artifact_role` do frontmatter (`framework_policy`, `template`, validador) e não pela profundidade do caminho. Um `project_profile` dispara apenas o evento do seu domínio.

### C-02 · `SCHEMAS.md` dispara `event:data` — P3-R2 · *Inspeção*

- **Evidência:** o stem `schemas` está na lista de `data`. `SCHEMAS.md` descreve artefatos do framework, não dados da aplicação, então a regra carrega `DATA.md`, que no template limpo ainda é placeholder.
- **Correção:** remover `schemas` do conjunto de `data`, ou restringir a regra a caminhos fora de `FCVW/`.

### C-03 · Qualquer arquivo em `.github/` dispara `event:automation` — P4-R1 · *Inspeção*

- **Evidência:** `FUNDING.yml` e templates de issue carregam `AUTOMATION.md` e **todos** os contratos (HOOKS, WATCHERS, DAEMONS, GATES), embora o `CONTEXT_MAP` peça "exactly one".
- **Correção:** disparar só em `.github/workflows/**`, `.gitlab-ci.yml`, `.pre-commit-config.yaml`, `.husky/**` e `Jenkinsfile`, e escolher o contrato pelo tipo.

### C-04 · `skills` e `memory` em código de aplicação disparam `event:ai` — P3-R2 · *Inspeção*

- **Evidência:** `"skills" in parts` e `stem in {"ai","memory"}`. Um app de RH com `src/skills/` ou um módulo `memory.py` de cache carrega `AI.md` e `SECURITY.md`.
- **Correção:** restringir a `FCVW/skills/**` e às pontes de IA, com padrões configuráveis no projeto.

### C-05 · `trigger_keywords` ambíguos nas skills — P3-R2 · *Inspeção*

| Skill | Palavra-chave problemática | Colisão |
|---|---|---|
| `git-conventional-commits` | `tag` | tags de frontmatter e da wiki |
| `project-instantiation` | `bootstrap` | o framework CSS Bootstrap, scripts de bootstrap |
| `agent-hephaestus` | `interface` | "public interface" (API), que é outro domínio |
| `agent-hermes` | `optimize` | qualquer pedido de otimização (inclusive de governança) |
| `obsidian-markdown` | `frontmatter` | toda edição de plano ou registro |
| `release-checklist` | `release` | leitura de release notes, `release_status` |
| `QA` | `QA` | sigla curta, casa com texto incidental |

- **Correção:** keywords compostas ("git tag", "bump version", "ui accessibility review") e uma tabela de colisões verificada por teste (ver C-06).

### C-06 · `trigger_keywords` não são consumidos por nenhuma ferramenta — P3-R2 · *Inspeção*

- **Evidência:** o campo só é exigido pelo validador. Nenhum roteador o usa, e as skills em `FCVW/skills/` não são descobertas automaticamente por hosts que leem `.claude/skills/`, `.cursor/rules/` etc.
- **Correção:** (a) testar colisões entre skills (mesma keyword em duas skills sem tipo de sessão compartilhado vira finding); (b) opcionalmente, gerar adaptadores de provedor fora do core (ver D-09).

### C-07 · "Declarative automation" carrega todos os contratos de automação — P4-R1 · *Inspeção*

- **Evidência:** o aviso do `resolve_routes` diz *"Automation loads every named contract"*, contrariando a tabela ("exactly one of").
- **Correção:** subeventos `event:automation:hook|watcher|daemon|gate`.

### C-08 · `MANGLED_DASH` pode acusar texto legítimo — P5-R1 · *Inspeção*

- **Evidência:** `(?<=\w)\s\?\s(?=\w)` sinaliza "A ? B", como em operadores ternários citados fora de crase ou em pesquisas "sim ? não".
- **Correção:** restringir a pacotes de release traduzidos ou ignorar código inline.

### C-09 · `documentation` exige `FILESYSTEM.md` mesmo em uma edição simples — P4-R1 · *Inspeção*

- **Evidência:** a linha *Documentation / file movement* carrega `OWNERSHIP.md` e `FILESYSTEM.md` para qualquer edição de documento, embora `event:filesystem` já cubra criação, movimentação e remoção.
- **Correção:** dividir a linha em "Documentation edit", com leitura mínima, e "File movement".

---

## 5. D — Contradições e deriva documental

| ID | Contradição | Evidência | Correção | P/R |
|---|---|---|---|---|
| D-01 | O AGENTS.md manda regenerar e versionar `FCVW/ROLE_MANIFEST.json`, mas o arquivo está no `.gitignore` e só é gerado pelo packager | `AGENTS.md:97`, `.gitignore` | Instrução condicional ("somente em instalação") e corrigir A-01 | P2-R3 |
| D-02 | `wiki/index.md` é "generated / regenerate" no `FCVW/README.md`, mas "preserved project profile" no `OWNERSHIP.md` e no frontmatter | `FCVW/README.md:55`, `OWNERSHIP.md:68` | Tirar o arquivo da lista de gerados | P3-R2 |
| D-03 | A ADR-0001 promete "no required runtime dependency", mas o fluxo obrigatório (AGENTS.md) exige Python para regenerar `QUEUE.md`, `DOCUMENT_GRAPH.md` (20 KB) e o manifesto | ADR-0001, AGENTS.md | Nova ADR que substitua a 0001 e assuma "Python ≥ 3.x stdlib" **ou** torne os gerados opcionais | P2-R3 |
| D-04 | `FILESYSTEM.md` diz "No database, service or collector", mas `adaptive_runtime_ledger_fcvw.py` usa `sqlite3` | `FILESYSTEM.md:164`, `ledger:8,44` | Corrigir o texto ("SQLite local opcional em `.fcvw-cache`") | P4-R1 |
| D-05 | O AGENTS.md usa `python FCVW/tools/...` (caminho instalado) e só às vezes lembra o equivalente em `tools/` no checkout-fonte | AGENTS.md, seção final | Um único parágrafo sobre o prefixo, ou um wrapper `fcvw` que resolva o caminho | P4-R1 |
| D-06 | A versão mínima de Python não é declarada; releases citam 3.12/3.14, mas o código roda em 3.11 | README, CI_CONTRACT | Declarar a mínima (ex.: 3.10, por causa de `X \| Y` em runtime) e testá-la | P3-R2 |
| D-07 | Os fragmentos de fila usam `artifact_role: project_profile`, mas não são profiles (são registros operacionais) | `Plans/*/queue.d/README.md` | Papel `record` ou um papel `queue_entry` dedicado | P4-R2 |
| D-08 | `CI_CONTRACT.md` foi aposentado, mas `TEMPLATE_CI_WORKFLOW.md` continua em `REQUIRED_PATHS` e os textos mencionam "repository CI" | `validate_fcvw.py:25`, `FILESYSTEM.md` | Decidir: reativar o CI (G-05) ou retirar e arquivar o template | P3-R2 |
| D-09 | As pontes de provedor são uma linha genérica. `.cursorrules` e `.windsurfrules` são formatos legados nesses editores, e não há ponte para outros hosts (ex.: `CLAUDE.md`, `.github/copilot-instructions.md`, `GEMINI.md`) | `.cursorrules` | Revisar os formatos atuais de cada provedor e gerar pontes opcionais fora do core | P4-R2 |
| D-10 | O guia de refatoração pula de `02-` para `08-` (faltam 03–07) | `FCVW/refactoring-guide/` | Renumerar ou documentar a lacuna no `MANIFEST.md` do guia | P5-R1 |

---

## 6. E — Redundâncias

- **E-01 · Validadores de registro duplicados** (`validate_wiki_ids`, `validate_audit_records`, `validate_troubleshooting_records`, regressão, releases de aplicação). Somam cerca de 500 linhas com o mesmo padrão: campos escalares, listas, enums, seções. **Proposta:** uma tabela declarativa `RECORD_SCHEMAS = {schema: {required, lists, enums, sections, id_pattern}}` e um único executor. É possível derivar essa tabela do próprio `SCHEMAS.md`, para ter uma única fonte de verdade. — P3-R3
- **E-02 · Mesmo código repetido em vários lugares:** o parser de *code fences* aparece três vezes (`outside_code_fences`, `validate_markdown`, `level_two_section`) e também em `document_graph_fcvw._outside_fences`. A leitura da versão no `FRAMEWORK_LOCK` existe em `validate_version` e em `role_manifest.installed_version`. **Proposta:** um módulo `markdown_fcvw.py` com utilitários compartilhados. — P3-R2
- **E-03 · Três skills de lint** (`agnix-linter`, `governance-validator`, `wiki-lint`) e **três de memória** (`aicc-compact`, `memory-rotation`, `wiki-curator`) com fronteiras sobrepostas. **Proposta:** fundir em `governance-lint` (modo wiki opcional) e `memory-curation` (handoff, rotação e promoção). — P3-R3
- **E-04 · Listas de arquivos obrigatórios em quatro lugares:** `REQUIRED_PATHS`, `REQUIRED_INSTALLED_PATHS`, `FILESYSTEM.md` e o `required_content` de `validate_regression_surfaces`. **Proposta:** uma fonte única (manifesto de papéis com a flag `required: true`). — P3-R2
- **E-05 · Seções por versão acumuladas nos índices:** o `README.md` raiz (745 linhas) tem 6 seções "V0.1x — …" no fim, além do conteúdo bilíngue duplicado; `FCVW/README.md` tem "V0.18.0 retrieval quality"; `FILESYSTEM.md` tem seções por feature. **Proposta:** mover novidades para `framework-releases/` e deixar nos índices apenas o estado atual. — P3-R2
- **E-06 · README bilíngue mantido à mão**, sem checagem de paridade PT/EN. **Proposta:** README curto em inglês com link para `README.pt-BR.md` (ou o inverso), e uma checagem de paridade de cabeçalhos. — P4-R2
- **E-07 · `--optional-token-budget` e `--context-budget`** coexistem em `retrieve_context.py` com semânticas diferentes (excerpt × JSON serializado). **Proposta:** um único orçamento, com a estimativa documentada. — P4-R2
- **E-08 · Dois registros de "CI"** (`CI_CONTRACT.md` aposentado e `LOCAL_VALIDATION_CONTRACT.md`) ficam em `governance/`, o diretório de templates, embora sejam registros. **Proposta:** movê-los para `decisions/` ou `audits/`, ou para um diretório `contracts/`. — P4-R2

---

## 7. F — Overengineering

| ID | Situação | Evidência | Proposta | P/R |
|---|---|---|---|---|
| F-01 | Camada adaptativa e de loop **desativada por padrão** e sem piloto qualificado ("current pilot does not qualify"), com cerca de 2.700 LOC de ferramentas, 1.200 LOC de testes, 2 contratos de 13 KB, 3 ADRs e 12 schemas `adaptive-*` / `loop-*` | `adaptive_*_fcvw.py`, `loop_*_fcvw.py`, `ADAPTIVE_EXPERIMENT_CONTRACT.md`, ADR-0006/8/9 | Mover para um pacote **opcional separado** (`fcvw-labs`), fora do payload instalado. O core mantém só o roteamento determinístico | P2-R4 |
| F-02 | **57 schemas** `fcvw/*@N`, vários só para JSON descartável em `.fcvw-cache` | `SCHEMAS.md` | Manter em `SCHEMAS.md` apenas os artefatos versionados; schemas de saída descartável vão para docstrings | P3-R3 |
| F-03 | `validate_fcvw.py` com **2.675 linhas / 113 KB** num framework que tem a skill `anti-monolith-guard` | `tools/validate_fcvw.py` | Dividir em pacote `fcvw_validate/` (plans, records, releases, graph, profiles, i18n) com CLI fino | P3-R3 |
| F-04 | Dicionários de tradução (~250 entradas) embutidos no validador para aceitar cabeçalhos em 4 idiomas | `validate_fcvw.py:229-600` | Mover os aliases para um arquivo de dados por idioma no pacote de release, ou exigir cabeçalhos canônicos em inglês (com o texto do corpo traduzido) | P3-R3 |
| F-05 | O histórico de desenvolvimento do framework (16 planos, cerca de 165 KB, audits e 8 releases) **é distribuído dentro do payload instalado** e se mistura aos planos da aplicação em `Plans/completed/` | `release_layout_fcvw.py`, `role_manifest` (`framework_history`) | Excluir `record_scope: framework` do pacote instalado, deixando só as release notes da versão atual | P2-R3 |
| F-06 | 22 subdiretórios de `wiki/`, 20 deles só com README no template limpo (`agents`, `prompts`, `raw`, `inbox`, `syntheses`…) | `FCVW/wiki/*/README.md` | Detalhado em **J-01/J-02** | P3-R2 |
| F-07 | 47 templates de governança, 11 deles só de refatoração, além de 18 arquivos do guia de refatoração (71 KB) | `FCVW/governance/`, `FCVW/refactoring-guide/` | Detalhado em **J-06/J-07/J-12** | P3-R2 |
| F-08 | Cerimônia desproporcional para mudanças triviais: plano, fragmento de fila, changelog ou release record, regeneração de 3 artefatos e ~110 KB de leitura (C-01) | AGENTS.md "Required change flow" | Caminho "trivial" (P5-R1, só texto) sem plano: apenas o commit convencional, com o validador aceitando esse caminho | P2-R3 |
| F-09 | A suíte de testes executa o pipeline local completo aninhado (os testes chamam `check_fcvw`, que roda os testes de novo) | saída do `unittest` com "1: governance: pass" repetido | Marcar os testes end-to-end como opt-in (`FCVW_E2E=1`) e manter a suíte unitária rápida | P4-R2 |

---

## 8. G — Otimizações

- **G-01 · Orçamento de contexto:** medir e publicar em `TOKEN_BUDGET.md` o custo real, em bytes e com o método de estimativa, de cada rota de sessão e evento. Definir um teto (ex.: ≤ 40 KB para `documentation`) e testar esse teto na suíte. Depende de C-01, C-09 e F-02. — P2-R2
- **G-02 · CLI de roteamento independente:** hoje `retrieve_context.py` exige `--index` e `--query` mesmo para obter só as rotas obrigatórias. Criar `route_fcvw.py --session X --file-change modify:PATH`, sem índice BM25. — P3-R2
- **G-03 · Configuração do roteamento no projeto:** padrões de caminho por evento declarados num bloco do `CONTEXT_MAP.md` (ou em `APP_RULES.md`) e lidos por `context_routing_fcvw.py` (base de B-08, B-09, C-03 e C-04). — P2-R3
- **G-04 · Linter estático:** adicionar `ruff` (ou `python -m pyflakes`) como checagem local opcional. Teria pegado A-03 (F601). — P4-R1
- **G-05 · CI gratuito:** GitHub Actions é gratuito para repositórios públicos. Reativar um workflow mínimo (Linux/Windows/macOS × Python mínimo/atual) rodando `check_fcvw.py`, com actions fixadas por SHA e permissões `contents: read`. O runner local continua como caminho sem conta. — P2-R3
- **G-06 · Validação incremental rápida:** depois de A-02, oferecer um hook `pre-commit` opcional (fora do core, contrato em `HOOKS.md`) que rode `validate_fcvw.py --since HEAD`. — P4-R2
- **G-07 · Evidência de plataforma:** registrar esta execução (Linux, Python 3.11, 305 testes OK) no próximo release record e reduzir os *Known gaps*. — P5-R1
- **G-08 · Índice de navegação menor:** `DOCUMENT_GRAPH.md` (20 KB) é regenerado a cada movimento de arquivo e é fonte frequente de conflito de merge. Avaliar gerá-lo apenas no pacote de release e usar o validador para a alcançabilidade no checkout-fonte. — P4-R2

---

## 9. H — Vault Obsidian indexado por YAML ("supercérebro" do projeto)

**Objetivo:** transformar toda a wiki, os registros de troubleshooting, as regras de
negócio, os fluxos de autenticação e o conhecimento sobre UI e código da aplicação num
**vault Obsidian único, indexado por frontmatter YAML**. A IA que opera o framework
consulta esse vault de forma seletiva e o mantém atualizado. Tudo isso sob uma
**condição inegociável:** o vault só entra no fluxo padrão se o consumo de tokens e a
qualidade dos desenvolvimentos **não piorarem** (ver H-05).

**Princípio de desenho:** reaproveitar o que já existe em vez de criar um sistema
paralelo (coerente com F-02 e com o "Framework proportionality" do `PLANNING.md`):

| Já existe | Papel no vault |
|---|---|
| `fcvw/wiki@1`, com relações tipadas, `source_digest` e `derived_from` ([wiki/schema.md](FCVW/wiki/schema.md)) | Envelope YAML comum de todas as notas |
| Wiki de produto e skill [QA](FCVW/skills/QA/SKILL.md) (inventário e superfícies de UI) | Notas de **elementos de UI** |
| `APP_RULES.md` (`APP-RULE-NNN`) | Notas de **regras de negócio** |
| `troubleshooting/` (`fcvw/troubleshooting@1`, `type: failure`) | Notas de **falhas**, que passam a participar do índice |
| `knowledge_graph_fcvw.py`, `build_context_index.py` e `retrieve_context.py` (BM25) | Grafo, índice e busca do vault |
| `LOOP_EVALUATION_CONTRACT.md` (TVC, FPVR, RFR, UCTR…) | Métricas de qualidade para o gate de ativação |

### H-01 · Definir o vault e a estrutura de pastas — P3-R3

- A raiz do vault é `FCVW/`, porque o `DOCUMENT_GRAPH` já é compatível com Obsidian e `.obsidian/` já está no `.gitignore`. Documentar isso em `MEMORY.md` e numa ADR nova ("Project knowledge vault").
- **Estrutura plana, sem pastas por tipo** (coerente com a seção J): o tipo da nota fica no YAML (`type:`) e no prefixo do `id`, e não em diretórios. O Obsidian filtra por propriedade, então pastas não são necessárias para navegar.

  ```text
  FCVW/wiki/README.md         índice curado + schema + taxonomia (um arquivo; hoje são 3)
  FCVW/wiki/<id>.md           todas as notas: UI-*, CODE-*, RULE-*, AUTH-*, DATA-*, FLOW-*, conceitos, decisões…
  FCVW/troubleshooting/       falhas (mantém o local e o schema atuais; é registro, não wiki)
  .fcvw-cache/vault/          catálogos, métricas e índice gerados — descartáveis, fora do versionamento
  ```

- Uma subpasta só é criada quando um tipo passa de cerca de 50 notas, e sempre sem README próprio.
- **Links:** manter o link Markdown relativo como forma canônica (regra do AGENTS.md). Wikilinks continuam opcionais e nunca duplicam a mesma relação.
- **Aceite:** um vault aberto no Obsidian mostra grafo, backlinks e busca por propriedades sem plugin obrigatório.

### H-02 · Envelope YAML único e novos tipos de nota — P2-R3

Estender `fcvw/wiki@1` (sem criar um schema paralelo) com novos valores de `type` e poucos campos opcionais:

```yaml
---
schema: "fcvw/wiki@1"
id: "CODE-billing-invoice-service"        # prefixo por tipo: UI-, CODE-, RULE-, AUTH-, DATA-, FLOW-, TRB-
type: "code_unit"                         # novos: ui_element | code_unit | business_rule | auth_flow | data_entity | flow
title: "InvoiceService — emissão e cancelamento de faturas"
summary: "Emite, cancela e reemite faturas; valida limite de crédito (RULE-012) antes de emitir."  # ≤ 280 caracteres
status: "validated"                       # draft | in_validation | validated | obsolete | superseded | contradictory
confidence: "high"
maturity: "established"
sensitivity: "internal"                   # public | internal | restricted  (ver H-08)
record_scope: "application"
retrieval_scope: "search_only"
source_path: "src/billing/invoice_service.py"
symbols: ["InvoiceService.issue", "InvoiceService.cancel"]   # âncoras estáveis, não números de linha
source_digest: "sha256:<digest do arquivo ou do símbolo>"
last_checked: "2026-09-25"
implements: ["RULE-012"]
depends_on: ["DATA-invoice", "AUTH-billing-roles"]
related: ["UI-invoice-form", "TRB-20260710-duplicate-invoice"]
tags: ["billing", "invoice"]
created_at: "2026-09-25"
last_reviewed: "2026-09-25"
sources: ["src/billing/invoice_service.py"]
---
```

- O **corpo** é curto e padronizado por tipo: *Propósito*, *Comportamento*, *Entradas/saídas*, *Regras e permissões*, *Estados de erro*, *Armadilhas conhecidas* e *Links*.
- O `summary` permite leitura progressiva: a IA lê frontmatter e resumo antes de decidir abrir o corpo ou o código.
- **Validador:** campos obrigatórios por tipo, `summary` com no máximo 280 caracteres, prefixo de `id` coerente com `type`, `source_path` existente e `symbols` presentes no arquivo (busca textual simples).
- **Aceite:** o validador cobre os 6 novos tipos, com fixtures positivas e negativas.

### H-03 · Migrar a wiki e o troubleshooting existentes para o índice único — P3-R2

- Os registros `fcvw/troubleshooting@1` continuam válidos, mas passam a ter `summary`, `tags` e as relações tipadas (`derived_from`, `related`, `invalidates`) indexadas pelo mesmo grafo e pelo mesmo índice. Assim, uma falha resolvida aparece quando alguém mexe no código de onde ela veio.
- Script de migração **não destrutivo** (`--dry-run` por padrão) que adiciona só os campos ausentes, nunca reescreve o corpo e gera um relatório do que não conseguiu inferir.
- Regras de negócio: **uma única fonte**. Ou o `APP_RULES.md` continua sendo o arquivo das regras e o vault apenas o indexa por seção (âncora `APP-RULE-NNN`), ou cada regra vira uma nota `RULE-*` e o `APP_RULES.md` deixa de existir. **Nunca as duas coisas.** A recomendação é a primeira opção enquanto houver menos de cerca de 30 regras, porque não cria arquivos novos.
- Depende de B-02 (todo troubleshooting precisa de schema) e de D-02 (definir quem gera o índice da wiki).

### H-04 · Índice e catálogos gerados (MOCs) — P3-R2

- Estender `knowledge_graph_fcvw.py` e `build_context_index.py` (sem criar uma ferramenta paralela) para emitir **em `.fcvw-cache/vault/`**, sem versionar e portanto sem somar arquivos ao repositório:
  - catálogo por tipo com `id`, `title`, `summary`, `status`, `last_checked` e o indicador de desatualização;
  - a lista de notas cujo `source_digest` não bate com o código atual.
- Opcional e versionado: **um único** arquivo de consulta do **Obsidian Bases** (`.base`, YAML) com uma visão por tipo, para navegação filtrada dentro do Obsidian sem plugins de terceiros. Verificar o formato atual do Obsidian antes de adotar.
- O índice BM25 passa a pesar `title`, `summary`, `tags` e `symbols` acima do corpo.
- **Aceite:** regeneração determinística (mesmos bytes para a mesma entrada); nenhum arquivo gerado versionado além do `.base` opcional.

### H-05 · Gate de ativação: tokens e qualidade não podem piorar — P1-R4

O vault começa **desligado para consulta automática** (modo `shadow`) e só vira padrão após um experimento com critérios pré-registrados:

| Dimensão | Métrica | Critério para ativar |
|---|---|---|
| Custo | tokens (ou bytes, com o método registrado) carregados por tarefa, somando vault e código lido | mediana ≤ baseline; p90 ≤ baseline + 10% |
| Custo | leituras de arquivos de código por tarefa | não aumenta |
| Qualidade | FPVR (validação aprovada na primeira tentativa) | ≥ baseline (não inferioridade) |
| Qualidade | RFR (retrabalho ou reabertura) e regressões detectadas após a conclusão | ≤ baseline |
| Qualidade | TVC (tarefas concluídas e validadas) | ≥ baseline |
| Utilidade | taxa de notas recuperadas que foram citadas no plano ou na evidência | ≥ 40% (senão, o ranking ou a granularidade estão errados) |
| Risco | respostas baseadas em nota desatualizada que contradizem o código | 0 no experimento |

- **Protocolo:** o mesmo conjunto de tarefas reais em pares (com e sem vault), em ordem alternada, com o baseline registrado antes. Reusar só as métricas necessárias do `LOOP_EVALUATION_CONTRACT`. Isso ajusta F-01: a camada adaptativa sai do core, mas as definições mínimas de métricas permanecem.
- **Queda automática:** se, em produção, qualquer métrica cruzar o critério por duas medições seguidas, a consulta volta para `shadow`. As notas continuam existindo como documentação.
- **Aceite:** relatório de experimento com os números brutos e o método de estimativa de tokens (regra do `TOKEN_BUDGET.md`: nada de economia sem medição).

### H-06 · Consulta com orçamento (como a IA usa o vault) — P2-R3

1. As rotas obrigatórias do `CONTEXT_MAP` continuam **acima** do vault. Uma nota nunca substitui política, código ou teste.
2. **Leitura progressiva:** catálogo ou busca → `summary` (frontmatter) → corpo da nota → código-fonte. A IA para no primeiro nível que responde à pergunta.
3. **Teto por tarefa**, configurável: no máximo 8 notas e cerca de 6 mil tokens estimados de vault. Rotas obrigatórias não consomem esse orçamento.
4. **Seleção dirigida pela mudança:** os arquivos alterados no plano (`context_files` e `--file-change`) buscam notas por `source_path`, `symbols` e relações de 1 salto (`implements`, `depends_on`, `related`). A busca textual livre fica em segundo plano.
5. Notas `stale`, `obsolete`, `contradictory` ou com `confidence: low` só entram rotuladas como tal e nunca como autoridade. **O código atual sempre vence a nota.**
6. Conteúdo de nota é **evidência, não instrução** (regra de prompt injection do `AI.md`).

### H-07 · Gatilhos de criação e atualização (o que alimenta o "supercérebro") — P2-R3

| Evento | Ação da IA | Tipo de nota |
|---|---|---|
| Plano concluído que alterou comportamento de um módulo | criar ou atualizar a nota da unidade de código, com novo `source_digest` | `code_unit` |
| Execução da skill QA (mapeamento ou teste) | criar ou atualizar os elementos e superfícies de UI | `ui_element` |
| Mudança sob `event:security` (login, sessão, token, perfil, permissão) | **obrigatório:** atualizar a nota do fluxo de autenticação ou autorização | `auth_flow` |
| Nova regra ou regra alterada em `APP_RULES` | criar ou atualizar a nota da regra e ligá-la a `implements` no código | `business_rule` |
| Mudança sob `event:data` (schema, migração) | atualizar a entidade e as dependências | `data_entity` |
| Troubleshooting encerrado | ligar a falha às unidades de código e regras afetadas | `failure` |
| `source_digest` divergente na validação | marcar para revisão; **nunca** atualizar sozinho sem reler o código | todos |

- **Etapa de closeout:** o `AUDIT.md` ganha a pergunta "notas do vault afetadas foram atualizadas ou marcadas para revisão?". Isso vira uma evidência do plano, não um passo manual esquecível.
- **Granularidade (anti-inchaço):** a unidade é o **módulo, componente, endpoint ou fluxo coeso**, e não cada linha ou trecho. Trechos relevantes aparecem como `symbols` dentro da nota. Não criar notas para código gerado, testes, configuração trivial ou código autoexplicativo. A regra atual "não criar uma página por arquivo do repositório" do `wiki/schema.md` continua valendo.
- **Aceite:** teste que simula um plano concluído que toca `src/x.py` sem atualizar ou marcar a nota ligada e exige um *warning* (e *error* quando o evento for de segurança).

### H-08 · Segurança e privacidade do vault — P1-R4

- Notas de autenticação descrevem **fluxo, papéis, pontos de verificação e riscos**, e **nunca** segredos, tokens, senhas, chaves, URLs internas sensíveis ou dados pessoais.
- Varredura no validador por padrões de segredo (chaves de API, JWT, `password=`, chaves privadas, `.env`) em todo o vault. Qualquer ocorrência bloqueia.
- `sensitivity: restricted` fica excluída da consulta automática por padrão e só é lida com rota explícita (`event:security`).
- O vault segue o mesmo controle de acesso do repositório. Nada é enviado a serviços externos, e não há embeddings remotos por padrão.

### H-09 · Métricas de saúde do vault (geradas em `.fcvw-cache/vault/metrics.json`; o `wiki/metrics.md` versionado deixa de existir) — P3-R2

| Métrica | Definição | Alvo inicial |
|---|---|---|
| Cobertura de UI | superfícies mapeadas pelo QA com nota validada ÷ superfícies no inventário | ≥ 80% no escopo declarado |
| Cobertura de código crítico | módulos marcados como críticos (auth, dados, regras, integrações) com nota ÷ total de críticos | ≥ 90% |
| Cobertura de regras | `APP-RULE` com nota **e** vínculo `implements` com o código ÷ total de regras | ≥ 90% |
| Cobertura de auth | fluxos de autenticação e autorização com nota validada ÷ fluxos identificados | 100% |
| Frescor | notas com `source_digest` coerente ÷ notas com `source_path` | ≥ 95% |
| Revisões vencidas | notas com `next_review` no passado | 0 bloqueantes |
| Qualidade estrutural | órfãs, links quebrados, contradições abertas, duplicatas por `source_path` e `symbols` | 0 |
| Tamanho | mediana e p90 de bytes por nota; notas acima do limite (ex.: 6 KB) | p90 ≤ 6 KB |
| Utilidade | taxa de citação das notas recuperadas (H-05) e notas nunca recuperadas em 90 dias (candidatas a arquivamento) | tendência ascendente |

- As métricas são **derivadas** (regeneradas), nunca editadas à mão. Métricas de cobertura não autorizam a criação em massa de notas de baixa qualidade: cobertura sem utilidade (H-05) é sinal de inchaço.

### H-10 · Ciclo de vida e poda — P3-R2

- A skill `wiki-curator` (ou a fusão proposta em E-03) cuida de desduplicar por `source_path` e `symbols`, arquivar notas nunca consultadas, consolidar notas pequenas demais e resolver `contradicts`.
- Código removido leva à nota `obsolete`, com `superseded_by` quando houver substituto. Nenhuma nota é apagada sem registro.

### H-11 · Integração com Obsidian sem dependência obrigatória — P4-R2

- Tudo funciona em Markdown puro com YAML. O Obsidian é visualizador e editor opcional; Dataview e outros plugins de terceiros ficam **fora** do core.
- A skill `obsidian-markdown` ganha a seção "propriedades do vault" (tipos de propriedade coerentes para o painel *Properties*: listas como listas, datas ISO).

### H-12 · Entrega incremental do vault — P2-R3

1. **V0 — Decisão:** ADR, extensão do schema (H-02) e regras de segurança (H-08).
2. **V1 — Base:** migração não destrutiva da wiki e do troubleshooting (H-03), catálogos (H-04) e métricas de saúde (H-09).
3. **V2 — Alimentação:** gatilhos de criação e atualização (H-07) em modo *warning*.
4. **V3 — Experimento:** consulta em `shadow` com orçamento (H-06) e experimento pareado (H-05).
5. **V4 — Ativação:** só se o gate H-05 passar; caso contrário, o vault continua como documentação navegável e o experimento é registrado como não promovido.

**Rollback:** desligar a consulta automática (volta para `shadow`) e manter as notas. Os campos YAML adicionados são opcionais e compatíveis com versões anteriores.

---

## 10. J — Redução de arquivos e pastas vazios ou redundantes (objetivo central)

**Situação medida em `FCVW/`: 228 arquivos e 65 diretórios.**

- **26 diretórios contêm apenas um `README.md`** (a maioria entre 200 e 500 bytes, dizendo só "guarde X aqui"): 20 sob `wiki/`, mais `briefings/`, `changelogs/unreleased/`, `Plans/discontinued/` e os 2 `queue.d/`.
- **11 profiles do projeto** estão com `instantiation_status: pending`, ou seja, só placeholders (~22 KB).
- **47 templates** de governança e **15** de wiki; 11 são só de refatoração e 5 só de automação.
- 18 arquivos no guia de refatoração.

**Meta:** reduzir `FCVW/` para **≤ 110 arquivos e ≤ 20 diretórios** (cerca de −50%) **sem perder nenhuma regra verificável**. Estado atual e final devem ser medidos e registrados no release record.

**Regra geral:** diretório nasce **sob demanda**, quando o primeiro registro real é criado, e nunca com um README de scaffolding. O "o que guardar aqui" passa a morar na política dona do assunto, que já existe.

| ID | Consolidação | Hoje → proposto | Economia aprox. | P/R |
|---|---|---|---|---|
| J-01 | **Wiki plana:** remover os 20 subdiretórios com README-only (`agents`, `archive`, `audits`, `components`, `concepts`, `decisions`, `failures`, `feedback`, `inbox`, `patterns`, `prompts`, `qa`, `raw`, `refactorings`, `regressions`, `releases`, `sessions`, `sources`, `syntheses`, `questions`); o tipo vai no YAML (ver H-01). Fundir `wiki/schema.md`, `taxonomy.md` e `index.md` num `wiki/README.md`. `log.md` sai (o `git log` é o log) e `metrics.md` vai para o cache | 43 arquivos / 22 dirs → ~4 arquivos / 1 dir | −39 arquivos, −21 dirs | P2-R3 |
| J-02 | **Templates de wiki:** 15 → **1** `TEMPLATE_NOTE.md` com o envelope YAML e blocos opcionais por `type`. Os 3 templates de produto (índice, superfície e execução de QA) vão para `skills/QA/`, que é quem os usa | 16 → 1 (+3 movidos) | −12 | P3-R2 |
| J-03 | **Fila de planos sem arquivos próprios:** `category`, `order`, `blocked_by` e `override_reason` passam para o frontmatter do plano; a fila é **derivada** por `plan_queue_fcvw.py` em `.fcvw-cache/`. Remove os 2 `queue.d/` e seus READMEs, os 2 `QUEUE.md` e, com eles, a classe inteira de erros "fila obsoleta" | 6 arquivos + 2 dirs → 0 | −6, −2 dirs | P2-R4 |
| J-04 | **Estados de plano:** manter as pastas de estado, mas sem README em cada uma (um único `Plans/README.md`). Alternativa mais radical: `Plans/` plana, com o status só no YAML, o que elimina o erro "status ≠ diretório" | 5 READMEs → 1 | −4 | P3-R3 |
| J-05 | **Profiles do projeto:** fundir `MANIFEST`, `SCOPE`, `STACK`, `ENVIRONMENT`, `DESIGN`, `DATA`, `PERFORMANCE`, `WORKFLOW` e `SECURITY` num **`PROJECT.md`** com uma seção por domínio e `instantiation_status` por seção. O questionário do `BRIEFING.md` vai para a skill `project-instantiation`. O `APP_RULES.md` continua separado (conteúdo que cresce) | 11 → 2 | −9 | P2-R4 |
| J-06 | **Automação:** `AUTOMATION`, `HOOKS`, `WATCHERS`, `DAEMONS` e `GOVERNANCE_GATES` → **`AUTOMATION.md`** com uma seção por `kind`. Os 5 templates (`AUTOMATION_CONTRACT`, `HOOK_CHECK`, `WATCHER_RULE`, `DAEMON_LOOP`, `GOVERNANCE_GATE_REPORT`) → 1 | 10 → 2 | −8 | P3-R3 |
| J-07 | **Refatoração:** `REFACTORING.md` + `refactoring-guide/` (18 arquivos, faltando 03–07) + 11 `TEMPLATE_REFACTORING_*` → `REFACTORING.md` (com o guia condensado em seções) + **1** `TEMPLATE_REFACTORING.md` | 30 → 2 | −28, −1 dir | P3-R2 |
| J-08 | **Pares política + README de diretório:** `ARCHITECTURAL_DECISIONS.md`/`decisions/README.md`, `TROUBLESHOOTING.md`/`troubleshooting/README.md`, `AUDIT.md`/`audits/README.md`, `framework-releases/README.md`/`RELEASE.md`. O catálogo vira seção da política ou é gerado; o README sai | 4 READMEs → 0 | −4 | P3-R2 |
| J-09 | **Políticas sobrepostas:** `VERSIONING` + `RELEASE` → `RELEASE.md`; `INSTANTIATION` + `RETROACTIVE_INSTANTIATION` → `INSTANTIATION.md` (dois modos); `TOKEN_BUDGET` → seção do `CONTEXT_MAP`; `FILESYSTEM` → seção do `OWNERSHIP` (resolve A-05); `MEMORY` + wiki schema → `wiki/README.md` | 9 → 4 | −5 | P3-R3 |
| J-10 | **Exemplos:** `examples/README.md` e `examples/minimal-change/{README,plan,changelog}.md` → blocos "exemplo preenchido" dentro dos próprios templates | 4 arquivos / 2 dirs → 0 | −4, −2 dirs | P4-R2 |
| J-11 | **Diretórios vazios de registro:** `briefings/`, `changelogs/unreleased/` e `Plans/discontinued/` são criados pela primeira escrita real (as ferramentas fazem `mkdir -p`) | 3 dirs → 0 | −3, −3 dirs | P4-R2 |
| J-12 | **Templates de governança restantes:** agrupar os de documentação de aplicação (`API_SPEC`, `DATA_SCHEMA`, `MODULE_DOCUMENTATION`, `FLOW_DOCUMENTATION`, `APP_DOCS_README`) → `TEMPLATE_APP_DOC.md` com seções por tipo; `AGENT_OR_SKILL_PROPOSAL` + `SELF_IMPROVEMENT_REPORT` → 1; `AI_RESOURCE` + `AI_SESSION_SYNTHESIS` → nota do vault | ~15 → ~5 | −10 | P3-R2 |
| J-13 | **Fora do payload instalado:** histórico do framework (F-05: 16 planos, audits e releases antigos) e camada adaptativa/loop (F-01: ~10 ferramentas e testes, 2 contratos, 3 ADRs) | — | −40 no pacote instalado | P2-R4 |

**Guarda contra o recrescimento** (a parte que impede o problema de voltar):

- **J-G1 · Regra no validador:** no perfil `clean-template`, um diretório sob `FCVW/` que contém só `README.md` vira finding (sem lista de exceções, ou com exceções nomeadas e justificadas).
- **J-G2 · Orçamento de superfície:** o release record passa a registrar `files`, `dirs` e bytes de `FCVW/`, com um teste falhando se o total crescer mais de X% sem justificativa no plano. É a pergunta 5 do "Framework proportionality" ("What is removed in exchange?") transformada em regra executável.
- **J-G3 · Um template por artefato versionado:** cada `schema` em `SCHEMAS.md` tem no máximo um template, e cada template tem um schema; o validador cruza os dois.

**Cuidados obrigatórios na execução da seção J:**

- **Registros existentes nunca são apagados:** em projetos instalados, notas e registros em pastas removidas são **movidos** (`git mv`) pela migração, com uma tabela caminho antigo → novo em `MIGRATIONS.md`, e o `upgrade_fcvw.py` executa a migração em `--dry-run` primeiro.
- Atualizar juntos: `REQUIRED_PATHS` do validador, rotas do `CONTEXT_MAP.md`, inferência de papéis no `role_manifest_fcvw.py`, empacotamento das 4 variantes de idioma, testes e links (a regeneração do `DOCUMENT_GRAPH` valida a alcançabilidade).
- Uma consolidação por plano (J-01, J-03, J-05… são planos separados), cada um com a suíte verde antes do próximo.
- **Aceite da seção:** contagem de arquivos e diretórios antes e depois registrada; nenhuma regra do validador sem teste equivalente; uma instalação V0.19.0 migrada sem perda de conteúdo (comparação de digests dos registros).

---

## 11. Roadmap proposto

### Fase 1 — Integridade (bloqueante; próximo patch V0.19.1)

- [ ] A-01 Upgrade: baseline imutável, modo seguro sem baseline, regravação após o apply (**P1-R5**, plano expandido, com rollback ensaiado)
- [ ] D-01 Corrigir a instrução do AGENTS.md sobre o `ROLE_MANIFEST` (junto com A-01)
- [ ] B-01 Restringir `fcvw/plan@1` a registros históricos
- [ ] A-02 Corrigir o escopo de `--since` (regras por atributo e arquivos removidos)
- [ ] A-03 Chaves duplicadas em `LOCALIZED_TITLES` e teste anti-duplicação
- [ ] B-02, B-03 Registros sem schema e superfícies ausentes viram findings
- [ ] A-04, A-06, A-07, A-09 Correções pontuais

**Aceite da fase:** cada bug tem um teste que falha no estado atual e passa após a correção; a suíte completa e o validador ficam verdes.

### Fase 2 — Gatilhos confiáveis (minor V0.20.0)

- [ ] G-03 Padrões de roteamento configuráveis
- [ ] C-01, C-02, C-03, C-04, C-07, C-09 Remover os falsos positivos
- [ ] B-06, B-07, B-08, B-09 Cobrir os falsos negativos
- [ ] B-04, B-05 Comparação exata em rotas, catálogo e cabeçalhos de skill
- [ ] C-05, C-06 Keywords de skills sem colisão, com teste
- [ ] B-10 Schema e validação de ADR
- [ ] G-01, G-02 Medição e teto de contexto e CLI de rotas

**Aceite da fase:** uma tabela de casos (caminho → eventos esperados) cobrindo framework e app típico (Python, Node, SQL), testada. A edição de um profile do projeto carrega ≤ 40 KB.

### Fase 3 — Simplificação e redução de arquivos (minor V0.21.0; exige migração)

- [ ] J-G1, J-G2, J-G3 Instalar primeiro as guardas contra o recrescimento (falham no estado atual e, depois da redução, passam a proteger o resultado)
- [ ] J-01, J-02 Wiki plana e template único de nota
- [ ] J-03, J-04 Fila derivada do frontmatter e READMEs de estado de plano consolidados
- [ ] J-05 `PROJECT.md` único para os profiles
- [ ] J-06, J-07, J-12 Consolidar os templates e as políticas de automação e refatoração
- [ ] J-08, J-09, J-10, J-11 Pares política/README, políticas sobrepostas, exemplos e diretórios vazios
- [ ] F-05 / J-13 Remover o histórico do framework do payload instalado (migração em `MIGRATIONS.md`)
- [ ] F-01 Extrair a camada adaptativa e de loop para um pacote opcional
- [ ] F-03, E-01, E-02, E-04 Modularizar o validador, tornar os schemas de registro declarativos e unificar a lista de obrigatórios
- [ ] F-04 Estratégia de i18n para cabeçalhos
- [ ] E-03 Fundir as skills sobrepostas (via `self-improvement` e `agent-factory`)
- [ ] F-02, F-06, F-07 Enxugar schemas, diretórios de wiki e templates de refatoração
- [ ] F-08 Caminho "trivial" sem plano
- [ ] D-02 a D-10, E-05 a E-08 Alinhar os documentos

**Aceite da fase:** `FCVW/` com ≤ 110 arquivos e ≤ 20 diretórios, e o payload instalado pelo menos 30% menor em bytes (medidos antes e depois); nenhuma regra do validador perde cobertura (a suíte de regressão continua verde); a migração foi testada numa instalação V0.19.0.

### Fase 4 — Operação contínua

- [ ] G-05 CI gratuito, reativado com uma matriz mínima
- [ ] G-04 Linter estático
- [ ] G-06 Hook opcional de validação incremental
- [ ] G-07, G-08 Evidência de plataforma e navegação mais leve

### Fase 5 — Vault "supercérebro" (depois da redução J, já na estrutura plana)

- [ ] H-01, H-02, H-08 ADR do vault, extensão do schema YAML e regras de segurança
- [ ] H-03, H-04, H-09 Migração da wiki e do troubleshooting, catálogos gerados e métricas de saúde
- [ ] H-07, H-10, H-11 Gatilhos de criação e atualização, poda e integração Obsidian
- [ ] H-06, H-05 Consulta com orçamento em `shadow` e experimento pareado
- [ ] H-12 Ativação condicionada ao gate (tokens ≤ baseline e qualidade não inferior)

**Aceite da fase:** relatório do experimento H-05 com números brutos; ativação só se todos os critérios passarem; rollback para `shadow` testado.

---

## 12. Riscos e cuidados na execução

- A-01 e F-05 mexem no mecanismo de upgrade e no conteúdo instalado: exigem plano **expandido**, backup e ensaio de rollback numa instalação real anterior.
- Mudanças em `CONTEXT_MAP.md`, `AGENTS.md` e skills disparam `event:ai` e `event:policy`: reexecutar os casos de fronteira (permitido, negado, ambíguo, injeção) descritos em [TESTS.md](FCVW/TESTS.md).
- Enxugar documentos traduzidos exige regenerar as 4 variantes de idioma do release. Planeje a Fase 3 junto com a revisão linguística.
- O vault (H) é o item com maior risco de **piorar** tokens e qualidade (inchaço, notas desatualizadas tratadas como verdade, vazamento de dados de autenticação). Por isso ele nasce em `shadow`, com teto de orçamento, código sempre acima da nota e gate de ativação medido.
- Nenhum item deste backlog autoriza, por si só, a implementação: cada um passa pelo fluxo de plano do [AGENTS.md](AGENTS.md).
