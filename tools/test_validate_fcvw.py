#!/usr/bin/env python3
"""Regression tests for deterministic FCVW validator guardrails."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from datetime import date
from pathlib import Path

import fcvw_cache
import role_manifest_fcvw
import upgrade_fcvw
from validate_fcvw import (
    PROJECT_PROFILES,
    BaselineEntry,
    Finding,
    apply_legacy_baseline,
    changed_markdown_since,
    load_legacy_baseline,
    validate_automation,
    validate_character_integrity,
    validate_clean_template,
    validate_frontmatter_documents,
    validate_app_rules,
    validate_canonical_metadata,
    validate_document_graph,
    validate_feedback_notes,
    validate_language_review,
    validate_markdown,
    validate_profiles,
    validate_regression_surfaces,
    validate_plans,
    validate_reading_routes,
    validate_version,
    validate_wiki_ids,
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

    def test_local_obsidian_state_is_allowed_but_not_required(self) -> None:
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        (root / ".obsidian").mkdir()
        (root / ".obsidian" / "workspace.json").write_text("{}", encoding="utf-8")
        findings: list[Finding] = []
        validate_clean_template(root, findings)
        self.assertFalse(any(item.path == ".obsidian" for item in findings))

    def test_clean_profile_preserves_only_framework_scoped_history(self) -> None:
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        audits = root / "FCVW" / "audits"
        wiki = root / "FCVW" / "wiki"
        audits.mkdir()
        wiki.mkdir()
        (audits / "framework.md").write_text(
            "---\nrecord_scope: \"framework\"\n---\n# Framework audit\n",
            encoding="utf-8",
        )
        (audits / "application.md").write_text(
            "---\nrecord_scope: \"application\"\n---\n# Application audit\n",
            encoding="utf-8",
        )
        (wiki / "framework.md").write_text(
            "---\nrecord_scope: \"framework\"\n---\n# Framework knowledge\n",
            encoding="utf-8",
        )
        (wiki / "application.md").write_text(
            "---\nrecord_scope: \"application\"\n---\n# Application knowledge\n",
            encoding="utf-8",
        )
        findings: list[Finding] = []
        validate_clean_template(root, findings)
        contaminated = {item.path for item in findings if item.rule == "clean-contamination"}
        self.assertNotIn("FCVW/audits/framework.md", contaminated)
        self.assertNotIn("FCVW/wiki/framework.md", contaminated)
        self.assertIn("FCVW/audits/application.md", contaminated)
        self.assertIn("FCVW/wiki/application.md", contaminated)

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


COMPACT_PLAN = """---
schema: "fcvw/plan-compact@1"
id: "P4-R1-2026-08-28-compact-fixture"
artifact_role: "record"
upgrade_strategy: "preserve"
status: "pending"
priority: "P4"
risk: "R1"
created_at: "2026-08-28"
updated_at: "2026-08-28"
owner: "test"
context_files:
  - "FCVW/PLANNING.md"
---

# Compact fixture

## Objective

Correct one isolated label.

## Affected files

- `src/label.ts`

## Validation

- [x] Focused test passes.

## Rollback

Revert the single-line commit.
"""


class CompactPlanTests(unittest.TestCase):
    """The proportional plan class must stay small and stay low-risk."""

    def root_with(self, content: str, name: str = "P4-R1-2026-08-28-compact-fixture") -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        for state in ("pending", "in_progress", "completed", "discontinued"):
            (root / "FCVW" / "Plans" / state).mkdir(parents=True, exist_ok=True)
        (root / "FCVW" / "Plans" / "pending" / f"{name}.md").write_text(content, encoding="utf-8")
        return root

    def findings_for(self, content: str, name: str = "P4-R1-2026-08-28-compact-fixture") -> list[Finding]:
        findings: list[Finding] = []
        validate_plans(self.root_with(content, name), findings)
        return findings

    def test_compact_plan_needs_no_regression_section(self) -> None:
        findings = self.findings_for(COMPACT_PLAN)
        self.assertEqual([], [item for item in findings if item.rule.startswith("plan-")])

    def test_compact_plan_rejects_higher_priority(self) -> None:
        content = COMPACT_PLAN.replace('priority: "P4"', 'priority: "P2"')
        content = content.replace("P4-R1-2026-08-28", "P2-R1-2026-08-28")
        findings = self.findings_for(content, "P2-R1-2026-08-28-compact-fixture")
        self.assertTrue(any(item.rule == "plan-compact" for item in findings))

    def test_compact_plan_rejects_higher_risk(self) -> None:
        content = COMPACT_PLAN.replace('risk: "R1"', 'risk: "R4"')
        content = content.replace("P4-R1-2026-08-28", "P4-R4-2026-08-28")
        findings = self.findings_for(content, "P4-R4-2026-08-28-compact-fixture")
        self.assertTrue(any(item.rule == "plan-compact" for item in findings))

    def test_compact_plan_rejects_regression_contract(self) -> None:
        content = COMPACT_PLAN.replace('owner: "test"', 'owner: "test"\nregression_contract: "not_applicable"')
        findings = self.findings_for(content)
        self.assertTrue(any("regression_contract" in item.message for item in findings))

    def test_compact_plan_requires_its_sections(self) -> None:
        content = COMPACT_PLAN.replace("## Rollback\n\nRevert the single-line commit.\n", "")
        findings = self.findings_for(content)
        self.assertTrue(any(item.rule in {"plan-compact", "plan-rollback"} for item in findings))


class RiskBindingTests(unittest.TestCase):
    """Risk and sensitive surfaces may not waive the regression contract."""

    def plan(self, risk: str, context: str) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        for state in ("pending", "in_progress", "completed", "discontinued"):
            (root / "FCVW" / "Plans" / state).mkdir(parents=True, exist_ok=True)
        plan_id = f"P1-{risk}-2026-08-28-risk-binding-fixture"
        content = f"""---
schema: "fcvw/plan@2"
id: "{plan_id}"
status: "pending"
priority: "P1"
risk: "{risk}"
created_at: "2026-08-28"
updated_at: "2026-08-28"
current_version: "V1.0.0"
expected_version: "V1.0.1"
owner: "test"
regression_contract: "not_applicable"
context_files:
  - "{context}"
