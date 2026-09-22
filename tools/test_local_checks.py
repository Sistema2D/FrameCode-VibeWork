"""Failure propagation and evidence boundaries of the optional local runner."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from check_fcvw import release_assets, run_checks, run_step, snapshot


class LocalChecksTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'source'
        (self.root / 'tools').mkdir(parents=True)
        (self.root / 'AGENTS.md').write_text('Trusted fixture', encoding='utf-8')
        for name in ('validate_fcvw.py', 'benchmark_retrieval_fcvw.py', 'verify_release_fcvw.py'):
            (self.root / 'tools' / name).write_text('# fixture', encoding='utf-8')

    def fake_step(self, name, command, root, directory, timeout):
        log = directory / (name + '.log')
        log.write_text(json.dumps({'version': 'test', 'executable': command[0], 'os': 'TEST-OS', 'machine': 'test'})
                       if name == 'runtime' else 'test evidence', encoding='utf-8')
        return {'name': name, 'command': command, 'status': 'pass', 'log': str(log), 'returncode': 0}

    def test_full_run_records_commands_and_actual_runtime(self):
        with patch('check_fcvw.run_step', side_effect=self.fake_step):
            report, path = run_checks(self.root, self.base / 'evidence', ['python-A', 'python-B'])
        self.assertEqual(report['status'], 'pass')
        self.assertEqual(len(report['runtimes']), 2)
        self.assertEqual(report['runtimes'][1]['identity']['os'], 'TEST-OS')
        self.assertEqual([s['name'] for s in report['runtimes'][0]['steps']],
                         ['runtime', 'tests', 'governance', 'benchmark', 'installed'])
        self.assertIn('--run-tests', report['runtimes'][0]['steps'][-1]['command'])
        self.assertEqual(json.loads(path.read_text(encoding='utf-8'))['status'], 'pass')

    def test_failed_check_cannot_be_hidden_by_later_pass(self):
        def failing(*args):
            result = self.fake_step(*args)
            if args[0] == 'tests':
                result.update(status='fail', returncode=7)
            return result
        with patch('check_fcvw.run_step', side_effect=failing):
            report, _ = run_checks(self.root, self.base / 'evidence', ['python'])
        self.assertEqual(report['status'], 'fail')
        self.assertEqual(report['runtimes'][0]['steps'][-1]['status'], 'pass')

    def test_unavailable_runtime_is_reported_without_silent_fallback(self):
        report, path = run_checks(self.root, self.base / 'evidence', [str(self.base / 'missing-python')])
        self.assertEqual(report['status'], 'fail')
        self.assertEqual(len(report['runtimes'][0]['steps']), 1)
        self.assertTrue(path.is_file())

    def test_failure_and_timeout_keep_logs(self):
        fail = run_step('failed', [sys.executable, '-c', 'print("failure evidence");raise SystemExit(7)'],
                        self.root, self.base, 5)
        self.assertEqual(fail['returncode'], 7)
        self.assertIn('failure evidence', Path(fail['log']).read_text(encoding='utf-8'))
        timeout = run_step('timeout', [sys.executable, '-c', 'import time;time.sleep(5)'], self.root, self.base, 1)
        self.assertEqual(timeout['status'], 'fail')
        self.assertIn('exceeded', timeout['error'])

    def test_asset_set_must_be_complete_and_one_version(self):
        with self.assertRaisesRegex(ValueError, 'four'):
            release_assets(self.base)
        for lang in ('pt-BR', 'en-US', 'es', 'de'):
            (self.base / f'FrameCode-VibeWork-V0.18.0-{lang}.zip').touch()
        with self.assertRaisesRegex(ValueError, 'SHA256SUMS'):
            release_assets(self.base)
        (self.base / 'SHA256SUMS.txt').touch()
        self.assertEqual(len(release_assets(self.base)), 4)
        (self.base / 'FrameCode-VibeWork-V0.18.0-de.zip').rename(self.base / 'FrameCode-VibeWork-V0.19.0-de.zip')
        with self.assertRaisesRegex(ValueError, 'one version'):
            release_assets(self.base)

    def test_source_hash_binds_changes_but_excludes_derived_cache(self):
        original = snapshot(self.root)['tree_sha256']
        cache = self.root / '.fcvw-cache'; cache.mkdir()
        (cache / 'report.json').write_text('{}', encoding='utf-8')
        self.assertEqual(snapshot(self.root)['tree_sha256'], original)
        (self.root / 'AGENTS.md').write_text('changed', encoding='utf-8')
        self.assertNotEqual(snapshot(self.root)['tree_sha256'], original)

    def test_output_cannot_contaminate_source_or_release_tree(self):
        with self.assertRaisesRegex(ValueError, 'under .fcvw-cache'):
            run_checks(self.root, self.root / 'reports', ['python'])
        with self.assertRaisesRegex(ValueError, 'requires --release-dir'):
            run_checks(self.root, self.base / 'reports', ['python'], release_source=self.root)
        with patch('check_fcvw.run_step', side_effect=self.fake_step):
            report, _ = run_checks(self.root, self.root / '.fcvw-cache/checks', ['python'])
        self.assertTrue(report['source_unchanged'])

    def test_source_change_during_run_invalidates_evidence(self):
        def changing(*args):
            result = self.fake_step(*args)
            (self.root / 'AGENTS.md').write_text('changed while testing', encoding='utf-8')
            return result
        with patch('check_fcvw.run_step', side_effect=changing):
            report, _ = run_checks(self.root, self.base / 'reports', ['python'])
        self.assertEqual(report['status'], 'fail')
        self.assertFalse(report['source_unchanged'])

    def test_archive_steps_use_explicit_matching_trusted_source(self):
        for lang in ('pt-BR', 'en-US', 'es', 'de'):
            (self.base / f'FrameCode-VibeWork-V0.18.0-{lang}.zip').touch()
        (self.base / 'SHA256SUMS.txt').touch()
        with patch('check_fcvw.run_step', side_effect=self.fake_step):
            report, _ = run_checks(self.root, self.base / 'reports', ['python'], release_dir=self.base,
                                   release_source=self.root)
        steps = report['runtimes'][0]['steps']
        self.assertEqual(len(steps), 9)
        self.assertEqual(len(report['release_assets']), 4)
        self.assertEqual(len(report['release_sha256']), 5)
        self.assertTrue(report['release_assets_unchanged'])
        for step in steps[-4:]:
            self.assertIn(str(self.root), step['command'])
            self.assertIn('--checksums', step['command'])
        def changing(*args):
            result = self.fake_step(*args)
            (self.base / 'SHA256SUMS.txt').write_text('changed during run', encoding='utf-8')
            return result
        with patch('check_fcvw.run_step', side_effect=changing):
            report, _ = run_checks(self.root, self.base / 'reports', ['python'], release_dir=self.base)
        self.assertFalse(report['release_assets_unchanged'])
        self.assertEqual(report['status'], 'fail')


if __name__ == '__main__':
    unittest.main()
