# Briefing Inicial do Projeto

Documento metodológico para conduzir a **Fase 0 — Descoberta e Briefing** antes do desenvolvimento ou reestruturação de uma aplicação.

Este arquivo define as perguntas, critérios mínimos e regras de preenchimento que devem ser usados por humanos e agentes de IA para coletar as informações necessárias antes de gerar ou atualizar `ESCOPO.md`, `STACK.md`, `DESIGN.md`, `WORKFLOW.md`, `PLANEJAMENTO.md`, `VERSIONAMENTO.md`, `SEGURANCA.md`, `DADOS.md`, `IA.md` e demais documentos oficiais do projeto.

## Objetivo

Garantir que o início do desenvolvimento seja guiado, rastreável e sem lacunas críticas.

A Fase 0 deve produzir um arquivo preenchido em:

```text
briefings/BRIEFING_INICIAL.md
```

Esse arquivo deve funcionar como a fonte inicial de entendimento do projeto. Depois que os documentos oficiais forem criados, ele deixa de ser fonte normativa principal, mas permanece como registro histórico da concepção do projeto.

## Relação com os demais documentos

- `AGENTS.md`: deve acionar este processo quando o usuário solicitar criação ou reestruturação de aplicação.
- `ESCOPO.md`: deve ser preenchido a partir das respostas sobre objetivo, público, limites e funcionalidades.
- `STACK.md`: deve ser preenchido a partir das decisões técnicas.
- `DESIGN.md`: deve ser preenchido a partir das preferências visuais e critérios de UX.
- `WORKFLOW.md`: deve ser preenchido a partir dos fluxos, telas, módulos e eventos.
- `SEGURANCA.md`: deve ser preenchido a partir dos riscos, permissões, dados sensíveis e integrações.
- `DADOS.md`: deve ser preenchido a partir da persistência, arquivos, banco, retenção e migração.
- `IA.md`: deve ser preenchido a partir do papel da IA, modelos, contexto, memória, RAG e limites de ação.
- `PLANEJAMENTO.md`: deve orientar os planos posteriores.
- `VERSIONAMENTO.md`: deve orientar a versão inicial e futuras releases.

## Regra de ativação obrigatória

Quando o usuário solicitar o início de uma nova aplicação, uma reconstrução do zero, uma migração ampla, ou a adaptação deste framework para outro projeto, o agente de IA deve:

1. Verificar se já existe `briefings/BRIEFING_INICIAL.md`.
2. Se não existir, iniciar a entrevista guiada.
3. Registrar as respostas no arquivo de briefing.
4. Consultar `INSTANCIACAO.md` e aplicar manualmente as regras de renomeação, placeholders e separação entre documentos canônicos e templates.
5. Marcar campos desconhecidos como `A definir`.
6. Listar lacunas críticas antes de gerar os documentos oficiais.
7. Não iniciar implementação de código enquanto houver lacunas críticas sem decisão explícita do usuário.

## Níveis de lacuna

### Lacuna crítica

Impede o início seguro do desenvolvimento.

Exemplos:

- objetivo da aplicação indefinido;
- público-alvo indefinido;
- plataforma alvo indefinida;
- forma de uso da IA indefinida;
- dados manipulados desconhecidos;
- requisitos de segurança não avaliados;
- stack obrigatória ou restrições técnicas não definidas;
- funcionalidades obrigatórias não priorizadas.

### Lacuna relevante

Não impede prototipação, mas deve ser resolvida antes de desenvolvimento estável.

Exemplos:

- identidade visual ainda não aprovada;
- nome final indefinido;
- integrações futuras ainda não detalhadas;
- política de backup pendente;
- critérios de aceite ainda genéricos.

### Lacuna tolerável

Pode permanecer em aberto durante as primeiras versões.

Exemplos:

- slogan;
- ícone final;
- documentação pública;
- recursos opcionais;
- internacionalização futura.

## Questionário obrigatório

### 1. Identificação do projeto

