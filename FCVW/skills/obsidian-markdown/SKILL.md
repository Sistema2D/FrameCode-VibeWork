---
schema: "fcvw/skill@1"
name: "obsidian-markdown"
description: "Format portable Markdown and optional Obsidian-compatible links."
version: "1.2.0"
trigger_keywords:
  - "obsidian"
  - "wikilink"
  - "frontmatter"
  - "markdown note"
session_types:
  - "wiki_maintenance"
  - "documentation"
---

# Obsidian-compatible Markdown

## Purpose

Create or normalize Markdown that remains valid under FCVW schemas while adding Obsidian-specific navigation only when the project uses it.

## Use conditions

Use when the user requests Obsidian formatting, wikilinks, embeds, callouts, note properties, or graph-oriented wiki maintenance. Ordinary FCVW documentation uses portable Markdown by default.

## Inputs

Target note, `wiki/schema.md`, taxonomy, source links, destination, current canonical page, and the project's decision on supported Obsidian syntax.

## Non-responsibilities

- inventing sources, confidence, status, tags, or relationships;
- replacing FCVW frontmatter with a second tool-specific metadata block;
- converting all Markdown to wikilinks without retrieval value;
- embedding secrets, private files, or unstable absolute paths;
- rewriting unrelated historical notes.

## Procedure

1. Select the applicable FCVW schema and preserve one YAML frontmatter block at the file start.
2. Check for an existing canonical page before creating a note.
3. Preserve sources, status, confidence, and semantic meaning.
4. Use ordinary Markdown links for portable repository navigation; add `[[wikilinks]]` only when Obsidian resolution is configured and useful.
5. Add embeds, callouts, highlights, or Mermaid only when they materially improve retrieval or comprehension.
6. Validate link targets, heading hierarchy, frontmatter, placeholders, and rendering in the supported mode.

## Formatting rules

- FCVW schema values and controlled statuses come from `wiki/schema.md`; this skill does not define competing values.
- A note has one H1 and a logical heading hierarchy.
- Internal wikilinks use the vault-relative note path or canonical title consistently.
- Embeds use `![[note]]` or `![[note#heading]]` only for stable reusable content.
- Obsidian callouts use a supported type and retain readable quoted content in ordinary Markdown renderers.
- Mermaid nodes must not contain sensitive values; clickable node behavior is optional and project-configured.

## Required output

Changed note paths, schema used, links/embeds added, sources preserved, Obsidian-only features, and validation limitations.

## Validation and exit

Exit when frontmatter matches FCVW, links resolve in the declared mode, no duplicate canonical page or placeholder remains, portable readers retain the essential content, and any Obsidian-only dependency is explicit.
