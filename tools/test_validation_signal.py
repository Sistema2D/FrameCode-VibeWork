#!/usr/bin/env python3
"""V0.24.0: a validation signal that separates new defects from known debt.

Each class reproduces a failure recorded while using FCVW on a real project:
the default profile, an unusable baseline, context_files read from the wrong
folder, a graph that indexed transient trees and mixed generation with
validation, completed plans with undecided criteria, deferred criteria that
nobody carried, gates that ignored the diff, and removals left half done.
"""

from __future__ import annotations

import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import date, timedelta
from pathlib import Path

import fcvw_cache
import validate_fcvw
from document_graph_fcvw import build_graph
from gates_fcvw import read_gate_table, select_gates
from path_policy_fcvw import glob_regex, governed_markdown_inventory, matches_ungoverned
from retrieve_context import mandatory_paths
from validate_fcvw import (
    PENDING_RESULT,
    BaselineEntry,
    Finding,
    apply_legacy_baseline,
    comparable_message,
    fix_moved_plan_links,
    load_legacy_baseline,
    resolve_profile,
    validate_frontmatter_documents,
    validate_plan_deferrals,
    validate_plans,
    validate_project_gates,
    write_legacy_baseline,
)

TOOLS = Path(__file__).resolve().parent
HAS_GIT = shutil.which("git") is not None
FUTURE = (date.today() + timedelta(days=30)).isoformat()
REGRESSION = """
## Regression impact

### Existing behaviors that may be affected
- Plan lifecycle.

### Regression contracts consulted
- `PLANNING.md`.

### Regression checks required
- [x] Validator replay.

### Regression evidence
| Check | Result | Evidence |
|---|---|---|
| Lifecycle | pass | unit fixture |

### Limitations and residual risk
- None.

## Rollback

Revert the commit that introduced the change.
"""


def temporary_root(test: unittest.TestCase) -> Path:
    directory = tempfile.TemporaryDirectory()
    test.addCleanup(directory.cleanup)
    fcvw_cache.clear()
    root = Path(directory.name).resolve()
    for state in ("pending", "in_progress", "completed", "discontinued"):
        (root / "FCVW" / "Plans" / state).mkdir(parents=True, exist_ok=True)
    return root


def write_plan(root: Path, plan_id: str, state: str, body: str, *, schema: str = "fcvw/plan@2",
               context: tuple[str, ...] = ("FCVW/PLANNING.md",), fields: str = "") -> Path:
    priority, risk = plan_id.split("-")[0], plan_id.split("-")[1]
    extra = 'regression_contract: "required"\ncurrent_version: "V0.23.0"\nexpected_version: "V0.24.0"\n'
    if schema == "fcvw/plan-compact@1":
        extra = ""
    extra += fields
    context_lines = "".join(f'  - "{item}"\n' for item in context)
    text = (
        f'---\nschema: "{schema}"\nid: "{plan_id}"\nstatus: "{state}"\npriority: "{priority}"\nrisk: "{risk}"\n'
        f'created_at: "2026-11-01"\nupdated_at: "2026-11-01"\nowner: "test"\n{extra}context_files:\n{context_lines}---\n\n'
        f"# Fixture\n\n{body}\n"
    )
    path = root / "FCVW" / "Plans" / state / f"{plan_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)  # an installed payload ships no plan directories
    path.write_text(text, encoding="utf-8")
    return path


def rules(findings: list[Finding], rule: str) -> list[Finding]:
    return [item for item in findings if item.rule == rule]


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "user.name=fcvw", "-c", "user.email=fcvw@example.invalid", "-C", str(root), *args],
                   check=True, capture_output=True)


class ProfileResolutionTests(unittest.TestCase):
    def lock(self, root: Path, label: str, value: str) -> None:
        (root / "FCVW" / "FRAMEWORK_LOCK.md").write_text(f"| Field | Value |\n|---|---|\n| {label} | `{value}` |\n",
                                                         encoding="utf-8")

    def test_instantiated_lock_is_inferred_in_any_language(self) -> None:
        for label in ("Installed profile", "Perfil instalado", "Installiertes Profil"):
            root = temporary_root(self)
            self.lock(root, label, "project-instantiated")
            profile, baseline, reason = resolve_profile(root, "auto", None)
            self.assertEqual(("instantiated", None), (profile, baseline), label)
            self.assertIn("FRAMEWORK_LOCK.md", reason)

    def test_complete_project_profile_is_instantiated_even_with_a_clean_lock(self) -> None:
        root = temporary_root(self)
        self.lock(root, "Installed profile", "clean-template")
        (root / "FCVW" / "PROJECT.md").write_text('---\ninstantiation_status: "complete"\n---\n', encoding="utf-8")
        self.assertEqual("instantiated", resolve_profile(root, "auto", None)[0])

    def test_clean_template_stays_the_fallback_and_explicit_profiles_win(self) -> None:
        root = temporary_root(self)
        self.lock(root, "Installed profile", "clean-template")
        self.assertEqual("clean-template", resolve_profile(root, "auto", None)[0])
        self.assertEqual(("strict", None, "requested"), resolve_profile(root, "strict", None))

    def test_default_baseline_turns_an_instantiated_project_incremental(self) -> None:
        root = temporary_root(self)
        self.lock(root, "Installed profile", "project-instantiated")
        (root / "FCVW" / "audits").mkdir()
        (root / "FCVW" / "audits" / "legacy-baseline.md").write_text("x", encoding="utf-8")
        profile, baseline, reason = resolve_profile(root, "auto", None)
        self.assertEqual("incremental", profile)
        self.assertEqual(root / "FCVW" / "audits" / "legacy-baseline.md", baseline)
        self.assertIn("legacy-baseline.md", reason)


