---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "merge"
---

# Wiki taxonomy

Start with a small canonical set and add project tags only when retrieval improves.

## Themes

- `planning-governance`
- `release-governance`
- `knowledge-governance`
- `framework-feedback`
- `ai-operations`
- `quality-validation`
- `regression-prevention`
- `security-data`
- `design-ux`
- `refactoring-hygiene`
- `environment-deploy`
- `project-instantiation`

## Rules

- lowercase kebab-case;
- prefer one theme and a few precise tags;
- do not create synonyms in multiple languages;
- merge aliases into the canonical tag;
- tags aid discovery and never replace sources or links.
- confirmed regression records use the `regression-prevention` theme plus the affected domain tag.