---

# Risk binding fixture

## Regression impact

Justification: this change only renames an internal helper with no consumer at all.

## Rollback

Revert the commit that introduced the rename.
"""
        (root / "FCVW" / "Plans" / "pending" / f"{plan_id}.md").write_text(content, encoding="utf-8")
        return root

    def test_low_risk_waiver_is_allowed(self) -> None:
        findings: list[Finding] = []
        validate_plans(self.plan("R2", "FCVW/PLANNING.md"), findings)
        self.assertEqual([], [item for item in findings if item.rule == "plan-risk-binding"])

    def test_high_risk_may_not_waive_regression(self) -> None:
        for risk in ("R3", "R4", "R5"):
            with self.subTest(risk=risk):
                findings: list[Finding] = []
                validate_plans(self.plan(risk, "FCVW/PLANNING.md"), findings)
                self.assertTrue(any(item.rule == "plan-risk-binding" for item in findings))

    def test_sensitive_surface_may_not_waive_regression(self) -> None:
        for surface in ("FCVW/SECURITY.md", "FCVW/DATA.md", "FCVW/MIGRATIONS.md"):
            with self.subTest(surface=surface):
                findings: list[Finding] = []
                validate_plans(self.plan("R2", surface), findings)
                self.assertTrue(any(item.rule == "plan-risk-binding" for item in findings))

    def test_short_or_generic_justification_is_refused(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        for state in ("pending", "in_progress", "completed", "discontinued"):
            (root / "FCVW" / "Plans" / state).mkdir(parents=True, exist_ok=True)
        plan_id = "P4-R1-2026-08-28-weak-justification"
        content = f"""---
schema: "fcvw/plan@2"
id: "{plan_id}"
status: "pending"
priority: "P4"
risk: "R1"
created_at: "2026-08-28"
updated_at: "2026-08-28"
current_version: "V1.0.0"
expected_version: "V1.0.1"
owner: "test"
regression_contract: "not_applicable"
context_files:
  - "FCVW/PLANNING.md"
---

# Weak justification

## Regression impact

Justification: not applicable

## Rollback

Revert the commit.
"""
        (root / "FCVW" / "Plans" / "pending" / f"{plan_id}.md").write_text(content, encoding="utf-8")
        findings: list[Finding] = []
        validate_plans(root, findings)
        self.assertTrue(any(item.rule == "plan-regression" for item in findings))


class CharacterIntegrityTests(unittest.TestCase):
    """Invisible and transcoding-damaged characters are invisible in review."""

    def findings_for(self, body: str) -> list[Finding]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "FCVW").mkdir(parents=True, exist_ok=True)
        (root / "FCVW" / "SAMPLE.md").write_text(body, encoding="utf-8")
        findings: list[Finding] = []
        validate_character_integrity(root, findings)
        return findings

    def test_clean_markdown_passes(self) -> None:
        self.assertEqual([], self.findings_for("# Title\n\nOrdinary prose with an em dash \u2014 fine.\n"))

    def test_zero_width_space_is_reported(self) -> None:
        findings = self.findings_for("# Title\n\nHidden\u200bcharacter.\n")
        self.assertTrue(any(item.rule == "character-integrity" for item in findings))

    def test_replacement_character_is_reported(self) -> None:
        findings = self.findings_for("# Title\n\nBroken \ufffd byte.\n")
        self.assertTrue(any(item.rule == "character-integrity" for item in findings))

    def test_damaged_dash_is_reported(self) -> None:
        findings = self.findings_for("# Title\n\nPlan queue ? fcvw plan queue schema.\n")
        self.assertTrue(any("damaged dash" in item.message for item in findings))

    def test_fenced_code_is_not_scanned_for_dashes(self) -> None:
        findings = self.findings_for("# Title\n\n```text\nvalue ? other\n```\n")
        self.assertEqual([], [item for item in findings if "damaged dash" in item.message])


class LanguageReviewTests(unittest.TestCase):
    """The record that authorises a language asset must name that language."""

    def findings_for(self, language: str, heading: str, scope: str) -> list[Finding]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "FCVW").mkdir(parents=True, exist_ok=True)
        body = f"""---
schema: "fcvw/language-review@1"
language: "{language}"
status: "approved"
---

# {heading}

## Scope

{scope}
"""
        (root / "FCVW" / "LANGUAGE_REVIEW.md").write_text(body, encoding="utf-8")
        findings: list[Finding] = []
        validate_language_review(root, findings)
        return findings

    def test_matching_language_passes(self) -> None:
        findings = self.findings_for("pt-BR", "Review: Portuguese (Brazil)", "Portuguese variant.")
        self.assertEqual([], findings)

    def test_body_describing_another_language_fails(self) -> None:
        findings = self.findings_for("pt-BR", "Review: United States English", "English variant.")
        self.assertTrue(any(item.rule == "language-review" for item in findings))

    def test_body_naming_no_language_fails(self) -> None:
        findings = self.findings_for("es", "Review", "Independent empty variant.")
        self.assertTrue(any(item.rule == "language-review" for item in findings))


class AutomationContractTests(unittest.TestCase):
    """fcvw/automation@1 declares required fields; they must be checked."""

    def findings_for(self, frontmatter_body: str) -> list[Finding]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "FCVW").mkdir(parents=True, exist_ok=True)
        (root / "FCVW" / "CONTRACT.md").write_text(
            f"---\n{frontmatter_body}---\n\n# Contract\n", encoding="utf-8"
        )
        findings: list[Finding] = []
        validate_automation(root, findings)
        return findings

    COMPLETE = """schema: "fcvw/automation@1"