class BaselineTests(unittest.TestCase):
    def test_line_numbers_and_successor_hints_do_not_make_known_debt_new(self) -> None:
        entry = BaselineEntry("FCVW/a.md", "markdown-link", "line 9: missing target: x.md", "known", "owner",
                              date.today() + timedelta(days=1))
        moved = Finding("markdown-link", "FCVW/a.md", "line 3: missing target: x.md; renamed in git history to y.md "
                                                      "(--fix-moved-links rewrites it)")
        blocking, accepted, stale = apply_legacy_baseline([moved], [entry])
        self.assertEqual(([], [moved], []), (blocking, accepted, stale))
        other = Finding("markdown-link", "FCVW/a.md", "line 3: missing target: z.md")
        self.assertEqual([other], apply_legacy_baseline([other], [entry])[0])

    def test_written_baseline_round_trips_pipes_and_keeps_reviewed_rows(self) -> None:
        root = temporary_root(self)
        (root / "FCVW" / "MIGRATIONS.md").write_text("# M\n", encoding="utf-8")
        target = root / "FCVW" / "audits" / "legacy-baseline.md"
        first = [Finding("document-link", "FCVW/a.md", "missing Markdown target: [[a|b]]"),
                 Finding("plan-acceptance", "FCVW/b.md", "line 4: undecided"),
                 Finding("baseline-stale", "FCVW/c.md", "ignored"),
                 Finding("x-warning", "FCVW/d.md", "warning only", "warning")]
        self.assertEqual((2, 0, 0), write_legacy_baseline(target, root, first, owner="team", review_due=date.today()
                                                          + timedelta(days=10), justification="debt"))
        entries, errors = load_legacy_baseline(target)
        self.assertEqual([], errors)
        self.assertIn("missing Markdown target: [[a|b]]", {entry.message for entry in entries})
        self.assertIn("undecided", {entry.message for entry in entries}, "stored without the line number")
        text = target.read_text(encoding="utf-8").replace("| debt | team |", "| reviewed: owner accepted | team |", 1)
        target.write_text(text, encoding="utf-8")
        fcvw_cache.clear()
        second = [first[0], Finding("plan-acceptance", "FCVW/e.md", "new debt")]
        self.assertEqual((1, 1, 1), write_legacy_baseline(target, root, second, owner="team",
                                                          review_due=date.today() + timedelta(days=10),
                                                          justification="debt"))
        fcvw_cache.clear()
        kept = {entry.message: entry.justification for entry in load_legacy_baseline(target)[0]}
        self.assertEqual("reviewed: owner accepted", kept["missing Markdown target: [[a|b]]"])

    def test_a_release_backlog_is_never_recorded_or_accepted(self) -> None:
        root = temporary_root(self)
        target = root / "FCVW" / "audits" / "legacy-baseline.md"
        backlog = Finding("release-backlog", "FCVW/changelogs/unreleased", "20 unreleased fragments exceed unreleased_limit 5")
        debt = Finding("plan-acceptance", "FCVW/a.md", "undecided")
        write_legacy_baseline(target, root, [backlog, debt], owner="team",
                              review_due=date.today() + timedelta(days=10), justification="debt")
        entries, _ = load_legacy_baseline(target)
        self.assertEqual(["plan-acceptance"], [entry.rule for entry in entries])
        forced = BaselineEntry(backlog.path, backlog.rule, backlog.message, "x", "team", date.today() + timedelta(days=1))
        self.assertEqual([backlog], apply_legacy_baseline([backlog], [forced])[0], "even a hand-written row cannot hide it")

    def test_the_written_baseline_creates_no_finding_of_its_own(self) -> None:
        root = temporary_root(self)
        (root / "FCVW" / "MIGRATIONS.md").write_text("# Migraciones\n\n## Línea base heredada\n", encoding="utf-8")
        target = root / "FCVW" / "audits" / "legacy-baseline.md"
        write_legacy_baseline(target, root, [Finding("plan-acceptance", "FCVW/a.md", "undecided")], owner="team",
                              review_due=date.today() + timedelta(days=10), justification="debt")
        findings: list[Finding] = []
        validate_fcvw.validate_markdown(root, findings)
        validate_fcvw.validate_anchors(root, findings)
        validate_fcvw.validate_audit_records(root, findings)
        self.assertEqual([], findings)

    def test_translated_header_row_is_not_read_as_an_entry(self) -> None:
        root = temporary_root(self)
        path = root / "baseline.md"
        path.write_text(
            f'---\nschema: "fcvw/legacy-baseline@1"\ncreated_at: "2026-01-01"\nreview_due: "{FUTURE}"\nowner: "t"\n---\n\n'
            "| Caminho exato | Regra | Achado | Justificativa | Dono | Revisão |\n|---|---|---|---|---|---|\n"
            f"| FCVW/a.md | markdown-link | missing target: x | known | t | {FUTURE} |\n",
            encoding="utf-8")
        entries, errors = load_legacy_baseline(path)
        self.assertEqual([], errors)
        self.assertEqual(["FCVW/a.md"], [entry.path for entry in entries])


