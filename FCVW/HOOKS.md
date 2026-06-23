# Declarative Hooks

## Objective

Define Markdown-only pseudo-hooks for repository operations in FrameCode VibeWork.

These hooks are not installed in Git. They are checklists evaluated by humans or AI agents before or after relevant operations.

## Hook Semantics

A declarative hook has:

- a trigger;
- required checks;
- blocking conditions;
- evidence to record;
- owner documents or skills.

A declarative hook must never execute a shell command, install a file into `.git/hooks`, or bypass the active plan workflow.

## pre-change

### Trigger

Before editing any versioned file.

### Required Checks

- [ ] An active plan exists in `FCVW/Plans/`.
- [ ] The file change is within the active plan scope.
- [ ] Priority and risk are classified.
- [ ] Required skills are identified through `AGENTS.md` and `CONTEXT_MAP.md`.
- [ ] `FCVW/Plans/in_progress/` has no overlapping scope conflict.
- [ ] The change does not require executable automation under Scenario 1.

### Blocking Conditions

- No plan exists.
- The change is outside the active plan.
- The change would introduce scripts, installed hooks, daemons, watchers, package dependencies, or CI/CD workflows.
- A security, AI, or planning rule conflict is detected.

## pre-commit

### Trigger

Before creating a commit or finalizing a documented change set.

### Required Checks

- [ ] Every modified versioned file is covered by the active plan.
- [ ] A changelog fragment exists for the change.
- [ ] `FILESYSTEM.md` is updated when files were added, moved, or removed.
- [ ] Internal links added or changed resolve to existing files.
- [ ] No secrets, credentials, tokens, private paths, or sensitive logs are included.
- [ ] Required validation evidence is recorded.

### Blocking Conditions

- Missing changelog fragment.
- Filesystem drift.
- Secret-like value detected.
- Broken mandatory internal reference.

## commit-msg

### Trigger

Before accepting a commit message.

### Required Checks

- [ ] Use `skills/git-conventional-commits/SKILL.md` when commit formatting is in scope.
- [ ] The message reflects the plan scope.
- [ ] The message does not claim validations that were not executed.

## pre-push

### Trigger

Before pushing a branch or opening a PR.

### Required Checks

- [ ] Active plan contains validation evidence.
- [ ] PR description can reference the plan, risk, validation, and rollback.
- [ ] No unresolved R4/R5 gate exists without required approval.
- [ ] No unplanned scope expansion remains.

## pre-release

### Trigger

Before publishing a release or consolidating changelogs.

### Required Checks

- [ ] Load `skills/release-checklist/SKILL.md`.
- [ ] Load `skills/governance-validator/SKILL.md` if structural consistency is in scope.
- [ ] Load `skills/wiki-lint/SKILL.md` if wiki synthesis, release notes, or knowledge promotion changed.
- [ ] Confirm version coherence across official documents.
- [ ] Confirm release synthesis coverage.

## post-release

### Trigger

After a release is published or documented.

### Required Checks

- [ ] Create or update the release synthesis under `FCVW/wiki/releases/`.
- [ ] Record reusable learnings in the wiki when applicable.
- [ ] Update `wiki/log.md` if wiki content changed.
- [ ] Confirm no plan remains incorrectly marked `in_progress`.

## Evidence

Evidence should be recorded in the active plan and, when applicable, in changelogs, audits, wiki logs, troubleshooting records, or PR descriptions.

## SantanderAI Inspiration Credit

The pseudo-hook and stop-condition framing is conceptually inspired by loop and control patterns from the public SantanderAI organization at `https://github.com/SantanderAI`, especially `SantanderAI/ralph`. No code is copied.
