# Snippets — Reusable Code Library

This folder contains code references ready to be adapted and applied during development.

The goal is for the AI and the developer to reuse tested implementations of visual components and behavioral patterns without starting from scratch for every new screen or session.

The Snippets Gallery (`snippets/gallery.html`) allows visualizing the components in real-time and copying the required code.

---

## AI Maintenance

The AI has the permission and duty to:
- **Update**: Adjust the code of existing snippets as the user requests visual changes or functional improvements.
- **Include**: Create new snippets when a useful component is developed and validated.
- **Delete**: Remove obsolete snippets or those that no longer meet the project's design standards.
- **Synchronize**: Ensure that `gallery.html` reflects the available snippets.

- Consult before implementing a UI component (button, modal, card, bar, etc.)
- Maintain visual consistency between sessions and projects.
- Reduce rework: the snippet already solves the base case; just adapt colors, sizes, and texts.
- Record approved implementations for future reuse.

This folder **does not replace** `DESIGN.md` (which defines visual *rules*) nor `wiki/components/` (which documents project modules). It contains *concrete code* ready for use.

---

## Global Reuse

To maintain the same visual identity across multiple projects, the `snippets/` folder (especially the `tokens.css` file) must be treated as a shared library. It is recommended to use **Git Submodules** to synchronize this folder between repositories, ensuring that visual adjustments made in one project are propagated to the others.

---

## Structure

```text
snippets/
├── README.md              ← this file (schema)
├── ui/
│   ├── buttons/           ← buttons and variants
│   ├── modals/            ← modals, overlays, dialogs
│   ├── cards/             ← cards, panels, surfaces
│   ├── navigation/        ← navbars, sidebars, tabs, breadcrumbs
│   ├── forms/             ← inputs, selects, checkboxes, sliders
│   ├── backgrounds/       ← gradients, background patterns, textures
│   └── animations/        ← transitions, micro-animations, loaders
└── patterns/
    ├── loading/            ← loading states
    ├── empty-states/       ← empty states and placeholders
    └── feedback/           ← toasts, alerts, banners, badges
```

---

## Mandatory Frontmatter

Every snippet file must start with YAML frontmatter.

```yaml
---
title: "<descriptive name of the snippet>"
stack: "web | mobile | desktop | cli | agnostic"
type: "button | modal | card | form | navigation | background | animation | pattern"
tags: [dark-theme, glassmorphism, hover, confirmation]
dependencies: ["Native CSS", "Native JS"]
tested: "yes | no"
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

---

## Naming Pattern

```text
{type}-{variant}-{modifier}.md
```

Examples:

```text
button-primary.md
button-danger-icon.md
modal-confirmation.md
card-glass.md
card-list-item.md
background-dark.md
toast-success.md
input-with-label.md
```

---

## How to Use (Workflow for AI)

When receiving a UI component implementation request:

1. Check if there is a corresponding snippet in `snippets/ui/` or `snippets/patterns/`.
2. Read the identified snippet.
3. Adapt colors, sizes, texts, and behaviors according to `DESIGN.md` of the project.
4. Implement without reinventing the base pattern.
5. If the result is significantly better than the original snippet, or if the user requests an adjustment in the pattern, the AI must update the corresponding snippet or create a new one.

Upon concluding a change in `snippets/`, the AI must update `gallery.html` to reflect the change.

When no snippet exists:

1. Implement following `DESIGN.md`.
2. Upon concluding and validating, evaluate if it is worth creating a reusable snippet.
3. Create the snippet in the correct folder with complete frontmatter.

---

## How to Contribute New Snippets

Criteria to promote code to a snippet:

- The component was visually and functionally validated.
- The pattern can be reused in other projects or screens with minimal adaptation.
- The code is self-contained or declares dependencies clearly.
- The snippet does not replicate content already covered by another existing snippet.

Minimum structure of a snippet:

```markdown
---
[frontmatter]
---

# Snippet Title

Brief description of the component, when to use it, and existing variations.

## Preview (optional)

Describe or illustrate the expected visual result.

## Code

\`\`\`html
<!-- code here -->
\`\`\`

## Common Adaptations

- How to change the highlight color: ...
- How to add an icon: ...
- How to disable: ...

## Dependencies

- Native CSS: no external dependencies.
- or: requires CSS variables defined in `:root { --highlight-color: ... }`.

## Notes

Observations on compatibility, limitations, or context of use.
```

---

## Loading by Component Type

| Component to Implement | Folder to Consult |
|---|---|
| Button, CTA, action | `snippets/ui/buttons/` |
| Modal, dialog, confirmation | `snippets/ui/modals/` |
| Card, panel, surface | `snippets/ui/cards/` |
| Navbar, sidebar, tabs | `snippets/ui/navigation/` |
| Input, select, form | `snippets/ui/forms/` |
| Background, gradient, texture | `snippets/ui/backgrounds/` |
| Transition, hover, animation | `snippets/ui/animations/` |
| Loading state | `snippets/patterns/loading/` |
| Empty screen, placeholder | `snippets/patterns/empty-states/` |
| Toast, alert, banner | `snippets/patterns/feedback/` |
