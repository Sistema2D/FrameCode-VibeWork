---
title: "Agent Skill Self-Improvement Governance"
type: "pattern"
status: "validated"
confidence: "high"
last_reviewed: "2026-06-13"
related_version: "V0.10.0"
tags:
  - "agent-factory"
  - "self-improvement"
  - "skills"
  - "token-efficiency"
---

# Agent Skill Self-Improvement Governance

## Problem

AI agents can overcorrect framework gaps by creating redundant skills, persona-only agents, or broad instructions that inflate context and produce inconsistent behavior.

## Pattern

Treat skills and agent profiles as governed assets:

- create them only when recurrence, coverage gap, token/risk ROI, scope, and validation metrics pass;
- improve them only when failure, drift, validation gap, or meaningful token/risk savings are evidenced;
- prefer inline checklist or template before creating a new skill;
- prefer skill before agent profile unless a bounded role with handoff is required;
- block style-only, naming-only, and catch-all agent changes.

## Operational Assets

- `skills/agent-factory/SKILL.md`
- `skills/self-improvement/SKILL.md`
- `governance/TEMPLATE_AGENT_OR_SKILL_PROPOSAL.md`
- `governance/TEMPLATE_SELF_IMPROVEMENT_REPORT.md`

## Reuse Rule

When a future project reports repeated hallucinations, context loss, monolith creation, duplication, or unsafe cleanup, first check whether an existing FCVW skill covers the procedure. Create or modify skills only after the metric gates pass.
