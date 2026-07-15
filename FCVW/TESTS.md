---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Testing and validation

## Purpose

Define risk-proportional evidence for new behavior, protected existing behavior, failure handling, and rollback. Each plan selects the applicable checks; this policy does not invent application-specific commands.

## General rules

- Validate both the requested outcome and the protected behaviors listed in the plan's Regression impact section.
- Prefer reproducible automated checks for stable contracts; record manual evidence when automation is unavailable or unsuitable.
- A test name or suite size is not evidence by itself: record command or procedure, result, protected contract, and limitation.
- Use representative synthetic or sanitized fixtures instead of private production data.
- A reproducible failure receives a troubleshooting record when diagnosis or recurrence value justifies it.
- Published changes carry concise validation evidence in their plan and changelog or framework release record.
- Missing tooling does not silently lower risk; it becomes a limitation, residual risk, and completion decision.

## Minimum regression evidence by risk

| Risk | Minimum evidence |
|---|---|
| R1 | Focused review or replay of the changed contract, structural checks when applicable, and changelog/release evidence |
| R2 | Direct component or document-contract test plus one relevant existing-behavior replay |
| R3 | Full build or equivalent integrity check, primary workflow, alternate/error workflow, and related-boundary regression |
| R4 | R3 plus dependent workflows, compatibility or recovery evidence, documented rollback, and explicit residual-risk review |
| R5 | Expanded regression across affected boundaries, security/data review when applicable, rollback rehearsal, and explicit human approval before completion |

Authentication, authorization, persistent data, public APIs or file formats, agent instructions, memory, filesystem, automation, migrations, destructive behavior, and releases are not R1 by default. An R1 classification for one of these surfaces requires a concrete blast-radius and reversibility rationale.

## Evidence matrix by change surface

| Surface | Required considerations |
|---|---|
| Documentation/governance | links, schema, ownership, instruction conflicts, lifecycle, generated summaries, negative structural fixture |
| UI/accessibility | supported viewport/state matrix, keyboard/focus, contrast, error/empty/loading states, primary and adjacent navigation |
| Frontend/client | focused tests, build, affected journey, navigation/state persistence, error and offline/dependency behavior |
| Backend/API | syntax/compile, contract tests, valid/invalid input, authorization, dependency failure, idempotency where required |
| Data/filesystem | CRUD or equivalent lifecycle, old-data compatibility, migration idempotency, reconciliation, backup and recovery |
| AI/agent/RAG | allowed and denied actions, untrusted-content handling, context/source traceability, unavailable model, memory boundaries |
| Security/privacy | authentication, authorization denial, secrets/logs, path boundaries, destructive confirmation, misuse cases |
| Refactoring | characterization baseline, before/after behavior, public contract, focused and dependent regressions |
| Performance/operations | measured baseline, representative load, startup/deploy/recovery, resource and failure thresholds |
| Release/build | clean artifact, version surfaces, primary smoke, migration/rollback, changelog, known gaps |

## Regression test design

1. Name the protected behavior and its authoritative contract.
2. Choose the narrowest check that can detect the unwanted change.
3. Capture a baseline before modification when the result is comparative.
4. Include negative, invalid, denied, empty, or recovery cases when relevant.
5. Confirm a new guardrail would fail on the known regressed state when practical.
6. Run focused checks first and broaden by risk and dependency radius.
7. Record nondeterminism, environment differences, skipped paths, and residual uncertainty.

## AI and agent boundary replay

Changes to `AGENTS.md`, AI policies, skills, prompts, memory, retrieval, or automation must replay representative allowed, denied, ambiguous, unavailable-runtime, and prompt-injection cases. Mature projects may automate evaluations in their chosen runtime, but FCVW does not require a particular vendor or test package.

## Visual evidence

Visual changes identify supported viewports and states before testing. Compare relevant before/after states; verify keyboard focus, zoom or scaling when applicable, long content, empty/error/loading states, disabled and destructive actions. Store only non-sensitive captures in project-owned paths.

## Data and rollback evidence

Schema, format, migration, retention, import/export, or destructive changes use representative prior-version data. Validate reconciliation, idempotency, backup, recovery, and rollback—or record why rollback is irreversible and who approved that risk.

## Completion checklist

- [ ] Requested behavior has evidence.
- [ ] Regression impact identifies protected behavior and source contracts.
- [ ] Applicable focused and dependent checks have final results.
- [ ] Invalid, denied, error, and recovery paths were considered.
- [ ] Compatibility and rollback were validated when applicable.
- [ ] Security, data, AI, visual, or operational gates ran when triggered.
- [ ] No pending regression result remains.
- [ ] Limitations, residual risks, and known gaps are explicit.
- [ ] Plan and changelog or framework release record contain reproducible evidence.

Use `governance/TEMPLATE_PLAN.md` to record change-specific validation and `REGRESSION_GUARDS.md` for blocking rules.
