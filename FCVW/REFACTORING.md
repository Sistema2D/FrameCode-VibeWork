# REFACTORING.md

Rules, criteria, and metrics for refactoring AI-assisted applications.

This document is a stack-agnostic methodological guide. Applicable to web, desktop, mobile applications, backend services, APIs, libraries, native Windows applications, local AI systems, and cloud AI systems.

> For detailed metrics (full ICR/IRR, complexity tables, commented examples, and bibliographical references), consult `wiki/refactorings/complete-guide.md`.

## 1. Objective

Establish rules, criteria, and workflows for controlled, traceable, and safe refactorings.

Help humans and AI agents decide: when to refactor, which type to apply, what the risk is, what evidence to require, how to test, and how to document.

## 2. Central Principle

Refactoring is the improvement of the internal structure without intentional alteration of the observable external behavior.

- Does not alter features perceived by the user.
- Does not change public contracts without a functional change plan.
- Does not modify business rules.
- Does not alter persisted data without a migration plan.
- Is done in small, verifiable, and reversible steps whenever possible.

If the external behavior needs to change, the modification is not just refactoring — it must be classified as a functional change, bugfix, migration, or architectural evolution.

## 3. Relationship with Other Documents

- `AGENTS.md`: general conduct, precedence of instructions, mandatory plans, and changelog.
- `PLANNING.md`: plan creation, priority, risk, acceptance criteria, and tests.
- `VERSIONING.md`: version increment, changelog, rollback.
- `TROUBLESHOOTING.md`: consult when refactoring is linked to failures or regressions.
- `DESIGN.md`: consult when refactoring affects the interface or visual components.
- `WORKFLOW.md`: update when refactoring alters the operational workflow.
- `SCOPE.md`: update only if refactoring reveals or requires a formal scope change.

## 4. Mandatory Rule

No refactoring that alters files should be applied without a plan in `Plans/`.

The plan must contain: reason, type, preserved external behavior, affected files, risk, testing strategy before and after, acceptance criteria, rollback when applicable, current version, expected version, and corresponding changelog.

## 5. What is Refactoring

- Extract function, method, class, component, service, or module.
- Rename internal elements to increase clarity.
- Remove duplication.
- Reduce conditional complexity.
- Separate responsibilities.
- Improve cohesion and reduce coupling.
- Reorganize folders and modules without changing public contracts.
- Centralize constants, tokens, settings, or utilities.
- Encapsulate access to data, API, global state, or external resources.
- Make code more testable.

## 6. What is Not Refactoring

Do not classify as isolated refactoring: feature creation, business rule change, visible layout modification, API contract change, database migration, stack swap, wide rewrite, bugfix that alters output, feature removal, or permission/security changes.

## 7. Valid Refactoring Objectives

Valid: reduce complexity, duplication, coupling; improve cohesion, readability, testability; prepare for planned change; remove documented technical debt.

Invalid: "improve everything", "make it more modern" without criteria, "rewrite because it is ugly", "apply design pattern without concrete need".

## 8. Signs that Motivate Refactoring

- **Complexity**: too many responsibilities, nested conditionals, excessive global variables.
- **Duplication**: similar blocks repeated, duplicated rules in frontend/backend.
- **Low cohesion**: module mixes UI, business rule, persistence, network, and validation.
- **High coupling**: small change affects many files; circular dependencies.
- **Fragility**: recurring failures in the same module; bugfixes caused previous regressions.
- **Obsolescence**: architecture does not support planned evolution; temporary decisions became the standard.

## 9. When to Avoid Refactoring

Avoid when: there is no clear success criterion; there is no possible validation; the system is unstable due to an misunderstood failure; the change mixes too many intentions; the motivation is purely aesthetic; refactoring is not necessary for the requested fix.

## 10. Refactoring Types

| Code | Type | Description |
|---|---|---|
| RF1 | Local | Small and isolated code block (extract function, rename) |
| RF2 | Component | Specific component, class, screen, or module |
| RF3 | Cross-cutting | Utilities, patterns, or shared code |
| RF4 | Architectural | Internal boundaries or layer organization |
| RF5 | Preparatory | Prepares for future already planned change |
| RF6 | Corrective | Reduces fragility linked to a bug or issue |
| RF7 | Testing | Improves test structure without altering production |
| RF8 | Visual internal | Reorganizes UI code without changing approved appearance |
| RF9 | Data | Reorganizes data access without changing persisted content |
| RF10 | Build/infrastructure | Organizes scripts, pipelines, or configuration |

