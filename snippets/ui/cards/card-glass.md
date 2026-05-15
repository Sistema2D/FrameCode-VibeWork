---
titulo: "Card com efeito glass — tema escuro"
stack: "web"
tipo: "card"
tags: [dark-theme, glassmorphism, hover, card, painel, stat]
dependencias: ["CSS nativo"]
testado: "sim"
criado: 2026-05-15
atualizado: 2026-05-15
---

# Card Glass — Tema Escuro

Card com efeito glassmorphism para tema escuro. Inclui: card simples, card interativo, card com header/footer e card de estatística.

## Código CSS

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

/* Interativo */
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

/* Borda colorida à esquerda */
.card-destaque-esquerda {
  border-left: 3px solid var(--cor-destaque, #6366f1);
  padding-left: 17px;
}
```

## Código HTML

```html
<!-- Card simples -->
<div class="card">
  <p class="card-body">Conteúdo aqui.</p>
</div>

<!-- Card com header e footer -->
<div class="card">
  <div class="card-header-area">
    <div>
      <h3 class="card-titulo">Título</h3>
      <p class="card-subtitulo">Subtítulo</p>
    </div>
    <span class="card-badge">Novo</span>
  </div>
  <div class="card-body">Corpo do card.</div>
  <div class="card-footer">
    <span style="font-size:13px;color:#64748b">Atualizado há 2h</span>
    <button class="btn btn-ghost btn-sm">Ver mais</button>
  </div>
</div>

<!-- Card interativo -->
<div class="card card-interativo" role="button" tabindex="0" onclick="...">
  <div class="card-body">Clique para navegar.</div>
</div>

<!-- Stat card -->
<div class="card card-stat">
  <span class="card-stat-label">Usuários ativos</span>
  <span class="card-stat-valor">1.284</span>
  <span class="card-stat-delta positivo">▲ 12,4%</span>
</div>

<!-- Borda colorida -->
<div class="card card-destaque-esquerda">
  <h3 class="card-titulo">Aviso</h3>
  <p class="card-body">Texto do aviso.</p>
</div>
```

## Adaptações comuns

- **Glass sobre imagem**: ativar `backdrop-filter: blur(8px)` e garantir fundo no elemento pai.
- **Grid de cards**: `display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:16px` no container.
- **Card aninhado (subnível)**: `background:rgba(255,255,255,0.03); border-radius:8px`.
- **Sombra base**: adicionar `box-shadow: 0 4px 24px rgba(0,0,0,0.3)` ao `.card`.

## Dependências

CSS nativo. Botões no footer usam `snippets/ui/buttons/button-primary.md`.

## Notas

- Cards clicáveis devem ter `role="button"` e `tabindex="0"` para acessibilidade.
- Não aninhar `.card` dentro de outro `.card` — usar fundo ligeiramente diferente para subnível.
