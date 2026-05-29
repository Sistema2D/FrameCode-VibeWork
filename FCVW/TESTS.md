# Testing and Validation

Methodological document to define the rules of testing, validation, and regression of the application.

This file complements `PLANNING.md`, `TROUBLESHOOTING.md`, `VERSIONING.md`, `DESIGN.md`, `STACK.md`, and `WORKFLOW.md`. It must be consulted whenever a functional, visual, structural, documental, build, data, security, or AI change is planned, implemented, or published.

## Objective

Ensure that each change is validated proportionally to its risk, priority, technical impact, and user impact.

This document does not replace individual plans in `Plans/`. Each plan must bring its own testing plan, but should use this file as a reference.

## General Principles

- Every change must have validation compatible with its risk.
- Manual validation must be recorded when automated testing does not exist.
- Reproducible failures must generate or update a record in `troubleshooting/`.
- Published changes must have testing evidence in the plan and in the changelog.
- Tests must cover expected behavior, invalid behavior, and probable regressions.
- No test should rely on real private data when it can use dummy data.
- Every testing limitation must be explicitly declared in the plan and in the changelog.

## Test Classification by Change Type

| Change Type | Minimum Required Tests |
|---|---|
| Documentation | Check links, coherence with related documents, and absence of normative conflict |
| UI/UX | Validate normal screen, maximized screen, minimum size, hover, focus, click, disabled states, and contrast |
| Frontend | Build, manual workflow of the affected screen, navigation regression, and visual persistence |
| Backend | Compilation/syntactic check, affected endpoints, invalid inputs, and controlled errors |
| Persistence | Create, read, update, delete, corrupt test file, validate backup and migration |
| AI | Simple input, long input, model failure, model absence, incorrect context, and action boundaries |
| Vault/RAG | Upload, read, search, links, sources, manifest, path traversal, and context retrieval |
| Security | Token, CORS, permissions, paths, secrets, logs, and destructive actions |
| Build/release | Clean build, initial execution, displayed version, changelog, and output files |
| Refactoring | Non-regression tests, before/after behavior comparison, and residual risk metrics |

## Validation Matrix by Risk

### R1 — Very Low Risk

Minimum validation:

- manual review of the altered file;
- checking document consistency;
- registry in the plan and in the changelog whenever there is a change to a versioned file.

### R2 — Low Risk

Minimum validation:

- pontuais/local manual tests;
- build or syntactic check when there is code;
- validation of the directly affected component.

### R3 — Moderate Risk

Minimum validation:

- full build;
- manual test of the affected main workflow;
- test of at least one alternative workflow;
- regression test of related modules;
- registry of limitations.

### R4 — High Risk

Minimum validation:

- full build;
- full manual tests of the affected workflow;
- regression tests of dependent workflows;
- error and recovery test;
- rollback plan;
- detailed registry in the changelog.

### R5 — Critical Risk

Minimum validation:

- full build;
- expanded regression test;
- validation of existing data;
- validation of rollback;
- explicit security evaluation;
- human approval before considering completed;
- detailed changelog with residual risks.

## General Checklist Before Concluding a Plan

- [ ] Tested scope matches the plan's scope.
- [ ] Expected behavior was validated.
- [ ] Invalid inputs were evaluated when applicable.
- [ ] Errors are handled safely.
- [ ] There was no perceptible regression in related workflows.
- [ ] Documentation was updated when necessary.
- [ ] Changelog records the executed validation.
- [ ] Testing limitations were recorded.
- [ ] Known gaps were recorded.

## Frontend Tests

Applicable to web, native desktop, mobile, TUI, or hybrid interfaces.

### Minimum Criteria

- Screen opens without error.
- Navigation works.
- Visual states are perceptible.
- Fields accept valid input.
- Fields reject or handle invalid input.
- Destructive actions request confirmation.
- Disabled buttons do not execute actions.
- Resizing does not cause overlap.
- Long text does not break layout.
- Icons and tooltips remain coherent.

### Visual Checklist

- [ ] Normal window.
- [ ] Maximized window.
- [ ] Minimum supported size.
- [ ] Expected theme.
- [ ] Adequate contrast.
- [ ] Hover.
- [ ] Keyboard focus.
- [ ] Pressed.
- [ ] Disabled.
- [ ] Error.
- [ ] Success.
- [ ] Tooltip.
- [ ] Modal.
- [ ] Scroll.

## Backend Tests

### Minimum Criteria

- Application starts.
- Main endpoints respond.
- Invalid inputs return a controlled error.
- External dependency failure does not crash the process.
- Logs do not expose secrets.
- Destructive operations require confirmation or adequate protection.

### API Checklist

- [ ] Health check.
- [ ] Endpoint with valid input.
- [ ] Endpoint with invalid input.
- [ ] Endpoint without authorization when applicable.
- [ ] Endpoint with authorization when applicable.
- [ ] Dependency error.
- [ ] Timeout.
- [ ] Empty response.
- [ ] Large response.

## Persistence Tests

### Minimum Criteria

- Data creation.
- Data reading.
- Data updating.
- Data deletion.
- Backup when applicable.
- Recovery after missing file.
- Recovery after corrupted file.
- Backward compatibility with data from previous version.

### Checklist

- [ ] New data is saved.
- [ ] Saved data is reloaded.
- [ ] Existing data is not lost.
- [ ] Missing file is safely recreated.
- [ ] Invalid file does not cause crash without message.
- [ ] Backup is created before a critical rewrite.
- [ ] Migration, if any, is idempotent.

## AI Tests

### Minimum Criteria

- Model unavailable is handled.
- Empty response is handled.
- Long response is handled.
- Streaming error is handled.
- Retrieved context is displayed when applicable.
- Sources are traceable when applicable.
- AI does not execute actions outside allowed scope.
- Prompt injection in retrieved data is treated as untrusted content.

### Automated Prompt Evaluation (LLM Regression)

For mature projects, relying solely on manual empirical prompt tests is insufficient. The project must adopt an automated LLM evaluation framework (e.g., `promptfoo`) integrated into the CI/CD pipeline to ensure that changes to `AGENTS.md` or the `FCVW/` knowledge base do not degrade the agent's behavior.

### Recommended Cases

- Simple question.
- Long question.
- Ambiguous question.
- Question trying to ignore rules.
- Question requiring local source.
- Question with no source available.
- Cancellation during generation.
- AI runtime failure.

## Security Tests

- [ ] Token or authentication when applicable.
- [ ] CORS or allowed origins when applicable.
- [ ] Path traversal blocked.
- [ ] Secrets do not appear in logs.
- [ ] Files outside the allowed directory are not accessed.
- [ ] Destructive actions require confirmation.
- [ ] Sensitive data is not sent to external services without an explicit rule.
- [ ] Prompt injection does not alter system rules.

## Release Tests

Before publishing a version:

- [ ] All plans of the release are completed.
- [ ] Changelog exists.
- [ ] Version displayed in the application is coherent.
- [ ] `STACK.md` records the correct version.
- [ ] Clean build was executed or limitation was recorded.
- [ ] Main workflow was validated.
- [ ] Known gaps were recorded.
- [ ] Rollback was described when applicable.

---

## Models and Templates

The registration of validation and tests must be done directly in the plan file, following the template in:
`governance/TEMPLATE_PLAN.md`
