---
title: "Release Synthesis V0.8.0 — Governance Gaps Closure"
type: "release"
status: "validated"
confidence: "high"
last_reviewed: "2026-06-11"
related_version: "V0.8.0"
sources:
  - "changelogs/unreleased/P1-R4-2026-06-11-service-research-mandate.md"
  - "changelogs/unreleased/P2-R3-2026-06-11-pr-branch-workflow.md"
  - "changelogs/unreleased/P2-R3-2026-06-11-environment-promotion-workflow.md"
  - "changelogs/unreleased/P2-R4-2026-06-11-multi-agent-concurrency.md"
  - "FCVW/skills/governance-validator/SKILL.md"
  - "FCVW/MANIFEST.md"
tags:
  - "release"
  - "governance"
  - "V0.8.0"
  - "gap-closure"
  - "structural-audit"
---

# Release Synthesis V0.8.0 — Governance Gaps Closure

## Version Summary

This release closes four governance gaps identified during hypothesis testing, consolidates all plans from the session into authoritative `completed/` versions, and reconciles stale file state across the Plans directory. All changes are document-only (pure Markdown, no scripts), consistent with ADR-0001.

---

## Main Changes

### 1. GAP-1.3 — Service Research Mandate (`P1-R4`)

| File | Change |
|---|---|
| **`AGENTS.md`** | New "Third-Party Services" operational rule + Initial Checklist item referencing `FCVW/AI.md §Third-Party Service Research` |
| **`FCVW/AI.md`** | New "Third-Party Service Research" section: mandatory research via Gravity Index, prohibited behaviors (no memory-based recommendation), integration protocol with Secret Handshake, exceptions (auth, hosting infra, skill-loading steps) |

**Impact**: Prevents AI agents from recommending outdated or incompatible third-party services from training memory alone.

### 2. GAP-2.2 — PR / Branch / Code Review Workflow (`P2-R3`)

| File | Change |
|---|---|
| **`AGENTS.md`** | New "Code Review / Pull Requests" operational rule + dedicated section: branch naming convention (`<type>/<scope>-<short-description>`), 6-step PR workflow, code review standards by risk level (R1–R5), cross-reference to `refactoring-guide/17-branch-and-pull-request-policy.md`. Item added to Checklist Before Finishing a Change. |
| **`FCVW/CONTEXT_MAP.md`** | New "Pull Request / Code Review" session type row in Session Type Reference Table |

**Impact**: Connects the previously invisible refactoring PR policy to the main governance entry points.

### 3. GAP-3.2 — Environment Promotion Workflow (`P2-R3`)

| File | Change |
|---|---|
| **`FCVW/ENVIRONMENT.md`** | New §5 "Environment Promotion Workflow": environment roles table (Dev/Staging/Prod), promotion gates (Dev→Staging: 6 conditions; Staging→Production: 6 conditions), rollback during promotion (5 steps), single-environment fallback. Frontmatter updated, section numbering re-indexed. |
| **`FCVW/RELEASE.md`** | Release states expanded to include `in_staging` and `in_production`. New "Deployment and Environment Promotion" section: 7-step promotion workflow, deploy rollback procedure, single-environment fallback. |
| **`FCVW/CONTEXT_MAP.md`** | New "Deploy / Environment Promotion" session type row |

**Impact**: Connects releases to deployment with defined validation gates and rollback procedures.

### 4. GAP-5.1 — Multi-Agent Concurrency Protocol (`P2-R4`)

| File | Change |
|---|---|
| **`AGENTS.md`** | New "Multi-Agent Concurrency" operational rule + dedicated section: plan-based signaling (soft lock via `Plans/in_progress/`), pre-work coordination check (3 overlap levels: low/medium/high), agent journals as coordination channels, scope locking convention (context_files frontmatter), conflict resolution (6 steps), branch isolation guidance. Items added to Initial Checklist and Checklist Before Finishing a Change. |
| **`FCVW/CONTEXT_MAP.md`** | New "Multi-Agent / Collaboration" session type row |

**Impact**: Enables safe concurrent work by multiple agents on the same project with Markdown-only signaling.

### 5. Plan Consolidation Audit

| Action | Detail |
|---|---|
| **Audited** | All 15 plan files across `pending/`, `in_progress/`, `completed/` |
| **Created** | 3 authoritative `completed/` versions (pr-branch, environments, multi-agent) |
| **Marked stale** | 7 obsolete copies (4 in `pending/`, 3 in `in_progress/`) — all set to `Status: superseded` with pointers to `completed/` |
| **Padronized** | P1-R4-service-research completed plan updated from "Known Residual Issues" to "Stale Files" format |
| **Updated** | `MANIFEST.md §14` with 4 new entries for all plans |

**Stale file convention established**: Each completed plan now has a `Stale Files` section listing where duplicate copies remain, preventing agent confusion.

