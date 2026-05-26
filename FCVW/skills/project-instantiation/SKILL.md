---
name: "project-instantiation"
version: "1.0.0"
trigger_keywords: ["bootstrap", "new project", "instantiate", "initialize", "novo projeto", "inicializar projeto", "fase 0", "briefing"]
session_types: ["briefing", "new_project", "document_audit"]
---

# SKILL: Project Instantiation & Bootstrapping

High-density manual and checklists for bootstrapping a new project from the FrameCode VibeWork template repository. Ensures correct variable and placeholder substitutions while preserving generic governance models.

## Activation Triggers

Load this skill (with `view_file` and `IsSkillFile: true`) when:
- The user declares "iniciar novo projeto", "instanciar framework", "bootstrap", "fase 0", "briefing", or similar.
- Instantiating the framework into a fresh downstream repository.

---

## 1. Safety Checks (Before Touching Files)

1. **Verify Sandbox Scope:** Confirm you are operating within the target downstream directory and not inside the core template repository.
2. **Template Preservation Rules:** 
   - Files under `/FCVW/governance/` and `/FCVW/wiki/templates/` **must remain 100% untouched** (no substitutions).
   - Only copies placed in the root or in active wiki subfolders should be modified.

---

## 2. Bootstrapping Steps Checklist

### Step 2.1: Briefing & Phase 0 Discovery
- Open and fill out `FCVW/BRIEFING.md` based on initial interviews or user requirements.
- Map out the exact stack to `FCVW/STACK.md` and project limits to `FCVW/SCOPE.md`.

### Step 2.2: Placeholder Substitutions
Go through the following canonical files in the workspace and replace the core placeholders (e.g. `[project-name]`, `[author-name]`):
- [ ] `README.md` (Raiz)
- [ ] `AGENTS.md` (Raiz)
- [ ] `FCVW/MANIFEST.md`

*Note: Use manual, localized search-and-replace rather than batch renaming scripts to prevent corruption.*

### Step 2.3: Initializing Versioning & Logs
- [ ] Clean up any generic template logs in `FCVW/wiki/log.md`, initializing it with the bootstrap event.
- [ ] Create the first formal changelog `FCVW/changelogs/V0.1.0.md` (or `V0.0.1.md`) documenting the initial project instantiation.
- [ ] Populate `FCVW/MANIFEST.md` under section `14. Manifest Update History` with the bootstrap event.

---

## 3. Post-Bootstrap Audit

Verify the filesystem layout after execution:
- [ ] The root folder contains `AGENTS.md`, `README.md`, `.gitignore`, `.cursorrules`, and `.windsurfrules`.
- [ ] The `/FCVW/` folder is cleanly isolated.
- [ ] All `.env` configurations are correctly filtered in `.gitignore`.
- [ ] A clean initial git commit has been formed.
