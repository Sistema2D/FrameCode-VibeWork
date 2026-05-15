# Auditoria Documental e Operacional

Documento metodológico para revisar a coerência entre documentação, planos, changelogs, versionamento, escopo, design, testes, segurança, dados e implementação.

Este arquivo deve ser consultado antes de encerrar planos relevantes, publicar versões, reorganizar documentação ou validar o estado geral do repositório.

## Objetivo

Garantir que o repositório permaneça consistente, rastreável e compreensível para humanos e agentes de IA.

## Princípios

- Documentos oficiais não devem se contradizer.
- Toda mudança em arquivo versionado deve ter changelog correspondente. Não há exceção para ajustes pequenos, documentais ou processuais.
- Planos concluídos devem corresponder a alterações realmente executadas.
- Versão exibida, versão documentada e changelog devem estar coerentes.
- Novos documentos devem ser citados no `AGENTS.md`.
- Lacunas conhecidas devem ser registradas, não escondidas.

## Tipos de auditoria

### Auditoria documental

Verifica consistência entre arquivos Markdown.

Itens:

- índice do `AGENTS.md` atualizado;
- documentos relacionados citados corretamente;
- nomes de arquivos consistentes;
- regras duplicadas sem conflito;
- ausência de instruções contraditórias;
- templates atualizados.

## Local dos registros

Este arquivo define a metodologia de auditoria. Relatórios formais de auditoria, quando criados, devem ficar em `auditorias/` na raiz da aplicação.

Sínteses reutilizáveis derivadas de auditorias podem ser registradas em `wiki/audits/`, desde que apontem para o relatório formal, plano, changelog ou documento oficial usado como fonte.

A wiki de governança não substitui relatórios formais, planos, changelogs ou documentos oficiais.

### Auditoria de versão

Verifica coerência da release.

Itens:

- versão no código;
- versão no `STACK.md`;
- changelog correspondente;
- status da release;
- planos relacionados;
- critérios de publicação.

### Auditoria de planos

Verifica consistência dos planos.

Itens:

- status interno do plano;
- pasta correta;
- prioridade e risco definidos;
- versão atual e prevista;
- critérios de aceite;
- plano de testes;
- conclusão e validação.

### Auditoria de troubleshooting

Verifica memória de falhas.

Itens:

- falhas abertas;
- falhas recorrentes;
- issues sem validação;
- soluções sem plano relacionado;
- tentativas não registradas.

### Auditoria de segurança

Verifica riscos de segurança.

Itens:

- segredos em arquivos;
- tokens em logs;
- path traversal;
- CORS ou rede local;
- permissões;
- execução de comandos;
- dados sensíveis;
- prompt injection.

### Auditoria de IA

Verifica comportamento de recursos de IA.

Itens:

- modelo indisponível;
- erro de streaming;
- fontes exibidas;
- contexto recuperado;
- limites de ação;
- memória e aprendizado;
- dados sensíveis;
- instruções conflitantes.

## Checklist mínimo de auditoria antes de release

> Este checklist é para **auditoria pré-release** (coerência do repositório como um todo). O checklist de **encerramento de tarefa** está em `AGENTS.md`.

- [ ] `AGENTS.md` cita todos os documentos oficiais relevantes.
- [ ] `STACK.md` registra a versão correta.
- [ ] Existe `changelogs/Vx.y.z.md`.
- [ ] O changelog cita planos relacionados.
- [ ] Todos os planos concluídos estão em `Planos/concluído`.
- [ ] Todos os planos em andamento estão em `Planos/em andamento`.
- [ ] Não há plano concluído sem validação.
- [ ] Não há issue resolvida sem evidência mínima.
- [ ] `DESIGN.md` reflete mudanças visuais aprovadas.
- [ ] `ESCOPO.md` reflete mudanças funcionais aprovadas.
- [ ] `WORKFLOW.md` reflete fluxos alterados.
- [ ] `DADOS.md` reflete mudanças de persistência.
- [ ] `SEGURANCA.md` reflete mudanças de segurança.
- [ ] `IA.md` reflete mudanças de IA.
- [ ] `TESTES.md` foi usado para validação compatível com o risco.
- [ ] A wiki de governança foi atualizada quando a auditoria gerou aprendizado reutilizável.
- [ ] Não há arquivos temporários sendo usados como fonte oficial.

## Checklist de auditoria rápida para agentes de IA

Antes de concluir uma resposta que envolveu alteração de arquivos, o agente deve seguir obrigatoriamente o **Checklist Antes De Finalizar Uma Alteração** localizado no final do arquivo:

`AGENTS.md`

Este checklist garante a integridade documental e técnica mínima para cada turno de trabalho.

## Template de relatório de auditoria

```markdown
# Relatório de Auditoria

## Data

YYYY-MM-DD

## Escopo da auditoria

- 

## Arquivos analisados

- 

## Resultado geral

`aprovado` / `aprovado com ressalvas` / `reprovado`

## Inconsistências encontradas

| Item | Documento/arquivo | Gravidade | Recomendação |
|---|---|---|---|
| | | | |

## Pendências

- 

## Recomendações

- 

## Validação final

- 
```