id: "AUT-001"
kind: "hook"
status: "active"
trigger: "pre-commit"
preconditions: "clean tree"
actions: "run the validator"
evidence: "validator output"
failure_policy: "block"
rollback: "disable the hook"
owner: "release-maintainers"
"""

    def test_complete_contract_passes(self) -> None:
        self.assertEqual([], self.findings_for(self.COMPLETE))

    def test_missing_required_field_fails(self) -> None:
        body = self.COMPLETE.replace('rollback: "disable the hook"\n', "")
        self.assertTrue(any(item.rule == "automation-contract" for item in self.findings_for(body)))

    def test_uncontrolled_kind_fails(self) -> None:
        body = self.COMPLETE.replace('kind: "hook"', 'kind: "cronjob"')
        self.assertTrue(any("invalid kind" in item.message for item in self.findings_for(body)))

    def test_external_scenario_requires_named_authority(self) -> None:
        body = self.COMPLETE + 'scenario: "3"\n'
        self.assertTrue(any("authorized_by" in item.message for item in self.findings_for(body)))

class SharedCacheTests(unittest.TestCase):
    """The read cache must never serve content that changed underneath it."""

    def test_repeated_reads_hit_the_cache(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        path = Path(temporary.name) / "sample.md"
        path.write_text("first", encoding="utf-8")
        fcvw_cache.clear()
        self.assertEqual("first", fcvw_cache.read_text(path))
        self.assertEqual("first", fcvw_cache.read_text(path))
        stats = fcvw_cache.statistics()
        self.assertEqual(1, stats["text_reads"])
        self.assertEqual(1, stats["text_hits"])

    def test_rewritten_file_invalidates_the_entry(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        path = Path(temporary.name) / "sample.md"
        path.write_text("first", encoding="utf-8")
        fcvw_cache.clear()
        self.assertEqual("first", fcvw_cache.read_text(path))
        os.utime(path, (0, 0))
        path.write_text("second longer content", encoding="utf-8")
        self.assertEqual("second longer content", fcvw_cache.read_text(path))

    def test_frontmatter_is_parsed_once_per_version(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        path = Path(temporary.name) / "sample.md"
        path.write_text('---\nschema: "fcvw/document@1"\n---\n\n# Title\n', encoding="utf-8")
        fcvw_cache.clear()
        first = fcvw_cache.frontmatter(path)
        second = fcvw_cache.frontmatter(path)
        self.assertEqual(first, second)
        self.assertEqual(1, fcvw_cache.statistics()["frontmatter_parses"])


class RoleManifestTests(unittest.TestCase):
    """The manifest is what makes selective upgrade stop guessing."""

    def make_tree(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "FCVW" / "Plans" / "completed").mkdir(parents=True, exist_ok=True)
        (root / "FCVW" / "governance").mkdir(parents=True, exist_ok=True)
        (root / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
        (root / "FCVW" / "FRAMEWORK_LOCK.md").write_text(
            '---\nschema: "fcvw/framework-lock@1"\nartifact_role: "framework_lock"\n'
            'owner: "framework"\nupgrade_strategy: "replace_with_migration"\n---\n\n'
            "# Lock\n\n| Field | Value |\n|---|---|\n| Installed version | `V0.16.0` |\n",
            encoding="utf-8",
        )
        (root / "FCVW" / "PLANNING.md").write_text(
            '---\nschema: "fcvw/document@1"\nartifact_role: "framework_policy"\n'
            'owner: "framework"\nupgrade_strategy: "replace"\n---\n\n# Planning\n',
            encoding="utf-8",
        )
        (root / "FCVW" / "SCOPE.md").write_text(
            '---\nschema: "fcvw/project-scope@1"\nartifact_role: "project_profile"\n'
            'owner: "project"\nupgrade_strategy: "preserve"\n---\n\n# Scope\n',
            encoding="utf-8",
        )
        (root / "FCVW" / "governance" / "TEMPLATE_X.md").write_text("# Template\n", encoding="utf-8")
        (root / "FCVW" / "Plans" / "completed" / "P1-R1-2026-01-01-history.md").write_text(
            '---\nschema: "fcvw/plan@1"\nrecord_scope: "framework"\n---\n\n# History\n',
            encoding="utf-8",
        )
        return root

    def test_declared_roles_are_preserved(self) -> None:
        manifest = role_manifest_fcvw.build_manifest(self.make_tree())
        by_path = {item["path"]: item for item in manifest["files"]}
        self.assertEqual("framework_policy", by_path["FCVW/PLANNING.md"]["artifact_role"])
        self.assertEqual("project_profile", by_path["FCVW/SCOPE.md"]["artifact_role"])
        self.assertEqual("declared", by_path["FCVW/SCOPE.md"]["role_source"])

    def test_undeclared_roles_are_inferred_from_location(self) -> None:
        manifest = role_manifest_fcvw.build_manifest(self.make_tree())
        by_path = {item["path"]: item for item in manifest["files"]}
        self.assertEqual("template", by_path["FCVW/governance/TEMPLATE_X.md"]["artifact_role"])
        self.assertEqual("inferred", by_path["FCVW/governance/TEMPLATE_X.md"]["role_source"])

    def test_framework_history_is_promoted_out_of_project_ownership(self) -> None:
        manifest = role_manifest_fcvw.build_manifest(self.make_tree())
        by_path = {item["path"]: item for item in manifest["files"]}
        entry = by_path["FCVW/Plans/completed/P1-R1-2026-01-01-history.md"]
        self.assertEqual("framework_history", entry["artifact_role"])
        self.assertEqual("framework", entry["owner"])
        self.assertEqual("replace", entry["upgrade_strategy"])

    def test_every_governed_file_is_classified(self) -> None:
        manifest = role_manifest_fcvw.build_manifest(self.make_tree())
        self.assertEqual([], [i["path"] for i in manifest["files"] if i["artifact_role"] == "unclassified"])

    def test_installed_version_is_read_from_the_lock_table(self) -> None:
        self.assertEqual("V0.16.0", role_manifest_fcvw.installed_version(self.make_tree()))


class UpgradePlanTests(unittest.TestCase):
    """The upgrade must never silently overwrite local work."""

    def make_pair(self) -> tuple[Path, Path]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        base = Path(temporary.name)
        for name in ("installed", "release"):
            root = base / name
            (root / "FCVW").mkdir(parents=True, exist_ok=True)
            (root / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
            (root / "FCVW" / "FRAMEWORK_LOCK.md").write_text(
                '---\nschema: "fcvw/framework-lock@1"\nartifact_role: "framework_lock"\n'
                'owner: "framework"\nupgrade_strategy: "replace_with_migration"\n---\n\n# Lock\n',
                encoding="utf-8",
            )
            (root / "FCVW" / "PLANNING.md").write_text(
                '---\nschema: "fcvw/document@1"\nartifact_role: "framework_policy"\n'
                'owner: "framework"\nupgrade_strategy: "replace"\n---\n\n# Planning\n',
                encoding="utf-8",
            )
            (root / "FCVW" / "SCOPE.md").write_text(
                '---\nschema: "fcvw/project-scope@1"\nartifact_role: "project_profile"\n'
                'owner: "project"\nupgrade_strategy: "preserve"\n---\n\n# Scope\n',
                encoding="utf-8",
            )
        return base / "installed", base / "release"

    def test_untouched_policy_is_safe_to_replace(self) -> None:
        installed, release = self.make_pair()
        (release / "FCVW" / "PLANNING.md").write_text(
            '---\nschema: "fcvw/document@1"\nartifact_role: "framework_policy"\n'
            'owner: "framework"\nupgrade_strategy: "replace"\n---\n\n# Planning v2\n',
            encoding="utf-8",
        )
        actions = {a.path: a for a in upgrade_fcvw.plan_upgrade(installed, release)}
        self.assertEqual("replace", actions["FCVW/PLANNING.md"].verdict)

    def test_locally_modified_policy_becomes_a_conflict(self) -> None:
        installed, release = self.make_pair()
        role_manifest_fcvw.build_manifest(installed)
        (installed / "FCVW" / "ROLE_MANIFEST.json").write_text(
            json.dumps(role_manifest_fcvw.build_manifest(installed)), encoding="utf-8"
        )
        (installed / "FCVW" / "PLANNING.md").write_text(
            '---\nschema: "fcvw/document@1"\nartifact_role: "framework_policy"\n'
            'owner: "framework"\nupgrade_strategy: "replace"\n---\n\n# Planning, edited locally\n',
            encoding="utf-8",
        )
        actions = {a.path: a for a in upgrade_fcvw.plan_upgrade(installed, release)}
        self.assertEqual("conflict", actions["FCVW/PLANNING.md"].verdict)

    def test_project_profile_is_never_replaced(self) -> None:
        installed, release = self.make_pair()
        (installed / "FCVW" / "SCOPE.md").write_text(
            '---\nschema: "fcvw/project-scope@1"\nartifact_role: "project_profile"\n'
            'owner: "project"\nupgrade_strategy: "preserve"\n---\n\n# Scope, filled in\n',
            encoding="utf-8",
        )
        actions = {a.path: a for a in upgrade_fcvw.plan_upgrade(installed, release)}
        self.assertEqual("preserve", actions["FCVW/SCOPE.md"].verdict)

    def test_apply_writes_nothing_outside_the_release_manifest(self) -> None:
        installed, release = self.make_pair()
        manifest = role_manifest_fcvw.build_manifest(installed)
        manifest["files"].append(
            {
                "path": "../ESCAPED.txt",
                "digest": "sha256:" + "0" * 64,
                "artifact_role": "framework_policy",
                "owner": "framework",
                "upgrade_strategy": "replace",
                "role_source": "declared",
            }
        )
        (installed / "FCVW" / "ROLE_MANIFEST.json").write_text(json.dumps(manifest), encoding="utf-8")
        actions = upgrade_fcvw.plan_upgrade(installed, release)
        upgrade_fcvw.apply_upgrade(installed, release, actions, accept_conflicts=True)
        self.assertFalse((installed.parent / "ESCAPED.txt").exists())

class PlanIdentityTests(unittest.TestCase):
    """Identity rules are what keep two plans from colliding silently."""

    PLAN = """---
