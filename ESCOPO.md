# ESCOPO.md

Escopo geral da aplicação conforme o estado atual do projeto.

Este documento descreve a finalidade, os limites, os módulos, as telas e os conteúdos principais da aplicação. Ele não substitui `README.md`, `STACK.md`, `DESIGN.md` ou `PLANEJAMENTO.md`; seu papel é consolidar a visão de escopo funcional para orientar análise, planejamento e evolução futura.

> Este é um modelo. Substitua os campos entre `<...>` pelas informações reais do projeto.

## Visão Geral

`<Descreva em duas ou três frases o que a aplicação é, sua stack principal e seu contexto de execução.>`

## Objetivo Geral

`<Descreva o objetivo principal da aplicação em uma ou duas frases.>`

## Objetivos Específicos

- `<objetivo 1>`
- `<objetivo 2>`
- `<objetivo 3>`

## Limites Do Escopo Atual

- `<limite 1>`
- `<limite 2>`
- `<limite 3>`

## Arquitetura Em Alto Nível

### Frontend

`<Descreva a tecnologia, responsabilidades principais e arquivos relevantes. Remover se não aplicável.>`

### Backend

`<Descreva o framework, porta local, endpoints principais e módulos relevantes. Remover se não aplicável.>`

### IA Local ou Remota

`<Descreva o runtime, as funções da IA na aplicação e os limites de uso. Remover se não aplicável.>`

### Vault / Base de Conhecimento

`<Descreva o local, o formato e a estrutura. Remover se não aplicável.>`

## Módulos E Telas

### `<Nome do módulo ou tela 1>`

Objetivo: `<objetivo>`

Conteúdo e recursos:

- `<item 1>`
- `<item 2>`

### API Pública e Contratos Exportados

`<Remover quando não for biblioteca ou SDK.>`

`<Descreva os contratos que consumidores externos enxergam: funções exportadas, endpoints públicos, eventos, schemas ou interfaces. Mudanças aqui exigem incremento de versão major.>`

### `<Nome do módulo ou tela 2>`

Objetivo: `<objetivo>`

Conteúdo e recursos:

- `<item 1>`
- `<item 2>`

## Componentes Transversais

### Navegação

`<Descreva como o usuário navega entre telas ou módulos.>`

### Persistência Local

`<Descreva quais dados são persistidos, onde e em qual formato.>`

### Segurança Local

`<Descreva controles de autenticação, token local, CORS e validação de caminhos.>`

### Build E Execução

`<Descreva como fazer build e executar a aplicação.>`

### Governança Documental

A aplicação mantém uma camada documental versionada para orientar planejamento, implementação, validação, release e aprendizado contínuo do próprio projeto.

Componentes principais:

- documentos oficiais na raiz do repositório;
- planos em `Planos/{status}`;
- changelogs em `changelogs/`;
- registros de falhas em `troubleshooting/`;
- wiki de governança em `wiki/`;
- modelos vazios reutilizáveis em `governança/`.

## Documentos Relacionados

- `README.md`: visão geral, requisitos, build, execução e solução de problemas.
- `STACK.md`: stack técnica e arquitetura.
- `DESIGN.md`: regras visuais e de experiência.
- `PLANEJAMENTO.md`: metodologia obrigatória para mudanças.
- `AGENTS.md`: guia operacional para humanos e agentes.
- `TROUBLESHOOTING.md`: processo de registro e tratamento de falhas.
- `VERSIONAMENTO.md`: regras de versão, release e changelog.
- `MANIFESTO.md`: identidade e síntese de governança do projeto.
