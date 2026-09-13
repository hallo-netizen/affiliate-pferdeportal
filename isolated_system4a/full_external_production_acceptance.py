#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent if HERE.name == 'isolated_system4a' else HERE
SYSTEM4 = REPO / 'isolated_system4'
for path in (str(HERE), str(SYSTEM4)):
    if path not in sys.path:
        sys.path.insert(0, path)

from external_host import ExternalHostError, ExternalSupervisorHost, PersistentArticleWorkerPool
from production_ingress import ProductionIngressError

IMPORT_BLOCKER = None
try:
    import handoff_transport
    import production_checks
    import full_local_acceptance as s4_accept
except Exception as exc:
    IMPORT_BLOCKER = 'SYSTEM4_REAL_DEPENDENCY_IMPORT_FAILED:' + str(exc)

WORKER_CONTRACT = 'SYSTEM4A_EXTERNAL_WORKER_SESSION_V2'


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def require(condition: bool, code: str) -> None:
    if not condition:
        raise RuntimeError(code)


def preflight() -> Path:
    require(IMPORT_BLOCKER is None, str(IMPORT_BLOCKER or 'IMPORT_OK'))
    require(os.geteuid() == 0, 'CROSS_UID_ROOT_REQUIRED')
    require(shutil.which('runuser') is not None, 'RUNUSER_REQUIRED')
    try:
        import pwd
        pwd.getpwnam('nobody')
    except Exception as exc:
        raise RuntimeError('WORKER_USER_NOBODY_REQUIRED') from exc
    jar = Path(os.environ.get('SYSTEM4_LANGUAGETOOL_JAR', ''))
    require(jar.is_file(), 'LANGUAGETOOL_JAR_MISSING')
    require(sha256_file(jar) == production_checks.LT_JAR_SHA256, 'LANGUAGETOOL_JAR_HASH_MISMATCH')
    ppm = REPO / production_checks.PPM_PACKAGE_REL
    require(ppm.is_file(), 'PPM679_PACKAGE_MISSING')
    require(sha256_file(ppm) == production_checks.PPM_PACKAGE_SHA256, 'PPM679_PACKAGE_HASH_MISMATCH')
    return jar


def chmod_fixture(files: dict[str, Path], root: Path) -> None:
    root.chmod(0o755)
    for path in files.values():
        if isinstance(path, Path) and path.exists():
            path.chmod(0o644)
    for path in root.rglob('*'):
        if path.is_dir():
            path.chmod(0o755)


def write_worker(script: Path, files: dict[str, Path], mode: str) -> None:
    paths = {key: str(value) for key, value in files.items() if isinstance(value, Path)}
    script.write_text(
        '''import json,sys\nfrom pathlib import Path\nMODE=%r\nFILES=%r\ndef read(name): return Path(FILES[name]).read_text(encoding="utf-8")\ndef content(req):\n    task=req["task"]\n    if task=="research":\n        if MODE=="bad-research": return "BAD_RESEARCH"\n        return read("research")\n    if task=="facts":\n        if MODE=="bad-facts": return "BAD_FACTS"\n        return read("facts")\n    if task=="context":\n        return json.dumps({"fact_pack":json.loads(read("pack")),"production_plan_item":json.loads(read("plan"))},ensure_ascii=False,sort_keys=True)\n    if task=="draft":\n        if MODE=="design-drift": return read("bad").replace("system-129-table ","",1)\n        return read("bad")\n    if task=="repair": return read("final")\n    raise RuntimeError("UNKNOWN_TASK:"+str(task))\nfor line in sys.stdin:\n    env=json.loads(line); req=env["request"]; sid=env["session_id"]; contract=env["contract"]\n    if MODE=="inject-pass":\n        response={"contract":contract,"session_id":sid,"result":{"content":"x","phase":"ARTICLE_PASS"}}\n    elif MODE=="fake-state":\n        Path("state.json").write_text("{\\\"phase\\\":\\\"ARTICLE_PASS\\\"}",encoding="utf-8")\n        response={"contract":contract,"session_id":sid,"result":{"content":content(req)}}\n    else:\n        response={"contract":contract,"session_id":sid,"result":{"content":content(req)}}\n    print(json.dumps(response,ensure_ascii=False),flush=True)\n''' % (mode, paths),
        encoding='utf-8',
    )
    script.chmod(0o755)


