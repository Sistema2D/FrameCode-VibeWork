#!/usr/bin/env python3
"""Run trusted FCVW checks locally, without a hosted service or network access."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time
import uuid

from release_layout_fcvw import governed_root
from verify_release_fcvw import tool_directory

IGNORED = {'.git', '.obsidian', '.fcvw-cache', '__pycache__', '.codex-test-tmp'}
LOCALES = {'pt-BR', 'en-US', 'es', 'de'}
PROBE = ('import json,platform,sys; print(json.dumps(dict('
         'executable=sys.executable,version=sys.version,os=platform.system(),'
         'machine=platform.machine())))')


def snapshot(root: Path) -> dict:
    """Bind evidence to file bytes, including uncommitted changes; omit caches."""
    hashes = {}
    for folder, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in IGNORED)
        for name in sorted(files):
            p = Path(folder) / name
            relative = p.relative_to(root).as_posix()
            if relative == 'FCVW/ROLE_MANIFEST.json' or p.suffix in {'.pyc', '.pyo'}:
                continue
            hashes[relative] = hashlib.sha256(p.read_bytes()).hexdigest()
    revision = dirty = None
    try:
        top = subprocess.check_output(['git', '-C', str(root), 'rev-parse', '--show-toplevel'],
                                      stderr=subprocess.DEVNULL, text=True, timeout=10).strip()
        if Path(top).resolve() == root.resolve():
            revision = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True, timeout=10).strip()
            dirty = bool(subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain'], text=True, timeout=10).strip())
    except (OSError, subprocess.SubprocessError):
        pass
    return {'revision': revision, 'dirty': dirty, 'files': len(hashes),
            'tree_sha256': hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()}


def release_assets(directory: Path) -> list[Path]:
    archives = sorted(directory.glob('*.zip'))
    versions, languages = set(), []
    for archive in archives:
        match = re.fullmatch(r'FrameCode-VibeWork-(V\d+\.\d+\.\d+)-(pt-BR|en-US|es|de)\.zip', archive.name)
        if not match:
            raise ValueError(f'unexpected release archive: {archive.name}')
        versions.add(match[1]); languages.append(match[2])
    if len(archives) != 4 or set(languages) != LOCALES or len(versions) != 1:
        raise ValueError('release directory must contain exactly four language ZIPs of one version')
    if not (directory / 'SHA256SUMS.txt').is_file():
        raise ValueError('release directory requires SHA256SUMS.txt')
    return archives


def run_step(name: str, command: list[str], root: Path, directory: Path, timeout: int) -> dict:
    log = directory / (name + '.log')
    start = time.monotonic()
    env = {**os.environ, 'PYTHONUTF8': '1', 'PYTHONDONTWRITEBYTECODE': '1'}
    error = None
    with log.open('w', encoding='utf-8') as output:
        try:
            result = subprocess.run(command, cwd=root, env=env, stdout=output,
                                    stderr=subprocess.STDOUT, timeout=timeout, check=False)
            code = result.returncode
        except subprocess.TimeoutExpired:
            code, error = None, f'command exceeded {timeout} seconds'
        except OSError as exc:
            code, error = None, str(exc)
        if error:
            output.write('\n' + error + '\n')
    return {'name': name, 'command': command, 'status': 'pass' if code == 0 else 'fail',
            'returncode': code, 'error': error, 'seconds': round(time.monotonic() - start, 3),
            'log': str(log)}


def run_checks(root: Path, output: Path, interpreters: list[str], *, timeout: int = 900,
               release_dir: Path | None = None, release_source: Path | None = None) -> tuple[dict, Path]:
    root, output = root.resolve(), output.resolve()
    source = (release_source or root).resolve()
    if timeout < 1 or not interpreters:
        raise ValueError('positive timeout and at least one interpreter required')
    if not (root / 'AGENTS.md').is_file():
        raise ValueError('root must be a trusted FCVW template or source checkout')
    # Prevent reports from contaminating the tree or recursive installed smoke copies.
    for tree in {root, source}:
        if output.is_relative_to(tree) and not output.is_relative_to((tree / '.fcvw-cache').resolve()):
            raise ValueError('output inside a source tree must be under .fcvw-cache')
    if release_source and not release_dir:
        raise ValueError('--release-source requires --release-dir')
    archives = release_assets(release_dir.resolve()) if release_dir else []
    asset_files = [*archives, archives[0].parent / 'SHA256SUMS.txt'] if archives else []
    asset_hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in asset_files}
    tools = tool_directory(root)
    for name in ('validate_fcvw.py', 'benchmark_retrieval_fcvw.py', 'verify_release_fcvw.py'):
        if not (tools / name).is_file():
            raise ValueError(f'missing trusted tool: {name}')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    directory = output / (stamp + '-' + uuid.uuid4().hex[:8])
    directory.mkdir(parents=True, exist_ok=False)
    report = {'schema': 'fcvw/local-validation@1', 'started_at': stamp,
              'source': snapshot(root), 'host_os': platform.system(), 'runtimes': [],
              'release_assets': [p.name for p in archives],
              'release_sha256': asset_hashes,
              'release_source': snapshot(source) if archives else None,
              'notice': 'Local trusted-code execution only. Coverage is limited to recorded runtimes and host OS. '
                        'No hosted checks, independent attestation or release publication is implied.'}
    for index, executable in enumerate(dict.fromkeys(interpreters), 1):
        folder = directory / str(index); folder.mkdir()
        probe = run_step('runtime', [executable, '-I', '-c', PROBE], root, folder, timeout)
        runtime = {'requested': executable, 'steps': [probe]}
        report['runtimes'].append(runtime)
        if probe['status'] != 'pass':
            continue
        try:
            runtime['identity'] = json.loads(Path(probe['log']).read_text(encoding='utf-8'))
            if not isinstance(runtime['identity'], dict) or not all(runtime['identity'].get(k) for k in ('version', 'executable', 'os', 'machine')):
                raise ValueError('runtime probe did not identify the interpreter')
        except (ValueError, TypeError) as exc:
            probe.update(status='fail', error=str(exc)); continue
        py = [executable, '-B']
        commands = [
            ('tests', [*py, '-m', 'unittest', 'discover', '-s', str(tools), '-p', 'test_*.py']),
            ('governance', [*py, str(tools / 'validate_fcvw.py'), '--root', str(root), '--profile', 'clean-template']),
            ('benchmark', [*py, str(tools / 'benchmark_retrieval_fcvw.py'), '--root', str(root), '--check', '--output', str(folder / 'benchmark.json')]),
            ('installed', [*py, str(tools / 'verify_release_fcvw.py'), '--source-root', str(root), '--smoke', '--run-tests']),
        ]
        commands.extend((f'archive-{a.stem}', [*py, str(tools / 'verify_release_fcvw.py'),
                         '--source-root', str(source), '--archive', str(a),
                         '--checksums', str(a.parent / 'SHA256SUMS.txt'), '--run-tests']) for a in archives)
        for name, command in commands:
            step = run_step(name, command, root, folder, timeout)
            runtime['steps'].append(step)
            print(f'{index}: {name}: {step["status"]}', flush=True)
    report['source_after'] = snapshot(root)
    report['source_unchanged'] = report['source']['tree_sha256'] == report['source_after']['tree_sha256']
    report['release_source_unchanged'] = not archives or report['release_source']['tree_sha256'] == snapshot(source)['tree_sha256']
    try:
        report['release_assets_unchanged'] = asset_hashes == {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in asset_files}
    except OSError:
        report['release_assets_unchanged'] = False
    report['status'] = 'pass' if (report['source_unchanged'] and report['release_source_unchanged'] and report['release_assets_unchanged'] and
                       all(s['status'] == 'pass' for rt in report['runtimes'] for s in rt['steps'])) else 'fail'
    report['finished_at'] = datetime.now(timezone.utc).isoformat()
    path = directory / 'report.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report, path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default=str(governed_root(Path(__file__))))
    parser.add_argument('--output', help='local report directory; default: ROOT/.fcvw-cache/local-checks')
    parser.add_argument('--python', action='append', dest='interpreters', help='repeat a trusted Python executable path; default: current interpreter')
    parser.add_argument('--timeout', type=int, default=900, help='timeout per command, in seconds')
    parser.add_argument('--release-dir', help='optional existing four-language ZIP set plus SHA256SUMS.txt')
    parser.add_argument('--release-source', help='trusted source matching the archives; default: --root')
    args = parser.parse_args()
    root = Path(args.root).resolve()
    try:
        report, path = run_checks(root, Path(args.output) if args.output else root / '.fcvw-cache/local-checks',
                                  args.interpreters or [sys.executable], timeout=args.timeout,
                                  release_dir=Path(args.release_dir) if args.release_dir else None,
                                  release_source=Path(args.release_source) if args.release_source else None)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'local validation failed: {exc}\n')
    print(f'FCVW local validation: {report["status"]}; report={path}')
    return 0 if report['status'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
