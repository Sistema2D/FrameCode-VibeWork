#!/usr/bin/env python3
"""Select the validation gates a change needs from the surfaces its diff touches.

TESTS.md asks for evidence proportional to risk and surface, but before V0.24.0
nothing turned that into a procedure: a commit that only added plans ran the same
type check, build and full test suite as a backend change (about two minutes and
thousands of output lines with no causal path to the Markdown that changed).

The project declares its surfaces once, in PROJECT.md after the
`<a id="validation-gates"></a>` anchor:

    | Surface | Paths | Gates |
    |---|---|---|
    | governance | `FCVW/**/*.md`, `AGENTS.md` | `git diff --check`, `python FCVW/tools/validate_fcvw.py --root . --since HEAD` |
    | frontend | `src/**` | `npx tsc --noEmit`, `npm run build` |
    | full | | `npm run lint`, `npm run build`, `npm test` |

The selection is conservative: a changed path that matches no surface, an
active plan at risk R4/R5 (or `--risk`), or `--release` selects `full`. This
tool prints commands; it never runs them.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

from frontmatter_fcvw import parse_frontmatter, scalar, scan_fences
from path_policy_fcvw import matches_ungoverned

ANCHOR = '<a id="validation-gates"></a>'
FULL = "full"
SURFACE_NAME = re.compile(r"^[a-z][a-z0-9_-]*$")
CODE_SPAN = re.compile(r"`([^`]+)`")
PLACEHOLDER = re.compile(r"<[A-Za-z][^>\n]*>")
HIGH_RISKS = {"R4", "R5"}
# Used when the project declares no table: only governance Markdown is known to
# be free of build and runtime consumers; everything else is `full`.
DEFAULT_SURFACES = (
    ("governance", ("FCVW/**/*.md", "AGENTS.md"), (
        "git diff --check",
        "python FCVW/tools/validate_fcvw.py --root . --since HEAD",
        "python FCVW/tools/plan_queue_fcvw.py --root . --recommend",
    )),
)


@dataclass(frozen=True)
class Surface:
    name: str
    paths: tuple[str, ...]
    gates: tuple[str, ...]


@dataclass
class GateTable:
    declared: bool
    surfaces: list[Surface] = field(default_factory=list)
    full: tuple[str, ...] = ()
    problems: list[str] = field(default_factory=list)


def _cells(row: str) -> list[str]:
    body = row.strip().strip("|")
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", body)]


def read_gate_table(root: Path) -> GateTable:
    """Parse the declared table; rows that still hold placeholders are skipped."""

    profile = root / "FCVW" / "PROJECT.md"
    if not profile.is_file():
        return GateTable(declared=False)
    text = profile.read_text(encoding="utf-8-sig")
    lines = [line for _, line, kind in scan_fences(text)[0] if kind == "text"]
    try:
        start = next(index for index, line in enumerate(lines) if ANCHOR in line)
    except StopIteration:
        return GateTable(declared=False)
    rows: list[str] = []
    for line in lines[start + 1:]:
        stripped = line.strip()
        if stripped.startswith("|"):
            rows.append(stripped)
        elif rows or stripped.startswith("#"):
            break
    table = GateTable(declared=True)
    body = [row for row in rows[2:] if not re.fullmatch(r"\|(?:\s*:?-{3,}:?\s*\|)+", row)]
    seen: set[str] = set()
    for row in body:
        if PLACEHOLDER.search(row):
            continue
        cells = _cells(row)
        if len(cells) != 3:
            table.problems.append(f"gate row must have Surface, Paths and Gates: {row[:60]}")
            continue
        name = cells[0].strip("` ").lower()
        paths = tuple(CODE_SPAN.findall(cells[1]))
        gates = tuple(CODE_SPAN.findall(cells[2]))
        if not SURFACE_NAME.match(name):
            table.problems.append(f"invalid surface name: {cells[0]!r}")
            continue
        if name in seen:
            table.problems.append(f"duplicate surface: {name}")
            continue
        seen.add(name)
        if not gates:
            table.problems.append(f"surface {name} declares no gate command (use inline code)")
        if name == FULL:
            table.full = gates
            continue
        if not paths:
            table.problems.append(f"surface {name} declares no path pattern (use inline code)")
        table.surfaces.append(Surface(name, paths, gates))
    if body and FULL not in seen and not any(PLACEHOLDER.search(row) for row in body):
        table.problems.append("the table must declare a `full` row: the complete gate set")
    return table


def changed_paths(root: Path, since: str) -> list[str]:
    """Paths changed since a revision, plus untracked files, as repository paths."""

    commands = (
        ["git", "-C", str(root), "-c", "core.quotepath=off", "diff", "--name-only", since],
        ["git", "-C", str(root), "-c", "core.quotepath=off", "ls-files", "--others", "--exclude-standard"],
    )
    found: set[str] = set()
    for command in commands:
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=60, check=False)
        if result.returncode != 0:
            raise ValueError(result.stderr.strip() or f"git failed: {' '.join(command[3:])}")
        found.update(line.strip() for line in result.stdout.splitlines() if line.strip())
    return sorted(found)


def active_risk(root: Path) -> str:
    """Highest risk among in-progress plans: the conservative reading."""

    risks = []
    for path in (root / "FCVW" / "Plans" / "in_progress").glob("*.md"):
        risk = scalar(parse_frontmatter(path.read_text(encoding="utf-8-sig")).data, "risk")
        if re.fullmatch(r"R[1-5]", risk):
            risks.append(risk)
    return max(risks, default="")


def select_gates(table: GateTable, paths: list[str], *, risk: str = "", release: bool = False) -> dict:
    surfaces = table.surfaces if table.declared else [Surface(*item) for item in DEFAULT_SURFACES]
    matched: dict[str, list[str]] = {}
    unmatched: list[str] = []
    for path in paths:
        hits = [surface.name for surface in surfaces if matches_ungoverned(path, list(surface.paths))]
        if not hits:
            unmatched.append(path)
        for name in hits:
            matched.setdefault(name, []).append(path)
    escalation: list[str] = []
    if unmatched:
        escalation.append(f"{len(unmatched)} changed path(s) match no declared surface")
    if risk in HIGH_RISKS:
        escalation.append(f"risk {risk}")
    if release:
        escalation.append("release")
    gates: list[str] = []
    if escalation:
        gates.extend(table.full or ("<complete project gate set: declare a `full` row in PROJECT.md>",))
    for surface in surfaces:
        if surface.name in matched:
            gates.extend(gate for gate in surface.gates if gate not in gates)
    return {
        "declared_table": table.declared,
        "changed": paths,
        "surfaces": matched,
        "unmatched": unmatched,
        "risk": risk or None,
        "escalation": escalation,
        "decision": FULL if escalation else (",".join(sorted(matched)) or "none"),
        "gates": gates,
        "problems": table.problems,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--root", default=".")
    parser.add_argument("--since", default="HEAD", help="git revision to diff against (default: HEAD, plus untracked)")
    parser.add_argument("--paths", nargs="+", help="explicit repository paths instead of the git diff")
    parser.add_argument("--risk", choices=[f"R{level}" for level in range(1, 6)],
                        help="override the risk read from in-progress plans")
    parser.add_argument("--release", action="store_true", help="release or publication work: always full")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    table = read_gate_table(root)
    try:
        paths = sorted(item.replace("\\", "/") for item in args.paths) if args.paths else changed_paths(root, args.since)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"ERROR [project-gates] cannot list changed paths: {error}")
        return 2
    report = select_gates(table, paths, risk=args.risk or active_risk(root), release=args.release)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for problem in report["problems"]:
            print(f"ERROR [project-gates] FCVW/PROJECT.md: {problem}")
        for name, files in report["surfaces"].items():
            print(f"- {name} ({len(files)}): {', '.join(files[:5])}{' ...' if len(files) > 5 else ''}")
        if report["unmatched"]:
            print(f"- unmatched ({len(report['unmatched'])}): {', '.join(report['unmatched'][:5])}")
        for reason in report["escalation"]:
            print(f"ESCALATE {reason}: full gate set")
        for gate in report["gates"]:
            print(f"RUN {gate}")
        source = "PROJECT.md" if table.declared else "built-in governance surface (no table declared)"
        print(f"FCVW gates: changed={len(paths)} decision={report['decision']} gates={len(report['gates'])} "
              f"source={source}")
    return 2 if report["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