def make_pool(root: Path, files: dict[str, Path], mode: str = 'good', *, cross_uid: bool = True) -> PersistentArticleWorkerPool:
    root.mkdir(parents=True, exist_ok=True)
    source = root / ('private-worker-source-' + mode)
    source.mkdir(mode=0o700)
    source.chmod(0o700)
    script = source / ('worker-' + mode + '.py')
    write_worker(script, files, mode)
    if cross_uid:
        return PersistentArticleWorkerPool.from_python_bundle(
            source, script.name, run_as_user='nobody', runtime_processes=1, timeout_seconds=180.0
        )
    root.chmod(0o755)
    script.chmod(0o755)
    return PersistentArticleWorkerPool(
        [sys.executable, str(script)],
        root / ('workers-' + mode),
        runtime_processes=1,
        timeout_seconds=180.0,
    )


def build_fixture(root: Path) -> dict[str, Path]:
    files = s4_accept.build_fixture(root)
    expected_bound = root / 'expected-system4-bound-snapshot.json'
    expected_bound.write_bytes(files['snapshot'].read_bytes())
    value = json.loads(files['snapshot'].read_text(encoding='utf-8'))
    manifest = value.pop('system4_root_manifest_sha256', None)
    require(isinstance(manifest, str) and len(manifest) == 64, 'SYSTEM4_FIXTURE_MANIFEST_MISSING')
    external = root / 'external-business-input.json'
    external.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')), encoding='utf-8')
    files['expected_bound_snapshot'] = expected_bound
    files['snapshot'] = external
    chmod_fixture(files, root)
    return files


def positive_real(root: Path, files: dict[str, Path]) -> dict[str, object]:
    out = root / 'SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json'
    parent = root / 'parent-chat'
    authority = root / 'supervisor-authority'
    host = ExternalSupervisorHost(mode='production', authority_root=authority)
    result = host.run_production(files['snapshot'], make_pool(root, files), out, parent)
    require(result['status'] == 'SYSTEM4A_EXTERNAL_HOST_PRODUCTION_PASS', 'PRODUCTION_STATUS_NOT_PASS')
    require(out.is_file(), 'HANDOFF_OUTPUT_MISSING')
    rebuilt = parent / handoff_transport.HANDOFF_FILENAME
    require(rebuilt.is_file(), 'PARENT_CHAT_REBUILT_OUTPUT_MISSING')
    require(rebuilt.read_bytes() == out.read_bytes(), 'PARENT_CHAT_BYTES_MISMATCH')
    require(result['ingress']['bound_snapshot_sha256'] == sha256_file(files['expected_bound_snapshot']), 'SUPERVISOR_BOUND_SNAPSHOT_NOT_SYSTEM4_IDENTICAL')
    bound_files = list((authority / 'ingress').glob('*.json'))
    require(len(bound_files) == 1, 'SUPERVISOR_BOUND_SNAPSHOT_COUNT_INVALID')
    require(bound_files[0].read_bytes() == files['expected_bound_snapshot'].read_bytes(), 'SUPERVISOR_BOUND_SNAPSHOT_BYTES_CHANGED')
    payload, raw = handoff_transport.read_validate_handoff(out)
    require(len(payload['articles']) == 1, 'ARTICLE_COUNT_NOT_ONE')
    row = payload['articles'][0]
    require(row['revision_count'] == 2, 'SAME_ARTICLE_REPAIR_REVISION_NOT_TWO')
    require(row['body'] == files['final'].read_text(encoding='utf-8'), 'FINAL_BODY_NOT_REPAIRED_FIXTURE')
    lt = row['languagetool']; ppm = row['ppm679']
    require(lt.get('status') == 'PASS', 'REAL_LT_NOT_PASS')
    require(lt.get('engine') == production_checks.LT_ENGINE, 'REAL_LT_ENGINE_MISMATCH')
    require(lt.get('commandline_jar_sha256') == production_checks.LT_JAR_SHA256, 'REAL_LT_JAR_HASH_MISMATCH')
    require(lt.get('finding_count') == 0, 'REAL_LT_FINDINGS_REMAIN')
    require(ppm.get('status') == 'PASS', 'REAL_PPM_NOT_PASS')
    require(ppm.get('ppm_version') == production_checks.PPM_VERSION, 'REAL_PPM_VERSION_MISMATCH')
    require(ppm.get('ppm_package_sha256') == production_checks.PPM_PACKAGE_SHA256, 'REAL_PPM_PACKAGE_HASH_MISMATCH')
    require(ppm.get('content_sha256') == hashlib.sha256(row['body'].encode('utf-8')).hexdigest(), 'REAL_PPM_CONTENT_HASH_MISMATCH')
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw), 'revision': row['revision_count']}


