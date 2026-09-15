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

    v3.run([sys.executable, str(v3.CONTROLLER), 'draft', str(workspace), str(broken_path)], 0, env)
    first = v3.run([sys.executable, str(v3.CONTROLLER), 'fullcheck', str(workspace)], {3, 4}, env)
    state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
    findings = state.get('checks', {}).get('findings')
    if not isinstance(findings, list) or not findings:
        raise AssertionError('REAL_LINK_FINDING_MISSING:' + first.stdout)
    owners = sorted({str(row.get('repair_owner') or '') for row in findings if isinstance(row, dict)})
    codes = sorted({str(row.get('error_code') or '') for row in findings if isinstance(row, dict)})
    fields = sorted({str(row.get('field_path') or '') for row in findings if isinstance(row, dict)})

    # The machine-bound plan is unchanged and valid. The defect was introduced only in the
    # written article, so the producing owner must be DRAFT_WORKER, not the portal-link planner.
    if state.get('checks', {}).get('repair_owner') != 'DRAFT_WORKER' or first.returncode != 3:
        raise AssertionError('LINK_REALIZATION_MUST_RETURN_DRAFT_WORKER:' + json.dumps({
            'rc': first.returncode, 'owners': owners, 'codes': codes, 'fields': fields, 'stdout': first.stdout
        }, ensure_ascii=False, sort_keys=True))

    v3.run([sys.executable, str(v3.CONTROLLER), 'repair', str(workspace), str(files['final'])], 0, env)
    second = v3.run([sys.executable, str(v3.CONTROLLER), 'fullcheck', str(workspace)], 0, env)
    if 'SYSTEM4_FULL_CHECK_PASS:OUTPUT_GATE_REQUIRED' not in second.stdout:
        raise AssertionError('LINK_REALIZATION_REPAIR_NOT_PASS:' + second.stdout)

    output = runtime / 'output'; output.mkdir()
    collected, envelope, reconstructed = legacy.handoff_from_state(files, workspace / 'state.json', output)
    final_root = Path(os.environ.get('SYSTEM4_ACCEPTANCE_OUTPUT_DIR', '/tmp/system4-acceptance-output'))
    final_root.mkdir(parents=True, exist_ok=True)
    final_path = final_root / 'SYSTEM4_PORTAL_LINK_REALIZATION_REPAIRED_WORDPRESS.json'
    final_path.write_bytes(reconstructed.read_bytes())
    if final_path.read_bytes() != reconstructed.read_bytes():
        raise AssertionError('LINK_OWNER_FINAL_FILE_NOT_BYTE_EQUAL')

    proof = {
        'contract': 'SYSTEM4_REAL_PORTAL_LINK_OWNER_ACCEPTANCE_V1',
        'status': 'PASS',
        'head': files['head'],
        'defect_class': 'BOUND_LINK_REALIZATION_DRIFT_IN_DRAFT',
        'repair_owner': 'DRAFT_WORKER',
        'portal_link_machine_policy': 'ONLY_BOUND_LINK_SELECTION_OR_UPSTREAM_PLAN_DEFECT',
        'ppm_error_codes': codes,
        'ppm_field_paths': fields,
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
