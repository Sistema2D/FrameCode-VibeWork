# Agnix Linter (AI Config Linter)

*Activation Triggers:* periodic maintenance, governance audit, validating AI instructions.

This skill is designed to audit the internal consistency and structural integrity of the `FrameCode-VibeWork` framework itself.

## Core Directives

When invoked to run a governance audit, you must behave as an AI Config Linter. Your job is to parse the markdown files inside `FCVW/` and the root `AGENTS.md` to ensure they are valid, non-conflicting, and functional for AI agents.

### Linter Rules to Enforce:

1. **Dead Links Check:** Verify that all `[links](...)` pointing to internal `FCVW/` documents resolve to actual files on disk. 
2. **Conflict Detection:** Compare `AGENTS.md` instructions against specific `FCVW/skills/*/SKILL.md` files. Report if a global rule contradicts a specific skill rule.
3. **Format Integrity:** 
   - Ensure all `SKILL.md` files clearly state their *Activation Triggers* at the top.
   - Ensure no markdown file has broken tables or unclosed code blocks.
4. **Mandatory Hooks:** Ensure `FCVW/PLANNING.md` correctly references `AGENTS.md` and the changelogs logic.

### Workflow:
1. Scan the `FCVW/` directory tree.
2. Cross-reference the files.
3. Automatically fix broken links or minor formatting issues.
4. If a logical conflict is found in governance, generate an audit report in `FCVW/AUDIT.md` (or a similar reporting structure) and present it to the human partner for review. Do not change governance logic without human approval.
