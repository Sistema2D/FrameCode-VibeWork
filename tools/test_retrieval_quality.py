"""Regression cases for exact identity, source-driven routes and bounded chunks."""
from __future__ import annotations

import copy
from datetime import date
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from benchmark_retrieval_fcvw import benchmark, synthetic_corpus, validate_cases
from build_context_index import bounded_chunks, build_index
from context_routing_fcvw import changed_file_events, normalized_path, resolve_routes, route_tables
from context_selection_fcvw import estimated_tokens, select_chunks
from document_graph_fcvw import build_graph, markdown_files
from fcvw_cache import clear
from knowledge_graph_fcvw import build_knowledge_graph
from release_layout_fcvw import governed_root
from retrieve_context import bm25, exact_requested
from verify_release_fcvw import verify_archive, validate_installed

ROOT = governed_root(Path(__file__))
# Framework tools live in tools/ in the source checkout and FCVW/tools/ when installed.
TOOLS = "tools/" if (ROOT / "tools" / "validate_fcvw.py").is_file() else "FCVW/tools/"


def chunk(path="a.md", text="Useful paragraph.", ident="a.md#one", score=1):
    return {"path": path, "chunk_id": ident, "excerpt": text, "score": score, "excerpt_complete": True}


class ExactIdentityTests(unittest.TestCase):
    def test_incidental_substrings_are_not_exact(self):
        for q in ("maintain docs", "email maintenance", "AI.md.bak", "not-AI.md", "foo/AI.md"):
            with self.subTest(q=q):
                self.assertFalse(exact_requested(q, {"path": "archive/AI.md"}))

    def test_explicit_path_name_stem_chunk_and_id(self):
        record = {"path": "archive/AI.md", "id": "NOTE-012", "chunk_id": "archive/AI.md#old"}
        for q in ("read AI", "read AI.md.", "`archive/AI.md`", "ARCHIVE\\AI.md", "NOTE-012", "archive/AI.md#old"):
            with self.subTest(q=q):
                self.assertTrue(exact_requested(q, record))

    def test_exact_regression_affects_real_ranking(self):
        record = {"path": "archive/AI.md", "content": "maintain docs", "retrieval_scope": "exact_only"}
        self.assertEqual(bm25("maintain docs", [record]), [])
        self.assertTrue(bm25("AI maintain docs", [record]))

    def test_temporary_test_markdown_never_enters_optional_index(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / '.codex-test-tmp' / 'secret.md'
            path.parent.mkdir()
            path.write_text('## Private fixture\nTemporary text.', encoding='utf-8')
            self.assertEqual(build_index(root), [])

    def test_benchmark_creates_requested_report_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / 'new' / 'benchmark.json'
            completed = subprocess.run(
                [sys.executable, '-B', str(Path(__file__).with_name('benchmark_retrieval_fcvw.py')),
                 '--root', str(ROOT), '--check', '--output', str(destination)],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(json.loads(destination.read_text(encoding='utf-8'))['corpus'],
                             'synthetic regression corpus (12 cases)')


class RoutingTests(unittest.TestCase):
    def test_cumulative_sessions_events_files(self):
        result = resolve_routes(ROOT, sessions=["security"], events=["data"], changed_files=[TOOLS + "retrieve_context.py"])
        expected = {"SECURITY", "DATA", "TESTS", "AI", "PLANNING", "REGRESSION_GUARDS", "ARCHITECTURAL_DECISIONS"}
        self.assertTrue({f"FCVW/{p}.md" for p in expected} <= set(result["mandatory_paths"]))
        self.assertTrue(all(result["reasons"][p] for p in result["mandatory_paths"]))
        self.assertIn('FCVW/PLANNING.md', result['section_hints'])

    def test_unknown_trigger_and_path_escape_fail(self):
        for kwargs in ({"sessions": ["missing"]}, {"events": ["missing"]}, {"changed_files": ["../secret"]}):
            with self.assertRaises(ValueError):
                resolve_routes(ROOT, **kwargs)
        for path in ("C:\\secret", "//server/share", "/etc/passwd", "a/../b"):
            with self.assertRaises(ValueError):
                normalized_path(path)

    def test_declared_file_operation_avoids_unrelated_filesystem_route(self):
        modified = resolve_routes(ROOT, events=['policy'],
                                  file_changes=['modify:FCVW/README.md'], versioned_change=True)
        self.assertNotIn('filesystem', modified['events'])
        self.assertIn('policy', modified['events'])
        added = resolve_routes(ROOT, events=['change'], file_changes=['add:FCVW/new.md'],
                               versioned_change=True)
        self.assertIn('filesystem', added['events'])
        internal = resolve_routes(ROOT, events=['change'],
                                  file_changes=['modify:' + TOOLS + 'fcvw_cache.py'], versioned_change=True)
        self.assertNotIn('public_interface', internal['events'])

    def test_project_profile_edit_does_not_trigger_framework_policy(self):
        # Regression: every FCVW/*.md used to trigger event:policy by path depth.
        profile = resolve_routes(ROOT, events=['change'], file_changes=['modify:FCVW/SECURITY.md'],
                                 versioned_change=True)
        self.assertNotIn('policy', profile['events'])
        self.assertIn('security', profile['events'])
        self.assertNotIn('FCVW/SCHEMAS.md', profile['mandatory_paths'])
        policy = resolve_routes(ROOT, events=['change'], file_changes=['modify:FCVW/PLANNING.md'],
                                versioned_change=True)
        self.assertIn('policy', policy['events'])
        template = resolve_routes(ROOT, events=['change'],
                                  file_changes=['modify:FCVW/governance/TEMPLATE_PLAN.md'], versioned_change=True)
        self.assertIn('policy', template['events'])

    def test_unknown_or_deleted_root_document_stays_conservative(self):
        deleted = resolve_routes(ROOT, events=['change'], file_changes=['delete:FCVW/REMOVED_POLICY.md'],
                                 versioned_change=True)
        self.assertIn('policy', deleted['events'])

    def test_framework_schema_catalog_is_not_application_data(self):
        schemas = resolve_routes(ROOT, events=['change'], file_changes=['modify:FCVW/SCHEMAS.md'],
                                 versioned_change=True)
        self.assertNotIn('data', schemas['events'])
        self.assertIn('policy', schemas['events'])

    # Phase 3 case table: path + operation -> implied events. Application paths
    # imply only file operations; framework paths keep their exact surfaces.
    PATH_EVENT_CASES = (
        ("modify", "src/auth_service.py", {"change"}),
        ("modify", "src/skills/memory.py", {"change"}),
        ("modify", "app/migrations/0001.sql", {"change"}),
        ("modify", "api/public.py", {"change"}),
        ("add", "src/new_module.py", {"change", "filesystem"}),
        ("delete", "assets/logo.png", {"change", "filesystem"}),
        ("rename", ".cursorrules", {"change", "filesystem", "policy", "ai"}),
        ("modify", "AGENTS.md", {"change", "policy", "ai"}),
        ("modify", ".windsurfrules", {"change", "policy", "ai"}),
        ("modify", ".github/FUNDING.yml", {"change"}),
        ("modify", ".github/workflows/ci.yml", {"change", "automation"}),
        ("modify", "FCVW/SECURITY.md", {"change", "security"}),
        ("modify", "FCVW/DATA.md", {"change", "data"}),
        ("modify", "FCVW/PROJECT.md", {"change"}),
        ("modify", "FCVW/AUTOMATION.md", {"change", "policy", "automation"}),
        ("modify", "FCVW/skills/QA/SKILL.md", {"change", "ai"}),
        ("modify", "FCVW/AI.md", {"change", "policy", "ai"}),
        ("modify", "FCVW/framework-releases/V0.20.0.md", {"change", "release"}),
        ("modify", TOOLS + "retrieve_context.py", {"change", "ai", "public_interface"}),
        ("modify", TOOLS + "validate_fcvw.py", {"change", "policy", "public_interface"}),
        ("modify", TOOLS + "fcvw_cache.py", {"change"}),
        ("unknown", "FCVW/wiki/note.md", {"change", "filesystem"}),
        ("unknown", "src/app.py", {"change"}),
    )

    def test_path_event_case_table(self):
        for operation, path, expected in self.PATH_EVENT_CASES:
            with self.subTest(path=path, operation=operation):
                self.assertEqual(expected, changed_file_events(path, operation, ROOT))

    def test_application_change_without_semantic_event_warns(self):
        silent = resolve_routes(ROOT, events=["change"], file_changes=["modify:src/auth_service.py"],
                                versioned_change=True)
        self.assertEqual(1, len(silent["warnings"]))
        self.assertIn("event:security", silent["warnings"][0])
        self.assertIn("src/auth_service.py", silent["warnings"][0])
        declared = resolve_routes(ROOT, events=["change", "security"],
                                  file_changes=["modify:src/auth_service.py"], versioned_change=True)
        self.assertEqual([], declared["warnings"])
        self.assertIn("FCVW/SECURITY.md", declared["mandatory_paths"])
        framework = resolve_routes(ROOT, events=["change"], file_changes=["modify:FCVW/PLANNING.md"],
                                   versioned_change=True)
        self.assertEqual([], framework["warnings"])

    def test_section_hints_accept_nested_paths(self):
        result = resolve_routes(ROOT, sessions=["wiki_maintenance"])
        self.assertIn("FCVW/wiki/README.md", result["section_hints"])

    def test_routes_only_cli_needs_no_index(self):
        script = str(Path(__file__).with_name("retrieve_context.py"))
        run = subprocess.run([sys.executable, "-B", script, "--root", str(ROOT), "--event", "security",
                              "--file-change", "modify:src/app.py", "--versioned-change"],
                             capture_output=True, text=True)
        self.assertEqual(0, run.returncode, run.stderr)
        result = json.loads(run.stdout)
        self.assertIn("FCVW/SECURITY.md", result["mandatory_paths"])
        self.assertEqual([], result["complementary_results"])
        half = subprocess.run([sys.executable, "-B", script, "--root", str(ROOT), "--query", "x"],
                              capture_output=True, text=True)
        self.assertNotEqual(0, half.returncode)

    def test_versioned_route_requires_declared_impact_and_changed_file(self):
        for kwargs in ({'file_changes': ['modify:FCVW/AI.md']},
                       {'events': ['ai']},
                       {'events': ['ai'], 'file_changes': ['rename:../outside.md']}):
            with self.assertRaises(ValueError):
                resolve_routes(ROOT, versioned_change=True, **kwargs)

    def test_policy_paths_are_read_from_source_not_copied_in_python(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); (root/"FCVW").mkdir()
            policy = root/"FCVW/CONTEXT_MAP.md"
            policy.write_text('| `event:security` | `OTHER.md` | evidence |\n', encoding="utf-8")
            self.assertEqual(resolve_routes(root, events=["security"])["mandatory_paths"], ["FCVW/OTHER.md"])

    def test_translated_labels_do_not_change_routes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); (root/"FCVW").mkdir()
            (root/"FCVW/CONTEXT_MAP.md").write_text(
                '| Seguridad (`security`) | señales | `SECURITY.md` | opcional | omitir |\n'
                '| `event:security` Authentifizierung | `DATA.md` | Nachweis |\n', encoding="utf-8")
            result = resolve_routes(root, sessions=["security"], events=["security"])
            self.assertEqual(result["mandatory_paths"], ["FCVW/SECURITY.md", "FCVW/DATA.md"])

    def test_duplicate_and_fenced_fake_routes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); (root/"FCVW").mkdir()
            p=root/"FCVW/CONTEXT_MAP.md"
            row='| `event:security` | `SECURITY.md` | evidence |\n'
            p.write_text('```\n'+row+'```\n'+row,encoding="utf-8")
            self.assertEqual(len(route_tables(root)[1]),1)
            p.write_text(row+row,encoding="utf-8")
            with self.assertRaises(ValueError):route_tables(root)


