# Governance templates

Reusable empty models. Templates keep placeholders on purpose and are replaced on schema-compatible framework upgrades. Copy a template into its record location; never fill project data into the template itself.

| Template | Use |
|---|---|
| [TEMPLATE_PLAN.md](TEMPLATE_PLAN.md) | standard and expanded change plan (`fcvw/plan@2`) |
| [TEMPLATE_PLAN_COMPACT.md](TEMPLATE_PLAN_COMPACT.md) | compact P4/P5-R1 plan |
| [TEMPLATE_RELEASE.md](TEMPLATE_RELEASE.md) | application release changelog |
| [TEMPLATE_FRAMEWORK_RELEASE.md](TEMPLATE_FRAMEWORK_RELEASE.md) | framework release record |
| [TEMPLATE_ADR.md](TEMPLATE_ADR.md) | architecture decision record |
| [TEMPLATE_TROUBLESHOOTING.md](TEMPLATE_TROUBLESHOOTING.md) | failure diagnosis record |
| [TEMPLATE_AUDIT.md](TEMPLATE_AUDIT.md) | formal audit |
| [TEMPLATE_NOTE.md](TEMPLATE_NOTE.md) | every wiki note type |
| [TEMPLATE_REGRESSION.md](TEMPLATE_REGRESSION.md) | confirmed reusable regression |
| [TEMPLATE_REFACTORING.md](TEMPLATE_REFACTORING.md) | refactoring plan and every lifecycle stage, hygiene and monolith gates |
| [TEMPLATE_APP_DOC.md](TEMPLATE_APP_DOC.md) | application documentation: docs README, module, flow, API, data schema, AI feature |
| [TEMPLATE_SKILL_CHANGE.md](TEMPLATE_SKILL_CHANGE.md) | new skill or agent proposal and self-improvement report |
| [TEMPLATE_AUTOMATION_CONTRACT.md](TEMPLATE_AUTOMATION_CONTRACT.md) | hook, watcher, daemon or governance gate contract |
| [TEMPLATE_ENV.md](TEMPLATE_ENV.md) | environment description |
| [TEMPLATE_BRIEFING.md](TEMPLATE_BRIEFING.md) | project briefing |
| [TEMPLATE_VISUAL_DIFF.md](TEMPLATE_VISUAL_DIFF.md) | visual before/after evidence |
| [TEMPLATE_MIGRATION_RUNNER.md](TEMPLATE_MIGRATION_RUNNER.md) | data migration runner |
| [TEMPLATE_LEGACY_BASELINE.md](TEMPLATE_LEGACY_BASELINE.md) | incremental validation baseline |
| [TEMPLATE_LANGUAGE_REVIEW.md](TEMPLATE_LANGUAGE_REVIEW.md) | language-specific release review |

## Framework automation record

- [Local validation contract](LOCAL_VALIDATION_CONTRACT.md): the explicit local runner that replaced hosted CI (retired contract kept in [git history](https://github.com/Sistema2D/FrameCode-VibeWork/blob/5c3ed95a27d02ce1939bb937af7ab11dfee9c71d/FCVW/governance/CI_CONTRACT.md)).
