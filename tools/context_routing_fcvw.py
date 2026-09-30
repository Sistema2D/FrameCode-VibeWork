"""Resolve explicit context triggers from the canonical Markdown tables."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path, PurePosixPath
import re

from document_graph_fcvw import _outside_fences
from fcvw_cache import frontmatter, read_text
from frontmatter_fcvw import find_section, markdown_sections, scalar

FILE_OPERATIONS = {"add", "modify", "delete", "move", "rename", "unknown"}
# Roles whose change is a framework policy change. A project profile such as
# FCVW/SECURITY.md lives beside the policies but only triggers its own domain.
POLICY_ROLES = {"framework_policy", "framework_lock", "template"}
PRIVATE_TOOL_STEMS = {"fcvw_cache", "frontmatter_fcvw", "release_layout_fcvw",
                      "knowledge_sources_fcvw", "plan_dependencies_fcvw", "context_routing_fcvw",
                      "context_selection_fcvw", "trace_fcvw"}


def normalized_path(value: str) -> str:
    value = value.replace("\\", "/")
    if value.startswith("./"):
        value = value[2:]
    if (not value or ":" in value or PurePosixPath(value).is_absolute()
            or any(p in {"", ".", ".."} for p in value.split("/"))):
        raise ValueError(f"expected a repository-relative path: {value}")
    return value


def route_tables(root: Path) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Stable tokens live in the existing tables, including translated variants."""
    sessions, events = {}, {}
    for line in _outside_fences(read_text(root / "FCVW/CONTEXT_MAP.md")):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        event_ids = re.findall(r"`event:([a-z_]+)`", cells[0])
        session_ids = re.findall(r"`([a-z_]+)`", cells[0]) if len(cells) == 5 else []
        if not event_ids and not session_ids:
            continue
        if event_ids and len(cells) != 3:
            raise ValueError("malformed canonical event row")
        source = cells[1] if event_ids else cells[2]
        paths = []
        for token in re.findall(r"`([^`]+)`", source):
            if token.endswith(".md"):
                path = token if token == "AGENTS.md" or token.startswith("FCVW/") else "FCVW/" + token
            elif re.fullmatch(r"[a-z][a-z-]+", token):
                path = f"FCVW/skills/{token}/SKILL.md"
            else:
                raise ValueError(f"unsupported immediate context reference: {token}")
            paths.append(normalized_path(path))
        if not paths:
            raise ValueError("canonical route has no explicit paths")
        table = events if event_ids else sessions
        for name in event_ids or session_ids:
            if name in table:
                raise ValueError(f"duplicate canonical route: {name}")
            table[name] = paths
    return sessions, events


def declared_role(root: Path | None, path: str) -> str | None:
    """The artifact_role of an existing governed Markdown file, if declared."""
    if root is None or not path.endswith(".md") or not (root / path).is_file():
        return None
    return scalar(frontmatter(root / path), "artifact_role") or None


AI_BRIDGES = {"AGENTS.md", ".cursorrules", ".windsurfrules"}
# Semantic events that only the host can classify for application files.
SEMANTIC_EVENTS = ("security", "data", "public_interface", "ai", "dependency", "automation", "release")


def is_framework_path(path: str, root: Path | None) -> bool:
    """Paths owned by the framework in either layout; everything else is application."""
    if path in AI_BRIDGES or path.startswith("FCVW/"):
        return True
    # The source checkout keeps the framework tools in a root tools/ directory.
    return path.startswith("tools/") and (root is None or (root / "tools" / "validate_fcvw.py").is_file())


def is_policy_path(path: str, root: Path | None) -> bool:
    if path in AI_BRIDGES or path.startswith("FCVW/governance/"):
        return True
    if not (path.startswith("FCVW/") and path.count("/") == 1):
        return False
    role = declared_role(root, path)
    # Unknown (deleted, unreadable or undeclared) stays conservative.
    return role is None or role in POLICY_ROLES


def changed_file_events(path: str, operation: str = "unknown", root: Path | None = None) -> set[str]:
    """Events implied by the path alone.

    Only unambiguous facts are derived: file operations and framework-owned
    paths. Application paths never imply a semantic event (G-03): guessing from
    names missed `auth_service.py` and fired on `src/skills/`, so the host
    declares security, data, interface and AI impact, and the route result warns
    when a versioned application change declares none.
    """
    path = normalized_path(path)
    if operation not in FILE_OPERATIONS:
        raise ValueError(f"unknown file operation: {operation}")
    lowered = path.lower()
    pure = PurePosixPath(lowered)
    stem, parts = pure.stem, set(pure.parts)
    result = {"change"}
    if operation in {"add", "delete", "move", "rename"} or (operation == "unknown" and lowered.endswith(".md")):
        result.add("filesystem")
    if lowered.startswith(".github/workflows/"):
        result.add("automation")
    if not is_framework_path(path, root):
        return result
    tool = pure.suffix == ".py" and "tools" in parts
    if is_policy_path(path, root) or (tool and stem == "validate_fcvw"):
        result.add("policy")
    if (path in AI_BRIDGES or lowered.startswith("fcvw/skills/") or stem in {"ai", "context_map"}
            or (tool and any(s in stem for s in ("retrieve_context", "context_routing", "context_selection", "context_index")))):
        result.add("ai")
    if lowered in {"fcvw/security.md"}:
        result.add("security")
    if lowered in {"fcvw/data.md", "fcvw/migrations.md"}:
        result.add("data")
    if parts & {"framework-releases", "changelogs"} or lowered in {"fcvw/release.md", "fcvw/framework_lock.md"}:
        result.add("release")
    if lowered == "fcvw/automation.md":
        result.add("automation")
    if tool and not stem.startswith("test_") and stem not in PRIVATE_TOOL_STEMS:
        result.add("public_interface")
    return result


