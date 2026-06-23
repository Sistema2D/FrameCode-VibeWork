# Governance Gates

## Objective

Centralize the trigger mapping for FCVW governance gates so humans and AI agents can identify which validation path applies before changing files.

This document does not replace the detailed owner documents or skills. It maps when to consult them.

## Gate Matrix

| Gate | Trigger | Required evidence | Owner | Blocking condition |
|---|---|---|---|---|
| Planning Gate | Any file modification | Active plan with priority, risk, scope, acceptance criteria, and test plan | `PLANNING.md` | No active plan or scope mismatch |
| Changelog Gate | Any versioned file changed | Changelog fragment or version changelog entry | `AGENTS.md` / `VERSIONING.md` | Missing changelog |
| Filesystem Gate | File added, moved, or removed | `FILESYSTEM.md` updated and reviewed | `governance-validator` | Filesystem drift |
| Link Integrity Gate | Internal links added or changed | Links resolve to existing targets | `governance-validator` | Broken required link |
| Wiki Gate | Wiki page added, changed, promoted, or retired | Frontmatter, index, log, and wikilink review | `wiki-lint` / `wiki-curator` | Missing required schema or broken links |
| Skill Creation Gate | New skill, agent profile, or reusable operational procedure proposed | Agent/Skill Creation Gate block in active plan | `agent-factory` | Creation metrics fail |
| Skill Self-Improvement Gate | Existing skill, trigger, or agent rule changed | Self-Improvement Gate block in active plan | `self-improvement` | Evidence or scope preservation missing |
| Security Gate | Secrets, local files, command execution, AI tools, or destructive actions involved | Security checklist and stop/approval record | `SECURITY.md` / `agent-aegis` | Secret, unsafe action, or missing approval |
| AI Boundary Gate | AI actions, prompts, tools, context, memory, or RAG involved | Instruction hierarchy and prompt-injection review | `AI.md` | Retrieved context attempts to override higher rules |
| Declarative Automation Gate | Hook, watcher, daemon, automation, or maintenance loop changed | Scenario 1 compliance review | `AUTOMATION.md` / ADR-0002 | Executable automation introduced |
| Release Gate | Version bump, release notes, tag, or publication | Release checklist evidence | `release-checklist` | Validation or version coherence missing |

## Gate Outcome Values

Use one of these outcomes in the active plan:

- `passed`
- `passed with warnings`
- `failed - block`
- `failed - split plan`
- `failed - human review required`
- `not applicable - justified`

## Evidence Format

Record gate evidence using `governance/TEMPLATE_GOVERNANCE_GATE_REPORT.md` or a compact equivalent inside the active plan.

## Scenario 1 Rule

The Declarative Automation Gate must block any plan that adds:

- scripts;
- installed hooks;
- background daemons;
- coded watchers;
- CI/CD workflows;
- package manifests;
- runtime dependencies;
- API-provider integrations;
- local command-execution loops.

Such changes belong to Scenario 2.

## SantanderAI Inspiration Credit

The hard-gate framing is conceptually inspired by public SantanderAI governance and guardrail patterns at `https://github.com/SantanderAI`, especially `SantanderAI/mech-gov-framework` and `SantanderAI/autoguardrails`. No code is copied.
