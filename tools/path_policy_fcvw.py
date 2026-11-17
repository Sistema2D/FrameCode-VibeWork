"""Shared local-disposable path policy for source inventories and validation."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

DISPOSABLE_PARTS = frozenset({'.git', '.obsidian', '.fcvw-cache',
                              '.codex-test-tmp', '__pycache__'})

# Directories that never hold governed Markdown: dependency trees, virtual
# environments, build and test output, caches. A test suite that writes a mirror
# of the repository (`.tmp-*`) while the graph is generated used to add phantom
# nodes; an application repository indexed `node_modules/` and agent worktrees.
TRANSIENT_PARTS = frozenset({
    'node_modules', '.venv', 'venv', '.tox', '.nox', '.pytest_cache',
    '.mypy_cache', '.ruff_cache', 'coverage', 'htmlcov', 'test-results',
    'playwright-report', 'dist', '.next', '.nuxt', '.svelte-kit', '.vite',
    '.turbo', '.parcel-cache',
})
TRANSIENT_PREFIXES = ('.tmp', 'tmp-')
# Project-owned exclusions: repository globs (see glob_regex) in PROJECT.md frontmatter.
UNGOVERNED_FIELD = 'ungoverned_paths'


def is_transient(relative: str) -> bool:
    """True when a repository-relative path sits in disposable or transient state."""

    parts = relative.replace('\\', '/').split('/')[:-1]
    return any(
        part in DISPOSABLE_PARTS or part in TRANSIENT_PARTS or part.startswith(TRANSIENT_PREFIXES)
        for part in parts
    )


def ungoverned_patterns(root: Path) -> list[str]:
    """Patterns a project declared as outside FCVW governance (vendored docs, mirrors)."""

    from frontmatter_fcvw import parse_frontmatter, string_list

    profile = root / 'FCVW' / 'PROJECT.md'
    if not profile.is_file():
        return []
    data = parse_frontmatter(profile.read_text(encoding='utf-8-sig')).data
    return [item.strip().replace('\\', '/') for item in string_list(data, UNGOVERNED_FIELD) if item.strip()]


def glob_regex(pattern: str) -> re.Pattern[str]:
    """Repository glob: `*` and `?` stay inside one directory, `**` crosses them,
    and a pattern that names a directory also covers everything below it."""

    pattern = pattern[2:] if pattern.startswith('./') else pattern
    pattern = pattern.rstrip('/')
    parts: list[str] = []
    index = 0
    while index < len(pattern):
        if pattern.startswith('**/', index):
            parts.append('(?:.*/)?')
            index += 3
        elif pattern.startswith('**', index):
            parts.append('.*')
            index += 2
        elif pattern[index] == '*':
            parts.append('[^/]*')
            index += 1
        elif pattern[index] == '?':
            parts.append('[^/]')
            index += 1
        else:
            parts.append(re.escape(pattern[index]))
            index += 1
    return re.compile(''.join(parts) + r'(?:/.*)?')


def matches_ungoverned(relative: str, patterns: list[str]) -> bool:
    """True when a POSIX repository path matches one of the repository globs."""

    relative = relative.replace('\\', '/')
    return any(pattern.strip() and glob_regex(pattern.strip()).fullmatch(relative) for pattern in patterns)


def _is_work_tree_root(root: Path) -> bool:
    top = subprocess.run(['git', '-C', str(root), 'rev-parse', '--show-toplevel'],
                         capture_output=True, text=True, timeout=30, check=False)
    return top.returncode == 0 and Path(top.stdout.strip()).resolve() == root


def git_ignored_root_entries(root: Path) -> frozenset[str]:
    """Root entries the git work tree at ``root`` ignores; empty outside one.

    An ignored entry (a side project, a local archive) is never committed,
    inventoried or packaged, so it is local state, not clean-template content.
    """

    root = Path(root).resolve()
    names = [entry.name + ('/' if entry.is_dir() else '') for entry in root.iterdir() if entry.name != '.git']
    try:
        if not names or not _is_work_tree_root(root):
            return frozenset()
        listed = subprocess.run(
            ['git', '-C', str(root), '-c', 'core.quotepath=off', 'check-ignore', '-z', '--stdin'],
            input='\0'.join(names).encode('utf-8'), capture_output=True, timeout=30, check=False)
    except (OSError, subprocess.SubprocessError):
        return frozenset()
    if listed.returncode not in (0, 1):
        return frozenset()
    return frozenset(item.rstrip('/') for item in listed.stdout.decode('utf-8', 'surrogateescape').split('\0') if item)


def _git_markdown(root: Path) -> list[str] | None:
    """Tracked plus untracked-but-not-ignored Markdown, or None outside a git work tree."""

    try:
        if not _is_work_tree_root(root):
            return None
        listed = subprocess.run(
            ['git', '-C', str(root), '-c', 'core.quotepath=off', 'ls-files', '-z', '--cached', '--others',
             '--exclude-standard', '--', '*.md'],
            capture_output=True, timeout=60, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    if listed.returncode != 0:
        return None
    return sorted({item for item in listed.stdout.decode('utf-8', 'surrogateescape').split('\0') if item})


def _walked_markdown(root: Path) -> list[str]:
    """Filesystem fallback; never descends into a nested repository or worktree."""

    found: list[str] = []
    for folder, directories, files in os.walk(root):
        current = Path(folder)
        directories[:] = sorted(
            name for name in directories
            if name not in DISPOSABLE_PARTS and name not in TRANSIENT_PARTS
            and not name.startswith(TRANSIENT_PREFIXES) and not (current / name / '.git').exists()
        )
        found.extend((current / name).relative_to(root).as_posix() for name in files if name.endswith('.md'))
    return found


def governed_markdown_inventory(root: Path) -> list[Path]:
    """One immutable snapshot of the Markdown that FCVW governs under ``root``.

    Inside a git work tree, git's own ignore rules decide what exists for
    governance; elsewhere the walk skips transient directories and nested
    repositories. The contract exclusions and the project's ``ungoverned_paths``
    apply in both cases. Every consumer (graph, catalog, knowledge graph,
    context index) reads this list, so a catalog and its validation can no
    longer observe two different trees.
    """

    root = Path(root).resolve()
    listed = _git_markdown(root)
    candidates = listed if listed is not None else _walked_markdown(root)
    patterns = ungoverned_patterns(root)
    paths = [
        root / relative
        for relative in candidates
        if not is_transient(relative) and not matches_ungoverned(relative, patterns) and (root / relative).is_file()
    ]
    return sorted(paths, key=lambda item: item.relative_to(root).as_posix().lower())

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

