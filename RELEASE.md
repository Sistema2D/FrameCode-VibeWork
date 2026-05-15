# Release e Publicação

Documento operacional para preparar, validar e publicar versões da aplicação.

Este arquivo complementa `VERSIONAMENTO.md`. Enquanto `VERSIONAMENTO.md` define regras de versão e changelog, este documento descreve o fluxo prático de preparação de uma release.

O changelog em `changelogs/Vx.y.z.md` é a fonte formal da release. Este documento não cria uma fonte paralela de versão.

## Objetivo

Padronizar o encerramento de versões, evitando publicação com planos incompletos, versão inconsistente, changelog incompleto, testes ausentes ou pendências desconhecidas.

## Estados de uma release

- `planejada`: versão prevista, ainda sem alterações concluídas.
- `em preparação`: alterações sendo agrupadas e documentadas.
- `em validação`: implementação concluída, testes em execução.
- `publicada`: versão finalizada.
- `cancelada`: versão planejada que não será publicada.

## Fluxo recomendado

1. Identificar planos que compõem a release.
2. Confirmar versão prevista.
3. Garantir que cada plano tem status correto.
4. Atualizar changelog da versão.
5. Executar testes conforme `TESTES.md`.
6. Executar auditoria conforme `AUDITORIA.md`.
7. Confirmar coerência de versão em código, `STACK.md` e changelog.
8. Registrar pendências conhecidas.
9. Registrar rollback quando aplicável.
10. Marcar changelog como `publicada`.
11. Avaliar se a release gerou aprendizado reutilizável para `wiki/releases/`.

## Critérios mínimos para publicar

- Todos os planos incluídos estão concluídos ou explicitamente removidos da release.
- Changelog existe e está completo.
- Versão exibida na aplicação está coerente.
- Versão em `STACK.md` está coerente.
- Testes mínimos foram executados.
- Pendências conhecidas foram registradas.
- Riscos residuais foram registrados.
- Rollback foi descrito ou justificado como não aplicável.

## Checklist de pré-release

- [ ] A versão prevista segue `Vx.y.z`.
- [ ] O tipo de release foi definido.
- [ ] Planos relacionados foram listados.
- [ ] Changelog foi criado.
- [ ] Arquivos afetados foram listados.
- [ ] Testes foram definidos.
- [ ] Validação foi executada ou limitação foi registrada.
- [ ] Pendências conhecidas foram registradas.
- [ ] Rollback foi registrado quando aplicável.
- [ ] Auditoria documental foi executada.

## Checklist de publicação

- [ ] Build final executado.
- [ ] Aplicação inicia.
- [ ] Fluxo principal funciona.
- [ ] Versão exibida confere.
- [ ] Changelog está como `publicada`.
- [ ] Planos estão em `Planos/concluído`.
- [ ] Não há arquivos temporários como fonte de verdade.
- [ ] Artefatos de build não foram versionados indevidamente.

## Checklist pós-release

- [ ] Próximas pendências foram registradas em planos futuros, se aplicável.
- [ ] Issues recorrentes foram revisadas.
- [ ] Documentos oficiais permanecem coerentes.
- [ ] Riscos residuais foram comunicados.
- [ ] Versão seguinte não foi iniciada sem plano.

---

## Modelos e Templates

Para criar notas de release ou resumos executivos, utilize o modelo em:
`governança/TEMPLATE_RELEASE.md`
