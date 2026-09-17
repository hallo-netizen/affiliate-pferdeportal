#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

import full_local_acceptance as legacy
import production_checks
import real_known_regression_acceptance_v3 as v3
import supervisor


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
    runtime = Path(tempfile.mkdtemp(prefix='system4-real-research-owner-v1-'))
    raw = legacy.build_fixture(runtime / 'fixture')
    files = v3._prepare_point0(runtime, raw)
    workspace = runtime / 'item-0'

    v3._start_real_pipeline(files, workspace, env)
    expected = supervisor.expected_research_document(workspace)
    good_path = v3.write_json(runtime / 'research.supervisor-bound.json', expected)

    bad = copy.deepcopy(expected)
    bad_evidence = bad['sources'][0]['evidence'] + ' Manipulierte Evidenz.'
    bad['sources'][0]['evidence'] = bad_evidence
    # Deliberately keep the original hash: this is a worker-produced malformed document,
    # not a valid-but-unbound alternate source pool.
    bad_path = v3.write_json(runtime / 'research.bad.json', bad)

    before = (workspace / 'state.json').read_bytes()
    failed = v3.run([sys.executable, str(v3.CONTROLLER), 'research', str(workspace), str(bad_path)], 4, env)
    if 'SYSTEM4_STAGE_OWNER_RETURN:RESEARCH_WORKER:RESEARCH_STAGE:' not in failed.stdout:
        raise AssertionError('REAL_RESEARCH_OWNER_RETURN_NOT_OBSERVED:' + failed.stdout)
    if 'RESEARCH_SOURCE_HASH_MISMATCH:0' not in failed.stdout:
        raise AssertionError('REAL_RESEARCH_ERROR_NOT_OBSERVED:' + failed.stdout)
    if (workspace / 'state.json').read_bytes() != before:
        raise AssertionError('RESEARCH_OWNER_RETURN_MUTATED_STATE')
    frozen = json.loads(before.decode('utf-8'))
    if frozen.get('phase') != 'RESEARCH_REQUIRED' or frozen.get('research') is not None:
        raise AssertionError('RESEARCH_OWNER_RETURN_ADVANCED_PIPELINE')

    passed = v3.run([sys.executable, str(v3.CONTROLLER), 'research', str(workspace), str(good_path)], 0, env)
    if 'SYSTEM4_RESEARCH_PASS:FACT_CHECK_REQUIRED' not in passed.stdout:
        raise AssertionError('RESEARCH_RETRY_DID_NOT_PASS:' + passed.stdout)
    v3.run([sys.executable, str(v3.CONTROLLER), 'facts', str(workspace), str(files['facts'])], 0, env)
    v3.run([sys.executable, str(v3.CONTROLLER), 'context', str(workspace), str(files['pack']), str(files['plan'])], 0, env)
    v3.run([sys.executable, str(v3.CONTROLLER), 'draft', str(workspace), str(files['final'])], 0, env)
    checked = v3.run([sys.executable, str(v3.CONTROLLER), 'fullcheck', str(workspace)], 0, env)
    if 'SYSTEM4_FULL_CHECK_PASS:OUTPUT_GATE_REQUIRED' not in checked.stdout:
        raise AssertionError('RESEARCH_RETRY_REAL_FULLCHECK_NOT_PASS:' + checked.stdout)

    state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
    evidence = state['checks']['production_evidence']['evidence']
    if evidence['languagetool']['status'] != 'PASS' or evidence['ppm679']['status'] != 'PASS':
        raise AssertionError('RESEARCH_RETRY_REAL_VALIDATORS_NOT_PASS')

    output = runtime / 'output'
    output.mkdir()
    collected, envelope, reconstructed = legacy.handoff_from_state(files, workspace / 'state.json', output)
    final_root = Path(os.environ.get('SYSTEM4_ACCEPTANCE_OUTPUT_DIR', '/tmp/system4-acceptance-output'))
    final_root.mkdir(parents=True, exist_ok=True)
    final_path = final_root / 'SYSTEM4_RESEARCH_OWNER_REPAIRED_WORDPRESS.json'
    final_path.write_bytes(reconstructed.read_bytes())
    if final_path.read_bytes() != reconstructed.read_bytes():
        raise AssertionError('RESEARCH_OWNER_FINAL_FILE_NOT_BYTE_EQUAL')

    proof = {
        'contract': 'SYSTEM4_REAL_RESEARCH_OWNER_ACCEPTANCE_V1',
        'status': 'PASS',
        'head': files['head'],
        'start_path': 'CHAT_START->POINT0->ROOT->SUPERVISOR->WORKER_DISPATCH->CODEX_WORKER_START',
        'initial_error': 'RESEARCH_SOURCE_HASH_MISMATCH:0',
        'repair_owner': 'RESEARCH_WORKER',
        'return_route': 'RESEARCH_STAGE',
        'state_frozen_on_return': True,
        'valid_but_unbound_research_policy': 'HARD_BLOCK_BY_SUPERVISOR',
        'real_languagetool_sha256': production_checks.LT_JAR_SHA256,
        'real_ppm_sha256': production_checks.PPM_PACKAGE_SHA256,
        'article_count': collected['article_count'],
        'handoff_parts': envelope['part_count'],
        'final_sha256': v3.sha_bytes(final_path.read_bytes()),
        'inline_byte_equal': True,
        'publish_allowed': False,
    }
    v3.write_json(final_root / 'SYSTEM4_REAL_RESEARCH_OWNER_ACCEPTANCE_V1.json', proof)
    print(json.dumps(proof, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
