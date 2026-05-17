# DESIGN.md

Visual and user experience guidelines for the application.

> This is a template. Replace the fields between `<...>` with the actual information of the project. Remove sections that do not apply to the chosen platform or stack.

This document records the expected UI/UX standards for future changes. It must be consulted before any visual modification, screen creation, component adjustment, or interaction change.

## Objective

`<Describe in one or two sentences the visual tone and purpose of the design: e.g., minimalist dark for technical use, colorful and friendly for casual use, etc.>`

## Visual Principles

- `<principle 1>`
- `<principle 2>`
- `<principle 3>`
- Every icon-only or non-obvious control must have a tooltip.
- Visual states must be explicit: active, hover, focus, pressed, disabled, error, and success.
- The layout must work in normal, maximized, and minimum supported window sizes.

## Official Palette

`<Define the color palette of the project. Record the exact values used in the code so that future implementations remain coherent.>`

```text
<BACKGROUND_COLOR>    <value>
<PANEL_COLOR>         <value>
<TEXT_COLOR>          <value>
<HIGHLIGHT_COLOR>      <value>
<ERROR_COLOR>         <value>
<SUCCESS_COLOR>       <value>
<WARNING_COLOR>       <value>
```

### Palette Usage

- General background: `<BACKGROUND_COLOR>`.
- Panels and surfaces: `<PANEL_COLOR>`.
- Main text: `<TEXT_COLOR>`.
- Primary action and active state: `<HIGHLIGHT_COLOR>`.
- Error or destruction: `<ERROR_COLOR>`.
- Success: `<SUCCESS_COLOR>`.
- Warning: `<WARNING_COLOR>`.

Do not introduce new color families without a specific plan and updating this document.

## Typography

```text
Default text: <font>, <size>
Main title: <font>, <size>
Subtitles: <font>, <size>
Helper text: <font>, <size>
Icons: <icon font>
Code: <monospaced font>
```

### Typographical Rules

- Use `<main font>` for interface text.
- Use `<icon font>` for icons.
- Use `<monospaced font>` only for code, paths, and logs.
- Ensure long texts use ellipsis, line breaks, or a scrollable area; never overlap.

## General Layout

### Structure

`<Describe the layout structure: sidebar, main panel, cards, modals, etc.>`

### Relevant Dimensions

`<Record margins, button sizes, card border radii, and other fixed metrics of the project.>`

- Main outer margin: `<value>`.
- Navigation buttons: `<width x height>`.
- Main card border radius: `<value>`.
- Secondary card border radius: `<value>`.

### Layout Rules

- Do not place a card inside another card.
- Use cards only for functional regions, repeated items, and modals.
- Maintain stable dimensions for toolbars, buttons, lists, and cards.
- No hover, label, or dynamic state should shift the layout unexpectedly.

## Buttons

### Icon-Only Buttons

Use icon-only buttons for frequent or familiar actions.

Rules:

- Always include a tooltip.
- Maintain a minimum clickable area of `<value>` for main actions.
- Destructive actions must use visual warning styling.

### Buttons with Text

Use text when:

- the action is ambiguous without a label;
- there is a risk of a destructive error;
- the action appears in a confirmation modal;
- the button is primary in a form.

## Tooltips

Mandatory for:

- icon-only buttons;
- compact controls;
- any action whose consequence is not obvious.

Tooltips must not persistently cover the control nor go outside the visible window area.

## Cards and Surfaces

### Main Cards

- Background: `<color>`.
- Radius: `<value>`.
- The card should frame the entire functional area of the screen.

### Secondary Cards

- Background: `<color>`.
- Radius: `<value>`.
- Subtle border.

## Modals

Rules:

- All modals must be native to the application itself, without system dialog boxes.
- Modals must be centered relative to the application window.
- The rest of the application should be visually layered beneath the modal.
- Controls behind the modal must be disabled.
- `Escape` should cancel when safe.
- `Enter` should confirm when the action is clear.
- Destructive actions must use a visually distinct button.

## Scrollbars

`<Adapt according to the platform and toolkit. Describe how scrollbars should appear in dark areas.>`

Mandatory rule:

- the scrollbar background must use the same background color as the container in which it appears;
- the thumb must be lighter than the background, but not pure white;
- apply this standard to all new or modified scrollable areas.

## Visual States

### Active

- Background: `<soft highlight color>`.
- Border: `<highlight color>`.
- Must be more persistent and noticeable than hover.

### Hover

- Increase contrast without changing size.
- Never shift the layout.

### Focus

- Must be visible via a border or outline.
- Must work with keyboard navigation.

### Disabled

- Text and background must have reduced contrast.
- Action must not visually respond as active.

### Error

- Use `<ERROR_COLOR>` or variations.
- Messages must be clear and not confused with success.

### Success

- Use `<SUCCESS_COLOR>` or discrete variations.
- Temporary feedback should return to normal state automatically.

## Accessibility and Usability

- Every mouse action must have a reasonable keyboard alternative when possible.
- Modals must trap focus.
- Texts must have sufficient contrast against the background.
- Icons must have tooltips.
- Clickable areas must be large enough for comfortable use.

## Rules for New Screens

When creating a new screen:

1. Use a main card with an appropriate background.
2. Define a compact toolbar for actions.
3. Use tooltips on all icon-only actions.
4. Ensure a stable layout during resizing.
5. Register any new standard in this document.
6. Create or update the corresponding plan in `Plans/`.

## Rules for New Components

New components must:

- reuse existing elements, styles, and standards;
- have hover, focus, pressed, and disabled states;
- not create scrollbars of incorrect colors in dark areas;
- be tested in normal, maximized, and minimum window sizes.

## Visual Review Criteria

Before completing a visual change, check:

- Is there overlapping text or controls?
- Does the text fit in the available space?
- Is the active state obvious?
- Is the hover subtle and consistent?
- Is the keyboard focus visible?
- Does the scrollbar match the container?
- Do icons have tooltips?
- Are destructive buttons differentiated?
- Does the maximized window preserve clicking and focus?
- Does the minimum window keep main actions accessible?
- Does the result follow the standards of this document?
