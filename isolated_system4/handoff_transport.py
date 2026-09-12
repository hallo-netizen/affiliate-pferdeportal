#!/usr/bin/env python3
import argparse, base64, hashlib, json, re
from pathlib import Path

HANDOFF_CONTRACT='SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1'
TRANSPORT_CONTRACT='SYSTEM4_PARENT_CHAT_TRANSPORT_V1'
HANDOFF_FILENAME='SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json'
TRANSPORT_FILENAME='SYSTEM4_PARENT_CHAT_TRANSPORT_V1.json'
SHA_RE=re.compile(r'^[0-9a-f]{64}$')

class HandoffError(RuntimeError):
    pass

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def _require(cond: bool, code: str):
    if not cond:
        raise HandoffError(code)

def validate_handoff(payload: dict) -> dict:
    _require(isinstance(payload,dict),'HANDOFF_NOT_OBJECT')
    required={'contract','batch_sha256','publish_allowed','signing_deferred','batch_gate_status','no_legacy_status','test_suite_status','wordpress_review','articles'}
    _require(set(payload)==required,'HANDOFF_SCHEMA_INVALID')
    _require(payload['contract']==HANDOFF_CONTRACT,'HANDOFF_CONTRACT_INVALID')
    _require(isinstance(payload['batch_sha256'],str) and SHA_RE.fullmatch(payload['batch_sha256']) is not None,'HANDOFF_BATCH_SHA_INVALID')
    _require(payload['publish_allowed'] is False,'HANDOFF_PUBLISH_MUST_BE_FALSE')
    _require(payload['signing_deferred'] is True,'HANDOFF_SIGNING_DEFERRED_REQUIRED')
    _require(payload['batch_gate_status']=='SYSTEM4_BATCH_FULL_PASS_COLLECTED','HANDOFF_BATCH_GATE_NOT_PASS')
    _require(payload['no_legacy_status']=='PASS','HANDOFF_NO_LEGACY_NOT_PASS')
    _require(payload['test_suite_status']=='PASS','HANDOFF_TEST_SUITE_NOT_PASS')
    wr=payload['wordpress_review']
    _require(isinstance(wr,dict),'HANDOFF_WORDPRESS_REVIEW_INVALID')
    wr_required={'file_format','mime_type','intended_next_step','plugin_name','plugin_version_verified_against','ppm_version_verified_against','direct_wordpress_upload_ready','direct_upload_block_reason','required_downstream_components'}
    _require(set(wr)==wr_required,'HANDOFF_WORDPRESS_REVIEW_SCHEMA_INVALID')
    _require(wr['file_format']=='JSON' and wr['mime_type']=='application/json','HANDOFF_WORDPRESS_FORMAT_INVALID')
    _require(wr['intended_next_step']=='WORDPRESS_DIRECT_IMPORT','HANDOFF_WORDPRESS_NEXT_STEP_INVALID')
    _require(wr['plugin_name']=='Portal SEO Editorial Plan Compiler','HANDOFF_WORDPRESS_PLUGIN_INVALID')
    _require(wr['plugin_version_verified_against']=='0.28.22','HANDOFF_WORDPRESS_PLUGIN_VERSION_INVALID')
    _require(wr['ppm_version_verified_against']=='6.7.9','HANDOFF_WORDPRESS_PPM_VERSION_INVALID')
    _require(wr['direct_wordpress_upload_ready'] is True,'HANDOFF_WORDPRESS_DIRECT_UPLOAD_REQUIRED')
    _require(wr['direct_upload_block_reason'] is None,'HANDOFF_WORDPRESS_BLOCK_REASON_MUST_BE_EMPTY')
    _require(wr['required_downstream_components']==[],'HANDOFF_WORDPRESS_DOWNSTREAM_MUST_BE_EMPTY')
    rows=payload['articles']
    _require(isinstance(rows,list) and len(rows)==7,'HANDOFF_ARTICLE_COUNT_INVALID')
    seen=set()
    row_required={'index','title','target_keyword','category','article_type','plan_slot','final_draft_sha256','revision_count','body','production_context','languagetool','ppm679'}
    for i,row in enumerate(rows):
        _require(isinstance(row,dict) and set(row)==row_required,f'HANDOFF_ARTICLE_SCHEMA_INVALID:{i}')
        _require(row['index']==i,f'HANDOFF_ARTICLE_INDEX_INVALID:{i}')
        for field in ('title','target_keyword','category'):
            _require(isinstance(row[field],str) and row[field].strip()!='',f'HANDOFF_ARTICLE_FIELD_INVALID:{i}:{field}')
        _require(row['article_type']=='Beratung',f'HANDOFF_ARTICLE_TYPE_INVALID:{i}')
        slot=row['plan_slot']; _require(isinstance(slot,str) and SHA_RE.fullmatch(slot) is not None,f'HANDOFF_PLAN_SLOT_INVALID:{i}')
        _require(slot not in seen,f'HANDOFF_PLAN_SLOT_DUPLICATE:{i}'); seen.add(slot)
        body=row['body']; _require(isinstance(body,str) and body!='',f'HANDOFF_BODY_INVALID:{i}')
        body_sha=sha256_bytes(body.encode('utf-8'))
        _require(row['final_draft_sha256']==body_sha,f'HANDOFF_BODY_SHA_MISMATCH:{i}')
        _require(isinstance(row['revision_count'],int) and row['revision_count']>=1,f'HANDOFF_REVISION_INVALID:{i}')
        pc=row['production_context']; _require(isinstance(pc,dict) and isinstance(pc.get('fact_pack'),dict) and isinstance(pc.get('production_plan_item'),dict),f'HANDOFF_PRODUCTION_CONTEXT_INVALID:{i}')
        lt=row['languagetool']; _require(isinstance(lt,dict) and lt.get('status')=='PASS' and lt.get('finding_count')==0 and lt.get('engine')=='LanguageTool 6.8 / Bestand 43',f'HANDOFF_LT_NOT_PASS:{i}')
        ppm=row['ppm679']; _require(isinstance(ppm,dict) and ppm.get('status')=='PASS' and ppm.get('ppm_version')=='6.7.9' and ppm.get('technical_status')=='TECHNICAL_CHECK_OK' and ppm.get('content_quality_status')=='CONTENT_QUALITY_CHECK_OK' and ppm.get('fail_closed_aggregate_status')=='PASS' and ppm.get('content_sha256')==body_sha,f'HANDOFF_PPM_NOT_PASS:{i}')
    return payload

