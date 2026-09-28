---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# FCVW operational index

This directory is the governance layer installed in a project. V0.19.0 is the current published framework release. `AGENTS.md` remains at repository root as the only framework file outside this directory in V0.15.0-or-later release assets.

## Installation and removal boundary

- A release payload exposes `AGENTS.md`, `FCVW/`, and the optional provider bridges `.cursorrules` and `.windsurfrules` at the template root. The bridges stay at the root because that is the only place their editors read them.
- Tools, legal notices, provider adapters, policies, templates, and framework records are contained by `FCVW/`.
- Run installed tools from `FCVW/tools/`; the framework source checkout keeps its development tools at root `tools/`.
- To remove the framework from an application, back up project-owned records if needed, delete `FCVW/`, then review and optionally delete `AGENTS.md`. No application path is part of that deletion boundary.
- Do not use this shortcut on a pre-V0.15.0 installation until completing the filesystem migration in `MIGRATIONS.md`.

## Start here

| Need | Load first | Load next |
|---|---|---|
| Orient a session | `CONTEXT_MAP.md` | domain document |
| Resolve file-reading triggers | `CONTEXT_MAP.md` event table | active plan `context_files` |
| Instantiate a new project | `INSTANTIATION.md` | the [briefing questionnaire](skills/project-instantiation/BRIEFING.md), `PROJECT.md` (identity and scope) |
| Adopt in an existing project | `INSTANTIATION.md` (retroactive mode) | `MIGRATIONS.md` |
| Plan a change | `PLANNING.md` | `governance/TEMPLATE_PLAN.md` |
| Protect existing behavior | `REGRESSION_GUARDS.md` | `TESTS.md`, `AUTOMATION.md` gates |
| Debug a failure | `TROUBLESHOOTING.md` | relevant failure record |
| Release | `skills/release-checklist/SKILL.md` | `RELEASE.md` |
| Validate governance | `skills/governance-validator/SKILL.md` | `SCHEMAS.md` |
| Curate memory | `wiki/README.md` | `skills/wiki-curator/SKILL.md` |
| Define automation | `AUTOMATION.md` | hook, watcher, daemon, or gate contract |
| Upgrade the framework | `OWNERSHIP.md` | `tools/upgrade_fcvw.py --root . --release <target>` |

## Document classes

### Framework policies — replace on compatible upgrades

[AI.md](AI.md), [APPLICATION_DOCUMENTATION.md](APPLICATION_DOCUMENTATION.md), [ARCHITECTURAL_DECISIONS.md](ARCHITECTURAL_DECISIONS.md), [AUDIT.md](AUDIT.md), [AUTOMATION.md](AUTOMATION.md), [CONTEXT_MAP.md](CONTEXT_MAP.md), [INSTANTIATION.md](INSTANTIATION.md), [MIGRATIONS.md](MIGRATIONS.md), [OWNERSHIP.md](OWNERSHIP.md), [PLANNING.md](PLANNING.md), this `README.md`, [REFACTORING.md](REFACTORING.md), [REFACTORING_GUIDE.md](REFACTORING_GUIDE.md), [REGRESSION_GUARDS.md](REGRESSION_GUARDS.md), [RELEASE.md](RELEASE.md), [SCHEMAS.md](SCHEMAS.md), [TESTS.md](TESTS.md), and [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

### Project profiles — instantiate and preserve

[PROJECT.md](PROJECT.md) (identity and scope, stack, environment, design, performance, workflows), [SECURITY.md](SECURITY.md), [DATA.md](DATA.md), and [APP_RULES.md](APP_RULES.md). The Phase 0 [briefing questionnaire](skills/project-instantiation/BRIEFING.md) is framework guidance used by the instantiation skill.

Some profiles contain generic guidance plus clearly marked project sections. Framework upgrades must never overwrite populated project values.

### Records — preserve

[Plans](Plans/README.md), `audits/`, `briefings/`, `changelogs/`, `decisions/`, `troubleshooting/`, and project notes in the [wiki](wiki/README.md). A record is reachable through its canonical directory ([ADR-0011](decisions/ADR-0011-record-reachability.md)); each record still links to its authoritative source.

### Catalogs

[Skills](skills/README.md), [governance templates](governance/README.md), [plans](Plans/README.md) and the [wiki contract](wiki/README.md), whose curated [index](wiki/index.md) is project-owned.

### Generated views — never versioned

The document graph catalog, the plan queue view, context indexes and knowledge graphs are written to `.fcvw-cache/` on demand.

`ROLE_MANIFEST.json` is not regenerated: it is the installation baseline shipped with each release and is replaced only by the upgrade tool after a successful apply.

## Framework versus application releases

Current published framework: [V0.19.0](framework-releases/V0.19.0.md). Previous version: [V0.18.0](framework-releases/V0.18.0.md).

- FCVW releases: `framework-releases/Vx.y.z.md`.
- Application releases: `changelogs/Vx.y.z.md`.
- Installed FCVW baseline: `FRAMEWORK_LOCK.md`.
- Application version: project `PROJECT.md` (identity and scope) or the application's runtime version source.

The namespaces must not be mixed.

## Clean baseline rule

Empty record directories keep a README only. Application examples, histories, and production-derived comparison fixtures remain outside the framework project and its clean distribution.

## New operational navigation

| Need | Load first | Validation |
|---|---|---|
| Review application-specific rules | [`APP_RULES.md`](APP_RULES.md) | unique rule IDs and project-profile ownership |
| Select the next plan | [Plans](Plans/README.md) and `tools/plan_queue_fcvw.py --recommend` | derived queue findings |
| Browse all governed Markdown | Obsidian graph and backlinks, or `tools/document_graph_fcvw.py --write` into `.fcvw-cache/` | incoming links and entrypoint reachability |
| Build optional lexical context | [`AI.md`](AI.md) | mandatory routes remain authoritative |

A generated catalog is a disposable view, never a source of policy. Graph reachability proves navigation, not that a host activated a skill or read a rule during a real task.

## V0.18.0 retrieval quality

See [usage and limits](AI.md), [benchmark and installed verification](TESTS.md) and the [release record](framework-releases/V0.18.0.md). Required routes are explained, optional chunks can be budgeted without truncation, and exact-only history no longer matches incidental substrings. Issues [55](https://github.com/Sistema2D/FrameCode-VibeWork/issues/55), [56](https://github.com/Sistema2D/FrameCode-VibeWork/issues/56) and [57](https://github.com/Sistema2D/FrameCode-VibeWork/issues/57) are closed with empirical promotion criteria unmet. The experimental adaptive and loop layer left the core in V0.20.0; see [ADR-0010](decisions/ADR-0010-core-reduction.md).

## Local validation

Current source validation uses the explicitly invoked [local checks](TESTS.md) and [Scenario 2 contract](governance/LOCAL_VALIDATION_CONTRACT.md). Hosted Actions are retired. Evidence reports only actually tested runtimes and operating systems; no payment or hosted account is required.

## Product behavior and QA

[Product wiki](skills/QA/PRODUCT_WIKI.md) centralizes sourced screen/control behavior and links observed execution evidence. [QA](skills/QA/SKILL.md) maps the application on first use, then performs selective functional tests and maintenance. It is invoked on demand; no background agent or new runtime dependency is activated.

