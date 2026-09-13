from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from realcase_production_entry import run_realcase

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
DEFAULT_CONTRACT = HERE / 'NO_CODEX_PRODUCTION_CONTRACT_V1.json'
PPM_REL = 'control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip'
PARENT_NAME = 'SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json'
INLINE_NAME = 'SYSTEM4_PARENT_CHAT_INLINE_V2.txt'


class ContractError(RuntimeError):
    pass


def req(ok: bool, code: str) -> None:
    if not ok:
        raise ContractError(code)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(Path(path).read_bytes())


def stable(value: Any) -> str:
    return sha256_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8'))


def load_contract(path: Path = DEFAULT_CONTRACT) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding='utf-8'))
    req(value.get('contract') == 'SYSTEM4A_NO_CODEX_PRODUCTION_CONTRACT_V1', 'CONTRACT_ID_INVALID')
    req(value.get('codex_allowed') is False, 'CODEX_MUST_BE_DISABLED')
    return value


def verify_contract_sources(contract: dict[str, Any], *, lt_jar: Path) -> None:
    for rel, expected in contract['production_source_sha256'].items():
        path = REPO / rel
        req(path.is_file(), 'SOURCE_MISSING:' + rel)
        req(sha256_file(path) == expected, 'SOURCE_SHA_MISMATCH:' + rel)
    inp = REPO / contract['input']['path']
    worker = REPO / contract['worker']['path']
    req(inp.is_file() and inp.stat().st_size == contract['input']['bytes'], 'INPUT_FILE_INVALID')
    req(sha256_file(inp) == contract['input']['sha256'], 'INPUT_SHA_MISMATCH')
    req(worker.is_file() and worker.stat().st_size == contract['worker']['bytes'], 'WORKER_FILE_INVALID')
    req(sha256_file(worker) == contract['worker']['sha256'], 'WORKER_SHA_MISMATCH')
    req(lt_jar.is_file(), 'LT_JAR_MISSING')
    req(sha256_file(lt_jar) == contract['dependencies']['languagetool_6_8_sha256'], 'LT_JAR_SHA_MISMATCH')
    ppm = REPO / PPM_REL
    req(ppm.is_file(), 'PPM_PACKAGE_MISSING')
    req(sha256_file(ppm) == contract['dependencies']['ppm_6_7_9_sha256'], 'PPM_PACKAGE_SHA_MISMATCH')
    wanted = {
        'portal-ist-export-20260710-read-only.json':'ppm_wp_snapshot_sha256',
        'canonical-complete-editorial-plan-v1.json':'ppm_editorial_plan_sha256',
        'complete-portal-category-source-v1.json':'ppm_category_source_sha256',
        'article-type-templates.json':'ppm_article_type_templates_sha256',
    }
    with zipfile.ZipFile(ppm) as zf:
        names = zf.namelist()
        for suffix, key in wanted.items():
            hits = [name for name in names if name.endswith(suffix)]
            req(len(hits) == 1, 'PPM_INNER_SOURCE_RESOLUTION_INVALID:' + suffix)
            req(sha256_bytes(zf.read(hits[0])) == contract['dependencies'][key], 'PPM_INNER_SOURCE_SHA_MISMATCH:' + suffix)


