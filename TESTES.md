# Testes e Validação

Documento metodológico para definir as regras de teste, validação e regressão da aplicação.

Este arquivo complementa `PLANEJAMENTO.md`, `TROUBLESHOOTING.md`, `VERSIONAMENTO.md`, `DESIGN.md`, `STACK.md` e `WORKFLOW.md`. Ele deve ser consultado sempre que uma alteração funcional, visual, estrutural, documental, de build, de dados, de segurança ou de IA for planejada, implementada ou publicada.

## Objetivo

Garantir que cada mudança seja validada de forma proporcional ao risco, à prioridade, ao impacto técnico e ao impacto no usuário.

Este documento não substitui os planos individuais em `Planos/`. Cada plano deve trazer seu próprio plano de testes, mas deve usar este arquivo como referência.

## Princípios gerais

- Toda alteração deve ter validação compatível com seu risco.
- Validação manual deve ser registrada quando teste automatizado não existir.
- Falha reproduzível deve gerar ou atualizar registro em `troubleshooting/`.
- Alteração publicada deve ter evidência de teste no plano e no changelog.
- Testes devem cobrir comportamento esperado, comportamento inválido e regressões prováveis.
- Nenhum teste deve depender de dados privados reais quando puder usar dados fictícios.
- Toda limitação de teste deve ser declarada explicitamente no plano e no changelog.

## Classificação dos testes por tipo de mudança

| Tipo de mudança | Testes mínimos exigidos |
|---|---|
| Documentação | Conferir links, coerência com documentos relacionados e ausência de conflito normativo |
| UI/UX | Validar tela normal, maximizada, tamanho mínimo, hover, foco, clique, estados desabilitados e contraste |
| Frontend | Build, fluxo manual da tela afetada, regressão de navegação e persistência visual |
| Backend | Compilação/verificação sintática, endpoints afetados, entradas inválidas e erro controlado |
| Persistência | Criar, ler, atualizar, excluir, corromper arquivo de teste, validar backup e migração |
| IA | Entrada simples, entrada longa, falha do modelo, ausência de modelo, contexto incorreto e limites de ação |
| Vault/RAG | Upload, leitura, busca, links, fontes, manifest, path traversal e recuperação de contexto |
| Segurança | Token, CORS, permissões, paths, segredos, logs e ações destrutivas |
| Build/release | Build limpo, execução inicial, versão exibida, changelog e arquivos de saída |
| Refatoração | Testes de não regressão, comparação de comportamento antes/depois e métrica de risco residual |

## Matriz de validação por risco

### R1 — Risco muito baixo

Validação mínima:

- revisão manual do arquivo alterado;
- conferência de consistência documental;
- registro no plano e no changelog sempre que houver alteração em arquivo versionado.

### R2 — Risco baixo

Validação mínima:

- testes manuais pontuais;
- build ou verificação sintática quando houver código;
- validação do componente diretamente afetado.

### R3 — Risco moderado

Validação mínima:

- build completo;
- teste manual do fluxo principal afetado;
- teste de pelo menos um fluxo alternativo;
- teste de regressão dos módulos relacionados;
- registro de limitações.

### R4 — Risco alto

Validação mínima:

- build completo;
- testes manuais completos do fluxo afetado;
- testes de regressão dos fluxos dependentes;
- teste de erro e recuperação;
- plano de rollback;
- registro detalhado no changelog.

### R5 — Risco crítico

Validação mínima:

- build completo;
- teste de regressão ampliado;
- validação de dados existentes;
- validação de rollback;
- avaliação explícita de segurança;
- aprovação humana antes de considerar concluído;
- changelog detalhado com riscos residuais.

## Checklist geral antes de concluir um plano

- [ ] O escopo testado corresponde ao escopo do plano.
- [ ] O comportamento esperado foi validado.
- [ ] Entradas inválidas foram avaliadas quando aplicável.
- [ ] Erros são tratados de forma segura.
- [ ] Não houve regressão perceptível em fluxos relacionados.
- [ ] A documentação foi atualizada quando necessário.
- [ ] O changelog registra a validação executada.
- [ ] Limitações de teste foram registradas.
- [ ] Pendências conhecidas foram registradas.

## Testes de frontend

