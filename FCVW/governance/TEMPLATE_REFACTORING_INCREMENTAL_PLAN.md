# Template: Incremental Plan

Use this template to split large refactorings into smaller, reversible, and testable stages.

## 1. Stage 1: Preparation
<E.g., adding characterization tests, creating new empty classes>

## 2. Stage 2: Parallel Implementation
<E.g., implementing the new structure alongside the old one>

## 3. Stage 3: Routing / Branching by Abstraction
<E.g., routing traffic to the new implementation via feature flags>

## 4. Stage 4: Cleanup
<E.g., deleting the old legacy code once the new code is stable>
