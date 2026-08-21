#!/usr/bin/env python3
"""Focused tests for plan dependencies and typed knowledge behavior."""

from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from build_context_index import build_index
from knowledge_graph_fcvw import build_knowledge_graph
from plan_queue_fcvw import recommend_next_plan, render_aggregate_queue, validate_plan_queues
from retrieve_context import bm25


class TemporaryRootTest(unittest.TestCase):
    def make_root(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return temporary, Path(temporary.name)


class PlanDependencyTests(TemporaryRootTest):
    @staticmethod
    def queue_text(state: str, rows: list[str]) -> str:
        return (
            "---\n"
            'schema: "fcvw/plan-queue@1"\n'
            'artifact_role: "project_profile"\n'
            'owner: "project"\n'
            'upgrade_strategy: "preserve"\n'
            f'state: "{state}"\n'
            'updated_at: "2026-08-21"\n'
            "---\n\n"
            "| Order | Plan | Category | Blocked by | Override reason |\n"
            "|---:|---|---|---|---|\n"
            + "\n".join(rows)
            + "\n"
        )

    @staticmethod
    def plan_text(
        plan_id: str,
        status: str,
        *,
        dependencies: list[str] | None = None,
        evidence: list[tuple[str, str, str]] | None = None,
    ) -> str:
        dependency_text = ""
        if dependencies is not None:
            dependency_text = "depends_on:\n" + "".join(f'  - "{item}"\n' for item in dependencies)
        body = "# Plan\n"
        if dependencies:
            body += (
                "\n## Dependency validation\n\n"
                "| Dependency | Blocking reason | Unblock criteria | Status | Evidence |\n"
                "|---|---|---|---|---|\n"
            )
            records = evidence or [(item, "pending", "pending") for item in dependencies]
            for dependency, state, proof in records:
                body += (
                    f"| {dependency} | Required sequencing contract | Observable prerequisite completion | "
                    f"{state} | {proof} |\n"
                )
        return (
            "---\n"
            'schema: "fcvw/plan@2"\n'
            f'id: "{plan_id}"\n'
            f'status: "{status}"\n'
            f'priority: "{plan_id[:2]}"\n'
            'risk: "R2"\n'
            + dependency_text
            + "---\n\n"
            + body
        )

    def setup_root(self) -> tuple[Path, dict[str, Path]]:
        _, root = self.make_root()
        states: dict[str, Path] = {}
        for state in ("pending", "in_progress", "completed", "discontinued"):
            states[state] = root / "FCVW" / "Plans" / state
            states[state].mkdir(parents=True)
        return root, states

    def write_empty_queues(self, states: dict[str, Path]) -> None:
        for state in ("pending", "in_progress"):
            (states[state] / "QUEUE.md").write_text(self.queue_text(state, []), encoding="utf-8")

    def test_completed_dependency_requires_and_accepts_evidence(self) -> None:
        root, states = self.setup_root()
        prerequisite = "P2-R2-2026-08-21-prerequisite"
        dependent = "P3-R2-2026-08-21-dependent"
        (states["completed"] / f"{prerequisite}.md").write_text(
            self.plan_text(prerequisite, "completed"), encoding="utf-8"
        )
        (states["pending"] / f"{dependent}.md").write_text(
            self.plan_text(
                dependent,
                "pending",
                dependencies=[prerequisite],
                evidence=[(prerequisite, "satisfied", "Plan validation table records passing checks")],
            ),
            encoding="utf-8",
        )
        (states["pending"] / "QUEUE.md").write_text(
            self.queue_text("pending", [f"| 1 | [{dependent}]({dependent}.md) | correction | none | none |"]),
            encoding="utf-8",
        )
        (states["in_progress"] / "QUEUE.md").write_text(self.queue_text("in_progress", []), encoding="utf-8")
        self.assertEqual([], validate_plan_queues(root))
        self.assertEqual(dependent, (recommend_next_plan(root) or (None, None))[1].plan_id)

        path = states["pending"] / f"{dependent}.md"
        path.write_text(path.read_text(encoding="utf-8").replace("Plan validation table records passing checks", "pending"), encoding="utf-8")
        self.assertTrue(any(item.rule == "plan-dependency-evidence" for item in validate_plan_queues(root)))

    def test_explicit_empty_dependency_list_needs_no_table(self) -> None:
        root, states = self.setup_root()
        plan_id = "P2-R2-2026-08-21-independent"
        (states["pending"] / f"{plan_id}.md").write_text(
            self.plan_text(plan_id, "pending", dependencies=[]), encoding="utf-8"
        )
        (states["pending"] / "QUEUE.md").write_text(
            self.queue_text("pending", [f"| 1 | [{plan_id}]({plan_id}.md) | correction | none | none |"]),
            encoding="utf-8",
        )
        (states["in_progress"] / "QUEUE.md").write_text(self.queue_text("in_progress", []), encoding="utf-8")
        self.assertEqual([], validate_plan_queues(root))

    def test_pending_and_invalidated_dependencies_remain_blocked(self) -> None:
        root, states = self.setup_root()
        prerequisite = "P2-R2-2026-08-21-prerequisite"
        dependent = "P3-R2-2026-08-21-dependent"
        (states["discontinued"] / f"{prerequisite}.md").write_text(
            self.plan_text(prerequisite, "discontinued"), encoding="utf-8"
        )
        (states["pending"] / f"{dependent}.md").write_text(
            self.plan_text(
                dependent,
                "pending",
                dependencies=[prerequisite],
                evidence=[(prerequisite, "invalidated", "Prerequisite was discontinued by owner decision")],
            ),
            encoding="utf-8",
        )
        (states["pending"] / "QUEUE.md").write_text(
            self.queue_text(
                "pending",
                [f"| 1 | [{dependent}]({dependent}.md) | correction | {prerequisite} | none |"],
            ),
            encoding="utf-8",
        )
        (states["in_progress"] / "QUEUE.md").write_text(self.queue_text("in_progress", []), encoding="utf-8")
        self.assertEqual([], validate_plan_queues(root))
        self.assertIsNone(recommend_next_plan(root))

    def test_cycles_and_queue_mismatch_fail(self) -> None:
        root, states = self.setup_root()
        first = "P2-R2-2026-08-21-first"
        second = "P3-R2-2026-08-21-second"
        (states["pending"] / f"{first}.md").write_text(
            self.plan_text(first, "pending", dependencies=[second]), encoding="utf-8"
        )
        (states["pending"] / f"{second}.md").write_text(
            self.plan_text(second, "pending", dependencies=[first]), encoding="utf-8"
        )
        (states["pending"] / "QUEUE.md").write_text(
            self.queue_text(
                "pending",
                [
                    f"| 1 | [{first}]({first}.md) | correction | none | none |",
                    f"| 2 | [{second}]({second}.md) | correction | {first} | none |",
                ],
            ),
            encoding="utf-8",
        )
        (states["in_progress"] / "QUEUE.md").write_text(self.queue_text("in_progress", []), encoding="utf-8")
        rules = {finding.rule for finding in validate_plan_queues(root)}
        self.assertIn("plan-dependency-cycle", rules)
        self.assertIn("plan-queue-dependency", rules)

    def test_aggregate_view_is_derived_from_both_queues(self) -> None:
        root, states = self.setup_root()
        active = "P2-R2-2026-08-21-active"
        pending = "P3-R2-2026-08-21-pending"
        (states["in_progress"] / f"{active}.md").write_text(self.plan_text(active, "in_progress"), encoding="utf-8")
        (states["pending"] / f"{pending}.md").write_text(self.plan_text(pending, "pending"), encoding="utf-8")
        (states["in_progress"] / "QUEUE.md").write_text(
            self.queue_text("in_progress", [f"| 1 | [{active}]({active}.md) | correction | none | none |"]), encoding="utf-8"
        )
        (states["pending"] / "QUEUE.md").write_text(
            self.queue_text("pending", [f"| 1 | [{pending}]({pending}.md) | correction | none | none |"]), encoding="utf-8"
        )
        rendered = render_aggregate_queue(root)
        self.assertIn(f"| in_progress | 1 | {active}", rendered)
        self.assertIn(f"| pending | 1 | {pending}", rendered)
        self.assertIn(f"{active} | correction | none | yes", rendered)


class KnowledgeGraphTests(TemporaryRootTest):
    @staticmethod
    def wiki_page(page_id: str, page_type: str, extra: str = "") -> str:
        return (
            "---\n"
            'schema: "fcvw/wiki@1"\n'
            f'id: "{page_id}"\n'
            'artifact_role: "record"\n'
            'owner: "team"\n'
            'upgrade_strategy: "preserve"\n'
            'record_scope: "application"\n'
            'retrieval_scope: "search_only"\n'
            f'title: "{page_id}"\n'
            f'type: "{page_type}"\n'
            'status: "validated"\n'
            'confidence: "high"\n'
            'maturity: "established"\n'
            'created_at: "2026-08-21"\n'
            'last_reviewed: "2026-08-21"\n'
            + extra
            + "sources:\n  - \"README.md\"\n"
            "tags:\n  - \"knowledge-governance\"\n"
            "---\n\n# Page\n\n## Content\n\nKnowledge content.\n"
        )

    def test_typed_edges_inverses_and_stale_review_candidates(self) -> None:
        _, root = self.make_root()
        wiki = root / "FCVW" / "wiki"
        wiki.mkdir(parents=True)
        tracked = root / "evidence.txt"
        tracked.write_text("version one", encoding="utf-8")
        digest = "sha256:" + hashlib.sha256(tracked.read_bytes()).hexdigest()
        source_extra = (
            'source_type: "repository_file"\n'
            'source_path: "../../evidence.txt"\n'
            f'source_digest: "{digest}"\n'
        )
        (wiki / "source.md").write_text(self.wiki_page("SRC-ONE", "source", source_extra), encoding="utf-8")
        knowledge_extra = 'derived_from:\n  - "SRC-ONE"\n'
        (wiki / "knowledge.md").write_text(self.wiki_page("KNOW-ONE", "concept", knowledge_extra), encoding="utf-8")

        graph = build_knowledge_graph(root)
        self.assertEqual([], [item for item in graph.findings if item.severity == "error"])
        relations = {(edge["relation"], edge["derived"]) for edge in graph.edges}
        self.assertIn(("derived_from", False), relations)
        self.assertIn(("source_for", True), relations)
        source_record = next(record for record in build_index(root) if record["path"] == "FCVW/wiki/source.md")
        self.assertEqual(digest, source_record["source_digest"])
        self.assertNotEqual(digest, source_record["chunk_hash"])

        tracked.write_text("version two", encoding="utf-8")
        rules = {item.rule for item in build_knowledge_graph(root).findings}
        self.assertIn("knowledge-source-stale", rules)
        self.assertIn("knowledge-review-candidate", rules)

    def test_missing_target_conflict_and_supersedes_cycle_fail(self) -> None:
        _, root = self.make_root()
        wiki = root / "FCVW" / "wiki"
        wiki.mkdir(parents=True)
        first_extra = (
            'supports:\n  - "SECOND"\n'
            'invalidates:\n  - "SECOND"\n'
            'supersedes:\n  - "SECOND"\n'
            'depends_on:\n  - "MISSING"\n'
        )
        second_extra = 'supersedes:\n  - "FIRST"\n'
        (wiki / "first.md").write_text(self.wiki_page("FIRST", "concept", first_extra), encoding="utf-8")
        (wiki / "second.md").write_text(self.wiki_page("SECOND", "concept", second_extra), encoding="utf-8")
        rules = {item.rule for item in build_knowledge_graph(root).findings}
        self.assertIn("knowledge-relation-target", rules)
        self.assertIn("knowledge-relation-conflict", rules)
        self.assertIn("knowledge-relation-cycle", rules)

    def test_index_metadata_and_bounded_graph_retrieval(self) -> None:
        _, root = self.make_root()
        wiki = root / "FCVW" / "wiki"
        wiki.mkdir(parents=True)
        (wiki / "alpha.md").write_text(
            self.wiki_page("ALPHA", "concept", 'supports:\n  - "BETA"\n'), encoding="utf-8"
        )
        (wiki / "beta.md").write_text(self.wiki_page("BETA", "concept"), encoding="utf-8")
        (wiki / "gamma.md").write_text(self.wiki_page("GAMMA", "concept"), encoding="utf-8")
        records = build_index(root)
        alpha = next(record for record in records if record["path"] == "FCVW/wiki/alpha.md")
        self.assertEqual("ALPHA", alpha["id"])
        self.assertEqual("established", alpha["maturity"])
        self.assertIn("supports", alpha["relationships"])
        self.assertEqual(alpha["chunk_hash"], alpha["content_hash"])

        for record in records:
            if record["path"] == "FCVW/wiki/alpha.md":
                record["content"] += " alpha-only-token"
        graph = build_knowledge_graph(root).as_dict()
        graph["edges"].append(
            {
                "source_path": "FCVW/wiki/beta.md",
                "relation": "supports",
                "target_path": "FCVW/wiki/gamma.md",
                "derived": False,
            }
        )
        result = bm25(
            "alpha-only-token",
            records,
            top_k=3,
            types={"concept"},
            tags={"knowledge-governance"},
            maturities={"established"},
            knowledge_graph=graph,
            graph_relations={"supports"},
            graph_limit=1,
        )
        paths = {str(item["path"]) for item in result}
        self.assertIn("FCVW/wiki/alpha.md", paths)
        self.assertIn("FCVW/wiki/beta.md", paths)
        self.assertNotIn("FCVW/wiki/gamma.md", paths)
        self.assertTrue(any(item["selection"] == "graph" for item in result))


class WikiLintContractTests(unittest.TestCase):
    def test_semantic_review_remains_bounded_non_mutating_and_non_gating(self) -> None:
        root = Path(__file__).resolve().parents[1]
        contract = (root / "FCVW" / "skills" / "wiki-lint" / "SKILL.md").read_text(encoding="utf-8").lower()

        self.assertIn("source-bounded", contract)
        self.assertIn("never rewrite, validate, supersede, invalidate, or refresh a digest automatically", contract)
        self.assertIn("do not make semantic findings a release gate", contract)
        self.assertIn("report semantic review as unavailable", contract)


if __name__ == "__main__":
    unittest.main()
