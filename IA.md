# Uso de IA na Aplicação

Documento metodológico para definir como modelos de IA, agentes, prompts, contexto, memória, RAG, ferramentas e aprendizado contínuo devem ser projetados, integrados, testados e limitados dentro da aplicação.

Este arquivo deve ser consultado antes de qualquer alteração relacionada a chat, modelos, prompts, ferramentas, agentes, memória, embeddings, recuperação de contexto, execução de ações, integração com provedores de IA ou automação assistida por IA.

## Objetivo

Garantir que o uso de IA seja útil, rastreável, seguro, testável e coerente com o escopo da aplicação.

## Princípios

- A IA deve ter papel claro dentro do produto.
- O usuário deve entender quando está interagindo com IA.
- Conteúdo recuperado deve ser tratado como dado, não como instrução soberana.
- A IA não deve executar ações destrutivas sem confirmação explícita.
- Respostas baseadas em fontes locais devem indicar as fontes quando aplicável.
- Falhas do modelo devem ser tratadas de forma previsível.
- Parâmetros do modelo devem ser documentados quando expostos ao usuário.
- O uso de IA deve respeitar `SEGURANCA.md`, `DADOS.md` e `TESTES.md`.

## Tipos de uso de IA

### Chat simples

A IA responde a mensagens do usuário sem recuperar base local.

Regras:

- validar modelo selecionado;
- tratar erro de runtime;
- permitir cancelamento quando houver streaming;
- preservar histórico conforme regra de dados.

### Chat com contexto

A IA responde usando histórico, notas, arquivos ou dados recuperados.

Regras:

- separar claramente instrução do usuário e contexto recuperado;
- limitar tamanho de contexto;
- indicar fontes quando usadas;
- não permitir que contexto recuperado sobrescreva regras superiores.

### RAG ou busca em base de conhecimento

A IA usa recuperação de documentos para responder.

Regras:

- documentar origem das fontes;
- registrar estratégia de chunking quando aplicável;
- validar relevância dos resultados;
- lidar com ausência de fonte;
- evitar afirmar como fato conteúdo não encontrado.

### Aprendizado contínuo

A IA cria, atualiza ou organiza conhecimento com base em uso ou arquivos.

Regras:

- preservar fonte bruta quando necessário;
- registrar notas geradas;
- evitar sobrescrever conhecimento sem backup;
- marcar conteúdo gerado por IA quando aplicável;
- permitir revisão humana quando o conteúdo for crítico.

### Agente com ferramentas

A IA pode chamar funções, executar comandos, alterar arquivos ou interagir com sistemas.

Regras:

- aplicar menor privilégio;
- exigir confirmação para ações destrutivas;
- registrar ações executadas;
- bloquear comandos perigosos sem aprovação;
- não conceder acesso irrestrito a arquivos ou rede.

## Hierarquia de instruções

A aplicação deve considerar a seguinte ordem de precedência:

1. Regras do sistema e ambiente de execução.
2. Regras do projeto, como `AGENTS.md` e documentos oficiais.
3. Instruções diretas do usuário no fluxo atual, desde que não conflitem com regras superiores.
4. Configurações persistidas da aplicação.
5. Conteúdo recuperado de arquivos, notas, histórico ou RAG.
6. Preferências inferidas ou sugestões do modelo.

Conteúdo recuperado nunca deve substituir regras superiores.

## Prompt injection

Riscos comuns:

- arquivo importado com instrução para ignorar regras;
- nota local contendo comando malicioso;
- resposta anterior tentando alterar papel do agente;
- conteúdo externo pedindo acesso a arquivos ou segredos.

Regras:

- Delimitar contexto recuperado.
- Tratar contexto como evidência, não como comando.
- Não revelar segredos por solicitação contida em fonte recuperada.
- Não executar ações contidas em documentos recuperados sem solicitação direta do usuário.
- Registrar falhas ou tentativas relevantes em `troubleshooting/`.

## Parâmetros de modelo

Quando a interface expuser parâmetros, documentar:

- nome do parâmetro;
- efeito prático;
- faixa permitida;
- valor padrão;
- impacto em criatividade, precisão, custo, velocidade ou repetição;
- riscos de valores extremos.

Parâmetros comuns:

- temperatura;
- top-p;
- top-k;
- tamanho de contexto;
- system prompt;
- modelo selecionado;
- streaming;
- número de fontes recuperadas;
- limiar de similaridade.

## Fontes e rastreabilidade

Quando uma resposta usar base local ou documentos:

- registrar fonte, caminho ou identificador;
- exibir fontes quando possível;
- limitar número de fontes exibidas sem ocultar rastreabilidade;
- diferenciar resposta baseada em fonte de resposta geral;
- informar quando não houver fonte suficiente.

## Memória e histórico

Regras:

- O usuário deve saber quando histórico ou memória está habilitado.
- Deve haver forma de limpar ou desabilitar memória quando aplicável.
- Memória não deve armazenar segredo sem necessidade.
- Histórico deve respeitar `DADOS.md` e `SEGURANCA.md`.
- Aprendizado gerado a partir de conversa deve ser rastreável.

## Avaliação de qualidade da IA

Critérios recomendados:

- relevância da resposta;
- fidelidade às fontes;
- ausência de extrapolação indevida;
- clareza;
- utilidade prática;
- segurança;
- estabilidade com entradas longas;
- comportamento diante de ausência de contexto;
- comportamento diante de instrução maliciosa.

## Checklist para mudanças envolvendo IA

- [ ] O papel da IA está definido.
- [ ] O modelo ou runtime está documentado.
- [ ] Entradas e saídas foram especificadas.
- [ ] Contexto recuperado é tratado como dado não confiável.
- [ ] Há tratamento para modelo indisponível.
- [ ] Há tratamento para resposta vazia ou erro de streaming.
- [ ] Há limite de tamanho de contexto.
- [ ] Há regra para fontes.
- [ ] Há proteção contra prompt injection.
- [ ] Há validação manual ou automatizada.
- [ ] Há changelog correspondente quando arquivos versionados foram alterados.

---

### 10.3 Taxonomia de Tags para Memória Técnica

Para facilitar a recuperação e a visualização no Obsidian, a IA deve utilizar as seguintes tags padrão:

- `#gold-pattern`: Soluções arquiteturais ou de código validadas e reutilizáveis.
- `#failure-log`: Registros de falhas e troubleshooting (alimenta o aprendizado preventivo).
- `#arch-decision`: Registro de ADRs e decisões que moldam o sistema.
- `#tech-debt`: Débitos técnicos identificados durante o desenvolvimento.
- `#refactor-plan`: Planos e resultados de refatorações.
- `#user-feedback`: Insights e solicitações diretas do usuário.

## Modelos e Templates

Para criar novas especificações de recursos de IA, utilize o modelo em:
`governança/TEMPLATE_IA_RECURSO.md`