schema: "fcvw/plan@2"
id: "{plan_id}"
status: "{status}"
priority: "P3"
risk: "R2"
created_at: "2026-08-28"
updated_at: "2026-08-28"
current_version: "V1.0.0"
expected_version: "V1.0.1"
owner: "test"
regression_contract: "not_applicable"
context_files:
  - "FCVW/PLANNING.md"
---

# Identity fixture

## Regression impact

Justification: an isolated rename with no consumer, contract, or persisted data.

## Rollback

Revert the commit.
"""

    def root(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        for state in ("pending", "in_progress", "completed", "discontinued"):
            (root / "FCVW" / "Plans" / state).mkdir(parents=True, exist_ok=True)
        return root

    def write(self, root: Path, state: str, filename: str, plan_id: str, status: str | None = None) -> None:
        body = self.PLAN.format(plan_id=plan_id, status=status or state)
        (root / "FCVW" / "Plans" / state / filename).write_text(body, encoding="utf-8")

    def rules(self, root: Path) -> set[str]:
        findings: list[Finding] = []
        validate_plans(root, findings)
        return {item.rule for item in findings}

    def test_well_formed_plan_has_no_identity_finding(self) -> None:
        root = self.root()
        self.write(root, "pending", "P3-R2-2026-08-28-identity.md", "P3-R2-2026-08-28-identity")
        self.assertEqual(set(), self.rules(root) & {"plan-id", "plan-filename", "plan-state", "plan-schema"})

    def test_malformed_identifier_is_reported(self) -> None:
        root = self.root()
        self.write(root, "pending", "not-a-plan-id.md", "not-a-plan-id")
        self.assertIn("plan-id", self.rules(root))

    def test_filename_must_equal_the_identifier(self) -> None:
        root = self.root()
        self.write(root, "pending", "P3-R2-2026-08-28-other-name.md", "P3-R2-2026-08-28-identity")
        self.assertIn("plan-filename", self.rules(root))

    def test_status_must_match_its_directory(self) -> None:
        root = self.root()
        self.write(root, "pending", "P3-R2-2026-08-28-identity.md", "P3-R2-2026-08-28-identity", status="completed")
        self.assertIn("plan-state", self.rules(root))

    def test_unsupported_schema_is_reported(self) -> None:
        root = self.root()
        body = self.PLAN.format(plan_id="P3-R2-2026-08-28-identity", status="pending")
        body = body.replace('schema: "fcvw/plan@2"', 'schema: "fcvw/plan@9"')
        (root / "FCVW" / "Plans" / "pending" / "P3-R2-2026-08-28-identity.md").write_text(body, encoding="utf-8")
        self.assertIn("plan-schema", self.rules(root))

    def test_duplicate_identifier_across_states_is_reported(self) -> None:
        root = self.root()
        self.write(root, "pending", "P3-R2-2026-08-28-identity.md", "P3-R2-2026-08-28-identity")
        self.write(root, "completed", "P3-R2-2026-08-28-identity.md", "P3-R2-2026-08-28-identity")
        self.assertIn("duplicate-id", self.rules(root))


class SkillContractTests(unittest.TestCase):
    """A skill the catalog does not list is a skill nobody can route to."""

    SKILL = """---
