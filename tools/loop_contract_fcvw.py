"""Strict, inert input contracts for optional validated-completion evaluation."""
from __future__ import annotations

from datetime import datetime
import json
import math
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fields(value, required, optional=()):
    require(isinstance(value, dict), 'expected object')
    require(set(required) <= value.keys(), 'missing fields: ' + ', '.join(sorted(set(required) - value.keys())))
    require(value.keys() <= set(required) | set(optional), 'unknown fields are not accepted in loop inputs')


def label(value):
    require(isinstance(value, str) and bool(value.strip()) and len(value) <= 2048, 'expected bounded nonempty string')
    return value


def integer(value, minimum=0, maximum=10**15):
    require(type(value) is int and minimum <= value <= maximum, 'expected bounded nonnegative integer')
    return value


def number(value, minimum=0, maximum=1):
    require(type(value) in (int, float) and math.isfinite(value) and minimum <= value <= maximum, 'invalid numeric value')
    return value


def boolean(value, nullable=False):
    require(type(value) is bool or (nullable and value is None), 'expected boolean')


def stamp(value):
    result = datetime.fromisoformat(label(value).replace('Z', '+00:00'))
    require(result.tzinfo is not None, 'timestamp requires timezone')
    return result


def strings(value):
    require(isinstance(value, list), 'expected list')
    for item in value:
        label(item)
    require(len(value) == len(set(value)), 'duplicate list identity')


def object_list(value):
    require(isinstance(value, list) and all(isinstance(x, dict) for x in value), 'expected object list')


def keyed(value):
    object_list(value)
    result = {}
    for row in value:
        key = label(row.get('id'))
        require(key not in result, 'duplicate id')
        result[key] = row
    return result


def protocol(value):
    fields(value, ('schema', 'id', 'frozen_at', 'registration', 'baseline', 'repetitions', 'min_pairs',
                   'limits', 'margins', 'followup_ms', 'primary_metric', 'analysis_ref', 'strategies', 'tasks'))
    require(value['schema'] == 'fcvw/loop-protocol@1', 'unsupported loop protocol schema')
    label(value['id']); label(value['baseline']); stamp(value['frozen_at']); label(value['analysis_ref'])
    require(value['registration'] in ('prospective', 'retrospective'), 'invalid registration')
    require(value['primary_metric'] in ('TVC', 'IVC', 'RTR', 'TTVS'), 'invalid primary metric')
    integer(value['repetitions'], 1, 100); integer(value['min_pairs'], 2, 10000)
    integer(value['followup_ms'])
    fields(value['limits'], ('max_iterations', 'max_wall_ms', 'max_tokens'))
    for item in value['limits'].values():
        integer(item, 1)
    fields(value['margins'], ('validation_defect_rate', 'human_correction_rate', 'useful_recall'))
    for item in value['margins'].values():
        number(item)
    strategies = keyed(value['strategies'])
    require(value['baseline'] in strategies and len(strategies) >= 2, 'baseline and comparison strategy required')
    configs = set()
    for key, row in strategies.items():
        fields(row, ('id', 'mode', 'delivered_strategy', 'config_ref'))
        require(row['mode'] in ('delivered', 'shadow'), 'invalid strategy mode')
        label(row['config_ref'])
        require(row['config_ref'] not in configs, 'duplicate strategy configuration')
        configs.add(row['config_ref'])
        actual = label(row['delivered_strategy'])
        require(actual in strategies and strategies[actual]['mode'] == 'delivered', 'invalid actual delivery strategy')
        require((row['mode'] == 'delivered' and actual == key) or (row['mode'] == 'shadow' and actual != key), 'shadow must identify unchanged delivered strategy')
    require(strategies[value['baseline']]['mode'] == 'delivered', 'baseline cannot be shadow')
    tasks = keyed(value['tasks'])
    require(tasks, 'protocol requires tasks')
    require(len(tasks) * len(strategies) * value['repetitions'] <= 50000,
            'protocol exceeds 50000 planned executions')
    for task in tasks.values():
        fields(task, ('id', 'split', 'origin', 'execution_kind', 'domain', 'source_revision', 'acceptance_ref',
                      'labels_ref', 'labeler', 'label_basis', 'labeled_at', 'mandatory_paths', 'useful_chunks', 'forbidden_chunks'))
        require(task['split'] in ('adjustment', 'evaluation'), 'invalid task split')
        require(task['origin'] in ('real', 'synthetic'), 'invalid task origin')
        require(task['execution_kind'] in ('agent', 'deterministic_audit', 'retrieval_replay'), 'invalid execution kind')
        require(task['label_basis'] in ('independent', 'author', 'synthetic'), 'invalid label basis')
        for key in ('domain', 'source_revision', 'acceptance_ref', 'labels_ref', 'labeler'):
            label(task[key])
        stamp(task['labeled_at'])
        for key in ('mandatory_paths', 'useful_chunks', 'forbidden_chunks'):
            strings(task[key])
        require(task['mandatory_paths'], 'mandatory labels required')
        require(not set(task['useful_chunks']) & set(task['forbidden_chunks']), 'conflicting useful/forbidden labels')
    return value


