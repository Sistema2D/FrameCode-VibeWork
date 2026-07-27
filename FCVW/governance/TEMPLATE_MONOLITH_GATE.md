# Template: Anti-Monolith Gate

Save or embed in the active plan before implementing a non-trivial module, component, route, service, prompt, or workflow.

```markdown
## Anti-Monolith Gate

- **Skill loaded:** `skills/anti-monolith-guard/SKILL.md`
- **Target artifact:** `<path or planned path>`
- **Change type:** `new file` / `extension` / `extraction` / `migration`
- **Artifact class:** `source` / `operational instruction` / `documentation` / `record/template/generated`
- **Numeric threshold applicability:** `applicable` / `warning only` / `not applicable`
- **Primary responsibility:** `<one sentence>`
- **Explicit non-responsibilities:**
  - `<responsibility excluded from this artifact>`
- **Inputs:** `<parameters, events, files, context, request body, props, messages>`
- **Outputs:** `<return, UI, event, written file, response, side effect>`
- **Collaborators:** `<direct dependencies only>`
- **State ownership:** `<none / local / shared / external / persistent>`
- **Side effects:** `<none / IO / network / persistence / process / UI>`
- **Size budget:** `<warning threshold and block threshold>`
- **Threshold source or resize rationale:** `<default, project override, or evidence-based adjustment>`
- **Similar code checked:** `<paths or search summary>`
- **Split decision:** `proceed` / `split first` / `temporary exception`
- **Temporary exception reason:** `<required if exception>`
- **Validation:** `<exact test, build, lint, manual check, or characterization>`
- **Follow-up debt:** `<none or #tech-debt link>`
```

## Pass Criteria

- One primary responsibility is stated.
- Excluded responsibilities are listed.
- Numeric thresholds are enforced only for applicable source or operational artifacts; documentary length alone cannot fail the gate.
- Any exception or resized threshold records critical-attribute impact, validation, owner, and revisit condition.
- Similar code was checked before writing.
- The planned artifact stays under the configured budget or has an explicit exception.
- Validation is specific enough to prove behavior and boundary integrity.
