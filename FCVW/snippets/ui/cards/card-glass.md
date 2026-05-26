---
title: "Glass Card — dark theme"
stack: "web"
type: "card"
tags: [dark-theme, glassmorphism, hover, card, panel, stat]
dependencies: ["Native CSS"]
tested: "yes"
created: 2026-05-15
updated: 2026-05-15
---

# Glass Card — Dark Theme

Card with glassmorphism effect for dark theme. Includes: simple card, interactive card, card with header/footer, and statistic card.

## CSS Code

```css
.card {
  background:    rgba(255,255,255,0.04);
  border:        1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding:       20px;
  color:         #e2e8f0;
  position:      relative;
  overflow:      hidden;
}

/* Interactive */
.card-interativo {
  cursor:     pointer;
  transition: background 150ms ease, border-color 150ms ease,
              transform 150ms ease, box-shadow 150ms ease;
}
.card-interativo:hover {
  background:   rgba(255,255,255,0.07);
  border-color: rgba(255,255,255,0.14);
  transform:    translateY(-2px);
  box-shadow:   0 8px 32px rgba(0,0,0,0.3);
}
.card-interativo:active { transform: translateY(0); box-shadow: none; }

/* Header */
.card-header-area {
  display:         flex;
  align-items:     center;
  justify-content: space-between;
  gap:             12px;
  margin-bottom:   16px;
  padding-bottom:  16px;
  border-bottom:   1px solid rgba(255,255,255,0.07);
}
.card-titulo    { font-size: 15px; font-weight: 600; color: #e2e8f0; margin: 0; }
.card-subtitulo { font-size: 13px; color: #64748b; margin: 4px 0 0; }
.card-badge {
  font-size: 11px; font-weight: 600; padding: 3px 8px;
  border-radius: 999px;
  background: rgba(99,102,241,0.15); color: #818cf8; white-space: nowrap;
}

/* Body */
.card-body { font-size: 14px; color: #94a3b8; line-height: 1.6; }

/* Footer */
.card-footer {
  margin-top: 16px; padding-top: 16px;
  border-top: 1px solid rgba(255,255,255,0.07);
  display: flex; align-items: center; justify-content: space-between; gap: 8px;
}

/* Stat card */
.card-stat { display: flex; flex-direction: column; gap: 6px; }
.card-stat-label {
  font-size: 12px; font-weight: 500; color: #64748b;
  text-transform: uppercase; letter-spacing: 0.06em;
}
.card-stat-valor  { font-size: 28px; font-weight: 700; color: #e2e8f0; line-height: 1; }
.card-stat-delta  { font-size: 12px; font-weight: 500; display: inline-flex; align-items: center; gap: 4px; }
.card-stat-delta.positivo { color: #34d399; }
.card-stat-delta.negativo { color: #f87171; }

/* Colored border on the left */
.card-destaque-esquerda {
  border-left: 3px solid var(--cor-destaque, #6366f1);
  padding-left: 17px;
}
```

## HTML Code

```html
<!-- Simple card -->
<div class="card">
  <p class="card-body">Content here.</p>
</div>

<!-- Card with header and footer -->
<div class="card">
  <div class="card-header-area">
    <div>
      <h3 class="card-titulo">Title</h3>
      <p class="card-subtitulo">Subtitle</p>
    </div>
    <span class="card-badge">New</span>
  </div>
  <div class="card-body">Card body.</div>
  <div class="card-footer">
    <span style="font-size:13px;color:#64748b">Updated 2h ago</span>
    <button class="btn btn-ghost btn-sm">See more</button>
  </div>
</div>

<!-- Interactive card -->
<div class="card card-interativo" role="button" tabindex="0" onclick="...">
  <div class="card-body">Click to navigate.</div>
</div>

<!-- Stat card -->
<div class="card card-stat">
  <span class="card-stat-label">Active users</span>
  <span class="card-stat-valor">1,284</span>
  <span class="card-stat-delta positivo">▲ 12.4%</span>
</div>

<!-- Colored border -->
<div class="card card-destaque-esquerda">
  <h3 class="card-titulo">Notice</h3>
  <p class="card-body">Notice text.</p>
</div>
```

## Common Adaptations

- **Glass over image**: enable `backdrop-filter: blur(8px)` and ensure parent element background.
- **Cards grid**: `display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:16px` on container.
- **Nested card (sub-level)**: `background:rgba(255,255,255,0.03); border-radius:8px`.
- **Base shadow**: add `box-shadow: 0 4px 24px rgba(0,0,0,0.3)` to `.card`.

## Dependencies

Native CSS. Buttons in footer use `snippets/ui/buttons/button-primary.md`.

## Notes

- Clickable cards must have `role="button"` and `tabindex="0"` for accessibility.
- Do not nest `.card` inside another `.card` — use a slightly different background for sub-level.
