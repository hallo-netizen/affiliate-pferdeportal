#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import chat_start_gate
import codex_entry
import full_local_acceptance as legacy
import machine_point0
import point0_snapshot
import production_checks
import root_entry
import source_acquisition
import supervisor

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
CONTROLLER = HERE / 'controller.py'
ROOT_ENTRY = HERE / 'root_entry.py'
CODEX_ENTRY = HERE / 'codex_entry.py'


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable(value) -> str:
    return sha_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8'))


def write_json(path: Path, value: dict) -> Path:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    return path


def run(argv: list[str], expected: int | set[int] = 0, env: dict | None = None):
    if isinstance(expected, int):
        expected = {expected}
    cp = subprocess.run(argv, cwd=REPO, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    if cp.returncode not in expected:
        raise AssertionError(
            f'COMMAND_RC:{cp.returncode}:EXPECTED:{sorted(expected)}:{argv}\nSTDOUT:\n{cp.stdout}\nSTDERR:\n{cp.stderr}'
        )
    return cp


def _bind_current_start(snapshot: dict) -> dict:
    batch = snapshot['next_textmachine_metadata_batch']
    event = {
        'contract': chat_start_gate.START_EVENT_CONTRACT,
        'button_id': chat_start_gate.START_BUTTON_ID,
        'action': chat_start_gate.START_ACTION,
        'route': chat_start_gate.START_ROUTE,
        'article_count': batch['item_count'],
        'batch_sha256': batch['batch_sha256'],
        'publish_allowed': False,
    }
    return chat_start_gate.bind(snapshot, event)


def _prepare_point0(root: Path, files: dict) -> dict:
    snapshot = json.loads(files['snapshot'].read_text(encoding='utf-8'))
    snapshot['system4_root_manifest_sha256'] = root_entry._critical_manifest_sha256()
    snapshot = _bind_current_start(snapshot)
    snapshot_path = root / 'production_snapshot.bound.json'
    snapshot_path.write_bytes(json.dumps(snapshot, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8'))
    snapshot_sha = sha_bytes(snapshot_path.read_bytes())

    pack = json.loads(files['pack'].read_text(encoding='utf-8'))
    pack['source_snapshot_id'] = snapshot_sha
    pack['fact_pack_id'] = snapshot_sha
    pack_path = write_json(root / 'fact_pack.bound.json', pack)

    plan = json.loads(files['plan'].read_text(encoding='utf-8'))
    plan['source_snapshot_id'] = snapshot_sha
    plan_path = write_json(root / 'plan_item.bound.json', plan)

    research = json.loads(files['research'].read_text(encoding='utf-8'))
    acquired_sources = []
    for row in research['sources']:
        out = copy.deepcopy(row)
        out['http_status'] = 200
        out.setdefault('source_kind', 'CAPTURED_REAL_SOURCE')
        acquired_sources.append(out)

    article = snapshot['next_textmachine_metadata_batch']['items'][0]
    acquired = {
        'contract': source_acquisition.RESULT_CONTRACT,
        'item_count': 1,
        'items': [{
            'item_index': 0,
            'plan_slot': article['plan_slot'],
            'sources': acquired_sources,
        }],
    }
    plans = {
        'contract': 'SYSTEM4_MACHINE_PREWRITE_PLAN_BATCH_V1',
        'item_count': 1,
        'items': [{
            'item_index': 0,
            'plan_slot': article['plan_slot'],
            'production_plan_item': plan,
        }],
    }
    manifest = root_entry._critical_manifest_sha256()
    head = subprocess.check_output(['git', 'rev-parse', '--verify', 'HEAD'], cwd=REPO, text=True).strip()
    point0 = machine_point0.build_from_acquired(
        snapshot_bytes=snapshot_path.read_bytes(),
        acquired_batch=acquired,
        prewrite_plan_batch=plans,
        provider='SYSTEM4_ACCEPTANCE_CAPTURED_REAL_SOURCES_V3',
        manifest=manifest,
        head=head,
    )
    point0_path = root / 'point0.json'
    point0_path.write_bytes(point0_snapshot.canon(point0))
    return {
        'snapshot': snapshot_path,
        'pack': pack_path,
        'plan': plan_path,
        'facts': files['facts'],
        'regression': files['regression'],
        'final': files['final'],
        'point0': point0_path,
        'head': head,
        'manifest': manifest,
        'chat_start_receipt_sha256': snapshot['system4_chat_start']['receipt_sha256'],
    }


def _start_real_pipeline(files: dict, workspace: Path, env: dict) -> None:
    cp = run([sys.executable, str(ROOT_ENTRY), 'start-point0', str(files['point0']), str(workspace), '0'], 0, env)
    if 'SYSTEM4_ROOT_POINT0_PASS:WORKER_DISPATCH_READY' not in cp.stdout:
        raise AssertionError('ROOT_POINT0_DISPATCH_MARKER_MISSING:' + cp.stdout)
    for required in ('point0.json', 'bound_snapshot.json', 'bound_research_sources.json', 'bound_machine_prewrite.json', 'supervisor_state.json', 'worker_dispatch.json', 'state.json'):
        if not (workspace / required).is_file():
            raise AssertionError('ROOT_DISPATCH_ARTIFACT_MISSING:' + required)
    cp = run([sys.executable, str(CODEX_ENTRY), 'worker-start', str(workspace)], 0, env)
    if 'SYSTEM4_CODEX_ENTRY_PASS:RESEARCH_REQUIRED' not in cp.stdout:
        raise AssertionError('WORKER_START_RESEARCH_MARKER_MISSING:' + cp.stdout)


def _stage_to_draft(files: dict, workspace: Path, env: dict) -> None:
    _start_real_pipeline(files, workspace, env)
    # The real worker is allowed to research only inside the supervisor-bound source pool.
    # Acceptance therefore submits the supervisor's own canonical expected document, not a
    # pre-Point0 fixture that merely contains similar sources.
    research = supervisor.expected_research_document(workspace)
    research_path = write_json(workspace.parent / 'research.supervisor-bound.json', research)
    run([sys.executable, str(CONTROLLER), 'research', str(workspace), str(research_path)], 0, env)
    run([sys.executable, str(CONTROLLER), 'facts', str(workspace), str(files['facts'])], 0, env)
    run([sys.executable, str(CONTROLLER), 'context', str(workspace), str(files['pack']), str(files['plan'])], 0, env)


def main() -> int:
    jar = Path(os.environ.get('SYSTEM4_LANGUAGETOOL_JAR', ''))
    if not jar.is_file() or production_checks.file_sha256(jar) != production_checks.LT_JAR_SHA256:
        raise SystemExit('LT68_HASH_BOUND_JAR_REQUIRED')
    ppm = REPO / production_checks.PPM_PACKAGE_REL
    if production_checks.file_sha256(ppm) != production_checks.PPM_PACKAGE_SHA256:
        raise SystemExit('PPM679_HASH_BOUND_PACKAGE_REQUIRED')

    env = os.environ.copy()
    env['SYSTEM4_LANGUAGETOOL_JAR'] = str(jar)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    runtime = Path(tempfile.mkdtemp(prefix='system4-real-known-regression-v3-'))
    raw_fixture = legacy.build_fixture(runtime / 'fixture')
    files = _prepare_point0(runtime, raw_fixture)
    workspace = runtime / 'item-0'

    _stage_to_draft(files, workspace, env)
    run([sys.executable, str(CONTROLLER), 'draft', str(workspace), str(files['regression'])], 0, env)
    first = run([sys.executable, str(CONTROLLER), 'fullcheck', str(workspace)], 3, env)
    if 'BLOCKED_KNOWN_REGRESSION_PATTERN' not in first.stdout:
        raise AssertionError('REAL_PPM_KNOWN_REGRESSION_NOT_OBSERVED:' + first.stdout)
    if 'REPAIR_OWNER=DRAFT_WORKER' not in first.stdout:
        raise AssertionError('REAL_PPM_KNOWN_REGRESSION_WRONG_OWNER:' + first.stdout)
    state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
    if state.get('phase') != 'REPAIR_REQUIRED' or state.get('checks', {}).get('repair_owner') != 'DRAFT_WORKER':
        raise AssertionError('REAL_PPM_REPAIR_STATE_INVALID')

    run([sys.executable, str(CONTROLLER), 'repair', str(workspace), str(files['final'])], 0, env)
    second = run([sys.executable, str(CONTROLLER), 'fullcheck', str(workspace)], 0, env)
    if 'SYSTEM4_FULL_CHECK_PASS:OUTPUT_GATE_REQUIRED' not in second.stdout:
        raise AssertionError('REAL_RECHECK_PASS_MARKER_MISSING:' + second.stdout)
    state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
    evidence = state['checks']['production_evidence']['evidence']
    if evidence['languagetool']['status'] != 'PASS' or evidence['ppm679']['status'] != 'PASS':
        raise AssertionError('REAL_VALIDATORS_NOT_PASS_AFTER_REPAIR')

    output = runtime / 'output'
    output.mkdir()
    collected, envelope, reconstructed = legacy.handoff_from_state(files, workspace / 'state.json', output)
    final_root = Path(os.environ.get('SYSTEM4_ACCEPTANCE_OUTPUT_DIR', '/tmp/system4-acceptance-output'))
    final_root.mkdir(parents=True, exist_ok=True)
    final_path = final_root / 'SYSTEM4_PPM_KNOWN_REGRESSION_REPAIRED_WORDPRESS.json'
    final_path.write_bytes(reconstructed.read_bytes())
    if final_path.read_bytes() != reconstructed.read_bytes():
        raise AssertionError('FINAL_FILE_NOT_BYTE_EQUAL')

    proof = {
        'contract': 'SYSTEM4_REAL_KNOWN_REGRESSION_ACCEPTANCE_V3',
        'status': 'PASS',
        'head': files['head'],
        'manifest': files['manifest'],
        'chat_start_receipt_sha256': files['chat_start_receipt_sha256'],
        'start_path': 'CHAT_START->POINT0->ROOT->SUPERVISOR->WORKER_DISPATCH->CODEX_WORKER_START',
        'ppm_error': 'BLOCKED_KNOWN_REGRESSION_PATTERN',
        'repair_owner': 'DRAFT_WORKER',
        'real_languagetool_sha256': production_checks.LT_JAR_SHA256,
        'real_ppm_sha256': production_checks.PPM_PACKAGE_SHA256,
        'revision': state['revision'],
        'article_count': collected['article_count'],
        'handoff_parts': envelope['part_count'],
        'final_sha256': sha_bytes(final_path.read_bytes()),
        'final_bytes': final_path.stat().st_size,
        'inline_byte_equal': True,
        'publish_allowed': False,
    }
    write_json(final_root / 'SYSTEM4_REAL_KNOWN_REGRESSION_ACCEPTANCE_V3.json', proof)
    print(json.dumps(proof, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
