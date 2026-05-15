# REFATORACAO.md

Regras, critérios e métricas para refatoração de aplicações assistidas por IA.

Este documento é um guia metodológico agnóstico de stack. Aplicável a aplicações web, desktop, mobile, serviços backend, APIs, bibliotecas, aplicações Windows nativas, sistemas com IA local e sistemas com IA em nuvem.

> Para métricas detalhadas (ICR/IRR completos, tabelas de complexidade, exemplos comentados e referências bibliográficas), consulte `wiki/refactorings/guia-completo.md`.

## 1. Objetivo

Estabelecer regras, critérios e fluxos para refatorações controladas, rastreáveis e seguras.

Ajudar humanos e agentes de IA a decidir: quando refatorar, qual tipo aplicar, qual o risco, quais evidências exigir, como testar e como documentar.

## 2. Princípio central

Refatoração é a melhoria da estrutura interna sem alteração intencional do comportamento externo observável.

- Não altera funcionalidades percebidas pelo usuário.
- Não muda contratos públicos sem plano de mudança funcional.
- Não modifica regras de negócio.
- Não altera dados persistidos sem plano de migração.
- É feita em passos pequenos, verificáveis e reversíveis sempre que possível.

Se o comportamento externo precisar mudar, a alteração não é apenas refatoração — deve ser classificada como mudança funcional, correção, migração ou evolução arquitetural.

## 3. Relação com os demais documentos

- `AGENTS.md`: conduta geral, precedência de instruções, obrigatoriedade de planos e changelog.
- `PLANEJAMENTO.md`: criação do plano, prioridade, risco, critérios de aceite e testes.
- `VERSIONAMENTO.md`: incremento de versão, changelog, rollback.
- `TROUBLESHOOTING.md`: consultar quando refatoração estiver ligada a falhas ou regressões.
- `DESIGN.md`: consultar quando a refatoração afetar interface ou componentes visuais.
- `WORKFLOW.md`: atualizar quando a refatoração alterar fluxo operacional.
- `ESCOPO.md`: atualizar apenas se a refatoração revelar ou exigir mudança formal de escopo.

## 4. Regra mandatória

Nenhuma refatoração que altere arquivos deve ser aplicada sem plano em `Planos/`.

O plano deve conter: motivo, tipo, comportamento externo preservado, arquivos afetados, risco, estratégia de testes antes e depois, critérios de aceite, rollback quando aplicável, versão atual, versão prevista e changelog correspondente.

## 5. O que é refatoração

- Extrair função, método, classe, componente, serviço ou módulo.
- Renomear elementos internos para aumentar clareza.
- Remover duplicação.
- Reduzir complexidade condicional.
- Separar responsabilidades.
- Melhorar coesão e reduzir acoplamento.
- Reorganizar pastas e módulos sem mudar contratos públicos.
- Centralizar constantes, tokens, configurações ou utilitários.
- Encapsular acesso a dados, API, estado global ou recursos externos.
- Tornar código mais testável.

## 6. O que não é refatoração

Não classifique como refatoração isolada: criação de funcionalidade, mudança de regra de negócio, alteração de layout visível, mudança de contrato de API, migração de banco, troca de stack, reescrita ampla, correção de bug que altera saída, remoção de funcionalidade ou mudança de permissões/segurança.

## 7. Objetivos válidos de refatoração

Válidos: reduzir complexidade, duplicação, acoplamento; melhorar coesão, legibilidade, testabilidade; preparar para mudança planejada; remover dívida técnica documentada.

Inválidos: "melhorar tudo", "deixar mais moderno" sem critério, "reescrever porque está feio", "aplicar padrão de projeto sem necessidade concreta".

## 8. Sinais que motivam refatoração

- **Complexidade**: muitas responsabilidades, condicionais aninhadas, variáveis globais excessivas.
- **Duplicação**: blocos semelhantes repetidos, regras duplicadas em frontend/backend.
- **Baixa coesão**: módulo mistura UI, regra de negócio, persistência, rede e validação.
- **Alto acoplamento**: mudança pequena afeta muitos arquivos; dependências circulares.
- **Fragilidade**: falhas recorrentes no mesmo módulo; correções causaram regressões anteriores.
- **Obsolescência**: arquitetura não suporta evolução planejada; decisões temporárias viraram padrão.

## 9. Quando evitar refatoração

Evite quando: não houver critério claro de sucesso; não houver validação possível; o sistema estiver instável por falha não compreendida; a mudança misturar muitas intenções; a motivação for apenas estética; a refatoração não for necessária para a correção pedida.

## 10. Tipos de refatoração

| Código | Tipo | Descrição |
|---|---|---|
| RF1 | Local | Trecho pequeno e isolado (extrair função, renomear) |
| RF2 | Componente | Componente, classe, tela ou módulo específico |
| RF3 | Transversal | Utilitários, padrões ou código compartilhado |
| RF4 | Arquitetural | Fronteiras internas ou organização de camadas |
| RF5 | Preparatória | Prepara para mudança futura já planejada |
| RF6 | Corretiva | Reduz fragilidade ligada a bug ou issue |
| RF7 | Testes | Melhora estrutura de testes sem alterar produção |
| RF8 | Visual interna | Reorganiza código de UI sem mudar aparência aprovada |
| RF9 | Dados | Reorganiza acesso a dados sem mudar conteúdo persistido |
| RF10 | Build/infraestrutura | Organiza scripts, pipelines ou configuração |