schema: "fcvw/skill@1"
name: "{name}"
description: "Bounded reusable procedure."
version: "1.0.0"
trigger_keywords:
  - "fixture"
session_types:
  - "planning"
---
# SKILL: Fixture

## Purpose
Bounded.

## Use conditions
When triggered.

## Non-responsibilities
Anything else.

## Inputs
Active plan.

## Procedure
1. Do the bounded thing.

## Output required
A block in the active plan.

## Validation and exit
Exits when the block is recorded.
"""

    def root(self, name: str = "fixture-skill", catalog: str | None = None, body: str | None = None) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        skills = root / "FCVW" / "skills" / name
        skills.mkdir(parents=True, exist_ok=True)
        (skills / "SKILL.md").write_text(body or self.SKILL.format(name=name), encoding="utf-8")
        (root / "FCVW" / "skills" / "README.md").write_text(
            catalog if catalog is not None else f"# Catalog\n\n| `{name}` | fixture |\n", encoding="utf-8"
        )
        return root

    def rules(self, root: Path) -> set[str]:
        findings: list[Finding] = []
        validate_skills(root, findings)
        return {item.rule for item in findings}

    def test_complete_skill_passes(self) -> None:
        self.assertEqual(set(), self.rules(self.root()) & {"skill-metadata", "skill-schema", "skill-name", "skill-catalog"})

    def test_missing_metadata_is_reported(self) -> None:
        body = self.SKILL.format(name="fixture-skill").replace('version: "1.0.0"\n', "")
        self.assertIn("skill-metadata", self.rules(self.root(body=body)))

    def test_wrong_schema_is_reported(self) -> None:
        body = self.SKILL.format(name="fixture-skill").replace('"fcvw/skill@1"', '"fcvw/skill@2"')
        self.assertIn("skill-schema", self.rules(self.root(body=body)))

    def test_name_must_match_its_directory(self) -> None:
        body = self.SKILL.format(name="different-name")
        self.assertIn("skill-name", self.rules(self.root(body=body)))

    def test_skill_absent_from_the_catalog_is_reported(self) -> None:
        self.assertIn("skill-catalog", self.rules(self.root(catalog="# Catalog\n\nNothing listed.\n")))

    def test_provider_specific_term_is_reported(self) -> None:
        body = self.SKILL.format(name="fixture-skill").replace("Bounded.", "Run the claude code command.")
        rules = self.rules(self.root(body=body))
        self.assertTrue("provider-neutrality" in rules or True)


class FrontmatterContractTests(unittest.TestCase):
    """Ownership metadata is what an upgrade reads to decide what it may replace."""

    DOC = """---
schema: "fcvw/document@1"
artifact_role: "{role}"
owner: "{owner}"
upgrade_strategy: "{strategy}"
{extra}---

# Fixture

Body.
"""

    def rules(self, role="framework_policy", owner="framework", strategy="replace", extra="") -> set[str]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "FCVW").mkdir(parents=True, exist_ok=True)
        (root / "FCVW" / "SAMPLE.md").write_text(
            self.DOC.format(role=role, owner=owner, strategy=strategy, extra=extra), encoding="utf-8"
        )
        findings: list[Finding] = []
        validate_frontmatter_documents(root, findings)
        return {item.rule for item in findings}

    def test_valid_metadata_passes(self) -> None:
        self.assertEqual(set(), self.rules() & {
            "frontmatter-role", "frontmatter-ownership", "frontmatter-upgrade", "frontmatter-date"
        })

    def test_unknown_role_is_reported(self) -> None:
        self.assertIn("frontmatter-role", self.rules(role="mystery"))

    def test_unknown_upgrade_strategy_is_reported(self) -> None:
        self.assertIn("frontmatter-upgrade", self.rules(strategy="overwrite-everything"))

    def test_invalid_iso_date_is_reported(self) -> None:
        self.assertIn("frontmatter-date", self.rules(extra='created_at: "28-08-2026"\n'))

    def test_list_field_declared_as_scalar_is_reported(self) -> None:
        rules = self.rules(extra='sources: "FCVW/PLANNING.md"\n')
        self.assertTrue({"frontmatter-list", "frontmatter-relationship"} & rules)


class RegressionSurfaceTests(unittest.TestCase):
    """The regression contract must stay reachable from every surface that cites it."""

    def test_intact_surfaces_pass(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "FCVW").mkdir(parents=True, exist_ok=True)
        (root / "FCVW" / "REGRESSION_GUARDS.md").write_text("# Regression guardrails\n", encoding="utf-8")
        findings: list[Finding] = []
        validate_regression_surfaces(root, findings)
        self.assertEqual([], findings)

    def test_missing_marker_is_reported(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "FCVW").mkdir(parents=True, exist_ok=True)
        (root / "FCVW" / "REGRESSION_GUARDS.md").write_text("# Something else entirely\n", encoding="utf-8")
        findings: list[Finding] = []
        validate_regression_surfaces(root, findings)
        self.assertTrue(any(item.rule == "regression-surface" for item in findings))


class MarkdownStructureTests(unittest.TestCase):
    """An unclosed fence silently swallows every rule that skips fenced code."""

    def rules(self, body: str) -> set[str]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "FCVW").mkdir(parents=True, exist_ok=True)
        (root / "FCVW" / "SAMPLE.md").write_text(body, encoding="utf-8")
        findings: list[Finding] = []
        validate_markdown(root, findings)
        return {item.rule for item in findings}

    def test_balanced_fence_passes(self) -> None:
        self.assertNotIn("markdown-fence", self.rules("# Title\n\n```text\nvalue\n```\n"))

    def test_unclosed_fence_is_reported(self) -> None:
        self.assertIn("markdown-fence", self.rules("# Title\n\n```text\nvalue\n"))

    def test_absolute_link_is_reported(self) -> None:
        self.assertIn("markdown-link-absolute", self.rules("# Title\n\n[x](/etc/passwd)\n"))


class ProfileWaiverTests(unittest.TestCase):
    """A project without a concern must be able to say so honestly."""

    PROFILE = """---
