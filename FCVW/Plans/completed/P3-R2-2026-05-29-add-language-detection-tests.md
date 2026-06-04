---
status: completed
priority: P3
risk: R2
current_version: "V0.7.5"
expected_version: "V0.7.5"
---
# Plan: Add Language Auto-Detection Tests

## Acceptance Criteria
- Logic in `docs/index.html` lines 1211-1222 for auto detecting language is tested.
- Fallbacks to 'pt' are tested.
- LocalStorage persistence is tested.

## Test Plan
- Run the tests with `npm test`.

## Execution Notes
- Installed `jest` and `jest-environment-jsdom`.
- Wrote tests in `tests/autoDetectLanguage.test.js` mocking JSDOM context.
- Tests successfully cover undefined language, unsupported languages, and reading from local storage.
