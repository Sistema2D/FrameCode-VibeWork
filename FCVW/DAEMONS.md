# Declarative Daemons

## Objective

Define daemon-like maintenance loops as Markdown-only procedures for FrameCode VibeWork.

In Scenario 1, a daemon is not a process. It is a repeatable loop followed by a human or AI agent during a bounded maintenance session.

## Definition

A declarative daemon loop has:

- entry conditions;
- iteration steps;
- stop conditions;
- maximum scope per iteration;
- evidence requirements;
- forbidden behavior.

## FCVW Maintenance Loop

### Entry Conditions

- A maintenance, audit, release, or governance task is requested.
- `AGENTS.md` and `CONTEXT_MAP.md` have been consulted.
- The task is covered by an active plan when files will be modified.

### Iteration Steps

1. Read `AGENTS.md`.
2. Read `FCVW/CONTEXT_MAP.md`.
3. Read the latest relevant `FCVW/wiki/sessions/S*.md` only when session continuity is needed.
4. Check `FCVW/Plans/in_progress/` for overlap.
5. Apply the relevant hook checklist from `HOOKS.md`.
6. Apply the relevant watcher rules from `WATCHERS.md`.
7. Apply the relevant gate from `GOVERNANCE_GATES.md`.
8. Perform one bounded maintenance action.
9. Record evidence in the active plan.
10. Update changelog when any versioned file changed.
11. Stop if a blocking condition is reached.

### Maximum Scope per Iteration

One iteration should cover one bounded action family, such as:

- filesystem consistency;
- plan-state consistency;
- wiki lint;
- release validation;
- skill gate validation;
- security review.

Do not mix unrelated cleanup, feature work, refactoring, and release work in a single daemon iteration.

## Stop Conditions

Stop immediately when:

- no active plan exists for a file modification;
- the requested action exceeds the active plan scope;
- a secret or sensitive value is detected;
- R4/R5 work requires approval that has not been recorded;
- a change would introduce executable automation under Scenario 1;
- a contradiction with ADR-0001, ADR-0002, `SECURITY.md`, or `AI.md` is found;
- the loop would need to run as a real background process;
- validation evidence cannot be produced.

## Forbidden Behavior

A declarative daemon loop must not:

- run in the background;
- install a service;
- create scheduled tasks;
- execute shell commands;
- watch the filesystem with code;
- bypass plan/changelog rules;
- perform destructive actions without confirmation;
- read outside allowed project paths.

## Evidence

Each loop execution should record:

- loop name;
- trigger;
- documents loaded;
- watcher/hook/gate checks applied;
- findings;
- files changed;
- validation result;
- residual risk.

## SantanderAI Inspiration Credit

The loop, stop-condition, and fresh-session framing is conceptually inspired by the public SantanderAI `ralph` repository at `https://github.com/SantanderAI/ralph`. FCVW adapts the idea as a Markdown-only protocol. No code is copied.
