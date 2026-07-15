---
schema: "fcvw/project-design@1"
artifact_role: "project_profile"
owner: "project"
upgrade_strategy: "preserve"
instantiation_status: "pending"
---

# Design and experience contract

## Experience principles

- Primary users and environment:
- Cognitive-load constraints:
- Accessibility target:
- Responsive/mobile commitment:
- Supported themes:

## Physical source of truth

Design tokens must be implemented in `<code path>`. This document explains intent and constraints; it does not replace runtime tokens.

## Tokens

| Group | Canonical names | Rules |
|---|---|---|
| Color | | |
| Typography | | |
| Spacing | | |
| Radius | | |
| Border | | |
| Elevation | | |
| Motion | | |
| Z-index/layers | | |

## Component contracts

For shared components define states, keyboard behavior, focus, labels, error feedback, density, loading, empty, disabled, destructive, and responsive behavior.

## Validation

- Verify keyboard-only operation and visible focus.
- Check contrast and non-color cues.
- Test at declared viewport breakpoints and zoom.
- Compare screenshots only when visual fidelity matters.
- Confirm motion respects reduced-motion preferences.
- Record exceptions with owner and review date.
