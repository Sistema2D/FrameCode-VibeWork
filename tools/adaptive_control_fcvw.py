"""Explicit adaptive experiment gates; declarations are not authentication."""
from datetime import datetime, timezone
from copy import deepcopy
import random
import statistics

from adaptive_router_fcvw import safe_path
from loop_contract_fcvw import fields, require, label, strings, integer, number, boolean, stamp, protocol
from loop_metrics_fcvw import digest, evaluate, percentile


def interval(values, minimum):
    if len(values) < minimum:
        return None
    rng = random.Random(0)
    samples = [statistics.mean(rng.choices(values, k=len(values))) for _ in range(1000)]
    return [percentile(samples, .025), percentile(samples, .975)]


def assess(config, events, strategy):
    """Recompute evidence, then conservatively screen quality, never grant authority."""
    report = evaluate(config, events)
    candidate = next((s for s in config['strategies'] if s['id'] == strategy), None)
    require(candidate is not None and strategy != config['baseline'], 'unknown comparison strategy')
    reasons, comparisons = [], {}
    if report['invariant_violations']:
        reasons.append('invariant_violation')
    if report['readiness'] != 'ready_for_independent_review':
        reasons.append('evidence_incomplete')
    if candidate['mode'] != 'delivered':
        reasons.append('shadow_is_not_active_evidence')
    runs = {(r['task_id'], r['strategy'], r['repetition']): r for r in report['runs'] if r['split'] == 'evaluation'}
    metrics = {'validation_defect': config['margins']['validation_defect_rate'],
               'human_corrected': config['margins']['human_correction_rate'],
               'late_defect': config['margins']['validation_defect_rate'],
               'late_regression': config['margins']['validation_defect_rate'],
               'useful_recall': config['margins']['useful_recall']}
    for metric, margin in metrics.items():
        by_task = {}
        for (task, arm, rep), current in runs.items():
            baseline = runs.get((task, config['baseline'], rep))
            if arm != strategy or not baseline or baseline['identity'] != current['identity']:
                continue
            a, b = (r['retrieval']['useful_recall'] if metric == 'useful_recall' else r[metric] for r in (baseline, current))
            if a is not None and b is not None:
                by_task.setdefault(task, []).append(b-a)
        deltas = [statistics.mean(v) for _, v in sorted(by_task.items())]
        ci = interval(deltas, config['min_pairs'])
        comparisons[metric] = {'paired_tasks': len(deltas), 'delta_interval_95': ci, 'margin': margin}
        if ci is None:
            reasons.append(metric + '_insufficient')
        elif (ci[0] < -margin if metric == 'useful_recall' else ci[1] > margin):
            reasons.append(metric + '_noninferiority_not_established')
    return {'schema': 'fcvw/adaptive-assessment@1', 'protocol_digest': digest(config),
            'events_digest': report['events_digest'], 'strategy': strategy, 'quality': comparisons,
            'decision': 'reject' if 'invariant_violation' in reasons else 'inconclusive' if reasons else 'eligible_for_review',
            'reasons': reasons, 'loop_report': report,
            'notice': 'Conservative descriptive screen, not statistical proof, authentication or promotion. Review power and rare events independently.'}


