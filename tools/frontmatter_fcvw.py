#!/usr/bin/env python3
"""Parse the portable YAML subset used by FrameCode VibeWork."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TypeAlias


FrontmatterValue: TypeAlias = str | list[str]
KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")
LIST_ITEM = re.compile(r"^  -\s*(.*)$")
UNSUPPORTED_VALUE = re.compile(r"^(?:[>|!]|&\S|\*\S)")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")


def scan_fences(text: str) -> tuple[list[tuple[int, str, str]], str]:
    """Classify each line as 'fence', 'code' or 'text' and return any unclosed fence.

    The single fence tracker shared by the tools: a fence closes only with the
    same character and at least the opening length.
    """

    lines: list[tuple[int, str, str]] = []
    marker = ""
    for number, line in enumerate(text.splitlines(), 1):
        fence = FENCE.match(line)
        if fence:
            current = fence.group(1)
            if not marker:
                marker = current
            elif current[0] == marker[0] and len(current) >= len(marker):
                marker = ""
            lines.append((number, line, "fence"))
        else:
            lines.append((number, line, "code" if marker else "text"))
    return lines, marker


HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
EXPLICIT_ANCHOR = re.compile(r"""<a\s+(?:id|name)\s*=\s*["']([^"']+)["']""", re.I)


def _body_lines(text: str) -> list[tuple[int, str, str]]:
    """Fence-classified lines with a leading frontmatter block marked as code."""

    lines = scan_fences(text)[0]
    if lines and lines[0][1].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index][1].strip() == "---":
                return [(n, line, "code" if i <= index else kind) for i, (n, line, kind) in enumerate(lines)]
    return lines


def heading_slug(title: str) -> str:
    """GitHub-style heading anchor: markup and punctuation dropped, spaces become hyphens."""

    value = re.sub(r"<[^>]+>", "", title).replace("`", "").strip().lower()
    return "".join(ch for ch in value if ch.isalnum() or ch in "-_ ").replace(" ", "-")


def heading_anchors(text: str) -> set[str]:
    """Every fragment a Markdown file answers to: heading slugs (with -N duplicates) and explicit anchors."""

    anchors: set[str] = set()
    seen: dict[str, int] = {}
    for _, line, kind in _body_lines(text):
        if kind != "text":
            continue
        anchors.update(EXPLICIT_ANCHOR.findall(line))
        match = HEADING.match(line)
        if match:
            slug = heading_slug(match.group(2))
            count = seen.get(slug, 0)
            seen[slug] = count + 1
            anchors.add(slug if count == 0 else f"{slug}-{count}")
    return anchors


def markdown_sections(text: str) -> list[dict[str, object]]:
    """Heading outline with 1-based inclusive line ranges and UTF-8 byte sizes.

    A section runs until the next heading of the same or a higher level. The
    first entry is the preamble (frontmatter, title and text before the first
    level-two heading).
    """

    lines = _body_lines(text)
    heads = [
        (number, len(match.group(1)), match.group(2).replace("`", "").strip())
        for number, line, kind in lines
        if kind == "text" and (match := HEADING.match(line)) and len(match.group(1)) >= 2
    ]
    total = len(lines)

    def size(start: int, end: int) -> int:
        return sum(len(line.encode("utf-8")) + 1 for _, line, _ in lines[start - 1:end])

    first = heads[0][0] - 1 if heads else total
    sections: list[dict[str, object]] = [
        {"heading": "(preamble)", "level": 1, "lines": [1, first], "bytes": size(1, first)}
    ]
    for index, (start, level, title) in enumerate(heads):
        end = next((n - 1 for n, other, _ in heads[index + 1:] if other <= level), total)
        sections.append({"heading": title, "level": level, "lines": [start, end], "bytes": size(start, end)})
    return sections


def find_section(sections: list[dict[str, object]], title: str) -> dict[str, object] | None:
    """The shallowest, earliest section whose heading equals the title, ignoring case and backticks."""

    wanted = title.replace("`", "").strip().lower()
    matches = [item for item in sections[1:] if str(item["heading"]).lower() == wanted]
    return min(matches, key=lambda item: (item["level"], item["lines"][0])) if matches else None


@dataclass(frozen=True)
class FrontmatterIssue:
    line: int
    message: str


@dataclass(frozen=True)
class FrontmatterResult:
    data: dict[str, FrontmatterValue]
    issues: tuple[FrontmatterIssue, ...]
    end_line: int


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        quote = value[0]
        inner = value[1:-1]
        if quote == '"':
            return inner.replace('\\"', '"').replace("\\\\", "\\")
        return inner.replace("''", "'")
    return value

def _unsupported(value: str) -> bool:
    stripped = value.strip()
    if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in "\"'":
        return False
    return (
        bool(UNSUPPORTED_VALUE.match(stripped))
        or any(marker in stripped for marker in ("{", "}"))
        or bool(re.search(r"(^|\s)[&*!][A-Za-z0-9_-]+(?=\s|$)", stripped))
    )


def parse_frontmatter(text: str) -> FrontmatterResult:
    """Return frontmatter data plus deterministic syntax findings.

    Supported values are scalars and first-level lists. Dates remain strings.
    Complex YAML is intentionally rejected so FCVW stays dependency-free.
    """

    normalized = text.removeprefix("\ufeff")
    lines = normalized.splitlines()
    if not lines or lines[0].strip() != "---":
        return FrontmatterResult({}, (), 0)

    try:
        closing = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration:
        return FrontmatterResult({}, (FrontmatterIssue(1, "frontmatter closing delimiter is missing"),), 0)

    data: dict[str, FrontmatterValue] = {}
    issues: list[FrontmatterIssue] = []
    current_list: str | None = None

    for index in range(1, closing):
        line_number = index + 1
        raw = lines[index]
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue

        item = LIST_ITEM.match(raw)
        if item:
            if current_list is None:
                issues.append(FrontmatterIssue(line_number, "list item has no owning key"))
                continue
            raw_item = item.group(1).strip()
            if _unsupported(raw_item):
                issues.append(FrontmatterIssue(line_number, f"unsupported YAML construct for {current_list}"))
                continue
            if raw_item[:1] in {"\"", "'"} and not raw_item.endswith(raw_item[0]):
                issues.append(FrontmatterIssue(line_number, f"unterminated quoted scalar for {current_list}"))
                continue
            value = _unquote(raw_item)
            if not value:
                issues.append(FrontmatterIssue(line_number, f"empty list item for {current_list}"))
                continue
            target = data[current_list]
            if isinstance(target, list):
                target.append(value)
            continue

        if raw[:1].isspace():
            issues.append(FrontmatterIssue(line_number, "nested or indented YAML mappings are not supported"))
            current_list = None
            continue

        if ":" not in raw:
            issues.append(FrontmatterIssue(line_number, "frontmatter entry must use key: value"))
            current_list = None
            continue

        key, raw_value = raw.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if not KEY.fullmatch(key):
            issues.append(FrontmatterIssue(line_number, f"invalid frontmatter key: {key!r}"))
            current_list = None
            continue
        if key in data:
            issues.append(FrontmatterIssue(line_number, f"duplicate frontmatter key: {key}"))
            current_list = None
            continue
        if raw_value.startswith("[") and raw_value.endswith("]"):
            if raw_value != "[]":
                issues.append(FrontmatterIssue(line_number, f"inline lists are not supported for {key}"))
                data[key] = []
            else:
                data[key] = []
            current_list = None
            continue
        if not raw_value:
            data[key] = []
            current_list = key
            continue
        if raw_value[:1] in {"\"", "'"} and not raw_value.endswith(raw_value[0]):
            issues.append(FrontmatterIssue(line_number, f"unterminated quoted scalar for {key}"))
        if _unsupported(raw_value):
            issues.append(FrontmatterIssue(line_number, f"unsupported YAML construct for {key}"))
        data[key] = _unquote(raw_value)
        current_list = None

    return FrontmatterResult(data, tuple(issues), closing + 1)


def scalar(metadata: dict[str, FrontmatterValue], key: str, default: str = "") -> str:
    value = metadata.get(key, default)
    return value if isinstance(value, str) else default


def string_list(metadata: dict[str, FrontmatterValue], key: str) -> list[str]:
    value = metadata.get(key, [])
    if isinstance(value, list):
        return list(value)
    if isinstance(value, str) and value:
        return [value]
    return []
