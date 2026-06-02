const fs = require('fs');
const path = require('path');
const { JSDOM, VirtualConsole } = require('jsdom');
const assert = require('assert');

// Setup virtual console to ignore tailwind errors
const virtualConsole = new VirtualConsole();
virtualConsole.on("error", () => {});

// Load HTML
const html = fs.readFileSync(path.resolve(__dirname, '../../../docs/index.html'), 'utf8');

// Initialize JSDOM
const dom = new JSDOM(html, { runScripts: "dangerously", url: "http://localhost/", virtualConsole });

// Run Tests
try {
  // 1. Test language switch to English
  dom.window.setLanguage('en');
  assert.strictEqual(dom.window.localStorage.getItem('fcvw-lang'), 'en');

  let whatIsTitleEn = dom.window.document.querySelector('[data-i18n="what_is_title"]').innerHTML;
  assert.strictEqual(whatIsTitleEn, 'What it is');

  // 2. Test language switch to Portuguese
  dom.window.setLanguage('pt');
  assert.strictEqual(dom.window.localStorage.getItem('fcvw-lang'), 'pt');

  let whatIsTitlePt = dom.window.document.querySelector('[data-i18n="what_is_title"]').innerHTML;
  assert.strictEqual(whatIsTitlePt, 'O que é');

  // 3. Test SVG element updates
  const svgActionFeedbackPt = dom.window.document.querySelector('[data-i18n="svg_action_feedback"]').textContent;
  assert.strictEqual(svgActionFeedbackPt, 'ALIMENTAÇÃO DE CONTEXTO');

  console.log('✅ setLanguage tests passed!');
} catch (err) {
  console.error('❌ Tests failed:', err);
  process.exit(1);
}