def control(value):
    fields(value, ('schema', 'id', 'enabled', 'phase', 'issued_at', 'expires_at', 'authorized_by', 'authorization_ref',
                   'review_decision', 'review_ref', 'source_digest', 'index_digest', 'scope', 'mandatory_paths',
                   'eligible_chunks', 'limits', 'learning', 'feedback_authorities', 'rollback',
                   'protocol', 'events', 'evaluation_strategy'))
    require(value['schema'] == 'fcvw/adaptive-control@1', 'unsupported adaptive control')
    for key in ('id', 'authorized_by', 'authorization_ref', 'review_ref', 'source_digest', 'index_digest', 'evaluation_strategy'):
        label(value[key])
    boolean(value['enabled'])
    require(value['phase'] in ('shadow', 'limited', 'operational'), 'invalid phase')
    require(value['review_decision'] in ('reject', 'approve_limited', 'approve_operational'), 'invalid review decision')
    require(stamp(value['expires_at']) > stamp(value['issued_at']), 'invalid control window')
    for key in ('scope', 'mandatory_paths', 'feedback_authorities'):
        strings(value[key]); require(value[key], 'empty '+key)
    require(all(safe_path(p) for p in value['mandatory_paths']), 'unsafe mandatory path')
    chunks = value['eligible_chunks']
    require(isinstance(chunks, dict) and 0 < len(chunks) <= 5000, 'bounded eligible chunk map required')
    for key, chunk in chunks.items():
        label(key); fields(chunk, ('path', 'chunk_hash'))
        require(safe_path(chunk['path']) and chunk['path'] not in value['mandatory_paths'], 'learned mandatory or unsafe path')
        label(chunk['chunk_hash'])
    fields(value['limits'], ('optional_tokens', 'max_iterations', 'max_wall_ms', 'max_tokens', 'repeat_failure_limit'))
    integer(value['limits']['optional_tokens'], 0, 100000)
    for key in ('max_iterations', 'max_wall_ms', 'max_tokens', 'repeat_failure_limit'):
        integer(value['limits'][key], 1)
    fields(value['learning'], ('step', 'bound', 'decay', 'max_feedback'))
    number(value['learning']['step'], 0, .1); number(value['learning']['bound'], 0, .25)
    number(value['learning']['decay']); integer(value['learning']['max_feedback'], 1, 1000)
    fields(value['rollback'], ('window', 'tvc_ratio', 'rtr_delta', 'rfr_delta', 'defect_delta'))
    integer(value['rollback']['window'], 1, 100)
    number(value['rollback']['tvc_ratio'], 1, 100)
    for key in ('rtr_delta', 'rfr_delta', 'defect_delta'):
        number(value['rollback'][key])
    protocol(value['protocol'])
    require(all(t['source_revision'] in (value['source_digest'], 'sha256:'+value['source_digest'])
                for t in value['protocol']['tasks']), 'evidence source differs from authorized source')
    require(isinstance(value['events'], list) and len(value['events']) <= 10000, 'bounded evidence events required')
    return value


def activation(value, now=None):
    control(value)
    current = now or datetime.now(timezone.utc)
    require(stamp(value['issued_at']) <= current < stamp(value['expires_at']), 'control expired or not yet active')
    require(value['enabled'], 'control disabled')
    expected = 'approve_operational' if value['phase'] == 'operational' else 'approve_limited'
    require(value['review_decision'] == expected, 'phase lacks explicit matching review')
    result = assess(value['protocol'], value['events'], value['evaluation_strategy'])
    require(result['decision'] == 'eligible_for_review', 'evidence does not support activation: '+result['decision'])
    return result


def seal(value):
    return {**value, 'checksum': digest(value)}


def verify_seal(value):
    require(isinstance(value, dict) and value.get('checksum') == digest({k:v for k,v in value.items() if k != 'checksum'}), 'state checksum mismatch')


def observation(value):
    fields(value, ('run_id', 'task_id', 'observed_at', 'iterations', 'elapsed_ms', 'tokens', 'token_source', 'usage_complete',
                   'qa_pending', 'safety_block', 'checkpoints', 'quality_windows'))
    label(value['run_id']); label(value['task_id']); stamp(value['observed_at'])
    for key in ('iterations', 'elapsed_ms', 'qa_pending'):
        integer(value[key])
    if value['tokens'] is not None:
        integer(value['tokens'])
    require(value['token_source'] in ('provider', 'tokenizer', 'estimate', 'unavailable'), 'invalid runtime token source')
    require(value['token_source'] != 'unavailable' or value['tokens'] is None, 'unavailable runtime usage cannot contain tokens')
    boolean(value['usage_complete'])
    boolean(value['safety_block'])
    require(isinstance(value['checkpoints'], list) and len(value['checkpoints']) == value['iterations'] <= 10000, 'checkpoint inventory mismatch')
    for checkpoint in value['checkpoints']:
        fields(checkpoint, ('validation', 'signature'))
        require(checkpoint['validation'] in ('pass', 'fail', 'not_run'), 'invalid checkpoint')
        if checkpoint['signature'] is not None:
            label(checkpoint['signature'])
        require(checkpoint['validation'] == 'fail' or checkpoint['signature'] is None, 'signature without failure')
    require(isinstance(value['quality_windows'], list) and len(value['quality_windows']) <= 1000, 'invalid quality windows')
    for point in value['quality_windows']:
        fields(point, ('tvc_ratio', 'rtr_delta', 'rfr_delta', 'defect_delta'))
        for key, metric in point.items():
            if metric is not None:
                number(metric, 0 if key == 'tvc_ratio' else -1, 100 if key == 'tvc_ratio' else 1)


