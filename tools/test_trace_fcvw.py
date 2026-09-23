"""Cross-tool traces report decisions without copying retrieved or product content."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from trace_fcvw import append


class TraceTests(unittest.TestCase):
    def test_trace_is_metadata_only_and_cannot_alias_source(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            root = base / 'project'
            root.mkdir()
            source = base / 'source.json'
            source.write_text('private-canary', encoding='utf-8')
            trace = root / '.fcvw-cache' / 'trace.jsonl'
            append(trace, root, run_id='run-1', component='qa_wiki', status='blocked',
                   reason='pending', duration_ms=3, protected=[source])
            text = trace.read_text(encoding='utf-8')
            self.assertNotIn('private-canary', text)
            record = json.loads(text)
            self.assertEqual(record['run_id'], 'run-1')
            self.assertEqual(record['token_source'], 'unavailable')
            with self.assertRaisesRegex(ValueError, 'overwrite'):
                append(source, root, run_id='run-1', component='qa_wiki',
                       status='pass', reason='test', protected=[source])
            self.assertEqual(source.read_text(encoding='utf-8'), 'private-canary')

    def test_retrieval_cli_writes_correlated_opt_in_event(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            root = base / 'project'
            (root / 'FCVW').mkdir(parents=True)
            (root / 'AGENTS.md').write_text('# Agent\n', encoding='utf-8')
            (root / 'FCVW/CONTEXT_MAP.md').write_text('# Routes\n', encoding='utf-8')
            index = base / 'index.jsonl'
            index.write_text('', encoding='utf-8')
            trace = root / '.fcvw-cache' / 'decisions.jsonl'
            tool = Path(__file__).with_name('retrieve_context.py')
            completed = subprocess.run([sys.executable, '-B', str(tool), '--root', str(root),
                                        '--index', str(index), '--query', 'private task',
                                        '--trace', str(trace), '--trace-run-id', 'task-42'],
                                       capture_output=True, text=True, check=False)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            row = json.loads(trace.read_text(encoding='utf-8'))
            self.assertEqual((row['run_id'], row['component'], row['status']),
                             ('task-42', 'retrieval', 'pass'))
            self.assertNotIn('private task', trace.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
