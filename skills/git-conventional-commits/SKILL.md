---
name: "git-conventional-commits"
version: "1.0.0"
trigger_keywords: ["commit", "tag", "push", "publish release", "git release", "release notes", "changelog commit", "version tag"]
session_types: ["release", "versioning"]
---

# SKILL: Git Conventional Commits

High-density procedural guide for standardizing Git commits, semantic versioning tags, and release note generation in FrameCode VibeWork projects.

## Activation Triggers

Load this skill (with `view_file` and `IsSkillFile: true`) when the task involves:
- Writing or reviewing a Git commit message
- Creating a version tag (`git tag`)
- Pushing a release to remote
- Generating release notes from a changelog
- Reviewing staged changes before a commit

## 1. Commit Message Standard (Conventional Commits)

### Format

```
<type>(<scope>): <short imperative summary>

[optional body — what and why, not how]

[optional footer — breaking changes, issue refs]
```

### Allowed Types

| Type | Use When |
|---|---|
| `feat` | New feature or functional addition |
| `fix` | Bug fix or correction |
| `docs` | Documentation-only changes |
| `refactor` | Code restructuring without behavior change |
| `chore` | Maintenance tasks (deps, config, scripts) |
| `style` | Formatting, whitespace (no logic change) |
| `test` | Adding or updating tests |
| `perf` | Performance improvement |
| `ci` | CI/CD configuration changes |
| `revert` | Reverting a previous commit |

### Scope (Optional)

Use the affected module, folder, or feature as scope:

```
feat(skills): add git-conventional-commits skill
docs(wiki): populate patterns and decisions pages
fix(manifest): fill placeholder fields
```

### Breaking Changes

Mark with `BREAKING CHANGE:` in footer or `!` after type:

```
feat(api)!: change session synthesis frontmatter schema

BREAKING CHANGE: session_number field is now mandatory in all S*.md files
```

## 2. Commit Checklist

Before committing:

- [ ] `git status -s` — confirm only intended files are staged
- [ ] `git diff --staged` — review exact changes
- [ ] Commit type is accurate (`feat` vs `docs` vs `chore`)
- [ ] Summary is imperative, lowercase, ≤72 chars, no period at end
- [ ] Breaking changes are flagged if applicable
- [ ] Related plan and changelog exist for the change

## 3. Semantic Version Tagging

### Tag Command

```bash
git tag -a v{MAJOR}.{MINOR}.{PATCH} -m "V{MAJOR}.{MINOR}.{PATCH} — {one-line summary}"
```

Examples:
```bash
git tag -a v0.5.0 -m "V0.5.0 — ASE expansion and wiki population"
git tag -a v1.0.0 -m "V1.0.0 — First stable release"
```

### When to Bump

| Bump | Rule | Example trigger |
|---|---|---|
| PATCH (`x.y.Z`) | Backward-compatible bugfix or doc fix | Fix broken link, correct typo in skill |
| MINOR (`x.Y.0`) | New backward-compatible feature | New skill, new wiki page, new template |
| MAJOR (`X.0.0`) | Breaking change | Rename core fields, drop a mandatory document |

## 4. Push and Publish Sequence

```bash
# 1. Stage
git add -A

# 2. Commit
git commit -m "chore: bump to V0.5.0 — ASE expansion and wiki population"

# 3. Tag
git tag -a v0.5.0 -m "V0.5.0 — ASE expansion, wiki population, CONTEXT_MAP"

# 4. Push branch + tags
git push origin main --tags
```

## 5. Release Notes Generation

Use `changelogs/Vx.y.z.md` as the authoritative source for GitHub release notes.

Copy the **Summary** and **Items Modified** sections from the changelog into the GitHub release body.

Format for GitHub release title: `V{MAJOR}.{MINOR}.{PATCH} — {one-line summary}`

## 6. Post-Release Checklist

- [ ] Tag visible on remote: `git tag -l`
- [ ] GitHub release page created with changelog content
- [ ] `MANIFEST.md` version field updated to new version
- [ ] `wiki/releases/v{x}-{y}-{z}.md` created (use `wiki/templates/TEMPLATE_RELEASE_SYNTHESIS.md`)
- [ ] AICC session synthesis created in `wiki/sessions/`
