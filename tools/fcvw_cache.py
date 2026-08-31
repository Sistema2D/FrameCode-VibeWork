#!/usr/bin/env python3
"""Process-local read and parse cache shared by the FCVW tools.

A single validation run reads every governed Markdown file several times: once
for link checking, once for frontmatter, once while building the document graph,
and again for each record-specific rule. The files cannot change during a run, so
the repeated work is pure waste that grows linearly with the repository.

The cache is keyed by path plus modification time and size, so a tool or test
that rewrites a file mid-process still observes the new content. Nothing here
changes validation semantics; it only removes duplicated I/O and parsing.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from frontmatter_fcvw import FrontmatterResult, parse_frontmatter


_TEXT: dict[tuple[str, int, int], str] = {}
_FRONTMATTER: dict[tuple[str, int, int], FrontmatterResult] = {}
_STATS = {"text_hits": 0, "text_reads": 0, "frontmatter_hits": 0, "frontmatter_parses": 0}


def _key(path: Path) -> tuple[str, int, int]:
    stat = path.stat()
    return (str(path), stat.st_mtime_ns, stat.st_size)


def read_text(path: Path) -> str:
    """Read governed text once per (path, mtime, size)."""

    try:
        key = _key(path)
    except OSError:
        return path.read_text(encoding="utf-8-sig")
    cached = _TEXT.get(key)
    if cached is not None:
        _STATS["text_hits"] += 1
        return cached
    text = path.read_text(encoding="utf-8-sig")
    _TEXT[key] = text
    _STATS["text_reads"] += 1
    return text


def parsed_frontmatter(path: Path) -> FrontmatterResult:
    """Parse frontmatter once per (path, mtime, size)."""

    try:
        key = _key(path)
    except OSError:
        return parse_frontmatter(path.read_text(encoding="utf-8-sig"))
    cached = _FRONTMATTER.get(key)
    if cached is not None:
        _STATS["frontmatter_hits"] += 1
        return cached
    parsed = parse_frontmatter(read_text(path))
    _FRONTMATTER[key] = parsed
    _STATS["frontmatter_parses"] += 1
    return parsed


def frontmatter(path: Path) -> dict[str, Any]:
    """Return only the frontmatter mapping for one path."""

    return parsed_frontmatter(path).data


def statistics() -> dict[str, int]:
    """Expose counters so a performance claim can cite measured numbers."""

    return dict(_STATS)


def clear() -> None:
    """Drop the cache; used by tests that rebuild trees in place."""

    _TEXT.clear()
    _FRONTMATTER.clear()
    for name in _STATS:
        _STATS[name] = 0
