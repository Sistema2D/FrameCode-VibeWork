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
| Installed version | `V0.16.0` |
| Release state | `ready` |
| Source | `https://github.com/Sistema2D/FrameCode-VibeWork` |
| License | `Apache-2.0` |
| Installed profile | `clean-template` |
| Installed modules | `core, plans, compact-plans, regression-guards, records, wiki, typed-knowledge, framework-feedback, skills, declarative-automation, contained-release-layout, fragmented-queues, role-manifest, assisted-upgrade, optional-validator` |
| Last migration | `V0.15.0 -> V0.16.0` |

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

The V0.16.0 candidate stays `in_preparation` in [`framework-releases/V0.16.0.md`](framework-releases/V0.16.0.md). Per `VERSIONING.md`, this lock only advances to V0.16.0 at the post-publication evidence commit; until then it records the last published version.
