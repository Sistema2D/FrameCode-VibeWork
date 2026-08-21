# Sources

Selected evidence records whose provenance, digest, or change impact is worth tracking.

## Rules

- Use this folder to create pages that explain the origin, context, and relevance of raw sources.
- Each relevant source must point to its raw file, if any.
- Sources used in syntheses must be cited in the frontmatter of the pages.
- Do not mirror every repository artifact. Create a source page only when explicit provenance or stale-impact analysis adds value.
- Use `source_digest` for tracked source bytes; `content_hash` and `chunk_hash` belong to context-index chunks.
- A changed digest creates review candidates for pages linked through `derived_from`; it never rewrites those pages or their status.
- Start from [`TEMPLATE_SOURCE.md`](../templates/TEMPLATE_SOURCE.md).