## 11. Escala de prioridade

| Prioridade | Use quando |
|---|---|
| P1 | Estrutura causa risco de perda de dados, falha grave ou bloqueia correção essencial |
| P2 | Afeta fluxo principal, estabilidade, manutenção frequente ou evolução planejada |
| P3 | Dificulta manutenção, testes ou evolução, mas não compromete operação imediata |
| P4 | Melhora clareza ou organização com baixo impacto |
| P5 | Desejável, experimental ou preventiva, sem impacto claro no curto prazo |

## 12. Escala de risco

| Risco | Critério |
|---|---|
| R1 | Alteração local, sem contrato público, sem persistência, sem integração |
| R2 | Limitada a um componente ou módulo, com testes pontuais suficientes |
| R3 | Fluxo relevante, arquivo compartilhado ou módulo com dependências |
| R4 | Estado global, persistência, integração, contratos internos ou múltiplos módulos |
| R5 | Arquitetura central, segurança, migração, dados críticos ou fluxo principal amplo |

Refatorações R4 e R5 devem ter rollback explícito e validação de regressão ampliada.

> Para os índices ICR (Candidatura) e IRR (Risco) com pontuação detalhada, consulte `wiki/refactorings/guia-completo.md`.

## 13. Code smells prioritários

| Smell | Sinal | Ação comum |
|---|---|---|
| Código duplicado | mesma lógica em dois ou mais pontos | extrair função, criar utilitário |
| Método longo | rotina extensa e difícil de entender | extrair método, decompor condição |
| Classe grande | muitas responsabilidades | extrair classe, dividir módulo |
| Dados primitivos obsessivos | regras implícitas em strings/números | criar tipo, enum ou constante semântica |
| Mudança divergente | módulo muda por motivos diferentes | separar responsabilidades |
| Cirurgia com escopeta | uma mudança exige muitos ajustes | centralizar regra ou contrato |
| Código morto | trecho não usado ou obsoleto | remover com validação e changelog |
| Condicionais complexas | muitas variações por tipo/estado | estratégia, tabela de decisão ou mapa de handlers |
| Estado global excessivo | muitos pontos leem/escrevem estado | encapsular, criar store ou serviço |
| Dependência oculta | ordem implícita de chamada | tornar dependência explícita |

## 14. Critérios de entrada e bloqueio

### Entrada — verificar antes de iniciar

- Existe plano em `Planos/` com motivação e comportamento preservado descritos.
- Arquivos afetados listados e risco classificado.
- Estratégia de teste antes e depois definida.
- Rollback documentado para R4/R5.
- Issues relacionadas consultadas em `troubleshooting/`.
- Escopo suficientemente pequeno para revisão.

### Bloqueio — parar ou reformular se

- Não for possível explicar o comportamento externo preservado.
- Não houver validação mínima possível.
- A refatoração estiver misturada com nova funcionalidade sem justificativa.
- A alteração exigir migração de dados não planejada.
- O risco for R4/R5 sem rollback ou estratégia de contenção.
- A alteração puder expor dados sensíveis ou credenciais.

## 15. Tamanho recomendado dos lotes

| Lote | Recomendação |
|---|---|
| 1 arquivo ou 1 unidade lógica | Preferencial |
| Poucos arquivos do mesmo módulo | Aceitável com testes claros |
| Múltiplos módulos ou camadas | Dividir em fases |
| Arquitetura, dados ou contratos globais | Tratar como mudança arquitetural |

Regra: se o plano exigir muitas frases para explicar o que permanece igual, o lote está grande demais.

## 16. Estratégias seguras

1. **Caracterizar antes de modificar**: registrar comportamento atual via testes de caracterização, snapshots, checklist manual ou comparação de saída.
2. **Passos pequenos**: entender → validar → isolar trecho → transformar → testar → registrar → repetir.
3. **Separar estrutural de comportamental**: nunca misturar refatoração com nova funcionalidade, correção, redesign, troca de biblioteca ou migração no mesmo passo.
4. **Preservar contratos**: identificar entradas, saídas, eventos, formatos de arquivo e compatibilidade antes de alterar internamente.
5. **Evitar especulação**: refatoração preparatória só é aceitável quando vinculada a plano aprovado ou risco documentado.

## 17. Métricas por tipo de aplicação

### Aplicações web

Avaliar: componentes grandes ou com responsabilidades misturadas; lógica de negócio em componentes visuais; chamadas HTTP espalhadas; tratamento de erro inconsistente; CSS duplicado ou fora do design system.

### Aplicações Windows nativas ou desktop

Avaliar: concentração excessiva de lógica em janela principal; handlers de eventos muito grandes; mensagens, timers e estados globais difíceis de rastrear; recursos do SO sem encapsulamento; inconsistência entre área clicável e área desenhada.

