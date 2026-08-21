---
schema: "fcvw/audit@1"
id: "AUD-20260821-typed-wiki-skills"
artifact_role: "record"
owner: "framework"
upgrade_strategy: "preserve"
record_scope: "framework"
retrieval_scope: "search_only"
status: "completed"
created_at: "2026-08-21"
last_reviewed: "2026-08-21"
sources:
  - "FCVW/wiki/schema.md"
  - "FCVW/skills/wiki-curator/SKILL.md"
  - "FCVW/skills/wiki-lint/SKILL.md"
---

# Skill or Agent Self-Improvement: wiki-curator and wiki-lint

## Scope

Review and update only the existing wiki curation and lint skills after typed relations, source digests, derived stale findings, and optional semantic review became canonical framework behavior.

## Authoritative sources

- [Wiki schema](../wiki/schema.md)
- [AI policy](../AI.md)
- [Completed implementation plan](../Plans/completed/P2-R4-2026-08-21-plan-dependencies-and-typed-knowledge.md)

## Method

Apply `self-improvement` using canonical-rule drift as evidence, preserve existing triggers and responsibilities, patch only the affected procedure and non-responsibilities, and replay the skill-contract validator plus focused policy assertions.

## Findings

### Evidence

- Assets changed: `wiki-curator` and `wiki-lint`.
- Drift: neither skill covered typed relation targets, generated inverses, tracked source digests, dependent stale review, or the boundary between deterministic and semantic lint.
- Severity: P2 plan scope because silent digest refresh or semantic mutation could invalidate technical memory.

### Improvement metrics

| Metric | Required threshold | Evidence | Pass |
|---|---|---|---|
| Rule drift | Canonical rule changed | `wiki/schema.md` now defines typed/provenance behavior | yes |
| Validation gap | Existing exit criteria missed a defect | No source-impact or semantic non-mutation check existed | yes |
| Scope preservation | Narrows or clarifies scope | Existing curation/lint ownership retained | yes |
| Backward compatibility | Valid triggers/outputs remain valid | Names, triggers, modes, and required outputs retained | yes |

### Change summary

- `wiki-curator` now reviews typed edges and changed-source dependents without broad loading or automatic digest refresh.
- `wiki-lint` now validates deterministic semantic structure and defines an optional, source-bounded, review-only semantic layer.
- No new skill, provider adapter, trigger, or catch-all responsibility was introduced.

## Validation

The focused skill-contract assertion passed with the full 87-test suite. The clean-template validator reported errors=0 and findings=0; both generated graph checks reported zero findings, and all 14 Python tools parsed successfully.

## Limitations and residual risk

The clean framework has no production wiki corpus, so semantic precision and token cost are not claimed. Semantic review remains non-blocking until downstream measurements justify a stronger gate.

## Follow-up

Revisit only after measured false positives, missed stale dependencies, or excessive source-bounded token cost provide evidence for another bounded patch.
