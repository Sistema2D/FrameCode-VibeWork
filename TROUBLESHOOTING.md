# Troubleshooting e Histórico de Issues

Este documento define as regras para registrar, consultar, atualizar e encerrar falhas identificadas na aplicação.

O objetivo é manter um histórico técnico das falhas e tratativas para que desenvolvedores humanos e agentes de IA possam consultar ocorrências anteriores, reutilizar soluções já validadas e evitar repetir tentativas que não funcionaram.

## Regra mandatória de consulta

Antes de iniciar qualquer tratativa de falha, bug, comportamento inesperado, erro de build, erro de execução, regressão visual, problema de persistência ou falha de integração, a pasta `troubleshooting/` deve ser consultada.

A consulta deve buscar:

- falhas com sintomas semelhantes;
- arquivos ou módulos afetados em ocorrências anteriores;
- hipóteses já testadas;
- tentativas que falharam;
- soluções já aplicadas;
- validações necessárias para confirmar a correção.

Quando uma falha similar já estiver documentada, a nova tratativa deve reutilizar o aprendizado registrado e atualizar o arquivo existente se for a mesma ocorrência ou recorrência direta.

## Relação com planos de alteração

O registro em `troubleshooting/` não substitui os planos formais de alteração definidos em `PLANEJAMENTO.md`.

Quando a solução de uma falha exigir mudança funcional, visual, estrutural, documental ou de configuração, deve existir um plano correspondente em `Planos/` antes da alteração ser aplicada.

Fluxo recomendado:

1. Consultar `troubleshooting/`.
2. Registrar ou atualizar a issue em `troubleshooting/`.
3. Criar ou localizar o plano correspondente em `Planos/`.
4. Executar a mudança conforme a metodologia de planejamento.
5. Atualizar a issue com as tratativas, resultado e validação.
6. Encerrar a issue somente após confirmação objetiva.

Quando uma falha gerar aprendizado reutilizável, a `wiki/` de governança deve ser avaliada para receber uma síntese em `wiki/failures/` ou `wiki/patterns/`.

## Local dos registros

```text
troubleshooting/
```

Cada falha deve ser documentada em um arquivo Markdown próprio.

## Padrão de nomenclatura

```text
YYYY-MM-DD-descricao-curta-da-falha.md
```

O status da issue deve ficar dentro do arquivo, não depender apenas do nome.

## Status permitidos

- `em aberto`: falha registrada, ainda sem análise conclusiva.
- `em análise`: falha em investigação, com reprodução, logs ou hipóteses em andamento.
- `em tratativa`: solução em implementação ou teste.
- `aguardando validação`: correção aplicada, aguardando confirmação.
- `resolvido`: falha corrigida e validada.
- `recorrente`: falha voltou a ocorrer após tratativa anterior.
- `descartado`: registro encerrado por não se confirmar como falha, por ficar fora de escopo ou por ter sido substituído.

## Estrutura mínima de uma issue

```markdown
# Título da issue

## Status

`em aberto`

## Data de identificação

YYYY-MM-DD

## Data de resolução

Não aplicável.

## Versão da aplicação

`Vx.y.z`

## Ambiente

- Sistema operacional:
- Build:
- Observações do ambiente:

## Resumo

Descrição curta do problema.

## Descrição detalhada

Contexto, sintomas e condições em que a falha ocorre.

## Passos para reproduzir

1.
2.
3.

## Comportamento esperado

-

## Comportamento observado

-

## Impacto

-

## Arquivos, módulos ou telas possivelmente afetados

-

## Evidências

- Logs:
- Mensagens de erro:
- Observações visuais:

## Hipóteses

-

## Tratativas tentadas

### Tentativa 1 — YYYY-MM-DD HH:MM

- Ação:
- Resultado:
- Funcionou: `sim` / `não` / `parcial`
- Observações:

## Resultado das tratativas

-

## Solução aplicada

Não aplicável enquanto a issue estiver em aberto.

## Plano relacionado

-

## Validação executada

-

## Prevenção ou recomendações futuras

-

## Observações técnicas

-
```

## Registro de tratativas

Todas as tratativas devem ser registradas, inclusive as que não funcionaram.

Cada tentativa deve indicar: data e hora aproximada, ação executada, resultado observado, se funcionou ou falhou e nova hipótese gerada.

Não apague tentativas antigas. Quando uma hipótese for descartada, registre o motivo.

## Critérios para encerrar uma issue

Uma issue só pode ser marcada como `resolvido` quando:

- a causa provável ou confirmada estiver documentada;
- a solução aplicada estiver descrita;
- houver validação objetiva;
- os testes relevantes tiverem sido executados ou a limitação estiver registrada;
- o plano relacionado estiver concluído, quando a solução tiver exigido alteração formal.

## Evidências e logs

Regras:

- não registrar tokens, segredos ou credenciais;
- não registrar dados privados do usuário;
- remover ou anonimizar caminhos pessoais quando não forem necessários;
- resumir logs longos em vez de colar conteúdo excessivo;
- preservar mensagens de erro com fidelidade suficiente para busca futura.

## Consulta recomendada

Antes de iniciar uma nova tratativa, use busca textual em `troubleshooting/`.

Exemplos:

```powershell
rg -n "<sintoma ou módulo>" troubleshooting
rg -n "<sintoma ou módulo>" Planos
```

## Responsabilidade de agentes de IA

Agentes de IA devem:

- consultar `troubleshooting/` antes de propor correção de falha;
- registrar novas falhas quando identificadas durante análise, implementação ou testes;
- atualizar tratativas com resultados reais dos comandos executados;
- não declarar uma issue como resolvida sem validação objetiva;
- criar plano formal em `Planos/` antes de aplicar mudanças na aplicação;
- preservar o histórico de tentativas, inclusive as malsucedidas.