class PlanAcceptanceTests(unittest.TestCase):
    def acceptance(self, root: Path) -> list[Finding]:
        findings: list[Finding] = []
        validate_plans(root, findings)
        return rules(findings, "plan-acceptance")

    def test_completed_plan_with_an_undecided_criterion_fails(self) -> None:
        root = temporary_root(self)
        write_plan(root, "P3-R2-2026-11-01-open", "completed", "## Acceptance criteria\n\n- [ ] Deep link still works.\n" + REGRESSION)
        found = self.acceptance(root)
        self.assertEqual(1, len(found))
        self.assertIn("Deep link still works", found[0].message)

    def test_decided_items_pass_and_open_items_are_fine_while_in_progress(self) -> None:
        root = temporary_root(self)
        body = ("## Acceptance criteria\n\n- [x] Met.\n- [~] Socket rereads the grant. deferred: P2-R4-2026-11-02-target\n"
                "- [~] Legacy export. waived: product owner dropped the export on 2026-11-01\n" + REGRESSION)
        write_plan(root, "P3-R2-2026-11-01-done", "completed", body)
        write_plan(root, "P3-R2-2026-11-01-active", "in_progress", "## Acceptance criteria\n\n- [ ] Pending work.\n" + REGRESSION)
        self.assertEqual([], self.acceptance(root))

    def test_partial_mark_needs_an_address_or_a_reason(self) -> None:
        root = temporary_root(self)
        body = ("## Acceptance criteria\n\n- [~] Half done.\n- [~] Too short. waived: no\n"
                "- [~] Self. deferred: P3-R2-2026-11-01-self\n" + REGRESSION)
        write_plan(root, "P3-R2-2026-11-01-self", "in_progress", body)
        messages = [item.message for item in self.acceptance(root)]
        self.assertEqual(3, len(messages))
        self.assertTrue(any("its own plan" in message for message in messages))

    def test_validation_and_regression_checklists_and_translated_headings_are_covered(self) -> None:
        root = temporary_root(self)
        body = ("## Critérios de aceitação\n\n- [ ] Critério aberto.\n\n## Validation plan\n\n- [ ] `npm run build`\n"
                + REGRESSION.replace("- [x] Validator replay.", "- [ ] Validator replay."))
        write_plan(root, "P3-R2-2026-11-01-multi", "completed", body)
        titles = sorted(item.message.split(":")[0] for item in self.acceptance(root))
        self.assertEqual(["Acceptance criteria", "Regression checks required", "Validation"], titles)

    def test_compact_plan_validation_and_code_fences(self) -> None:
        root = temporary_root(self)
        body = ("## Objective\n\nText.\n\n## Affected files\n\n- a\n\n## Validation\n\n```markdown\n- [ ] example\n```\n"
                "- [ ] Real check.\n\n## Rollback\n\nRevert the commit.\n")
        write_plan(root, "P4-R1-2026-11-01-compact", "completed", body, schema="fcvw/plan-compact@1")
        found = self.acceptance(root)
        self.assertEqual(1, len(found))
        self.assertIn("Real check", found[0].message)

    def test_legacy_plan_history_is_not_rejudged(self) -> None:
        root = temporary_root(self)
        write_plan(root, "P3-R2-2026-11-01-legacy", "completed", "## Acceptance criteria\n\n- [ ] Old.\n", schema="fcvw/plan@1")
        self.assertEqual([], self.acceptance(root))


class PlanDeferralTests(unittest.TestCase):
    ORIGIN = "P2-R4-2026-11-01-origin"
    TARGET = "P2-R4-2026-11-02-target"

    def deferrals(self, root: Path) -> list[Finding]:
        findings: list[Finding] = []
        validate_plan_deferrals(root, findings)
        return rules(findings, "plan-deferral")

    def origin(self, root: Path, target: str | None = None) -> None:
        write_plan(root, self.ORIGIN, "completed",
                   f"## Acceptance criteria\n\n- [~] Live sockets reread the grant. deferred: {target or self.TARGET}\n" + REGRESSION)

    def test_a_deferral_the_target_carries_is_valid(self) -> None:
        root = temporary_root(self)
        self.origin(root)
        write_plan(root, self.TARGET, "pending", f"## Acceptance criteria\n\n- [ ] Live sockets reread the grant. from: {self.ORIGIN}\n")
        self.assertEqual([], self.deferrals(root))

    def test_the_field_case_target_closes_without_the_deferred_criterion(self) -> None:
        root = temporary_root(self)
        self.origin(root)
        write_plan(root, self.TARGET, "completed", "## Acceptance criteria\n\n- [x] Socket unified.\n" + REGRESSION)
        found = self.deferrals(root)
        self.assertEqual(1, len(found))
        self.assertIn("does not carry", found[0].message)
        self.assertIn("reopen", found[0].message)

    def test_carried_criterion_blocks_the_target_from_closing_undecided(self) -> None:
        root = temporary_root(self)
        self.origin(root)
        write_plan(root, self.TARGET, "completed", f"## Acceptance criteria\n\n- [ ] Reread grant. from: {self.ORIGIN}\n" + REGRESSION)
        findings: list[Finding] = []
        validate_plans(root, findings)
        validate_plan_deferrals(root, findings)
        self.assertEqual([], rules(findings, "plan-deferral"))
        self.assertEqual(1, len(rules(findings, "plan-acceptance")))

    def test_missing_discontinued_and_dangling_relations(self) -> None:
        root = temporary_root(self)
        self.origin(root, "P2-R4-2026-11-09-missing")
        self.assertIn("missing plan", self.deferrals(root)[0].message)
        root = temporary_root(self)
        self.origin(root)
        write_plan(root, self.TARGET, "discontinued", f"## Acceptance criteria\n\n- [ ] x from: {self.ORIGIN}\n")
        self.assertIn("discontinued", self.deferrals(root)[0].message)
        root = temporary_root(self)
        write_plan(root, self.ORIGIN, "completed", "## Acceptance criteria\n\n- [x] Done.\n" + REGRESSION)
        write_plan(root, self.TARGET, "pending", f"## Acceptance criteria\n\n- [ ] x from: {self.ORIGIN}\n")
        found = self.deferrals(root)
        self.assertEqual(["warning"], [item.severity for item in found])
        write_plan(root, self.TARGET, "pending", "## Acceptance criteria\n\n- [ ] x from: P2-R4-2026-11-09-ghost\n")
        self.assertIn("missing plan", self.deferrals(root)[0].message)


