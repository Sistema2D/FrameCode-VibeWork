# LLM Wiki Schema

This file defines the structural, semantic, and operational rules of the project's wiki.

The wiki must be maintained in Markdown readable by humans and AI agents. Its goal is to preserve accumulated technical knowledge, reduce rework, avoid repeating failures, and improve future decisions.

---

## 1. Mandatory Structure

```text
wiki/
├── README.md
├── schema.md
├── index.md
├── log.md
├── inbox/
├── raw/
├── sources/
├── concepts/
├── decisions/
├── patterns/
├── failures/
├── refactorings/
├── audits/
├── agents/
├── releases/
├── components/
├── prompts/
├── questions/
├── syntheses/
└── templates/
```

---

## 2. Page Categories

### Basic Structure of a File

All wiki files must start with a YAML metadata block to allow advanced indexing and visualization, except for files explicitly exempted in the frontmatter section.

Use the minimum template defined in the **Mandatory Frontmatter** section. Do not mix equivalent fields in different languages, such as mixing English and Portuguese fields, or mixing status values in different languages.

### Naming and Folders

| Category | Folder | Purpose |
|---|---|---|
| Inbox | `inbox/` | Temporary inputs not yet analyzed |
| Raw | `raw/` | Preserved raw sources, preferably immutable |
| Sources | `sources/` | Description or normalization of relevant sources |
| Concepts | `concepts/` | Technical, product, or process concepts |
| Decisions | `decisions/` | Consolidated architectural decisions |
| Patterns | `patterns/` | Validated and reusable patterns |
| Failures | `failures/` | Recurring failures, root causes, and solutions |
| Refactorings | `refactorings/` | Opportunities, learnings, and refactoring criteria |
| Audits | `audits/` | Recurring findings and patterns derived from reports in `audits/` |
| Agents | `agents/` | Agent-specific journals named `<agent_name>_journal.md` |
| Releases | `releases/` | Syntheses of published versions |
| Components | `components/` | Modules, screens, services, and responsibilities |
| Prompts | `prompts/` | Useful, tested, or recommended prompts |
| Questions | `questions/` | Open questions and hypotheses to investigate |
| Syntheses | `syntheses/` | Cross-cutting syntheses between multiple sources |

---

## 3. Mandatory Frontmatter

Every knowledge page, except `README.md`, `schema.md`, `index.md`, `log.md`, and folder-internal READMEs, must start with YAML frontmatter.

Minimum template:

```yaml
---
title: "<page title>"
type: "concept | decision | pattern | failure | refactoring | audit | agent | release | component | prompt | question | synthesis | source | raw"
status: "draft | in_validation | validated | obsolete | superseded | contradictory"
confidence: "low | medium | high"
last_reviewed: "YYYY-MM-DD"
related_version: "V0.0.0"
sources:
  - "<source path or reference>"
tags:
  - "<tag>"
---
```

---

## 4. Allowed Statuses

### `draft`

Page created, but still incomplete or unvalidated.

### `in_validation`

Page awaiting review, test, audit, or confirmation.

### `validated`

Checked knowledge, with sufficient sources and evidence.

### `obsolete`

Old knowledge that should no longer be used as a primary reference.

### `superseded`

Knowledge replaced by another page or later decision.

### `contradictory`

Knowledge in conflict with another source or evidence. Requires investigation.

---

## 5. Confidence Levels

### `low`

Use when the page contains an initial hypothesis, unconfirmed observation, or inference.

### `medium`

Use when there are indications, but full validation is still lacking.

### `high`

Use when there is sufficient source, validation, test, audit, or confirmation.

---

## 6. Promotion Rule for Knowledge

Not every record should become a wiki page.

Content should be promoted to the wiki when it meets at least one criterion:

- The failure can occur again.
- The solution can be reapplied.
- The decision affects architecture, stack, security, data, or UX.
- The audit revealed a recurring pattern.
- The refactoring created reusable learning.
- The prompt can be reused.
- The open question guides future decisions.
- The synthesis reduces rework in next interactions.
- The knowledge improves the AI's ability to act in the project.

Pontuais, trivial, or non-reusable content should remain only in original records.

---

## 7. Sources Rule

Every interpretative page must point to its sources.

Sources can be:

- files in `Plans/`;
- files in `changelogs/`;
- files in `troubleshooting/`;
- files in `audits/`;
- ADRs in `decisions/`;
- project official documents;
- technical logs;
- code snippets;
- relevant prompts;
- consolidated answers;
- raw files in `wiki/raw/`.

