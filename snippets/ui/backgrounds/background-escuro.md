---
titulo: "Backgrounds — gradientes e superfícies para tema escuro"
stack: "web"
tipo: "background"
tags: [dark-theme, gradiente, noise, mesh, radial, scrollbar]
dependencias: ["CSS nativo"]
testado: "sim"
criado: 2026-05-15
atualizado: 2026-05-15
---

# Backgrounds — Tema Escuro

Receitas prontas de fundo para aplicações com tema escuro.

## Variantes

1. Fundo sólido escuro base
2. Gradiente radial com ponto de luz
3. Mesh gradient (múltiplos pontos de cor)
4. Noise texture overlay
5. Scrollbar customizada (tema escuro)
6. Variáveis CSS de superfície (tokens de cor)

## Código CSS

```css
/* ── 1. Tokens de superfície ───────────────────────────────── */
:root {
  --bg-base:       #0f0f17;  /* fundo geral da página */
  --bg-painel:     #1a1a27;  /* painéis, sidebars */
  --bg-superficie: #1e1e2e;  /* cards, modais */
  --bg-elevado:    #252538;  /* dropdowns, tooltips */
  --cor-borda:     rgba(255,255,255,0.08);
}

/* ── 2. Fundo sólido base ──────────────────────────────────── */
body {
  background-color: var(--bg-base);
  color:            #e2e8f0;
  margin:           0;
  font-family:      'Inter', system-ui, sans-serif;
  min-height:       100vh;
}

/* ── 3. Gradiente radial com ponto de luz ──────────────────── */
.bg-radial {
  background:
    radial-gradient(ellipse 80% 60% at 50% -10%,
      rgba(99, 102, 241, 0.18) 0%,   /* cor de destaque */
      transparent 70%),
    var(--bg-base);
}

/* Variante: luz no canto superior direito */
.bg-radial-canto {
  background:
    radial-gradient(ellipse 50% 50% at 90% 0%,
      rgba(99, 102, 241, 0.2) 0%,
      transparent 60%),
    var(--bg-base);
}

/* ── 4. Mesh gradient (dois pontos de cor) ─────────────────── */
.bg-mesh {
  background:
    radial-gradient(ellipse 60% 50% at 20% 80%,
      rgba(99, 102, 241, 0.12) 0%, transparent 60%),
    radial-gradient(ellipse 50% 40% at 80% 20%,
      rgba(139, 92, 246, 0.10) 0%, transparent 60%),
    var(--bg-base);
}

/* ── 5. Noise texture overlay ──────────────────────────────── */
/* Aplicar sobre qualquer fundo para adicionar granulação sutil */
.bg-noise::before {
  content:    '';
  position:   fixed;
  inset:      0;
  z-index:    0;
  pointer-events: none;
  opacity:    0.035;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  background-size: 200px 200px;
}
/* Garantir que o conteúdo fique acima do noise */
.bg-noise > * { position: relative; z-index: 1; }

/* ── 6. Scrollbar customizada (Webkit/Blink) ───────────────── */
/* Aplicar no elemento rolável ou em * para global */
::-webkit-scrollbar        { width: 6px; height: 6px; }
::-webkit-scrollbar-track  { background: transparent; }
::-webkit-scrollbar-thumb  {
  background:    rgba(255,255,255,0.12);
  border-radius: 99px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.22); }

/* Scrollbar apenas quando hover no container (elegante) */
.scroll-suave {
  overflow-y: auto;
  scrollbar-width: thin;               /* Firefox */
  scrollbar-color: rgba(255,255,255,0.12) transparent; /* Firefox */
}
.scroll-suave::-webkit-scrollbar       { width: 5px; }
.scroll-suave::-webkit-scrollbar-track { background: transparent; }
.scroll-suave::-webkit-scrollbar-thumb {
  background:    rgba(255,255,255,0.10);
  border-radius: 99px;
  transition:    background 150ms;
}
.scroll-suave:hover::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); }

/* ── 7. Divisor sutil ──────────────────────────────────────── */
.divider {
  height:     1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
  border:     none;
  margin:     0;
}
```

## Aplicação típica

```html
<!-- Layout completo com gradiente + noise -->
<body class="bg-radial bg-noise">
  <aside class="sidebar">...</aside>
  <main class="scroll-suave">...</main>
</body>

<!-- Divider entre seções -->
<hr class="divider">
```

## Adaptações comuns

- **Trocar cor de destaque do gradiente**: substituir `rgba(99,102,241,...)` pela cor do projeto.
- **Desativar noise**: remover a classe `.bg-noise` ou setar `opacity: 0`.
- **Gradiente horizontal (sidebar)**: usar `linear-gradient(180deg, rgba(99,102,241,0.12), transparent)`.
- **Fundo de painel lateral**: `background: var(--bg-painel); border-right: 1px solid var(--cor-borda)`.

## Dependências

CSS nativo. Sem dependências externas.

## Notas

- O noise SVG inline elimina dependência de arquivo de imagem externo.
- A scrollbar customizada funciona em Chrome, Edge e Safari. Firefox usa `scrollbar-width` e `scrollbar-color`.
- Manter o `--bg-base` consistente com o fundo de cards e modais para evitar descontinuidade visual.
