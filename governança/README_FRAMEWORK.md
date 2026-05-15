# FrameCode VibeWork — Modelos Vazios de Governança

Esta pasta contém modelos vazios reutilizáveis do framework FrameCode VibeWork.

No FrameCode VibeWork, os documentos oficiais preenchidos ficam na raiz da aplicação. Esta pasta não é fonte canônica preenchida do projeto; ela serve para preservar versões genéricas dos documentos, reutilizáveis em outros projetos.

Regra estrutural: quando a estrutura de um documento oficial da raiz for alterada, o modelo correspondente nesta pasta deve receber ajuste equivalente, mantendo placeholders e removendo dados específicos de projetos anteriores.

As regras para transformar o framework em uma aplicação concreta, incluindo renomeação de pasta, títulos e placeholders, ficam em `INSTANCIACAO.md`. Esta pasta não deve ser alterada por substituições globais de instanciação.

## Conteúdo

- `MANIFESTO.md`
- `BRIEFING.md`
- `PLANEJAMENTO.md`, quando houver modelo correspondente
- `VERSIONAMENTO.md`, quando houver modelo correspondente
- `AUDITORIA.md`
- `TESTES.md`
- `SEGURANCA.md`
- `DADOS.md`
- `IA.md`
- `REFATORACAO.md`
- `RELEASE.md`
- `DECISOES_ARQUITETURAIS.md`
- `wiki/`

## Localização canônica ao instanciar

Ao aplicar este framework em uma aplicação, os documentos preenchidos devem ficar na raiz do projeto, e os registros formais devem usar pastas raiz como `Planos/`, `changelogs/`, `troubleshooting/`, `decisoes/`, `auditorias/`, `briefings/` e `wiki/`.