class FailureOriginTests(unittest.TestCase):
    """A failure found during other work becomes data on both plans."""

    FOUND = "P2-R3-2026-11-01-feature-work"
    FIX = "P2-R3-2026-11-02-socket-grant-reread"

    def origins(self, root: Path) -> list[Finding]:
        findings: list[Finding] = []
        validate_fcvw.validate_plan_origins(root, findings)
        return rules(findings, "plan-origin")

    def failure_plan(self, root: Path, origin: str) -> None:
        write_plan(root, self.FIX, "pending", "## Acceptance criteria\n\n- [ ] Live sockets reread the grant.\n",
                   fields=f'found_by: "{origin}"\ncategory: "correction"\n')

    def test_both_plans_name_each_other(self) -> None:
        root = temporary_root(self)
        write_plan(root, self.FOUND, "completed",
                   f"## Validation executed\n\n| Failure found | planned | [{self.FIX}](../pending/{self.FIX}.md) |\n" + REGRESSION)
        self.failure_plan(root, self.FOUND)
        self.assertEqual([], self.origins(root))

    def test_origin_that_forgets_the_failure_or_does_not_exist_fails(self) -> None:
        root = temporary_root(self)
        write_plan(root, self.FOUND, "completed", "## Validation executed\n\nAll green.\n" + REGRESSION)
        self.failure_plan(root, self.FOUND)
        self.assertIn("does not name", self.origins(root)[0].message)
        root = temporary_root(self)
        self.failure_plan(root, "P2-R3-2026-11-09-ghost")
        self.assertIn("missing plan", self.origins(root)[0].message)
        root = temporary_root(self)
        self.failure_plan(root, self.FIX)
        self.assertIn("itself", self.origins(root)[0].message)


class DraftedPlanReviewTests(unittest.TestCase):
    """A plan drafted outside the agent (screenshot comments, imports) runs only after review."""

    DRAFT = 'source: "screenshot-review"\nai_review: "{review}"\ncategory: "visual"\n'

    def review(self, root: Path) -> list[Finding]:
        findings: list[Finding] = []
        validate_plans(root, findings)
        return rules(findings, "plan-review")

    def test_pending_review_may_wait_but_never_run(self) -> None:
        root = temporary_root(self)
        write_plan(root, "P3-R2-2026-11-01-draft", "pending", "Body.", fields=self.DRAFT.format(review="pending"))
        self.assertEqual([], self.review(root))
        root = temporary_root(self)
        write_plan(root, "P3-R2-2026-11-01-draft", "in_progress", "Body.", fields=self.DRAFT.format(review="pending"))
        self.assertIn("awaits review", self.review(root)[0].message)
        root = temporary_root(self)
        write_plan(root, "P3-R2-2026-11-01-draft", "completed", "Body." + REGRESSION, fields=self.DRAFT.format(review="confirmed"))
        self.assertEqual([], self.review(root))
        write_plan(root, "P3-R2-2026-11-02-typo", "pending", "Body.", fields=self.DRAFT.format(review="ok"))
        self.assertIn("invalid ai_review", self.review(root)[0].message)

    def test_queue_never_recommends_a_plan_awaiting_review(self) -> None:
        from plan_queue_fcvw import derive_queue, recommend_next_plan

        root = temporary_root(self)
        write_plan(root, "P1-R2-2026-11-01-draft", "pending", "Body.", fields=self.DRAFT.format(review="pending"))
        write_plan(root, "P4-R2-2026-11-01-ready", "pending", "Body.", fields='category: "visual"\n')
        entries, _ = derive_queue(root)
        self.assertIn("ai_review pending", next(item.blocked_by for item in entries if item.plan_id.endswith("draft")))
        self.assertEqual("P4-R2-2026-11-01-ready", recommend_next_plan(root)[1].plan_id)


