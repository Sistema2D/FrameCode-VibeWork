---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# QA execution evidence

Store application QA runs here using [TEMPLATE_QA_RUN.md](../templates/TEMPLATE_QA_RUN.md). Each run is an application-owned wiki audit with unique ID, app revision, environment, runtime/toolchain or hardware identity, roles, time, selected behavior hashes and case results. Reports are exact-only context. Screenshots, traces and large logs remain external or in the project's evidence location; remove secrets and personal data before retaining or sharing.

Link runs from their [product surface pages](../product/README.md). Preserve prior runs; a new run supersedes current evidence without erasing failures. Never turn not-run or blocked cases into passes. No application execution records are shipped in the clean framework.
