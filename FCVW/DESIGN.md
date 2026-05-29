---
version: "1.0.0"
name: "FrameCode VibeWork Base Design"
description: "Premium Minimalist Dark Mode design system with fluid micro-animations and sleek surfaces."
colors:
  primary: "#8b5cf6"
  secondary: "#1a1d24"
  accent: "#8b5cf6"
  background: "#0b0e14"
  surface: "#1a1d24"
  surface-alt: "#20232b"
  text-primary: "#d1d5db"
  text-secondary: "#9ca3af"
  border: "#3a3c42"
  success: "#10b981"
  warning: "#f59e0b"
  error: "#ef4444"
  on-primary: "#ffffff"
  on-accent: "#ffffff"
typography:
  h1:
    fontFamily: "Inter, sans-serif"
    fontSize: "24px"
    fontWeight: "600"
    lineHeight: "32px"
  h2:
    fontFamily: "Inter, sans-serif"
    fontSize: "18px"
    fontWeight: "500"
    lineHeight: "24px"
  h3:
    fontFamily: "Inter, sans-serif"
    fontSize: "14px"
    fontWeight: "400"
    lineHeight: "20px"
  body-md:
    fontFamily: "Inter, sans-serif"
    fontSize: "14px"
    fontWeight: "400"
    lineHeight: "22px"
  code:
    fontFamily: "Fira Code, monospace"
    fontSize: "13px"
    fontWeight: "400"
    lineHeight: "20px"
rounded:
  sm: "6px"
  md: "8px"
  lg: "12px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "36px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
    padding: "{spacing.sm} {spacing.md}"
    height: "{spacing.xl}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.md}"
    padding: "{spacing.sm} {spacing.md}"
    border: "1px solid {colors.border}"
    height: "{spacing.xl}"
  input:
    backgroundColor: "{colors.background}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.md}"
    padding: "{spacing.sm} {spacing.md}"
    border: "1px solid {colors.border}"
    height: "{spacing.xl}"
  card:
    backgroundColor: "{colors.surface-alt}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
    border: "1px solid {colors.border}"
  modal:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
    border: "1px solid {colors.border}"
  table:
    backgroundColor: "transparent"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.md}"
    padding: "0"
  navbar:
    backgroundColor: "{colors.background}"
    textColor: "{colors.text-primary}"
    height: "64px"
    border: "1px solid {colors.border}"
  badge:
    backgroundColor: "{colors.surface-alt}"
    textColor: "{colors.text-secondary}"
    rounded: "{rounded.sm}"
    padding: "{spacing.xs} {spacing.sm}"
---

## Overview

This document establishes the official visual identity, component tokens, and user experience standards for the VibeWork application. The default visual identity is a **Premium Minimalist Dark Mode** prioritizing high visual depth, fluid micro-animations, and keyboard-first accessibility. 

The YAML front matter above acts as the Single Source of Truth (SSOT) for UI components. AI agents must extract the variables programmatically to generate CSS, Tailwind classes, or React components.

## Design System Source of Truth

`DESIGN.md` is the only canonical design-system source for the framework. The former `FCVW/snippets/` sample-storage model is discontinued.

Rules:

- Do not create or depend on a framework-level snippets directory.
- Store visual rules, tokens, component contracts, and interaction constraints in this document.
- Generate downstream CSS, Tailwind, React, or platform-specific components from this document during instantiation or implementation.
- Keep project-specific examples in the application codebase, not in the generic FCVW framework layer.

## Colors

The color palette was strictly defined to avoid generic plain colors, utilizing deep dark tones to prevent eye strain while ensuring components "pop" off the background.

- **Background & Surfaces**: `{colors.background}` is the absolute lowest z-index layer. Panels (`{colors.surface}`) and cards (`{colors.surface-alt}`) have progressively lighter hex values to simulate lighting elevation.
- **Brand/Primary**: We use a sleek violet accent (`{colors.primary}`) because it conveys a premium, modern feel.
- **Text**: Pure white is avoided to reduce blooming. `{colors.text-primary}` guarantees an excellent WCAG AA contrast ratio against the dark background. Helper texts use `{colors.text-secondary}`.
- **Feedback**: Standard semantic colors (`success`, `warning`, `error`) are used to convey state instantly.

## Typography

Google Fonts like **Inter** or **Outfit** are chosen for their high geometric legibility, which is crucial for technical dashboards.

- **H1 (Main Title)**: Used solely for page headers. The tight line-height ensures titles feel cohesive.
- **H2 (Section Title)**: Groups major blocks of content.
- **Body-Md**: The workhorse font token. Sized at 14px to balance readability with high information density.
- **Code**: `Fira Code` or `JetBrains Mono` for logs and technical readouts.

## Layout

The layout is built upon an 8-point spatial grid system.

- **Base Grid Unit**: `{spacing.xs}` (4px) or `{spacing.sm}` (8px).
- **Responsive Sizing**: Layouts must dynamically reflow under three viewport targets without breaking: `1920x1080` (spacious), `1024x768` (dense), and `800x600` (mobile/compact focus).
- **Margins**: Components must maintain at least `{spacing.md}` between sibling elements.

## Elevation & Depth

To build visual hierarchy without overwhelming borders, we rely on background lightening and glassmorphism.

- Modals and Overlays must use a backdrop-filter blur.
- Elevated cards (e.g., `{components.card}`) utilize a semi-transparent `{colors.surface-alt}` to allow subtle background bleeding, creating a premium depth effect.

## Shapes

Rounding scales follow modern SaaS conventions, eschewing sharp corners.

- **Buttons & Inputs**: Use `{rounded.md}` (8px) for friendly, approachable interaction zones.
- **Badges/Tags**: Use `{rounded.sm}` (6px) since their overall height is smaller.
- **Modals/Dialogs**: Use `{rounded.lg}` (12px) to softly frame large intrusive content.

## Components

The YAML front matter lists explicit tokens for components. When building them, you must respect these mapped values.

- **Buttons**: Minimum `{spacing.xl}` (36px) height is enforced for touch accessibility and click ease. 
- **Modals**: Native system alerts are forbidden. All modals must trap keyboard focus.
- **Scrollbars**: Native scrollbars dilute the dark interface. They must be themed with custom CSS to match the `{colors.surface}` track and `{colors.border}` thumb.

## Do's and Don'ts

### Do's
- **DO verify WCAG Contrast**: Ensure any custom button backgrounds maintain high contrast against `{colors.on-primary}`.
- **DO use Custom Scrollbars**: Native browser scrollbars break immersion. Always use custom pseudo-elements (`::-webkit-scrollbar`).
- **DO run a Visual Description Audit (VDA)**: When generating components, simulate a browser render mentally. Write a markdown checklist verifying that paddings equal `{spacing.md}` and colors match the YAML front matter.
- **DO infer missing elements gracefully**: If a missing visual state (e.g., hover color) is required, calculate it based on the closest token (e.g., 10% lighter than `{colors.primary}`) and document it.

### Don'ts
- **DON'T use generic named colors** like `red` or `blue` in the CSS. Always use the hex references from the YAML.
- **DON'T overlap text**: Long labels must gracefully truncate with an ellipsis or break lines.
- **DON'T guess padding values**: Stick strictly to the `{spacing.*}` scale. Avoid magic numbers like 13px or 17px.