class ReleaseAssemblyTests(unittest.TestCase):
    """Unreleased fragments may not pile up while plans keep closing."""

    def project(self, limit: str | None, fragments: int, *, published: str = "2026-11-01") -> Path:
        root = temporary_root(self)
        changelogs = root / "FCVW" / "changelogs"
        (changelogs / "unreleased").mkdir(parents=True)
        if limit is not None:
            (root / "FCVW" / "PROJECT.md").write_text(f'---\nunreleased_limit: "{limit}"\n---\n', encoding="utf-8")
        (changelogs / "V1.0.0.md").write_text(
            f'---\nrelease_status: "published"\ndate: "{published}"\nrelated_plans:\n  - "P3-R2-2026-10-01-old"\n---\n',
            encoding="utf-8")
        for index in range(fragments):
            (changelogs / "unreleased" / f"P3-R2-2026-11-0{index % 9 + 1}-f{index}.md").write_text(
                f'---\nrelease_status: "unreleased"\nrelated_plans:\n  - "P3-R2-2026-11-05-named-{index}"\n---\n',
                encoding="utf-8")
        return root

    def assembly(self, root: Path) -> list[Finding]:
        findings: list[Finding] = []
        validate_fcvw.validate_release_assembly(root, findings)
        return findings

    def test_backlog_over_the_declared_limit_blocks(self) -> None:
        self.assertEqual([], rules(self.assembly(self.project("5", 5)), "release-backlog"))
        blocked = rules(self.assembly(self.project("5", 6)), "release-backlog")
        self.assertEqual(["error"], [item.severity for item in blocked])
        self.assertIn("6 unreleased fragments", blocked[0].message)
        self.assertEqual([], rules(self.assembly(self.project(None, 40)), "release-backlog"), "opt-in: no limit, no rule")
        self.assertIn("whole number", rules(self.assembly(self.project("five", 0)), "release-backlog")[0].message)

    def test_plan_closed_after_the_last_release_without_a_changelog_warns(self) -> None:
        root = self.project("5", 1)
        for plan_id, updated in (("P3-R2-2026-10-01-old", "2026-10-01"), ("P3-R2-2026-10-02-history", "2026-10-02"),
                                 ("P3-R2-2026-11-05-named-0", "2026-11-05"), ("P3-R2-2026-11-06-orphan", "2026-11-06")):
            path = write_plan(root, plan_id, "completed", "Body." + REGRESSION)
            path.write_text(path.read_text(encoding="utf-8").replace('updated_at: "2026-11-01"', f'updated_at: "{updated}"'),
                            encoding="utf-8")
        warned = rules(self.assembly(root), "release-unassembled")
        self.assertEqual(["P3-R2-2026-11-06-orphan.md"], [item.path.split("/")[-1] for item in warned])
        self.assertEqual(["warning"], [item.severity for item in warned])


class RegressionTextTests(unittest.TestCase):
    def regression(self, body: str) -> list[Finding]:
        root = temporary_root(self)
        write_plan(root, "P3-R2-2026-11-01-text", "completed", body)
        findings: list[Finding] = []
        validate_plans(root, findings)
        return rules(findings, "plan-regression")

    def test_markup_quoted_in_inline_code_is_not_a_placeholder(self) -> None:
        body = REGRESSION.replace("| unit fixture |", "| the `<main>` element is transparent |")
        self.assertEqual([], self.regression(body))
        self.assertTrue(self.regression(REGRESSION.replace("- None.", "- <Limitation, owner and follow-up.>")))

    def test_pending_is_read_as_a_result_not_as_a_folder_name(self) -> None:
        linked = REGRESSION.replace("| unit fixture |", "| fixed by [plan](../pending/P3-R2-2026-11-02-x.md) |")
        self.assertEqual([], self.regression(linked))
        for cell in ("| `pending` |", "| **pending** |", "| pending |"):
            self.assertTrue(self.regression(REGRESSION.replace("| pass |", cell)), cell)
        self.assertTrue(PENDING_RESULT.search("- **Result:** pending"))


class RemovalSanitizationTests(unittest.TestCase):
    def removal(self, section: str) -> list[Finding]:
        root = temporary_root(self)
        write_plan(root, "P3-R2-2026-11-01-remove", "completed", REGRESSION + "\n## Removal sanitization\n\n" + section)
        findings: list[Finding] = []
        validate_plans(root, findings)
        return rules(findings, "plan-removal")

    def test_prose_and_complete_fields_pass(self) -> None:
        self.assertEqual([], self.removal("Terms: `<select id=\"x\">`, NextButton. Final search: no live match.\n"))
        self.assertEqual([], self.removal("- Removed:\n  - interface\n  - styles\n- Final search: no match.\n"))

    def test_empty_placeholder_or_blank_field_fails(self) -> None:
        self.assertTrue(self.removal(""))
        self.assertTrue(self.removal("- Final search: <result>\n"))
        found = self.removal("- Removed: interface\n- Final search without remaining unjustified match:\n")
        self.assertEqual(1, len(found))
        self.assertIn("Final search", found[0].message)


class MissingReadmeTests(unittest.TestCase):
    def test_a_project_without_a_root_readme_is_a_finding_not_a_crash(self) -> None:
        root = temporary_root(self)
        (root / "FCVW" / "FRAMEWORK_LOCK.md").write_text("| Installed version | `V0.24.0` |\n| Release state | `published` |\n",
                                                         encoding="utf-8")
        findings: list[Finding] = []
        validate_fcvw.validate_version(root, findings)
        self.assertIn("README is missing", [item.message for item in findings])


