# Template: initial product inventory

Follow the [product contract](../product/README.md).

Copy to the receiving application's product index and replace placeholders. Link it from the preserved wiki index. Do not fill this template in the clean framework.

```markdown
---
schema: "fcvw/wiki-index@1"
artifact_role: "project_profile"
owner: "project"
upgrade_strategy: "preserve"
inventory_status: "in_progress"
scope: "<environment, entrypoints and bounded discovery scope>"
app_revision: "<tested build or commit>"
roles: "<roles actually accessible>"
---

# Product inventory

## Discovery checkpoint

Record execution modes, runtime/toolchain or hardware prerequisites, visited navigation or non-GUI entrypoints, explored dialogs/protocols/states, available roles, excluded actions, discovery time, next entrypoint and remaining limits. Set complete only after mapped entries and resolved frontier cover the declared scope. Missing tooling or access keeps this in progress.

## Surfaces

| surface_id | page | kind | route | discovery |
|---|---|---|---|---|
| UI-profile | FCVW/wiki/product/profile.md | screen | /profile | not_visited |

## Frontier

| target | reason | status |
|---|---|---|
| /profile | Initial mapping not yet performed | open |

## Navigation

Add portable Markdown links to mapped pages and the product operating contract. The machine page column alone is not a navigation link.
```