class ChunkSelectionTests(unittest.TestCase):
    def test_atomic_fence_and_paragraph_preserved(self):
        code='```python\n'+'print(1)\n'*30+'```'
        pieces=bounded_chunks('## Example\n\n'+code+'\n\nFinal paragraph.',limit=100)
        self.assertIn(code,pieces)
        self.assertEqual('\n\n'.join(pieces),'## Example\n\n'+code+'\n\nFinal paragraph.')

    def test_oversized_paragraph_not_silently_truncated(self):
        text='x'*5000
        self.assertEqual(bounded_chunks(text),[text])
        selected=select_chunks([chunk(text=text)],[],budget=100)
        self.assertEqual(selected['results'],[])
        self.assertEqual(selected['decisions'][0]['decision'],'budget')

    def test_budget_counts_serialized_metadata_and_whole_text(self):
        first=chunk(); exact=estimated_tokens([first])
        self.assertEqual(select_chunks([first],[],budget=exact)['results'],[first])
        self.assertEqual(select_chunks([first],[],budget=exact-1)['results'],[])
        self.assertEqual(select_chunks([first],[],budget=0)['estimated_optional_tokens'],0)

    def test_mandatory_duplicates_and_file_diversity(self):
        items=[chunk('required.md','required','required.md#a'),chunk(),
               chunk('b.md','Useful paragraph.','b.md#a'),chunk('a.md','Another','a.md#two'),
               chunk('a.md','Third','a.md#three'),chunk('c.md','Distinct','c.md#a')]
        before=copy.deepcopy(items)
        result=select_chunks(items,['required.md'],budget=1000,per_file=1)
        self.assertEqual([r['path'] for r in result['results']],['a.md','c.md'])
        self.assertEqual(items,before)

    def test_larger_pool_can_fill_budget_after_expensive_top_result(self):
        items=[chunk(text='x'*10000),chunk('b.md','Short useful chunk','b.md#b')]
        result=select_chunks(items,[],budget=100,top_k=1)
        self.assertEqual(result['results'][0]['path'],'b.md')

    def test_index_chunks_unique_and_derived_cache_excluded(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'FCVW').mkdir();(root/'.fcvw-cache').mkdir()
            (root/'FCVW/policy.md').write_text('## Topic\n\n'+('paragraph '*60+'\n\n')*4,encoding='utf-8')
            (root/'.fcvw-cache/secret.md').write_text('secret',encoding='utf-8')
            indexed=build_index(root)
            self.assertGreater(len(indexed),1)
            self.assertEqual(len({r['chunk_id'] for r in indexed}),len(indexed))
            self.assertFalse(any('.fcvw-cache' in r['path'] for r in indexed))
            result=bm25('paragraph',indexed,include_chunks=True,complete_chunks=True)
            self.assertTrue(all(r['excerpt_complete'] and r['chunk_id'] and r['chunk_hash'] for r in result))


