# Template: skill or agent change

Use the proposal section with `agent-factory` for a new skill or agent, and the report section with `self-improvement` for a change to an existing one. Either is saved as a wiki note with the [note envelope](TEMPLATE_NOTE.md), `type: "audit"`, and the `agent-factory` or `self-improvement` tag.

## Agent or Skill Proposal: <Asset Name>

### 1. Problem Evidence

- Request or failure:
- Occurrence count:
- Related plans/sessions/troubleshooting:
- Priority/risk:

### 2. Existing Coverage Check

| Existing asset | Coverage estimate | Gap |
|---|---:|---|
| `<document-or-skill>` | `<0-100%>` | `<missing procedure>` |

### 3. Creation Metrics

| Metric | Required threshold | Evidence | Pass |
|---|---|---|---|
| Recurrence | `>=2 occurrences` or `1 P1/P2 blocker` |  |  |
| Coverage gap | Existing assets cover `<70%` |  |  |
| Token ROI | `>=20%` initial-context reduction or avoids `500+` base-doc words |  |  |
| Risk ROI | Reduces recurrent failure or high-risk gap |  |  |
| Scope narrowness | One trigger family, one output, one validation path |  |  |
| Validation path | Replayable against one real task |  |  |

### 4. Asset Decision

- Decision: `inline checklist` / `template` / `skill` / `agent profile` / `defer`
- Proposed path:
- Responsibility:
- Non-responsibilities:
- Trigger keywords:
- Primary output:
- Validation task:

### 5. Catalog and Handoff Updates

- [ ] `skills/README.md` updated when a skill/profile is created.
- [ ] `CONTEXT_MAP.md` updated when the asset affects session routing.
- [ ] `PROJECT.md` (stack) updated when the active skill catalog changes.
- [ ] `AGENTS.md` updated only if the behavior must be base-loaded.
- [ ] Changelog and active plan cite the proposal.

### 6. Residual Risk

- Risks:
- Deferred alternatives:
- Next review trigger:

## Skill or Agent Self-Improvement: <Asset Name>

### 1. Evidence

- Asset changed:
- Failure, drift, or inefficiency:
- Related plans/sessions/troubleshooting:
- Severity:

### 2. Improvement Metrics

| Metric | Required threshold | Evidence | Pass |
|---|---|---|---|
| Failure evidence | `>=2` failures/ambiguities or `1 P1/P2` incident |  |  |
| Rule drift | Canonical rule changed or contradiction found |  |  |
| Validation gap | Existing exit criteria missed a defect |  |  |
| Token ROI | `>=15%` reduction or removes repeated clarifications |  |  |
| Scope preservation | Narrows or clarifies scope |  |  |
| Backward compatibility | Valid triggers/outputs remain valid |  |  |

### 3. Change Summary

- Before:
- After:
- Sections changed:
- Trigger changes:
- Non-responsibility changes:

### 4. Validation Replay

- Replay task:
- Expected behavior:
- Observed behavior:
- Remaining limitation:

### 5. Catalog and Traceability

- [ ] `skills/README.md` updated if trigger, name, or summary changed.
- [ ] `CONTEXT_MAP.md` updated if routing changed.
- [ ] `PROJECT.md` (stack) updated if active catalog changed.
- [ ] Changelog and active plan cite the report.
- [ ] Session synthesis records invoked skills and next review trigger.
