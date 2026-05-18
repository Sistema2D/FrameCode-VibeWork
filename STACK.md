# Tech Stack

> This is a template. Replace the fields between `<...>` with the actual information of the project.

## Application

- Name: `<project name>`
- Current version: `V0.3.1`
- Type: `<web / desktop / mobile / CLI / API / library / hybrid>`
- Target platform: `<Windows / Linux / macOS / Web / cross-platform>`
- Objective: `<one-line summary>`

## Frontend

`<Remove if there is no UI.>`

- Language: `<technology>`
- Framework / UI toolkit: `<framework or API>`
- Build: `<build tool>`
- Compiler / bundler: `<compiler or bundler>`
- Main libraries: `<list>`

## Backend

`<Remove if there is no separate backend.>`

- Language: `<technology>`
- HTTP Framework: `<framework>`
- Local port: `<address and port>`
- Local security: `<token, authentication, or CORS>`
- Main modules: `<list>`

## Local or Remote AI

`<Remove if there is no AI.>`

- Runtime / model server: `<Ollama / OpenAI / other>`
- API: `<endpoint>`
- Used resources: `<list, chat, embeddings, etc.>`
- Continuous learning: `<describe or "not applicable">`

## Vault / Knowledge Base

`<Remove if there is no vault or RAG.>`

- Local directory: `<path>`
- Format: `<Markdown / JSON / other>`
- Main structure: `<schema.md, index.md, log.md, raw/, notes/, etc.>`

## Build and Execution

- Build script: `<command or file>`
- Execution script: `<command or file>`
- Main output: `<artifact path>`

## Build Matrix

`<Remove if the project is not cross-platform.>`

| Platform / OS | Compiler / Runtime | Flags or Variants | Status |
|---|---|---|---|
| `<Windows x64>` | `<MSVC / MinGW / clang>` | `<Release / Debug>` | `<supported>` |
| `<Linux x64>` | `<GCC / clang>` | `<Release>` | `<supported>` |

## Persistence and Logs

- User data: `<path and format>`
- Settings: `<path and format>`
- Logs: `<folder or mechanism>`
- Writing strategy: `<atomic / backup / direct>`
- Data ignored by Git: `<logs, builds, vault, private data>`

## Document Governance

- Completed official documents: Markdown files at the root of the application.
- Reusable empty templates: `governance/` folder.
- Technical memory of governance: `wiki/` folder.
- Formal records: `Plans/`, `changelogs/`, `troubleshooting/`.
- Instantiation and renaming: `INSTANTIATION.md`.
- Versioning exclusions: `.gitignore`.
- Mandatory changelog: every change in a versioned file must be registered in `changelogs/Vx.y.z.md`.
