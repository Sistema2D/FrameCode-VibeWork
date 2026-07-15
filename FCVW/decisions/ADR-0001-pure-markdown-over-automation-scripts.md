---
schema: "fcvw/adr@1"
id: "ADR-0001"
status: "accepted"
date: "2026-07-15"
artifact_role: "record"
record_scope: "framework"
---

# ADR-0001: Markdown-first baseline

## Context

FCVW must remain usable in repositories that have no specific language runtime, package manager, CI provider, or agent vendor. Requiring executable automation for basic governance would make the framework harder to inspect, adopt, and migrate.

## Decision

Normative governance is stored in portable Markdown and version control. Optional tooling may validate or accelerate the contracts, but the documents remain readable and executable as human procedures when tooling is unavailable.

## Consequences

- The clean package has no required runtime dependency.
- Validation claims must identify whether they came from manual review or optional tooling.
- Application-specific scripts may be added downstream without becoming framework requirements.
- Rules that cannot be evaluated manually need an explicit external-runtime profile.

## Supersession

A replacement ADR must preserve a runtime-independent baseline or document a breaking migration.