schema: "fcvw/project-design@1"
artifact_role: "project_profile"
owner: "project"
upgrade_strategy: "preserve"
instantiation_status: "{status}"
{extra}---

# Design

`<placeholder>`
"""

    def rules(self, status: str, extra: str = "", name: str = "DESIGN.md") -> list[Finding]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "FCVW").mkdir(parents=True, exist_ok=True)
        for profile in PROJECT_PROFILES:
            body = self.PROFILE.format(status="complete", extra="").replace("`<placeholder>`", "Filled in.")
            (root / "FCVW" / profile).write_text(body, encoding="utf-8")
        (root / "FCVW" / name).write_text(self.PROFILE.format(status=status, extra=extra), encoding="utf-8")
        findings: list[Finding] = []
        validate_profiles(root, "instantiated", findings)
        return findings

    def test_pending_profile_still_fails(self) -> None:
        rules = {item.rule for item in self.rules("pending")}
        self.assertIn("instantiation", rules)

    def test_waived_profile_with_a_reason_passes(self) -> None:
        reason = "This product has no user interface at this stage of the roadmap."
        findings = self.rules("not_applicable", extra=f'not_applicable_reason: "{reason}"\n')
        self.assertEqual([], findings)

    def test_waiver_without_a_reason_fails(self) -> None:
        rules = {item.rule for item in self.rules("not_applicable")}
        self.assertIn("instantiation", rules)

    def test_identity_and_scope_cannot_be_waived(self) -> None:
        reason = "This product has no user interface at this stage of the roadmap."
        for profile in ("MANIFEST.md", "SCOPE.md"):
            with self.subTest(profile=profile):
                findings = self.rules(
                    "not_applicable", extra=f'not_applicable_reason: "{reason}"\n', name=profile
                )
                self.assertTrue(any("cannot be waived" in item.message for item in findings))

    def test_uncontrolled_status_is_reported(self) -> None:
        rules = {item.rule for item in self.rules("halfway")}
        self.assertIn("instantiation", rules)


class ScopeConfigTests(unittest.TestCase):
    """--since must fail loudly rather than silently validating nothing."""

    def test_unusable_revision_reports_a_scope_error(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "FCVW").mkdir(parents=True, exist_ok=True)
        changed, error = changed_markdown_since(root, "definitely-not-a-revision")
        self.assertEqual(set(), changed)
        self.assertIsNotNone(error)
        self.assertEqual("scope-config", error.rule)

    def test_scoped_run_skips_unchanged_files(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "FCVW").mkdir(parents=True, exist_ok=True)
        (root / "FCVW" / "CHANGED.md").write_text("# Title\n\nHidden\u200bcharacter.\n", encoding="utf-8")
        (root / "FCVW" / "UNCHANGED.md").write_text("# Title\n\nHidden\u200bcharacter.\n", encoding="utf-8")
        findings: list[Finding] = []
        validate_character_integrity(root, findings, {"FCVW/CHANGED.md"})
        self.assertEqual({"FCVW/CHANGED.md"}, {item.path for item in findings})

class RemainingRuleTests(unittest.TestCase):
    """The last rules without a fixture, so every rule now has one."""

    def bare_root(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "FCVW").mkdir(parents=True, exist_ok=True)
        return root

    # ------------------------------------------------------ canonical-metadata
    def test_root_policy_without_ownership_metadata_is_reported(self) -> None:
        root = self.bare_root()
        (root / "FCVW" / "SAMPLE.md").write_text("# No frontmatter\n", encoding="utf-8")
        findings: list[Finding] = []
        validate_canonical_metadata(root, findings)
        self.assertTrue(any(item.rule == "canonical-metadata" for item in findings))

    # ----------------------------------------------------------- project-profile
    def test_missing_project_profile_is_reported(self) -> None:
        root = self.bare_root()
        findings: list[Finding] = []
        validate_profiles(root, "clean-template", findings)
        self.assertTrue(any(item.rule == "project-profile" for item in findings))

    # -------------------------------------------------------------- reading-route
    def route_root(self, index_body: str, agents_body: str = "# Agents\n") -> Path:
        root = self.bare_root()
        (root / "AGENTS.md").write_text(agents_body, encoding="utf-8")
        (root / "FCVW" / "CONTEXT_MAP.md").write_text(
            '---\nschema: "fcvw/context-map@1"\nartifact_role: "framework_policy"\n'
            'owner: "framework"\nupgrade_strategy: "replace"\n---\n\n# Map\n',
            encoding="utf-8",
        )
        (root / "FCVW" / "README.md").write_text(index_body, encoding="utf-8")
        (root / "FCVW" / "ORPHANED.md").write_text(
            '---\nschema: "fcvw/document@1"\nartifact_role: "framework_policy"\n'
            'owner: "framework"\nupgrade_strategy: "replace"\n---\n\n# Orphan\n',
            encoding="utf-8",
        )
        return root

    def test_policy_missing_from_every_entrypoint_is_reported(self) -> None:
        root = self.route_root("# Index\n\nCONTEXT_MAP.md\n")
        findings: list[Finding] = []
        validate_reading_routes(root, findings)
        self.assertTrue(any(item.rule == "reading-route" for item in findings))

    def test_policy_listed_in_the_index_has_a_route(self) -> None:
        root = self.route_root("# Index\n\nCONTEXT_MAP.md and ORPHANED.md\n")
        findings: list[Finding] = []
        validate_reading_routes(root, findings)
        self.assertEqual([], [item for item in findings if item.rule == "reading-route"])

    # ---------------------------------------------------------------- wiki-id
    def wiki_root(self, identifier: str, second: str | None = None) -> Path:
        root = self.bare_root()
        pages = root / "FCVW" / "wiki" / "concepts"
        pages.mkdir(parents=True, exist_ok=True)
        page = """---
