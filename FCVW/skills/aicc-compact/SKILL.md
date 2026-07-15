---
schema: "fcvw/skill@1"
name: "aicc-compact"
description: "Create a bounded session handoff with collision-resistant identity."
version: "1.1.1"
trigger_keywords:
  - "compact session"
  - "close session"
  - "handoff"
  - "síntese de sessão"
session_types:
  - "handoff"
  - "maintenance"
---

# Session compaction

## Purpose

Capture only the state required to continue work without replaying the full conversation.

## Use when

- an active governed batch is handed to another session or agent;
- work stops with meaningful unresolved state;
- a completed batch produced reusable operational context.

Do not create a session file for a trivial read-only exchange or duplicate information already canonical elsewhere.

## Identity

Use `id: SES-YYYYMMDD-HHMMSS-<short-id>`. The short ID may be a commit prefix or random hexadecimal token. Never derive uniqueness only from “highest session number + 1”.

Suggested filename: `YYYYMMDD-HHMMSS-<short-id>-<slug>.md`.

## Inputs

- active plan and its current state;
- actual modified files;
- validation evidence;
- open risks and next authorized action.

## Non-responsibilities

- copying full files or chat transcripts into the handoff;
- inventing commit, test, publication, or completion evidence;
- treating the newest or highest sequence as relevant without checking scope;
- deleting older sessions as part of compaction.

## Procedure

1. Verify actual workspace and plan state.
2. Create the page from `wiki/templates/TEMPLATE_SESSION_SYNTHESIS.md`.
3. Link canonical files rather than copying their contents.
4. Record decisions, failures, validation, unresolved risks, and next step.
5. Add index/log entry only when the session is useful for future retrieval.
6. Check ID uniqueness.

## Required output

A concise, sourced handoff that distinguishes completed work, active work, blocked work, and optional next steps.

## Validation and exit

- unique ID;
- no secrets or private runtime data;
- links resolve;
- plan/status matches disk state;
- no unsupported claim of commit, tag, test, or publication.