ITERATION = ('schema', 'kind', 'event_id', 'run_id', 'protocol_digest', 'task_id', 'strategy', 'repetition', 'iteration',
             'source_revision', 'initial_state_ref', 'operator', 'model', 'tokenizer', 'measurement_note',
             'started_at', 'ended_at', 'validation', 'state', 'stop_reason', 'acceptance_satisfied', 'blockers', 'qa',
             'failure_signature', 'evidence_ref', 'usage_complete', 'context_complete', 'human_corrected', 'calls', 'contexts', 'durations_ms')
FOLLOWUP = ('schema', 'kind', 'event_id', 'run_id', 'observed_until', 'defect', 'regression', 'evidence_ref')


def event(row):
    require(isinstance(row, dict), 'event must be an object')
    fields(row, FOLLOWUP if row.get('kind') == 'followup' else ITERATION)
    require(row['schema'] == 'fcvw/loop-run@1', 'unsupported loop run schema')
    for key in ('event_id', 'run_id', 'evidence_ref'):
        label(row[key])
    if row['kind'] == 'followup':
        stamp(row['observed_until']); boolean(row['defect'], True); boolean(row['regression'], True)
        return row
    require(row['kind'] == 'iteration', 'invalid event kind')
    for key in ('protocol_digest', 'task_id', 'strategy', 'source_revision', 'initial_state_ref', 'operator', 'measurement_note'):
        label(row[key])
    for key in ('model', 'tokenizer', 'failure_signature'):
        if row[key] is not None:
            label(row[key])
    integer(row['repetition'], 1, 100); integer(row['iteration'], 1, 10000); integer(row['blockers'])
    require(stamp(row['ended_at']) >= stamp(row['started_at']), 'negative iteration duration')
    require(row['validation'] in ('pass', 'fail', 'not_run'), 'invalid validation result')
    require(row['state'] in ('running', 'validated', 'blocked', 'aborted', 'budget_exhausted'), 'invalid run state')
    if row['state'] == 'running':
        require(row['stop_reason'] is None, 'running iteration cannot have a stop reason')
    else:
        label(row['stop_reason'])
    boolean(row['acceptance_satisfied']); boolean(row['usage_complete']); boolean(row['context_complete']); boolean(row['human_corrected'], True)
    fields(row['qa'], ('divergences', 'asked', 'pending'))
    for count in row['qa'].values():
        integer(count)
    qa = row['qa']
    require(qa['asked'] <= qa['divergences'] and qa['divergences'] - qa['asked'] <= qa['pending'] <= qa['divergences'], 'invalid QA decision counts')
    if row['state'] == 'validated':
        require(row['validation'] == 'pass' and row['acceptance_satisfied'] and row['blockers'] == 0
                and qa['asked'] == qa['divergences'] and qa['pending'] == 0, 'false validated completion')
    require(row['validation'] == 'fail' or row['failure_signature'] is None, 'failure signature without failed checkpoint')
    object_list(row['calls'])
    call_ids = set()
    for call in row['calls']:
        fields(call, ('call_id', 'input_tokens', 'output_tokens', 'token_source', 'usage_ref'), ('cost', 'currency', 'cost_ref'))
        label(call['call_id']); label(call['usage_ref'])
        require(call['call_id'] not in call_ids, 'duplicate call id')
        call_ids.add(call['call_id'])
        require(call['token_source'] in ('provider', 'tokenizer', 'estimate', 'unavailable'), 'invalid token source')
        for key in ('input_tokens', 'output_tokens'):
            if call[key] is not None:
                integer(call[key])
        require(call['token_source'] != 'unavailable' or all(call[k] is None for k in ('input_tokens', 'output_tokens')), 'unavailable usage cannot contain tokens')
        if any(k in call for k in ('cost', 'currency', 'cost_ref')):
            require(all(k in call for k in ('cost', 'currency', 'cost_ref')), 'cost requires currency and billing evidence')
            number(call['cost'], 0, 10**12); label(call['cost_ref'])
            require(isinstance(call['currency'], str) and len(call['currency']) == 3 and call['currency'].isalpha() and call['currency'].isupper(), 'currency requires three uppercase letters')
    object_list(row['contexts'])
    require(not row['context_complete'] or len(row['contexts']) >= len(row['calls']), 'complete context needs a delivery observation per model call')
    delivery_ids = set()
    for context in row['contexts']:
        fields(context, ('delivery_id', 'mandatory_paths', 'chunks', 'token_source', 'evidence_ref'), ('proposed_chunks',))
        label(context['delivery_id']); label(context['evidence_ref']); strings(context['mandatory_paths'])
        require(context['delivery_id'] not in delivery_ids, 'duplicate context delivery id')
        delivery_ids.add(context['delivery_id'])
        require(context['token_source'] in ('tokenizer', 'estimate', 'unavailable'), 'invalid context token source')
        for key in ('chunks', 'proposed_chunks'):
            chunks = context.get(key, [])
            object_list(chunks)
            seen = set()
            for chunk in chunks:
                fields(chunk, ('chunk_id', 'tokens'))
                label(chunk['chunk_id'])
                require(chunk['chunk_id'] not in seen, 'duplicate chunk within a delivery')
                seen.add(chunk['chunk_id'])
                if chunk['tokens'] is not None:
                    integer(chunk['tokens'])
                require(context['token_source'] != 'unavailable' or chunk['tokens'] is None, 'unknown tokenizer cannot supply token counts')
    fields(row['durations_ms'], (), ('retrieval', 'model', 'tools', 'validation', 'human_wait'))
    wall = (stamp(row['ended_at']) - stamp(row['started_at'])).total_seconds() * 1000
    for duration in row['durations_ms'].values():
        if duration is not None:
            integer(duration)
            require(duration <= wall + 1, 'phase duration exceeds iteration wall time')
    return row


def strict_json(text):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON object key')
            result[key] = value
        return result
    def invalid(value):
        raise ValueError('non-finite JSON number: ' + value)
    return json.loads(text, object_pairs_hook=pairs, parse_constant=invalid)


def read_json(path: Path):
    require(path.stat().st_size <= 32 * 1024 * 1024, 'input exceeds 32 MiB')
    return strict_json(path.read_text(encoding='utf-8-sig'))


def read_events(paths):
    rows = []
    for path in paths:
        require(path.stat().st_size <= 32 * 1024 * 1024, 'input exceeds 32 MiB')
        with path.open(encoding='utf-8-sig') as stream:
            for line in stream:
                if line.strip():
                    require(len(line) <= 1024 * 1024, 'event exceeds 1 MiB')
                    rows.append(strict_json(line))
                    require(len(rows) <= 50000, 'too many events')
    return rows
