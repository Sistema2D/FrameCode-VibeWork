#!/usr/bin/env python3
"""Aggregate explicit local loop evidence; never run models or promote strategies."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import os
import random
import statistics
import tempfile

from benchmark_retrieval_fcvw import score
from loop_contract_fcvw import event, protocol, read_events, read_json, require, stamp
from release_layout_fcvw import governed_root


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def percentile(values, fraction):
    ordered = sorted(values)
    if not ordered:
        return None
    index = (len(ordered) - 1) * fraction
    low = int(index)
    return ordered[low] + (ordered[min(low + 1, len(ordered) - 1)] - ordered[low]) * (index - low)


def distribution(values):
    known = [v for v in values if v is not None]
    return {'n': len(known), 'missing': len(values) - len(known),
            'mean': statistics.mean(known) if known else None,
            'median': percentile(known, .5), 'p75': percentile(known, .75) if len(known) >= 4 else None,
            'p95': percentile(known, .95) if len(known) >= 20 else None, 'max': max(known) if known else None}


def known_any(values):
    return True if True in values else None if not values or None in values else False


def context_metrics(contexts, task, proposed=False):
    scores, mandatory, useful_tokens, total_tokens = [], [], 0, 0
    complete = bool(contexts)
    sources = set()
    forbidden = set()
    for context in contexts:
        key = 'proposed_chunks' if proposed else 'chunks'
        if key not in context:
            complete = False
            continue
        chunks = context[key]
        result = score(chunks, task)
        scores.append(result)
        forbidden.update(result['forbidden_hits'])
        mandatory.append(len(set(task['mandatory_paths']) & set(context['mandatory_paths'])) / len(task['mandatory_paths']))
        sources.add(context['token_source'])
        for chunk in chunks:
            if chunk['tokens'] is None:
                complete = False
            else:
                total_tokens += chunk['tokens']
                if chunk['chunk_id'] in task['useful_chunks']:
                    useful_tokens += chunk['tokens']
    # Never mix heuristic and tokenizer counts into one apparently measured ratio.
    complete = complete and len(sources) == 1 and 'unavailable' not in sources
    precisions = [s['optional_precision'] for s in scores if s['optional_precision'] is not None]
    return {'deliveries': len(scores), 'mandatory_recall_min': min(mandatory) if mandatory and not proposed else None,
            'useful_recall': statistics.mean(s['useful_recall'] for s in scores) if scores else None,
            'optional_precision': statistics.mean(precisions) if precisions else None,
            'forbidden_hits': sorted(forbidden),
            'UCTR': useful_tokens / total_tokens if complete and total_tokens else None,
            'context_token_basis': next(iter(sources)) if complete else 'unavailable',
            'optional_tokens': total_tokens if complete else None}


def summarize_run(rows, followups, task, strategy, config):
    first, last = rows[0], rows[-1]
    complete = last['state'] == 'validated'
    calls = [c for row in rows for c in row['calls']]
    provider = [c for c in calls if c['token_source'] == 'provider']
    measured = all(r['usage_complete'] for r in rows) and all(c['token_source'] == 'provider'
               and c['input_tokens'] is not None and c['output_tokens'] is not None for c in calls)
    known_input = sum(c['input_tokens'] or 0 for c in provider)
    known_output = sum(c['output_tokens'] or 0 for c in provider)
    spent = known_input + known_output if measured else None
    currencies = {c['currency'] for c in calls if 'currency' in c}
    cost_complete = bool(calls) and all(r['usage_complete'] for r in rows) and all('cost' in c for c in calls) and len(currencies) == 1
    failed = [i for i, row in enumerate(rows) if row['validation'] == 'fail']
    rework = sum(c['input_tokens'] + c['output_tokens'] for row in rows[failed[0] + 1:] for c in row['calls']) if measured and failed else 0
    signed_failures = [r for r in rows if r['validation'] == 'fail' and r['failure_signature'] is not None]
    repeats = sum(b['validation'] == 'fail' and a['validation'] == 'fail' and b['failure_signature'] is not None
                  and b['failure_signature'] == a['failure_signature'] for a, b in zip(rows, rows[1:]))
    elapsed = (stamp(last['ended_at']) - stamp(first['started_at'])).total_seconds() * 1000
    followup_complete = bool(followups) and max(stamp(f['observed_until']) for f in followups) >= stamp(last['ended_at'])
    if followup_complete:
        followup_complete = (max(stamp(f['observed_until']) for f in followups) - stamp(last['ended_at'])).total_seconds() * 1000 >= config['followup_ms']
    contexts = [c for r in rows for c in r['contexts']]
    retrieval = context_metrics(contexts, task)
    proposal = context_metrics(contexts, task, True) if strategy['mode'] == 'shadow' else None
    violations = []
    if retrieval['mandatory_recall_min'] is not None and retrieval['mandatory_recall_min'] < 1:
        violations.append('mandatory_context_missing')
    if retrieval['forbidden_hits']:
        violations.append('forbidden_context_delivered')
    if proposal and proposal['forbidden_hits']:
        violations.append('forbidden_context_proposed')
    if len(rows) > config['limits']['max_iterations'] or elapsed > config['limits']['max_wall_ms'] or known_input + known_output > config['limits']['max_tokens']:
        violations.append('declared_limit_exceeded')
    correction = known_any([r['human_corrected'] for r in rows])
    defects = known_any([r['validation'] == 'fail' if r['validation'] != 'not_run' else None for r in rows])
    phases = {key: sum(r['durations_ms'][key] for r in rows)
              if all(r['durations_ms'].get(key) is not None for r in rows) else None
              for key in ('retrieval', 'model', 'tools', 'validation', 'human_wait')}
    gaps = []
    if not complete: gaps.append('not_validated_completion')
    if not measured: gaps.append('provider_usage_incomplete_or_estimated')
    if not contexts or not all(r['context_complete'] for r in rows): gaps.append('actual_context_incompletely_observed')
    if not followup_complete or any(f[k] is None for f in followups for k in ('defect', 'regression')):
        gaps.append('late_quality_window_incomplete')
    if correction is None: gaps.append('human_correction_unknown')
    if stamp(first['started_at']) < stamp(config['frozen_at']) or stamp(task['labeled_at']) > stamp(config['frozen_at']):
        gaps.append('protocol_or_labels_not_frozen_before_run')
    if task['label_basis'] != 'independent' or task['labeler'] == first['operator']:
        gaps.append('independent_review_not_established')
    if task['origin'] != 'real' or task['execution_kind'] != 'agent':
        gaps.append('not_real_agent_execution')
    if first['model'] is None or first['tokenizer'] is None:
        gaps.append('model_or_tokenizer_unidentified')
    return {'run_id': first['run_id'], 'task_id': task['id'], 'split': task['split'], 'strategy': strategy['id'],
            'delivered_strategy': strategy['delivered_strategy'], 'mode': strategy['mode'], 'repetition': first['repetition'],
            'state': last['state'], 'stop_reason': last['stop_reason'], 'iterations_observed': len(rows),
            'input_tokens': known_input if measured else None, 'output_tokens': known_output if measured else None,
            'known_provider_tokens_lower_bound': known_input + known_output, 'tokens_accumulated': spent,
            'monetary_cost': {'amount': sum(c['cost'] for c in calls), 'currency': next(iter(currencies))} if cost_complete else None,
            'TVC': spent if complete else None, 'IVC': len(rows) if complete else None,
            'RTR': rework / spent if complete and spent else 0.0 if complete and measured and not failed else None,
            'TTVS_ms': elapsed if complete else None, 'elapsed_ms': elapsed, 'phase_ms': phases,
            'FPV': complete and len(rows) == 1, 'RFR': repeats / len(signed_failures) if signed_failures else None,
            'failure_signatures_known': len(signed_failures), 'failed_checkpoints': len(failed),
            'human_corrected': correction, 'validation_defect': defects,
            'late_defect': known_any([f['defect'] for f in followups]), 'late_regression': known_any([f['regression'] for f in followups]),
            'followup_complete': followup_complete, 'retrieval': retrieval,
            'proposal': proposal,
            'invariant_violations': violations, 'evidence_gaps': gaps,
            'identity': {k: first[k] for k in ('source_revision', 'initial_state_ref', 'model', 'tokenizer')}}


def paired_comparisons(config, runs):
    lookup = {(r['task_id'], r['strategy'], r['repetition']): r for r in runs if r['split'] == 'evaluation'}
    comparisons = []
    for strategy in config['strategies']:
        if strategy['id'] == config['baseline']:
            continue
        pairs, incompatible = [], 0
        for key, candidate in lookup.items():
            if key[1] != strategy['id']:
                continue
            baseline = lookup.get((key[0], config['baseline'], key[2]))
            if baseline:
                if candidate['identity'] == baseline['identity']:
                    pairs.append((baseline, candidate))
                else:
                    incompatible += 1
        estimates = {}
        for metric in ('TVC', 'IVC', 'RTR', 'TTVS_ms', 'validation_defect', 'human_corrected'):
            by_task = {}
            for baseline, candidate in pairs:
                if baseline[metric] is not None and candidate[metric] is not None:
                    by_task.setdefault(candidate['task_id'], []).append(candidate[metric] - baseline[metric])
            # Collapse repetitions before resampling tasks; repeats are not independent tasks.
            deltas = [statistics.mean(v) for _, v in sorted(by_task.items())]
            ci = None
            if len(deltas) >= config['min_pairs']:
                rng = random.Random(0)
                samples = [statistics.mean(rng.choices(deltas, k=len(deltas))) for _ in range(1000)]
                ci = [percentile(samples, .025), percentile(samples, .975)]
            estimates[metric] = {'paired_tasks': len(deltas), 'candidate_minus_baseline_mean': statistics.mean(deltas) if deltas else None,
                                 'descriptive_task_bootstrap_95': ci}
        comparisons.append({'strategy': strategy['id'], 'mode': strategy['mode'], 'paired_runs': len(pairs),
                            'incompatible_pairs': incompatible, 'metrics': estimates,
                            'attribution': 'same_delivery_only_overhead_or_noise' if strategy['mode'] == 'shadow' else 'requires_controlled_execution_and_review'})
    return comparisons


def evaluate(config, records):
    protocol(config)
    protocol_digest = digest(config)
    tasks = {t['id']: t for t in config['tasks']}
    strategies = {s['id']: s for s in config['strategies']}
    events, duplicates = {}, 0
    for row in records:
        event(row)
        key = row['run_id'], row['event_id']
        if key in events:
            require(events[key] == row, 'conflicting duplicate event')
            duplicates += 1
        events[key] = row
    groups, followups, call_ids, delivery_ids = {}, {}, set(), set()
    for row in events.values():
        if row['kind'] == 'followup':
            followups.setdefault(row['run_id'], []).append(row)
            continue
        require(row['protocol_digest'] == protocol_digest, 'protocol digest mismatch')
        require(row['task_id'] in tasks and row['strategy'] in strategies, 'unknown task or strategy')
        require(row['source_revision'] == tasks[row['task_id']]['source_revision'], 'task source revision mismatch')
        require(row['repetition'] <= config['repetitions'], 'unplanned repetition')
        groups.setdefault(row['run_id'], []).append(row)
        for field, identity, seen in (('calls', 'call_id', call_ids), ('contexts', 'delivery_id', delivery_ids)):
            for item in row[field]:
                require(item[identity] not in seen, 'reused call or delivery identity across events')
                seen.add(item[identity])
    require(followups.keys() <= groups.keys(), 'followup without run')
    runs, cohort_ids = [], set()
    stable = ('task_id', 'strategy', 'repetition', 'source_revision', 'initial_state_ref', 'operator', 'model', 'tokenizer')
    for run_id, rows in sorted(groups.items()):
        rows.sort(key=lambda r: r['iteration'])
        first = rows[0]
        require([r['iteration'] for r in rows] == list(range(1, len(rows) + 1)), 'missing or duplicate iteration')
        require(all(all(r[k] == first[k] for k in stable) for r in rows), 'run identity changed during resume')
        for previous, current in zip(rows, rows[1:]):
            require(previous['state'] == 'running', 'execution after terminal run state')
            require(stamp(current['started_at']) >= stamp(previous['ended_at']), 'overlapping iteration checkpoints')
        cohort = first['task_id'], first['strategy'], first['repetition']
        require(cohort not in cohort_ids, 'duplicate planned execution under another run id')
        cohort_ids.add(cohort)
        for followup in followups.get(run_id, []):
            require(stamp(followup['observed_until']) >= stamp(rows[-1]['ended_at']), 'followup predates execution')
        runs.append(summarize_run(rows, followups.get(run_id, []), tasks[first['task_id']], strategies[first['strategy']], config))
    missing = [{'task_id': t, 'strategy': s, 'repetition': rep} for t in tasks for s in strategies
               for rep in range(1, config['repetitions'] + 1) if (t, s, rep) not in cohort_ids]
    summaries = []
    for split in ('adjustment', 'evaluation'):
        planned_tasks = sum(t['split'] == split for t in tasks.values())
        for strategy in strategies:
            cohort = [r for r in runs if r['split'] == split and r['strategy'] == strategy]
            planned = planned_tasks * config['repetitions']
            if not planned:
                continue
            summaries.append({'split': split, 'strategy': strategy, 'planned': planned, 'started': len(cohort),
                              'validated': sum(r['state'] == 'validated' for r in cohort),
                              'completion_rate_started': sum(r['state'] == 'validated' for r in cohort) / len(cohort) if cohort else None,
                              'FPVR': sum(r['FPV'] for r in cohort) / len(cohort) if cohort else None,
                              'metrics': {k: distribution([r[k] for r in cohort]) for k in ('TVC', 'IVC', 'RTR', 'TTVS_ms', 'RFR', 'human_corrected', 'validation_defect', 'late_defect', 'late_regression')},
                              'UCTR': distribution([r['retrieval']['UCTR'] if r['retrieval']['context_token_basis'] == 'tokenizer' else None for r in cohort]),
                              'UCTR_estimated': distribution([r['retrieval']['UCTR'] if r['retrieval']['context_token_basis'] == 'estimate' else None for r in cohort])})
    comparisons = paired_comparisons(config, runs)
    gaps = []
    if missing: gaps.append('planned_executions_missing')
    if config['registration'] != 'prospective': gaps.append('retrospective_protocol')
    evaluation_runs = [r for r in runs if r['split'] == 'evaluation']
    if not evaluation_runs: gaps.append('no_evaluation_runs')
    if any(r['evidence_gaps'] for r in evaluation_runs): gaps.append('run_evidence_incomplete')
    if any(c['incompatible_pairs'] or c['metrics'][config['primary_metric'] if config['primary_metric'] != 'TTVS' else 'TTVS_ms']['paired_tasks'] < config['min_pairs'] for c in comparisons):
        gaps.append('paired_evaluation_insufficient')
    if not any(s['mode'] == 'delivered' and s['id'] != config['baseline'] for s in config['strategies']):
        gaps.append('shadow_only_does_not_test_changed_delivery')
    violations = [{'run_id': r['run_id'], 'findings': r['invariant_violations']} for r in runs if r['invariant_violations']]
    return {'schema': 'fcvw/loop-report@1', 'protocol_id': config['id'], 'protocol_digest': protocol_digest,
            'events_digest': digest(sorted(events.values(), key=lambda r: (r['run_id'], r['event_id']))),
            'duplicate_events_ignored': duplicates, 'runs': runs, 'missing_runs': missing, 'cohorts': summaries,
            'comparisons': comparisons, 'predeclared_margins': config['margins'], 'evidence_gaps': gaps,
            'quality_assessment': 'independent_review_against_predeclared_margins_required',
            'invariant_violations': violations,
            'readiness': 'invariant_violation' if violations else 'inconclusive' if gaps else 'ready_for_independent_review',
            'dependent_experiments': {'issue_56': 'not_authorized_by_tool', 'issue_57': 'not_authorized_by_tool'},
            'notice': 'Caller-supplied evidence, not independent attestation. Bootstrap intervals are descriptive, not proof of non-inferiority. '
                      'Completion-only costs have survivor bias: inspect all missing/incomplete runs and quality windows. '
                      'No model executed, authority changed, reward learned or strategy promoted.'}


def markdown(report):
    def cell(value):
        return html.escape(str(value)).replace('|', '\\|').replace('\n', ' ')
    lines = ['# Loop evaluation', '', 'Readiness: ' + report['readiness'], '', report['notice'], '',
             '| Split | Strategy | Planned | Started | Validated | FPVR | TVC median | IVC median |', '|---|---|---|---|---|---|---|---|']
    for row in report['cohorts']:
        lines.append('| ' + ' | '.join(cell(v) for v in (row['split'], row['strategy'], row['planned'], row['started'], row['validated'], row['FPVR'], row['metrics']['TVC']['median'], row['metrics']['IVC']['median'])) + ' |')
    lines += ['', '## Evidence gaps', '', *['- ' + cell(g) for g in report['evidence_gaps']], '',
              'Invariant violations: ' + cell(report['invariant_violations']), '',
              'Missing planned runs: ' + str(len(report['missing_runs'])), '',
              'Complete provenance, denominators and comparisons are available with --format json.', '']
    return '\n'.join(lines)


def write_report(path, payload, root, inputs):
    target = path.resolve()
    root = root.resolve()
    require(not target.is_relative_to(root) or target.is_relative_to(root / '.fcvw-cache'), 'output inside framework must be in .fcvw-cache')
    require(target not in {p.resolve() for p in inputs}, 'output cannot overwrite an input')
    if target.exists():
        require(not any(target.samefile(p) for p in inputs), 'output aliases an input')
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=target.parent, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(payload)
    try:
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default=str(governed_root(Path(__file__))))
    parser.add_argument('--protocol', required=True)
    parser.add_argument('--runs', action='append', default=[], help='repeat JSONL files for resumed evidence')
    parser.add_argument('--show-protocol-digest', action='store_true', help='validate protocol and print its binding digest')
    parser.add_argument('--format', choices=('json', 'markdown'), default='json')
    parser.add_argument('--output')
    parser.add_argument('--check', action='store_true', help='nonzero if evidence is inconclusive or violates invariants')
    args = parser.parse_args()
    if args.show_protocol_digest and (args.runs or args.output or args.check):
        parser.error('digest-only mode cannot aggregate, check or write reports')
    if not args.show_protocol_digest and not args.runs:
        parser.error('--runs is required for aggregation')
    try:
        inputs = [Path(args.protocol), *map(Path, args.runs)]
        config = protocol(read_json(inputs[0]))
        if args.show_protocol_digest:
            print(digest(config))
            return 0
        report = evaluate(config, read_events(inputs[1:]))
        payload = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + '\n' if args.format == 'json' else markdown(report)
        if args.output:
            write_report(Path(args.output), payload, Path(args.root), inputs)
        else:
            print(payload, end='')
        return int(args.check and report['readiness'] != 'ready_for_independent_review')
    except (ValueError, OSError, RecursionError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    raise SystemExit(main())
