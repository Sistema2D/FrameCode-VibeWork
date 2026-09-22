---
schema: "fcvw/adr@1"
id: "ADR-0007"
status: "accepted"
date: "2026-09-22"
artifact_role: "record"
owner: "framework"
upgrade_strategy: "preserve"
record_scope: "framework"
retrieval_scope: "routed"
language: "en-US"
---

# ADR-0007: Product knowledge and multidisciplinary QA

## Context and decision

The user explicitly requested an agent named QA, first-run mapping of application controls, ongoing functional tests and wiki maintenance, then clarified that it must work across web, C++, firmware, native Windows/Linux and other application types. Adopt an on-demand agent profile with target-specific execution guidance and existing wiki schemas. First use maps reachable surfaces or saves a resumable checkpoint; later work selects affected pages and interfaces. Approved expected behavior and actual observations remain separate. Existing approved specifications retain authority.

The optional standard-library checker reads explicitly selected pages. It checks declared elements/cases, discovery gaps, expectation classification, runtime provenance and contract hashes. It does not run the application or certify truth. UI, command, API, library, service and device interfaces share this contract. Execution adapters come from host capabilities and project harnesses; no universal driver, background agent, dependency or hardware service is installed.

## Alternatives and consequences

A browser-only agent would exclude headless and physical systems. A universal automation runtime would add dependencies and pretend capability across unavailable hosts/hardware. Extending the generic curator would mix source curation and execution responsibilities. Choose one narrow QA role across disciplines, with execution modes selected only when relevant. Mapping has a real initial cost; later selective maintenance bounds repeated context and interaction cost. Static checks cannot establish exhaustive discovery, semantic correctness or genuine execution.

## Agent proposal: problem and existing coverage

This section fills the [agent proposal](../governance/TEMPLATE_AGENT_OR_SKILL_PROPOSAL.md) for the [implementation plan](../Plans/completed/P2-R4-2026-09-22-product-wiki-qa.md), priority P2/risk R4. Recurrence and percentage coverage have not been measured. The user's explicit creation instruction takes precedence over speculative quantitative gate estimates.

| Existing asset | Coverage evidence | Gap |
|---|---|---|
| wiki-curator | Generic source/knowledge lifecycle | No live application discovery/test loop |
| Hephaestus | Focused UI diagnosis and repair | No cross-platform evidence/inventory ownership |
| TESTS | Test policy and preservation checks | No first-run product mapping procedure |

| Creation metric | Evidence and decision |
|---|---|
| Recurrence / coverage percentage | Unmeasured; explicit user request authorizes creation without fabricated threshold claims |
| Token ROI | Full instructions stay outside base-loaded AGENTS; no measured savings claim |
| Risk ROI | Explicit gaps and source authority prevent untested passes and defect normalization |
| Narrow scope | One QA loop and product knowledge output; no source-code repair or general wiki sweep |
| Validation | This implementation task, structural negative cases and isolated live fixtures |

Asset: agent profile [QA](../skills/QA/SKILL.md), maintained by the framework maintainer. Trigger family: initial mapping, functional QA, product-wiki maintenance. Primary output: inventory/checkpoint, behavior contracts and scoped run evidence. Non-responsibilities: deployment, unapproved physical actions, production cleanup, product repair and inferred acceptance criteria. Catalog, context route, STACK, filesystem and release record are updated; AGENTS stays unchanged. Next review follows downstream execution gaps or measured excess mapping cost.

## Curator improvement report

This section fills the [self-improvement report](../governance/TEMPLATE_SELF_IMPROVEMENT_REPORT.md). Canonical product documentation now distinguishes expected behavior from observations; the curator needed an explicit handoff preserving that distinction. Rule drift is the evidence metric. No independent failure count or numerical token improvement is claimed.

Before: generic curation had no product-specific execution boundary. After: a compact product-knowledge section links QA, preserves approved sources and immutable run history, and prohibits turning defects into intended behavior. Existing triggers and responsibilities remain; the skill receives a patch version. Catalog changes are limited to the new QA profile. Replay checks preserve an expected/observed mismatch and reject stale or unapproved passes; results are recorded in the linked plan. Remaining risk: source interpretation and actual execution still depend on the host agent and target capabilities.

## Migration, validation and rollback

The [migration contract](../MIGRATIONS.md) preserves filled application inventories and audits. Guides/templates alone enter the clean framework. Selected product pages are search-only; exact QA runs are loaded only when needed. Structural checks and live replay evidence are recorded in the implementation plan, with unavailable platforms/hardware explicitly excluded. Stop invoking QA to roll back operationally; retain application knowledge and prior evidence. [V0.19.0](../framework-releases/V0.19.0.md) remains in preparation.