- Nome provisório:
- Nome final, se houver:
- Tipo de aplicação:
- Plataforma alvo:
- Sistema operacional alvo:
- Público-alvo:
- Problema que a aplicação resolve:
- Objetivo principal:
- Critério de sucesso do produto:

### 2. Contexto de uso

- Quem usará a aplicação?
- Em qual ambiente a aplicação será usada?
- A aplicação será usada de forma pessoal, interna, corporativa ou pública?
- A aplicação precisa funcionar offline?
- A aplicação precisa funcionar em rede local?
- A aplicação terá múltiplos usuários?
- Existe alguma restrição de hardware ou desempenho?

### 3. Escopo funcional

- Funcionalidades obrigatórias:
- Funcionalidades desejáveis:
- Funcionalidades explicitamente fora de escopo:
- Fluxo principal do usuário:
- Telas ou módulos previstos:
- Ações críticas do usuário:
- Ações destrutivas que exigem confirmação:
- Integrações necessárias:
- Relatórios, exportações ou importações necessárias:

### 4. Uso de IA

- A aplicação usará IA local, online ou híbrida?
- Qual runtime, provedor ou modelo está previsto?
- A IA será usada para chat, automação, análise, RAG, geração de conteúdo, classificação, agentes ou outro uso?
- A IA poderá executar ações ou apenas responder?
- Haverá memória, histórico ou base de conhecimento?
- Haverá embeddings ou busca vetorial?
- Haverá aprendizado contínuo?
- Quais informações a IA não deve acessar?
- Quais ações a IA nunca poderá executar automaticamente?

### 5. Dados e persistência

- Quais dados serão armazenados?
- Onde serão armazenados?
- Haverá banco de dados?
- Haverá arquivos locais?
- Haverá dados sensíveis?
- Haverá logs?
- Haverá backup?
- Haverá exportação ou importação?
- Haverá migração entre versões?
- Qual dado deve ser ignorado pelo Git?

### 6. Segurança e privacidade

- A aplicação exigirá autenticação?
- Haverá perfis ou permissões?
- Haverá tokens, chaves ou segredos?
- Haverá execução de comandos locais?
- Haverá acesso ao sistema de arquivos?
- Haverá comunicação com APIs externas?
- Quais ameaças iniciais são previsíveis?
- Como serão tratados dados privados ou sensíveis?

### 7. Design e experiência

- Estilo visual desejado:
- Tema claro, escuro ou ambos:
- Densidade da interface:
- Referências visuais:
- Paleta desejada:
- Tipografia desejada:
- Componentes principais:
- Requisitos de acessibilidade:
- Restrições de layout:
- Comportamento em telas pequenas ou janelas redimensionadas:

### 8. Stack técnica

- Linguagem principal:
- Framework de frontend:
- Framework de backend:
- Banco de dados:
- Runtime de IA:
- Ferramentas de build:
- Dependências externas:
- Padrão de empacotamento:
- Restrições obrigatórias:
- Tecnologias proibidas:

### 9. Qualidade, testes e validação

- Como o projeto será testado?
- Quais fluxos precisam de teste manual obrigatório?
- Haverá testes automatizados?
- Haverá checklist de release?
- Quais critérios definem que uma versão está pronta?
- Quais regressões seriam inaceitáveis?

### 10. Versionamento e governança

- Versão inicial:
- Estratégia de versionamento:
- Padrão de changelog:
- Padrão de planos:
- Critério para versão minor:
- Critério para versão patch:
- Critério para versão major:
- Responsável por aprovar mudanças de escopo:
- Responsável por aprovar mudanças visuais:

---

## Modelos e Templates

Para realizar o levantamento inicial de um novo projeto, utilize o modelo em:
`governança/TEMPLATE_BRIEFING.md`

## Regra de encerramento da Fase 0

A Fase 0 só pode ser marcada como concluída quando:

- o briefing inicial existir;
- as lacunas críticas estiverem resolvidas ou formalmente aceitas pelo usuário;
- o agente tiver indicado quais documentos oficiais serão criados ou atualizados;
- o usuário tiver aprovado o escopo mínimo de início;
- qualquer premissa assumida estiver registrada.
