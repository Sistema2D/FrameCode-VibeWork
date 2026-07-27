---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# FCVW operational index

This directory is the governance layer installed in a project. `AGENTS.md` remains at repository root as the entrypoint.

## Start here

| Need | Load first | Load next |
|---|---|---|
| Orient a session | `CONTEXT_MAP.md` | domain document |
| Resolve file-reading triggers | `CONTEXT_MAP.md` event table | active plan `context_files` |
| Instantiate a new project | `INSTANTIATION.md` | `BRIEFING.md`, `MANIFEST.md` |
| Adopt in an existing project | `RETROACTIVE_INSTANTIATION.md` | `MIGRATIONS.md` |
| Plan a change | `PLANNING.md` | `governance/TEMPLATE_PLAN.md` |
| Protect existing behavior | `REGRESSION_GUARDS.md` | `TESTS.md`, `GOVERNANCE_GATES.md` |
| Debug a failure | `TROUBLESHOOTING.md` | relevant failure record |
| Release | `skills/release-checklist/SKILL.md` | `VERSIONING.md`, `RELEASE.md` |
| Validate governance | `skills/governance-validator/SKILL.md` | `SCHEMAS.md` |
| Curate memory | `MEMORY.md` | `wiki/schema.md` |
| Define automation | `AUTOMATION.md` | hook, watcher, daemon, or gate contract |

## Document classes

### Framework policies — replace on compatible upgrades

`AI.md`, `APPLICATION_DOCUMENTATION.md`, `ARCHITECTURAL_DECISIONS.md`, `AUDIT.md`, `AUTOMATION.md`, `CONTEXT_MAP.md`, `DAEMONS.md`, `GOVERNANCE_GATES.md`, `HOOKS.md`, `INSTANTIATION.md`, `MEMORY.md`, `MIGRATIONS.md`, `OWNERSHIP.md`, `PLANNING.md`, this `README.md`, `REFACTORING.md`, `REGRESSION_GUARDS.md`, `RELEASE.md`, `RETROACTIVE_INSTANTIATION.md`, `SCHEMAS.md`, `TESTS.md`, `TOKEN_BUDGET.md`, `TROUBLESHOOTING.md`, `VERSIONING.md`, and `WATCHERS.md`.

### Project profiles — instantiate and preserve

`APP_RULES.md`, `BRIEFING.md`, `DATA.md`, `DESIGN.md`, `ENVIRONMENT.md`, `MANIFEST.md`, `PERFORMANCE.md`, `SCOPE.md`, `SECURITY.md`, `STACK.md`, and `WORKFLOW.md`.

Some profiles contain generic guidance plus clearly marked project sections. Framework upgrades must never overwrite populated project values.

### Records — preserve

`Plans/`, `audits/`, `briefings/`, `changelogs/`, `decisions/`, `troubleshooting/`, and project-created pages under `wiki/`.

### Generated summaries — regenerate

`DOCUMENT_GRAPH.md`, `FILESYSTEM.md`, `wiki/index.md`, `wiki/log.md`, and `wiki/metrics.md`.

## Framework versus application releases

- FCVW releases: `framework-releases/Vx.y.z.md`.
- Application releases: `changelogs/Vx.y.z.md`.
- Installed FCVW baseline: `FRAMEWORK_LOCK.md`.
- Application version: project `MANIFEST.md` or the application's runtime version source.

The namespaces must not be mixed.

## Clean baseline rule

Empty record directories keep a README only. Application examples, histories, and production-derived comparison fixtures remain outside the framework project and its clean distribution.

## New operational navigation

| Need | Load first | Validation |
|---|---|---|
| Review application-specific rules | [`APP_RULES.md`](APP_RULES.md) | unique rule IDs and project-profile ownership |
| Select the next plan | [`Plans/in_progress/QUEUE.md`](Plans/in_progress/QUEUE.md), then [`Plans/pending/QUEUE.md`](Plans/pending/QUEUE.md) | queue/state consistency |
| Browse all governed Markdown | [`DOCUMENT_GRAPH.md`](DOCUMENT_GRAPH.md) | incoming links and entrypoint reachability |
| Build optional lexical context | [`AI.md`](AI.md) | mandatory routes remain authoritative |

`DOCUMENT_GRAPH.md` is a generated navigation surface for Obsidian and portable Markdown readers. It does not become a source of policy merely because it links one.
