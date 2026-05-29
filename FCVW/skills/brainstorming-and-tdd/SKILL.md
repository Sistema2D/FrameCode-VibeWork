# Brainstorming & Test-Driven Development (TDD) Workflow

*Activation Triggers:* starting a new feature, fixing a bug, answering a request, implementing a plan.

This skill combines the philosophy of the **Superpowers methodology** and the **Spartan AI Toolkit** to enforce discipline on the AI agent.

## Part 1: Brainstorming (Anti-Immediate Action)

When the user asks you to build or fix something, **do not immediately jump into writing code or creating a plan.**

Instead, you must step back and extract a clear specification.

### Brainstorming Rules:
1. **Ask clarifying questions.** What is the edge case? What is the expected user flow?
2. **Do not create a plan in `FCVW/Plans/pending/`** until you have received explicit confirmation of the design/spec from the user.
3. If the request is vague, present options to the user and wait for their choice.
4. **Draft the Spec**: Summarize the agreed-upon requirements into a concise specification block before moving to the FCVW Planning phase.

---

## Part 2: Test-Driven Development (Red/Green TDD)

Once a plan is approved and moved to `FCVW/Plans/in_progress/`, you must enforce TDD.

### Implementation Workflow:
1. **Write the failing test first (Red).** Based on the plan, write the unit or integration test that verifies the expected behavior.
2. **Run the test.** Confirm that it fails because the feature does not exist or the bug is present.
3. **Write the implementation code (Green).** Write the minimal amount of code necessary to make the test pass.
4. **Run the test again.** Ensure it now passes.
5. **YAGNI (You Aren't Gonna Need It).** Do not implement speculative features that are not covered by the failing tests you just wrote.

### Spartan Quality Gates:
- Ensure the commit message format complies with semantic conventions.
- Never commit broken code. If the test fails, do not proceed to close the plan. Fix the code.
