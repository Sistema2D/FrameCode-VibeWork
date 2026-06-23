# Unreleased — Declarative Automation Contracts

## Added

- `FCVW/decisions/ADR-0002-declarative-automation-contracts.md` to clarify Markdown-only automation contracts.
- `FCVW/AUTOMATION.md` as the parent document for declarative automation.
- `FCVW/HOOKS.md` for pseudo-hook checklists.
- `FCVW/WATCHERS.md` for Markdown-only watcher rules.
- `FCVW/DAEMONS.md` for manual/agentic daemon loop protocols.
- `FCVW/GOVERNANCE_GATES.md` for central gate trigger mapping.
- `FCVW/governance/TEMPLATE_AUTOMATION_CONTRACT.md`.
- `FCVW/governance/TEMPLATE_HOOK_CHECK.md`.
- `FCVW/governance/TEMPLATE_WATCHER_RULE.md`.
- `FCVW/governance/TEMPLATE_DAEMON_LOOP.md`.
- `FCVW/governance/TEMPLATE_GOVERNANCE_GATE_REPORT.md`.

## Changed

- `AGENTS.md` now references declarative automation contracts for automation/maintenance sessions.
- `FCVW/CONTEXT_MAP.md` now includes a Declarative Automation / Maintenance session type.
- `FCVW/STACK.md` clarifies that automation contracts remain Markdown-only and do not add runtime dependencies.
- `FCVW/MANIFEST.md` includes declarative automation contracts in scope while keeping executable automation out of scope.
- `FCVW/WORKFLOW.md` documents the declarative automation workflow.
- `FCVW/AI.md` clarifies that automation contracts are governance data, not permission to execute commands.
- `FCVW/SECURITY.md` adds security boundaries for hook/watcher/daemon terminology.
- `FCVW/skills/governance-validator/SKILL.md` adds declarative automation integrity checks.
- `FCVW/skills/wiki-lint/SKILL.md` adds knowledge-gap checks for declarative automation contracts.
- `FCVW/skills/README.md` maps declarative automation tasks to existing skills rather than creating a new skill.
- `FCVW/FILESYSTEM.md` lists the new official documents and templates.

## Credits

- The new declarative automation contracts credit public architectural inspiration from `https://github.com/SantanderAI`, especially loop, stop-condition, vault-lint, hard-gate, and guardrail concepts.
- No SantanderAI source code was copied into FCVW.

## Notes

- No executable scripts were introduced.
- No installed Git hooks were introduced.
- No local daemons or coded watchers were introduced.
- No package manifests or runtime dependencies were introduced.
- No CI/CD workflows were introduced.
