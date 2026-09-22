#!/usr/bin/env python3
"""Validate explicitly selected product-wiki contracts and QA coverage; never browse."""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re

from document_graph_fcvw import _outside_fences
from frontmatter_fcvw import parse_frontmatter, scalar

EMPTY = {'', '-', 'unknown', 'unconfirmed', 'pending', 'none', 'n/a'}
KINDS = {'screen', 'modal', 'component', 'flow', 'cli', 'api', 'service', 'library', 'device', 'firmware', 'protocol'}
ID = re.compile(r'[A-Za-z][A-Za-z0-9_-]*\Z')


def meaningful(value: str) -> bool:
    value = value.strip()
    return value.lower() not in EMPTY and not re.fullmatch(r'<[^<>]+>', value)


def read_page(root: Path, relative: str) -> tuple[dict, str]:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or path.suffix.lower() != '.md':
        raise ValueError('page must be Markdown inside the selected root')
    if path.stat().st_size > 1024 * 1024:
        raise ValueError('selected page exceeds 1 MiB; split the surface')
    text = path.read_text(encoding='utf-8-sig')
    parsed = parse_frontmatter(text)
    if parsed.issues:
        raise ValueError(f'invalid frontmatter: {relative}')
    return parsed.data, text


def table(text: str, section: str, columns: tuple[str, ...]) -> list[dict[str, str]]:
    active, header, separator, found = False, False, False, False
    rows = []
    for line in _outside_fences(text):
        if line.startswith('## '):
            active = line == '## ' + section
            if active:
                if found:
                    raise ValueError(f'duplicate section: {section}')
                found = True
            continue
        if not active or not line.strip().startswith('|'):
            continue
        cells = [v.strip().replace(r'\|', '|') for v in re.split(r'(?<!\\)\|', line.strip().strip('|'))]
        if not header:
            if tuple(cells) != columns:
                raise ValueError(f'{section} requires columns: {", ".join(columns)}')
            header = True
        elif not separator:
            if len(cells) != len(columns) or not all(re.fullmatch(r':?-{3,}:?', c) for c in cells):
                raise ValueError(f'invalid {section} separator')
            separator = True
        else:
            if len(cells) != len(columns):
                raise ValueError(f'wrong number of {section} cells; escape literal pipes')
            rows.append(dict(zip(columns, cells)))
    if not found or not header or not separator:
        raise ValueError(f'missing {section} table')
    return rows


def unique(rows: list[dict], key: str) -> dict[str, dict]:
    result = {}
    for row in rows:
        identity = row[key]
        if not ID.fullmatch(identity) or identity in result:
            raise ValueError(f'invalid or duplicate {key}: {identity}')
        result[identity] = row
    return result


def surface(root: Path, path: str) -> dict:
    meta, text = read_page(root, path)
    identity = scalar(meta, 'id')
    if (meta.get('schema') != 'fcvw/wiki@1' or meta.get('type') != 'component'
            or meta.get('qa_surface') not in KINDS or not ID.fullmatch(identity)
            or not meaningful(scalar(meta, 'route'))):
        raise ValueError(f'invalid product surface metadata: {path}')
    elements = unique(table(text, 'Elements', ('element_id', 'kind', 'locator', 'purpose')), 'element_id')
    cases = unique(table(text, 'Cases', ('case_id', 'element_ids', 'preconditions', 'action', 'expectation', 'expected', 'source')), 'case_id')
    if not elements or not cases:
        raise ValueError(f'surface needs elements and cases: {path}')
    if any(not all(meaningful(v) for v in row.values()) for row in elements.values()):
        raise ValueError('elements require kind, locator and purpose')
    covered = set()
    for case in cases.values():
        ids = [v.strip() for v in case['element_ids'].split(',')]
        if len(set(ids)) != len(ids) or not set(ids) <= elements.keys():
            raise ValueError('case references missing or duplicate elements')
        covered.update(ids)
        if case['expectation'] not in {'approved', 'provisional', 'unknown'} or not meaningful(case['action']):
            raise ValueError('case needs action and expectation classification')
        if case['expectation'] == 'approved' and not all(meaningful(case[k]) for k in ('expected', 'source')):
            raise ValueError('approved expectation needs expected behavior and source')
    if covered != elements.keys():
        raise ValueError('every declared element needs at least one case, including unknown expectations')
    contract = {'id': identity, 'kind': meta['qa_surface'], 'route': meta['route'], 'elements': elements, 'cases': cases}
    return {**contract, 'path': path, 'sha256': hashlib.sha256(json.dumps(contract, sort_keys=True).encode()).hexdigest()}


