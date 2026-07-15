---
schema: "fcvw/project-stack@1"
artifact_role: "project_profile"
owner: "project"
upgrade_strategy: "preserve"
instantiation_status: "pending"
---

# Technology stack

## Application

| Concern | Selection | Version/source | Notes |
|---|---|---|---|
| Application type | `<web, desktop, mobile, service, library>` | | |
| Primary language | `<language>` | | |
| Runtime | `<runtime>` | | |
| UI | `<framework or not_applicable>` | | |
| Backend | `<framework or not_applicable>` | | |
| Persistence | `<database/files or not_applicable>` | | |
| Deployment | `<target>` | | |

## Canonical version sources

- Application version: `<single source path>`.
- Framework version: `FRAMEWORK_LOCK.md`.
- Dependency versions: lockfile or platform-native equivalent.

Do not copy the application version into multiple documents unless it is derived automatically.

## Required commands

| Purpose | Command | Environment |
|---|---|---|
| Install | `<command>` | |
| Type/static check | `<command>` | |
| Lint | `<command>` | |
| Unit tests | `<command>` | |
| Integration tests | `<command>` | |
| Build | `<command>` | |
| Start | `<command>` | |

## Boundaries

- Supported operating systems:
- Supported browsers/clients:
- Required external services:
- Unsupported or intentionally excluded technologies:

## Governance layer

- Framework: FrameCode VibeWork `V0.13.0`.
- Plans: `FCVW/Plans/`.
- Application releases: `FCVW/changelogs/`.
- Framework baseline: `FCVW/FRAMEWORK_LOCK.md`.
- Optional validator: `tools/validate_fcvw.py`.
