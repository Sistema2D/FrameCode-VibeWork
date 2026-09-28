# Template: refactoring

Use this template for controlled refactorings (internal improvement without functional change).

```markdown
# P<P>-R<R>-YYYY-MM-DD-refactor-<componente>

## Classification
- Type: `RF1` to `RF10`
- Priority: `P1` to `P5`
- Risk: `R1` to `R5`
- ICR (Candidacy): 0-100
- IRR (Risk): 0-100

## Motivation
<What code smell or structural problem justifies this action?>

## Preserved External Behavior
<What must continue working exactly as before? List contracts and outputs.>

## Scope
- Included:
- Excluded:

## Implementation Plan
1. Characterize behavior (tests before).
2. Isolate code block.
3. Transform.
4. Validate (tests after).

## Test Plan
- Before:
- After:
- Regression:

## Acceptance Criteria
- [ ] Preserved external behavior.
- [ ] Complexity reduced.
- [ ] Tests approved.

## Rollback
<How to revert in case of failure?>

## Final Result (Fill on completion)
| Metric | Before | After |
|---|---|---|
| | | |
```


Each section below is one stage of the refactoring lifecycle described in the [refactoring guide](../REFACTORING_GUIDE.md). Copy only the stages the plan needs, in the recommended order: opening, inventory, dependency map, risk matrix, characterization tests, incremental plan, rollback, ADR exception, pull request, post-validation, then the hygiene and monolith gates when applicable.


## Template: Refactoring Opening

Use this template to formalize the start of a refactoring initiative.

### 1. Context and Motivation
<Describe the technical debt, code smell, or motivation to start the refactoring.>

### 2. Refactoring Scope
- **Included:** <Modules, classes, or files to be refactored>
- **Excluded:** <Modules or files specifically out of scope>

### 3. Preserved External Behavior
<What must continue working exactly as before? List contracts and outputs.>

### 4. Acceptance Criteria
- [ ] Complexity reduced.
- [ ] All regression tests passing.
- [ ] No behavioral change observed.

## Template: Module Inventory

Use this template to map module ownership, dependencies, and criticality before refactoring.

### 1. Module Overview
- **Module Name:**
- **Code Owner(s):**
- **Criticality Level:** (Low/Medium/High/Critical)

### 2. Dependencies
- **Upstream Dependencies:**
- **Downstream Consumers:**

### 3. Current Test Coverage
- **Unit Tests:** %
- **Integration Tests:** %
- **Missing Coverage:** <Identify gaps that need tests before refactoring>

## Template: Dependency and Impact Map

Use this template to map direct and indirect dependencies before starting.

### 1. Direct Dependencies
<Libraries, internal modules, or external APIs directly called by this code.>

### 2. Indirect Consumers
<Other systems or modules that rely on the output of this code, even indirectly.>

### 3. Breaking Change Assessment
- Are there any API contract changes? (Yes/No)
- If Yes, how will consumers be migrated?

## Template: Refactoring Risk Matrix

Use this matrix to score and classify the risk of the proposed refactoring.

### 1. Risk Factors
| Factor | Score (1-5) | Justification |
|---|---|---|
| Module Criticality | | |
| Scope Breadth | | |
| Shared State Impact | | |
| Lack of Test Coverage | | |
| **Total Risk Score:** | | |

### 2. Classification
- **Risk Level:** (R1 to R5 based on total score)
- **Mandatory Controls:** <List required testing or rollback strategies based on risk>

## Template: Characterization Test Plan

Use this template to plan tests that record the current behavior before changing code.

### 1. Behaviors to Characterize
<List the precise behaviors, edge cases, and outputs that need to be captured.>

### 2. Test Implementation
- [ ] Write characterization tests for success paths.
- [ ] Write characterization tests for error handling.
- [ ] Ensure CI pipeline passes with these tests on the legacy code.

### 3. Verification
<How will we prove the new code behaves identically to the characterized baseline?>

## Template: Incremental Plan

Use this template to split large refactorings into smaller, reversible, and testable stages.

### 1. Stage 1: Preparation
<E.g., adding characterization tests, creating new empty classes>

### 2. Stage 2: Parallel Implementation
<E.g., implementing the new structure alongside the old one>

### 3. Stage 3: Routing / Branching by Abstraction
<E.g., routing traffic to the new implementation via feature flags>

### 4. Stage 4: Cleanup
<E.g., deleting the old legacy code once the new code is stable>

## Template: Rollback Plan

Use this template to define how to safely revert the refactoring if critical issues are discovered in production.

### 1. Rollback Triggers
<What specific metrics or errors will trigger an immediate rollback?>

### 2. Rollback Procedure
1. <Step 1 to revert code or feature flag>
2. <Step 2 to revert data or state changes (if applicable)>
3. <Communication plan>