Ao instanciar o framework, registrar aqui módulos, eventos ou fluxos específicos do projeto que exigem atenção especial.

### Backends, APIs e serviços

Avaliar: rotas com regra de negócio embutida; validação duplicada; DTOs implícitos; tratamento de exceções inconsistente; queries espalhadas; contratos de API sem testes.

### Aplicações com IA

Avaliar: prompts espalhados e sem versionamento; ausência de fronteira entre sistema, usuário e contexto; parsing de JSON de modelo sem validação; ausência de fallback; risco de prompt injection; falta de separação entre dados do usuário, contexto recuperado e instruções do sistema.

### Aplicações com persistência local

Avaliar: escrita não atômica; ausência de backup; ausência de migração; dados versionados misturados com dados do usuário; paths não validados; ausência de compatibilidade com versões anteriores.

## 18. Testes mínimos por risco

| Risco | Testes mínimos |
|---|---|
| R1 | build ou lint, teste manual do trecho afetado |
| R2 | testes pontuais, validação manual do componente |
| R3 | testes do módulo, regressão do fluxo afetado, comparação antes/depois |
| R4 | testes ampliados, regressão de fluxos principais, validação de dados, rollback documentado |
| R5 | plano faseado, caracterização forte, validação de migração, rollback, revisão humana recomendada |

## 19. Critérios de aceite

Uma refatoração só pode ser considerada concluída quando:

- o comportamento externo preservado foi validado;
- os testes definidos no plano foram executados ou a limitação foi registrada;
- a complexidade, duplicação ou outro problema-alvo foi reduzido ou justificado;
- não foram introduzidas mudanças funcionais não planejadas;
- não houve regressão conhecida nos fluxos afetados;
- os documentos impactados foram atualizados;
- o changelog registra o que mudou, por que mudou e como foi validado;
- o plano foi atualizado com resultado e status final.

## 20. Checklists

### Antes de refatorar

- [ ] A alteração é realmente refatoração?
- [ ] O comportamento externo preservado está descrito?
- [ ] Existe plano em `Planos/`?
- [ ] O plano indica tipo, prioridade e risco?
- [ ] Há critério objetivo de sucesso?
- [ ] Há plano de testes?
- [ ] Há rollback para R4/R5?
- [ ] `TROUBLESHOOTING.md` foi consultado se houver relação com falha?
- [ ] `DESIGN.md` foi consultado se houver impacto em UI?
- [ ] `WORKFLOW.md` será atualizado se houver impacto em fluxo?

### Durante a refatoração

- [ ] Alterar em pequenos passos.
- [ ] Evitar misturar comportamento novo.
- [ ] Executar validação incremental.
- [ ] Preservar contratos públicos.
- [ ] Não remover código sem confirmar que está morto ou substituído.
- [ ] Não alterar dados persistidos sem plano próprio.
- [ ] Não ampliar escopo sem atualizar o plano.

### Após a refatoração

- [ ] Build, lint ou verificação equivalente executada.
- [ ] Testes definidos no plano executados.
- [ ] Fluxos afetados validados.
- [ ] Comportamento externo preservado confirmado.
- [ ] Changelog atualizado.
- [ ] Plano atualizado com resultado final.
- [ ] Documentação impactada atualizada.
- [ ] Pendências conhecidas registradas.
- [ ] Rollback documentado quando aplicável.

## 21. Modelos e Templates

Para criar planos de refatoração, utilize o modelo em:
`governança/TEMPLATE_REFATORACAO.md`

## 22. Regras para agentes de IA

Ao receber pedido de refatoração, a IA deve:

1. Identificar se é análise, planejamento ou alteração real.
2. Se for alteração real, localizar ou criar plano antes de modificar arquivos.
3. Declarar o comportamento externo que deve ser preservado.
4. Classificar tipo, prioridade e risco.
5. Verificar documentos relacionados.
6. Propor divisão em fases se o risco for alto.
7. Evitar mudanças funcionais não solicitadas.
8. Executar validações compatíveis com a stack.
9. Atualizar changelog e documentação impactada.
10. Registrar limitações quando não conseguir testar tudo.

A IA não deve: reescrever módulos inteiros sem justificativa; mudar comportamento externo sem avisar; remover código por parecer inútil sem evidência; aplicar padrões de projeto por preferência; ignorar testes porque a alteração "parece simples".

Quando a refatoração for R3/R4/R5, a IA deve responder ou perguntar: qual problema estrutural será resolvido; qual comportamento deve permanecer igual; quais arquivos serão afetados; há testes ou validação confiável; há histórico de falhas; como será feito rollback; qual é o menor lote seguro.

## 23. Regra final

Refatoração boa é aquela que torna o software mais simples de entender, testar, modificar e evoluir, sem surpreender o usuário, sem quebrar contratos e sem esconder mudança funcional dentro de reorganização técnica.

Quando houver dúvida entre refatorar agora ou preservar estabilidade, priorize estabilidade, evidência e rastreabilidade.
