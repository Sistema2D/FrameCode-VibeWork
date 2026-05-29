# Document and Operational Audit

Methodological document to review coherence between documentation, plans, changelogs, versioning, scope, design, tests, security, data, and implementation.

This file should be consulted before closing relevant plans, publishing versions, reorganizing documentation, or validating the general state of the repository.

## Objective

Ensure that the repository remains consistent, traceable, and understandable to humans and AI agents.

## Principles

- Official documents must not contradict each other.
- Every change in a versioned file must have a corresponding changelog. There is no exception for small, document, or process adjustments.
- Completed plans must correspond to changes actually executed.
- Displayed version, documented version, and changelog must be coherent.
- New documents must be cited in `AGENTS.md`.
- Known gaps must be recorded, not hidden.

## Audit Types

### Document Audit

Verifies consistency among Markdown files.

Items:

- updated `AGENTS.md` index;
- related documents cited correctly;
- consistent filenames;
- duplicate rules without conflict;
- absence of contradictory instructions;
- updated templates.

## Records Location

This file defines the audit methodology. Formal audit reports, when created, must be kept in `audits/` at the root of the application.

Reusable syntheses derived from audits can be recorded in `wiki/audits/`, provided they point to the formal report, plan, changelog, or official document used as source.

The governance wiki does not replace formal reports, plans, changelogs, or official documents.

### Version Audit

Verifies coherence of the release.

Items:

- version in code;
- version in `STACK.md`;
- corresponding changelog;
- release status;
- related plans;
- publication criteria.

### Plans Audit

Verifies consistency of the plans.

Items:

- internal plan status;
- correct folder;
- priority and risk defined;
- current and expected version;
- acceptance criteria;
- test plan;
- completion and validation.

### Troubleshooting Audit

Verifies issue memory.

Items:

- open failures;
- recurring failures;
- issues without validation;
- solutions without related plan;
- unrecorded attempts.

### Security Audit

Verifies security risks.

Items:

- secrets in files;
- tokens in logs;
- path traversal;
- CORS or local network;
- permissions;
- command execution;
- sensitive data;
- prompt injection.

### AI Audit

Verifies behavior of AI features.

Items:

- unavailable model;
- streaming errors;
- displayed sources;
- retrieved context;
- boundaries of action;
- memory and learning;
- sensitive data;
- conflicting instructions.

## Minimum Audit Checklist Before Release

> This checklist is for **pre-release auditing** (coherence of the repository as a whole). The **task closure** checklist is in `AGENTS.md`.

- [ ] `AGENTS.md` cites all relevant official documents.
- [ ] The repository root is application-owned: no framework `README.md`, permanent root `docs/`, or framework-owned generated artifacts are present outside `FCVW/`, except bridge/config files such as `AGENTS.md`, `.gitignore`, `.cursorrules`, `.windsurfrules`, and `.github/`.
- [ ] `STACK.md` records the correct version.
- [ ] `changelogs/Vx.y.z.md` exists.
- [ ] The changelog cites related plans.
- [ ] All completed plans are in `Plans/completed`.
- [ ] All in-progress plans are in `Plans/in_progress`.
- [ ] There is no completed plan without validation.
- [ ] There is no resolved issue without minimum evidence.
- [ ] `DESIGN.md` reflects approved visual changes.
- [ ] `SCOPE.md` reflects approved functional changes.
- [ ] `WORKFLOW.md` reflects modified flows.
- [ ] `DATA.md` reflects persistence changes.
- [ ] `SECURITY.md` reflects security changes.
- [ ] `AI.md` reflects AI changes.
- [ ] `TESTS.md` was used for validation compatible with risk.
- [ ] The governance wiki was updated when the audit generated reusable learning.
- [ ] There are no temporary files being used as official source.

## Quick Audit Checklist for AI Agents

Before concluding a response that involved modifying files, the agent must mandatory follow the **Checklist Before Finishing a Change** located at the end of the file:

`AGENTS.md`

This checklist ensures minimal technical and document integrity for each shift.

## Audit Report Template

```markdown
# Audit Report

## Date

YYYY-MM-DD

## Scope of Audit

- 

## Analyzed Files

- 

## Overall Result

`approved` / `approved with reservations` / `rejected`

## Inconsistencies Found

| Item | Document/file | Severity | Recommendation |
|---|---|---|---|
| | | | |

## Gaps

- 

## Recommendations

- 

## Final Validation

- 
```
