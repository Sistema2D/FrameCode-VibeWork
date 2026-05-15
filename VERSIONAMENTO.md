# Versionamento e Changelogs

Este documento define as regras de versionamento, release e changelog da aplicação.

O objetivo é garantir rastreabilidade entre planos, alterações aplicadas, arquivos modificados, justificativas, validações executadas e versões publicadas.

## Versão base e versão atual

A versão base formal do processo de versionamento documentado é:

```text
V0.0.0
```

A versão atual da aplicação deve ser consultada em conjunto em:

- código-fonte da aplicação (constante ou arquivo de versão);
- `STACK.md`, campo `Versao atual`;
- `MANIFESTO.md`, campo `Versão atual`;
- `changelogs/Vx.y.z.md` correspondente.

Enquanto a versão não for centralizada em um único arquivo de release, as referências de versão em código e documentação devem permanecer coerentes entre si.

## Relação com release

`RELEASE.md` descreve o fluxo operacional para preparar, validar e publicar uma release. Este `VERSIONAMENTO.md` é a fonte normativa para versão, incremento, status de changelog e critérios de publicação.

O changelog em `changelogs/Vx.y.z.md` é a fonte formal da versão publicada ou em preparação. Sínteses em `wiki/releases/` podem registrar aprendizados reutilizáveis, mas não substituem o changelog.

## Formato da versão

```text
Vx.y.z
```

Onde:

- `x`: versão maior;
- `y`: versão menor;
- `z`: versão de correção.

## Critérios de incremento

### Versão maior (`x`)

Incrementar quando a alteração:

- modificar arquitetura central;
- alterar contratos principais de API;
- exigir migração estrutural relevante;
- quebrar compatibilidade com dados persistidos antigos;
- alterar fluxo principal de forma incompatível com versões anteriores;
- introduzir mudança ampla de produto ou distribuição.

### Versão menor (`y`)

Incrementar quando a alteração:

- adicionar funcionalidade relevante;
- criar nova tela, módulo ou fluxo de uso;
- expandir capacidades sem quebrar compatibilidade;
- adicionar integração ou melhoria funcional significativa.

### Versão de correção (`z`)

Incrementar quando a alteração:

- corrigir bug;
- ajustar comportamento existente sem mudar contrato;
- melhorar documentação;
- atualizar processo, planejamento, troubleshooting ou design;
- corrigir falha visual pontual;
- aplicar refatoração pequena sem impacto funcional relevante.

## Regra obrigatória de changelog

Toda alteração funcional, visual, estrutural, documental, de build, de processo ou de dados versionados deve ter arquivo Markdown correspondente em `changelogs/`.

O arquivo deve ser criado ou atualizado antes do encerramento do plano.

Nenhuma versão deve ser considerada concluída sem changelog correspondente.

## Padrão de nomenclatura

```text
changelogs/Vx.y.z.md
```

O nome do arquivo deve corresponder exatamente à versão registrada no conteúdo do changelog.

## Estrutura obrigatória do changelog

```markdown
# Changelog Vx.y.z

## Versão

`Vx.y.z`

## Data

YYYY-MM-DD

## Status da release

`em preparação`

## Tipo de release

`maior` / `menor` / `correção`

## Resumo

-

## Planos relacionados

-

## Itens criados

-

## Itens modificados

-

## Itens removidos

-

## Justificativas

-

## Arquivos afetados

-

## Impacto funcional

-

## Impacto visual

-

## Impacto técnico

-

## Riscos e regressões avaliados

-

## Validação executada

-

## Pendências conhecidas

-

## Observações de rollback

-
```

## Status permitidos para release

- `em preparação`: release em montagem, ainda sujeita a mudanças.
- `em validação`: alterações concluídas, validação em andamento.
- `publicada`: release concluída e registrada como versão oficial.
- `cancelada`: release planejada, mas não publicada.

## Tipos de release

- `maior`: incremento de `x`.
- `menor`: incremento de `y`.
- `correção`: incremento de `z`.

## Relação com planos

Cada item relevante de changelog deve apontar para um ou mais planos em `Planos/`.

- Planos concluídos devem ser citados pelo nome do arquivo.
- Planos em andamento não devem ser tratados como concluídos.
- Planos descontinuados só entram no changelog se afetaram decisões, arquivos ou escopo.

## Critérios para publicar uma versão

Uma versão só pode ser marcada como `publicada` quando:

- todos os planos incluídos estiverem em `Planos/concluído/`;
- o changelog existir e listar itens criados, modificados e removidos;
- a validação definida nos planos tiver sido executada ou a limitação estiver documentada;
- referências de versão em código, documentação e build estiverem coerentes;
- pendências conhecidas estiverem registradas;
- não houver arquivo temporário usado como fonte de verdade.

## Rollback

Quando uma release alterar código, dados persistidos, build, migração ou contratos de API, o changelog deve indicar o procedimento de rollback ou justificar por que rollback não se aplica.

## Auditoria mínima antes de concluir uma release

- Existe arquivo `changelogs/Vx.y.z.md`?
- O nome do arquivo corresponde ao campo **Versão**?
- Todos os planos citados existem e estão em `Planos/concluído/`?
- Arquivos criados, modificados e removidos foram listados?
- Justificativas e validações foram registradas?
- Pendências conhecidas estão explícitas?
