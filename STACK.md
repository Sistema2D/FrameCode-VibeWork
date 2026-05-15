# Stack

> Este é um modelo. Substitua os campos entre `<...>` pelas informações reais do projeto.

## Aplicacao

- Nome: `<nome do projeto>`
- Versao atual: `V0.0.0`
- Tipo: `<web / desktop / mobile / CLI / API / biblioteca / híbrida>`
- Plataforma alvo: `<Windows / Linux / macOS / Web / multiplataforma>`
- Objetivo: `<resumo em uma linha>`

## Frontend

`<Remover se não houver UI.>`

- Linguagem: `<tecnologia>`
- Framework / UI toolkit: `<framework ou API>`
- Build: `<ferramenta de build>`
- Compilador / bundler: `<compilador ou bundler>`
- Bibliotecas principais: `<lista>`

## Backend

`<Remover se não houver backend separado.>`

- Linguagem: `<tecnologia>`
- Framework HTTP: `<framework>`
- Porta local: `<endereço e porta>`
- Seguranca local: `<token, autenticação ou CORS>`
- Módulos principais: `<lista>`

## IA local ou remota

`<Remover se não houver IA.>`

- Runtime / model server: `<Ollama / OpenAI / outro>`
- API: `<endpoint>`
- Recursos usados: `<listagem, chat, embeddings, etc.>`
- Aprendizado contínuo: `<descrever ou "não aplicável">`

## Vault / Base de conhecimento

`<Remover se não houver vault ou RAG.>`

- Diretório local: `<caminho>`
- Formato: `<Markdown / JSON / outro>`
- Estrutura principal: `<schema.md, index.md, log.md, raw/, notes/, etc.>`

## Build e execucao

- Script de build: `<comando ou arquivo>`
- Script de execução: `<comando ou arquivo>`
- Saída principal: `<caminho do artefato>`

## Build matrix

`<Remover se o projeto não for multiplataforma.>`

| Plataforma / SO | Compilador / runtime | Flags ou variantes | Status |
|---|---|---|---|
| `<Windows x64>` | `<MSVC / MinGW / clang>` | `<Release / Debug>` | `<suportado>` |
| `<Linux x64>` | `<GCC / clang>` | `<Release>` | `<suportado>` |

## Persistencia e logs

- Dados do usuário: `<caminho e formato>`
- Configurações: `<caminho e formato>`
- Logs: `<pasta ou mecanismo>`
- Estratégia de escrita: `<atômica / backup / direto>`
- Dados ignorados pelo Git: `<logs, builds, vault, dados privados>`

## Governanca documental

- Documentos oficiais preenchidos: arquivos Markdown na raiz da aplicação.
- Modelos vazios reutilizáveis: pasta `governança/`.
- Memória técnica de governança: pasta `wiki/`.
- Registros formais: `Planos/`, `changelogs/`, `troubleshooting/`.
- Instanciação e renomeação: `INSTANCIACAO.md`.
- Exclusões de versionamento: `.gitignore`.
- Changelog obrigatório: toda alteração em arquivo versionado deve ser registrada em `changelogs/Vx.y.z.md`.
