#!/usr/bin/env python3
"""Regression tests for deterministic FCVW validator guardrails."""

from __future__ import annotations

import tempfile
import unittest
from datetime import date
from pathlib import Path

from validate_fcvw import (
    BaselineEntry,
    Finding,
    apply_legacy_baseline,
    load_legacy_baseline,
    validate_clean_template,
    validate_plans,
    validate_reading_routes,
    validate_skills,
)


VALID_REGRESSION = """
## Regression impact

### Existing behaviors that may be affected
- Plan lifecycle.

### Regression contracts consulted
- `PLANNING.md`.

### Regression checks required
- Validator replay.

### Regression evidence
| Check | Result | Evidence |
|---|---|---|
| Lifecycle | pass | unit fixture |

### Limitations and residual risk
- None.
"""


class ValidatorRegressionTests(unittest.TestCase):
    def make_root(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        for state in ("pending", "in_progress", "completed", "discontinued"):
            (root / "FCVW" / "Plans" / state).mkdir(parents=True, exist_ok=True)
        return temporary, root

    def write_plan(
        self,
        root: Path,
        regression_body: str,
        status: str = "completed",
        regression_contract: str = "required",
    ) -> None:
        plan_id = "P3-R2-2026-07-15-validator-regression-fixture"
        content = f'''---
schema: "fcvw/plan@2"
id: "{plan_id}"
status: "{status}"
priority: "P3"
risk: "R2"
created_at: "2026-07-15"
updated_at: "2026-07-15"
current_version: "V0.13.0"
expected_version: "V0.13.0"
owner: "test"
regression_contract: "{regression_contract}"
context_files:
  - "FCVW/PLANNING.md"
---

# Fixture
{regression_body}
'''
        (root / "FCVW" / "Plans" / status / f"{plan_id}.md").write_text(content, encoding="utf-8")

    def test_valid_plan2_regression_contract_passes(self) -> None:
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        self.write_plan(root, VALID_REGRESSION)
        findings: list[Finding] = []
        validate_plans(root, findings)
        self.assertEqual([], [item for item in findings if item.rule == "plan-regression"])

    def test_missing_regression_section_fails(self) -> None:
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        self.write_plan(root, "")
        findings: list[Finding] = []
        validate_plans(root, findings)
        self.assertTrue(any(item.rule == "plan-regression" for item in findings))

    def test_pending_evidence_in_completed_plan_fails(self) -> None:
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        self.write_plan(root, VALID_REGRESSION.replace("| pass |", "| pending |"))
        findings: list[Finding] = []
        validate_plans(root, findings)
        self.assertTrue(any("pending regression" in item.message for item in findings))

    def test_not_applicable_requires_specific_justification(self) -> None:
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        self.write_plan(
            root,
            "## Regression impact\n\nJustification: no\n",
            regression_contract="not_applicable",
        )
        findings: list[Finding] = []
        validate_plans(root, findings)
        self.assertTrue(any("specific Justification" in item.message for item in findings))

    def test_comparison_fixture_in_root_fails_clean_profile(self) -> None:
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        (root / "FCVW - Exemplo retirado de aplicação real").mkdir()
        findings: list[Finding] = []
        validate_clean_template(root, findings)
        self.assertTrue(any(item.path.startswith("FCVW - Exemplo") for item in findings))

    def test_unexpected_root_entry_fails_clean_profile(self) -> None:
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        (root / "production-export").mkdir()
        findings: list[Finding] = []
        validate_clean_template(root, findings)
        self.assertTrue(any(item.path == "production-export" for item in findings))

    def test_incomplete_skill_body_fails_contract(self) -> None:
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        skill_root = root / "FCVW" / "skills"
        (skill_root / "example").mkdir(parents=True)
        (skill_root / "README.md").write_text("# Skills\n\n`example`\n", encoding="utf-8")
        (skill_root / "example" / "SKILL.md").write_text(
            '''---
schema: "fcvw/skill@1"
name: "example"
description: "Incomplete fixture."
version: "1.0.0"
trigger_keywords:
  - "fixture"
session_types:
  - "test"
---
# Example

## Purpose
Test fixture.
''',
            encoding="utf-8",
        )
        findings: list[Finding] = []
        validate_skills(root, findings)
        self.assertTrue(any(item.rule == "skill-contract" for item in findings))

    def make_route_root(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / "FCVW" / "skills").mkdir(parents=True)
        (root / "AGENTS.md").write_text("# Agents\n\nRead `CONTEXT_MAP.md`.\n", encoding="utf-8")
        (root / "FCVW" / "README.md").write_text("# Index\n", encoding="utf-8")
        (root / "FCVW" / "CONTEXT_MAP.md").write_text("# Routes\n", encoding="utf-8")
        return temporary, root

    def test_orphan_framework_policy_fails_reading_routes(self) -> None:
        temporary, root = self.make_route_root()
        self.addCleanup(temporary.cleanup)
        (root / "FCVW" / "ORPHAN.md").write_text(
            '''---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---
# Orphan
''',
            encoding="utf-8",
        )
        findings: list[Finding] = []
        validate_reading_routes(root, findings)
        self.assertTrue(any(item.path.endswith("ORPHAN.md") for item in findings))

    def test_unmapped_skill_session_type_fails_reading_routes(self) -> None:
        temporary, root = self.make_route_root()
        self.addCleanup(temporary.cleanup)
        skill = root / "FCVW" / "skills" / "example"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            '''---
schema: "fcvw/skill@1"
name: "example"
description: "Route fixture."
version: "1.0.0"
trigger_keywords:
  - "fixture"
session_types:
  - "unmapped_fixture"
---
# Example
''',
            encoding="utf-8",
        )
        findings: list[Finding] = []
        validate_reading_routes(root, findings)
        self.assertTrue(any("unmapped skill session type" in item.message for item in findings))

    def test_routed_policy_missing_from_operational_index_fails(self) -> None:
        temporary, root = self.make_route_root()
        self.addCleanup(temporary.cleanup)
        (root / "AGENTS.md").write_text("# Agents\n\nRead `INDEXED.md`.\n", encoding="utf-8")
        (root / "FCVW" / "INDEXED.md").write_text(
            '''---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---
# Indexed only by route
''',
            encoding="utf-8",
        )
        findings: list[Finding] = []
        validate_reading_routes(root, findings)
        self.assertTrue(any(item.rule == "framework-index" for item in findings))

    def test_exact_legacy_baseline_accepts_matching_finding(self) -> None:
        entry = BaselineEntry(
            path="FCVW/STACK.md",
            rule="placeholder",
            message="instantiated profile contains placeholders",
            justification="Migration debt",
            owner="maintainer",
            review_due=date(2999, 12, 31),
        )
        finding = Finding("placeholder", "FCVW\\STACK.md", "instantiated profile contains placeholders")
        blocking, accepted, stale = apply_legacy_baseline([finding], [entry])
        self.assertEqual([], blocking)
        self.assertEqual([finding], accepted)
        self.assertEqual([], stale)

    def test_changed_finding_is_not_hidden_by_legacy_baseline(self) -> None:
        entry = BaselineEntry(
            path="FCVW/STACK.md",
            rule="placeholder",
            message="old exact message",
            justification="Migration debt",
            owner="maintainer",
            review_due=date(2999, 12, 31),
        )
        finding = Finding("placeholder", "FCVW/STACK.md", "changed violation")
        blocking, accepted, stale = apply_legacy_baseline([finding], [entry])
        self.assertEqual([finding], blocking)
        self.assertEqual([], accepted)
        self.assertTrue(any(item.rule == "baseline-stale" for item in stale))

    def test_baseline_configuration_error_cannot_be_baselined(self) -> None:
        entry = BaselineEntry(
            path="baseline.md",
            rule="baseline-config",
            message="invalid or missing baseline schema",
            justification="Invalid exception attempt",
            owner="maintainer",
            review_due=date(2999, 12, 31),
        )
        finding = Finding("baseline-config", "baseline.md", "invalid or missing baseline schema")
        blocking, accepted, _ = apply_legacy_baseline([finding], [entry])
        self.assertEqual([finding], blocking)
        self.assertEqual([], accepted)

    def test_expired_legacy_baseline_fails_configuration(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        path = Path(temporary.name) / "baseline.md"
        path.write_text(
            '''---
schema: "fcvw/legacy-baseline@1"
created_at: "2000-01-01"
review_due: "2000-01-02"
owner: "maintainer"
---

| Exact path | Rule ID | Existing finding | Justification | Owner | Review due |
|---|---|---|---|---|---|
| FCVW/STACK.md | placeholder | instantiated profile contains placeholders | Migration debt | maintainer | 2000-01-02 |
''',
            encoding="utf-8",
        )
        _, errors = load_legacy_baseline(path)
        self.assertTrue(any(item.rule == "baseline-expired" for item in errors))


if __name__ == "__main__":
    unittest.main()
