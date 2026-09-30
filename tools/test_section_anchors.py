#!/usr/bin/env python3
"""Section ranges, link anchors, link successors, section digests and evidence provenance (V0.21.0)."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from context_routing_fcvw import named_sections, resolve_routes, section_ranges, selective_rows
from frontmatter_fcvw import find_section, heading_anchors, markdown_sections
from knowledge_graph_fcvw import build_knowledge_graph
from knowledge_sources_fcvw import section_bytes
from release_layout_fcvw import governed_root
from validate_fcvw import (
    Finding,
    check_evidence,
    fix_moved_plan_links,
    validate_anchors,
    validate_markdown,
)


ROOT = governed_root(Path(__file__))


class TemporaryRoot(unittest.TestCase):
    def make_root(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "FCVW").mkdir()
        return root


class SectionRangeTests(TemporaryRoot):
    def test_outline_ranges_cover_nested_headings_and_skip_fences(self) -> None:
        text = "---\nx: 1\n---\n# T\n\nintro\n\n## A\n\na\n\n### A1\n\n```md\n## not a heading\n```\n\n## B\n\nb\n"
        sections = markdown_sections(text)
        self.assertEqual(["(preamble)", "A", "A1", "B"], [item["heading"] for item in sections])
        self.assertEqual([8, 17], find_section(sections, "a")["lines"])
        self.assertEqual([18, 20], find_section(sections, "B")["lines"])

    def test_every_named_section_in_the_source_map_resolves(self) -> None:
        for path, (hint, _) in selective_rows(ROOT).items():
            names, _ = named_sections(hint)
            self.assertTrue(names, path)
            outline = markdown_sections((ROOT / path).read_text(encoding="utf-8"))
            missing = [name for name in names if find_section(outline, name) is None]
            self.assertEqual([], missing, path)

    def test_routes_report_first_read_ranges_smaller_than_whole_files(self) -> None:
        routing = resolve_routes(ROOT, sessions=["feature"], events=["security"])
        paths = ["AGENTS.md", "FCVW/CONTEXT_MAP.md", *routing["mandatory_paths"]]
        result = section_ranges(ROOT, paths)
        ranges = result["ranges"]
        self.assertIn("FCVW/CONTEXT_MAP.md", ranges)
        self.assertEqual([], [path for path, value in ranges.items() if value["unresolved"]])
        self.assertLess(result["context_bytes"]["first_read"], result["context_bytes"]["whole_files"])
        self.assertTrue(ranges["FCVW/PROJECT.md"]["alternatives"])

    def test_unresolved_heading_falls_back_to_the_whole_file(self) -> None:
        root = self.make_root()
        (root / "FCVW" / "CONTEXT_MAP.md").write_text(
            "# Map\n\n## Selective loading for long documents\n\n| Document | First | Expand |\n|---|---|---|\n"
            "| `DOC.md` | `Gone` and `Kept` | never |\n",
            encoding="utf-8",
        )
        (root / "FCVW" / "DOC.md").write_text("# Doc\n\n## Kept\n\nbody\n", encoding="utf-8")
        entry = section_ranges(root, ["FCVW/DOC.md"])["ranges"]["FCVW/DOC.md"]
        self.assertEqual(["Gone"], entry["unresolved"])
        self.assertEqual(entry["file_bytes"], entry["first_read_bytes"])

    def test_cli_route_output_carries_ranges(self) -> None:
        script = str(Path(__file__).with_name("retrieve_context.py"))
        run = subprocess.run([sys.executable, "-B", script, "--root", str(ROOT), "--session", "planning"],
                             capture_output=True, text=True)
        self.assertEqual(0, run.returncode, run.stderr)
        routing = json.loads(run.stdout)["routing"]
        self.assertIn("FCVW/PLANNING.md", routing["ranges"])
        self.assertIn("whole_files", routing["context_bytes"])


class AnchorAndSuccessorTests(TemporaryRoot):
    def run_rules(self, root: Path) -> list[Finding]:
        findings: list[Finding] = []
        validate_markdown(root, findings)
        validate_anchors(root, findings)
        return findings

    def test_anchor_forms(self) -> None:
        root = self.make_root()
        (root / "FCVW" / "DOC.md").write_text(
            '# Doc\n\n<a id="custom"></a>\n\n## Plan — `fcvw/plan@2`\n\n## Same\n\n## Same\n', encoding="utf-8"
        )
        (root / "FCVW" / "LINKS.md").write_text(
            "# Links\n\n[a](DOC.md#plan--fcvwplan2) [b](DOC.md#custom) [c](DOC.md#same-1) "
            "[d](DOC.md#Plan%20—%20fcvw/plan@2) [e](#links) [f](DOC.md#missing) [g](#nowhere)\n",
            encoding="utf-8",
        )
        messages = [item.message for item in self.run_rules(root) if item.rule == "markdown-anchor"]
        self.assertEqual(2, len(messages), messages)
        self.assertTrue(any("#missing" in message for message in messages))
        self.assertTrue(any("#nowhere" in message for message in messages))

    def test_heading_anchors_count_duplicates(self) -> None:
        self.assertEqual({"a", "a-1", "a-2"}, heading_anchors("## A\n\n## A\n\n### A\n"))

    def test_moved_plan_is_named_and_fixed(self) -> None:
        root = self.make_root()
        plans = root / "FCVW" / "Plans" / "completed"
        plans.mkdir(parents=True)
        (plans / "P3-R2-2026-01-01-x.md").write_text("# Plan\n", encoding="utf-8")
        record = root / "FCVW" / "decisions"
        record.mkdir()
        (record / "ADR.md").write_text(
            "# ADR\n\n[plan](../Plans/in_progress/P3-R2-2026-01-01-x.md#plan)\n", encoding="utf-8"
        )
        messages = [item.message for item in self.run_rules(root) if item.rule == "markdown-link"]
        self.assertIn("plan moved, use ../Plans/completed/P3-R2-2026-01-01-x.md", messages[0])
        changes = fix_moved_plan_links(root)
        self.assertEqual(1, len(changes))
        self.assertIn("(../Plans/completed/P3-R2-2026-01-01-x.md#plan)", (record / "ADR.md").read_text(encoding="utf-8"))
        self.assertEqual([], [item for item in self.run_rules(root) if item.rule.startswith("markdown-")])

    def test_removed_framework_path_names_its_successor(self) -> None:
        root = self.make_root()
        (root / "FCVW" / "MIGRATIONS.md").write_text(
            "# M\n\n1. Step\n\n   | Removed | Consolidated into |\n   |---|---|\n   | `TOKEN_BUDGET.md` | `AI.md` |\n",
            encoding="utf-8",
        )
        (root / "FCVW" / "NOTE.md").write_text("# N\n\n[old](TOKEN_BUDGET.md)\n", encoding="utf-8")
        message = next(item.message for item in self.run_rules(root) if item.rule == "markdown-link")
        self.assertIn("now in AI.md", message)


class SectionDigestTests(TemporaryRoot):
    PAGE = (
        '---\nschema: "fcvw/wiki@1"\nid: "SRC-RULES"\nartifact_role: "record"\nowner: "team"\n'
        'upgrade_strategy: "preserve"\nrecord_scope: "application"\nretrieval_scope: "search_only"\n'
        'title: "Rules"\ntype: "source"\nstatus: "validated"\nconfidence: "high"\n'
        'created_at: "2026-09-30"\nlast_reviewed: "2026-09-30"\nsource_type: "repository_file"\n'
        'source_path: "FCVW/APP_RULES.md#app-rule-001"\nsource_digest: "{digest}"\n'
        'sources:\n  - "FCVW/APP_RULES.md"\ntags:\n  - "quality-validation"\n---\n\n# Rules\n\n[Rules](../APP_RULES.md)\n'
    )

    def test_edit_outside_the_anchored_section_is_not_stale(self) -> None:
        root = self.make_root()
        rules = root / "FCVW" / "APP_RULES.md"
        rules.write_text("# Rules\n\n## APP-RULE-001\n\nOne.\n\n## APP-RULE-002\n\nTwo.\n", encoding="utf-8")
        digest = "sha256:" + hashlib.sha256(section_bytes(rules.read_text(encoding="utf-8"), "app-rule-001")).hexdigest()
        (root / "FCVW" / "wiki").mkdir()
        (root / "FCVW" / "wiki" / "source.md").write_text(self.PAGE.format(digest=digest), encoding="utf-8")

        def rules_found() -> set[str]:
            return {item.rule for item in build_knowledge_graph(root).findings}

        self.assertNotIn("knowledge-source-stale", rules_found())
        rules.write_text(rules.read_text(encoding="utf-8").replace("Two.", "Two, edited."), encoding="utf-8")
        self.assertNotIn("knowledge-source-stale", rules_found())
        rules.write_text(rules.read_text(encoding="utf-8").replace("One.", "One, edited."), encoding="utf-8")
        self.assertIn("knowledge-source-stale", rules_found())
        rules.write_text("# Rules\n\n## APP-RULE-009\n\nOther.\n", encoding="utf-8")
        self.assertIn("knowledge-source", rules_found())


class EvidenceProvenanceTests(TemporaryRoot):
    def messages(self, root: Path, metadata: dict) -> list[str]:
        page = root / "FCVW" / "wiki" / "note.md"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text("# Note\n", encoding="utf-8")
        findings: list[Finding] = []
        check_evidence(root, page, metadata, findings)
        return [item.message for item in findings]

    def test_rules(self) -> None:
        root = self.make_root()
        (root / "tests").mkdir()
        (root / "tests" / "test_rule.py").write_text("", encoding="utf-8")
        validated = {"status": "validated"}
        self.assertEqual([], self.messages(root, {}))
        self.assertEqual([], self.messages(root, {**validated, "evidence_method": "test",
                                                  "verified_by": ["tests/test_rule.py::test_limit"]}))
        self.assertIn("ai_inference alone cannot validate a claim",
                      self.messages(root, {**validated, "evidence_method": "ai_inference"}))
        self.assertIn("validated claim requires verified_by evidence",
                      self.messages(root, {**validated, "evidence_method": "human_review"}))
        self.assertIn("invalid evidence_method: 'guess'", self.messages(root, {"evidence_method": "guess"}))
        missing = self.messages(root, {"evidence_method": "test", "verified_by": ["../outside.py", "P3-R2-2026-01-01-none"]})
        self.assertEqual(2, len(missing), missing)
        self.assertEqual([], self.messages(root, {"status": "draft", "evidence_method": "ai_inference"}))


if __name__ == "__main__":
    unittest.main()