def verify_output(contract: dict[str, Any], root: Path) -> dict[str, Any]:
    out = root / 'output.json'
    parent = root / 'parent-chat' / PARENT_NAME
    inline = root / INLINE_NAME
    req(out.is_file(), 'OUTPUT_MISSING')
    req(parent.is_file(), 'PARENT_HANDOFF_MISSING')
    req(inline.is_file(), 'INLINE_HANDOFF_MISSING')
    raw = out.read_bytes()
    req(len(raw) == contract['expected']['output_bytes'], 'OUTPUT_BYTES_MISMATCH')
    req(sha256_bytes(raw) == contract['expected']['output_sha256'], 'OUTPUT_SHA_MISMATCH')
    req(parent.read_bytes() == raw, 'PARENT_BYTE_MISMATCH')
    req(sha256_file(inline) == contract['expected']['inline_sha256'], 'INLINE_SHA_MISMATCH')
    value = json.loads(raw)
    req(value.get('batch_sha256') == contract['expected']['batch_sha256'], 'BATCH_FIELD_MISMATCH')
    rows = value.get('articles')
    req(isinstance(rows, list) and len(rows) == 1, 'ARTICLE_COUNT_MISMATCH')
    row = rows[0]
    req(row.get('revision_count') == contract['expected']['revision_count'], 'REVISION_FIELD_MISMATCH')
    for key, expected in contract['expected']['article_identity'].items():
        req(row.get(key) == expected, 'ARTICLE_FIELD_MISMATCH:' + key)
    ctx = row.get('production_context') or {}
    req(stable(ctx.get('fact_pack')) == contract['expected']['fact_pack_stable_sha256'], 'FACT_PACK_FIELD_MISMATCH')
    req(stable(ctx.get('production_plan_item')) == contract['expected']['production_plan_stable_sha256'], 'PRODUCTION_PLAN_FIELD_MISMATCH')
    plan = ctx.get('production_plan_item') or {}
    req(plan.get('quality_binding_hash') == contract['expected']['quality_binding_sha256'], 'QUALITY_BINDING_FIELD_MISMATCH')
    req(row.get('languagetool', {}).get('status') == contract['expected']['lt_status'], 'LT_STATUS_MISMATCH')
    req(row.get('ppm679', {}).get('status') == contract['expected']['ppm_status'], 'PPM_STATUS_MISMATCH')
    return value


def run_once(contract: dict[str, Any], run_root: Path, *, lt_jar: Path, input_bytes: bytes | None = None, worker_bytes: bytes | None = None) -> dict[str, Any]:
    shutil.rmtree(run_root, ignore_errors=True)
    (run_root / 'worker-src').mkdir(parents=True)
    (run_root / 'runtime').mkdir(parents=True)
    os.chmod(run_root, 0o755); os.chmod(run_root / 'worker-src', 0o755); os.chmod(run_root / 'runtime', 0o755)
    source_input = (REPO / contract['input']['path']).read_bytes() if input_bytes is None else input_bytes
    source_worker = (REPO / contract['worker']['path']).read_bytes() if worker_bytes is None else worker_bytes
    (run_root / 'external.json').write_bytes(source_input)
    worker = run_root / 'worker-src' / 'worker.py'; worker.write_bytes(source_worker); os.chmod(worker, 0o755)
    old = os.environ.get('SYSTEM4_LANGUAGETOOL_JAR')
    os.environ['SYSTEM4_LANGUAGETOOL_JAR'] = str(lt_jar)
    try:
        result = run_realcase(
            external_input=run_root/'external.json',
            worker_source=run_root/'worker-src',
            worker_entrypoint='worker.py',
            runtime_parent=run_root/'runtime',
            authority_root=run_root/'authority',
            output=run_root/'output.json',
            parent_chat_dir=run_root/'parent-chat',
            timeout_seconds=180.0,
        )
    finally:
        if old is None: os.environ.pop('SYSTEM4_LANGUAGETOOL_JAR', None)
        else: os.environ['SYSTEM4_LANGUAGETOOL_JAR'] = old
    value = verify_output(contract, run_root)
    return {'result':result,'value':value,'root':str(run_root)}