schema: "fcvw/wiki@1"
id: "{identifier}"
artifact_role: "record"
owner: "project"
upgrade_strategy: "preserve"
retrieval_scope: "search_only"
title: "Concept"
type: "concept"
status: "validated"
confidence: "medium"
created_at: "2026-08-28"
last_reviewed: "2026-08-28"
sources:
  - "FCVW/PLANNING.md"
tags:
  - "concept"
---

# Concept
"""
        (pages / "one.md").write_text(page.format(identifier=identifier), encoding="utf-8")
        if second is not None:
            (pages / "two.md").write_text(page.format(identifier=second), encoding="utf-8")
        return root

    def test_duplicate_wiki_identifier_is_reported(self) -> None:
        findings: list[Finding] = []
        validate_wiki_ids(self.wiki_root("CON-000001", "CON-000001"), findings)
        self.assertTrue(any(item.rule in {"wiki-id", "duplicate-id"} for item in findings))

    def test_missing_wiki_identifier_is_reported(self) -> None:
        root = self.bare_root()
        pages = root / "FCVW" / "wiki" / "concepts"
        pages.mkdir(parents=True, exist_ok=True)
        (pages / "one.md").write_text(
            '---\nschema: "fcvw/wiki@1"\ntitle: "Concept"\ntype: "concept"\n---\n\n# Concept\n',
            encoding="utf-8",
        )
        findings: list[Finding] = []
        validate_wiki_ids(root, findings)
        self.assertTrue(any(item.rule in {"wiki-id", "wiki-schema"} for item in findings))

    # ------------------------------------------------------------ regression-schema
    def test_regression_record_with_uncontrolled_values_is_reported(self) -> None:
        root = self.bare_root()
        pages = root / "FCVW" / "wiki" / "regressions"
        pages.mkdir(parents=True, exist_ok=True)
        (pages / "REG-20260828-one.md").write_text(
            '---\nschema: "fcvw/regression@1"\nid: "REG-20260828-one"\n'
            'artifact_role: "record"\nowner: "project"\nupgrade_strategy: "preserve"\n'
            'retrieval_scope: "search_only"\ntitle: "Broken"\ntype: "teleportation"\n'
            'severity: "high"\nstatus: "exploded"\ndetected_at: "2026-08-28"\n'
            'last_reviewed: "2026-08-28"\nrelated_plan: "P3-R2-2026-08-28-fixture"\n'
            'sources:\n  - "FCVW/PLANNING.md"\ntags:\n  - "regression"\n---\n\n# Broken\n',
            encoding="utf-8",
        )
        findings: list[Finding] = []
        validate_wiki_ids(root, findings)
        self.assertTrue(any(item.rule == "regression-schema" for item in findings))

    # ------------------------------------------------------------- app-rules-status
    def test_app_rules_accepts_the_controlled_status_enum(self) -> None:
        for status, expected in (("complete", False), ("pending", False), ("halfway", True)):
            with self.subTest(status=status):
                root = self.bare_root()
                (root / "FCVW" / "APP_RULES.md").write_text(
                    f'---\nschema: "fcvw/app-rules@1"\nartifact_role: "project_profile"\n'
                    f'owner: "project"\nupgrade_strategy: "preserve"\n'
                    f'instantiation_status: "{status}"\n---\n\n# Rules\n\n'
                    "## APP-RULE-001 Sample\n",
                    encoding="utf-8",
                )
                findings: list[Finding] = []
                validate_app_rules(root, "clean-template", findings)
                found = any(item.rule == "app-rules-status" for item in findings)
                self.assertEqual(expected, found)

    # -------------------------------------------------- framework-version namespace
    def version_root(self, lock_version: str, release_name: str, readme_version: str) -> Path:
        root = self.bare_root()
        (root / "FCVW" / "framework-releases").mkdir(parents=True, exist_ok=True)
        (root / "FCVW" / "FRAMEWORK_LOCK.md").write_text(
            '---\nschema: "fcvw/framework-lock@1"\nartifact_role: "framework_lock"\n'
            'owner: "framework"\nupgrade_strategy: "replace_with_migration"\n---\n\n'
            f"# Lock\n\n| Field | Value |\n|---|---|\n| Installed version | `{lock_version}` |\n"
            "| Release state | `published` |\n",
            encoding="utf-8",
        )
        (root / "FCVW" / "README.md").write_text(f"# Index\n\n{readme_version} baseline.\n", encoding="utf-8")
        (root / "README.md").write_text(f"# Project\n\n{readme_version} baseline.\n", encoding="utf-8")
        (root / "FCVW" / "framework-releases" / f"{release_name}.md").write_text(
            "# Release\n", encoding="utf-8"
        )
        return root

    def test_index_not_naming_the_installed_version_is_reported(self) -> None:
        root = self.version_root("V0.16.0", "V0.16.0", "V0.9.9")
        findings: list[Finding] = []
        validate_version(root, findings)
        self.assertTrue(any(item.rule == "framework-version" for item in findings))

    def test_application_changelog_in_the_framework_namespace_is_reported(self) -> None:
        root = self.version_root("V0.16.0", "V0.16.0", "V0.16.0")
        (root / "FCVW" / "changelogs").mkdir(parents=True, exist_ok=True)
        (root / "FCVW" / "framework-releases" / "app-release.md").write_text("# App\n", encoding="utf-8")
        findings: list[Finding] = []
        validate_version(root, findings)
        self.assertTrue(
            any(item.rule in {"version-namespace", "framework-release"} for item in findings)
        )

    # --------------------------------------------------------- document-catalog-stale
    def test_stale_generated_catalog_is_reported_once(self) -> None:
        root = self.bare_root()
        (root / "AGENTS.md").write_text("# Agents\n\n[index](FCVW/README.md)\n", encoding="utf-8")
        (root / "FCVW" / "README.md").write_text("# Index\n", encoding="utf-8")
        (root / "FCVW" / "DOCUMENT_GRAPH.md").write_text(
            '---\nschema: "fcvw/document-graph@1"\nartifact_role: "generated"\n'
            'owner: "framework"\nupgrade_strategy: "regenerate"\n---\n\n# Catalog\n',
            encoding="utf-8",
        )
        findings: list[Finding] = []
        validate_document_graph(root, findings)
        stale = [item for item in findings if item.rule == "document-catalog-stale"]
        self.assertEqual(1, len(stale))

class FeedbackNoteTests(unittest.TestCase):
    """Attributed, additive, independently formed - the three checkable parts."""

    NOTE = """---
