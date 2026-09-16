"""Resolve explicit context triggers from the canonical Markdown tables."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path, PurePosixPath
import re

from document_graph_fcvw import _outside_fences
from fcvw_cache import read_text


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


def changed_file_events(path: str) -> set[str]:
    path = normalized_path(path)
    lowered = path.lower()
    parts = set(PurePosixPath(lowered).parts)
    stem = PurePosixPath(lowered).stem
    result = {"change"}
    if lowered.endswith(".md"):
        result.add("filesystem")
    if (path == "AGENTS.md" or (path.startswith("FCVW/") and path.count("/") == 1)
            or "validate_fcvw" in stem):
        result.add("policy")
    if ("skills" in parts or stem in {"ai", "memory", "context_map"}
            or any(s in stem for s in ("retrieve_context", "adaptive_router", "context_routing", "context_selection", "context_index"))):
        result.add("ai")
    if parts & {"auth", "security", "permissions"} or stem in {"security", "auth", "permissions"}:
        result.add("security")
    if parts & {"migrations", "database"} or stem in {"data", "schemas", "migrations"}:
        result.add("data")
    if "framework-releases" in parts or "changelogs" in parts or stem in {"release", "versioning", "framework_lock"}:
        result.add("release")
    if ".github" in parts or stem in {"automation", "hooks", "watchers", "daemons", "governance_gates"}:
        result.add("automation")
    if lowered.endswith(".py") and ("tools" in parts):
        result.add("public_interface")
    return result


def resolve_routes(root: Path, *, sessions: list[str] | None = None,
                   events: list[str] | None = None, changed_files: list[str] | None = None) -> dict:
    session_table, event_table = route_tables(root)
    reasons = defaultdict(list)
    selected_events = defaultdict(list)
    for event in events or []:
        selected_events[event].append(f"explicit:event:{event}")
    for changed in changed_files or []:
        path = normalized_path(changed)
        for event in sorted(changed_file_events(path)):
            selected_events[event].append(f"changed-file:{path}:event:{event}")
    for session in dict.fromkeys(sessions or []):
        if session not in session_table:
            raise ValueError(f"unknown session: {session}; available: {', '.join(sorted(session_table))}")
        for path in session_table[session]:
            reasons[path].append(f"session:{session}")
    for event in sorted(selected_events):
        if event not in event_table:
            raise ValueError(f"unknown event: {event}; available: {', '.join(sorted(event_table))}")
        for path in event_table[event]:
            reasons[path].extend(selected_events[event])
    return {"source": "FCVW/CONTEXT_MAP.md", "mandatory_paths": list(reasons),
            "reasons": dict(reasons), "events": sorted(selected_events),
            "notice": "Explicit triggers and conservative file hints only; declare additional semantic events. "
                      "File additions/deletions require event:filesystem. Automation loads every named contract."}
