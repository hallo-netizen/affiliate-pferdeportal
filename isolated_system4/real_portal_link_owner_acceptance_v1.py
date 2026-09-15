#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

import full_local_acceptance as legacy
import production_checks
import real_known_regression_acceptance_v3 as v3


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
    runtime = Path(tempfile.mkdtemp(prefix='system4-real-link-owner-v1-'))
    raw = legacy.build_fixture(runtime / 'fixture')
    files = v3._prepare_point0(runtime, raw)
    workspace = runtime / 'item-0'
    v3._stage_to_draft(files, workspace, env)

    plan = json.loads(files['plan'].read_text(encoding='utf-8'))
    quality = plan['quality_binding']
    links = quality['link_bindings']
    if not isinstance(links, list) or not links:
        raise AssertionError('BOUND_LINKS_MISSING')
    href = str(links[0]['href'])
    final_html = files['final'].read_text(encoding='utf-8')
    if href not in final_html:
        raise AssertionError('BOUND_LINK_NOT_REALIZED_IN_BASELINE:' + href)
    broken_html = final_html.replace(href, '/__system4_wrong_internal_link__', 1)
    broken_path = runtime / 'article_link_drift.html'
    broken_path.write_text(broken_html, encoding='utf-8')

    state_path = workspace / 'state.json'
    before = state_path.read_bytes()
    first = v3.run([sys.executable, str(v3.CONTROLLER), 'draft', str(workspace), str(broken_path)], 4, env)
    if 'SYSTEM4_STAGE_OWNER_RETURN:DRAFT_WORKER:DRAFT_STAGE:ARTICLE_AUTHORING_CONTRACT_FAIL:PREWRITE_BOUND_LINK_MISSING:' not in first.stdout:
        raise AssertionError('LINK_REALIZATION_WRONG_DRAFT_OWNER_RETURN:' + first.stdout)
    if state_path.read_bytes() != before:
        raise AssertionError('LINK_REALIZATION_REJECT_MUTATED_STATE')
    rejected_state = json.loads(state_path.read_text(encoding='utf-8'))
    if rejected_state.get('phase') != 'DRAFT_REQUIRED' or rejected_state.get('draft_markdown') is not None:
        raise AssertionError('LINK_REALIZATION_BAD_DRAFT_WAS_ACCEPTED')

    # Same producing stage resubmits the corrected article. The invalid candidate was never
    # accepted, therefore this is a fresh draft submission, not a same-article repair command.
    accepted = v3.run([sys.executable, str(v3.CONTROLLER), 'draft', str(workspace), str(files['final'])], 0, env)
    if 'SYSTEM4_DRAFT_ACCEPTED:REVISION=1:CHECK_REQUIRED' not in accepted.stdout:
        raise AssertionError('LINK_REALIZATION_CORRECT_DRAFT_NOT_ACCEPTED:' + accepted.stdout)
    second = v3.run([sys.executable, str(v3.CONTROLLER), 'fullcheck', str(workspace)], 0, env)
    if 'SYSTEM4_FULL_CHECK_PASS:OUTPUT_GATE_REQUIRED' not in second.stdout:
        raise AssertionError('LINK_REALIZATION_RECHECK_NOT_PASS:' + second.stdout)

    output = runtime / 'output'; output.mkdir()
    collected, envelope, reconstructed = legacy.handoff_from_state(files, state_path, output)
    final_root = Path(os.environ.get('SYSTEM4_ACCEPTANCE_OUTPUT_DIR', '/tmp/system4-acceptance-output'))
    final_root.mkdir(parents=True, exist_ok=True)
    final_path = final_root / 'SYSTEM4_PORTAL_LINK_REALIZATION_REPAIRED_WORDPRESS.json'
    final_path.write_bytes(reconstructed.read_bytes())
    if final_path.read_bytes() != reconstructed.read_bytes():
        raise AssertionError('LINK_OWNER_FINAL_FILE_NOT_BYTE_EQUAL')

    state = json.loads(state_path.read_text(encoding='utf-8'))
    proof = {
        'contract': 'SYSTEM4_REAL_PORTAL_LINK_OWNER_ACCEPTANCE_V1',
        'status': 'PASS',
        'head': files['head'],
        'defect_class': 'BOUND_LINK_REALIZATION_DRIFT_IN_DRAFT',
        'detected_by': 'AUTHORING_CONTRACT_BEFORE_DRAFT_ACCEPTANCE',
        'repair_owner': 'DRAFT_WORKER',
        'return_route': 'DRAFT_STAGE',
        'invalid_draft_never_accepted': True,
        'state_frozen_on_return': True,
        'portal_link_machine_policy': 'ONLY_BOUND_LINK_SELECTION_OR_UPSTREAM_PLAN_DEFECT',
        'revision': state['revision'],
        'article_count': collected['article_count'],
        'handoff_parts': envelope['part_count'],
        'final_sha256': v3.sha_bytes(final_path.read_bytes()),
        'inline_byte_equal': True,
        'publish_allowed': False,
    }
    v3.write_json(final_root / 'SYSTEM4_REAL_PORTAL_LINK_OWNER_ACCEPTANCE_V1.json', proof)
    print(json.dumps(proof, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
