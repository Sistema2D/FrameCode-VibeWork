"""Shared local-disposable path policy for source inventories and validation."""

DISPOSABLE_PARTS = frozenset({'.git', '.obsidian', '.fcvw-cache',
                              '.codex-test-tmp', '__pycache__'})

CLEAN_ROOT_ENTRIES = frozenset({
    '.cursorrules', '.git', '.gitattributes', '.github', '.gitignore',
    '.obsidian', '.fcvw-cache', '.codex-test-tmp', '.windsurfrules',
    'AGENTS.md', 'FCVW', 'LICENSE', 'NOTICE', 'README.md', 'TODO.md', 'tools',
})

# Paths every framework tree must contain, in source-checkout form. The validator
# maps them to the installed layout with release_layout_fcvw.installed_path.
REQUIRED_SOURCE_PATHS = (
    "AGENTS.md",
    "README.md",
    "LICENSE",
    "NOTICE",
    "tools/validate_fcvw.py",
    "tools/test_validate_fcvw.py",
    "tools/test_open_issues.py",
    "tools/test_plan_dependencies_and_knowledge.py",
    "tools/frontmatter_fcvw.py",
    "tools/document_graph_fcvw.py",
    "tools/knowledge_graph_fcvw.py",
    "tools/knowledge_sources_fcvw.py",
    "tools/plan_dependencies_fcvw.py",
    "tools/plan_queue_fcvw.py",
    "tools/build_context_index.py",
    "tools/retrieve_context.py",
    "tools/locale_fcvw.py",
    "tools/package_release_fcvw.py",
    "tools/release_layout_fcvw.py",
    "tools/fcvw_cache.py",
    "tools/role_manifest_fcvw.py",
    "tools/upgrade_fcvw.py",
    "FCVW/README.md",
    "FCVW/APP_RULES.md",
    "FCVW/FRAMEWORK_LOCK.md",
    "FCVW/OWNERSHIP.md",
    "FCVW/SCHEMAS.md",
    "FCVW/MIGRATIONS.md",
    "FCVW/PLANNING.md",
    "FCVW/CONTEXT_MAP.md",
    "FCVW/RELEASE.md",
    "FCVW/AUTOMATION.md",
    "FCVW/REGRESSION_GUARDS.md",
    "FCVW/governance/TEMPLATE_PLAN.md",
    "FCVW/governance/TEMPLATE_PLAN_COMPACT.md",
    "FCVW/governance/TEMPLATE_AUDIT.md",
    "FCVW/skills/README.md",
    "FCVW/wiki/README.md",
    "FCVW/governance/TEMPLATE_NOTE.md",
    "FCVW/governance/TEMPLATE_REGRESSION.md",
)