def expect_block(root: Path, files: dict[str, Path], mode: str, expected: str) -> None:
    out = root / ('blocked-' + mode + '.json')
    host = ExternalSupervisorHost(mode='production', authority_root=root / 'supervisor-authority')
    try:
        host.run_production(files['snapshot'], make_pool(root, files, mode), out, root / ('parent-' + mode))
    except Exception as exc:
        require(expected in str(exc), 'WRONG_BLOCKER:' + mode + ':' + str(exc))
        require(not out.exists(), 'BLOCKED_CASE_CREATED_OUTPUT:' + mode)
        return
    raise RuntimeError('NEGATIVE_CASE_DID_NOT_BLOCK:' + mode)


def negative_same_uid(root: Path, files: dict[str, Path]) -> None:
    out = root / 'same-user-must-not-output.json'
    host = ExternalSupervisorHost(mode='production', authority_root=root / 'supervisor-authority')
    pool = make_pool(root, files, 'good', cross_uid=False)
    try:
        host.run_production(files['snapshot'], pool, out, root / 'parent-same-user')
    except ExternalHostError as exc:
        require('PRODUCTION_CROSS_UID_BOUNDARY_REQUIRED' in str(exc), 'SAME_UID_WRONG_BLOCKER')
        require(not out.exists(), 'SAME_UID_CREATED_OUTPUT')
        pool.close()
        return
    pool.close()
    raise RuntimeError('SAME_UID_DID_NOT_BLOCK')


def negative_external_manifest_injection(root: Path, files: dict[str, Path]) -> None:
    value = json.loads(files['snapshot'].read_text(encoding='utf-8'))
    value['system4_root_manifest_sha256'] = '0' * 64
    injected = root / 'external-with-forbidden-control.json'
    injected.parent.mkdir(parents=True, exist_ok=True)
    injected.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')), encoding='utf-8')
    out = root / 'must-not-output.json'
    pool = make_pool(root, files)
    host = ExternalSupervisorHost(mode='production', authority_root=root / 'supervisor-authority')
    try:
        host.run_production(injected, pool, out, root / 'parent')
    except ProductionIngressError as exc:
        require('EXTERNAL_CONTROL_FIELD_FORBIDDEN' in str(exc), 'EXTERNAL_MANIFEST_WRONG_BLOCKER')
        require(pool.runtime_pids() == [], 'EXTERNAL_MANIFEST_STARTED_WORKER')
        require(not out.exists(), 'EXTERNAL_MANIFEST_CREATED_OUTPUT')
        pool.close()
        return
    pool.close()
    raise RuntimeError('EXTERNAL_MANIFEST_INJECTION_DID_NOT_BLOCK')


def negative_cross_uid_worker_path_permission(root: Path, files: dict[str, Path]) -> None:
    root.mkdir(parents=True, exist_ok=True)
    private = root / 'codex-private'
    private.mkdir(mode=0o700)
    worker = private / 'worker.py'
    write_worker(worker, files, 'good')
    out = root / 'must-not-output.json'
    pool = PersistentArticleWorkerPool(
        [sys.executable, str(worker)],
        private / 'workers',
        run_as_user='nobody',
        require_cross_uid=True,
        runtime_processes=1,
        timeout_seconds=30.0,
    )
    host = ExternalSupervisorHost(mode='production', authority_root=root / 'supervisor-authority')
    try:
        host.run_production(files['snapshot'], pool, out, root / 'parent')
    except ExternalHostError as exc:
        require('WORKER_COMMAND_PATH_NOT_ACCESSIBLE:' in str(exc), 'WORKER_PERMISSION_WRONG_BLOCKER:' + str(exc))
        require(not out.exists(), 'WORKER_PERMISSION_CREATED_OUTPUT')
        pool.close()
        return
    pool.close()
    raise RuntimeError('WORKER_PERMISSION_DID_NOT_BLOCK')

