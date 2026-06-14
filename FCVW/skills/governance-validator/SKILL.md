# Governance Validator

*Activation Triggers:* validate governance, verify filesystem, check document integrity, pre-audit check, structural audit

## Purpose

Validate two critical governance invariants using only manual AI-driven inspection — no scripts, no automation. Loaded on-demand before releases, structural audits, or when discrepancies are suspected.

## Validation 1 — FILESYSTEM.md Accuracy

Verify that `FILESYSTEM.md`'s visual tree matches the physical disk state exactly.

### Checklist

- [ ] **Root files**: Confirm `.cursorrules`, `.gitignore`, `.windsurfrules`, `AGENTS.md`, `README.md` exist at project root.
- [ ] **FCVW/ files**: All `.md` files listed under `FCVW/` (e.g., `AI.md`, `SCOPE.md`, `PLANNING.md`) exist. No listed file is missing; no unlisted file is present.
- [ ] **Subdirectory structure**: For every directory in the tree, confirm the subdirectory exists and contains only the files shown. Directories with only a `README.md` must be annotated `(empty baseline)`.
- [ ] **No ghost files**: Every file path in the tree resolves to an actual file. Remove or annotate any that do not.
- [ ] **No omissions**: Every `.md` file physically present under `FCVW/` (excluding `.gitignore`d paths) has a corresponding entry in the tree.

### Correction Protocol

If a discrepancy is found:
1. If the tree lists a file that does not exist, remove the entry or annotate it as `(removed)`.
2. If a file exists but is not in the tree, add it.
3. Update the **last_reviewed** date in FILESYSTEM.md frontmatter.
4. Record the discrepancy and correction in the active plan or changelog.

---

## Validation 2 — Governance Document Integrity

Verify that all governance documents are internally consistent and structurally sound.

### Checklist

#### Frontmatter Integrity

- [ ] Every knowledge page under `wiki/` (except `README.md`, `schema.md`, `index.md`, `log.md`, and folder-internal `README.md`) has valid YAML frontmatter per `wiki/schema.md §3`.
- [ ] Frontmatter fields are in English, not mixed with Portuguese equivalents (e.g., no `status: "validado"` alongside `status: "validated"`).
- [ ] `type` values match the allowed list from `wiki/schema.md §3`.
- [ ] `status` values match the allowed list from `wiki/schema.md §4`.

#### Internal Link Integrity

- [ ] All literal Markdown relative links such as ``[label](relative/path.md)`` under `FCVW/` resolve to existing files. Check links in:
  - `AGENTS.md`
  - `FCVW/README.md`
  - `FCVW/CONTEXT_MAP.md`
  - `FCVW/STACK.md`
  - `FCVW/MANIFEST.md`
  - `FCVW/PLANNING.md`
- [ ] All Obsidian-style `[[wikilink]]` references in `wiki/` point to existing files or known valid targets.
- [ ] No `FCVW/` document links to a path that was removed or relocated.

#### Cross-Reference Consistency

- [ ] **Version coherence**: `MANIFEST.md §1`, `STACK.md`, and the active changelog all declare the same current version (`Vx.y.z`).
- [ ] **Document index**: Every document listed in `MANIFEST.md §7` exists on disk. Every official document on disk is listed in `MANIFEST.md §7`.
- [ ] **Skill catalog**: Every skill in `skills/README.md` has a corresponding `skills/<name>/SKILL.md` file. No `SKILL.md` exists without a catalog entry.
- [ ] **AGENTS.md references**: Every `FCVW/` document referenced in `AGENTS.md` (selective loading table, operational rules, checklist) exists and has not been renamed.
- [ ] **CONTEXT_MAP.md accuracy**: Session types listed match the actual operational documents.

#### Table & Format Integrity

- [ ] No broken markdown tables (uneven column counts, missing separators).
- [ ] No unclosed code blocks (triple backticks without a closing pair).
- [ ] No raw HTML that could introduce rendering inconsistencies.

### Correction Protocol

For each issue found:
1. Fix the broken link, frontmatter, or reference directly.
2. If a document was renamed, update all cross-references.
3. If a file is orphaned (no longer referenced), either add it to the appropriate index or deprecate it.
4. Record all corrections in the active plan and changelog.

---

## Token Optimization Note

Use instead of loading FILESYSTEM.md + AUDIT.md + TESTS.md for validation checks. Load on-demand only when:
- Preparing a release (`skill:release-checklist` is already the primary)
- Running a structural audit (`skill:agnix-linter` covers formatting)
- Suspicion of FILESYSTEM.md drift
- Before closing a plan that alters directory structure

Do not load this skill during routine development work.