class LocalizedLineageTests(unittest.TestCase):
    def test_translated_migration_tables_still_name_the_successor(self) -> None:
        tables = {
            "pt-BR": ("Removido", "Consolidado em"),
            "es": ("Eliminado", "Consolidado en"),
            "de": ("Entfernt", "Konsolidiert in"),
            "en-US": ("Removed", "Consolidated into"),
        }
        for language, (removed, consolidated) in tables.items():
            root = temporary_root(self)
            (root / "FCVW" / "MIGRATIONS.md").write_text(
                f"5. Passo:\n\n   | {removed} | {consolidated} |\n   |---|---|\n   | `HOOKS.md` | `AUTOMATION.md` |\n",
                encoding="utf-8")
            self.assertEqual({"HOOKS.md": "AUTOMATION.md"}, validate_fcvw.lineage(root), language)
            hint = validate_fcvw.successor_hint(root, root / "FCVW" / "README.md", "HOOKS.md")
            self.assertIn("now in AUTOMATION.md", hint, language)


class ContextFileTests(unittest.TestCase):
    def relationship(self, root: Path) -> list[Finding]:
        findings: list[Finding] = []
        validate_frontmatter_documents(root, findings)
        return rules(findings, "frontmatter-relationship")

    def test_repository_paths_and_plan_relative_spellings_both_resolve(self) -> None:
        root = temporary_root(self)
        (root / "src").mkdir()
        (root / "src" / "App.tsx").write_text("x", encoding="utf-8")
        (root / "FCVW" / "Plans" / "completed" / "notes.md").write_text("x", encoding="utf-8")
        plan = write_plan(root, "P3-R2-2026-11-01-paths", "completed", "Body.",
                          context=("src/App.tsx", "../../../src/App.tsx", "notes.md"))
        self.assertEqual([], self.relationship(root))
        self.assertEqual(["src/App.tsx", "FCVW/Plans/completed/notes.md"],
                         [item for item in mandatory_paths(root, plan) if item not in {"AGENTS.md", "FCVW/CONTEXT_MAP.md",
                                                                                       plan.relative_to(root).as_posix()}])

    def test_a_path_that_exists_nowhere_is_still_missing(self) -> None:
        root = temporary_root(self)
        write_plan(root, "P3-R2-2026-11-01-missing", "in_progress", "Body.", context=("src/Gone.tsx",))
        self.assertEqual(1, len(self.relationship(root)))


@unittest.skipUnless(HAS_GIT, "git is required for history-based successors")
class GitHistoryTests(unittest.TestCase):
    def repository(self) -> Path:
        root = temporary_root(self)
        git(root, "init", "-q")
        (root / "docs").mkdir()
        (root / "docs" / "guide.md").write_text("# Guide\n", encoding="utf-8")
        (root / "src").mkdir()
        (root / "src" / "old.ts").write_text("export const a = 1;\n", encoding="utf-8")
        (root / "FCVW" / "README.md").write_text("[guide](../docs/guide.md)\n", encoding="utf-8")
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "init")
        return root

    def test_renamed_targets_get_a_proven_successor_and_are_rewritten(self) -> None:
        root = self.repository()
        write_plan(root, "P3-R2-2026-11-01-renamed", "in_progress", "See [guide](../../../docs/guide.md).",
                   context=("docs/guide.md",))
        git(root, "mv", "docs/guide.md", "docs/handbook.md")
        git(root, "commit", "-q", "-m", "rename")
        validate_fcvw._GIT_RENAMES.clear()
        findings: list[Finding] = []
        validate_frontmatter_documents(root, findings)
        validate_fcvw.validate_markdown(root, findings)
        hinted = [item for item in findings if "renamed in git history to" in item.message]
        self.assertEqual(3, len(hinted), [item.message for item in findings])
        self.assertTrue(any("docs/handbook.md (--fix" in item.message for item in hinted))
        changes = fix_moved_plan_links(root)
        self.assertEqual(3, len(changes), changes)
        fcvw_cache.clear()
        findings = []
        validate_frontmatter_documents(root, findings)
        validate_fcvw.validate_markdown(root, findings)
        self.assertEqual([], [item for item in findings if item.rule in {"frontmatter-relationship", "markdown-link"}])

    def test_a_file_deleted_after_a_completed_record_is_history_not_a_defect(self) -> None:
        root = self.repository()
        write_plan(root, "P3-R2-2026-11-01-history", "completed", "Body.", context=("src/old.ts",))
        write_plan(root, "P3-R2-2026-11-01-active", "in_progress", "Body.", context=("src/old.ts",))
        git(root, "rm", "-q", "src/old.ts")
        git(root, "commit", "-q", "-m", "delete")
        validate_fcvw._GIT_DELETED.clear()
        found = {item.path.split("/")[-1]: item.severity for item in ContextFileTests.relationship(self, root)}
        self.assertEqual({"P3-R2-2026-11-01-history.md": "warning", "P3-R2-2026-11-01-active.md": "error"}, found)


