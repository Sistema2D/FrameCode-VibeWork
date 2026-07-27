---
schema: "fcvw/plan-queue@1"
artifact_role: "project_profile"
owner: "project"
upgrade_strategy: "preserve"
state: "pending"
updated_at: "2026-07-27"
---

# Pending plan queue

Plans are ordered by `correction`, `optimization`, `code_hygiene`, `visual`, then `other`. A lower-ranked category may appear earlier only with a concrete override reason.

| Order | Plan | Category | Blocked by | Override reason |
|---:|---|---|---|---|