def divergence_decisions(text: str, results: dict, expected: dict) -> dict:
    """Account for declared mismatches; evidence references cannot attest user consent."""
    decisions = {}
    if any(line == '## Divergences' for line in _outside_fences(text)):
        for row in table(text, 'Divergences', ('surface_id', 'case_id', 'question', 'question_ref', 'decision', 'decision_ref')):
            key = row['surface_id'], row['case_id']
            if key not in results or key in decisions or results[key]['result'] == 'pass':
                raise ValueError('divergence must reference a unique non-passing result')
            if row['decision'] not in {'pending', 'fix_implementation', 'update_expectation', 'investigate', 'defer'}:
                raise ValueError('invalid user divergence decision')
            asked = meaningful(row['question']) and meaningful(row['question_ref'])
            if row['decision'] != 'pending' and (not asked or not meaningful(row['decision_ref'])):
                raise ValueError('user decision requires a recorded question and explicit user response reference')
            decisions[key] = row
    # A failed case cannot bypass consultation by omitting the divergence table/row.
    keys = {key for key, row in results.items() if row['result'] == 'fail'} | decisions.keys()
    asked_count = decided_count = 0
    pending = []
    for key in sorted(keys):
        row = decisions.get(key, {})
        asked = meaningful(row.get('question', '')) and meaningful(row.get('question_ref', ''))
        decided = row.get('decision', 'pending') != 'pending'
        asked_count += asked
        decided_count += decided
        if not decided:
            pending.append({'surface_id': key[0], 'case_id': key[1],
                            'expected': expected[key]['expected'], 'source': expected[key]['source'],
                            'observed': results[key]['observed'], 'evidence': results[key]['evidence'],
                            'question_recorded': asked})
    total = len(keys)
    return {'user_decision_gate': 'blocked' if pending else 'clear',
            'divergence_metrics': {'total': total, 'asked': asked_count, 'unasked': total - asked_count,
                                   'consultation_coverage_pct': round(100 * asked_count / total, 2) if total else None,
                                   'decided': decided_count, 'pending_decisions': total - decided_count},
            'pending_divergences': pending}


