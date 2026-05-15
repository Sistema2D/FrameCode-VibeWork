# Snippets — Biblioteca de Código Reutilizável

Esta pasta contém referências de código prontas para serem adaptadas e aplicadas durante o desenvolvimento.

O objetivo é que a IA e o desenvolvedor possam reutilizar implementações testadas de componentes visuais e padrões de comportamento sem partir do zero a cada nova tela ou sessão.

A Galeria de Snippets (`snippets/gallery.html`) permite visualizar os componentes em tempo real e copiar o código necessário.

---

## Manutenção por IA

A IA tem permissão e dever de:
- **Atualizar**: Ajustar o código dos snippets existentes conforme o usuário solicitar mudanças visuais ou melhorias funcionais.
- **Incluir**: Criar novos snippets quando um componente útil for desenvolvido e validado.
- **Excluir**: Remover snippets obsoletos ou que não atendam mais aos padrões de design do projeto.
- **Sincronizar**: Garantir que a `gallery.html` reflita os snippets disponíveis.

- Consultar antes de implementar um componente de UI (botão, modal, card, barra, etc.)
- Manter consistência visual entre sessões e entre projetos
- Reduzir retrabalho: o snippet já resolve o caso base; basta adaptar cores, tamanhos e textos
- Registrar implementações aprovadas para reutilização futura

Esta pasta **não substitui** `DESIGN.md` (que define *regras* visuais) nem `wiki/components/` (que documenta módulos do projeto). Ela contém *código concreto* pronto para uso.

---

## Reutilização Global

Para manter a mesma identidade visual entre múltiplos projetos, a pasta `snippets/` (especialmente o arquivo `tokens.css`) deve ser tratada como uma biblioteca compartilhada. Recomenda-se o uso de **Git Submodules** para sincronizar esta pasta entre repositórios, garantindo que ajustes visuais feitos em um projeto sejam propagados para os demais.

---

## Estrutura

```text
snippets/
├── README.md              ← este arquivo (schema)
├── ui/
│   ├── buttons/           ← botões e variantes
│   ├── modals/            ← modais, overlays, diálogos
│   ├── cards/             ← cards, painéis, superfícies
│   ├── navigation/        ← navbars, sidebars, tabs, breadcrumbs
│   ├── forms/             ← inputs, selects, checkboxes, sliders
│   ├── backgrounds/       ← gradientes, padrões de fundo, texturas
│   └── animations/        ← transições, micro-animações, loaders
└── patterns/
    ├── loading/            ← estados de carregamento
    ├── empty-states/       ← estados vazios e placeholders
    └── feedback/           ← toasts, alerts, banners, badges
```

---

## Frontmatter obrigatório

Todo arquivo de snippet deve iniciar com frontmatter YAML.

```yaml
---
titulo: "<nome descritivo do snippet>"
stack: "web | mobile | desktop | cli | agnostico"
tipo: "button | modal | card | form | navigation | background | animation | pattern"
tags: [dark-theme, glassmorphism, hover, confirmacao]
dependencias: ["CSS nativo", "JS nativo"]
testado: "sim | não"
criado: AAAA-MM-DD
atualizado: AAAA-MM-DD
---
```

---

## Padrão de nomenclatura

```text
{tipo}-{variante}-{modificador}.md
```

Exemplos:

```text
button-primary.md
button-danger-icon.md
modal-confirmacao.md
card-glass.md
card-lista-item.md
background-gradient-escuro.md
toast-sucesso.md
input-com-label.md
```

---

## Como usar (fluxo para a IA)

Ao receber uma solicitação de implementação de componente de UI:

1. Verificar se existe snippet correspondente em `snippets/ui/` ou `snippets/patterns/`.
2. Ler o snippet identificado.
3. Adaptar cores, tamanhos, textos e comportamentos conforme `DESIGN.md` do projeto.
4. Implementar sem reinventar o padrão base.
5. Se o resultado for significativamente melhor que o snippet original, ou se o usuário solicitar um ajuste no padrão, a IA deve atualizar o snippet correspondente ou criar um novo.

Ao concluir uma alteração em `snippets/`, a IA deve atualizar a `gallery.html` para refletir a mudança.

Quando não existir snippet:

1. Implementar seguindo `DESIGN.md`.
2. Ao concluir e validar, avaliar se vale criar um snippet reutilizável.
3. Criar o snippet na pasta correta com frontmatter completo.

---

## Como contribuir com novos snippets

Critérios para promover código a snippet:

- O componente foi validado visualmente e funcionalmente.
- O padrão pode ser reutilizado em outros projetos ou telas com adaptação mínima.
- O código é autocontido ou declara dependências claramente.
- O snippet não replica conteúdo já coberto por outro snippet existente.

Estrutura mínima de um snippet:

```markdown
---
[frontmatter]
---

# Título do snippet

Breve descrição do componente, quando usar e variações existentes.

## Preview (opcional)

Descreva ou ilustre o resultado visual esperado.

## Código

\`\`\`html
<!-- código aqui -->
\`\`\`

## Adaptações comuns

- Como mudar a cor de destaque: ...
- Como adicionar ícone: ...
- Como desabilitar: ...

## Dependências

- CSS nativo: sem dependências externas.
- ou: requer variáveis CSS definidas em `:root { --cor-destaque: ... }`.

## Notas

Observações sobre compatibilidade, limitações ou contexto de uso.
```

---

## Carregamento por tipo de componente

| Componente a implementar | Pasta a consultar |
|---|---|
| Botão, CTA, ação | `snippets/ui/buttons/` |
| Modal, diálogo, confirmação | `snippets/ui/modals/` |
| Card, painel, superfície | `snippets/ui/cards/` |
| Navbar, sidebar, tabs | `snippets/ui/navigation/` |
| Input, select, formulário | `snippets/ui/forms/` |
| Fundo, gradiente, textura | `snippets/ui/backgrounds/` |
| Transição, hover, animação | `snippets/ui/animations/` |
| Estado de carregamento | `snippets/patterns/loading/` |
| Tela vazia, placeholder | `snippets/patterns/empty-states/` |
| Toast, alerta, banner | `snippets/patterns/feedback/` |
