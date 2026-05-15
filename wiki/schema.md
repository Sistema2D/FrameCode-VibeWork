# Schema da LLM Wiki

Este arquivo define as regras estruturais, semânticas e operacionais da wiki do projeto.

A wiki deve ser mantida em Markdown legível por humanos e por agentes de IA. Seu objetivo é preservar conhecimento técnico acumulado, reduzir retrabalho, evitar repetição de falhas e melhorar decisões futuras.

---

## 1. Estrutura obrigatória

```text
wiki/
├── README.md
├── schema.md
├── index.md
├── log.md
├── inbox/
├── raw/
├── sources/
├── concepts/
├── decisions/
├── patterns/
├── failures/
├── refactorings/
├── audits/
├── releases/
├── components/
├── prompts/
├── questions/
├── syntheses/
└── templates/
```

---

## 2. Categorias de páginas

### Estrutura Básica de um Arquivo

Todos os arquivos da Wiki devem iniciar com um bloco de metadados YAML para permitir indexação e visualização avançada, exceto os arquivos explicitamente isentos na seção de frontmatter.

Use o modelo mínimo definido na seção **Frontmatter obrigatório**. Não misture campos equivalentes em idiomas diferentes, como o campo inglês para tipo e `tipo`, ou valores de status em inglês e português.

### Nomenclatura e Pastas

| Categoria | Pasta | Finalidade |
|---|---|---|
| Inbox | `inbox/` | Entradas temporárias ainda não analisadas |
| Raw | `raw/` | Fontes brutas preservadas, preferencialmente imutáveis |
| Sources | `sources/` | Descrição ou normalização de fontes relevantes |
| Concepts | `concepts/` | Conceitos técnicos, de produto ou processo |
| Decisions | `decisions/` | Decisões arquiteturais consolidadas |
| Patterns | `patterns/` | Padrões validados e reutilizáveis |
| Failures | `failures/` | Falhas recorrentes, causas raiz e soluções |
| Refactorings | `refactorings/` | Oportunidades, aprendizados e critérios de refatoração |
| Audits | `audits/` | Achados e padrões recorrentes derivados de relatórios em `auditorias/` |
| Releases | `releases/` | Sínteses de versões publicadas |
| Components | `components/` | Módulos, telas, serviços e responsabilidades |
| Prompts | `prompts/` | Prompts úteis, testados ou recomendados |
| Questions | `questions/` | Perguntas abertas e hipóteses a investigar |
| Syntheses | `syntheses/` | Sínteses transversais entre múltiplas fontes |

---

## 3. Frontmatter obrigatório

Toda página de conhecimento, exceto `README.md`, `schema.md`, `index.md`, `log.md` e READMEs internos de pasta, deve iniciar com frontmatter YAML.

Modelo mínimo:

```yaml
---
titulo: "<título da página>"
tipo: "concept | decision | pattern | failure | refactoring | audit | release | component | prompt | question | synthesis | source | raw"
status: "rascunho | em_validacao | validado | obsoleto | substituido | contraditorio"
confianca: "baixa | media | alta"
ultima_revisao: "AAAA-MM-DD"
versao_relacionada: "V0.0.0"
fontes:
  - "<caminho ou referência da fonte>"
tags:
  - "<tag>"
---
```

---

## 4. Estados permitidos

### `rascunho`

Página criada, mas ainda incompleta ou não validada.

### `em_validacao`

Página aguardando revisão, teste, auditoria ou confirmação.

### `validado`

Conhecimento conferido, com fontes e evidências suficientes.

### `obsoleto`

Conhecimento antigo que não deve ser usado como referência principal.

### `substituido`

Conhecimento substituído por outra página ou decisão posterior.

### `contraditorio`

Conhecimento em conflito com outra fonte ou evidência. Exige investigação.

---

## 5. Níveis de confiança

### `baixa`

Use quando a página contém hipótese inicial, observação não confirmada ou inferência.

### `media`

Use quando há indícios, mas ainda falta validação completa.

### `alta`

Use quando há fonte, validação, teste, auditoria ou confirmação suficiente.

---

## 6. Regra de promoção para conhecimento

Nem todo registro deve virar página da wiki.

Um conteúdo deve ser promovido para a wiki quando atender a pelo menos um critério:

- A falha pode ocorrer novamente.
- A solução pode ser reaplicada.
- A decisão afeta arquitetura, stack, segurança, dados ou UX.
- A auditoria revelou padrão recorrente.
- A refatoração criou aprendizado reutilizável.
- O prompt pode ser reaproveitado.
- A pergunta aberta orienta decisões futuras.
- A síntese reduz retrabalho em próximas interações.
- O conhecimento melhora a capacidade da IA de atuar no projeto.

Conteúdos pontuais, triviais ou sem reutilização clara devem permanecer apenas nos registros originais.

---

## 7. Regra de fontes

Toda página interpretativa deve apontar para suas fontes.

Fontes podem ser:

- arquivos em `Planos/`;
- arquivos em `changelogs/`;
- arquivos em `troubleshooting/`;
- arquivos em `auditorias/`;
- ADRs em `decisoes/`;
- documentos oficiais do projeto;
- logs técnicos;
- trechos de código;
- prompts relevantes;
- respostas consolidadas;
- arquivos brutos em `wiki/raw/`.

