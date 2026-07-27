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
