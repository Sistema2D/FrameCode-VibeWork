# FrameCode VibeWork — Empty Governance Templates

This folder contains empty, reusable templates from the FrameCode VibeWork framework.

In FrameCode VibeWork, the official completed documents reside at the root of the application. This folder is not the canonical filled source of the project; it serves to preserve generic versions of the documents, reusable in other projects.

Structural rule: when the structure of an official root document is altered, the corresponding template in this folder must receive an equivalent adjustment, maintaining placeholders and removing project-specific data.

The rules to transform the framework into a concrete application, including renaming folders, titles, and placeholders, reside in `INSTANTIATION.md`. This folder must not be altered by global instantiation replacements.

## Contents

- `MANIFEST.md`
- `BRIEFING.md`
- `PLANNING.md`, when there is a corresponding template
- `VERSIONING.md`, when there is a corresponding template
- `AUDIT.md`
- `TESTS.md`
- `SECURITY.md`
- `DATA.md`
- `AI.md`
- `REFACTORING.md`
- `RELEASE.md`
- `ARCHITECTURAL_DECISIONS.md`
- `wiki/`

## Canonical Location Upon Instantiation

When applying this framework to an application, the completed documents must reside at the root of the project, and formal records must use root folders such as `Plans/`, `changelogs/`, `troubleshooting/`, `decisions/`, `audits/`, `briefings/`, and `wiki/`.
