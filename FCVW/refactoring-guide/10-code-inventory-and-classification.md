# 10 — Code Inventory and Classification

This file defines how to inventory an application before starting refactoring in large codebases, especially when there are thousands of files, multiple folders, legacy modules, or poorly documented dependencies.

## Objective

Prevent the team from refactoring "in the dark". No structural refactoring should begin without a minimal overview of:

- existing modules, packages, services, components, libraries, and routes;
- files critical for execution, build, deploy, authentication, authorization, payments, data, or integrations;
- internal and external dependencies;
- areas with low test coverage;
- areas with high change frequency;
- areas without a clear technical owner.

## When to use

Mandatory use before any refactoring that involves:

- more than one module, folder, or package;
- moving files, classes, services, components, or public functions;
- changing a public signature;
- changing shared code;
- changes to infrastructure, build, configuration, routes, databases, or APIs;
- code without sufficient automated tests.

## Governance rule

> Refactoring a large codebase requires a minimal inventory before the first change. Without an inventory, refactoring must be limited to local scope, reversible, and low-impact.

## Mandatory minimal inventory

| Item | What to map | Expected evidence |
|---|---|---|
| Physical structure | Folders, files, modules, packages, and subprojects. | Summarized tree or inventory report. |
| Entrypoints | Initialization files, routes, commands, jobs, workers, scripts, and main pages. | List with path and purpose. |
| Functional domains | Business areas or system capabilities. | Map module → domain. |
| Internal dependencies | Who calls whom, imports, extends, delegates, events, and contracts. | Graph, table, or report. |
| External dependencies | Libraries, SDKs, APIs, services, queues, databases, and external files. | Versioned list. |
| Existing tests | Unit, integration, contract, e2e, smoke, and manual tests. | Test paths and estimated coverage. |
| Critical points | Authentication, authorization, data, payments, integration, security, compliance, and deploy. | Criticality tags. |
| Technical owners | Person/team responsible for review and acceptance. | Defined owner per module. |
| Legacy code | Areas without tests, without an owner, with low readability, or obsolete dependencies. | `LEGACY` tag. |
| Dead code | Files, methods, classes, or routes with no confirmed usage. | `CANDIDATE_FOR_REMOVAL` tag, never remove without validation. |

## Classification by module

Each module must receive the following classification:

| Field | Options | Criteria |
|---|---|---|
| Functional criticality | Low / Medium / High / Critical | Impact on users, operations, or revenue. |
| Exposure | Internal / Public / External | If it is used by other modules, clients, or integrations. |
| Test coverage | High / Medium / Low / Absent | Protection against regression. |
| Coupling | Low / Medium / High | Quantity and strength of dependencies. |
| Volatility | Low / Medium / High | Change frequency in recent cycles. |
| Complexity | Low / Medium / High | Size, branching, duplication, and reading difficulty. |
| Technical owner | Name/team | Responsible for approval. |
| Change window | Free / Controlled / Restricted | When it can be changed or deployed. |

## Inventory levels

### Level 1 — Quick inventory

Applicable to local and low-risk refactorings.

Mandatory to map:

- modified file(s);
- existing tests;
- direct calls;
- expected behavior before/after;
- rollback strategy via `git revert`.

### Level 2 — Module inventory

Applicable to medium refactorings.

Mandatory to map:

- complete module;
- inbound and outbound dependencies;
- owner;
- characterization tests;
- public contracts;
- build/deploy risks.

### Level 3 — Systemic inventory

Applicable to broad refactorings.

Mandatory to map:

- dependencies between modules;
- critical business flows;
- persisted data;
- external integrations;
- jobs/queues/events;
- incremental plan;
- rollback plan;
- technical and functional approval.

## Useful indicators

To prioritize areas, collect when possible:

- number of files per module;
- number of lines per module;
- cyclomatic complexity;
- duplication;
- test coverage;
- change frequency via `git log`;
- number of recent bugs per module;
- build and test time;
- obsolete dependencies;
- number of imports/cross-calls.

## Rules for very large codebases

1. Do not start with critical areas without tests.
2. Do not combine refactoring with a feature or functional fix.
3. Do not move many files in a single PR without justification and a validation plan.
4. Do not remove apparently dead code without confirmation through static search, logs, metrics, or owner validation.
5. Do not change a public signature without a map of consumers.
6. Do not change directory structure used by build, import aliases, bundlers, automatic routes, or framework conventions without a specific test.
7. Do not rely solely on textual search; use dependency analysis when the language/framework allows.

## Mandatory actions

Before refactoring:

- fill out the module inventory template;
- classify initial risk;
- define maximum scope of the first PR;
- identify minimum tests;
- register owner and approvers.

During refactoring:

- keep commits small;
- update the inventory if unmapped dependencies emerge;
- interrupt if the scope grows without approval.

After refactoring:

- update architecture documentation;
- record changes in dependencies;
- record validation evidence;
- archive the decision in the PR or ADR.

## Applicable template

Use [`../governance/TEMPLATE_REFACTORING_MODULE_INVENTORY.md`](../governance/TEMPLATE_REFACTORING_MODULE_INVENTORY.md).
