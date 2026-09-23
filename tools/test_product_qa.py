"""Optional product-wiki checks preserve unknown intent and honest live coverage."""
from pathlib import Path
import tempfile
import unittest

from qa_wiki_fcvw import evaluate, surface
from context_routing_fcvw import resolve_routes
from release_layout_fcvw import governed_root


def fixture(root: Path) -> None:
    (root / 'surface.md').write_text('''---
schema: "fcvw/wiki@1"
id: "UI-profile"
type: "component"
qa_surface: "screen"
route: "/profile"
---
# Profile
## Elements
| element_id | kind | locator | purpose |
|---|---|---|---|
| name | field | textbox: Name | Enter display name |
| save | button | button: Save | Save profile |
## Cases
| case_id | element_ids | preconditions | action | expectation | expected | source |
|---|---|---|---|---|---|---|
| save-name | name, save | Disposable profile | Enter Alice and save | approved | Name is Alice | requirements.md |
''', encoding='utf-8')
    (root / 'inventory.md').write_text('''---
inventory_status: "complete"
scope: "local synthetic profile"
app_revision: "fixture-1"
roles: "test-user"
---
## Surfaces
| surface_id | page | kind | route | discovery |
|---|---|---|---|---|
| UI-profile | surface.md | screen | /profile | mapped |
## Frontier
| target | reason | status |
|---|---|---|
''', encoding='utf-8')
    digest = surface(root, 'surface.md')['sha256']
    (root / 'run.md').write_text('''---
schema: "fcvw/wiki@1"
type: "audit"
qa_run: "true"
app_revision: "fixture-1"
environment: "isolated synthetic fixture"
runtime: "fixture browser"
roles: "test-user"
observed_at: "2026-09-22T12:00:00+00:00"
---
## Contracts
| surface_id | sha256 |
|---|---|
| UI-profile | '''+digest+''' |
## Results
| surface_id | case_id | result | observed | evidence |
|---|---|---|---|---|
| UI-profile | save-name | pass | Name is Alice | trace-1 |
''', encoding='utf-8')