Aplicável a interfaces web, desktop nativas, mobile, TUI ou híbridas.

### Critérios mínimos

- A tela abre sem erro.
- A navegação funciona.
- Estados visuais são perceptíveis.
- Campos aceitam entrada válida.
- Campos rejeitam ou tratam entrada inválida.
- Ações destrutivas pedem confirmação.
- Botões desabilitados não executam ação.
- Redimensionamento não causa sobreposição.
- Texto longo não quebra o layout.
- Ícones e tooltips continuam coerentes.

### Checklist visual

- [ ] Janela normal.
- [ ] Janela maximizada.
- [ ] Tamanho mínimo suportado.
- [ ] Tema esperado.
- [ ] Contraste adequado.
- [ ] Hover.
- [ ] Foco por teclado.
- [ ] Pressionado.
- [ ] Desabilitado.
- [ ] Erro.
- [ ] Sucesso.
- [ ] Tooltip.
- [ ] Modal.
- [ ] Scroll.

## Testes de backend

### Critérios mínimos

- Aplicação inicia.
- Endpoints principais respondem.
- Entradas inválidas retornam erro controlado.
- Falha de dependência externa não derruba o processo.
- Logs não expõem segredos.
- Operações destrutivas exigem confirmação ou proteção adequada.

### Checklist de API

- [ ] Health check.
- [ ] Endpoint com entrada válida.
- [ ] Endpoint com entrada inválida.
- [ ] Endpoint sem autorização quando aplicável.
- [ ] Endpoint com autorização quando aplicável.
- [ ] Erro de dependência.
- [ ] Timeout.
- [ ] Resposta vazia.
- [ ] Resposta grande.

## Testes de persistência

### Critérios mínimos

- Criação de dados.
- Leitura de dados.
- Atualização de dados.
- Exclusão de dados.
- Backup quando aplicável.
- Recuperação após arquivo ausente.
- Recuperação após arquivo corrompido.
- Compatibilidade com dados de versão anterior.

### Checklist

- [ ] Dados novos são salvos.
- [ ] Dados salvos são recarregados.
- [ ] Dados existentes não são perdidos.
- [ ] Arquivo ausente é recriado com segurança.
- [ ] Arquivo inválido não causa travamento sem mensagem.
- [ ] Backup é criado antes de reescrita crítica.
- [ ] Migração, se houver, é idempotente.

## Testes de IA

### Critérios mínimos

- Modelo indisponível é tratado.
- Resposta vazia é tratada.
- Resposta longa é tratada.
- Erro de streaming é tratado.
- Contexto recuperado é exibido quando aplicável.
- Fontes são rastreáveis quando aplicável.
- A IA não executa ações fora do escopo permitido.
- Prompt injection em dados recuperados é tratado como conteúdo não confiável.

### Casos recomendados

- Pergunta simples.
- Pergunta longa.
- Pergunta ambígua.
- Pergunta com tentativa de ignorar regras.
- Pergunta que exige fonte local.
- Pergunta sem fonte disponível.
- Cancelamento durante geração.
- Falha do runtime de IA.

## Testes de segurança

- [ ] Token ou autenticação quando aplicável.
- [ ] CORS ou origens permitidas quando aplicável.
- [ ] Path traversal bloqueado.
- [ ] Segredos não aparecem em log.
- [ ] Arquivos fora do diretório permitido não são acessados.
- [ ] Ações destrutivas exigem confirmação.
- [ ] Dados sensíveis não são enviados a serviços externos sem regra explícita.
- [ ] Prompt injection não altera regras de sistema.

## Testes de release

Antes de publicar uma versão:

- [ ] Todos os planos da release estão concluídos.
- [ ] O changelog existe.
- [ ] A versão exibida na aplicação está coerente.
- [ ] `STACK.md` registra a versão correta.
- [ ] Build limpo foi executado ou limitação foi registrada.
- [ ] Fluxo principal foi validado.
- [ ] Pendências conhecidas foram registradas.
- [ ] Rollback foi descrito quando aplicável.

---

## Modelos e Templates

O registro de validação e testes deve ser feito diretamente no arquivo de plano, seguindo o modelo em:
`governança/TEMPLATE_PLANO.md`
