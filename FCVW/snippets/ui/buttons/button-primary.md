---
title: "Buttons Set — dark theme"
stack: "web"
type: "button"
tags: [dark-theme, hover, focus, disabled, primary, secondary, danger]
dependencies: ["Native CSS", "Google Fonts — Inter"]
tested: "yes"
created: 2026-05-15
updated: 2026-05-15
---

# Buttons — Dark Theme

Complete set of buttons for dark theme applications. Covers primary, secondary, ghost, and danger variants, in addition to hover, focus, active, and disabled states.

## Available Variants

- `.btn-primary` — main action, filled background
- `.btn-secondary` — secondary action, subtle border
- `.btn-ghost` — tertiary action, no border
- `.btn-danger` — destructive action, red tone
- `.btn-icon` — square button with icon only
- Modifier `.btn-sm` — smaller version

## CSS Code

```css
/* ── Recommended variables in project's :root ────────────── */
:root {
  --cor-destaque:    #6366f1;   /* indigo — replace with project highlight color */
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

/* ── Primary ──────────────────────────────────────────────── */
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

/* ── Secondary ────────────────────────────────────────────── */
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

/* ── Danger ────────────────────────────────────────────────── */
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

/* ── Icon ─────────────────────────────────────────────────── */
.btn-icon {
  padding:       10px;
  width:         40px;
  height:        40px;
  justify-content: center;
}

/* ── Smaller Size ─────────────────────────────────────────── */
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

## HTML Code

```html
<!-- Primary -->
<button class="btn btn-primary">Save</button>

<!-- Secondary -->
<button class="btn btn-secondary">Cancel</button>

<!-- Ghost -->
<button class="btn btn-ghost">Learn more</button>

<!-- Danger -->
<button class="btn btn-danger">Delete</button>

<!-- With icon (using Lucide or inline SVG) -->
<button class="btn btn-primary">
  <svg width="16" height="16" ...></svg>
  Publish
</button>

<!-- Icon only (requires tooltip) -->
<button class="btn btn-icon btn-secondary" title="Settings" aria-label="Settings">
  <svg width="16" height="16" ...></svg>
</button>

<!-- Disabled -->
<button class="btn btn-primary" disabled>Processing...</button>

<!-- Smaller size -->
<button class="btn btn-secondary btn-sm">Filter</button>
```

## Common Adaptations

- **Highlight color**: replace `--cor-destaque` and `--cor-hover` with project highlight colors in `:root`.
- **Border radius**: adjust `--raio` (0 = square, 999px = pill).
- **Font**: replace `--fonte` with project font.
- **Loading button**: add `pointer-events: none` and replace text with a spinner during request.
- **Full width**: add `width: 100%; justify-content: center;` inline or via utility class.

## Dependencies

Native CSS. No external dependencies. Works with any framework or pure HTML.

## Notes

- `.btn:focus-visible` ensures keyboard accessibility without showing up during mouse clicks.
- Icon-only buttons **always** must have `title` or `aria-label` and visual tooltip.
- Do not use `<a>` styled as a button for actions that do not navigate — use `<button>`.