### 3. Post-Rollback Validation
<How to ensure the system stabilized after the rollback is applied?>

## Architectural Decision Record (ADR): Refactoring Exception

Use this template if the refactoring requires a relevant architectural exception or decision.

### 1. Context
<What is the specific situation that requires an exception or architectural decision?>

### 2. Decision
<State the decision clearly.>

### 3. Consequences
- **Positive:**
- **Negative:**

## Pull Request: Refactoring

### Description
<Brief description of what was refactored and why.>

### Checklist
- [ ] No functional changes were introduced.
- [ ] Tests cover all refactored paths.
- [ ] CI pipeline is green.
- [ ] Rollback plan is documented (if required by risk level).

### Risk Level
<State the risk level (R1-R5) and confirm mitigations.>

## Post-Validation Report

Use this template to record the results of the post-deploy verification of a refactoring.

### 1. Validation Steps Executed
<List the steps taken to verify the code in the target environment.>

### 2. Metrics / Performance Impact
- **Before Refactoring:**
- **After Refactoring:**

### 3. Final Conclusion
- [ ] Refactoring stabilized.
- [ ] No unexpected regressions.
- [ ] Old code safely deleted (if applicable).

## Template: Code Hygiene Report

Save in the active plan, `audits/`, or `wiki/` (`type: refactoring` notes) depending on scope. Use this before broad cleanup, retroactive instantiation cleanup, or refactoring of duplicated/monolithic areas.

```markdown
# Code Hygiene Report: <target area>

## Metadata

- **Date:** YYYY-MM-DD
- **Related plan:** `<Plans/...>`
- **Skill loaded:** `skills/code-hygiene-refactor/SKILL.md`
- **Scan level:** `local` / `module` / `systemic`
- **Target area:** `<folder, module, feature, service, or workflow>`
- **Behavior to preserve:** `<observable behavior>`

## Inventory

| Path | Role | Owner | Risk | Tests/validation | Notes |
|---|---|---|---|---|---|
| `<path>` | `<role>` | `<owner>` | `R1-R5` | `<tests>` | `<notes>` |

## Findings

| Finding | Path | Evidence | Action | Status |
|---|---|---|---|---|
| `duplicate` / `large-file` / `dead-code` / `stale-file` / `catch-all` | `<path>` | `<search/test/manual evidence>` | `<extract/remove/defer/split>` | `open` / `done` / `deferred` |

## Selected Cleanup Batch

- **Batch scope:** `<smallest reversible unit>`
- **Why this batch first:** `<impact and risk>`
- **Files changed:** `<paths>`
- **Rollback:** `<git revert or manual rollback>`

## Validation

| Check | Result | Evidence |
|---|---|---|
| `<check>` | `passed` / `failed` / `not run` | `<stdout, manual note, or limitation>` |

## Deferred Debt

- `<debt item, reason, follow-up plan or wiki card>`
```

## Template: Anti-Monolith Gate

Save or embed in the active plan before implementing a non-trivial module, component, route, service, prompt, or workflow.

```markdown
## Anti-Monolith Gate

- **Skill loaded:** `skills/anti-monolith-guard/SKILL.md`
- **Target artifact:** `<path or planned path>`
- **Change type:** `new file` / `extension` / `extraction` / `migration`
- **Artifact class:** `source` / `operational instruction` / `documentation` / `record/template/generated`
- **Numeric threshold applicability:** `applicable` / `warning only` / `not applicable`
- **Primary responsibility:** `<one sentence>`
- **Explicit non-responsibilities:**
  - `<responsibility excluded from this artifact>`
- **Inputs:** `<parameters, events, files, context, request body, props, messages>`
- **Outputs:** `<return, UI, event, written file, response, side effect>`
- **Collaborators:** `<direct dependencies only>`
- **State ownership:** `<none / local / shared / external / persistent>`
- **Side effects:** `<none / IO / network / persistence / process / UI>`
- **Size budget:** `<warning threshold and block threshold>`
- **Threshold source or resize rationale:** `<default, project override, or evidence-based adjustment>`
- **Similar code checked:** `<paths or search summary>`
- **Split decision:** `proceed` / `split first` / `temporary exception`
- **Temporary exception reason:** `<required if exception>`
- **Validation:** `<exact test, build, lint, manual check, or characterization>`
- **Follow-up debt:** `<none or #tech-debt link>`
```

### Pass Criteria

- One primary responsibility is stated.
- Excluded responsibilities are listed.
- Numeric thresholds are enforced only for applicable source or operational artifacts; documentary length alone cannot fail the gate.
- Any exception or resized threshold records critical-attribute impact, validation, owner, and revisit condition.
- Similar code was checked before writing.
- The planned artifact stays under the configured budget or has an explicit exception.
- Validation is specific enough to prove behavior and boundary integrity.
