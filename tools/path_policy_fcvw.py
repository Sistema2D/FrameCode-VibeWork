"""Shared local-disposable path policy for source inventories and validation."""

DISPOSABLE_PARTS = frozenset({'.git', '.obsidian', '.fcvw-cache',
                              '.codex-test-tmp', '__pycache__'})

CLEAN_ROOT_ENTRIES = frozenset({
    '.cursorrules', '.git', '.gitattributes', '.github', '.gitignore',
    '.obsidian', '.fcvw-cache', '.codex-test-tmp', '.windsurfrules',
    'AGENTS.md', 'FCVW', 'LICENSE', 'NOTICE', 'README.md', 'tools',
})
