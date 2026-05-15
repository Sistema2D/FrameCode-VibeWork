# Planejamento de Alterações

## Objetivo

Definir a metodologia obrigatória para planejar alterações antes de qualquer modificação em código, documentação, configuração, build, testes ou dados versionados.

Planos individuais ficam em `Planos/{status}`. Este arquivo é metodologia, não lista de tarefas.

## Regra mandatória

Nenhuma alteração deve ser aplicada sem plano correspondente em `Planos/`.

Sequência obrigatória antes de qualquer mudança:

1. Identificar a alteração necessária.
2. Criar arquivo de plano em `Planos/pendente/`.
3. Classificar prioridade (`P1`–`P5`) e risco (`R1`–`R5`).
4. Registrar versão atual e versão prevista.
5. Descrever plano de implementação, critérios de aceite e plano de testes.
6. Mover para `Planos/em andamento/` ao iniciar.
7. Aplicar somente o escopo do plano.
8. Criar ou atualizar `changelogs/Vx.y.z.md`.
9. Validar critérios de aceite.
10. Atualizar plano com resultado e mover para `Planos/concluído/` ou `Planos/descontinuado/`.

---

## Modelos e Templates

Para criar novos planos de alteração, utilize o modelo em:
`governança/TEMPLATE_PLANO.md`

Quando aplicável, incluir também: análise de segurança (`SEGURANCA.md`), dados e migração (`DADOS.md`), impacto de IA (`IA.md`), decisão arquitetural (`DECISOES_ARQUITETURAIS.md`), atualização esperada da `wiki/`.

## Padrão de nomenclatura

```text
P{prioridade}-R{risco}-{data}-{descricao-curta}.md
```

Exemplos:

```text
P1-R4-2026-05-13-correcao-persistencia-dados.md
P3-R2-2026-05-13-ajuste-interface-dashboard.md
```

## Escala de prioridade

| Prioridade | Nome | Usar quando |
|---|---|---|
| P1 | Crítica | segurança, integridade de dados, falhas que impedem o uso |
| P2 | Alta | fluxo principal, estabilidade, funcionalidades relevantes |
| P3 | Média | melhorias funcionais, organização, usabilidade |
| P4 | Baixa | ajustes visuais, textos, pequenas refatorações |
| P5 | Opcional | ideias futuras, melhorias experimentais |

## Escala de risco

| Risco | Nome | Usar quando |
|---|---|---|
| R1 | Muito baixo | apenas textos, estilos, sem lógica ou dados |
| R2 | Baixo | componente isolado, lógica simples, testes pontuais |
| R3 | Moderado | lógica compartilhada, fluxos importantes, regressão possível |
| R4 | Alto | persistência, estados globais, integrações, refatoração relevante |
| R5 | Crítico | segurança, arquitetura, autenticação, migração, risco de perda de dados |

## Organização das pastas

```text
Planos/
├── pendente/
├── em andamento/
├── concluído/
└── descontinuado/
```

Cada arquivo deve estar na pasta correspondente ao campo **Status** do plano. Ao mudar o status, mover o arquivo para a subpasta correta.

## Relação com governança documental

Mudanças nos documentos oficiais da raiz e em modelos de `governança/` seguem a mesma metodologia.

Quando uma alteração modificar a estrutura de um documento oficial, avaliar se o modelo vazio correspondente em `governança/` precisa ser atualizado com a mesma estrutura, sem dados específicos do projeto.

A `wiki/` pode ser atualizada quando a mudança gerar aprendizado reutilizável. Essa atualização não substitui planos, changelogs, troubleshooting ou documentos oficiais.
