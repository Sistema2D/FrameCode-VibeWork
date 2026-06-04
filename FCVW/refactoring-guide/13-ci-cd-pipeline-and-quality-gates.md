# 13 — CI/CD Pipeline and Quality Gates

This file defines the automation controls that must protect refactorings before merge and, when applicable, before deploy.

## Objective

Ensure that a refactoring does not enter the main branch without minimal automated evidence of quality, build, testing, and compatibility.

## Governance rule

> No medium, high, or critical risk refactoring should be approved with a broken pipeline, ignored tests without justification, or pending quality analysis.

## Minimum gates

| Gate | Purpose | Mandatory for |
|---|---|---|
| Clean build | Confirm compilation/packaging. | All levels. |
| Lint/format | Avoid noise and divergent patterns. | All levels. |
| Unit tests | Validate local behavior. | All levels when they exist. |
| Integration tests | Validate communication between parts. | Medium or higher. |
| Contract tests | Validate APIs/events/DTOs. | High/critical or public interface. |
| E2e/smoke tests | Validate user flow or initialization. | High/critical. |
| Type check | Validate static types when applicable. | Typed projects. |
| Static analysis | Detect bugs, vulnerabilities, duplication, complexity. | Medium or higher. |
| Coverage | Prevent unjustified reduction. | Medium or higher. |
| Dependency scan | Detect library impact and security. | When dependencies change. |
| Artifact generation | Confirm packaging/deploy. | High/critical. |

## Pipeline policy

1. The main branch pipeline must be green before starting.
2. Pre-existing failures must be registered before refactoring.
3. New failures block merge.
4. Removed or ignored tests require explicit justification.
5. Changes to the pipeline itself must be in a separate PR.
6. Refactoring must not relax quality rules to pass.
7. Quality metrics should improve or remain stable.

## Gates by risk

### Low

- build;
- lint/format;
- local tests or available CI;
- PR checklist.

### Medium

- build;
- lint/format;
- unit tests;
- characterization tests when applicable;
- coverage without unjustified drop;
- 1 technical reviewer.

### High

- all medium risk gates;
- integration/regression tests;
- static analysis;
- attached impact map;
- rollback plan;
- 2 reviewers.

### Critical

- all high risk gates;
- smoke/e2e of critical flows;
- artifact validation;
- execution in staging/homologation environment when it exists;
- post-deploy monitoring;
- formal approval from the owner.

## Recommended metrics

- coverage before/after;
- build time before/after;
- test time before/after;
- cyclomatic complexity;
- duplication;
- number of changed files;
- number of added/removed lines;
- added/removed dependencies;
- number of warnings.

## Rules for monorepos or very large codebases

- Execute tests affected by the dependency graph when available.
- Run the full suite before merge on high-impact PRs.
- Avoid global formatting changes together with logical refactoring.
- Separate dependency update PR from refactoring PR.
- On import/path changes, validate clean build from scratch.

## Evidence in the PR

```markdown
### Executed gates
- Build: passed/failed/link
- Lint/format: passed/failed/link
- Unit tests: passed/failed/link
- Integration/e2e/smoke: passed/failed/link
- Coverage before/after:
- Static analysis:
- Observations:
```
