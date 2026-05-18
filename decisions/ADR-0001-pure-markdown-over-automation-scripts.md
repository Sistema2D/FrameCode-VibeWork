# ADR-0001 — Pure Markdown Instructions over Automation Scripts and Mockups

## Status

`accepted`

## Date

2026-05-18

## Context

The framework initially introduced a physical `mockups/` folder for visual mockup comparisons and a PowerShell script `governance/scripts/sync-filesystem.ps1` to automatically synchronize directory trees. While this provided some automation, it introduced external environment setup dependencies (PowerShell ExecutionPolicies, CLI tools), increased filesystem maintenance debt, and diluted the primary identity of FrameCode VibeWork as a lightweight, highly portable, pure-markdown governance model.

## Decision

We decide to:
1. Deprecate and physically remove the `mockups/` folder. All layout specifications, interactive guidelines, and component descriptions will reside natively inside a robust `DESIGN.md` file.
2. Deprecate and physically remove the `sync-filesystem.ps1` script. The project's visual filesystem tree will be declared and maintained purely via Markdown files (`FILESYSTEM.md` and `README.md`) using strict manual verification by the agent, without executing local automation scripts.
3. Re-orient the framework's entire operation around declarative Markdown-based prose and the AI Skills Engine (ASE) rather than active programmatic scripting.

## Alternatives Considered

### Alternative 1: Keeping the PowerShell Scripting Suite
- **Description**: Maintain the `sync-filesystem.ps1` script and expand it into other tasks like wiki linting and plans management.
- **Advantages**: Automates layout mapping and taxonomy checking.
- **Disadvantages**: Fails to run on environments without PowerShell (macOS/Linux), requires manual bypass of execution policies on Windows, and increases programming logic overhead in a document-based framework.

### Alternative 2: Introducing node-based CLI tools
- **Description**: Rewrite the scripts using JavaScript/Node.js.
- **Advantages**: Cross-platform execution.
- **Disadvantages**: Introduces a `package.json`, node_modules clutter, dependency management debt, and makes the framework heavy.

## Justification

We chose the pure-markdown approach because LLM agents are highly proficient at linguistic reasoning, textual formatting, and checking directory layouts. Moving design requirements into `DESIGN.md` and keeping directory trees declarative inside `FILESYSTEM.md` keeps the project 100% portable, secure, lightweight, and perfectly readable by any AI model without runtime constraints.

## Positive Consequences
- **Absolute Portability**: Works out of the box in Windows, macOS, Linux, and custom cloud sandboxes.
- **Simplified Structure**: Eliminated dependency on execution policies and shell scripts.
- **Stronger Design System**: A significantly more robust `DESIGN.md` centralized visual rules, reducing context dilution.
- **Fewer Workspace Files**: Deprecating scripts and mockups folder slimmed down the framework workspace.

## Negative Consequences
- Updates to `FILESYSTEM.md` visual trees must be done manually by the agent. (But this is highly safe because agents are excellent at editing markdown text).

## Risks
- Minor risk of agent oversight when updating visual directory trees, mitigated by explicit checklist steps inside `AGENTS.md`.

## Impact on Files or Modules
- `mockups/` folder: Deleted.
- `governance/scripts/sync-filesystem.ps1` script: Deleted.
- `DESIGN.md`: Heavily expanded.
- `FILESYSTEM.md`: Converted to a purely declarative manual ledger.
- `AGENTS.md`: Checklist updated to remove script execution commands.
- `AI.md`: Policies updated.

## Relationship with Documents
- `SCOPE.md`: Unchanged.
- `STACK.md`: Updated to declare pure-markdown architecture.
- `WORKFLOW.md`: Unchanged.
- `DATA.md`: Unchanged.
- `SECURITY.md`: Simplified (no script execution threat vectors).
- `AI.md`: Focuses on prose and ASE skills triggers.

## Related Plan
- `P4-R2-2026-05-18-discontinue-mockups-and-automation-scripts.md`

## Related Changelog
- `V0.4.0`

## Related ADRs
- None.
