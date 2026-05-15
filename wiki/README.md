# Wiki de Governança do Projeto

Esta pasta armazena a memória técnica acumulativa de governança do projeto em formato Markdown.

A wiki não substitui os documentos oficiais do repositório, como `AGENTS.md`, `PLANEJAMENTO.md`, `VERSIONAMENTO.md`, `TROUBLESHOOTING.md`, `AUDITORIA.md`, `REFATORACAO.md`, `IA.md` ou `DESIGN.md`.

Ela funciona como uma camada de aprendizado contínuo: registra padrões validados, falhas recorrentes, decisões consolidadas, refatorações, auditorias, releases, componentes, prompts úteis, perguntas abertas e sínteses reutilizáveis.

Quando o projeto também possuir uma wiki ou vault de usuário/runtime, diferencie explicitamente essa estrutura da wiki de governança.

## Princípios

1. Fontes brutas devem ser preservadas.
2. Sínteses devem apontar para suas fontes.
3. Conhecimento reutilizável deve ser promovido para páginas próprias.
4. Hipóteses não devem ser tratadas como verdades.
5. Conteúdo obsoleto deve ser marcado como tal, não apagado sem justificativa.
6. A wiki deve ser consultada antes de mudanças relevantes.
7. A wiki deve ser atualizada após mudanças que gerem aprendizado reutilizável.
8. A wiki não deve armazenar segredos, tokens, logs privados ou dados pessoais desnecessários.

## Arquivos principais

- `schema.md`: regras estruturais da wiki.
- `index.md`: índice navegável dos conhecimentos.
- `log.md`: registro cronológico de ingestões, sínteses, auditorias e lint.
- `inbox/`: entradas ainda não processadas.
- `raw/`: fontes brutas imutáveis.
- `sources/`: fontes normalizadas ou descritas.
- `concepts/`: conceitos técnicos e de produto.
- `decisions/`: decisões arquiteturais consolidadas.
- `patterns/`: padrões técnicos aprovados.
- `failures/`: aprendizados sobre falhas.
- `refactorings/`: aprendizados e oportunidades de refatoração.
- `audits/`: achados recorrentes de auditorias.
- `releases/`: sínteses de versões publicadas.
- `components/`: componentes, módulos e responsabilidades.
- `prompts/`: prompts úteis e validados.
- `questions/`: perguntas abertas.
- `syntheses/`: sínteses transversais.
- `templates/`: modelos de páginas da wiki.

## Fontes formais

Fontes formais preferenciais:

- `Planos/concluído/`
- `changelogs/`
- `troubleshooting/`
- `decisoes/`
- `auditorias/`
- documentos oficiais da raiz
- trechos de código ou documentação usados como evidência