class BenchmarkAndGraphTests(unittest.TestCase):
    def test_benchmark_has_independent_labels_and_unknown_real_outcomes(self):
        records,cases=synthetic_corpus()
        result=benchmark(ROOT,records,cases,repeats=1,today=date(2026,9,16))
        self.assertEqual(len(result['cases']),12)
        self.assertTrue(all(r['mandatory_recall']==1 and r['selected']['useful_recall']==1 for r in result['cases']))
        self.assertIsNone(result['outcomes']['mean_actual_input_tokens'])
        self.assertIsNone(result['outcomes']['validation_defect_rate'])

    def test_bad_labels_rejected_and_external_outcomes_counted(self):
        records,cases=synthetic_corpus()
        cases[0]['useful_chunks']=['missing#chunk']
        with self.assertRaises(ValueError):validate_cases(cases,records)
        records,cases=synthetic_corpus()
        cases[0]['outcome']={'corrected':True,'validation_passed':False,'actual_input_tokens':123}
        result=benchmark(ROOT,records,cases[:1],repeats=1)
        self.assertEqual(result['outcomes']['mean_actual_input_tokens'],123)
        self.assertEqual(result['outcomes']['correction_rate'],1)
        self.assertEqual(result['outcomes']['validation_defect_rate'],1)

    def test_shared_inventory_preserves_existing_graphs(self):
        files=markdown_files(ROOT)
        self.assertEqual(build_graph(ROOT),build_graph(ROOT,files=files))
        self.assertEqual(build_knowledge_graph(ROOT),build_knowledge_graph(ROOT,files=files))


