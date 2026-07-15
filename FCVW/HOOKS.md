---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Hook contracts

A hook is a deterministic checklist at a lifecycle boundary such as pre-edit, pre-commit, pre-release, post-deploy, or session close.

Each hook declares:

- event and scope;
- execution mode: manual, agent, local tool, or CI;
- preconditions and required permissions;
- ordered checks;
- pass, warn, and block outcomes;
- evidence destination;
- timeout/failure behavior;
- bypass authority and expiry;
- rollback or disable procedure.

Scenario 1 hooks are Markdown checklists. Do not claim a Git hook is installed unless its executable artifact exists and was authorized.

Use `governance/TEMPLATE_HOOK_CHECK.md`.