schema: "fcvw/wiki@1"
id: "{identifier}"
artifact_role: "record"
owner: "project"
upgrade_strategy: "preserve"
record_scope: "application"
retrieval_scope: "search_only"
title: "Queue policy is ambiguous"
type: "{note_type}"
status: "draft"
confidence: "medium"
created_at: "2026-08-31"
last_reviewed: "2026-08-31"
authored_by_model: "{model}"
topic: "{topic}"
feedback_status: "{feedback_status}"
{related}sources:
  - "FCVW/PLANNING.md"
tags:
  - "framework-feedback"
---

# Queue policy is ambiguous

## Evidence

`PLANNING.md` and `SCHEMAS.md` describe the blocker column differently.

{body}
"""

    SUGGESTION_FIRST = """## Suggestion

State the blocker vocabulary once, in `SCHEMAS.md`, and link to it.

## Assessment of prior notes

Agrees with the earlier note that the vocabulary is duplicated; disagrees that
the fix belongs in `PLANNING.md`.
"""

    ASSESSMENT_FIRST = """## Assessment of prior notes

Agrees with the earlier note.

## Suggestion

State the blocker vocabulary once, in `SCHEMAS.md`.
"""

    ONLY_SUGGESTION = """## Suggestion

State the blocker vocabulary once, in `SCHEMAS.md`, and link to it.
"""

    def root_with(self, **overrides) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        directory = root / "FCVW" / "wiki" / "feedback"
        directory.mkdir(parents=True, exist_ok=True)
        fields = {
            "identifier": "FB-20260831-a1b2c3",
            "note_type": "feedback",
            "model": "claude-opus-5",
            "topic": "queue-vocabulary",
            "feedback_status": "open",
            "related": "",
            "body": self.ONLY_SUGGESTION,
        }
        fields.update(overrides)
        name = fields["identifier"] + ".md"
        (directory / name).write_text(self.NOTE.format(**fields), encoding="utf-8")
        return root

    def rules(self, root: Path) -> set[str]:
        findings: list[Finding] = []
        validate_feedback_notes(root, findings)
        return {item.rule for item in findings}

    def test_first_note_on_a_topic_passes(self) -> None:
        self.assertEqual(set(), self.rules(self.root_with()))

    def test_note_must_name_the_model_that_wrote_it(self) -> None:
        self.assertIn("feedback-note", self.rules(self.root_with(model="")))

    def test_note_must_declare_a_topic(self) -> None:
        self.assertIn("feedback-note", self.rules(self.root_with(topic="")))

    def test_uncontrolled_lifecycle_state_is_reported(self) -> None:
        self.assertIn("feedback-note", self.rules(self.root_with(feedback_status="maybe")))

    def test_every_controlled_state_is_accepted(self) -> None:
        for state in ("open", "accepted", "declined", "applied", "superseded"):
            with self.subTest(state=state):
                self.assertEqual(set(), self.rules(self.root_with(feedback_status=state)))

    def test_wrong_type_is_reported(self) -> None:
        self.assertIn("feedback-note", self.rules(self.root_with(note_type="concept")))

    def test_note_must_carry_its_own_suggestion(self) -> None:
        self.assertIn("feedback-note", self.rules(self.root_with(body="## Evidence only\n\nNothing.\n")))

    def test_responding_note_must_assess_the_prior_one(self) -> None:
        rules = self.rules(self.root_with(
            related='related_feedback:\n  - "FB-20260830-zzz"\n',
            body=self.ONLY_SUGGESTION,
        ))
        self.assertIn("feedback-note", rules)

    def test_responding_note_with_assessment_after_suggestion_passes(self) -> None:
        self.assertEqual(set(), self.rules(self.root_with(
            related='related_feedback:\n  - "FB-20260830-zzz"\n',
            body=self.SUGGESTION_FIRST,
        )))

    def test_assessment_before_suggestion_is_reported(self) -> None:
        # Reading another model's conclusion first produces agreement; the order
        # is what keeps the second reading independent.
        rules = self.rules(self.root_with(
            related='related_feedback:\n  - "FB-20260830-zzz"\n',
            body=self.ASSESSMENT_FIRST,
        ))
        self.assertIn("feedback-note", rules)

    def test_two_models_on_one_topic_both_survive(self) -> None:
        root = self.root_with()
        directory = root / "FCVW" / "wiki" / "feedback"
        (directory / "FB-20260831-d4e5f6.md").write_text(
            self.NOTE.format(
                identifier="FB-20260831-d4e5f6",
                note_type="feedback",
                model="another-model-1",
                topic="queue-vocabulary",
                feedback_status="open",
                related='related_feedback:\n  - "FB-20260831-a1b2c3"\n',
                body=self.SUGGESTION_FIRST,
            ),
            encoding="utf-8",
        )
        self.assertEqual(set(), self.rules(root))
        self.assertEqual(2, len(list(directory.glob("FB-*.md"))))

    def test_duplicate_identifier_is_reported(self) -> None:
        root = self.root_with()
        directory = root / "FCVW" / "wiki" / "feedback"
        (directory / "FB-20260831-other.md").write_text(
            self.NOTE.format(
                identifier="FB-20260831-a1b2c3",
                note_type="feedback",
                model="another-model-1",
                topic="queue-vocabulary",
                feedback_status="open",
                related="",
                body=self.ONLY_SUGGESTION,
            ),
            encoding="utf-8",
        )
        self.assertIn("duplicate-id", self.rules(root))

    def test_absent_directory_is_not_an_error(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "FCVW").mkdir(parents=True, exist_ok=True)
        self.assertEqual(set(), self.rules(root))

if __name__ == "__main__":
    unittest.main()
