---
titulo: "Conjunto de botões — tema escuro"
stack: "web"
tipo: "button"
tags: [dark-theme, hover, focus, disabled, primary, secondary, danger]
dependencias: ["CSS nativo", "Google Fonts — Inter"]
testado: "sim"
criado: 2026-05-15
atualizado: 2026-05-15
---

# Botões — Tema Escuro

Conjunto completo de botões para aplicações com tema escuro. Cobre variantes primário, secundário, ghost e perigo, além dos estados hover, foco, pressionado e desabilitado.

## Variantes disponíveis

- `.btn-primary` — ação principal, fundo colorido
- `.btn-secondary` — ação secundária, borda sutil
- `.btn-ghost` — ação terciária, sem borda
- `.btn-danger` — ação destrutiva, tom vermelho
- `.btn-icon` — botão quadrado só com ícone
- Modificador `.btn-sm` — versão menor

## Código CSS

```css
/* ── Variáveis recomendadas no :root do projeto ────────────── */
:root {
  --cor-destaque:    #6366f1;   /* indigo — trocar pela cor do projeto */
  --cor-hover:       #4f46e5;
  --cor-perigo:      #ef4444;
  --cor-perigo-hover:#dc2626;
  --cor-superficie:  #1e1e2e;
  --cor-borda:       rgba(255,255,255,0.1);
  --cor-texto:       #e2e8f0;
  --cor-texto-muted: #94a3b8;
  --raio:            8px;
  --fonte:           'Inter', system-ui, sans-serif;
  --transicao:       150ms ease;
}

/* ── Base ──────────────────────────────────────────────────── */
.btn {
  display:         inline-flex;
  align-items:     center;
  gap:             8px;
  padding:         10px 20px;
  border:          1px solid transparent;
  border-radius:   var(--raio);
  font-family:     var(--fonte);
  font-size:       14px;
  font-weight:     500;
  line-height:     1;
  cursor:          pointer;
  user-select:     none;
  white-space:     nowrap;
  text-decoration: none;
  transition:      background var(--transicao),
                   border-color var(--transicao),
                   opacity var(--transicao),
                   box-shadow var(--transicao);
  outline:         none;
}

.btn:focus-visible {
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.4);
}

.btn:disabled,
.btn[aria-disabled="true"] {
  opacity: 0.4;
  cursor:  not-allowed;
  pointer-events: none;
}

/* ── Primário ──────────────────────────────────────────────── */
.btn-primary {
  background: var(--cor-destaque);
  color:      #fff;
  border-color: var(--cor-destaque);
}

.btn-primary:hover {
  background:   var(--cor-hover);
  border-color: var(--cor-hover);
}

.btn-primary:active {
  transform:    scale(0.97);
}

/* ── Secundário ────────────────────────────────────────────── */
.btn-secondary {
  background:   transparent;
  color:        var(--cor-texto);
  border-color: var(--cor-borda);
}

.btn-secondary:hover {
  background: rgba(255,255,255,0.06);
  border-color: rgba(255,255,255,0.2);
}

.btn-secondary:active {
  transform: scale(0.97);
}

/* ── Ghost ─────────────────────────────────────────────────── */
.btn-ghost {
  background:   transparent;
  color:        var(--cor-texto-muted);
  border-color: transparent;
}

.btn-ghost:hover {
  background: rgba(255,255,255,0.06);
  color:      var(--cor-texto);
}

/* ── Perigo ────────────────────────────────────────────────── */
.btn-danger {
  background:   transparent;
  color:        var(--cor-perigo);
  border-color: rgba(239,68,68,0.3);
}

.btn-danger:hover {
  background:   var(--cor-perigo);
  border-color: var(--cor-perigo);
  color:        #fff;
}

.btn-danger:active {
  background:   var(--cor-perigo-hover);
  border-color: var(--cor-perigo-hover);
  transform:    scale(0.97);
}

/* ── Ícone ─────────────────────────────────────────────────── */
.btn-icon {
  padding:       10px;
  width:         40px;
  height:        40px;
  justify-content: center;
}

/* ── Tamanho menor ─────────────────────────────────────────── */
.btn.btn-sm {
  padding:     6px 14px;
  font-size:   13px;
}

.btn-icon.btn-sm {
  padding:  6px;
  width:   32px;
  height:  32px;
}
```

## Código HTML

```html
<!-- Primário -->
<button class="btn btn-primary">Salvar</button>

<!-- Secundário -->
<button class="btn btn-secondary">Cancelar</button>

<!-- Ghost -->
<button class="btn btn-ghost">Saiba mais</button>

<!-- Perigo -->
<button class="btn btn-danger">Excluir</button>

<!-- Com ícone (usando Lucide ou SVG inline) -->
<button class="btn btn-primary">
  <svg width="16" height="16" ...></svg>
  Publicar
</button>

<!-- Ícone only (requer tooltip) -->
<button class="btn btn-icon btn-secondary" title="Configurações" aria-label="Configurações">
  <svg width="16" height="16" ...></svg>
</button>

<!-- Desabilitado -->
<button class="btn btn-primary" disabled>Processando...</button>

<!-- Tamanho menor -->
<button class="btn btn-secondary btn-sm">Filtrar</button>
```

## Adaptações comuns

- **Cor de destaque**: trocar `--cor-destaque` e `--cor-hover` pelas cores do projeto em `:root`.
- **Raio de borda**: ajustar `--raio` (0 = quadrado, 999px = pill).
- **Fonte**: trocar `--fonte` pela fonte do projeto.
- **Botão de loading**: adicionar `pointer-events: none` e substituir o texto por spinner durante request.
- **Largura total**: adicionar `width: 100%; justify-content: center;` inline ou via classe auxiliar.

## Dependências

CSS nativo. Sem dependências externas. Funciona com qualquer framework ou HTML puro.

## Notas

- `.btn:focus-visible` garante acessibilidade por teclado sem aparecer em clique por mouse.
- Botões icon-only **sempre** devem ter `title` ou `aria-label` e tooltip visual.
- Não usar `<a>` estilizado como botão para ações que não navegam — usar `<button>`.
