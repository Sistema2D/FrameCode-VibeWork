---
title: "Backgrounds — gradients and surfaces for dark theme"
stack: "web"
type: "background"
tags: [dark-theme, gradient, noise, mesh, radial, scrollbar]
dependencies: ["Native CSS"]
tested: "yes"
created: 2026-05-15
updated: 2026-05-15
---

# Backgrounds — Dark Theme

Ready-made background recipes for dark theme applications.

## Variants

1. Dark base solid background
2. Radial gradient with spotlight
3. Mesh gradient (multiple color points)
4. Noise texture overlay
5. Customized scrollbar (dark theme)
6. Surface CSS variables (color tokens)

## CSS Code

```css
/* ── 1. Surface Tokens ───────────────────────────────── */
:root {
  --bg-base:       #0f0f17;  /* page main background */
  --bg-painel:     #1a1a27;  /* panels, sidebars */
  --bg-superficie: #1e1e2e;  /* cards, modals */
  --bg-elevado:    #252538;  /* dropdowns, tooltips */
  --cor-borda:     rgba(255,255,255,0.08);
}

/* ── 2. Solid Base Background ──────────────────────────────────── */
body {
  background-color: var(--bg-base);
  color:            #e2e8f0;
  margin:           0;
  font-family:      'Inter', system-ui, sans-serif;
  min-height:       100vh;
}

/* ── 3. Radial Gradient with Spotlight ──────────────────── */
.bg-radial {
  background:
    radial-gradient(ellipse 80% 60% at 50% -10%,
      rgba(99, 102, 241, 0.18) 0%,   /* highlight color */
      transparent 70%),
    var(--bg-base);
}

/* Variant: spotlight on top right corner */
.bg-radial-canto {
  background:
    radial-gradient(ellipse 50% 50% at 90% 0%,
      rgba(99, 102, 241, 0.2) 0%,
      transparent 60%),
    var(--bg-base);
}

/* ── 4. Mesh Gradient (two color points) ─────────────────── */
.bg-mesh {
  background:
    radial-gradient(ellipse 60% 50% at 20% 80%,
      rgba(99, 102, 241, 0.12) 0%, transparent 60%),
    radial-gradient(ellipse 50% 40% at 80% 20%,
      rgba(139, 92, 246, 0.10) 0%, transparent 60%),
    var(--bg-base);
}

/* ── 5. Noise Texture Overlay ──────────────────────────────── */
/* Apply over any background to add subtle grain */
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
/* Ensure content stays above noise */
.bg-noise > * { position: relative; z-index: 1; }

/* ── 6. Customized Scrollbar (Webkit/Blink) ───────────────── */
/* Apply to scrollable element or * for global */
::-webkit-scrollbar        { width: 6px; height: 6px; }
::-webkit-scrollbar-track  { background: transparent; }
::-webkit-scrollbar-thumb  {
  background:    rgba(255,255,255,0.12);
  border-radius: 99px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.22); }

/* Scrollbar only when hovering container (elegant) */
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

/* ── 7. Subtle Divider ──────────────────────────────────────── */
.divider {
  height:     1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
  border:     none;
  margin:     0;
}
```

## Typical Application

```html
<!-- Full layout with gradient + noise -->
<body class="bg-radial bg-noise">
  <aside class="sidebar">...</aside>
  <main class="scroll-suave">...</main>
</body>

<!-- Divider between sections -->
<hr class="divider">
```

## Common Adaptations

- **Change gradient highlight color**: replace `rgba(99,102,241,...)` with project highlight color.
- **Deactivate noise**: remove the `.bg-noise` class or set `opacity: 0`.
- **Horizontal gradient (sidebar)**: use `linear-gradient(180deg, rgba(99,102,241,0.12), transparent)`.
- **Side panel background**: `background: var(--bg-painel); border-right: 1px solid var(--cor-borda)`.

## Dependencies

Native CSS. No external dependencies.

## Notes

- Inline SVG noise eliminates the need for an external image file.
- Customized scrollbar works in Chrome, Edge, and Safari. Firefox uses `scrollbar-width` and `scrollbar-color`.
- Keep `--bg-base` consistent with cards and modals backgrounds to avoid visual discontinuity.