## 11. Priority Scale

| Priority | Use when |
|---|---|
| P1 | Structure causes risk of data loss, severe failure, or blocks essential fix |
| P2 | Affects main workflow, stability, frequent maintenance, or planned evolution |
| P3 | Hinders maintenance, testing, or evolution, but does not compromise immediate operation |
| P4 | Improves clarity or organization with low impact |
| P5 | Desirable, experimental, or preventive, with no clear short-term impact |

## 12. Risk Scale

| Risk | Criterion |
|---|---|
| R1 | Local change, no public contract, no persistence, no integration |
| R2 | Limited to a component or module, with sufficient localized tests |
| R3 | Relevant workflow, shared file, or module with dependencies |
| R4 | Global state, persistence, integration, internal contracts, or multiple modules |
| R5 | Core architecture, security, migration, critical data, or broad main workflow |

R4 and R5 refactorings must have explicit rollback and expanded regression validation.

> For ICR (Candidacy) and IRR (Risk) indices with detailed scoring, consult `wiki/refactorings/complete-guide.md`.

## 13. Priority Code Smells

| Smell | Sign | Common Action |
|---|---|---|
| Duplicated code | same logic in two or more points | extract function, create utility |
| Long method | extensive routine difficult to understand | extract method, decompose condition |
| Large class | too many responsibilities | extract class, divide module |
| Primitive obsession | implicit rules in strings/numbers | create type, enum, or semantic constant |
| Divergent change | module changes for different reasons | separate responsibilities |
| Shotgun surgery | one change requires many adjustments | centralize rule or contract |
| Dead code | unused or obsolete snippet | remove with validation and changelog |
| Complex conditionals | too many variations by type/status | strategy, decision table, or handler map |
| Excessive global state | too many points read/write state | encapsulate, create store or service |
| Hidden dependency | implicit call order | make dependency explicit |

## 14. Entry and Block Criteria

### Entry — check before starting

- Plan exists in `Plans/` with motivation and preserved external behavior described.
- Affected files listed and risk classified.
- Testing strategy before and after defined.
- Rollback documented for R4/R5.
- Related issues consulted in `troubleshooting/`.
- Scope sufficiently small for review.

### Block — stop or reformulate if

- It is not possible to explain the preserved external behavior.
- There is no minimal validation possible.
- Refactoring is mixed with new features without justification.
- The change requires unplanned data migration.
- The risk is R4/R5 without rollback or containment strategy.
- The change could expose sensitive data or credentials.

## 15. Recommended Batch Sizes

| Batch | Recommendation |
|---|---|
| 1 file or 1 logical unit | Preferred |
| Few files from the same module | Acceptable with clear tests |
| Multiple modules or layers | Divide into phases |
| Core architecture, data, or global contracts | Treat as architectural change |

Rule: if the plan requires too many sentences to explain what remains the same, the batch is too large.

## 16. Safe Strategies

1. **Characterize before modifying**: record current behavior via characterization tests, snapshots, manual checklist, or output comparison.
2. **Small steps**: understand → validate → isolate snippet → transform → test → record → repeat.
3. **Separate structural from behavioral**: never mix refactoring with new features, bugfixes, redesigns, library swaps, or migrations in the same step.
4. **Preserve contracts**: identify inputs, outputs, events, file formats, and compatibility before altering internally.
5. **Avoid speculation**: preparatory refactoring is only acceptable when linked to an approved plan or documented risk.

## 17. Metrics by Application Type

### Web Applications

Evaluate: large components or components with mixed responsibilities; business logic in visual components; scattered HTTP calls; inconsistent error handling; CSS duplicated or outside the design system.

### Native Windows or Desktop Applications

Evaluate: excessive concentration of logic in the main window; very large event handlers; messages, timers, and global states difficult to track; OS resources without encapsulation; inconsistency between clickable area and drawn area.

When instantiating the framework, record here specific modules, events, or workflows of the project that require special attention.

### Backends, APIs, and Services

Evaluate: routes with embedded business rules; duplicated validation; implicit DTOs; inconsistent exception handling; scattered queries; API contracts without tests.

### Applications with AI

Evaluate: scattered prompts without versioning; absence of boundary between system, user, and context; parser of model JSON without validation; absence of fallback; prompt injection risk; lack of separation between user data, retrieved context, and system instructions.

### Applications with Local Persistence

