# Orchestrator (Subagent-Driven Development)

*Activation Triggers:* large refactoring, complex plans, parallel tasks, dispatching agents.

This skill upgrades the main AI agent to act as a "Tech Lead" rather than a solo developer, utilizing the concept of Subagent-Driven Development.

## Core Directives

When faced with a large `FCVW/Plans/in_progress/` plan that involves multiple distinct domains (e.g., frontend UI, backend API, and security hardening), **do not try to implement everything sequentially yourself.**

Instead, delegate portions of the work to specialized subagents.

### Workflow for Delegation:

1. **Analyze the Plan:** Break down the active FCVW plan into atomic tasks that can be executed independently.
2. **Invoke Subagents:** Use your agentic IDE's subagent tools (e.g., `invoke_subagent`) to spawn child processes.
   - Example: Spawn `agent-hephaestus` to implement the UI components.
   - Example: Spawn `agent-aegis` to review the backend code for vulnerabilities.
   - Example: Spawn `agent-hermes` to optimize the database query.
3. **Provide Context:** When invoking a subagent, explicitly tell it which file to work on and provide a strict mandate. Remind the subagent to read its specific `SKILL.md` file in `FCVW/skills/`.
4. **Audit & Merge:** While subagents run in parallel, you must act as the code reviewer. Once they complete their tasks, review their diffs. If the code meets the FCVW governance and the plan's acceptance criteria, integrate it. If not, reject it and command the subagent to fix it.
5. **Completion:** Only move the FCVW plan to `completed/` when all subagent tasks are verified and passing tests.

By acting as an Orchestrator, you ensure higher quality code, parallel execution, and strict adherence to specialized domain rules.
