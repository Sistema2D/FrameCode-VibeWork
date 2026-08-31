---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# Artifact ownership and upgrades

Ownership determines what an FCVW upgrade may replace.

| Role | Meaning | Examples | Upgrade action |
|---|---|---|---|
| `framework_policy` | Generic operating rule | `PLANNING.md`, `VERSIONING.md` | replace when compatible |
| `framework_lock` | Installed baseline | `FRAMEWORK_LOCK.md` | update through migration |
| `project_profile` | Application-specific truth | `MANIFEST.md`, `SCOPE.md` | preserve; merge deliberately |
| `template` | Reusable empty model | `governance/` | replace when schema-compatible |
| `record` | Historical evidence | plans, changelogs, ADRs, failures | preserve; never bulk-overwrite |
| `generated` | Derived navigation or metrics | `FILESYSTEM.md`, indexes | regenerate from current state |
| `example` | Non-authoritative sample | `examples/` | replace; never instantiate as truth |

## Required metadata

Canonical documents and new records should declare:

- `schema`;
- `artifact_role`;
- `owner`;
- `upgrade_strategy`;
- status and dates when the artifact has a lifecycle.

Legacy documents without metadata remain readable but are validated as legacy until touched.

## Upgrade algorithm

1. Read `FRAMEWORK_LOCK.md` and the target migration note.
2. Inventory local roles before copying.
3. Back up project profiles and records.
4. Replace compatible framework policies and templates.
5. Merge project profiles section by section; never use global text replacement.
6. Preserve all records.
7. Regenerate generated artifacts.
8. Run the validator in `instantiated` profile.
9. Update `FRAMEWORK_LOCK.md` only after validation.

## Protected paths

The following are always project-owned after instantiation:

- `Plans/**`;
- `changelogs/**`;
- `audits/**`;
- `briefings/**`;
- `troubleshooting/**`;
- application-created `decisions/**`;
- application-created `wiki/**`;
- populated project profiles.

An upstream release must publish a file-role manifest or equivalent migration table so selective upgrade does not depend on guesswork.

## New operational surfaces

- `APP_RULES.md` is a preserved project profile and is never overwritten by a framework upgrade.
- `Plans/<state>/queue.d/*.md` are project-owned operational indexes and the canonical queue source. `Plans/<state>/QUEUE.md` is the generated view; regenerate it instead of editing it once fragments exist.
- `DOCUMENT_GRAPH.md` is generated and may be regenerated from the physical Markdown graph.
- Context indexes are disposable generated artifacts and never replace their source documents.
- Knowledge graphs, stale-source reports, and aggregate queue views are disposable generated artifacts; their Markdown/frontmatter sources and the two state queues remain authoritative.
- `wiki/index.md` is a small preserved project profile; framework upgrades never replace its curated active links.
- Language-specific release variants contain the same ownership classes as the canonical source. A user downloads one variant; its framework policies and templates remain framework-owned, while populated project profiles and new project records become project-owned. FCVW does not install or own parallel language trees in the project.
- Release assets from V0.16.0 onward contain every framework filesystem path under the `FCVW/` root except `AGENTS.md` and the optional provider bridges `.cursorrules` and `.windsurfrules`, which only work at the repository root. Physical containment does not change ownership of populated profiles or records inside that directory; back them up before upgrading or removing.
- Removal may target only `FCVW/` as a directory plus a separate, explicit review of `AGENTS.md`, `.cursorrules`, and `.windsurfrules`. Never infer ownership of an application root `tools/`, `LICENSE`, `NOTICE`, or other ambiguous pre-V0.15.0 path, and never bulk-delete those paths.
