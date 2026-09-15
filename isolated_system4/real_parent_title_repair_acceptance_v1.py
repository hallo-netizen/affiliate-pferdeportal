#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import os
import sys
import tempfile
from pathlib import Path

import full_local_acceptance as legacy
import parent_owner_repair
import production_checks
import real_known_regression_acceptance_v3 as v3


def _apply_title(files: dict, title: str) -> None:
    snapshot = json.loads(files['snapshot'].read_text(encoding='utf-8'))
    snapshot['next_textmachine_metadata_batch']['items'][0]['title'] = title
    files['snapshot'].write_text(json.dumps(snapshot, ensure_ascii=False, sort_keys=True, separators=(',', ':')), encoding='utf-8')

    plan = json.loads(files['plan'].read_text(encoding='utf-8'))
    plan['topic'] = title
    if isinstance(plan.get('canonical_article'), dict):
        plan['canonical_article']['title'] = title
    if isinstance(plan.get('quality_binding'), dict):
        plan['quality_binding_hash'] = v3.stable(plan['quality_binding'])
    v3.write_json(files['plan'], plan)


def _item_from_snapshot(path: Path) -> dict:
    value = json.loads(path.read_text(encoding='utf-8'))
    return copy.deepcopy(value['next_textmachine_metadata_batch']['items'][0])


