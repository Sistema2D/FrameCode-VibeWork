---
titulo: "Modal de confirmação — tema escuro"
stack: "web"
tipo: "modal"
tags: [dark-theme, overlay, confirmacao, acessibilidade, escape, focus-trap]
dependencias: ["CSS nativo", "JS nativo"]
testado: "sim"
criado: 2026-05-15
atualizado: 2026-05-15
---

# Modal de Confirmação — Tema Escuro

Modal de confirmação com overlay, animação de entrada, trap de foco, fechamento por Escape e suporte a ação destrutiva.

## Variantes disponíveis

- Modal de confirmação genérica (neutro)
- Modal de ação destrutiva (botão de confirmar em vermelho)
- Adaptável para formulários simples substituindo o parágrafo pelo form

## Código CSS

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
  background:    #1e1e2e;          /* trocar por --cor-superficie */
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

/* ── Cabeçalho ─────────────────────────────────────────────── */
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

/* ── Corpo ─────────────────────────────────────────────────── */
.modal-corpo {
  color:       #94a3b8;
  font-size:   14px;
  line-height: 1.6;
  margin:      0 0 24px;
}

/* ── Rodapé ────────────────────────────────────────────────── */
.modal-footer {
  display:         flex;
  gap:             10px;
  justify-content: flex-end;
}
```

## Código HTML

```html
<!-- Trigger -->
<button class="btn btn-danger" onclick="abrirModal('modal-excluir')">
  Excluir item
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
      <h2 class="modal-titulo" id="modal-excluir-titulo">Excluir item?</h2>
      <button
        class="modal-fechar"
        onclick="fecharModal('modal-excluir')"
        aria-label="Fechar"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"/>
          <line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
      </button>
    </div>

    <p class="modal-corpo">
      Esta ação não pode ser desfeita. O item será removido permanentemente.
    </p>

    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="fecharModal('modal-excluir')">
        Cancelar
      </button>
      <button class="btn btn-danger" onclick="confirmarExcluir()">
        Excluir
      </button>
    </div>
  </div>
</div>
```

## Código JS

```javascript
function abrirModal(id) {
  const overlay = document.getElementById(id);
  if (!overlay) return;
  overlay.style.display = 'flex';
  // força reflow para a animação funcionar
  requestAnimationFrame(() => overlay.classList.add('modal-aberto'));
  // foca o overlay para acessibilidade e captura de Escape
  overlay.focus();
  // listener de Escape
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
  // aguarda a transição antes de esconder
  overlay.addEventListener('transitionend', () => {
    overlay.style.display = 'none';
  }, { once: true });
}

function fecharModalOverlay(event, id) {
  // fecha somente se o clique for no overlay, não no modal em si
  if (event.target === event.currentTarget) fecharModal(id);
}

// Exemplo de ação de confirmação
function confirmarExcluir() {
  // sua lógica aqui
  fecharModal('modal-excluir');
}
```

## Adaptações comuns

- **Modal informativo** (sem ação destrutiva): trocar `.btn-danger` por `.btn-primary` no rodapé.
- **Modal com formulário**: substituir `.modal-corpo > p` por `<form>` com inputs.
- **Modal centralizado no painel** (não na tela): trocar `position: fixed` por `position: absolute` no overlay e garantir `position: relative` no pai.
- **Sem backdrop blur**: remover `backdrop-filter: blur(4px)`.
- **Tamanho maior**: aumentar `max-width` (ex: `640px` para formulários extensos).

## Dependências

CSS e JS nativos. Sem dependências externas. Os botões usam as classes de `snippets/ui/buttons/button-primary.md`.

## Notas

- `aria-modal="true"` e `aria-labelledby` são obrigatórios para acessibilidade com leitores de tela.
- O overlay recebe `tabindex="-1"` para poder receber foco programaticamente.
- Sempre remover o listener de Escape ao fechar para evitar vazamento de memória.
- Em aplicações com múltiplos modais simultâneos, usar um `z-index` crescente por instância.
