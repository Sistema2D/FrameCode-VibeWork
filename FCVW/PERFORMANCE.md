---
schema: "fcvw/project-performance@1"
artifact_role: "project_profile"
owner: "project"
upgrade_strategy: "preserve"
instantiation_status: "pending"
---

# Performance profile

Optimize only after establishing a user-visible or operational problem and a reproducible baseline.

## Budgets

| Scenario | Metric | Target | Hard limit | Measurement |
|---|---|---|---|---|
| Startup | | | | |
| Primary interaction | | | | |
| API/service | | | | |
| Build/artifact | | | | |
| Memory/storage | | | | |

## Investigation contract

1. Reproduce under a documented environment.
2. Measure before changing.
3. Identify the dominant bottleneck.
4. Change the smallest responsible boundary.
5. Measure after changing with equivalent inputs.
6. Check correctness, accessibility, resource use, and regressions.

Do not claim percentage improvement without retaining the commands, sample size, environment, and before/after measurements.