class ArchiveBoundaryTests(unittest.TestCase):
    def test_zip_traversal_and_duplicate_checksum_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); archive=root/'FrameCode-VibeWork-V0.18.0-en-US.zip'; checks=root/'SHA256SUMS.txt'
            with zipfile.ZipFile(archive,'w') as z:z.writestr('../escape.txt','bad')
            line=hashlib.sha256(archive.read_bytes()).hexdigest()+'  '+archive.name+'\n'
            checks.write_text(line,encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'unsafe'):verify_archive(archive,checks,ROOT)
            checks.write_text(line+line,encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'duplicate'):verify_archive(archive,checks,ROOT)

    def test_installed_code_is_not_executed_without_source_parity(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source=root/'source';installed=root/'installed'
            (source/'tools').mkdir(parents=True);(installed/'FCVW/tools').mkdir(parents=True)
            (source/'tools/validate_fcvw.py').write_text('safe',encoding='utf-8')
            (installed/'FCVW/tools/validate_fcvw.py').write_text('untrusted',encoding='utf-8')
            with patch('verify_release_fcvw.validate_release_layout'),patch('verify_release_fcvw.subprocess.run') as execute:
                with self.assertRaisesRegex(ValueError,'differs'):validate_installed(installed,source,run_tests=True)
                execute.assert_not_called()
            (installed/'FCVW/tools/validate_fcvw.py').write_text('safe',encoding='utf-8')
            (installed/'FCVW/tools/validate_fcvw').mkdir()
            (installed/'FCVW/tools/validate_fcvw/__init__.py').write_text('untrusted',encoding='utf-8')
            with patch('verify_release_fcvw.validate_release_layout'),patch('verify_release_fcvw.subprocess.run') as execute:
                with self.assertRaisesRegex(ValueError,'inventory'):validate_installed(installed,source,run_tests=True)
                execute.assert_not_called()


if __name__=='__main__':
    unittest.main()
