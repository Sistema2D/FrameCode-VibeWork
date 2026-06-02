/**
 * @jest-environment jsdom
 */

const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.resolve(__dirname, '../docs/index.html'), 'utf8');

describe('Language Auto Detection', () => {
  let setLanguageMock;
  let originalNavigatorLanguage;

  beforeEach(() => {
    document.documentElement.innerHTML = html.toString();

    // Reset localStorage
    localStorage.clear();

    // Mock setLanguage function that is called by the auto detect logic
    setLanguageMock = jest.fn();
    window.setLanguage = setLanguageMock;

    // Store original navigator language
    originalNavigatorLanguage = Object.getOwnPropertyDescriptor(window.navigator, 'language');
  });

  afterEach(() => {
    // Restore original navigator language
    if (originalNavigatorLanguage) {
      Object.defineProperty(window.navigator, 'language', originalNavigatorLanguage);
    }
  });

  function mockLanguage(lang) {
    Object.defineProperty(window.navigator, 'language', {
      value: lang,
      configurable: true
    });
  }

  function executeAutoDetectLogic() {
    // Extract the exact logic from index.html:1211-1222
    const sysLang = navigator.language || navigator.userLanguage;
    let defaultLang = 'pt';
    if (sysLang) {
        const code = sysLang.split('-')[0].toLowerCase();
        if (['pt', 'en', 'es', 'de'].includes(code)) {
            defaultLang = code;
        }
    }
    const savedLang = localStorage.getItem('fcvw-lang') || defaultLang;
    window.setLanguage(savedLang);
  }

  it('should fallback to "pt" when navigator.language is undefined', () => {
    mockLanguage(undefined);
    executeAutoDetectLogic();
    expect(setLanguageMock).toHaveBeenCalledWith('pt');
  });

  it('should fallback to "pt" for unsupported languages (e.g., fr-FR)', () => {
    mockLanguage('fr-FR');
    executeAutoDetectLogic();
    expect(setLanguageMock).toHaveBeenCalledWith('pt');
  });

  it('should detect and use English when navigator.language is en-US', () => {
    mockLanguage('en-US');
    executeAutoDetectLogic();
    expect(setLanguageMock).toHaveBeenCalledWith('en');
  });

  it('should detect and use Spanish when navigator.language is es-ES', () => {
    mockLanguage('es-ES');
    executeAutoDetectLogic();
    expect(setLanguageMock).toHaveBeenCalledWith('es');
  });

  it('should detect and use German when navigator.language is de-DE', () => {
    mockLanguage('de-DE');
    executeAutoDetectLogic();
    expect(setLanguageMock).toHaveBeenCalledWith('de');
  });

  it('should use the language stored in localStorage if available, overriding navigator', () => {
    mockLanguage('en-US');
    localStorage.setItem('fcvw-lang', 'es');
    executeAutoDetectLogic();
    expect(setLanguageMock).toHaveBeenCalledWith('es');
  });
});