---

## Relevant Decisions

- **No FILESYSTEM.md update needed**: `governance-validator/SKILL.md` was already present in the visual tree from a previous cycle — confirmed by glob comparison (16 SKILL.md on disk, all 16 in tree).
- **Single-environment fallback** documented for all promotion workflows to accommodate solo developers without staging/production separation.
- **CI/CD out of scope**: PR merge rule says "automated tests or validations fail (or have not been run)" — aligned with ADR-0001.
- **Soft lock, not hard lock**: Multi-agent coordination uses convention-based signaling (`Plans/in_progress/` presence), not file locks or scripts.

---

## Patterns Created or Reinforced

| Pattern | Where Defined | Status |
|---|---|---|
| **Gap hypothesis → Plan → Implementation → Review → Completion** | Full session | Reinforced as canonical workflow |
| **Stale file superseded status** | `Plans/completed/` (all plans) | Created — each completed plan has `Stale Files` section |
| **Plan-based signaling for concurrency** | `AGENTS.md §Multi-Agent Concurrency` | Created |
| **Cross-reference to refactoring policy** | `AGENTS.md §Code Review and Pull Requests` → `refactoring-guide/17-branch-and-pull-request-policy.md` | Created |
| **Service research via Gravity Index** | `FCVW/AI.md §Third-Party Service Research` | Created |

---

## Fixed Failures

| Failure | Gap | Resolution |
|---|---|---|
| Agents could recommend services from training memory | GAP-1.3 | Added mandatory research rule + Gravity Index protocol |
| Framework had no PR/branch workflow in governance entry points | GAP-2.2 | Added PR section + review standards by risk |
| Environments had no promotion workflow between them | GAP-3.2 | Added promotion gates + rollback in ENVIRONMENT.md and RELEASE.md |
| Framework assumed single-agent operation | GAP-5.1 | Added multi-agent coordination protocol |
| Duplicate plan files across directories with conflicting statuses | Plan audit | All stale files marked `superseded`; authoritative versions in `completed/` |
| FILESYSTEM.md not verified for governance-validator presence | User request | Confirmed already correct |

---

## Refactorings Executed

- **AGENTS.md**: 3 new operational rules + 3 new dedicated sections + 3 checklist items
- **FCVW/ENVIRONMENT.md**: §5 inserted, §6→§6/§7 renumbered, frontmatter updated
- **FCVW/RELEASE.md**: Release states expanded + new deployment section
- **FCVW/CONTEXT_MAP.md**: 3 new session type rows
- **FCVW/AI.md**: New "Third-Party Service Research" section
- **MANIFEST.md §14**: 4 new entries in Manifest Update History

---

## Related Audits

- **Plan consistency audit**: All 15 plan files mapped, 7 stale copies identified and marked
- **FILESYSTEM.md verification**: Confirmed governance-validator/SKILL.md already in tree
- **Code review cycles**: 4 plans reviewed in 12 total review rounds (3 per plan), all resolved

---

## Known Gaps / Open Items

| Gap | Impact | Suggested Action |
|---|---|---|
| Stale files in `pending/` and `in_progress/` remain on disk | Low — they're marked `superseded` but could still be read by agents not checking status | Future cleanup: delete or physically reorganize |
| No automated validation for stale file detection | Low — manual audit caught all cases this session | Consider adding to governance-validator skill |
| `CONTEXT_MAP.md` Multi-Agent session type references `AGENTS.md §checklist` but checklist doesn't mention environment promotion explicitly | Minimal — an agent can still discover the protocol via the dedicated section | Minor refinement in next pass |
| Release states order requires changelog publication *after* production deploy | Design choice — rigid for some workflows | Revisit in next release if needed |

---

## Reusable Learnings

1. **Plan auditing is now part of the closure checklist**: The `Checklist Before Finishing a Change` now asks about releasing the soft lock (moving plan to `completed/`). This prevents stale file accumulation in future sessions.
2. **Session pattern for gap closure**: Hypothesis → gap identification → plan → implementation → review cycles → plan consolidation → release summary. This is now the canonical pattern for structural improvements.
3. **Soft lock via directory convention**: `Plans/in_progress/` acts as a signaling channel without requiring git hooks or scripts — viable for any Markdown-governed project.
4. **Stale file convention**: Setting `Status: superseded` with a pointer to the authoritative version is a minimal-effort pattern for managing file duplication when tools cannot delete files.

---

## Next Recommendations

- Configure the `governance-validator` skill as a pre-merge step for all P1–P2 plans to prevent governance document decay
- Review whether the `FILESYSTEM.md` visual tree should include stale file notes in comments (e.g., `# superseded — see completed/`)
- Consider consolidating the 4 open changelog fragments in `changelogs/unreleased/` into a single `V0.9.0` release