def read_validate_handoff(path: Path) -> tuple[dict,bytes]:
    raw=path.read_bytes()
    try:
        payload=json.loads(raw.decode('utf-8'))
    except Exception as exc:
        raise HandoffError('HANDOFF_JSON_INVALID') from exc
    validate_handoff(payload)
    return payload,raw

def pack(input_path: Path, output_path: Path) -> dict:
    _,raw=read_validate_handoff(input_path)
    env={
        'contract':TRANSPORT_CONTRACT,
        'filename':HANDOFF_FILENAME,
        'mime_type':'application/json',
        'byte_length':len(raw),
        'plaintext_sha256':sha256_bytes(raw),
        'payload_base64':base64.b64encode(raw).decode('ascii'),
        'publish_allowed':False,
    }
    output_path.write_text(json.dumps(env,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n',encoding='utf-8')
    return env

def unpack(transport_path: Path, output_dir: Path) -> Path:
    try:
        env=json.loads(transport_path.read_text(encoding='utf-8'))
    except Exception as exc:
        raise HandoffError('TRANSPORT_JSON_INVALID') from exc
    _require(isinstance(env,dict),'TRANSPORT_NOT_OBJECT')
    required={'contract','filename','mime_type','byte_length','plaintext_sha256','payload_base64','publish_allowed'}
    _require(set(env)==required,'TRANSPORT_SCHEMA_INVALID')
    _require(env['contract']==TRANSPORT_CONTRACT,'TRANSPORT_CONTRACT_INVALID')
    _require(env['filename']==HANDOFF_FILENAME and env['mime_type']=='application/json','TRANSPORT_TARGET_INVALID')
    _require(env['publish_allowed'] is False,'TRANSPORT_PUBLISH_MUST_BE_FALSE')
    _require(isinstance(env['byte_length'],int) and env['byte_length']>0,'TRANSPORT_LENGTH_INVALID')
    _require(isinstance(env['plaintext_sha256'],str) and SHA_RE.fullmatch(env['plaintext_sha256']) is not None,'TRANSPORT_SHA_INVALID')
    try:
        raw=base64.b64decode(env['payload_base64'],validate=True)
    except Exception as exc:
        raise HandoffError('TRANSPORT_BASE64_INVALID') from exc
    _require(len(raw)==env['byte_length'],'TRANSPORT_LENGTH_MISMATCH')
    _require(sha256_bytes(raw)==env['plaintext_sha256'],'TRANSPORT_SHA_MISMATCH')
    try:
        payload=json.loads(raw.decode('utf-8'))
    except Exception as exc:
        raise HandoffError('TRANSPORT_PAYLOAD_JSON_INVALID') from exc
    validate_handoff(payload)
    output_dir.mkdir(parents=True,exist_ok=True)
    out=output_dir/HANDOFF_FILENAME
    out.write_bytes(raw)
    _require(sha256_bytes(out.read_bytes())==env['plaintext_sha256'],'TRANSPORT_WRITTEN_SHA_MISMATCH')
    return out

def main(argv=None):
    p=argparse.ArgumentParser()
    sp=p.add_subparsers(dest='cmd',required=True)
    a=sp.add_parser('validate'); a.add_argument('handoff')
    a=sp.add_parser('pack'); a.add_argument('handoff'); a.add_argument('transport')
    a=sp.add_parser('unpack'); a.add_argument('transport'); a.add_argument('output_dir')
    ns=p.parse_args(argv)
    try:
        if ns.cmd=='validate':
            _,raw=read_validate_handoff(Path(ns.handoff)); print(json.dumps({'status':'SYSTEM4_HANDOFF_VALIDATE_PASS','sha256':sha256_bytes(raw)},separators=(',',':')))
        elif ns.cmd=='pack':
            env=pack(Path(ns.handoff),Path(ns.transport)); print(json.dumps({'status':'SYSTEM4_HANDOFF_PACK_PASS','sha256':env['plaintext_sha256'],'bytes':env['byte_length']},separators=(',',':')))
        else:
            out=unpack(Path(ns.transport),Path(ns.output_dir)); print(json.dumps({'status':'SYSTEM4_HANDOFF_UNPACK_PASS','file':str(out),'sha256':sha256_bytes(out.read_bytes())},separators=(',',':')))
        return 0
    except HandoffError as exc:
        print('SYSTEM4_HANDOFF_BLOCK:'+str(exc))
        return 2

if __name__=='__main__':
    raise SystemExit(main())
