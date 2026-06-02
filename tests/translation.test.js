const fs = require('fs');
const assert = require('assert');

const html = fs.readFileSync('docs/index.html', 'utf8');

const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
if (!scriptMatch) {
    console.error("Could not find script tag in index.html");
    process.exit(1);
}

const scriptContent = scriptMatch[1];

global.localStorage = { setItem: () => {}, getItem: () => 'pt' };
const mockElements = [];
global.document = {
    querySelectorAll: (selector) => {
        if (selector === '[data-i18n]') return mockElements;
        return [];
    },
    documentElement: { lang: '' },
    getElementById: () => ({ classList: { toggle: () => {} }, style: {} })
};

global.window = {
    addEventListener: () => {},
    matchMedia: () => ({ matches: false, addEventListener: () => {} }),
    scrollY: 0
};
global.navigator = { language: 'en-US' };

eval(scriptContent);

function runTests() {
    console.log("Running translation fallback tests...");

    mockElements.length = 0;
    let el1 = { getAttribute: (attr) => attr === 'data-i18n' ? 'page_title' : null, tagName: 'TITLE', innerHTML: 'Old Title', namespaceURI: 'http://www.w3.org/1999/xhtml' };
    mockElements.push(el1);
    setLanguage('en');
    assert.strictEqual(el1.innerHTML, 'Frame Code Vibe Work', 'Existing translation should update innerHTML');
    console.log("✅ Test 1 Passed: Existing translation updates the element.");

    mockElements.length = 0;
    let el2 = { getAttribute: (attr) => attr === 'data-i18n' ? 'missing_key' : null, tagName: 'P', innerHTML: 'Original Text', namespaceURI: 'http://www.w3.org/1999/xhtml' };
    mockElements.push(el2);
    setLanguage('en');
    assert.strictEqual(el2.innerHTML, 'Original Text', 'Missing key should not modify innerHTML');
    console.log("✅ Test 2 Passed: Missing translation key does not modify the element.");

    mockElements.length = 0;
    let el3 = { getAttribute: (attr) => attr === 'data-i18n' ? 'page_title' : null, tagName: 'P', innerHTML: 'Original Text', namespaceURI: 'http://www.w3.org/1999/xhtml' };
    mockElements.push(el3);
    setLanguage('fr');
    assert.strictEqual(el3.innerHTML, 'Original Text', 'Missing language should not modify innerHTML');
    console.log("✅ Test 3 Passed: Missing language does not modify the element.");

    mockElements.length = 0;
    let el4 = { getAttribute: (attr) => attr === 'data-i18n' ? 'missing_key' : null, tagName: 'INPUT', placeholder: 'Original Placeholder', namespaceURI: 'http://www.w3.org/1999/xhtml' };
    mockElements.push(el4);
    setLanguage('en');
    assert.strictEqual(el4.placeholder, 'Original Placeholder', 'Missing key should not modify placeholder');
    console.log("✅ Test 4 Passed: Missing key does not modify the input placeholder.");

    console.log("All tests passed!");
}

runTests();
