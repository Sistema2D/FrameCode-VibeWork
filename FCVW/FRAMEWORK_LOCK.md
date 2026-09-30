---
schema: "fcvw/framework-lock@1"
artifact_role: "framework_lock"
owner: "framework"
upgrade_strategy: "replace_with_migration"
---

# Framework lock

| Field | Value |
|---|---|
| Framework | `FrameCode VibeWork` |
| Installed version | `V0.21.0` |
| Release state | `published` |
| Source | `https://github.com/Sistema2D/FrameCode-VibeWork` |
| License | `Apache-2.0` |
| Installed profile | `clean-template` |
| Installed modules | `core, plans, compact-plans, derived-queue, regression-guards, records, record-reachability, project-profile, wiki, typed-knowledge, framework-feedback, skills, declarative-automation, contained-release-layout, role-manifest, assisted-upgrade, optional-validator, verified-context-routing, section-ranges, section-anchors, complete-chunk-selection, product-QA, local-validation, optional-decision-trace` |
| Last migration | `V0.20.0 -> V0.21.0` |

## Schema baselines

| Artifact | Schema |
|---|---|
| Plan | `fcvw/plan@2` (`fcvw/plan@1` legacy-readable) |
| Compact plan | `fcvw/plan-compact@1` |
| Application changelog | `fcvw/changelog@1` |
| Framework release | `fcvw/framework-release@1` |
| Project profile | `fcvw/project@1` |
| Wiki page | `fcvw/wiki@1` |
| Regression record | `fcvw/regression@1` |
| Architecture decision | `fcvw/adr@1` |
| Skill | `fcvw/skill@1` |
| Automation contract | `fcvw/automation@1` |
| Application rules | `fcvw/app-rules@1` |
| Language review | `fcvw/language-review@1` |
| Formal audit | `fcvw/audit@1` |
| Troubleshooting | `fcvw/troubleshooting@1` |
| Legacy validation baseline | `fcvw/legacy-baseline@1` |

Downstream projects update this file only through a governed framework migration. Application releases never change `Installed version`.

Published baseline: [V0.21.0](https://github.com/Sistema2D/FrameCode-VibeWork/blob/main/FCVW/framework-releases/V0.21.0.md). The prior version is [V0.20.0](https://github.com/Sistema2D/FrameCode-VibeWork/blob/main/FCVW/framework-releases/V0.20.0.md); the new record contains verified GitHub publication evidence.