Se a fonte não estiver disponível, registrar:

```text
Fonte não disponível. Página baseada em síntese contextual.
```

---

## 8. Links internos

Use links no estilo Obsidian quando possível:

```markdown
[[patterns/padrao-escrita-atomica]]
[[failures/erro-exemplo-de-reproducao]]
[[decisions/escolha-de-stack-exemplo]]
```

Sempre que uma página citar outro conceito, falha, decisão ou padrão existente, deve criar link interno para ele.

---

## 9. Regras para `raw/`

A pasta `raw/` armazena fontes brutas.

Regras:

- não alterar conteúdo bruto sem justificativa explícita;
- preferir adicionar nova versão em vez de sobrescrever;
- registrar origem, data e contexto;
- não armazenar segredos, tokens, senhas ou dados sensíveis desnecessários;
- quando houver dado sensível, anonimizar antes de registrar.

---

## 10. Regras para `index.md`

O arquivo `index.md` deve funcionar como mapa navegável da wiki.

Ele deve conter:

- páginas mais importantes;
- padrões validados;
- falhas recorrentes;
- decisões principais;
- refatorações relevantes;
- auditorias com aprendizados;
- releases;
- perguntas abertas;
- páginas obsoletas importantes.

O índice deve ser atualizado sempre que uma nova página relevante for criada ou quando uma página mudar de status.

---

## 11. Regras para `log.md`

O arquivo `log.md` deve registrar eventos cronológicos da wiki.

Registrar eventos como:

- ingestão de fonte;
- criação de página;
- atualização de síntese;
- lint da wiki;
- contradição encontrada;
- promoção de conhecimento;
- marcação de obsolescência;
- consolidação pós-release;
- aprendizado pós-troubleshooting;
- aprendizado pós-auditoria.

---

## 12. Lint da wiki

A IA deve executar ou recomendar lint da wiki quando ocorrer:

1. publicação de versão minor ou major;
2. falha recorrente resolvida;
3. auditoria reprovada;
4. refatoração estrutural;
5. inclusão de múltiplas fontes novas;
6. contradição entre documentos oficiais;
7. solicitação explícita do usuário.

O lint deve verificar:

- páginas órfãs;
- links quebrados;
- conceitos citados sem página;
- falhas resolvidas sem síntese;
- planos concluídos sem aprendizado extraído;
- changelogs sem síntese de release;
- ADRs sem página em `decisions/`;
- páginas antigas com status incorreto;
- contradições entre fontes;
- ausência de atualização no `index.md`;
- ausência de registro no `log.md`.

---

## 13. Política de contradições

Quando uma nova fonte contradisser uma página existente:

1. Não apagar a página antiga sem justificativa.
2. Marcar a página antiga como `contraditorio`, `obsoleto` ou `substituido`, conforme o caso.
3. Registrar a contradição na própria página.
4. Criar ou atualizar síntese em `syntheses/`, se necessário.
5. Registrar o evento em `log.md`.
6. Indicar qual fonte deve prevalecer e por quê.

---

## 14. Política de obsolescência

Quando uma página deixar de representar o estado atual:

- alterar `status` para `obsoleto` ou `substituido`;
- indicar página substituta, se houver;
- registrar data da revisão;
- atualizar `index.md`, se a página estiver listada;
- registrar em `log.md`.

---

## 15. Uso por agentes de IA

A wiki implementa três operações principais: **Ingest**, **Query** e **Lint**. Consulte a seção correspondente para cada situação.

Antes de executar ações relevantes, a IA deve consultar:

1. `AGENTS.md`;
2. `MANIFESTO.md`;
3. `wiki/index.md`;
4. páginas da wiki relacionadas ao tema;
5. documentos oficiais correspondentes.

Após executar ação que gere aprendizado reutilizável, a IA deve avaliar se deve atualizar a wiki.

A IA não deve alegar que consultou, validou ou atualizou a wiki se isso não tiver sido feito.

---

## 16. Operação de Query

Query é o fluxo de resposta a perguntas usando a wiki como fonte primária antes de recorrer a pesquisa externa ou influência do modelo.

### Fluxo

1. Ler `wiki/index.md` para identificar páginas relevantes ao tema.
2. Ler as páginas identificadas, priorizando `status: validado` e `confianca: alta`.
3. Sintetizar a resposta com citações às fontes wiki.
4. Avaliar se a resposta merece ser promovida como nova página ou atualização de página existente.

### Regras

- Respostas de alta qualidade ou reutilizáveis devem ser arquivadas em `wiki/syntheses/`.
- Toda resposta promovida deve ter frontmatter com `tipo: synthesis` e apontar para a pergunta ou fonte original.
- Páginas com `status: rascunho` ou `confianca: baixa` devem ser usadas com reserva e citar essa limitação.
- Perguntas abertas que não puderem ser respondidas com as fontes disponíveis devem ir para `wiki/questions/`.
- Registrar o evento de query em `log.md` quando gerar uma página nova ou atualizar uma existente.
- Não fabricar informações quando a wiki não tiver fonte suficiente; informar explicitamente a lacuna.
