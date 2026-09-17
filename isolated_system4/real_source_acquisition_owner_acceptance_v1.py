#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import full_local_acceptance as legacy
import machine_point0
import production_checks
import real_known_regression_acceptance_v3 as v3
import root_entry
import supervisor


class _Handler(BaseHTTPRequestHandler):
    sources: dict[str, dict] = {}

    def do_GET(self):
        if self.path == '/forbidden':
            self.send_response(403)
            self.end_headers()
            return
        key = self.path.lstrip('/')
        row = self.sources.get(key)
        if row is None:
            self.send_response(404)
            self.end_headers()
            return
        body = ('<html><head><title>' + row['source_title'] + '</title></head><body><main>' + row['evidence'] + '</main></body></html>').encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass


def _bind_machine_inputs(root: Path, raw: dict) -> dict:
    snapshot = json.loads(raw['snapshot'].read_text(encoding='utf-8'))
    snapshot['system4_root_manifest_sha256'] = root_entry._critical_manifest_sha256()
    snapshot = v3._bind_current_start(snapshot)
    snapshot_path = root / 'production_snapshot.bound.json'
    snapshot_path.write_bytes(json.dumps(snapshot, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8'))
    snapshot_sha = v3.sha_bytes(snapshot_path.read_bytes())

    plan = json.loads(raw['plan'].read_text(encoding='utf-8'))
    plan['source_snapshot_id'] = snapshot_sha
    quality = plan.get('quality_binding') if isinstance(plan.get('quality_binding'), dict) else None
    runtime = plan.get('runtime_order') if isinstance(plan.get('runtime_order'), dict) else None
    links = quality.get('link_bindings') if isinstance(quality, dict) else None
    if not isinstance(runtime, dict) or not isinstance(links, list) or not links:
        raise AssertionError('SOURCE_ACCEPTANCE_PREWRITE_LINK_INPUT_MISSING')
    runtime['links'] = copy.deepcopy(links)
    plan_path = v3.write_json(root / 'plan_item.bound.json', plan)

    article = snapshot['next_textmachine_metadata_batch']['items'][0]
    plans = {
        'contract': 'SYSTEM4_MACHINE_PREWRITE_PLAN_BATCH_V1',
        'item_count': 1,
        'items': [{
            'item_index': 0,
            'plan_slot': article['plan_slot'],
            'production_plan_item': plan,
        }],
    }
    plans_path = v3.write_json(root / 'prewrite_plans.json', plans)
    return {
        'snapshot': snapshot_path,
        'snapshot_sha': snapshot_sha,
        'plan': plan_path,
        'plans': plans_path,
        'article': article,
        'facts': raw['facts'],
        'final': raw['final'],
    }


def _source_request(article: dict, base: str, *, forbidden: bool) -> dict:
    rows = []
    for index, (sid, meta) in enumerate(legacy.SOURCES.items()):
        url = base + ('/forbidden' if forbidden and index == 0 else '/' + sid)
        rows.append({
            'source_id': sid,
            'source_title': meta['source_title'],
            'source_url': url,
            'source_kind': 'WEB',
        })
    return {
        'contract': 'SYSTEM4_MACHINE_SOURCE_REQUEST_BATCH_V1',
        'item_count': 1,
        'items': [{
            'item_index': 0,
            'plan_slot': article['plan_slot'],
            'sources': rows,
        }],
    }


def _pack_from_bound_research(raw_pack: Path, research: dict, snapshot_sha: str) -> dict:
    pack = json.loads(raw_pack.read_text(encoding='utf-8'))
    pack['source_snapshot_id'] = snapshot_sha
    pack['fact_pack_id'] = snapshot_sha
    pack['sources'] = copy.deepcopy(research['sources'])
    by_id = {row['source_id']: row for row in research['sources']}
    for claim in pack.get('claims', []):
        sid = claim['source_id']
        claim['source_url'] = by_id[sid]['source_url']
    for key in ('fact_pack_hash', 'source_manifest_hash', 'claim_register_hash'):
        pack.pop(key, None)
    return pack


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
    runtime = Path(tempfile.mkdtemp(prefix='system4-real-source-owner-v1-'))
    raw = legacy.build_fixture(runtime / 'fixture')
    bound = _bind_machine_inputs(runtime, raw)

    _Handler.sources = copy.deepcopy(legacy.SOURCES)
    server = ThreadingHTTPServer(('127.0.0.1', 0), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f'http://127.0.0.1:{server.server_address[1]}'
    try:
        bad_request = v3.write_json(runtime / 'source_request.bad.json', _source_request(bound['article'], base, forbidden=True))
        bad_point0 = runtime / 'point0.bad.json'
        failed = v3.run([
            sys.executable, str(v3.HERE / 'machine_point0.py'), 'build-fetch',
            str(bound['snapshot']), str(bad_request), str(bound['plans']), str(bad_point0),
            'SYSTEM4_REAL_SOURCE_HTTP_V1',
        ], 4, env)
        if 'SYSTEM4_SOURCE_OWNER_RETURN:SOURCE_ACQUISITION_MACHINE:SOURCE_ACQUISITION_STAGE:SOURCE_HTTP_FAIL:0:0:403' not in failed.stdout:
            raise AssertionError('REAL_SOURCE_OWNER_RETURN_NOT_OBSERVED:' + failed.stdout)
        if bad_point0.exists():
            raise AssertionError('POINT0_CREATED_AFTER_SOURCE_403')

        good_request = v3.write_json(runtime / 'source_request.good.json', _source_request(bound['article'], base, forbidden=False))
        point0 = runtime / 'point0.json'
        passed = v3.run([
            sys.executable, str(v3.HERE / 'machine_point0.py'), 'build-fetch',
            str(bound['snapshot']), str(good_request), str(bound['plans']), str(point0),
            'SYSTEM4_REAL_SOURCE_HTTP_V1',
        ], 0, env)
        if 'SYSTEM4_MACHINE_POINT0_PASS:' not in passed.stdout or not point0.is_file():
            raise AssertionError('REAL_SOURCE_REACQUISITION_POINT0_NOT_CREATED:' + passed.stdout)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)

    files = {
        'snapshot': bound['snapshot'],
        'plan': bound['plan'],
        'facts': bound['facts'],
        'final': bound['final'],
        'point0': point0,
        'head': os.popen(f'cd {v3.REPO} && git rev-parse --verify HEAD').read().strip(),
    }
    workspace = runtime / 'item-0'
    v3._start_real_pipeline(files, workspace, env)
    research = supervisor.expected_research_document(workspace)
    research_path = v3.write_json(runtime / 'research.supervisor-bound.json', research)
    v3.run([sys.executable, str(v3.CONTROLLER), 'research', str(workspace), str(research_path)], 0, env)
    v3.run([sys.executable, str(v3.CONTROLLER), 'facts', str(workspace), str(files['facts'])], 0, env)

    pack = _pack_from_bound_research(raw['pack'], research, bound['snapshot_sha'])
    pack_path = v3.write_json(runtime / 'fact_pack.source-bound.json', pack)
    v3.run([sys.executable, str(v3.CONTROLLER), 'context', str(workspace), str(pack_path), str(files['plan'])], 0, env)
    v3.run([sys.executable, str(v3.CONTROLLER), 'draft', str(workspace), str(files['final'])], 0, env)
    checked = v3.run([sys.executable, str(v3.CONTROLLER), 'fullcheck', str(workspace)], 0, env)
    if 'SYSTEM4_FULL_CHECK_PASS:OUTPUT_GATE_REQUIRED' not in checked.stdout:
        raise AssertionError('SOURCE_REACQUISITION_REAL_FULLCHECK_NOT_PASS:' + checked.stdout)

    state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
    evidence = state['checks']['production_evidence']['evidence']
    if evidence['languagetool']['status'] != 'PASS' or evidence['ppm679']['status'] != 'PASS':
        raise AssertionError('SOURCE_REACQUISITION_REAL_VALIDATORS_NOT_PASS')

    output = runtime / 'output'
    output.mkdir()
    collected, envelope, reconstructed = legacy.handoff_from_state(files, workspace / 'state.json', output)
    final_root = Path(os.environ.get('SYSTEM4_ACCEPTANCE_OUTPUT_DIR', '/tmp/system4-acceptance-output'))
    final_root.mkdir(parents=True, exist_ok=True)
    final_path = final_root / 'SYSTEM4_SOURCE_ACQUISITION_REPAIRED_WORDPRESS.json'
    final_path.write_bytes(reconstructed.read_bytes())
    if final_path.read_bytes() != reconstructed.read_bytes():
        raise AssertionError('SOURCE_OWNER_FINAL_FILE_NOT_BYTE_EQUAL')

    proof = {
        'contract': 'SYSTEM4_REAL_SOURCE_ACQUISITION_OWNER_ACCEPTANCE_V1',
        'status': 'PASS',
        'head': files['head'],
        'initial_error': 'SOURCE_HTTP_FAIL:0:0:403',
        'repair_owner': 'SOURCE_ACQUISITION_MACHINE',
        'return_route': 'SOURCE_ACQUISITION_STAGE',
        'point0_absent_after_failure': True,
        'point0_created_only_after_successful_reacquisition': True,
        'source_transport': 'REAL_LOCAL_HTTP_403_THEN_200',
        'real_languagetool_sha256': production_checks.LT_JAR_SHA256,
        'real_ppm_sha256': production_checks.PPM_PACKAGE_SHA256,
        'article_count': collected['article_count'],
        'handoff_parts': envelope['part_count'],
        'final_sha256': v3.sha_bytes(final_path.read_bytes()),
        'inline_byte_equal': True,
        'publish_allowed': False,
    }
    v3.write_json(final_root / 'SYSTEM4_REAL_SOURCE_ACQUISITION_OWNER_ACCEPTANCE_V1.json', proof)
    print(json.dumps(proof, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
