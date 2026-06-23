---
name: "wiki-lint"
version: "1.0.1"
trigger_keywords: ["wiki lint", "lint wiki", "wiki check", "orphan pages", "broken links", "wiki validation", "wiki audit", "wiki frontmatter"]
session_types: ["document_audit", "release", "wiki_maintenance"]
---

# SKILL: Wiki Lint

High-density operational checklist for validating the structural integrity of the `wiki/` directory in a FrameCode VibeWork project. Condenses the 15-section `wiki/schema.md` lint procedure into an actionable execution guide.

## Activation Triggers

Load this skill (with `view_file` and `IsSkillFile: true`) when the task involves:
- Publishing a minor or major version
- Running a post-audit or post-release wiki consolidation
- Detecting a contradiction between wiki pages or official documents
- User explicitly requests "wiki lint", "wiki audit", or "wiki check"
- Adding 3 or more new wiki pages in a single session
- Adding or changing declarative automation contracts that may produce reusable knowledge

## 1. Pre-Lint Context Load

Before starting the lint, read:
1. `wiki/index.md` — current page map
2. `wiki/log.md` — recent events
3. Directory listing of all `wiki/` subfolders

Do NOT read individual wiki pages unless a specific anomaly requires investigation.

## 2. Structural Checks

### 2.1 Mandatory Frontmatter

Every file in `wiki/` **except** `README.md`, `schema.md`, `index.md`, `log.md`, and folder-internal READMEs must have YAML frontmatter with all these fields:

```yaml
---
title: "..."
type: "concept | decision | pattern | failure | refactoring | audit | agent | release | session | component | prompt | question | synthesis | source | raw"
status: "draft | in_validation | validated | obsolete | superseded | contradictory"
confidence: "low | medium | high"
last_reviewed: "YYYY-MM-DD"
related_version: "Vx.y.z"
sources:
  - "<source>"
tags:
  - "<tag>"
---
```

**Check:** Open each non-exempt file; flag any missing or malformed field.

### 2.2 Orphan Pages

A page is orphaned if it has zero incoming links from:
- `wiki/index.md`, OR
- another wiki page via `[[wikilink]]`

**Check:** For each wiki page, search for its filename or wikilink in `wiki/index.md` and other pages. Flag pages with no incoming references.

**Resolution:** Either add a link in `wiki/index.md` or mark as `status: obsolete`.

### 2.3 Broken Internal Links

**Check:** For each `[[Target]]` or `[[folder/target]]` link found in any wiki page, verify that the target file physically exists in `wiki/`.

**Resolution:** Fix the link path or create the missing target page.

### 2.4 Index Coverage

**Check:** For each thematic section in `wiki/index.md` (Validated Patterns, Known Failures, etc.), verify that listed pages actually exist. Remove dead entries.

### 2.5 Status Accuracy

**Check:** Pages with `status: validated` should have `confidence: medium` or `high`. Pages with `confidence: low` should not have `status: validated`. Flag mismatches.

### 2.6 Stale Knowledge

**Check:** Pages with `last_reviewed` older than 90 days that describe system behavior should be reviewed. Flag for human review, do not auto-change status.

## 3. Knowledge Gap Checks

### 3.1 Completed Plans Without Wiki Promotion

For each file in `Plans/completed/`, check if the plan generated reusable knowledge that has not been promoted. Criteria (from `wiki/schema.md §6`):
- Does the plan describe a pattern that can be reapplied? → `wiki/patterns/`
- Did the plan resolve a failure that could recur? → `wiki/failures/`
- Did the plan introduce an architectural decision? → `wiki/decisions/`

### 3.2 Changelogs Without Release Synthesis

For each file in `changelogs/`, check if a corresponding `wiki/releases/v{x}-{y}-{z}.md` exists.

### 3.3 ADRs Without Wiki Page

For each file in `decisions/`, check if a corresponding page exists in `wiki/decisions/`.

### 3.4 Unresolved Questions

Review `wiki/questions/` for pages with `status: draft` older than 30 days. Flag for follow-up.

### 3.5 Declarative Automation Knowledge Gaps

When `AUTOMATION.md`, `HOOKS.md`, `WATCHERS.md`, `DAEMONS.md`, `GOVERNANCE_GATES.md`, or their templates change, check whether the change generated reusable knowledge that should be promoted to:

- `wiki/patterns/` — reusable Markdown-only maintenance patterns;
- `wiki/decisions/` — automation boundary or governance decisions;
- `wiki/refactorings/` — governance refactoring patterns;
- `wiki/failures/` — recurring mistakes avoided by hooks/watchers/gates.

If the change credits an external reference such as `https://github.com/SantanderAI`, verify whether a `wiki/sources/` note is appropriate. Credit must remain conceptual unless copied material is explicitly licensed and documented.

## 4. Lint Report Format

Record the lint result in `wiki/log.md` using:

```markdown
## [YYYY-MM-DD HH:MM] lint | Wiki Structural Lint

- Source: Manual lint execution (trigger: <trigger reason>)
- Executed action: Full structural validation per wiki/schema.md §12
- Checks performed: frontmatter, orphans, broken links, index coverage, status accuracy, knowledge gaps
- Findings:
  - Orphan pages: <list or "none">
  - Broken links: <list or "none">
  - Missing frontmatter: <list or "none">
  - Status mismatches: <list or "none">
  - Knowledge gaps: <list or "none">
- Pages created: <list or "none">
- Pages updated: <list or "none">
- Pages obsoleted: <list or "none">
- Result: <clean / issues found and resolved / issues found, pending resolution>
- Gaps: <remaining items requiring human review>
```

## 5. Post-Lint Actions

- [ ] Update `wiki/index.md` if any page changed status or was added/removed
- [ ] Record lint event in `wiki/log.md` (use format above)
- [ ] If breaking issues found, create troubleshooting record before closing
- [ ] If knowledge gap found, promote to wiki before session ends
