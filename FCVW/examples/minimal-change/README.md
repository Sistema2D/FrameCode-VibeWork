---
artifact_role: example
owner: framework
upgrade_strategy: replace
---

# Minimal governed change

This fixture shows the smallest complete chain for a low-risk application change:

1. Copy `plan.md` into the appropriate `FCVW/Plans/<state>/` directory and replace all placeholders.
2. Implement and validate only the approved scope.
3. Copy `changelog.md` into `FCVW/changelogs/unreleased/`, link the completed plan, and record observed evidence.
4. Move the plan through the lifecycle without changing its ID.

The fixture is intentionally not stored inside a live plan or changelog directory, so clean-template validation cannot mistake it for project history.
