# Template: Troubleshooting Record

Save in: `troubleshooting/{YYYY-MM-DD}-{short-description}.md`

```markdown
---
title: "<Short description of the issue>"
type: "failure"
status: "draft | in_validation | validated | obsolete"
confidence: "low | medium | high"
last_reviewed: "YYYY-MM-DD"
related_version: "Vx.y.z"
tags:
  - "#failure-log"
  - "<additional tags>"
---

# Troubleshooting: <Short Description>

## 1. Identification

- **Date detected:** YYYY-MM-DD
- **Detected by:** <human / AI agent / automated check>
- **Affected version:** `Vx.y.z`
- **Affected files / modules:**
  - `<path/to/file.ext>`
- **Related plan (if any):** `Plans/{status}/<plan-file>.md`

## 2. Symptom Description

```text
<Describe exactly what was observed. Include error messages, unexpected behavior, or failed validations verbatim.>
```

## 3. Hypotheses

| # | Hypothesis | Validated | Result |
|---|---|---|---|
| H1 | `<hypothesis>` | `yes / no / partial` | `<outcome>` |
| H2 | `<hypothesis>` | `yes / no / partial` | `<outcome>` |

## 4. Root Cause

```text
<After investigation, describe the confirmed root cause. Leave blank until confirmed.>
```

## 5. Solution Applied

- [ ] `<Step 1>`
- [ ] `<Step 2>`
- [ ] `<Step 3>`

**Files modified:**
- `<path/to/modified-file.ext>`

## 6. Validation

| Check | Result | Evidence |
|---|---|---|
| `<validation check>` | `pass / fail` | `<evidence or link>` |

## 7. Prevention

```text
<How to prevent this issue from recurring. This section feeds the wiki/failures/ knowledge page.>
```

## 8. Wiki Promotion

- [ ] Failure is worth promoting to `wiki/failures/` (reusable, likely to recur)
- Proposed wiki page: `wiki/failures/<slug>.md`
- Tags for wiki page: `#failure-log`

## 9. Status

`open | investigating | resolved | wont-fix`

**Resolution date:** YYYY-MM-DD (when resolved)
```
