"""Trusted local run identity and monotonic runtime state for opt-in assist."""

from __future__ import annotations

import json
import os
from pathlib import Path
import sqlite3
from typing import Callable

from adaptive_control_fcvw import validate_runtime
from loop_contract_fcvw import require


def ledger_path(path: Path, root: Path) -> Path:
    target, source = path.resolve(), root.resolve()
    requested = Path(os.path.abspath(path))
    require(not requested.is_relative_to(source) or requested.is_relative_to(source / '.fcvw-cache'),
            'runtime ledger inside framework must be in .fcvw-cache')
    require(not target.is_relative_to(source) or target.is_relative_to(source / '.fcvw-cache'),
            'runtime ledger inside framework must be in .fcvw-cache')
    require(not requested.is_relative_to(source / '.fcvw-cache') or target.is_relative_to(source / '.fcvw-cache'),
            'runtime ledger cache path escapes through a filesystem link')
    return target


def _key(state: dict) -> tuple[str, str]:
    return state['control_digest'], state['observation']['run_id']


def record(path: Path, root: Path, config: dict, state: dict, previous: dict | None,
           write_output: Callable[[], None]) -> None:
    """Register a transition transactionally; a failed cross-file write stays fail-closed."""
    target = ledger_path(path, root)
    validate_runtime(state, config)
    if previous is not None:
        validate_runtime(previous, config)
        require(_key(previous) == _key(state), 'runtime identity changed')
        require(state['sequence'] == previous['sequence'] + 1, 'runtime sequence skipped')
    else:
        require(state['sequence'] == 0, 'new runtime must start at sequence zero')
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with sqlite3.connect(target, timeout=5) as database:
            database.execute('BEGIN IMMEDIATE')
            version = database.execute('PRAGMA user_version').fetchone()[0]
            require(version in (0, 1), 'unsupported runtime ledger version')
            database.execute('CREATE TABLE IF NOT EXISTS runs ('
                             'control_digest TEXT NOT NULL, run_id TEXT NOT NULL, task_id TEXT NOT NULL, '
                             'sequence INTEGER NOT NULL, '
                             'checksum TEXT NOT NULL, blocked INTEGER NOT NULL, state_json TEXT NOT NULL, '
                             'PRIMARY KEY(control_digest, run_id))')
            database.execute('PRAGMA user_version=1')
            key = _key(state)
            existing = database.execute('SELECT sequence, checksum, blocked FROM runs '
                                        'WHERE control_digest=? AND run_id=?', key).fetchone()
            if previous is None:
                require(existing is None, 'run_id already exists in runtime ledger; use observe or a new run_id')
                blocked_task = database.execute('SELECT run_id FROM runs WHERE control_digest=? '
                                                'AND task_id=? AND blocked=1',
                                                (key[0], state['observation']['task_id'])).fetchone()
                require(blocked_task is None, 'task has a persistent stop under this control')
                database.execute('INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?, ?)',
                                 (*key, state['observation']['task_id'], state['sequence'],
                                  state['checksum'], int(state['blocked']),
                                  json.dumps(state, sort_keys=True)))
            else:
                require(existing is not None and existing[:2] == (previous['sequence'], previous['checksum']),
                        'stale or unregistered previous runtime')
                require(not existing[2] or state['blocked'], 'persistent stop latch was cleared')
                database.execute('UPDATE runs SET sequence=?, checksum=?, blocked=?, state_json=? '
                                 'WHERE control_digest=? AND run_id=?',
                                 (state['sequence'], state['checksum'], int(state['blocked']),
                                  json.dumps(state, sort_keys=True), *key))
            write_output()
    except sqlite3.Error as error:
        raise ValueError(f'runtime ledger unavailable: {error}') from error


def verify_latest(path: Path, root: Path, config: dict, state: dict) -> None:
    """Reject stale, restarted or unregistered runtime files before selection."""
    target = ledger_path(path, root)
    validate_runtime(state, config)
    require(target.is_file(), 'runtime ledger missing')
    try:
        with sqlite3.connect(target, timeout=5) as database:
            require(database.execute('PRAGMA user_version').fetchone()[0] == 1,
                    'unsupported runtime ledger version')
            row = database.execute('SELECT sequence, checksum, blocked FROM runs '
                                   'WHERE control_digest=? AND run_id=?', _key(state)).fetchone()
    except sqlite3.Error as error:
        raise ValueError(f'runtime ledger unavailable: {error}') from error
    require(row is not None and row == (state['sequence'], state['checksum'], int(state['blocked'])),
            'runtime is not the latest registered state')