def evaluate(root: Path, paths: list[str], *, inventory: str | None = None, run: str | None = None) -> dict:
    paths = list(dict.fromkeys(paths))
    inventory_status = None
    mapped = {}
    inventory_revision = None
    if inventory:
        meta, text = read_page(root, inventory)
        inventory_status = scalar(meta, 'inventory_status')
        inventory_revision = scalar(meta, 'app_revision')
        if inventory_status not in {'in_progress', 'complete'} or not all(meaningful(scalar(meta, k)) for k in ('scope', 'app_revision', 'roles')):
            raise ValueError('inventory needs status, scope, app_revision and roles')
        entries = unique(table(text, 'Surfaces', ('surface_id', 'page', 'kind', 'route', 'discovery')), 'surface_id')
        frontier = table(text, 'Frontier', ('target', 'reason', 'status'))
        if not entries or any(r['discovery'] not in {'mapped', 'blocked', 'not_visited'}
                              or r['kind'] not in KINDS or not meaningful(r['route']) for r in entries.values()):
            raise ValueError('inventory requires valid discovery entries')
        if any(r['status'] not in {'open', 'blocked', 'resolved'} or not meaningful(r['reason']) for r in frontier):
            raise ValueError('invalid frontier status or reason')
        if inventory_status == 'complete' and (any(r['discovery'] != 'mapped' for r in entries.values()) or any(r['status'] != 'resolved' for r in frontier)):
            raise ValueError('complete inventory cannot hide unresolved discovery')
        for key, entry in entries.items():
            if entry['discovery'] == 'mapped':
                mapped[key] = entry
                if entry['page'] not in paths:
                    paths.append(entry['page'])
    surfaces = {}
    for path in paths:
        page = surface(root, path)
        if page['id'] in surfaces:
            raise ValueError('duplicate surface id across selected pages')
        surfaces[page['id']] = page
    for key, entry in mapped.items():
        if key not in surfaces or any(surfaces[key][k] != entry[k] for k in ('kind', 'route')) or surfaces[key]['path'] != entry['page']:
            raise ValueError('inventory identity, kind, route or page differs from surface')
    if not surfaces:
        raise ValueError('select at least one mapped surface')
    expected = {(p['id'], cid): case for p in surfaces.values() for cid, case in p['cases'].items()}
    results = {}
    decision_report = {'user_decision_gate': 'not_evaluated', 'divergence_metrics': None, 'pending_divergences': []}
    if run:
        meta, text = read_page(root, run)
        if meta.get('schema') != 'fcvw/wiki@1' or meta.get('type') != 'audit' or scalar(meta, 'qa_run') != 'true':
            raise ValueError('run must be a QA wiki audit')
        if not all(meaningful(scalar(meta, k)) for k in ('app_revision', 'environment', 'runtime', 'roles')):
            raise ValueError('run requires revision, environment, runtime and roles')
        if datetime.fromisoformat(scalar(meta, 'observed_at').replace('Z', '+00:00')).tzinfo is None:
            raise ValueError('observed_at requires timezone')
        if inventory_revision and scalar(meta, 'app_revision') != inventory_revision:
            raise ValueError('run and inventory must identify the same application revision')
        contracts = unique(table(text, 'Contracts', ('surface_id', 'sha256')), 'surface_id')
        if contracts.keys() != surfaces.keys() or any(contracts[k]['sha256'] != p['sha256'] for k, p in surfaces.items()):
            raise ValueError('run does not match current selected behavior contracts; review and rerun affected cases')
        for row in table(text, 'Results', ('surface_id', 'case_id', 'result', 'observed', 'evidence')):
            key = row['surface_id'], row['case_id']
            if key not in expected or key in results or row['result'] not in {'pass', 'fail', 'blocked', 'not_run'}:
                raise ValueError('unknown, duplicate or invalid case result')
            if not meaningful(row['observed']):
                raise ValueError('result requires observation or blocking reason')
            if row['result'] in {'pass', 'fail'} and not meaningful(row['evidence']):
                raise ValueError('executed result requires evidence reference')
            if row['result'] == 'pass' and expected[key]['expectation'] != 'approved':
                raise ValueError('unknown/provisional expectation cannot pass')
            results[key] = row
        decision_report = divergence_decisions(text, results, expected)
    missing = sorted(set(expected) - set(results))
    counts = {s: sum(r['result'] == s for r in results.values()) for s in ('pass', 'fail', 'blocked', 'not_run')}
    status = 'not_run' if not run else 'fail' if counts['fail'] else 'incomplete' if missing or counts['blocked'] or counts['not_run'] else 'pass'
    return {'schema': 'fcvw/product-qa-check@1', 'structural_status': 'pass', 'execution_status': status,
            **decision_report,
            'inventory_status': inventory_status, 'surfaces': len(surfaces), 'elements': sum(len(p['elements']) for p in surfaces.values()),
            'declared_cases': len(expected), 'results': counts, 'missing_cases': [list(k) for k in missing],
            'contract_hashes': {k: p['sha256'] for k, p in surfaces.items()},
            'notice': 'Checks declared scope and evidence fields only; does not prove live execution, evidence truth, actual user consultation/consent, hidden surface completeness or requirement approval.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default='.')
    parser.add_argument('--surface', action='append', default=[])
    parser.add_argument('--inventory')
    parser.add_argument('--run')
    parser.add_argument('--output')
    args = parser.parse_args()
    try:
        report = evaluate(Path(args.root).resolve(), args.surface, inventory=args.inventory, run=args.run)
        data = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
        if args.output:
            Path(args.output).write_text(data, encoding='utf-8')
        print(data, end='')
        return int(bool(args.run) and (report['execution_status'] != 'pass' or report['user_decision_gate'] == 'blocked'))
    except (ValueError, OSError) as exc:
        parser.exit(1, f'QA wiki check failed: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