def _finding_from_state(workspace: Path) -> dict:
    state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
    findings = state.get('checks', {}).get('findings')
    if not isinstance(findings, list) or not findings:
        raise AssertionError('PARENT_TITLE_FINDING_MISSING')
    title_findings = [row for row in findings if isinstance(row, dict) and row.get('repair_owner') == 'PARENT_TITLE_MACHINE']
    if len(title_findings) != 1:
        raise AssertionError('PARENT_TITLE_FINDING_NOT_UNIQUE:' + repr(title_findings))
    if state.get('phase') != 'CHECK_REQUIRED':
        raise AssertionError('PARENT_TITLE_RETURN_MUST_FREEZE_CHECK_REQUIRED')
    if state.get('checks', {}).get('return_route') != 'PARENT_LAUNCH':
        raise AssertionError('PARENT_TITLE_RETURN_ROUTE_INVALID')
    return title_findings[0]


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
    runtime = Path(tempfile.mkdtemp(prefix='system4-real-parent-title-v1-'))

    bad_raw = legacy.build_fixture(runtime / 'bad-fixture')
    bad_title = 'Was muss vor einer Fahrt mit Pferdeanhänger geprüft werden: Checkliste?'
    _apply_title(bad_raw, bad_title)
    bad_generation = runtime / 'bad-generation'
    bad_generation.mkdir()
    bad_files = v3._prepare_point0(bad_generation, bad_raw)
    bad_workspace = bad_generation / 'item-0'
    v3._stage_to_draft(bad_files, bad_workspace, env)
    v3.run([sys.executable, str(v3.CONTROLLER), 'draft', str(bad_workspace), str(bad_files['final'])], 0, env)
    first = v3.run([sys.executable, str(v3.CONTROLLER), 'fullcheck', str(bad_workspace)], 4, env)
    if 'PARENT_TITLE_MACHINE' not in first.stdout or 'PARENT_LAUNCH' not in first.stdout:
        raise AssertionError('REAL_PARENT_TITLE_OWNER_RETURN_NOT_OBSERVED:' + first.stdout)
    finding = _finding_from_state(bad_workspace)
    if finding.get('error_code') != 'BLOCKED_CONTENT_TITLE_COLON':
        raise AssertionError('REAL_PARENT_TITLE_ERROR_CODE_UNEXPECTED:' + repr(finding))

    old_point0 = bad_files['point0'].read_bytes()
    old_point0_sha = v3.sha_bytes(old_point0)
    old_item = _item_from_snapshot(bad_files['snapshot'])
    repaired = parent_owner_repair.repair_item(old_item, finding)
    repaired_title = repaired['item']['title']
    if ':' in repaired_title or repaired_title == bad_title:
        raise AssertionError('PARENT_TITLE_MACHINE_DID_NOT_REPAIR_TITLE')

    good_raw = legacy.build_fixture(runtime / 'repaired-fixture')
    _apply_title(good_raw, repaired_title)
    repaired_generation = runtime / 'repaired-generation'
    repaired_generation.mkdir()
    good_files = v3._prepare_point0(repaired_generation, good_raw)
    good_workspace = repaired_generation / 'item-0'

    if bad_files['point0'].read_bytes() != old_point0:
        raise AssertionError('SEALED_OLD_POINT0_MUTATED')
    if v3.sha_bytes(bad_files['point0'].read_bytes()) != old_point0_sha:
        raise AssertionError('SEALED_OLD_POINT0_HASH_CHANGED')
    if good_files['point0'].read_bytes() == old_point0:
        raise AssertionError('REPAIRED_GENERATION_MUST_CREATE_NEW_POINT0')

    v3._stage_to_draft(good_files, good_workspace, env)
    v3.run([sys.executable, str(v3.CONTROLLER), 'draft', str(good_workspace), str(good_files['final'])], 0, env)
    second = v3.run([sys.executable, str(v3.CONTROLLER), 'fullcheck', str(good_workspace)], 0, env)
    if 'SYSTEM4_FULL_CHECK_PASS:OUTPUT_GATE_REQUIRED' not in second.stdout:
        raise AssertionError('REAL_PARENT_TITLE_RECHECK_NOT_PASS:' + second.stdout)
    state = json.loads((good_workspace / 'state.json').read_text(encoding='utf-8'))
    evidence = state['checks']['production_evidence']['evidence']
    if evidence['languagetool']['status'] != 'PASS' or evidence['ppm679']['status'] != 'PASS':
        raise AssertionError('REAL_VALIDATORS_NOT_PASS_AFTER_PARENT_TITLE_RESTART')

    output = repaired_generation / 'output'
    output.mkdir()
    collected, envelope, reconstructed = legacy.handoff_from_state(good_files, good_workspace / 'state.json', output)
    final_root = Path(os.environ.get('SYSTEM4_ACCEPTANCE_OUTPUT_DIR', '/tmp/system4-acceptance-output'))
    final_root.mkdir(parents=True, exist_ok=True)
    final_path = final_root / 'SYSTEM4_PARENT_TITLE_REPAIRED_WORDPRESS.json'
    final_path.write_bytes(reconstructed.read_bytes())
    if final_path.read_bytes() != reconstructed.read_bytes():
        raise AssertionError('PARENT_TITLE_FINAL_FILE_NOT_BYTE_EQUAL')

    proof = {
        'contract': 'SYSTEM4_REAL_PARENT_TITLE_REPAIR_ACCEPTANCE_V1',
        'status': 'PASS',
        'head': good_files['head'],
        'initial_error': 'BLOCKED_CONTENT_TITLE_COLON',
        'repair_owner': 'PARENT_TITLE_MACHINE',
        'return_route': 'PARENT_LAUNCH',
        'old_point0_sha256': old_point0_sha,
        'new_point0_sha256': v3.sha_bytes(good_files['point0'].read_bytes()),
        'old_point0_immutable': True,
        'bad_title': bad_title,
        'repaired_title': repaired_title,
        'real_languagetool_sha256': production_checks.LT_JAR_SHA256,
        'real_ppm_sha256': production_checks.PPM_PACKAGE_SHA256,
        'article_count': collected['article_count'],
        'handoff_parts': envelope['part_count'],
        'final_sha256': v3.sha_bytes(final_path.read_bytes()),
        'inline_byte_equal': True,
        'publish_allowed': False,
    }
    v3.write_json(final_root / 'SYSTEM4_REAL_PARENT_TITLE_REPAIR_ACCEPTANCE_V1.json', proof)
    print(json.dumps(proof, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