def negative_suite(contract: dict[str, Any], base: Path, lt_jar: Path, proof_root: Path) -> list[dict[str, Any]]:
    rows=[]
    original=json.loads((REPO/contract['input']['path']).read_text(encoding='utf-8'))
    mutated=copy.deepcopy(original); mutated['next_textmachine_metadata_batch']['items'][0]['plan_slot']='0'*64
    try:
        run_once(contract, base/'neg-plan-slot', lt_jar=lt_jar, input_bytes=json.dumps(mutated,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
        raise ContractError('NEG_PLAN_SLOT_ACCEPTED')
    except Exception as exc:
        req('PPM679_PLAN_SLOT_HASH_MISMATCH' in str(exc), 'NEG_PLAN_SLOT_WRONG_BLOCKER:' + str(exc)); rows.append({'case':'NEG_PLAN_SLOT','status':'PASS'})
    mutated=copy.deepcopy(original); mutated['next_textmachine_metadata_batch']['items'][0]['category']='pferdeanhaenger-beratung'
    try:
        run_once(contract, base/'neg-category', lt_jar=lt_jar, input_bytes=json.dumps(mutated,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
        raise ContractError('NEG_CATEGORY_ACCEPTED')
    except Exception as exc:
        req('PPM679_CATEGORY_NOT_CANONICAL' in str(exc), 'NEG_CATEGORY_WRONG_BLOCKER:' + str(exc)); rows.append({'case':'NEG_CATEGORY','status':'PASS'})
    worker=(REPO/contract['worker']['path']).read_bytes(); req(sha256_bytes(worker)!=sha256_bytes(worker+b'\n#tamper\n'),'NEG_WORKER_MUTATION_INVALID')
    tampered=copy.deepcopy(contract); tampered['worker']['sha256']=sha256_bytes(worker+b'\n#tamper\n')
    try:
        verify_contract_sources(tampered,lt_jar=lt_jar); raise ContractError('NEG_WORKER_FINGERPRINT_ACCEPTED')
    except ContractError as exc:
        req(str(exc)=='WORKER_SHA_MISMATCH','NEG_WORKER_WRONG_BLOCKER:'+str(exc)); rows.append({'case':'NEG_WORKER_BYTES','status':'PASS'})
    proof=base/'neg-output-tamper'; shutil.rmtree(proof, ignore_errors=True); shutil.copytree(proof_root, proof)
    p=proof/'output.json'; b=bytearray(p.read_bytes()); b[-2]=b[-2]^1; p.write_bytes(bytes(b))
    try:
        verify_output(contract,proof); raise ContractError('NEG_OUTPUT_TAMPER_ACCEPTED')
    except ContractError as exc:
        req(str(exc) in {'OUTPUT_SHA_MISMATCH','OUTPUT_BYTES_MISMATCH'},'NEG_OUTPUT_WRONG_BLOCKER:'+str(exc)); rows.append({'case':'NEG_OUTPUT_TAMPER','status':'PASS'})
    proof=base/'neg-parent-tamper'; shutil.rmtree(proof, ignore_errors=True); shutil.copytree(proof_root, proof)
    p=proof/'parent-chat'/PARENT_NAME; p.write_bytes(p.read_bytes()+b' ')
    try:
        verify_output(contract,proof); raise ContractError('NEG_PARENT_TAMPER_ACCEPTED')
    except ContractError as exc:
        req(str(exc)=='PARENT_BYTE_MISMATCH','NEG_PARENT_WRONG_BLOCKER:'+str(exc)); rows.append({'case':'NEG_PARENT_TAMPER','status':'PASS'})
    return rows


def double_proof(contract: dict[str, Any], base: Path, lt_jar: Path) -> dict[str, Any]:
    a=run_once(contract,base/'A',lt_jar=lt_jar)
    b=run_once(contract,base/'B',lt_jar=lt_jar)
    pa=Path(a['root'])/'output.json'; pb=Path(b['root'])/'output.json'
    req(pa.read_bytes()==pb.read_bytes(),'DOUBLE_PROOF_BYTE_MISMATCH')
    req(a['value']==b['value'],'DOUBLE_PROOF_FIELD_MISMATCH')
    neg=negative_suite(contract,base/'negative',lt_jar,Path(a['root']))
    return {
        'status':'SYSTEM4A_NO_CODEX_PRODUCTION_CONTRACT_PASS',
        'byte_equal':True,
        'field_equal':True,
        'output_sha256':sha256_file(pa),
        'output_bytes':pa.stat().st_size,
        'negative_cases':neg,
        'negative_passed':len(neg),
        'codex_used':False,
        'publish_allowed':False,
    }


def main(argv: list[str] | None=None) -> int:
    p=argparse.ArgumentParser(); p.add_argument('--contract',default=str(DEFAULT_CONTRACT)); p.add_argument('--lt-jar',required=True); p.add_argument('--work-root',default='/tmp/system4a-no-codex-contract-proof')
    args=p.parse_args(argv)
    contract=load_contract(Path(args.contract)); lt=Path(args.lt_jar)
    verify_contract_sources(contract,lt_jar=lt)
    result=double_proof(contract,Path(args.work_root),lt)
    print(json.dumps(result,ensure_ascii=False,sort_keys=True))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
