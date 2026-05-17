# Template: Refactoring Plan

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
