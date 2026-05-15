# Log da LLM Wiki

Registro cronológico de eventos relevantes da wiki.

Este arquivo deve ser tratado como histórico append-first: preferir adicionar novos registros em vez de apagar registros antigos.

---

## Formato recomendado

```markdown
## [AAAA-MM-DD HH:MM] <tipo> | <título curto>

- Origem:
- Ação executada:
- Páginas criadas:
- Páginas atualizadas:
- Páginas obsoletas:
- Resultado:
- Pendências:
```

---

## Tipos de evento

- `init`: inicialização da wiki.
- `ingest`: entrada de nova fonte.
- `synthesis`: criação ou atualização de síntese.
- `promotion`: promoção de registro para conhecimento reutilizável.
- `lint`: verificação estrutural da wiki.
- `audit`: aprendizado derivado de auditoria.
- `failure`: aprendizado derivado de troubleshooting.
- `refactoring`: aprendizado derivado de refatoração.
- `release`: aprendizado derivado de release.
- `decision`: decisão consolidada.
- `obsolete`: marcação de página como obsoleta.
- `contradiction`: contradição identificada.
- `maintenance`: manutenção geral.

---

## Registros

## [AAAA-MM-DD HH:MM] init | Inicialização da LLM Wiki

- Origem: criação da estrutura inicial da pasta `wiki/`.
- Ação executada: criação de `README.md`, `schema.md`, `index.md`, `log.md`, pastas temáticas e templates.
- Páginas criadas:
  - `wiki/README.md`
  - `wiki/schema.md`
  - `wiki/index.md`
  - `wiki/log.md`
- Páginas atualizadas: nenhuma.
- Páginas obsoletas: nenhuma.
- Resultado: estrutura inicial criada.
- Pendências: preencher índice com conhecimentos reais do projeto conforme novas evidências forem surgindo.
