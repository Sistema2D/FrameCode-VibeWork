---
schema: "fcvw/adr@1"
id: "ADR-0004"
status: "accepted"
date: "2026-07-27"
artifact_role: "record"
owner: "framework"
upgrade_strategy: "preserve"
record_scope: "framework"
retrieval_scope: "routed"
language: "en-US"
---

# ADR-0004: Language-specific clean release artifacts

## Context

Open issues [#43](https://github.com/Sistema2D/FrameCode-VibeWork/issues/43) and [#45](https://github.com/Sistema2D/FrameCode-VibeWork/issues/45) require complete Brazilian Portuguese, United States English, Spanish, and German framework variants, clean release assets, and standardized GitHub release records for both applications and FCVW itself.

The framework source and every installed copy must remain a conventional single tree. Multilingual support is a release-production concern: it measures whether the release offers four equivalent, reviewed, clean templates. It is not an automatic runtime mode, a repository-layout migration, or a mechanism that asks an installed framework to select or synchronize languages.

## Alternatives considered

1. Migrate the repository to four top-level language trees.
2. Put all languages in every installed template and select one automatically.
3. Keep one conventional source tree and prepare four reviewed, self-contained clean release variants outside it.
4. Publish only translated README files.

## Decision

Adopt option 3 as the release-production model.

- The governed source repository remains a single conventional tree with root `AGENTS.md`, `README.md`, `FCVW/`, and `tools/`.
- The release pipeline prepares independent variants named `pt-BR`, `en-US`, `es`, and `de` in an external or disposable staging area.
- Each finished variant must contain the same functional paths, schemas, machine identifiers, and executable behavior.
- Human prose is adapted; schemas, IDs, enums, commands, paths, code, and checksums remain stable.
- A language variant is releasable only after structural parity, internal-link, language-review, clean-template, and package-root validation.
- Each published folder or archive is already a conventional standalone FCVW tree; it neither contains nor links to the other language variants.
- The user chooses a language by downloading exactly one folder or asset. FCVW performs no automatic language detection, selection, fallback, or synchronization during instantiation or use.
- Language parity and completeness are release metrics only. They do not alter the behavior or filesystem of a downloaded template.
- GitHub-generated source archives are not described as clean templates.

## Current release state

The current single-tree source remains authoritative. The repository must not claim issue #45 complete or publish the language-specific assets until all four external release variants pass the gates above. No source-layout migration is planned or required. This prevents placeholder translations or mechanically copied English prose from being represented as adapted content.

## Consequences

- Language-specific releases have deterministic names and comparable contents.
- Translation work cannot silently change schemas or code.
- Publication remains blocked until native or otherwise accountable language-review evidence exists.
- An installed framework remains monolingual and does not carry unused language copies.
- Release staging can be rebuilt or discarded without changing the source layout.

## Conditions for review

- A translation management system provides stronger parity guarantees.
- GitHub or package consumers require a different root contract.
- Maintaining the canonical content baseline becomes a measurable bottleneck.

## Relationships

- Active implementation plan: [P2-R5 open-issues update](../Plans/in_progress/P2-R5-2026-07-27-open-issues-42-48-and-document-graph.md).
- Governing policies: [Filesystem](../FILESYSTEM.md), [Release](../RELEASE.md), [Versioning](../VERSIONING.md), and [Migrations](../MIGRATIONS.md).
