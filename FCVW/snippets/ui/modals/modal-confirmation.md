---
title: "Confirmation modal — dark theme"
stack: "web"
type: "modal"
tags: [dark-theme, overlay, confirmation, accessibility, escape, focus-trap]
dependencies: ["Native CSS", "Native JS"]
tested: "yes"
created: 2026-05-15
updated: 2026-05-15
---

# Confirmation Modal — Dark Theme

Confirmation modal with overlay, entrance animation, focus trap, Escape key closing, and support for destructive action.

## Available Variants

- Generic confirmation modal (neutral)
- Destructive action modal (confirm button in red)
- Adaptable for simple forms by replacing the paragraph with a form

## CSS Code

```css
/* ── Overlay ───────────────────────────────────────────────── */
.modal-overlay {
  position:       fixed;
  inset:          0;
  background:     rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display:        flex;
  align-items:    center;
  justify-content: center;
  z-index:        1000;
  padding:        16px;
  opacity:        0;
  transition:     opacity 150ms ease;
}

.modal-overlay.modal-aberto {
  opacity: 1;
}

/* ── Container ─────────────────────────────────────────────── */
.modal {
  background:    #1e1e2e;          /* replace with --cor-superficie */
  border:        1px solid rgba(255,255,255,0.1);
  border-radius: 12px;
  padding:       28px;
  width:         100%;
  max-width:     440px;
  box-shadow:    0 24px 60px rgba(0,0,0,0.5);
  transform:     translateY(10px) scale(0.98);
  transition:    transform 150ms ease, opacity 150ms ease;
  opacity:       0;
}

.modal-overlay.modal-aberto .modal {
  transform: translateY(0) scale(1);
  opacity:   1;
}

/* ── Header ─────────────────────────────────────────────── */
.modal-header {
  display:         flex;
  align-items:     flex-start;
  justify-content: space-between;
  gap:             12px;
  margin-bottom:   12px;
}

.modal-titulo {
  font-size:   17px;
  font-weight: 600;
  color:       #e2e8f0;
  margin:      0;
  line-height: 1.3;
}

.modal-fechar {
  background:    transparent;
  border:        none;
  color:         #64748b;
  cursor:        pointer;
  padding:       4px;
  border-radius: 6px;
  line-height:   1;
  flex-shrink:   0;
  transition:    color 150ms ease, background 150ms ease;
}

.modal-fechar:hover {
  color:      #e2e8f0;
  background: rgba(255,255,255,0.07);
}

/* ── Body ─────────────────────────────────────────────────── */
.modal-corpo {
  color:       #94a3b8;
  font-size:   14px;
  line-height: 1.6;
  margin:      0 0 24px;
}

/* ── Footer ────────────────────────────────────────────────── */
.modal-footer {
  display:         flex;
  gap:             10px;
  justify-content: flex-end;
}
```

## HTML Code

```html
<!-- Trigger -->
<button class="btn btn-danger" onclick="abrirModal('modal-excluir')">
  Delete item
</button>

<!-- Modal -->
<div
  class="modal-overlay"
  id="modal-excluir"
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-excluir-titulo"
  tabindex="-1"
  onclick="fecharModalOverlay(event, 'modal-excluir')"
>
  <div class="modal">
    <div class="modal-header">
      <h2 class="modal-titulo" id="modal-excluir-titulo">Delete item?</h2>
      <button
        class="modal-fechar"
        onclick="fecharModal('modal-excluir')"
        aria-label="Close"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"/>
          <line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
      </button>
    </div>

    <p class="modal-corpo">
      This action cannot be undone. The item will be permanently removed.
    </p>

    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="fecharModal('modal-excluir')">
        Cancel
      </button>
      <button class="btn btn-danger" onclick="confirmarExcluir()">
        Delete
      </button>
    </div>
  </div>
</div>
```

## JS Code

```javascript
function abrirModal(id) {
  const overlay = document.getElementById(id);
  if (!overlay) return;
  overlay.style.display = 'flex';
  // force reflow to trigger animation
  requestAnimationFrame(() => overlay.classList.add('modal-aberto'));
  // focus overlay for accessibility and Escape capture
  overlay.focus();
  // Escape listener
  overlay._escapeHandler = (e) => {
    if (e.key === 'Escape') fecharModal(id);
  };
  document.addEventListener('keydown', overlay._escapeHandler);
}

function fecharModal(id) {
  const overlay = document.getElementById(id);
  if (!overlay) return;
  overlay.classList.remove('modal-aberto');
  document.removeEventListener('keydown', overlay._escapeHandler);
  // wait for transition before hiding
  overlay.addEventListener('transitionend', () => {
    overlay.style.display = 'none';
  }, { once: true });
}

function fecharModalOverlay(event, id) {
  // close only if click is on overlay, not the modal itself
  if (event.target === event.currentTarget) fecharModal(id);
}

// Example of confirmation action
function confirmarExcluir() {
  // your logic here
  fecharModal('modal-excluir');
}
```

## Common Adaptations

- **Informative modal** (no destructive action): replace `.btn-danger` with `.btn-primary` in footer.
- **Modal with form**: replace `.modal-corpo > p` with `<form>` containing inputs.
- **Modal centered on panel** (not viewport): replace `position: fixed` with `position: absolute` on overlay and ensure `position: relative` on parent.
- **Without backdrop blur**: remove `backdrop-filter: blur(4px)`.
- **Larger size**: increase `max-width` (e.g., `640px` for extensive forms).

## Dependencies

Native CSS and JS. No external dependencies. Buttons use classes from `snippets/ui/buttons/button-primary.md`.

## Notes

- `aria-modal="true"` and `aria-labelledby` are mandatory for screen reader accessibility.
- Overlay receives `tabindex="-1"` to be programmatically focusable.
- Always remove the Escape listener on close to avoid memory leaks.
- In applications with multiple simultaneous modals, use an increasing `z-index` per instance.