Evaluate: non-atomic writing; absence of backup; absence of migration; versioned data mixed with user data; unvalidated paths; absence of backward compatibility.

## 18. Minimum Tests by Risk

| Risk | Minimum Tests |
|---|---|
| R1 | build or lint, manual test of the affected snippet |
| R2 | localized tests, manual validation of the component |
| R3 | module tests, regression of the affected workflow, before/after comparison |
| R4 | expanded tests, regression of main workflows, data validation, documented rollback |
| R5 | phased plan, strong characterization, migration validation, rollback, human review recommended |

## 19. Acceptance Criteria

A refactoring can only be considered completed when:

- the preserved external behavior was validated;
- the tests defined in the plan were executed or the limitation was recorded;
- the complexity, duplication, or other target problem was reduced or justified;
- no unplanned functional changes were introduced;
- there was no known regression in the affected workflows;
- impacted documents were updated;
- the changelog records what changed, why it changed, and how it was validated;
- the plan was updated with the result and final status.

## 20. Checklists

### Before Refactoring

- [ ] Is the change really a refactoring?
- [ ] Is the preserved external behavior described?
- [ ] Does a plan exist in `Plans/`?
- [ ] Does the plan indicate type, priority, and risk?
- [ ] Is there an objective success criterion?
- [ ] Is there a test plan?
- [ ] Is there a rollback plan for R4/R5?
- [ ] Was `TROUBLESHOOTING.md` consulted if there is a relationship with a failure?
- [ ] Was `DESIGN.md` consulted if there is an impact on UI?
- [ ] Will `WORKFLOW.md` be updated if there is an impact on workflow?

### During Refactoring

- [ ] Change in small steps.
- [ ] Avoid mixing new behavior.
- [ ] Perform incremental validation.
- [ ] Preserve public contracts.
- [ ] Do not remove code without confirming it is dead or replaced.
- [ ] Do not alter persisted data without its own plan.
- [ ] Do not expand scope without updating the plan.

### After Refactoring

- [ ] Build, lint, or equivalent verification executed.
- [ ] Tests defined in the plan executed.
- [ ] Affected workflows validated.
- [ ] Preserved external behavior confirmed.
- [ ] Changelog updated.
- [ ] Plan updated with final result.
- [ ] Impacted documentation updated.
- [ ] Known gaps recorded.
- [ ] Rollback documented when applicable.

## 21. Models and Templates

To create refactoring plans, use the template in:
`governance/TEMPLATE_REFACTORING.md`

## 22. Rules for AI Agents

Upon receiving a refactoring request, the AI must:

1. Identify if it is an analysis, planning, or actual change.
2. If it is an actual change, locate or create a plan before modifying files.
3. Declare the external behavior that must be preserved.
4. Classify type, priority, and risk.
5. Check related documents.
6. Propose division into phases if the risk is high.
7. Avoid unsolicited functional changes.
8. Perform validations compatible with the stack.
9. Update changelog and impacted documentation.
10. Record limitations when unable to test everything.

The AI must not: rewrite entire modules without justification; change external behavior without warning; remove code because it seems useless without evidence; apply design patterns out of preference; ignore tests because the change "seems simple".

When the refactoring is R3/R4/R5, the AI must respond or ask: what structural problem will be solved; what behavior must remain the same; which files will be affected; are there tests or reliable validation; is there a history of failures; how rollback will be done; what is the smallest safe batch.

## 23. Final Rule

A good refactoring is one that makes the software simpler to understand, test, modify, and evolve, without surprising the user, breaking contracts, or hiding functional changes inside a technical reorganization.

When in doubt between refactoring now or preserving stability, prioritize stability, evidence, and traceability.

---

## 24. Technical Debt & Refactoring Ledger

To ensure that temporary shortcuts or non-blocking design flaws do not accumulate silently:
1. **Mandatory Logging:** Any compromise in design patterns, missing test cases, or temporary workarounds must be logged as a `#tech-debt` item in the wiki using the template: `wiki/templates/TEMPLATE_TECH_DEBT.md`.
2. **Refactoring Priority Alignment:** Remediation plans for high-severity technical debt must be scheduled into the priority list (P1-P5) in future change plans.
3. **Continuous Pay-Down:** When modifying a file or module that contains an active `#tech-debt` wiki card, evaluate if part or all of that debt can be safely paid down (refactored) as part of the preparatory work of your active plan, moving the wiki card status to `obsolete` or `superseded` upon completion.

