# Template: Plano de Refatoração

Use este template para refatorações controladas (melhoria interna sem mudança funcional).

```markdown
# P<P>-R<R>-YYYY-MM-DD-refactor-<componente>

## Classificação
- Tipo: `RF1` a `RF10`
- Prioridade: `P1` a `P5`
- Risco: `R1` a `R5`
- ICR (Candidatura): 0-100
- IRR (Risco): 0-100

## Motivação
<Qual code smell ou problema estrutural justifica esta ação?>

## Comportamento externo preservado
<O que deve continuar funcionando exatamente como antes? Liste contratos e saídas.>

## Escopo
- Incluído:
- Excluído:

## Plano de implementação
1. Caracterizar comportamento (testes antes).
2. Isolar trecho.
3. Transformar.
4. Validar (testes depois).

## Plano de testes
- Antes:
- Depois:
- Regressão:

## Critérios de aceite
- [ ] Comportamento externo preservado.
- [ ] Complexidade reduzida.
- [ ] Testes aprovados.

## Rollback
<Como reverter em caso de falha?>

## Resultado final (Preencher ao concluir)
| Métrica | Antes | Depois |
|---|---|---|
| | | |
```
