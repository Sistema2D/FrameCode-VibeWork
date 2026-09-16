#!/usr/bin/env python3
"""Inspect signed structural routing; suggestions never change delivered context."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
import re
from pathlib import Path, PurePosixPath

from knowledge_graph_fcvw import build_knowledge_graph
from document_graph_fcvw import build_graph
from frontmatter_fcvw import parse_frontmatter, scalar


SCHEMA = "fcvw/adaptive-structure@1"
RUN_SCHEMA = "fcvw/adaptive-shadow@1"
NOTICE = "Derived evidence only; no authority, learning, or production selection."
# Contradictions remain visible counterevidence. Only explicit obsolescence
# relationships inhibit a target, never the inverse relationship.
WEIGHTS = {"route_reference": 0.15, "document_link": 0.15, "related": 0.25, "supports": 0.5, "supported_by": 0.5,
           "depends_on": 0.5, "required_by": 0.25, "implements": 0.5,
           "implemented_by": 0.25, "derived_from": 0.5, "source_for": 0.25,
           "canonical_page": 0.5, "canonical_for": 0.25,
           "contradicts": 0.25, "invalidates": -0.5, "supersedes": -0.5}
MAX_NODES, MAX_EDGES, MAX_CANDIDATES = 20000, 100000, 20


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(",", ":")).encode()).hexdigest()


def safe_path(value: object) -> bool:
    return (isinstance(value, str) and bool(value) and "\\" not in value
            and ":" not in value and not PurePosixPath(value).is_absolute()
            and all(part not in {".", "..", ""} for part in value.split("/")))


def structural_graph(root: Path) -> dict:
    """Rebuild from governed sources, never from a persisted adaptive cache."""
    root = root.resolve()
    # Existing graph discovery follows paths; reject symlinks before invoking it.
    for path in root.rglob("*.md"):
        if any(part in {".git", ".fcvw-cache", "__pycache__"} for part in path.parts):
            continue
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError("graph source escapes root or is a symlink")
    knowledge = build_knowledge_graph(root)
    if any(item.severity == "error" for item in knowledge.findings):
        raise ValueError("knowledge graph has blocking findings; validate sources first")
    documents = build_graph(root)
    canonical = set()
    for name in documents.nodes:
        if not safe_path(name):
            raise ValueError("invalid document path")
        metadata = parse_frontmatter((root / name).read_text(encoding="utf-8-sig")).data
        if name == "AGENTS.md" or scalar(metadata, "artifact_role") in {
                "framework_policy", "framework_lock", "project_profile"}:
            canonical.add(name)
    nodes = sorted(canonical | {str(node["path"]) for node in knowledge.nodes})
    typed = {(str(edge["source_path"]), str(edge["target_path"]),
                    str(edge["relation"])) for edge in knowledge.edges
                   if edge["relation"] in WEIGHTS}
    edges = sorted(typed | {(s, t, "document_link") for s in canonical
                            for t in documents.outgoing.get(s, ()) if t in canonical and s != t})
    # Path references are structural evidence, not an automatic event classifier.
    route_edges = set()
    for source in ("AGENTS.md", "FCVW/CONTEXT_MAP.md"):
        for target in re.findall(r"`([^`\n]+\.md)`", (root / source).read_text(encoding="utf-8-sig")):
            target = target if target.startswith("FCVW/") or target == "AGENTS.md" else "FCVW/" + target
            if target in canonical and source != target:
                route_edges.add((source, target, "route_reference"))
    edges = sorted(set(edges) | route_edges)
    sources = {}
    for name in sorted(set(nodes) | {"AGENTS.md", "FCVW/CONTEXT_MAP.md"}):
        if not safe_path(name):
            raise ValueError("invalid source path")
        path = root / name
        if not path.is_file():
            raise ValueError("missing structural source")
        sources[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    result = {"schema": SCHEMA, "authority": "derived", "authority_notice": NOTICE,
              "source_hash": digest(sources), "nodes": nodes,
              "edges": [{"source": s, "target": t, "relation": r,
                         "weight": WEIGHTS[r]} for s, t, r in edges]}
    result["structural_hash"] = digest(result)
    validate_structure(result)
    return result


def validate_structure(graph: dict) -> None:
    if (not isinstance(graph, dict) or graph.get("schema") != SCHEMA
            or graph.get("authority") != "derived"):
        raise ValueError("invalid structural schema or authority")
    nodes, edges = graph.get("nodes"), graph.get("edges")
    if (not isinstance(nodes, list) or len(nodes) > MAX_NODES
            or not all(safe_path(n) for n in nodes)
            or len(set(nodes)) != len(nodes) or not isinstance(edges, list)
            or len(edges) > MAX_EDGES):
        raise ValueError("invalid graph size or nodes")
    known, seen = set(nodes), set()
    for edge in edges:
        if not isinstance(edge, dict):
            raise ValueError("invalid edge")
        s, t, r = (edge.get(key) for key in ("source", "target", "relation"))
        if not all(isinstance(v, str) for v in (s, t, r)):
            raise ValueError("invalid edge fields")
        if (s not in known or t not in known or s == t or r not in WEIGHTS
                or type(edge.get("weight")) not in {int, float}
                or edge["weight"] != WEIGHTS[r] or (s, t, r) in seen):
            raise ValueError("invalid edge endpoints, relation or weight")
        seen.add((s, t, r))
    expected = digest({k: v for k, v in graph.items() if k != "structural_hash"})
    if graph.get("structural_hash") != expected:
        raise ValueError("structural hash mismatch")


def analyze(graph: dict) -> dict:
    validate_structure(graph)
    incoming, outgoing = Counter(), Counter()
    adjacent = defaultdict(set)
    for e in graph["edges"]:
        s, t = e["source"], e["target"]
        outgoing[s] += 1
        incoming[t] += 1
        adjacent[s].add(t)
        adjacent[t].add(s)
    unseen, components = set(graph["nodes"]), []
    while unseen:
        stack, size = [min(unseen)], 0
        unseen.remove(stack[0])
        while stack:
            node = stack.pop()
            size += 1
            for neighbor in sorted(adjacent[node] & unseen):
                unseen.remove(neighbor)
                stack.append(neighbor)
        components.append(size)
    pairs = {(e["source"], e["target"]) for e in graph["edges"]}
    return {"schema": "fcvw/adaptive-analysis@1", "authority_notice": NOTICE,
            "structural_hash": graph["structural_hash"],
            "nodes": len(graph["nodes"]), "edges": len(graph["edges"]),
            "negative_edges": sum(e["weight"] < 0 for e in graph["edges"]),
            "weak_component_sizes": sorted(components, reverse=True),
            "isolated_nodes": sorted(n for n in graph["nodes"] if not adjacent[n]),
            "reciprocal_pairs": sum((t, s) in pairs for s, t in pairs) // 2,
            "integrators": sorted(incoming.items(), key=lambda x: (-x[1], x[0]))[:10],
            "broadcasters": sorted(outgoing.items(), key=lambda x: (-x[1], x[0]))[:10]}


def compare(baseline: list[str], proposed: list[str], mandatory: list[str],
            expected_mandatory: list[str] | None = None,
            useful_paths: list[str] | None = None) -> dict:
    a, b, m = set(baseline), set(proposed), set(mandatory)
    expected = set(expected_mandatory) if expected_mandatory is not None else m
    useful = set(useful_paths) if useful_paths is not None else None
    return {"mandatory_recall": len(m & expected) / len(expected) if expected else 1.0,
            "mandatory_reference": "provided" if expected_mandatory is None else "fixture",
            "optional_jaccard": len(a & b) / len(a | b) if a | b else 1.0,
            "optional_precision": (len(b & useful) / len(b) if b else 0.0)
            if useful is not None else None,
            "missing_useful_paths": sorted(useful - b - m) if useful is not None else None,
            "baseline_optional_count": len(a), "proposed_optional_count": len(b)}


def shadow_route(graph: dict, baseline: list[dict], mandatory: list[str], *,
                 hops: int = 2, budget: int = 2000, top_k: int = 8) -> dict:
    validate_structure(graph)
    if type(hops) is not int or not 0 <= hops <= 3 or type(budget) is not int or budget < 0:
        raise ValueError("hops must be 0..3 and budget must be nonnegative")
    if type(top_k) is not int or not 0 <= top_k <= MAX_CANDIDATES:
        raise ValueError("top_k must be 0..20")
    if len(baseline) > MAX_CANDIDATES:
        raise ValueError("candidate pool exceeds 20")
    # Only already eligible BM25/graph results enter the experiment. No new
    # candidate can bypass language, maturity, exact-only or exclusion filters.
    candidates = {}
    for record in baseline:
        path = record.get("path")
        if not safe_path(path) or not isinstance(record.get("score"), (int, float)):
            raise ValueError("invalid candidate")
        if not math.isfinite(record["score"]) or record["score"] < 0:
            raise ValueError("invalid candidate score")
        if path not in mandatory:
            if path not in candidates or (record["score"], str(record.get("excerpt", ""))) > (
                    candidates[path]["score"], str(candidates[path].get("excerpt", ""))):
                candidates[path] = record
    peak = max((r["score"] for r in candidates.values()), default=1) or 1
    base = {p: r["score"] / peak for p, r in candidates.items()}
    frontier = dict(base)
    excitation, inhibition, traces = defaultdict(float), defaultdict(float), defaultdict(list)
    adjacency = defaultdict(list)
    for edge in graph["edges"]:
        if edge["source"] in candidates and edge["target"] in candidates:
            adjacency[edge["source"]].append(edge)
    for hop in range(1, hops + 1):
        following = defaultdict(float)
        for source in sorted(frontier):
            edges = adjacency[source]
            for edge in sorted(edges, key=lambda e: (e["target"], e["relation"])):
                target = edge["target"]
                amount = frontier[source] * abs(edge["weight"]) * 0.5 / len(edges)
                if edge["weight"] < 0:
                    inhibition[target] += amount
                else:
                    excitation[target] += amount
                    following[target] += amount
                traces[target].append({"from": source, "relation": edge["relation"],
                                       "hop": hop, "signed_contribution": round(
                                           amount if edge["weight"] > 0 else -amount, 8)})
        # Inhibition terminates: a negative edge never becomes excitation at hop 2.
        frontier = following
    ranked = []
    for path, record in candidates.items():
        score = max(0, base[path] + excitation[path] - inhibition[path])
        ranked.append({"path": path, "score": round(score, 8),
                       "base": round(base[path], 8), "excitation": round(excitation[path], 8),
                       "inhibition": round(inhibition[path], 8), "trace": traces[path],
                       "estimated_excerpt_tokens": (len(str(record.get("excerpt", ""))) + 3) // 4})
    ranked.sort(key=lambda r: (-r["score"], r["path"]))
    remaining, selected = budget, []
    for item in ranked:
        cost = item["estimated_excerpt_tokens"]
        reason = ("nonpositive" if item["score"] <= 0 else "top_k" if len(selected) >= top_k
                  else "budget" if cost > remaining else "selected")
        item["decision"] = reason
        if reason == "selected":
            selected.append(item["path"])
            remaining -= cost
    mandatory = list(dict.fromkeys(mandatory))
    return {"schema": RUN_SCHEMA, "mode": "shadow", "authority_notice": NOTICE,
            "structural_hash": graph["structural_hash"], "mandatory_paths": mandatory,
            "proposed_optional_paths": selected, "candidates": ranked,
            "estimated_optional_excerpt_tokens": budget - remaining,
            "token_estimator": "ceil(excerpt Unicode characters / 4); not model tokens or full files",
            "metrics": compare(list(candidates), selected, mandatory)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build", "analyze", "compare"])
    parser.add_argument("--root", default=".")
    parser.add_argument("--baseline", help="JSON list of baseline optional paths")
    parser.add_argument("--proposed", help="JSON list of proposed optional paths")
    parser.add_argument("--mandatory", action="append", default=[])
    parser.add_argument("--expected-mandatory", action="append")
    parser.add_argument("--useful", action="append")
    args = parser.parse_args()
    try:
        if args.command == "compare":
            if not args.baseline or not args.proposed:
                parser.error("compare requires --baseline and --proposed")
            values = [json.loads(Path(p).read_text(encoding="utf-8-sig"))
                      for p in (args.baseline, args.proposed)]
            if any(not isinstance(v, list) or not all(safe_path(p) for p in v) for v in values):
                raise ValueError("comparison inputs must be JSON lists of relative paths")
            result = compare(*values, args.mandatory, args.expected_mandatory, args.useful)
        else:
            graph = structural_graph(Path(args.root))
            result = graph if args.command == "build" else analyze(graph)
    except (OSError, ValueError) as error:
        parser.exit(1, f"adaptive routing unavailable: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