def stop_reason(config, obs):
    observation(obs)
    require(obs['task_id'] in config['scope'], 'task outside authorized scope')
    if obs['safety_block']: return 'safety_block'
    if obs['qa_pending']: return 'qa_user_decision_required'
    if obs['tokens'] is None or obs['token_source'] != 'provider' or not obs['usage_complete']:
        return 'usage_unknown_or_estimated'
    for key, actual in (('max_iterations', obs['iterations']), ('max_wall_ms', obs['elapsed_ms']), ('max_tokens', obs['tokens'])):
        if actual >= config['limits'][key]: return key
    previous, count = None, 0
    for point in obs['checkpoints']:
        if point['validation'] == 'pass':
            previous, count = None, 0
        elif point['validation'] == 'fail':
            if point['signature'] is None: return 'failure_signature_unknown'
            count = count + 1 if previous == point['signature'] else 1
            previous = point['signature']
            if count >= config['limits']['repeat_failure_limit']: return 'stagnation_review_required'
    window = config['rollback']['window']
    points = obs['quality_windows'][-window:]
    if len(points) == window and all(any(p[k] is not None and p[k] > config['rollback'][k] for k in p) for p in points):
        return 'persistent_quality_degradation'
    return None


def runtime(config, obs, previous=None):
    control(config); observation(obs)
    reason = stop_reason(config, obs)
    if previous is not None:
        validate_runtime(previous, config)
        old = previous['observation']
        require(obs['run_id'] == old['run_id'] and obs['task_id'] == old['task_id'], 'runtime identity changed')
        require(stamp(obs['observed_at']) >= stamp(old['observed_at']), 'observation moved backwards')
        require(all(obs[k] >= old[k] for k in ('iterations', 'elapsed_ms')), 'counters moved backwards')
        require(old['tokens'] is None or obs['tokens'] is not None and obs['tokens'] >= old['tokens'], 'token counter moved backwards')
        require(obs['checkpoints'][:len(old['checkpoints'])] == old['checkpoints'], 'checkpoint history rewritten')
        require(obs['quality_windows'][:len(old['quality_windows'])] == old['quality_windows'], 'quality history rewritten')
        reason = previous['reason'] if previous['blocked'] else reason
    return seal({'schema':'fcvw/adaptive-runtime@1', 'control_digest':digest(config),
                 'sequence':previous['sequence']+1 if previous else 0, 'observation':deepcopy(obs),
                 'blocked':reason is not None, 'reason':reason})


def validate_runtime(value, config):
    verify_seal(value)
    fields(value, ('schema', 'control_digest', 'sequence', 'observation', 'blocked', 'reason', 'checksum'))
    require(value['schema'] == 'fcvw/adaptive-runtime@1' and value['control_digest'] == digest(config), 'runtime control mismatch')
    integer(value['sequence']); boolean(value['blocked']); observation(value['observation'])
    require(value['blocked'] == (value['reason'] is not None), 'invalid stop latch')
    if value['reason'] is not None: label(value['reason'])
    require(value['blocked'] or stop_reason(config, value['observation']) is None, 'suppressed stop condition')
    return value