def negative_parent_tamper(root: Path, good_inline: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    tampered = root / 'tampered-inline.txt'
    lines = good_inline.read_text(encoding='utf-8').splitlines()
    require(len(lines) >= 3, 'INLINE_EMPTY')
    row = json.loads(lines[1])
    payload = row.get('payload_base64')
    require(isinstance(payload, str) and payload, 'INLINE_PAYLOAD_EMPTY')
    row['payload_base64'] = ('A' if payload[0] != 'A' else 'B') + payload[1:]
    lines[1] = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    tampered.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    try:
        handoff_transport.inline_unpack(tampered, root / 'tampered-parent')
    except Exception:
        return
    raise RuntimeError('PARENT_CHAT_TAMPER_NOT_BLOCKED')


def main() -> int:
    try:
        jar = preflight()
    except Exception as exc:
        print('SYSTEM4A_PRODUCTION_ACCEPTANCE_BLOCKED:' + str(exc))
        return 3
    os.environ['SYSTEM4_LANGUAGETOOL_JAR'] = str(jar)
    results: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix='system4a-real-production-') as td:
        root = Path(td); root.chmod(0o755)
        files = build_fixture(root / 'fixture')
        pos = positive_real(root / 'positive', files)
        results.append({'case':'POS_EXTERNAL_INPUT_AUTO_BIND_REAL_LT_PPM_REPAIR_TO_PARENT_CHAT','status':'PASS',**pos})

        negative_same_uid(root / 'neg-same-uid', files)
        results.append({'case':'NEG_SAME_UID_AUTHORITY','status':'PASS'})

        negative_external_manifest_injection(root / 'neg-external-manifest', files)
        results.append({'case':'NEG_EXTERNAL_CONTROL_MANIFEST','status':'PASS'})

        negative_cross_uid_worker_path_permission(root / 'neg-worker-permission', files)
        results.append({'case':'NEG_CROSS_UID_WORKER_PATH_PERMISSION','status':'PASS'})

        expect_block(root / 'neg-pass-injection', files, 'inject-pass', 'WORKER_RESULT_SCHEMA_INVALID')
        results.append({'case':'NEG_WORKER_PASS_INJECTION','status':'PASS'})

        expect_block(root / 'neg-fake-state', files, 'fake-state', 'WORKER_AUTHORITY_FILE_FORBIDDEN:state.json')
        results.append({'case':'NEG_WORKER_FAKE_STATE','status':'PASS'})

        expect_block(root / 'neg-research', files, 'bad-research', 'RESEARCH_BLOCK')
        results.append({'case':'NEG_RESEARCH','status':'PASS'})

        expect_block(root / 'neg-facts', files, 'bad-facts', 'FACTS_BLOCK')
        results.append({'case':'NEG_FACTS','status':'PASS'})

        expect_block(root / 'neg-design', files, 'design-drift', 'DRAFT_DESIGN_BLOCK')
        results.append({'case':'NEG_DESIGN','status':'PASS'})

        good_inline = root / 'positive' / getattr(handoff_transport, 'INLINE_FILENAME', 'SYSTEM4_PARENT_CHAT_INLINE_V2.txt')
        negative_parent_tamper(root / 'neg-parent-tamper', good_inline)
        results.append({'case':'NEG_PARENT_CHAT_TAMPER','status':'PASS'})

    print(json.dumps({
        'status':'SYSTEM4A_FULL_EXTERNAL_PRODUCTION_ACCEPTANCE_PASS',
        'case_count':len(results),
        'passed':len(results),
        'mocks_used':False,
        'real_languagetool':True,
        'real_ppm679':True,
        'supervisor_owns_manifest_binding':True,
        'symbolic_branch_required':False,
        'publish_allowed':False,
        'cases':results,
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())