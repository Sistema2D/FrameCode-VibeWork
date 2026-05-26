---
name: "release-checklist"
version: "1.0.0"
trigger_keywords: ["release", "publish", "v0.", "v1.", "version bump", "tag release", "minor release", "major release", "patch release", "cut a release"]
session_types: ["release"]
---

# SKILL: Release Checklist

Condensed operational checklist for executing a FrameCode VibeWork release. Replaces loading `RELEASE.md` (~2.9k bytes) + `VERSIONING.md` (~4.9k bytes) + `AUDIT.md` (~4.4k bytes) separately (~12.2k bytes total → ~2.7k tokens saved per release session).

## Activation Triggers

Load this skill (with `view_file` and `IsSkillFile: true`) when the task involves:
- Bumping a version number (patch, minor, or major)
- Creating a `changelogs/Vx.y.z.md`
- Publishing a GitHub release
- Executing pre-release audit or validation
- User says "release", "publish", or references a specific version number

## 1. Version Decision

Determine the bump type before starting:

| Change Type | Bump | Example |
|---|---|---|
| Bugfix, typo, doc correction only | PATCH (`x.y.Z`) | `V0.4.0 → V0.4.1` |
| New feature, new skill, new wiki section | MINOR (`x.Y.0`) | `V0.4.0 → V0.5.0` |
| Breaking change to core fields, document removal, schema change | MAJOR (`X.0.0`) | `V0.4.0 → V1.0.0` |

## 2. Pre-Release Checklist

### 2.1 Audit

- [ ] All files modified in this release are listed in `changelogs/Vx.y.z.md`
- [ ] No placeholder fields (`<...>`) remain in modified documents
- [ ] No broken internal links introduced in this release
- [ ] `MANIFEST.md` version field matches the new version
- [ ] Related plan in `Plans/completed/` or `Plans/discontinued/`

### 2.2 Wiki Lint (Required for MINOR and MAJOR releases)

- [ ] Load skill `skills/wiki-lint/SKILL.md` and execute full lint
- [ ] Record lint result in `wiki/log.md`

### 2.3 Acceptance Criteria

- [ ] All acceptance criteria in the release plan are checked
- [ ] No P1 or P2 issues remain open in `Plans/in_progress/`

## 3. Changelog Creation

Create `changelogs/V{MAJOR}.{MINOR}.{PATCH}.md` using the structure:

```markdown
# Changelog V{MAJOR}.{MINOR}.{PATCH}

## Version
`V{MAJOR}.{MINOR}.{PATCH}`

## Date
YYYY-MM-DD

## Release Status
`published`

## Release Type
`patch | minor | major`

## Summary
- <bullet: what changed and why>

## Related Plans
- `<plan filename>`

## Items Modified
- `<file>` (<created | modified | deleted>)

## Justifications
- <why these changes were necessary>

## Validation Executed
- <what was verified>
```

## 4. Publication Sequence

```bash
# 1. Stage all changes
git add -A

# 2. Commit (use git-conventional-commits skill for message format)
git commit -m "chore: release V{MAJOR}.{MINOR}.{PATCH} — <one-line summary>"

# 3. Tag
git tag -a v{MAJOR}.{MINOR}.{PATCH} -m "V{MAJOR}.{MINOR}.{PATCH} — <one-line summary>"

# 4. Push with tags
git push origin main --tags

# 5. Create GitHub release from tag using changelogs/V*.md content
```

## 5. Post-Release Checklist

- [ ] GitHub release page created with tag `v{x}.{y}.{z}`
- [ ] Release notes match `changelogs/V{x}.{y}.{z}.md` content
- [ ] `wiki/releases/v{x}-{y}-{z}.md` created (use `wiki/templates/TEMPLATE_RELEASE_SYNTHESIS.md`)
- [ ] `wiki/index.md` → Releases section updated with link to new release page
- [ ] `wiki/log.md` → release event recorded
- [ ] AICC session synthesis (`wiki/sessions/S{num}.md`) created for this session
- [ ] `MANIFEST.md` update history entry added

## 6. Release Type Guidance

### Patch Release
- Scope: only bugfixes, doc corrections, broken links, frontmatter fixes
- Wiki lint: optional (run if wiki was modified)
- Announcement: not required

### Minor Release
- Scope: new features, new skills, new wiki content, new templates
- Wiki lint: mandatory
- Announcement: recommended (GitHub release + update README if needed)

### Major Release
- Scope: breaking changes, major architectural pivots, schema changes
- Wiki lint: mandatory
- Announcement: required
- ADR: required if architectural decision was made
- Update `INSTANTIATION.md` if the framework structure changed for downstream users