class ProductQATests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root = Path(temp.name); fixture(self.root)

    def replace(self, name, old, new):
        p = self.root / name
        p.write_text(p.read_text(encoding='utf-8').replace(old, new), encoding='utf-8')

    def test_structure_never_claims_execution(self):
        report = evaluate(self.root, ['surface.md'])
        self.assertEqual(report['structural_status'], 'pass')
        self.assertEqual(report['execution_status'], 'not_run')
        self.assertEqual(report['missing_cases'], [['UI-profile', 'save-name']])

    def test_complete_declared_run_and_real_failure_are_distinct(self):
        report = evaluate(self.root, [], inventory='inventory.md', run='run.md')
        self.assertEqual(report['execution_status'], 'pass')
        self.assertEqual(report['consultation_provenance'], 'declared_only')
        self.replace('run.md', '| pass | Name is Alice |', '| fail | Name is Bob |')
        self.assertEqual(evaluate(self.root, ['surface.md'], run='run.md')['execution_status'], 'fail')

    def test_unknown_expectations_cannot_pass(self):
        old = surface(self.root, 'surface.md')['sha256']
        self.replace('surface.md', '| approved | Name is Alice | requirements.md |', '| unknown | unknown | unknown |')
        self.replace('run.md', old, surface(self.root, 'surface.md')['sha256'])
        with self.assertRaisesRegex(ValueError, 'cannot pass'):
            evaluate(self.root, ['surface.md'], run='run.md')
        self.replace('run.md', '| pass | Name is Alice | trace-1 |', '| blocked | Product intent unconfirmed | - |')
        self.assertEqual(evaluate(self.root, ['surface.md'], run='run.md')['execution_status'], 'incomplete')

    def test_old_pass_cannot_survive_changed_contract(self):
        self.replace('surface.md', 'Name is Alice', 'Name is Alicia')
        with self.assertRaisesRegex(ValueError, 'current selected behavior'):
            evaluate(self.root, ['surface.md'], run='run.md')

    def test_notes_do_not_invalidate_behavior_hash(self):
        old = surface(self.root, 'surface.md')['sha256']
        p = self.root / 'surface.md'
        p.write_text(p.read_text(encoding='utf-8')+'\n## Observed behavior\nSee latest run.\n', encoding='utf-8')
        self.assertEqual(surface(self.root, 'surface.md')['sha256'], old)

    def test_missing_duplicate_or_evidenceless_results_rejected(self):
        row = '| UI-profile | save-name | pass | Name is Alice | trace-1 |'
        original = (self.root / 'run.md').read_text(encoding='utf-8')
        self.replace('run.md', row, '')
        self.assertEqual(evaluate(self.root, ['surface.md'], run='run.md')['execution_status'], 'incomplete')
        (self.root / 'run.md').write_text(original+row+'\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            evaluate(self.root, ['surface.md'], run='run.md')
        (self.root / 'run.md').write_text(original.replace('trace-1', '-'), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'evidence'):
            evaluate(self.root, ['surface.md'], run='run.md')

    def test_uncovered_element_and_duplicate_ids_rejected(self):
        self.replace('surface.md', '| name, save |', '| name |')
        with self.assertRaisesRegex(ValueError, 'every declared element'):
            surface(self.root, 'surface.md')
        fixture(self.root)
        self.replace('surface.md', '| save | button |', '| name | button |')
        with self.assertRaisesRegex(ValueError, 'duplicate element'):
            surface(self.root, 'surface.md')

    def test_incomplete_discovery_cannot_claim_bootstrap_complete(self):
        self.replace('inventory.md', '| mapped |', '| blocked |')
        with self.assertRaisesRegex(ValueError, 'unresolved discovery'):
            evaluate(self.root, ['surface.md'], inventory='inventory.md')
        self.replace('inventory.md', '"complete"', '"in_progress"')
        self.assertEqual(evaluate(self.root, ['surface.md'], inventory='inventory.md')['inventory_status'], 'in_progress')

    def test_first_run_with_every_surface_blocked_keeps_a_valid_checkpoint(self):
        self.replace('inventory.md', '"complete"', '"in_progress"')
        self.replace('inventory.md', '| mapped |', '| blocked |')
        self.replace('inventory.md', '\n|---|---|---|\n', '\n|---|---|---|\n| /profile | application unavailable | blocked |\n')
        report = evaluate(self.root, [], inventory='inventory.md')
        self.assertEqual(report['inventory_status'], 'in_progress')
        self.assertEqual(report['execution_status'], 'not_run')
        self.assertEqual(report['surfaces'], 0)
        self.assertEqual(report['checkpoint_state'], 'blocked')
        with self.assertRaisesRegex(ValueError, 'select at least one mapped'):
            evaluate(self.root, [], inventory='inventory.md', run='run.md')

    def test_frontier_and_revision_mismatch_are_explicit(self):
        self.replace('inventory.md', '\n|---|---|---|\n', '\n|---|---|---|\n| /admin | Unavailable role | blocked |\n')
        with self.assertRaisesRegex(ValueError, 'unresolved discovery'):
            evaluate(self.root, [], inventory='inventory.md')
        fixture(self.root)
        self.replace('run.md', 'fixture-1', 'fixture-2')
        with self.assertRaisesRegex(ValueError, 'same application revision'):
            evaluate(self.root, [], inventory='inventory.md', run='run.md')

    def test_fenced_fake_tables_and_outside_paths_not_trusted(self):
        self.replace('surface.md', '## Elements', '```markdown\n## Elements')
        with self.assertRaisesRegex(ValueError, 'missing Elements'):
            surface(self.root, 'surface.md')
        with self.assertRaisesRegex(ValueError, 'inside'):
            surface(self.root, '../outside.md')

    def test_qa_session_is_explicit_and_other_routes_unchanged(self):
        root = governed_root(Path(__file__))
        qa = resolve_routes(root, sessions=['product_qa'])['mandatory_paths']
        self.assertIn('FCVW/skills/QA/SKILL.md', qa)
        normal = resolve_routes(root, sessions=['security'])['mandatory_paths']
        self.assertNotIn('FCVW/skills/QA/SKILL.md', normal)
        self.assertEqual(normal, ['FCVW/SECURITY.md', 'FCVW/DATA.md', 'FCVW/REGRESSION_GUARDS.md'])

    def test_non_gui_targets_use_same_contract_without_browser(self):
        for kind, route, runtime in (
            ('cli', 'cli:profile/set-name', 'Windows; native executable; terminal'),
            ('library', 'cpp:Profile::set_name', 'Linux; C++ test harness'),
            ('api', 'http:PUT/profile', 'HTTP client; staging API'),
            ('firmware', 'uart:board/profile', 'board revision A; firmware build fixture-1'),
            ('device', 'gpio:board/output', 'hardware-in-loop; instrument model test'),
            ('protocol', 'serial:device/config', 'protocol simulator; physical hardware excluded'),
            ('service', 'service:profile-worker', 'container; process harness'),
        ):
            with self.subTest(kind=kind):
                fixture(self.root)
                old = surface(self.root, 'surface.md')['sha256']
                self.replace('surface.md', 'qa_surface: "screen"', 'qa_surface: "'+kind+'"')
                self.replace('surface.md', '/profile', route)
                self.replace('inventory.md', '| screen | /profile |', '| '+kind+' | '+route+' |')
                self.replace('run.md', 'fixture browser', runtime)
                self.replace('run.md', old, surface(self.root, 'surface.md')['sha256'])
                self.assertEqual(evaluate(self.root, [], inventory='inventory.md', run='run.md')['execution_status'], 'pass')

    def test_missing_execution_runtime_is_rejected(self):
        self.replace('run.md', 'runtime: "fixture browser"', 'runtime: "unknown"')
        with self.assertRaisesRegex(ValueError, 'runtime'):
            evaluate(self.root, ['surface.md'], run='run.md')

    def test_numeric_requirements_accept_comparisons_but_not_placeholders(self):
        self.replace('surface.md', 'Name is Alice', 'Response time < 5 ms')
        self.assertIn('sha256', surface(self.root, 'surface.md'))
        self.replace('surface.md', 'Response time < 5 ms', '<approved threshold>')
        with self.assertRaisesRegex(ValueError, 'approved expectation'):
            surface(self.root, 'surface.md')

    def divergence(self, *, question='Expected Alice; observed Bob. Which behavior should prevail?',
                   question_ref='conversation/question-1', decision='pending', decision_ref='-'):
        p = self.root / 'run.md'
        p.write_text(p.read_text(encoding='utf-8') + '''
## Divergences
| surface_id | case_id | question | question_ref | decision | decision_ref |
|---|---|---|---|---|---|
| UI-profile | save-name | ''' + ' | '.join((question, question_ref, decision, decision_ref)) + ' |\n', encoding='utf-8')

    def test_failed_case_without_question_blocks_decision_gate(self):
        self.replace('run.md', '| pass | Name is Alice |', '| fail | Name is Bob |')
        report = evaluate(self.root, ['surface.md'], run='run.md')
        self.assertEqual(report['user_decision_gate'], 'blocked')
        self.assertEqual(report['divergence_metrics'], dict(total=1, asked=0, unasked=1,
                         consultation_coverage_pct=0, decided=0, pending_decisions=1))
        self.assertEqual(report['pending_divergences'][0]['expected'], 'Name is Alice')
        self.assertEqual(report['pending_divergences'][0]['observed'], 'Name is Bob')

    def test_drafted_question_is_not_consultation_and_asked_is_not_answered(self):
        self.replace('run.md', '| pass | Name is Alice |', '| fail | Name is Bob |')
        self.divergence(question_ref='-')
        report = evaluate(self.root, ['surface.md'], run='run.md')
        self.assertEqual(report['divergence_metrics']['asked'], 0)
        self.replace('run.md', '| - | pending |', '| conversation/question-1 | pending |')
        report = evaluate(self.root, ['surface.md'], run='run.md')
        self.assertEqual(report['divergence_metrics']['consultation_coverage_pct'], 100)
        self.assertEqual(report['divergence_metrics']['pending_decisions'], 1)
        self.assertEqual(report['user_decision_gate'], 'blocked')

    def test_user_directions_preserve_original_failure_and_contract(self):
        for decision in ('fix_implementation', 'update_expectation', 'investigate', 'defer'):
            with self.subTest(decision=decision):
                fixture(self.root)
                digest = surface(self.root, 'surface.md')['sha256']
                self.replace('run.md', '| pass | Name is Alice |', '| fail | Name is Bob |')
                self.divergence(decision=decision, decision_ref='conversation/user-response-2')
                report = evaluate(self.root, ['surface.md'], run='run.md')
                self.assertEqual(report['user_decision_gate'], 'clear')
                self.assertEqual(report['divergence_metrics']['pending_decisions'], 0)
                self.assertEqual(report['execution_status'], 'fail')
                self.assertEqual(report['contract_hashes']['UI-profile'], digest)

    def test_decisions_require_user_response_and_real_question_fields(self):
        for args in ({'decision': 'fix_implementation'},
                     {'decision': 'update_expectation', 'question_ref': '-', 'decision_ref': 'user-2'},
                     {'decision': 'update_expectation', 'question': '-', 'decision_ref': 'user-2'},
                     {'decision': 'automatic_approval', 'decision_ref': 'model-confidence'}):
            with self.subTest(args=args):
                fixture(self.root)
                self.replace('run.md', '| pass | Name is Alice |', '| fail | Name is Bob |')
                self.divergence(**args)
                with self.assertRaisesRegex(ValueError, 'decision'):
                    evaluate(self.root, ['surface.md'], run='run.md')

    def test_divergence_identity_and_nonpassing_result_required(self):
        self.divergence()
        with self.assertRaisesRegex(ValueError, 'non-passing'):
            evaluate(self.root, ['surface.md'], run='run.md')
        self.replace('run.md', '| pass | Name is Alice |', '| fail | Name is Bob |')
        self.replace('run.md', '| UI-profile | save-name | Expected', '| UI-missing | save-name | Expected')
        with self.assertRaisesRegex(ValueError, 'non-passing'):
            evaluate(self.root, ['surface.md'], run='run.md')
        self.replace('run.md', '| UI-missing |', '| UI-profile |')
        p = self.root / 'run.md'
        text = p.read_text(encoding='utf-8')
        p.write_text(text + text.splitlines()[-1] + '\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'unique'):
            evaluate(self.root, ['surface.md'], run='run.md')

    def test_no_divergence_is_not_applicable_and_provisional_mismatch_still_blocks(self):
        report = evaluate(self.root, ['surface.md'])
        self.assertEqual(report['user_decision_gate'], 'not_evaluated')
        report = evaluate(self.root, ['surface.md'], run='run.md')
        self.assertIsNone(report['divergence_metrics']['consultation_coverage_pct'])
        self.assertEqual(report['user_decision_gate'], 'clear')
        old = surface(self.root, 'surface.md')['sha256']
        self.replace('surface.md', '| approved |', '| provisional |')
        self.replace('run.md', old, surface(self.root, 'surface.md')['sha256'])
        self.replace('run.md', '| pass | Name is Alice |', '| blocked | Bob observed; intent unconfirmed |')
        # Lack of access alone need not imply a mismatch; an explicit discrepancy does.
        self.assertEqual(evaluate(self.root, ['surface.md'], run='run.md')['divergence_metrics']['total'], 0)
        self.divergence()
        report = evaluate(self.root, ['surface.md'], run='run.md')
        self.assertEqual(report['divergence_metrics']['total'], 1)
        self.assertEqual(report['user_decision_gate'], 'blocked')

    def test_partial_consultation_cannot_hide_another_failed_case(self):
        old = surface(self.root, 'surface.md')['sha256']
        p = self.root / 'surface.md'
        text = p.read_text(encoding='utf-8')
        row = text.splitlines()[-1]
        p.write_text(text + row.replace('save-name', 'save-again') + '\n', encoding='utf-8')
        self.replace('run.md', old, surface(self.root, 'surface.md')['sha256'])
        self.replace('run.md', '| pass | Name is Alice |', '| fail | Name is Bob |')
        p = self.root / 'run.md'
        text = p.read_text(encoding='utf-8')
        p.write_text(text + text.splitlines()[-1].replace('save-name', 'save-again') + '\n', encoding='utf-8')
        self.divergence(decision='fix_implementation', decision_ref='conversation/user-2')
        report = evaluate(self.root, ['surface.md'], run='run.md')
        self.assertEqual(report['divergence_metrics'], dict(total=2, asked=1, unasked=1,
                         consultation_coverage_pct=50, decided=1, pending_decisions=1))
        self.assertEqual(report['user_decision_gate'], 'blocked')


if __name__ == '__main__':
    unittest.main()
