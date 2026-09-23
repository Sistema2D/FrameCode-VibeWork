"""Bounded human-reviewed optional feedback; no automatic reward or training."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path

from adaptive_control_fcvw import activation, assess, control, runtime, seal, verify_seal, validate_runtime
from adaptive_router_fcvw import shadow_route, structural_graph
from context_selection_fcvw import select_chunks
from loop_contract_fcvw import fields, require, label, stamp, read_json
from loop_metrics_fcvw import digest, write_report
from release_layout_fcvw import governed_root


def replay(config, feedback, assessment=None):
    control(config)
    require(isinstance(feedback, list) and len(feedback) <= 5000, 'feedback input must be bounded')
    if not feedback:
        return seal({'schema':'fcvw/adaptive-state@1', 'algorithm':'bounded-feedback-v1',
                     'control_digest':digest(config), 'feedback':[], 'weights':{}})
    assessment = assessment or activation(config)
    require(assessment['decision'] == 'eligible_for_review', 'feedback evidence rejected')
    tasks = {t['id']:t for t in config['protocol']['tasks']}
    runs = {r['run_id']:r for r in assessment['loop_report']['runs']}
    unique, outcomes = {}, {}
    for row in feedback:
        fields(row, ('schema', 'id', 'recorded_at', 'source', 'author', 'review_ref', 'authorization_ref',
                     'task_id', 'run_id', 'chunk_id', 'verdict', 'evidence_ref'))
        require(row['schema'] == 'fcvw/adaptive-feedback@1' and row['source'] == 'human', 'explicit human feedback required')
        for key in ('id', 'author', 'review_ref', 'authorization_ref', 'task_id', 'run_id', 'chunk_id', 'evidence_ref'):
            label(row[key])
        require(stamp(config['issued_at']) <= stamp(row['recorded_at']) < stamp(config['expires_at']), 'feedback outside authorized window')
        require(row['author'] in config['feedback_authorities'] and row['authorization_ref'] == config['authorization_ref'], 'feedback lacks authority')
        require(row['verdict'] in ('useful', 'harmful'), 'no implicit reward from clicks, silence or usage')
        task, run = tasks.get(row['task_id']), runs.get(row['run_id'])
        require(task is not None and task['split'] == 'adjustment', 'holdout or unknown task cannot train')
        require(run is not None and run['task_id'] == task['id'] and run['state'] == 'validated'
                and not run['evidence_gaps'] and not run['invariant_violations']
                and run['late_defect'] is False and run['late_regression'] is False, 'feedback requires complete validated outcome')
        chunk = config['eligible_chunks'].get(row['chunk_id'])
        require(chunk is not None and chunk['path'] not in task['mandatory_paths']
                and row['chunk_id'] not in task['forbidden_chunks'], 'feedback target is not optional eligible content')
        require((row['chunk_id'] in task['useful_chunks']) == (row['verdict'] == 'useful'), 'feedback contradicts frozen labels')
        delivered = {c['chunk_id'] for e in config['events'] if e.get('kind') == 'iteration' and e['run_id'] == row['run_id']
                     for context in e['contexts'] for c in context['chunks']}
        require(row['chunk_id'] in delivered, 'feedback target was not delivered')
        observed_until = max(stamp(e['ended_at'] if e['kind'] == 'iteration' else e['observed_until'])
                             for e in config['events'] if e['run_id'] == row['run_id'])
        require(stamp(row['recorded_at']) >= observed_until, 'feedback precedes validated follow-up')
        if row['id'] in unique:
            require(unique[row['id']] == row, 'conflicting feedback id')
            continue
        outcome = row['run_id'], row['chunk_id']
        require(outcome not in outcomes, 'same outcome cannot reward twice under different ids')
        outcomes[outcome] = row['id']; unique[row['id']] = deepcopy(row)
    require(len(unique) <= config['learning']['max_feedback'], 'feedback budget exceeded')
    ordered = sorted(unique.values(), key=lambda r:(stamp(r['recorded_at']), r['id']))
    weights = {}
    for row in ordered:
        weights = {key:round(value*config['learning']['decay'], 12) for key,value in weights.items()}
        key = row['chunk_id']
        value = weights.get(key, 0) + config['learning']['step'] * (1 if row['verdict'] == 'useful' else -1)
        weights[key] = round(max(-config['learning']['bound'], min(config['learning']['bound'], value)), 12)
    return seal({'schema':'fcvw/adaptive-state@1', 'algorithm':'bounded-feedback-v1',
                 'control_digest':digest(config), 'feedback':ordered, 'weights':weights})


def validate_state(value, config, assessment=None):
    verify_seal(value)
    fields(value, ('schema', 'algorithm', 'control_digest', 'feedback', 'weights', 'checksum'))
    require(value['schema'] == 'fcvw/adaptive-state@1' and value['control_digest'] == digest(config), 'state incompatible with control')
    assessment = assessment or assess(config['protocol'], config['events'], config['evaluation_strategy'])
    require(value == replay(config, value['feedback'], assessment), 'state does not match authorized deterministic replay')
    return value


def select(config, current, candidates, mandatory, *, root, source_digest, index_digest,
           mode='assist', state=None, top_k=8, per_file=2, now=None, budget=None):
    """Return a decision; callers retain the exact baseline on any failed gate."""
    decision = {'schema':'fcvw/adaptive-selection@1', 'status':'fallback', 'execution_blocked':False,
                'baseline_preserved':True, 'reason':None, 'results':None}
    try:
        control(config)
        validate_runtime(current, config)
        obs = current['observation']
        moment = now or datetime.now(timezone.utc)
        require(stamp(config['issued_at']) <= stamp(obs['observed_at']) <= moment, 'runtime timestamp outside control')
        require(obs['elapsed_ms'] + max(0, (moment-stamp(obs['observed_at'])).total_seconds()*1000) < config['limits']['max_wall_ms'], 'wall budget exhausted since observation')
        if current['blocked']:
            decision.update(reason=current['reason'], execution_blocked=True)
            return decision
        if mode == 'disabled':
            decision['reason'] = 'explicit_rollback'
            return decision
        assessment = activation(config, moment)
        require(config['source_digest'] == source_digest and config['index_digest'] == index_digest, 'source or index drift')
        require(set(config['mandatory_paths']) <= set(mandatory), 'mandatory route mismatch')
        decision.update(control_digest=digest(config), phase=config['phase'], runtime_checksum=current['checksum'])
    except (ValueError, TypeError, KeyError, RecursionError) as error:
        decision.update(reason=str(error), execution_blocked=True)
        return decision
    try:
        require(len(candidates) <= 20, 'candidate limit exceeded')
        weights = validate_state(state, config, assessment)['weights'] if state is not None else {}
        allowed = []
        for row in candidates:
            entry = config['eligible_chunks'].get(row['chunk_id'])
            if row['path'] in mandatory or entry is None:
                continue
            require(entry == {'path':row['path'], 'chunk_hash':row['chunk_hash']}, 'candidate content drift')
            require(row.get('excerpt_complete') is True, 'assistance needs complete chunks')
            allowed.append(row)
        proposal = shadow_route(structural_graph(root), allowed, mandatory, budget=config['limits']['optional_tokens'])
        scores = {r['path']:r['score'] for r in proposal['candidates']}
        ranked = sorted(allowed, key=lambda r:(-(scores.get(r['path'], 0)+weights.get(r['chunk_id'], 0)), r['chunk_id']))
        ranked = [r for r in ranked if scores.get(r['path'],0)+weights.get(r['chunk_id'],0) > 0]
        limit = config['limits']['optional_tokens'] if budget is None else min(budget, config['limits']['optional_tokens'])
        selection = select_chunks(ranked, mandatory, budget=limit, top_k=top_k, per_file=per_file)
        decision.update(selection=selection, state_checksum=state['checksum'] if state is not None else None)
        if mode == 'shadow' or config['phase'] == 'shadow':
            decision.update(status='shadow', reason='proposal_only')
        else:
            decision.update(status='active', reason='scoped_reviewed_selection', baseline_preserved=False, results=selection['results'])
    except (ValueError, OSError, TypeError, KeyError, RecursionError) as error:
        decision['reason'] = str(error)
    return decision


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('assess', 'replay', 'reset', 'export', 'rollback', 'start', 'observe'))
    parser.add_argument('--root', default=str(governed_root(Path(__file__))))
    parser.add_argument('--control', required=True)
    parser.add_argument('--feedback')
    parser.add_argument('--state', help='state to export, or known state to restore by validated replay')
    parser.add_argument('--observation')
    parser.add_argument('--runtime', help='prior stop latch; observe appends without clearing it')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    inputs = [Path(p) for p in (args.control, args.feedback, args.state, args.observation, args.runtime) if p]
    try:
        cfg = control(read_json(Path(args.control)))
        if args.command == 'assess':
            result = assess(cfg['protocol'], cfg['events'], cfg['evaluation_strategy'])
        elif args.command in ('start', 'observe'):
            require(args.observation is not None, '--observation required')
            require(args.runtime is not None if args.command == 'observe' else args.runtime is None,
                    'observe requires previous --runtime; start explicitly creates a new run')
            result = runtime(cfg, read_json(Path(args.observation)), read_json(Path(args.runtime)) if args.runtime else None)
        elif args.command in ('export', 'rollback'):
            require(args.state is not None, '--state required')
            result = validate_state(read_json(Path(args.state)), cfg)
        else:
            require(args.command == 'reset' or args.feedback is not None, '--feedback required')
            result = replay(cfg, [] if args.command == 'reset' else read_json(Path(args.feedback)))
        write_report(Path(args.output), json.dumps(result, ensure_ascii=False, indent=2)+'\n', Path(args.root), inputs)
        return int(result.get('decision', 'eligible_for_review') != 'eligible_for_review' or result.get('blocked', False))
    except (ValueError, OSError, TypeError, KeyError, RecursionError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    raise SystemExit(main())
