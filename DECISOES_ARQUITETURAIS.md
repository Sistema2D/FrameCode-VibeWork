# Decisões Arquiteturais

Documento metodológico para registrar decisões técnicas relevantes do projeto por meio de ADRs, Architecture Decision Records.

Este arquivo deve ser consultado antes de mudanças que alterem arquitetura, stack, persistência, contratos de API, organização de módulos, runtime, segurança, distribuição, integração com IA ou fluxo central da aplicação.

## Objetivo

Evitar que decisões importantes fiquem implícitas em conversas, commits, prompts ou código.

Cada decisão arquitetural relevante deve ser registrada para que humanos e agentes de IA entendam:

- o contexto da decisão;
- as alternativas consideradas;
- a decisão tomada;
- as consequências;
- os riscos;
- a relação com planos, versões e changelogs.

## Local dos registros

As decisões devem ficar em:

```text
decisoes/
```

Modelo de nome:

```text
ADR-0001-descricao-curta.md
ADR-0002-descricao-curta.md
```

## Quando criar uma ADR

Criar ADR quando a mudança envolver:

- troca de stack;
- criação de novo módulo central;
- alteração de arquitetura frontend/backend;
- mudança de banco ou formato de persistência;
- alteração de contrato de API;
- adoção de novo runtime de IA;
- mudança de estratégia de RAG ou memória;
- alteração de segurança relevante;
- alteração de build, empacotamento ou distribuição;
- decisão de abandonar alternativa técnica importante;
- reescrita de módulo;
- separação ou fusão de serviços.

## Quando não criar ADR

Não é necessário criar ADR para:

- ajustes visuais simples;
- correção de texto;
- bug pontual sem impacto arquitetural;
- refatoração pequena sem mudança de responsabilidade;
- atualização documental comum;
- melhoria local de componente sem impacto em outros módulos.

## Status permitidos

- `proposta`: decisão ainda em análise;
- `aceita`: decisão aprovada e vigente;
- `substituída`: decisão trocada por ADR posterior;
- `rejeitada`: decisão analisada e não adotada;
- `obsoleta`: decisão não se aplica mais ao estado atual do projeto.

## Relação com planos e changelogs

- ADR não substitui plano em `Planos/`.
- Mudança que implementa uma ADR deve ter plano próprio.
- Release que implementa uma ADR deve citar a decisão no changelog.
- ADR substituída deve apontar para a nova ADR.
- Páginas em `wiki/decisions/` são sínteses de aprendizado e não substituem a ADR formal.

---

## Modelos e Templates

Para criar novas Decisões Arquiteturais (ADRs), utilize o modelo em:
`governança/TEMPLATE_ADR.md`

## Checklist antes de aceitar uma ADR

- [ ] O problema foi descrito com clareza.
- [ ] Alternativas foram consideradas.
- [ ] A decisão não contradiz o escopo aprovado.
- [ ] Impactos em segurança foram avaliados.
- [ ] Impactos em dados foram avaliados.
- [ ] Impactos em testes foram avaliados.
- [ ] Consequências negativas foram registradas.
- [ ] Existe plano para implementar a decisão, se necessário.
