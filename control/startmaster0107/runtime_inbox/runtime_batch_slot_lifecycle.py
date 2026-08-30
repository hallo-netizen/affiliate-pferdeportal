#!/usr/bin/env python3
from __future__ import annotations
import argparse, importlib.util, json, shutil, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
GUARD_PATH = HERE / 'runtime_batch_slot_guard.py'
if not GUARD_PATH.is_file():
    matches = sorted(HERE.glob('*runtime_batch_slot_guard.py'))
    if len(matches) != 1:
        raise RuntimeError('RUNTIME_GUARD_NOT_FOUND_OR_AMBIGUOUS')
    GUARD_PATH = matches[0]
spec = importlib.util.spec_from_file_location('runtime_batch_slot_guard', GUARD_PATH)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)

class LifecycleBlocked(RuntimeError):
    pass

def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))

def dump_atomic(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    tmp.replace(path)

def repo_rel(repo: Path, path: Path) -> str:
    full = path.resolve()
    root = repo.resolve()
    if root not in full.parents and full != root:
        raise LifecycleBlocked('SOURCE_OUTSIDE_REPO_AFTER_COPY')
    return full.relative_to(root).as_posix()

def state_path(repo: Path, contract: dict) -> Path:
    return guard.rel(repo, contract['state_ref'])

def validate_idle(repo: Path, contract_path: Path, statep: Path):
    out = guard.validate(repo, contract_path, statep)
    if out.get('status') != 'READY_IDLE':
        raise LifecycleBlocked('RUNTIME_SLOT_NOT_IDLE')
    return out

def source_file(path_value: str) -> Path:
    p = Path(path_value).resolve()
    if not p.is_file():
        raise LifecycleBlocked('SOURCE_FILE_MISSING')
    return p

def generation_dir(repo: Path, generation: int) -> Path:
    return repo / 'control/startmaster0107/runtime_inbox/generations' / f'{generation:06d}'

def prepare_snapshot(repo: Path, contract: dict, source: Path, generation: int):
    snap = load(source)
    manifest = snap.get('manifest_sha256')
    if not guard.valid_sha(manifest):
        raise LifecycleBlocked('SOURCE_MANIFEST_INVALID')
    batch = snap.get('next_textmachine_metadata_batch')
    checked = guard.validate_batch(batch, contract)
    gdir = generation_dir(repo, generation)
    gdir.mkdir(parents=True, exist_ok=False)
    dst = gdir / 'SOURCE_SNAPSHOT.json'
    shutil.copyfile(source, dst)
    return dst, manifest, checked

def package_candidate(repo: Path, contract_path: Path, contract: dict, base_state: dict, source: Path, gdir: Path):
    dst = gdir / 'PRODUCTION_PACKAGE.json'
    shutil.copyfile(source, dst)
    candidate = dict(base_state)
    candidate['status'] = 'EXECUTION_READY'
    candidate['production_package_ref'] = repo_rel(repo, dst)
    candidate['production_package_sha256'] = guard.sha_file(dst)
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', suffix='.json', delete=False, dir=str(gdir)) as tf:
        json.dump(candidate, tf, ensure_ascii=False, indent=2)
        tf.write('\n')
        tmpp = Path(tf.name)
    try:
        out = guard.validate(repo, contract_path, tmpp)
        if out.get('status') != 'RUNTIME_INPUTS_BOUND':
            raise LifecycleBlocked('PRODUCTION_PACKAGE_NOT_EXECUTION_READY')
    finally:
        tmpp.unlink(missing_ok=True)
    return candidate, out

def bind_snapshot(repo: Path, contract_path: Path, snapshot_source: str):
    contract = load(contract_path)
    statep = state_path(repo, contract)
    validate_idle(repo, contract_path, statep)
    current = load(statep)
    generation = int(current['generation']) + 1
    gdir = generation_dir(repo, generation)
    if gdir.exists():
        raise LifecycleBlocked('GENERATION_DIR_ALREADY_EXISTS')
    try:
        dst, manifest, checked = prepare_snapshot(repo, contract, source_file(snapshot_source), generation)
        candidate = {
            'contract': 'PFERDE_ATELIER_RUNTIME_BATCH_SLOT_STATE_V1',
            'status': 'BATCH_READY_PACKAGE_PENDING',
            'generation': generation,
            'source_snapshot_ref': repo_rel(repo, dst),
            'source_snapshot_sha256': guard.sha_file(dst),
            'source_manifest_sha256': manifest,
            'batch_sha256': checked['batch_sha256'],
            'production_package_ref': '',
            'production_package_sha256': '',
            'publish_allowed': False,
        }
        with tempfile.NamedTemporaryFile('w', encoding='utf-8', suffix='.json', delete=False, dir=str(gdir)) as tf:
            json.dump(candidate, tf, ensure_ascii=False, indent=2); tf.write('\n'); tmpp=Path(tf.name)
        try:
            out = guard.validate(repo, contract_path, tmpp)
            if out.get('status') != 'READY_WAITING_PACKAGE':
                raise LifecycleBlocked('BIND_SNAPSHOT_VALIDATION_FAILED')
        finally:
            tmpp.unlink(missing_ok=True)
        dump_atomic(statep, candidate)
        return {'ok': True, 'status': 'RUNTIME_BATCH_BOUND_WAITING_PACKAGE', 'generation': generation, 'batch_sha256': checked['batch_sha256'], 'item_count': len(checked['items']), 'publish_allowed': False}
    except Exception:
        if gdir.exists():
            shutil.rmtree(gdir)
        raise

def attach_package(repo: Path, contract_path: Path, package_source: str):
    contract = load(contract_path)
    statep = state_path(repo, contract)
    current = load(statep)
    if current.get('status') != 'BATCH_READY_PACKAGE_PENDING':
        raise LifecycleBlocked('RUNTIME_SLOT_NOT_WAITING_PACKAGE')
    generation = int(current['generation'])
    gdir = generation_dir(repo, generation)
    if not gdir.is_dir():
        raise LifecycleBlocked('GENERATION_DIR_MISSING')
    pkgdst = gdir / 'PRODUCTION_PACKAGE.json'
    if pkgdst.exists():
        raise LifecycleBlocked('PRODUCTION_PACKAGE_ALREADY_PRESENT')
    try:
        candidate, out = package_candidate(repo, contract_path, contract, current, source_file(package_source), gdir)
        dump_atomic(statep, candidate)
        return {'ok': True, 'status': 'RUNTIME_BATCH_EXECUTION_READY', 'generation': generation, 'batch_sha256': out['batch_sha256'], 'selected_item_count': out['selected_item_count'], 'package_id': out['package_id'], 'publish_allowed': False}
    except Exception:
        pkgdst.unlink(missing_ok=True)
        raise

def bind_ready(repo: Path, contract_path: Path, snapshot_source: str, package_source: str):
    first = bind_snapshot(repo, contract_path, snapshot_source)
    try:
        second = attach_package(repo, contract_path, package_source)
        return {'ok': True, 'status': 'RUNTIME_BATCH_EXECUTION_READY', 'generation': second['generation'], 'batch_sha256': second['batch_sha256'], 'selected_item_count': second['selected_item_count'], 'package_id': second['package_id'], 'publish_allowed': False}
    except Exception:
        contract = load(contract_path)
        statep = state_path(repo, contract)
        current = load(statep)
        generation = int(current.get('generation', first['generation']))
        gdir = generation_dir(repo, generation)
        idle = {
            'contract': 'PFERDE_ATELIER_RUNTIME_BATCH_SLOT_STATE_V1',
            'status': 'NO_ACTIVE_BATCH',
            'generation': generation - 1,
            'source_snapshot_ref': '', 'source_snapshot_sha256': '', 'source_manifest_sha256': '', 'batch_sha256': '',
            'production_package_ref': '', 'production_package_sha256': '', 'publish_allowed': False,
        }
        dump_atomic(statep, idle)
        if gdir.exists(): shutil.rmtree(gdir)
        raise

def clear_after_review(repo: Path, contract_path: Path):
    contract = load(contract_path)
    statep = state_path(repo, contract)
    current = load(statep)
    if current.get('status') == 'NO_ACTIVE_BATCH':
        validate_idle(repo, contract_path, statep)
        return {'ok': True, 'status': 'RUNTIME_SLOT_ALREADY_IDLE', 'generation': int(current['generation']), 'publish_allowed': False}
    if current.get('status') != 'EXECUTION_READY':
        raise LifecycleBlocked('RUNTIME_SLOT_NOT_EXECUTION_READY_FOR_CLEAR')
    checked = guard.validate(repo, contract_path, statep)
    if checked.get('status') != 'RUNTIME_INPUTS_BOUND':
        raise LifecycleBlocked('RUNTIME_INPUTS_NOT_VALID_FOR_CLEAR')
    generation = int(current['generation'])
    expected_dir = generation_dir(repo, generation).resolve()
    for field in ('source_snapshot_ref', 'production_package_ref'):
        p = guard.rel(repo, current[field]).resolve()
        if expected_dir not in p.parents:
            raise LifecycleBlocked('RUNTIME_FILE_NOT_IN_GENERATION_DIR')
    idle = {
        'contract': 'PFERDE_ATELIER_RUNTIME_BATCH_SLOT_STATE_V1',
        'status': 'NO_ACTIVE_BATCH',
        'generation': generation,
        'source_snapshot_ref': '', 'source_snapshot_sha256': '', 'source_manifest_sha256': '', 'batch_sha256': '',
        'production_package_ref': '', 'production_package_sha256': '', 'publish_allowed': False,
    }
    dump_atomic(statep, idle)
    if expected_dir.exists():
        shutil.rmtree(expected_dir)
    out = guard.validate(repo, contract_path, statep)
    if out.get('status') != 'READY_IDLE':
        raise LifecycleBlocked('POST_CLEAR_IDLE_VALIDATION_FAILED')
    return {'ok': True, 'status': 'RUNTIME_SLOT_CLEARED_AND_IDLE', 'generation': generation, 'publish_allowed': False}

def status(repo: Path, contract_path: Path):
    contract = load(contract_path)
    return guard.validate(repo, contract_path, state_path(repo, contract))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('command', choices=['bind-snapshot','attach-package','bind-ready','clear-after-review','status'])
    ap.add_argument('--repo', default='.')
    ap.add_argument('--contract', default=str(HERE / 'RUNTIME_BATCH_SLOT_CONTRACT_V1.json'))
    ap.add_argument('--snapshot')
    ap.add_argument('--package')
    a = ap.parse_args()
    repo = Path(a.repo).resolve(); contract_path = Path(a.contract).resolve()
    try:
        if a.command == 'bind-snapshot':
            if not a.snapshot: raise LifecycleBlocked('SNAPSHOT_REQUIRED')
            out = bind_snapshot(repo, contract_path, a.snapshot)
        elif a.command == 'attach-package':
            if not a.package: raise LifecycleBlocked('PACKAGE_REQUIRED')
            out = attach_package(repo, contract_path, a.package)
        elif a.command == 'bind-ready':
            if not a.snapshot or not a.package: raise LifecycleBlocked('SNAPSHOT_AND_PACKAGE_REQUIRED')
            out = bind_ready(repo, contract_path, a.snapshot, a.package)
        elif a.command == 'clear-after-review':
            out = clear_after_review(repo, contract_path)
        else:
            out = status(repo, contract_path)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    except (LifecycleBlocked, guard.Blocked, ValueError, KeyError, TypeError, json.JSONDecodeError, OSError) as e:
        print(json.dumps({'ok': False, 'status': 'RUNTIME_BATCH_LIFECYCLE_BLOCKED', 'error': str(e), 'publish_allowed': False}, ensure_ascii=False, indent=2))
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
