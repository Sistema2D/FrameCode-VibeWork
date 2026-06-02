---
status: completed
priority: medium
risk: low
version: "1.0.0"
expected_version: "1.0.0"
context_files: ["docs/index.html"]
---

# Add tests for translation fallback

## Problem
The translation script in `docs/index.html` relies on implicit behavior when a translation is missing:
```javascript
if (translations[lang] && translations[lang][key]) {
    // apply translation
}
```
If a translation is missing, it simply skips updating the DOM element. There are no tests verifying that this edge case works correctly and doesn't crash or throw errors.

## Solution
1. In the `docs/index.html` file, add a test suite script block if none exists, or append to it. Since there's no `package.json` or external testing framework configured according to the `TESTS.md` (it says we have to do manual testing when there are no automated tests, but the prompt asks to "Write Tests" which suggests we should add automated checks for this JavaScript logic).
2. Given it's a standalone HTML file with inline JS, we can write a simple ad-hoc test function right in the HTML file (e.g. at the bottom of the `<script>` tag or in a new `<script>` tag for tests) that runs on page load, or use a lightweight test approach. Alternatively, create a separate test file `docs/index.test.html` or `docs/test.js` if that's preferred, but usually keeping it self-contained is simplest if there's no framework. Wait, the `TESTS.md` mentions: "When no automated tests are available, the execution plan's final testing requirement must be satisfied with an explicit bash command formally recording the manual test completion (e.g., `echo 'Manual visual regression test passed; no automated test scripts exist.').". But the current task explicitely says "Missing edge case tests for translation fallback" and "Write effective tests", "Use appropriate mocks and test doubles".

Let's look at how to mock DOM and test it. We can write a simple Node.js test script using `jsdom` or just vanilla JS in a new file, or maybe run tests in the browser console. Since there's no package.json, we can create a simple JS file that reads the HTML, extracts the translation logic, and tests it, or better yet, inject a testing script.

Let me write a Node script `test-translation.js` that uses vanilla JS to test the logic by mocking the DOM.

Wait, if I just add a test script into the codebase, where should it go? I can create a `tests/` directory.

## Execution Notes
- Added Node.js test script to verify missing translations handling.
