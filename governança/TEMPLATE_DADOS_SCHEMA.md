# Template: Registro de Schema de Dados

Copie este conteúdo ao definir um novo formato de persistência (JSON, banco, CSV, etc.).

```markdown
# Schema: <Nome do dado>

## Versão do schema

`1`

## Arquivo ou tabela

- Caminho/tabela: `<caminho>`

## Finalidade

- <Descreva para que serve este dado.>

## Campos

| Campo | Tipo | Obrigatório | Valor padrão | Descrição |
|---|---|---|---|---|
| | | | | |

## Regras de validação

- <Ex: campos não nulos, formato de data, etc.>

## Migrações

| Origem | Destino | Descrição | Rollback |
|---|---|---|---|
| | | | |

## Dados sensíveis

- <Liste se há tokens, nomes, emails ou dados privados.>

## Observações

- <Notas adicionais sobre integridade ou performance.>
```