class InventoryTests(unittest.TestCase):
    def tree(self) -> Path:
        root = temporary_root(self)
        for relative in ("AGENTS.md", "FCVW/README.md", "node_modules/pkg/README.md", ".tmp-api-smoke/FCVW/README.md",
                         "test-results/report.md", ".claude/worktrees/copy/AGENTS.md", "vendor/lib/doc.md", "docs/a.md"):
            (root / relative).parent.mkdir(parents=True, exist_ok=True)
            (root / relative).write_text("# x\n", encoding="utf-8")
        (root / ".claude" / "worktrees" / "copy" / ".git").write_text("gitdir: elsewhere\n", encoding="utf-8")
        return root

    def names(self, root: Path) -> list[str]:
        return [path.relative_to(root).as_posix() for path in governed_markdown_inventory(root)]

    def test_transient_trees_and_nested_worktrees_are_not_governed(self) -> None:
        root = self.tree()
        self.assertEqual(["AGENTS.md", "docs/a.md", "FCVW/README.md", "vendor/lib/doc.md"], self.names(root))
        (root / "FCVW" / "PROJECT.md").write_text('---\nungoverned_paths:\n  - "vendor/**"\n---\n', encoding="utf-8")
        self.assertNotIn("vendor/lib/doc.md", self.names(root))

    @unittest.skipUnless(HAS_GIT, "git is required")
    def test_git_ignore_rules_decide_inside_a_work_tree(self) -> None:
        root = self.tree()
        shutil.rmtree(root / ".claude")
        (root / ".gitignore").write_text("docs/\n", encoding="utf-8")
        git(root, "init", "-q")
        self.assertNotIn("docs/a.md", self.names(root))
        self.assertIn("FCVW/README.md", self.names(root), "untracked but not ignored files are governed")

    def test_repository_glob_semantics(self) -> None:
        self.assertTrue(glob_regex("FCVW/**/*.md").fullmatch("FCVW/README.md"))
        self.assertTrue(glob_regex("FCVW/**/*.md").fullmatch("FCVW/Plans/pending/x.md"))
        self.assertFalse(glob_regex("*.md").fullmatch("docs/a.md"))
        self.assertTrue(matches_ungoverned("docs/deep/a.md", ["docs"]))
        self.assertFalse(matches_ungoverned("documents/a.md", ["docs"]))

    @unittest.skipUnless(HAS_GIT, "git is required")
    def test_a_git_ignored_root_entry_is_local_state(self) -> None:
        from validate_fcvw import validate_clean_template

        root = self.tree()
        (root / "side-project").mkdir()
        (root / "side-project" / "README.md").write_text("# side\n", encoding="utf-8")
        git(root, "init", "-q")

        def contamination() -> set[str]:
            findings: list[Finding] = []
            validate_clean_template(root, findings)
            return {item.path for item in findings if item.rule == "clean-contamination"}

        self.assertIn("side-project", contamination())
        self.assertIn("side-project/README.md", self.names(root))
        with (root / ".git" / "info" / "exclude").open("a", encoding="utf-8") as stream:
            stream.write("/side-project/\n")
        self.assertNotIn("side-project", contamination())
        self.assertNotIn("side-project/README.md", self.names(root))

    def test_graph_and_catalog_read_one_inventory(self) -> None:
        root = self.tree()
        graph = build_graph(root)
        self.assertNotIn("node_modules/pkg/README.md", graph.nodes)
        self.assertNotIn(".tmp-api-smoke/FCVW/README.md", graph.nodes)


class DocumentGraphCommandTests(unittest.TestCase):
    def run_graph(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, "-B", str(TOOLS / "document_graph_fcvw.py"), "--root", str(root), *args],
                              capture_output=True, text=True, encoding="utf-8", check=False)

    def test_generation_and_validation_report_separate_states(self) -> None:
        root = temporary_root(self)
        (root / "AGENTS.md").write_text("[missing](FCVW/nothing.md)\n", encoding="utf-8")
        written = self.run_graph(root, "--write")
        self.assertEqual(0, written.returncode, written.stdout)
        self.assertIn("catalog_written=true", written.stdout)
        self.assertIn("validation=not_run", written.stdout)
        both = self.run_graph(root, "--write", "--check")
        self.assertEqual(1, both.returncode)
        self.assertIn("catalog_written=true validation=fail", both.stdout)
        self.assertTrue((root / ".fcvw-cache" / "document-graph.md").is_file())
        self.assertEqual([], list((root / ".fcvw-cache").glob("*.tmp")), "no partial file is left behind")
        self.assertEqual(1, self.run_graph(root).returncode)

    def test_a_catalog_that_cannot_be_written_is_its_own_exit_state(self) -> None:
        root = temporary_root(self)
        (root / "AGENTS.md").write_text("# ok\n", encoding="utf-8")
        (root / ".fcvw-cache" / "document-graph.md").mkdir(parents=True)
        result = self.run_graph(root, "--write")
        self.assertEqual(2, result.returncode, result.stdout)
        self.assertIn("catalog_written=false", result.stdout)


