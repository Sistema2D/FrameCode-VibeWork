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
| Installed version | `V0.19.0` |
| Release state | `ready` |
| Source | `https://github.com/Sistema2D/FrameCode-VibeWork` |
| License | `Apache-2.0` |
| Installed profile | `clean-template` |
| Installed modules | `core, plans, compact-plans, regression-guards, records, wiki, typed-knowledge, framework-feedback, skills, declarative-automation, contained-release-layout, fragmented-queues, role-manifest, assisted-upgrade, optional-validator, optional-shadow-routing, verified-context-routing, complete-chunk-selection, product-QA, local-validation, loop-evaluation, guarded-adaptive-assist, optional-decision-trace` |
| Last migration | `V0.18.0 -> V0.19.0` |

## Schema baselines

| Artifact | Schema |
|---|---|
| Plan | `fcvw/plan@2` (`fcvw/plan@1` legacy-readable) |
| Application changelog | `fcvw/changelog@1` |
| Framework release | `fcvw/framework-release@1` |
| Project manifest | `fcvw/project-manifest@1` |
| Wiki page | `fcvw/wiki@1` |
| Regression record | `fcvw/regression@1` |
| Skill | `fcvw/skill@1` |
| Automation contract | `fcvw/automation@1` |
| Plan queue | `fcvw/plan-queue@1` |
| Application rules | `fcvw/app-rules@1` |
| Document graph | `fcvw/document-graph@1` |
| Language review | `fcvw/language-review@1` |
| Formal audit | `fcvw/audit@1` |
| Troubleshooting | `fcvw/troubleshooting@1` |
| Knowledge graph | `fcvw/knowledge-graph@1` |

Downstream projects update this file only through a governed framework migration. Application releases never change `Installed version`.

Ready candidate: [V0.19.0](framework-releases/V0.19.0.md). The previous published baseline is [V0.18.0](framework-releases/V0.18.0.md). Publication evidence follows in a separate commit after GitHub confirms the release.