def selective_rows(root: Path) -> dict[str, list[str]]:
    """The 'Selective loading' table as {path: [first-read cell, expand-when cell]}."""
    rows: dict[str, list[str]] = {}
    active = False
    for line in _outside_fences(read_text(root / 'FCVW/CONTEXT_MAP.md')):
        if line.startswith('## '):
            active = line == '## Selective loading for long documents'
            continue
        if not active or not line.startswith('|'):
            continue
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        if len(cells) != 3:
            continue
        match = re.fullmatch(r'`([A-Za-z_][A-Za-z0-9_/-]*\.md)`', cells[0])
        if match:
            rows['FCVW/' + match.group(1)] = cells[1:]
    return rows


def section_hints(root: Path, selected: set[str]) -> dict[str, str]:
    """Expose the canonical first-section guidance without loading whole policies."""
    return {path: cells[0] for path, cells in selective_rows(root).items() if path in selected}


# 'One of:' as written in each release language (en-US, pt-BR, es, de).
ALTERNATIVE_PREFIXES = ('one of', 'um de', 'uma de', 'uno de', 'una de', 'eines von', 'einer von', 'eine von')


def named_sections(hint: str) -> tuple[list[str], bool]:
    """Backticked heading names of a first-read hint and whether they are alternatives ('One of:')."""
    names = [token for token in re.findall(r'`([^`]+)`', hint)
             if '/' not in token and not re.search(r'\.[A-Za-z]{1,4}$', token)]
    return names, hint.lower().startswith(ALTERNATIVE_PREFIXES)


def section_ranges(root: Path, paths: list[str]) -> dict:
    """Line ranges of the first-read sections of each routed long document.

    The host reads these ranges instead of whole files. A heading that no longer
    resolves is reported and the whole file is counted, so the fallback reads
    more, never less. Alternatives ('One of:') count the largest candidate.
    """
    rows = selective_rows(root)
    ranges: dict[str, dict] = {}
    whole = first = 0
    for path in paths:
        target = root / path
        if not path.endswith('.md') or not target.is_file():
            continue
        size = target.stat().st_size
        whole += size
        if path not in rows:
            first += size
            continue
        names, alternatives = named_sections(rows[path][0])
        outline = markdown_sections(read_text(target))
        found = [(name, find_section(outline, name)) for name in names]
        chosen = [section for _, section in found if section]
        unresolved = [name for name, section in found if not section]
        preamble = outline[0]
        if unresolved or not chosen:
            first_read = size
        elif alternatives:
            first_read = int(preamble['bytes']) + max(int(item['bytes']) for item in chosen)
        else:
            first_read = int(preamble['bytes']) + sum(int(item['bytes']) for item in chosen)
        first += first_read
        ranges[path] = {
            'file_bytes': size,
            'first_read_bytes': first_read,
            'alternatives': alternatives,
            'sections': [{'heading': item['heading'], 'lines': item['lines'], 'bytes': item['bytes']}
                         for item in [preamble, *chosen]],
            'expand_when': rows[path][1],
            'unresolved': unresolved,
        }
    return {'ranges': ranges, 'context_bytes': {'whole_files': whole, 'first_read': first}}


def resolve_routes(root: Path, *, sessions: list[str] | None = None,
                   events: list[str] | None = None, changed_files: list[str] | None = None,
                   file_changes: list[str] | None = None, versioned_change: bool = False) -> dict:
    session_table, event_table = route_tables(root)
    if versioned_change and (not events or not (changed_files or file_changes)):
        raise ValueError("versioned change requires at least one explicit --event and changed file")
    reasons = defaultdict(list)
    selected_events = defaultdict(list)
    for event in events or []:
        selected_events[event].append(f"explicit:event:{event}")
    for changed in changed_files or []:
        path = normalized_path(changed)
        for event in sorted(changed_file_events(path, root=root)):
            selected_events[event].append(f"changed-file:{path}:event:{event}")
    for value in file_changes or []:
        operation, separator, raw_path = value.partition(":")
        if not separator:
            raise ValueError("file change must be OPERATION:repository-relative-path")
        path = normalized_path(raw_path)
        for event in sorted(changed_file_events(path, operation, root)):
            selected_events[event].append(f"file-change:{operation}:{path}:event:{event}")
    for session in dict.fromkeys(sessions or []):
        if session not in session_table:
            raise ValueError(f"unknown session: {session}; available: {', '.join(sorted(session_table))}")
        for path in session_table[session]:
            reasons[path].append(f"session:{session}")
    warnings = []
    declared = set(events or [])
    application = sorted({normalized_path(value.partition(":")[2]) for value in file_changes or []}
                         | {normalized_path(value) for value in changed_files or []})
    application = [path for path in application if not is_framework_path(path, root)]
    if versioned_change and application and not declared & set(SEMANTIC_EVENTS):
        warnings.append(
            "application files changed without a semantic event; declare any that apply: "
            + ", ".join(f"event:{name}" for name in SEMANTIC_EVENTS)
            + f" (files: {', '.join(application[:5])}{', ...' if len(application) > 5 else ''})"
        )
    for event in sorted(selected_events):
        if event not in event_table:
            raise ValueError(f"unknown event: {event}; available: {', '.join(sorted(event_table))}")
        for path in event_table[event]:
            reasons[path].extend(selected_events[event])
    return {"source": "FCVW/CONTEXT_MAP.md", "mandatory_paths": list(reasons),
            "section_hints": section_hints(root, set(reasons)),
            "reasons": dict(reasons), "events": sorted(selected_events), "warnings": warnings,
            "notice": "Paths imply only file operations and framework-owned surfaces; declare every semantic "
                      "event (security, data, interface, AI, dependency) for application files."}