class GateSelectionTests(unittest.TestCase):
    TABLE = """---
schema: "fcvw/project@1"
---

### Validation gates

<a id="validation-gates"></a>

| Surface | Paths | Gates |
|---|---|---|
| governance | `FCVW/**/*.md`, `AGENTS.md` | `git diff --check`, `python FCVW/tools/validate_fcvw.py --root .` |
| frontend | `src/**` | `npx tsc --noEmit`, `npm run build` |
| `<surface>` | `<glob>` | `<command>` |
| full | | `npm run lint`, `npm run build`, `npm test` |
"""

    def table(self, text: str | None = TABLE):
        root = temporary_root(self)
        if text is not None:
            (root / "FCVW" / "PROJECT.md").write_text(text, encoding="utf-8")
        return root, read_gate_table(root)

    def test_documentation_only_change_runs_only_governance_gates(self) -> None:
        _, table = self.table()
        report = select_gates(table, ["FCVW/Plans/pending/P3-R2-2026-11-01-x.md", "AGENTS.md"])
        self.assertEqual("governance", report["decision"])
        self.assertNotIn("npm test", report["gates"])

    def test_surfaces_union_and_conservative_escalation(self) -> None:
        _, table = self.table()
        mixed = select_gates(table, ["FCVW/README.md", "src/App.tsx"])
        self.assertEqual(["git diff --check", "npx tsc --noEmit", "npm run build"],
                         [gate for gate in mixed["gates"] if gate != "python FCVW/tools/validate_fcvw.py --root ."])
        for report in (select_gates(table, ["server/index.js"]), select_gates(table, ["src/App.tsx"], risk="R4"),
                       select_gates(table, ["FCVW/README.md"], release=True)):
            self.assertEqual("full", report["decision"])
            self.assertIn("npm test", report["gates"])

    def test_without_a_table_only_governance_markdown_is_known(self) -> None:
        _, table = self.table(None)
        self.assertEqual("governance", select_gates(table, ["FCVW/PLANNING.md"])["decision"])
        self.assertEqual("full", select_gates(table, ["FCVW/tools/validate_fcvw.py"])["decision"])

    def test_invalid_tables_are_reported_by_the_validator(self) -> None:
        root, table = self.table(self.TABLE.replace("| full | | `npm run lint`, `npm run build`, `npm test` |\n", "")
                                 .replace("| `<surface>` | `<glob>` | `<command>` |\n", "| Back End | `server/**` | `npm t` |\n"))
        findings: list[Finding] = []
        validate_project_gates(root, findings)
        messages = " ".join(item.message for item in findings)
        self.assertIn("invalid surface name", messages)
        self.assertIn("`full` row", messages)

    def test_command_line_report(self) -> None:
        root, _ = self.table()
        output = io.StringIO()
        from gates_fcvw import main

        with redirect_stdout(output):
            code = main(["--root", str(root), "--paths", "src/App.tsx", "--format", "json"])
        self.assertEqual(0, code)
        self.assertEqual("frontend", json.loads(output.getvalue())["decision"])


@unittest.skipUnless(HAS_GIT, "git is required for an end-to-end incremental run")
class IncrementalGateEndToEndTests(unittest.TestCase):
    """The whole loop on a copy of this framework turned into a project with debt."""

    def test_write_baseline_then_only_new_findings_fail(self) -> None:
        from release_layout_fcvw import governed_root

        source = governed_root(Path(__file__))
        root = temporary_root(self)
        shutil.rmtree(root / "FCVW")
        for name in ("AGENTS.md", "README.md", "LICENSE", "NOTICE"):
            if (source / name).is_file():
                shutil.copy2(source / name, root / name)
        shutil.copytree(source / "FCVW", root / "FCVW", ignore=shutil.ignore_patterns("__pycache__", ".fcvw-cache"))
        tools = TOOLS
        if (source / "tools").is_dir():
            shutil.copytree(source / "tools", root / "tools", ignore=shutil.ignore_patterns("__pycache__"))
            tools = root / "tools"
        lock = root / "FCVW" / "FRAMEWORK_LOCK.md"
        lock.write_text(lock.read_text(encoding="utf-8").replace("`clean-template`", "`project-instantiated`"), encoding="utf-8")
        write_plan(root, "P3-R2-2026-11-01-old-debt", "completed", "## Acceptance criteria\n\n- [ ] Old open box.\n" + REGRESSION)

        def validate(*args: str) -> subprocess.CompletedProcess[str]:
            return subprocess.run([sys.executable, "-B", str(tools / "validate_fcvw.py"), "--root", str(root), *args],
                                  capture_output=True, text=True, encoding="utf-8", check=False)

        before = validate()
        self.assertEqual(1, before.returncode)
        self.assertIn("profile=instantiated", before.stdout)
        written = validate("--write-baseline", "--baseline-owner", "maintainer")
        self.assertEqual(0, written.returncode, written.stdout)
        clean = validate()
        self.assertEqual(0, clean.returncode, clean.stdout)
        self.assertIn("profile=incremental", clean.stdout)
        self.assertIn("known finding(s) accepted", clean.stdout)
        self.assertNotIn("BASELINE [", clean.stdout, "accepted debt is summarized, not listed")
        write_plan(root, "P3-R2-2026-11-02-new-debt", "completed", "## Acceptance criteria\n\n- [ ] New open box.\n" + REGRESSION)
        regressed = validate()
        self.assertEqual(1, regressed.returncode)
        self.assertIn("New open box", regressed.stdout)
        self.assertNotIn("Old open box", regressed.stdout)


if __name__ == "__main__":
    unittest.main()
