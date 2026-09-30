<a id="top"></a>

<div align="center">

# FrameCode VibeWork

**Markdown-First Declarative Governance for AI-Assisted Software Development**

Scoped planning · regression protection · selective context · controlled technical memory

[![Support](https://img.shields.io/badge/Support-Buy_Me_a_Coffee-FFDD00?style=flat-square&logo=buymeacoffee&logoColor=000000)](https://buymeacoffee.com/hugomelovek)
[![License](https://img.shields.io/badge/License-Apache_2.0-6f42c1?style=flat-square)](LICENSE)
[![LinkedIn](https://img.shields.io/badge/Contact-LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/hugoaraujo92/)
[![Release](https://img.shields.io/badge/Release-v0.23.0-6f42c1?style=flat-square)](https://github.com/Sistema2D/FrameCode-VibeWork/releases/tag/v0.23.0)

Stable release **V0.23.0**

[![PT-BR](https://img.shields.io/badge/Leia_em-PT--BR-009C3B?style=for-the-badge)](#pt-br)
[![ENG-US](https://img.shields.io/badge/Read_in-ENG--US-3C3B6E?style=for-the-badge)](#en-us)

</div>

---

<a id="pt-br"></a>

## Português (Brasil)

FrameCode VibeWork (FCVW) é uma camada de governança em Markdown para projetos feitos por pessoas e agentes de IA. Cada mudança segue um caminho verificável: contexto mínimo → plano → execução no escopo → evidência → registro de versão.

**O que resolve:** mudanças sem escopo ou rollback, agentes que leem contexto de menos (ou demais), entregas sem prova de não regressão e memória de sessões sem curadoria.

### Como usar

1. Baixe o template no idioma desejado na [release estável](https://github.com/Sistema2D/FrameCode-VibeWork/releases/tag/v0.23.0) e copie `AGENTS.md` e `FCVW/` para o seu projeto.
2. Siga o [INSTANTIATION.md](FCVW/INSTANTIATION.md) (projeto novo ou [existente](FCVW/INSTANTIATION.md#retroactive-instantiation)) e preencha o [PROJECT.md](FCVW/PROJECT.md).
3. Peça ao seu agente de IA que leia o [AGENTS.md](AGENTS.md) antes de trabalhar.

Toda mudança versionada ganha um plano em `FCVW/Plans/`, evidência de validação e um registro de changelog. Consultas e revisões não exigem plano.

### Validação (opcional)

Ferramentas em Python 3.10+, só biblioteca padrão:

```sh
python FCVW/tools/validate_fcvw.py --root . --profile instantiated
python FCVW/tools/plan_queue_fcvw.py --root . --recommend
```

### Saiba mais

[Índice do framework](FCVW/README.md) · [Mapa de contexto](FCVW/CONTEXT_MAP.md) · [Planejamento](FCVW/PLANNING.md) · [Regressão](FCVW/REGRESSION_GUARDS.md) · [Upgrade](FCVW/MIGRATIONS.md) · [Skills](FCVW/skills/README.md)

O FCVW não é runtime de agente nem substitui testes, CI ou revisão humana.

[English (US)](#en-us) · [Topo](#top)

---

<a id="en-us"></a>

## English (United States)

FrameCode VibeWork (FCVW) is a Markdown governance layer for projects built by people and AI agents. Every change follows a verifiable path: minimum context → plan → scoped execution → evidence → version record.

**What it solves:** changes without scope or rollback, agents reading too little (or too much) context, delivery without regression evidence, and uncurated session memory.

### How to use

1. Download the template in your language from the [stable release](https://github.com/Sistema2D/FrameCode-VibeWork/releases/tag/v0.23.0) and copy `AGENTS.md` and `FCVW/` into your project.
2. Follow [INSTANTIATION.md](FCVW/INSTANTIATION.md) (new or [existing](FCVW/INSTANTIATION.md#retroactive-instantiation) project) and fill in [PROJECT.md](FCVW/PROJECT.md).
3. Ask your AI agent to read [AGENTS.md](AGENTS.md) before working.

Every versioned change gets a plan under `FCVW/Plans/`, validation evidence and a changelog entry. Queries and reviews need no plan.

### Validation (optional)

Python 3.10+ tools, standard library only:

```sh
python FCVW/tools/validate_fcvw.py --root . --profile instantiated
python FCVW/tools/plan_queue_fcvw.py --root . --recommend
```

### Learn more

[Framework index](FCVW/README.md) · [Context map](FCVW/CONTEXT_MAP.md) · [Planning](FCVW/PLANNING.md) · [Regression](FCVW/REGRESSION_GUARDS.md) · [Upgrade](FCVW/MIGRATIONS.md) · [Skills](FCVW/skills/README.md)

FCVW is not an agent runtime and does not replace tests, CI or human review.

[Português (Brasil)](#pt-br) · [Top](#top)

---

<div align="center">

[Apache License 2.0](LICENSE) · [Attribution / Atribuição](NOTICE) · [Release record V0.23.0](FCVW/framework-releases/V0.23.0.md) · [Maintainer backlog](TODO.md)

</div>
