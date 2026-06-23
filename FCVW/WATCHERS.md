# Declarative Watchers

## Objective

Define Markdown-only watcher rules for changes that require governance attention in FrameCode VibeWork.

These watcher rules are not implemented as file-system observers. They are event/reaction contracts evaluated by humans or AI agents during review, maintenance, PR preparation, or release validation.

## Watcher Rule Model

Each watcher rule has:

- an observed event;
- a detection method;
- expected reaction;
- owner document or skill;
- blocking behavior;
- required evidence.

## Watcher Matrix

| Observed event | Detection method | Expected reaction | Owner | Blocking? |
|---|---|---|---|---|
| File added under `FCVW/` | Repository diff or manual inspection | Update `FILESYSTEM.md` and related indexes | `governance-validator` | Yes |
| File removed under `FCVW/` | Repository diff or manual inspection | Update `FILESYSTEM.md`, references, and changelog | `governance-validator` | Yes |
| File moved or renamed | Repository diff or manual inspection | Update links, `FILESYSTEM.md`, and any manifest/index entries | `governance-validator` | Yes |
| Plan moved between status folders | Plan folder review | Confirm internal `Status` field matches folder | `PLANNING.md` | Yes |
| Versioned file changed | Repository diff | Confirm changelog fragment exists | `VERSIONING.md` / `AGENTS.md` | Yes |
| New skill or agent profile proposed | Scope review | Run Agent/Skill Creation Gate | `agent-factory` | Yes |
| Existing skill or agent rule changed | Scope review | Run Skill/Agent Self-Improvement Gate | `self-improvement` | Yes |
| Wiki page added or changed | Repository diff or manual inspection | Run wiki lint, update `wiki/index.md` and `FILESYSTEM.md` as needed | `wiki-lint` | Yes |
| ADR created | Decisions review | Check wiki decision promotion and related references | `wiki-lint` | Warning |
| Release changelog changed | Release review | Check release synthesis and version coherence | `release-checklist` | Yes |
| Release summary added or changed | Repository diff | Update `wiki/index.md`, run wiki lint, and verify version coherence | `release-checklist` | Yes |
| Secret-like value detected | Manual or AI inspection | Stop and apply `SECURITY.md` | `SECURITY.md` / `agent-aegis` | Yes |
| Automation terminology appears | Document review | Confirm Markdown-only Scenario 1 compliance | `AUTOMATION.md` | Yes |
| External inspiration credited | Document review | Confirm credit is conceptual and not copied code | `AUTOMATION.md` / `ADR-0002` | Warning |

## False Positive Handling

If a watcher appears to trigger incorrectly, record:

- the observed event;
- why it looked relevant;
- why it was dismissed;
- which document or skill owns the final decision.

False positives should not be silently ignored when the event involves security, file movement, changelogs, plan state, or skill changes.

## Evidence

Watcher evidence belongs in the active plan. If the watcher affects wiki curation, release validation, audit, or troubleshooting, also update the appropriate target record.

## SantanderAI Inspiration Credit

The event/reaction style and vault-maintenance thinking are conceptually inspired by public SantanderAI repositories at `https://github.com/SantanderAI`, especially `SantanderAI/ralph-vault-skill`. No code is copied.
