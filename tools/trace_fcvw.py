"""Opt-in, content-free cross-tool decision events; the caller supplies one run ID."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
from typing import Iterable


IDENTITY = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")


def append(path: Path, root: Path, *, run_id: str, component: str, status: str,
           reason: str, input_digest: str | None = None, duration_ms: int | None = None,
           provider_tokens: int | None = None, protected: Iterable[Path] = ()) -> None:
    protected = tuple(protected)
    if any(not IDENTITY.fullmatch(value) for value in (run_id, component, status, reason)):
        raise ValueError('trace identities must be short safe labels')
    if duration_ms is not None and (type(duration_ms) is not int or duration_ms < 0):
        raise ValueError('invalid trace duration')
    if provider_tokens is not None and (type(provider_tokens) is not int or provider_tokens < 0):
        raise ValueError('invalid provider token count')
    if input_digest is not None and not re.fullmatch(r'[0-9a-f]{64}', input_digest):
        raise ValueError('input digest must be SHA-256 hex')
    target, source = path.resolve(), root.resolve()
    requested = Path(os.path.abspath(path))
    if requested.is_relative_to(source) and not requested.is_relative_to(source / '.fcvw-cache'):
        raise ValueError('trace inside framework must be in .fcvw-cache')
    if target.is_relative_to(source) and not target.is_relative_to(source / '.fcvw-cache'):
        raise ValueError('trace inside framework must be in .fcvw-cache')
    if requested.is_relative_to(source / '.fcvw-cache') and not target.is_relative_to(source / '.fcvw-cache'):
        raise ValueError('trace cache path escapes through a filesystem link')
    if target in {item.resolve() for item in protected} or (target.exists() and any(
            item.exists() and target.samefile(item) for item in protected)):
        raise ValueError('trace cannot overwrite an input or report')
    record = {'schema': 'fcvw/decision-trace@1', 'at': datetime.now(timezone.utc).isoformat(),
              'run_id': run_id, 'component': component, 'status': status, 'reason': reason,
              'input_digest': input_digest, 'duration_ms': duration_ms,
              'provider_tokens': provider_tokens,
              'token_source': 'provider' if provider_tokens is not None else 'unavailable'}
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(target, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    try:
        payload = (json.dumps(record, sort_keys=True) + '\n').encode('utf-8')
        if os.write(descriptor, payload) != len(payload):
            raise OSError('incomplete trace write')
    finally:
        os.close(descriptor)
