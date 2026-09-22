# Template: product surface

Follow the [product contract](../product/README.md).

Use a cohesive screen, modal, component, flow, cli, api, service, library, device, firmware or protocol surface. The route field may be a URL or logical entrypoint; element locators may identify commands, symbols or signals. Use the applicable execution mode from QA target guidance. Preserve expected and observed information separately; meaningful placeholders must be replaced before checking.

```markdown
---
schema: "fcvw/wiki@1"
id: "UI-profile"
artifact_role: "record"
record_scope: "application"
owner: "<product owner>"
upgrade_strategy: "preserve"
retrieval_scope: "search_only"
title: "<surface name>"
type: "component"
qa_surface: "screen"
route: "/profile"
status: "draft"
confidence: "low"
created_at: "YYYY-MM-DD"
last_reviewed: "YYYY-MM-DD"
sources:
  - "<requirement or observed evidence reference>"
tags:
  - "quality-validation"
---

# Product surface

## Purpose and context

Describe users or system consumers, business goal, entry/exit paths, roles, permissions, inputs, side effects and relationships. State whether this page was interactively visited, executed through a harness, simulated, physically exercised or inferred from sources. Record keyboard/focus, responsive, loading, empty, error, success and recovery states that apply; explain exclusions.

## Elements

| element_id | kind | locator | purpose |
|---|---|---|---|
| field-name | field | textbox: Name | Enter the display name |
| button-save | button | button: Save | Request saving the form |

## Cases

| case_id | element_ids | preconditions | action | expectation | expected | source |
|---|---|---|---|---|---|---|
| save-valid | field-name, button-save | Authenticated test user and disposable data | Enter a name and activate Save | unknown | unknown | unknown |

## Observed behavior

Link the latest exact QA run, revision and observation date. Distinguish actual results from the expected contract above. Do not populate this section from code reading alone as if it were live testing.

## Gaps and maintenance

List missing requirements, untested states, unavailable roles, identified defects and review triggers. Link selected tracked sources when digest-based review is useful. Preserve prior evidence when replacing a claim.

## Sources and related pages

Add portable Markdown links to approved requirements, existing module docs, inventory, related surfaces and QA reports. Unconfirmed expected behavior remains provisional or unknown until sourced approval is available.
```
