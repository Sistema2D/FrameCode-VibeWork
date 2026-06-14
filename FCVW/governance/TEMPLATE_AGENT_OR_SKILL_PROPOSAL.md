---
title: "Agent or Skill Proposal: <asset-name>"
type: "proposal"
status: "draft"
confidence: "medium"
last_reviewed: "YYYY-MM-DD"
related_version: "Vx.y.z"
tags:
  - "agent-factory"
  - "skills"
---

# Agent or Skill Proposal: <Asset Name>

## 1. Problem Evidence

- Request or failure:
- Occurrence count:
- Related plans/sessions/troubleshooting:
- Priority/risk:

## 2. Existing Coverage Check

| Existing asset | Coverage estimate | Gap |
|---|---:|---|
| `<document-or-skill>` | `<0-100%>` | `<missing procedure>` |

## 3. Creation Metrics

| Metric | Required threshold | Evidence | Pass |
|---|---|---|---|
| Recurrence | `>=2 occurrences` or `1 P1/P2 blocker` |  |  |
| Coverage gap | Existing assets cover `<70%` |  |  |
| Token ROI | `>=20%` initial-context reduction or avoids `500+` base-doc words |  |  |
| Risk ROI | Reduces recurrent failure or high-risk gap |  |  |
| Scope narrowness | One trigger family, one output, one validation path |  |  |
| Validation path | Replayable against one real task |  |  |

## 4. Asset Decision

- Decision: `inline checklist` / `template` / `skill` / `agent profile` / `defer`
- Proposed path:
- Responsibility:
- Non-responsibilities:
- Trigger keywords:
- Primary output:
- Validation task:

## 5. Catalog and Handoff Updates

- [ ] `skills/README.md` updated when a skill/profile is created.
- [ ] `CONTEXT_MAP.md` updated when the asset affects session routing.
- [ ] `STACK.md` updated when the active skill catalog changes.
- [ ] `AGENTS.md` updated only if the behavior must be base-loaded.
- [ ] Changelog and active plan cite the proposal.

## 6. Residual Risk

- Risks:
- Deferred alternatives:
- Next review trigger:
