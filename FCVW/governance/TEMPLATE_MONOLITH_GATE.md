# Template: Anti-Monolith Gate

Save or embed in the active plan before implementing a non-trivial module, component, route, service, prompt, or workflow.

```markdown
## Anti-Monolith Gate

- **Skill loaded:** `skills/anti-monolith-guard/SKILL.md`
- **Target artifact:** `<path or planned path>`
- **Change type:** `new file` / `extension` / `extraction` / `migration`
- **Primary responsibility:** `<one sentence>`
- **Explicit non-responsibilities:**
  - `<responsibility excluded from this artifact>`
- **Inputs:** `<parameters, events, files, context, request body, props, messages>`
- **Outputs:** `<return, UI, event, written file, response, side effect>`
- **Collaborators:** `<direct dependencies only>`
- **State ownership:** `<none / local / shared / external / persistent>`
- **Side effects:** `<none / IO / network / persistence / process / UI>`
- **Size budget:** `<warning threshold and block threshold>`
- **Similar code checked:** `<paths or search summary>`
- **Split decision:** `proceed` / `split first` / `temporary exception`
- **Temporary exception reason:** `<required if exception>`
- **Validation:** `<exact test, build, lint, manual check, or characterization>`
- **Follow-up debt:** `<none or #tech-debt link>`
```

## Pass Criteria

- One primary responsibility is stated.
- Excluded responsibilities are listed.
- Similar code was checked before writing.
- The planned artifact stays under the configured budget or has an explicit exception.
- Validation is specific enough to prove behavior and boundary integrity.
