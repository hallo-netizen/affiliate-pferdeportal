#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import os
import sys
import tempfile
from pathlib import Path

import full_local_acceptance as legacy
import production_checks
import real_known_regression_acceptance_v3 as v3
import supervisor


def _bad_pack_from(path: Path, out: Path) -> Path:
    value = json.loads(path.read_text(encoding='utf-8'))
    bad = copy.deepcopy(value)
    bad['claims'] = []
    return v3.write_json(out, bad)


def main() -> int:
    jar = Path(os.environ.get('SYSTEM4_LANGUAGETOOL_JAR', ''))
    if not jar.is_file() or production_checks.file_sha256(jar) != production_checks.LT_JAR_SHA256:
        raise SystemExit('LT68_HASH_BOUND_JAR_REQUIRED')
    ppm = v3.REPO / production_checks.PPM_PACKAGE_REL
    if production_checks.file_sha256(ppm) != production_checks.PPM_PACKAGE_SHA256:
        raise SystemExit('PPM679_HASH_BOUND_PACKAGE_REQUIRED')

    env = os.environ.copy()
    env['SYSTEM4_LANGUAGETOOL_JAR'] = str(jar)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    runtime = Path(tempfile.mkdtemp(prefix='system4-real-context-owner-v1-'))
    raw = legacy.build_fixture(runtime / 'fixture')
    files = v3._prepare_point0(runtime, raw)
    workspace = runtime / 'item-0'

    v3._start_real_pipeline(files, workspace, env)
    research = supervisor.expected_research_document(workspace)
    research_path = v3.write_json(runtime / 'research.supervisor-bound.json', research)
    v3.run([sys.executable, str(v3.CONTROLLER), 'research', str(workspace), str(research_path)], 0, env)
    v3.run([sys.executable, str(v3.CONTROLLER), 'facts', str(workspace), str(files['facts'])], 0, env)

    bad_pack = _bad_pack_from(files['pack'], runtime / 'fact_pack.bad.json')
    before = (workspace / 'state.json').read_bytes()
    bad = v3.run([sys.executable, str(v3.CONTROLLER), 'context', str(workspace), str(bad_pack), str(files['plan'])], 4, env)
    if 'SYSTEM4_STAGE_OWNER_RETURN:CONTEXT_WORKER:CONTEXT_STAGE:' not in bad.stdout:
        raise AssertionError('REAL_CONTEXT_OWNER_RETURN_NOT_OBSERVED:' + bad.stdout)
    if 'FACT_PACK_CLAIMS_TOO_LOW' not in bad.stdout:
        raise AssertionError('REAL_CONTEXT_ERROR_NOT_OBSERVED:' + bad.stdout)
    if (workspace / 'state.json').read_bytes() != before:
        raise AssertionError('CONTEXT_OWNER_RETURN_MUTATED_STATE')
    frozen = json.loads(before.decode('utf-8'))
    if frozen.get('phase') != 'CONTEXT_REQUIRED' or frozen.get('production_context') is not None:
        raise AssertionError('CONTEXT_OWNER_RETURN_ADVANCED_PIPELINE')

    good = v3.run([sys.executable, str(v3.CONTROLLER), 'context', str(workspace), str(files['pack']), str(files['plan'])], 0, env)
    if 'SYSTEM4_PRODUCTION_CONTEXT_PASS:DRAFT_REQUIRED' not in good.stdout:
        raise AssertionError('CONTEXT_RETRY_DID_NOT_PASS:' + good.stdout)
    v3.run([sys.executable, str(v3.CONTROLLER), 'draft', str(workspace), str(files['final'])], 0, env)
    checked = v3.run([sys.executable, str(v3.CONTROLLER), 'fullcheck', str(workspace)], 0, env)
    if 'SYSTEM4_FULL_CHECK_PASS:OUTPUT_GATE_REQUIRED' not in checked.stdout:
        raise AssertionError('CONTEXT_RETRY_REAL_FULLCHECK_NOT_PASS:' + checked.stdout)

    state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
    evidence = state['checks']['production_evidence']['evidence']
    if evidence['languagetool']['status'] != 'PASS' or evidence['ppm679']['status'] != 'PASS':
        raise AssertionError('CONTEXT_RETRY_REAL_VALIDATORS_NOT_PASS')

    output = runtime / 'output'
    output.mkdir()
    collected, envelope, reconstructed = legacy.handoff_from_state(files, workspace / 'state.json', output)
    final_root = Path(os.environ.get('SYSTEM4_ACCEPTANCE_OUTPUT_DIR', '/tmp/system4-acceptance-output'))
    final_root.mkdir(parents=True, exist_ok=True)
    final_path = final_root / 'SYSTEM4_CONTEXT_OWNER_REPAIRED_WORDPRESS.json'
    final_path.write_bytes(reconstructed.read_bytes())
    if final_path.read_bytes() != reconstructed.read_bytes():
        raise AssertionError('CONTEXT_OWNER_FINAL_FILE_NOT_BYTE_EQUAL')

    proof = {
        'contract': 'SYSTEM4_REAL_CONTEXT_OWNER_ACCEPTANCE_V1',
        'status': 'PASS',
        'head': files['head'],
        'start_path': 'CHAT_START->POINT0->ROOT->SUPERVISOR->WORKER_DISPATCH->CODEX_WORKER_START',
        'initial_error': 'FACT_PACK_CLAIMS_TOO_LOW',
        'repair_owner': 'CONTEXT_WORKER',
        'return_route': 'CONTEXT_STAGE',
        'state_frozen_on_return': True,
        'real_languagetool_sha256': production_checks.LT_JAR_SHA256,
        'real_ppm_sha256': production_checks.PPM_PACKAGE_SHA256,
        'article_count': collected['article_count'],
        'handoff_parts': envelope['part_count'],
        'final_sha256': v3.sha_bytes(final_path.read_bytes()),
        'inline_byte_equal': True,
        'publish_allowed': False,
    }
    v3.write_json(final_root / 'SYSTEM4_REAL_CONTEXT_OWNER_ACCEPTANCE_V1.json', proof)
    print(json.dumps(proof, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
