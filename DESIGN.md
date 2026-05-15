# DESIGN.md

Diretrizes visuais e de experiência do usuário da aplicação.

> Este é um modelo. Substitua os campos entre `<...>` pelas informações reais do projeto. Remova seções que não se aplicarem à plataforma ou stack escolhida.

Este documento registra o padrão de UI/UX esperado para alterações futuras. Deve ser consultado antes de qualquer mudança visual, criação de tela, ajuste de componente ou alteração de interação.

## Objetivo

`<Descreva em uma ou duas frases o tom visual e o propósito do design: ex: minimalista escuro para uso técnico, colorido e amigável para uso casual, etc.>`

## Princípios Visuais

- `<princípio 1>`
- `<princípio 2>`
- `<princípio 3>`
- Todo controle icon-only ou pouco óbvio deve ter tooltip.
- Estados visuais devem ser explícitos: ativo, hover, foco, pressionado, desabilitado, erro e sucesso.
- O layout deve funcionar em janela normal, maximizada e tamanho mínimo suportado.

## Paleta Oficial

`<Defina a paleta de cores do projeto. Registre os valores exatos usados no código para que futuras implementações permaneçam coerentes.>`

```text
<COR_FUNDO>      <valor>
<COR_PAINEL>     <valor>
<COR_TEXTO>      <valor>
<COR_DESTAQUE>   <valor>
<COR_ERRO>       <valor>
<COR_SUCESSO>    <valor>
<COR_AVISO>      <valor>
```

### Uso Da Paleta

- Fundo geral: `<COR_FUNDO>`.
- Painéis e superfícies: `<COR_PAINEL>`.
- Texto principal: `<COR_TEXTO>`.
- Ação primária e estado ativo: `<COR_DESTAQUE>`.
- Erro ou destruição: `<COR_ERRO>`.
- Sucesso: `<COR_SUCESSO>`.
- Aviso: `<COR_AVISO>`.

Não introduzir nova família de cores sem plano específico e atualização deste documento.

## Tipografia

```text
Texto padrão: <fonte>, <tamanho>
Título principal: <fonte>, <tamanho>
Subtítulos: <fonte>, <tamanho>
Texto auxiliar: <fonte>, <tamanho>
Ícones: <fonte de ícones>
Código: <fonte monoespaçada>
```

### Regras Tipográficas

- Usar `<fonte principal>` para texto de interface.
- Usar `<fonte de ícones>` para ícones.
- Usar `<fonte monoespaçada>` apenas para código, caminhos e logs.
- Garantir que textos longos usem elipse, quebra de linha ou área rolável; nunca sobreposição.

## Layout Geral

### Estrutura

`<Descreva a estrutura de layout: sidebar, painel principal, cards, modais, etc.>`

### Medidas Relevantes

`<Registre margens, tamanhos de botões, raios de cards e demais métricas fixas do projeto.>`

- Margem externa principal: `<valor>`.
- Botões de navegação: `<largura x altura>`.
- Raio de cards principais: `<valor>`.
- Raio de cards secundários: `<valor>`.

### Regras De Layout

- Não colocar card dentro de card.
- Usar cards apenas para regiões funcionais, itens repetidos e modais.
- Manter dimensões estáveis para toolbars, botões, listas e cards.
- Nenhum hover, label ou estado dinâmico deve deslocar o layout de forma inesperada.

## Botões

### Botões Icon-Only

Usar icon-only para ações frequentes ou familiares.

Regras:

- Sempre incluir tooltip.
- Manter área clicável mínima de `<valor>` para ações principais.
- Ações destrutivas devem usar tratamento visual de perigo.

### Botões Com Texto

Usar texto quando:

- a ação é ambígua sem rótulo;
- há risco de erro destrutivo;
- a ação aparece em modal de confirmação;
- o botão é primário em um formulário.

## Tooltips

Obrigatórios para:

- botões icon-only;
- controles compactos;
- qualquer ação cuja consequência não seja óbvia.

Tooltips não devem encobrir o controle de forma persistente nem sair da área visível da janela.

## Cards E Superfícies

### Cards Principais

- Fundo: `<cor>`.
- Raio: `<valor>`.
- O card deve enquadrar a área funcional inteira da tela.

### Cards Secundários

- Fundo: `<cor>`.
- Raio: `<valor>`.
- Borda sutil.

## Modais

Regras:

- Todos os modais devem ser nativos da própria aplicação, sem caixas de sistema.
- Modais devem ser centralizados em relação à janela da aplicação.
- O restante da aplicação deve ficar visualmente abaixo do modal.
- Controles por trás do modal devem ficar desabilitados.
- `Escape` deve cancelar quando seguro.
- `Enter` deve confirmar quando a ação estiver clara.
- Ação destrutiva deve usar botão visualmente distinto.

## Barras De Rolagem

`<Adapte conforme a plataforma e toolkit. Descreva como as barras devem aparecer em áreas escuras.>`

Regra obrigatória:

- o fundo da barra de rolagem deve usar a mesma cor de fundo do contêiner em que aparece;
- o thumb deve ser mais claro que o fundo, mas não branco puro;
- aplicar este padrão a todas as áreas roláveis novas ou alteradas.

## Estados Visuais

### Ativo

- Fundo: `<cor de destaque suave>`.
- Borda: `<cor de destaque>`.
- Deve ser mais persistente e perceptível que hover.

### Hover

- Aumentar contraste sem mudar tamanho.
- Nunca deslocar layout.

### Foco

- Deve ser visível por borda ou realce.
- Deve funcionar com navegação por teclado.

### Desabilitado

- Texto e fundo devem ter contraste reduzido.
- Ação não deve responder visualmente como ativa.

### Erro

- Usar `<COR_ERRO>` ou variações.
- Mensagens devem ser claras e não confundidas com sucesso.

### Sucesso

- Usar `<COR_SUCESSO>` ou variações discretas.
- Feedback temporário deve voltar ao estado normal automaticamente.

## Acessibilidade E Usabilidade

- Toda ação por mouse deve ter alternativa razoável por teclado quando possível.
- Modais devem controlar foco.
- Textos devem ter contraste suficiente sobre o fundo.
- Ícones devem ter tooltip.
- Áreas clicáveis devem ser grandes o bastante para uso confortável.

## Regras Para Novas Telas

Ao criar uma nova tela:

1. Usar card principal com fundo adequado.
2. Definir toolbar compacta para ações.
3. Usar tooltip em todas as ações icon-only.
4. Garantir layout estável em resize.
5. Registrar qualquer novo padrão neste documento.
6. Criar ou atualizar o plano correspondente em `Planos/`.

## Regras Para Novos Componentes

Novos componentes devem:

- reutilizar elementos, estilos e padrões existentes;
- ter estados hover, foco, pressionado e desabilitado;
- não criar scrollbars de cor incorreta em áreas escuras;
- ser testados em janela normal, maximizada e mínima.

## Critérios De Revisão Visual

Antes de concluir uma alteração visual, verificar:

- Há sobreposição de texto ou controles?
- O texto cabe no espaço disponível?
- O estado ativo é óbvio?
- O hover é discreto e consistente?
- O foco por teclado é visível?
- A barra de rolagem combina com o contêiner?
- Ícones têm tooltip?
- Botões destrutivos são diferenciados?
- A janela maximizada preserva clique e foco?
- A janela mínima mantém ações principais acessíveis?
- O resultado segue os padrões deste documento?
