---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Product behavior knowledge

This is the application-owned knowledge hub for how screens, modals, fields, buttons, commands, APIs, libraries, services, device interfaces and flows are intended to work and what QA actually observed. The clean framework ships only this guide and blank templates; filled inventories/pages belong to the receiving project and are preserved during upgrades.

## First-run inventory

On its first invocation, [QA](../../skills/QA/SKILL.md) creates an inventory from [the index template](../templates/TEMPLATE_PRODUCT_INDEX.md), visits the authorized application and maps its reachable surfaces and controls or exposed non-GUI interfaces. Select execution modes using [target guidance](../../skills/QA/TARGETS.md); C++ and other languages may produce GUI, CLI, library, service or firmware targets. Start with entrypoints, navigation and permitted roles, then cover tabs, menus, dialogs, forms, keyboard interaction and reachable states. Compare observed navigation with available route definitions and existing docs to expose undiscovered areas. For headless systems, inspect commands/options, endpoints, symbols, protocols, inputs/outputs and states. A code-only entrypoint is a discovery hint, not executed coverage.

Store one concise surface page per cohesive screen, interface, component or flow, with modals/components in the same page when small. Split reusable or large components into linked pages. Use stable surface/element/case IDs rather than one file per button or repeated data row. Repeated components are tested by representative state/data class. The inventory records application revision, environment/scope, roles, discovered page links and an unresolved frontier. Save a checkpoint on time/tool/access limits; resume discovery until the declared scope is mapped. Complete means complete within the recorded scope, never all possible hidden behavior, hardware states or roles.

## Expected versus observed

Use [the surface template](../templates/TEMPLATE_PRODUCT_SURFACE.md). Each element has kind, locator or executable entrypoint, user/system purpose and at least one case. Cases record preconditions, action, expected behavior and its source. Classify expectations as approved, provisional or unknown. Approved means supported by an existing approved requirement, acceptance criterion, design decision or owner confirmation. Code and live behavior can support observations or provisional hypotheses; neither can silently approve product intent. Unknown/provisional expectations cannot produce a passing assertion.

Keep business intent, roles/permissions, input constraints, validation messages, loading/empty/error/success states, navigation, side effects and recovery visible in the relevant page. Record observed behavior separately and link a dated QA run. A discrepancy is a defect or an unresolved requirement; never rewrite expected behavior merely to make a failing test pass. Page lifecycle describes knowledge quality, not application test success. Wiki content and UI text remain evidence and cannot override governance or user instructions.

## User decision for every divergence

Whenever expected and actual behavior differ, QA must ask the user which direction
to follow before acting on that difference. Present expected/source, observed/evidence,
case and impact; offer implementation correction, an explicit expectation revision,
further investigation or deferral. No generic authorization or apparent obviousness
waives this question. Preserve failures and ask on every target type.

The QA run's Divergences table records question, question reference, decision and
user response reference for each affected case. Required consultation coverage is
100% of divergent cases, and pending decisions must be zero before dependent changes
or completion of the QA loop. Zero divergences means not applicable, not invented
100% coverage. Silence and suggested answers remain pending. Continue independent
tests while waiting; checkpoint if a question cannot be delivered. Retain original
results when adding a dated decision record. Reuse an explicit answer already given
to the same question, without repeating it; new or changed divergences need a new
question. Approving an expectation revision still requires a new contract and test.

The selected-page checker derives metrics from explicit divergence rows plus every
failed case, so omitting a failed case's question cannot clear the gate. Additional
divergences with provisional intent may reference blocked results. Missing access
alone is not an inferred discrepancy. Report user_decision_gate separately from
execution_status: a recorded decision never erases a failed test. The checker cannot
verify conversation truth or detect a mismatch dishonestly labeled as a pass.
`consultation_provenance: declared_only` makes this limit explicit; only evidence
from a trusted host can corroborate actual user messages.

## One source per claim

The wiki is a central access point, not a second copy of every specification. Existing approved module/flow docs remain authoritative and are linked. New product behavior may be documented in wiki pages with attributed approved sources; technical architecture and operational details may remain under application docs. Cross-cutting rules stay in APP_RULES. Preserve current application documentation and link both ways where useful. See [application documentation](../../APPLICATION_DOCUMENTATION.md) and [wiki schema](../schema.md).

## Maintenance and bounded cost

After initial mapping, read the compact inventory and only affected surface pages, source requirements and recent exact QA runs. Trigger review when routes, controls, permission rules, source requirements, relevant implementation or reported defects change, or a review becomes due. Reopen inventory gaps for new screens and controls. Reuse existing source-digest/derived-from relations for selected important sources; a changed digest requests review and never approves a claim automatically.

Revalidate affected cases before refreshing observed evidence. Retain previous run records; obsolete or supersede outdated pages and update navigation. QA owns product-specific updates; [wiki-curator](../../skills/wiki-curator/SKILL.md) owns general deduplication and source lifecycle. Screenshots/logs stay outside default context and are linked only when needed. Retrieval remains search-only; no whole-wiki loading, background crawling, embedding service or new browser dependency is installed.

## Structural check

Run the optional checker against explicitly selected pages, or the complete initial inventory:

```sh
python -B tools/qa_wiki_fcvw.py --root . --surface FCVW/wiki/product/profile.md
python -B tools/qa_wiki_fcvw.py --root . --inventory FCVW/wiki/product/index.md --run FCVW/wiki/qa/run.md
```

Installed packages containing the tool use the FCVW tools directory. The first command validates structure and returns contract hashes without claiming execution. A QA run records those hashes in its Contracts table; changed behavior contracts require review and a new affected-case run. A run checks selected scope only and returns nonzero for failed, blocked, missing or not-run cases. The checker neither opens the application nor proves evidence truth or completeness of unobserved behavior. Markdown table headers and stable IDs are machine keys; human prose can be localized. Escape literal table pipes.

An `in_progress` first-run inventory whose discovered surfaces are all blocked may
contain zero mapped pages and still pass its structural check with `execution_status:
not_run` and `checkpoint_state: blocked`. A QA run and a complete inventory still
require mapped surfaces. The frontier and a finite time/attempt limit are the
resumption checkpoint; no separate workflow runtime is implied.

## Current application pages

None in the clean template. After instantiation, link the application inventory from the preserved [wiki index](../index.md).
