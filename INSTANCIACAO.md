# Instanciação do Framework

Documento operacional para transformar o FrameCode VibeWork em uma aplicação concreta sem depender de scripts automáticos de substituição em massa.

## Objetivo

Definir como copiar, renomear, preencher e validar os arquivos do framework ao iniciar um novo projeto assistido por IA.

Este arquivo substitui qualquer regra anterior baseada em script `init.ps1`. A instanciação deve ser explícita, revisável e rastreável.

## Quando Usar

Use este documento quando:

- um novo projeto for iniciado a partir do VibeWork FrameCode;
- uma pasta clonada do framework precisar virar uma aplicação real;
- houver dúvida sobre quais arquivos devem permanecer genéricos e quais devem ser preenchidos;
- um agente de IA precisar renomear arquivos, pastas, títulos ou placeholders do framework.

## Princípios

- Não executar substituição recursiva automática em todos os arquivos.
- Não alterar templates genéricos como se fossem documentos canônicos do projeto.
- Não preencher placeholders sem evidência do briefing ou confirmação do usuário.
- Renomear apenas o que estiver dentro do escopo da instanciação.
- Registrar a mudança em plano e changelog quando a instanciação ocorrer dentro de um repositório versionado.

## Separação Entre Camadas

### Documentos canônicos do projeto

Ficam na raiz do projeto e devem ser preenchidos com dados reais da aplicação:

- `README.md`
- `MANIFESTO.md`
- `STACK.md`
- `ESCOPO.md`
- `DESIGN.md`, quando houver UI
- `WORKFLOW.md`
- `DADOS.md`, quando houver persistência
- `IA.md`, quando houver recursos de IA
- `AGENTS.md`

### Templates do framework

Devem permanecer genéricos e reutilizáveis:

- `governança/`
- `wiki/templates/`
- snippets reutilizáveis em `snippets/`, exceto quando a identidade visual do projeto exigir adaptação planejada.

## Regras de Renomeação

### Nome da pasta do projeto

- Use nome curto em `kebab-case`, sem espaços.
- Prefira caracteres ASCII no nome da pasta para evitar problemas em ferramentas de build, scripts e CI.
- Exemplo: `meu-produto`, `controle-financeiro`, `assistente-juridico`.

### Títulos de documentos

- Substitua títulos genéricos apenas nos documentos canônicos da raiz.
- Preserve prefixos técnicos quando eles identificarem o papel do arquivo, por exemplo `AGENTS.md`, `STACK.md` e `DESIGN.md`.
- Não renomeie arquivos oficiais sem atualizar `AGENTS.md`, `MANIFESTO.md` e referências cruzadas.

### Placeholders

- Substitua placeholders como `<nome do projeto>`, `<tecnologia>`, `<objetivo>` e `<risco>` somente quando houver resposta no briefing, decisão registrada ou confirmação direta do usuário.
- Se a informação ainda não existir, registre a lacuna em `BRIEFING.md`, `MANIFESTO.md` ou `wiki/questions/`.
- Não substitua placeholders dentro de `governança/` e `wiki/templates/`, pois eles são modelos reutilizáveis.

### Versão inicial

- Defina a versão inicial no `MANIFESTO.md`, `STACK.md` e primeiro changelog.
- Use `V0.1.0` quando houver escopo inicial usável.
- Use `V0.0.1` quando a mudança for apenas estrutural, documental ou preparatória.

### README da raiz

- O `README.md` da raiz deve descrever a aplicação instanciada, não o framework genérico.
- Use `governança/README_FRAMEWORK.md` apenas como referência técnica sobre o VibeWork FrameCode.
- Se o repositório for o próprio framework, o `README.md` pode continuar descrevendo o framework.

## Fluxo De Instanciação

1. Ler `AGENTS.md`, este arquivo e `BRIEFING.md`.
2. Confirmar se o diretório atual é o framework original ou uma aplicação derivada.
3. Registrar ou atualizar plano em `Planos/`.
4. Preencher `BRIEFING.md` com as respostas conhecidas.
5. Atualizar `MANIFESTO.md`, `STACK.md`, `ESCOPO.md` e `README.md`.
6. Remover seções não aplicáveis nos documentos canônicos.
7. Criar ou atualizar `changelogs/Vx.y.z.md`.
8. Validar placeholders remanescentes fora de templates.
9. Atualizar `wiki/index.md` e `wiki/log.md` se a instanciação gerar aprendizado reutilizável.
10. Concluir o plano e mover para a pasta de status final.

## Validação Recomendada

Antes de encerrar a instanciação:

- verificar que nenhum script de bootstrap removido é citado como obrigatório;
- buscar placeholders fora de `governança/`, `wiki/templates/` e snippets;
- confirmar que `README.md` descreve o alvo correto;
- confirmar que `AGENTS.md` lista documentos oficiais existentes;
- confirmar que planos e changelogs foram criados ou atualizados;
- verificar que `.gitignore` cobre caches, builds, logs e dados privados.

## Regra Final

Instanciação não é uma substituição textual global. É uma migração controlada de um framework genérico para um projeto específico, com revisão dos arquivos afetados, rastreabilidade por plano e changelog, e preservação dos templates reutilizáveis.
