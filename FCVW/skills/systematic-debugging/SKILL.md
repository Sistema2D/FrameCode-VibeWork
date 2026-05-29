# Systematic Debugging

*Activation Triggers:* debugging, fixing an error, tracking down a bug, stack trace analysis.

This skill forces a structured, scientific approach to fixing bugs, eliminating the "guess and check" anti-pattern commonly exhibited by AI agents.

## Core Directives

When faced with a bug or an error log, **do not immediately modify code.**

1. **Reproduction & Observation:**
   - Run the code or write a test to reliably reproduce the error.
   - Analyze the stack trace or output. If necessary, use debugging tools (e.g., breakpoints, verbose logging, or the AlmogBaku `debug-skill` if available in your IDE).

2. **Formulate a Hypothesis in FCVW/TROUBLESHOOTING.md:**
   - Before editing any source files in `src/`, you must open or create a troubleshooting log.
   - Document your hypothesis: "I believe the error is caused by X because of Y in file Z."
   - State how you will prove or disprove it.

3. **Verify the Hypothesis:**
   - Add temporary logs, use a debugger, or write an isolated test to confirm your theory.
   - Do not make a logic change until the hypothesis is proven.

4. **Apply the Fix:**
   - Once proven, apply the minimal fix required.
   - Run the tests again to verify the fix.
   - Remove any temporary logging or debugging artifacts.

5. **Update Documentation:**
   - Ensure the resolution is documented in `FCVW/TROUBLESHOOTING.md`.
   - Update the relevant plan in `FCVW/Plans/in_progress/`.

## Anti-Patterns to Avoid
- **Guess and Check**: Changing a line, running a test, seeing it fail, and changing another line blindly.
- **Silent Fixes**: Making a fix without updating the FCVW documentation.
- **Broad Changes**: Refactoring unrelated code while trying to fix a specific bug.