If the source is not available, record:

```text
Source not available. Page based on contextual synthesis.
```

---

## 8. Internal Links

Use Obsidian-style links when possible:

```markdown
[[patterns/atomic-writing-pattern]]
[[failures/reproduction-error-example]]
[[decisions/stack-choice-example]]
```

Whenever a page cites another existing concept, failure, decision, or pattern, it must create an internal link to it.

---

## 9. Rules for `raw/`

The `raw/` folder stores raw sources.

Rules:

- do not alter raw content without explicit justification;
- prefer adding a new version over overwriting;
- record origin, date, and context;
- do not store secrets, tokens, passwords, or unnecessary sensitive data;
- when there is sensitive data, anonymize it before recording.

---

## 10. Rules for `agents/`

The `agents/` folder stores agent-specific journals.

Rules:

- use `agents/<agent_name>_journal.md`;
- keep one predictable journal per agent;
- append entries rather than overwriting;
- record durable project-specific learnings, not routine execution narration;
- do not store secrets, tokens, private logs, or unnecessary personal data;
- promote reusable knowledge to the proper wiki category and link back to the journal source.

---

## 11. Rules for `index.md`

The `index.md` file must function as a navigable map of the wiki.

It must contain:

- most important pages;
- validated patterns;
- recurring failures;
- main decisions;
- relevant refactorings;
- audits with learnings;
- releases;
- open questions;
- important obsolete pages.

The index must be updated whenever a new relevant page is created or when a page changes status.

---

## 12. Rules for `log.md`

The `log.md` file must record chronological wiki events.

Record events such as:

- source ingestion;
- page creation;
- synthesis update;
- wiki linting;
- identified contradiction;
- knowledge promotion;
- obsolescence marking;
- post-release consolidation;
- post-troubleshooting learning;
- post-audit learning.

---

## 13. Wiki Linting

The AI must execute or recommend a wiki lint when there is:

1. publication of a minor or major version;
2. a resolved recurring failure;
3. a failed audit;
4. structural refactoring;
5. inclusion of multiple new sources;
6. contradiction between official documents;
7. explicit user request.

The lint must verify:

- orphan pages;
- broken links;
- concepts cited without a page;
- resolved failures without a synthesis;
- completed plans without extracted learning;
- changelogs without a release synthesis;
- ADRs without a page in `decisions/`;
- old pages with incorrect status;
- contradictions between sources;
- lack of update in `index.md`;
- lack of record in `log.md`.

---

## 14. Contradictions Policy

When a new source contradicts an existing page:

1. Do not delete the old page without justification.
2. Mark the old page as `contradictory`, `obsolete`, or `superseded`, as appropriate.
3. Record the contradiction on the page itself.
4. Create or update a synthesis in `syntheses/`, if necessary.
5. Record the event in `log.md`.
6. Indicate which source should prevail and why.

---

## 15. Obsolescence Policy

When a page no longer represents the current state:

- change `status` to `obsolete` or `superseded`;
- indicate a replacement page, if any;
- record the review date;
- update `index.md`, if the page is listed;
- record in `log.md`.

---

## 16. Use by AI Agents

The wiki implements three main operations: **Ingest**, **Query**, and **Lint**. Consult the corresponding section for each situation.

Before executing relevant actions, the AI must consult:

1. `AGENTS.md`;
2. `MANIFEST.md`;
3. `wiki/index.md`;
4. wiki pages related to the topic;
5. corresponding official documents.

After executing an action that generates reusable learning, the AI must evaluate whether to update the wiki.

The AI must not claim it has consulted, validated, or updated the wiki if this has not been done.

---

## 17. Query Operation

Query is the flow of answering questions using the wiki as a primary source before resorting to external search or model influence.

### Workflow

1. Read `wiki/index.md` to identify pages relevant to the topic.
2. Read the identified pages, prioritizing `status: validated` and `confidence: high`.
3. Synthesize the response with citations to the wiki sources.
4. Evaluate if the response deserves to be promoted as a new page or page update.

### Rules

- High-quality or reusable responses must be archived in `wiki/syntheses/`.
- Every promoted response must have frontmatter with `type: synthesis` and point to the original question or source.
- Pages with `status: draft` or `confidence: low` must be used with caution, and cite this limitation.
- Open questions that cannot be answered with available sources must go to `wiki/questions/`.
- Record the query event in `log.md` when it generates a new page or updates an existing one.
- Do not fabricate information when the wiki lacks sufficient source; explicitly state the gap.
