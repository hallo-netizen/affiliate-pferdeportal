#!/usr/bin/env python3
import argparse, base64, hashlib, json, lzma, re
from pathlib import Path

import content_guard

HANDOFF_CONTRACT='SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1'
INLINE_CONTRACT='SYSTEM4_PARENT_CHAT_INLINE_V1'
HANDOFF_FILENAME='SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json'
INLINE_FILENAME='SYSTEM4_PARENT_CHAT_INLINE_V1.txt'
INLINE_BEGIN='SYSTEM4_PARENT_CHAT_INLINE_V1_BEGIN'
INLINE_END='SYSTEM4_PARENT_CHAT_INLINE_V1_END'
INLINE_MAX_CHARS=60000
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
    seen=set(); bodies=[]
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
        try:
            content_guard.validate_single_article(body,pc['fact_pack'])
        except content_guard.ContentGuardError as exc:
            raise HandoffError(f'HANDOFF_CONTENT_GUARD:{i}:'+str(exc)) from exc
        lt=row['languagetool']; _require(isinstance(lt,dict) and lt.get('status')=='PASS' and lt.get('finding_count')==0 and lt.get('engine')=='LanguageTool 6.8 / Bestand 43',f'HANDOFF_LT_NOT_PASS:{i}')
        ppm=row['ppm679']; _require(isinstance(ppm,dict) and ppm.get('status')=='PASS' and ppm.get('ppm_version')=='6.7.9' and ppm.get('technical_status')=='TECHNICAL_CHECK_OK' and ppm.get('content_quality_status')=='CONTENT_QUALITY_CHECK_OK' and ppm.get('fail_closed_aggregate_status')=='PASS' and ppm.get('content_sha256')==body_sha,f'HANDOFF_PPM_NOT_PASS:{i}')
        bodies.append(body)
    try:
        content_guard.validate_batch_distinctness(bodies)
    except content_guard.ContentGuardError as exc:
        raise HandoffError('HANDOFF_CONTENT_GUARD:'+str(exc)) from exc
    return payload

def read_validate_handoff(path: Path) -> tuple[dict,bytes]:
    raw=path.read_bytes()
    try:
        payload=json.loads(raw.decode('utf-8'))
    except Exception as exc:
        raise HandoffError('HANDOFF_JSON_INVALID') from exc
    validate_handoff(payload)
    return payload,raw

def canonicalize_handoff(input_path: Path, output_path: Path) -> bytes:
    payload,_=read_validate_handoff(input_path)
    raw=(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode('utf-8')
    output_path.write_bytes(raw)
    _require(sha256_bytes(output_path.read_bytes())==sha256_bytes(raw),'HANDOFF_CANONICAL_WRITE_MISMATCH')
    return raw

def inline_pack(input_path: Path, output_path: Path) -> dict:
    payload,_=read_validate_handoff(input_path)
    raw=(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode('utf-8')
    compressed=lzma.compress(raw,format=lzma.FORMAT_XZ,preset=9|lzma.PRESET_EXTREME)
    env={
        'contract':INLINE_CONTRACT,
        'filename':HANDOFF_FILENAME,
        'mime_type':'application/json',
        'compression':'xz-lzma2-preset9e',
        'encoding':'base64',
        'byte_length':len(raw),
        'plaintext_sha256':sha256_bytes(raw),
        'payload_base64':base64.b64encode(compressed).decode('ascii'),
        'publish_allowed':False,
    }
    body=json.dumps(env,ensure_ascii=False,sort_keys=True,separators=(',',':'))
    text=INLINE_BEGIN+'\n'+body+'\n'+INLINE_END+'\n'
    _require(len(text)<=INLINE_MAX_CHARS,'INLINE_ENVELOPE_TOO_LARGE')
    output_path.write_text(text,encoding='utf-8')
    return env

def _parse_inline_text(text: str) -> dict:
    begin=text.find(INLINE_BEGIN)
    _require(begin>=0,'INLINE_BEGIN_MISSING')
    start=begin+len(INLINE_BEGIN)
    end=text.find(INLINE_END,start)
    _require(end>=0,'INLINE_END_MISSING')
    between=text[start:end].strip()
    _require(between!='','INLINE_BODY_MISSING')
    try:
        env=json.loads(between)
    except Exception as exc:
        raise HandoffError('INLINE_JSON_INVALID') from exc
    return env

def inline_unpack(inline_path: Path, output_dir: Path) -> Path:
    text=inline_path.read_text(encoding='utf-8')
    env=_parse_inline_text(text)
    _require(isinstance(env,dict),'INLINE_NOT_OBJECT')
    required={'contract','filename','mime_type','compression','encoding','byte_length','plaintext_sha256','payload_base64','publish_allowed'}
    _require(set(env)==required,'INLINE_SCHEMA_INVALID')
    _require(env['contract']==INLINE_CONTRACT,'INLINE_CONTRACT_INVALID')
    _require(env['filename']==HANDOFF_FILENAME and env['mime_type']=='application/json','INLINE_TARGET_INVALID')
    _require(env['compression']=='xz-lzma2-preset9e' and env['encoding']=='base64','INLINE_CODEC_INVALID')
    _require(env['publish_allowed'] is False,'INLINE_PUBLISH_MUST_BE_FALSE')
    _require(isinstance(env['byte_length'],int) and env['byte_length']>0,'INLINE_LENGTH_INVALID')
    _require(isinstance(env['plaintext_sha256'],str) and SHA_RE.fullmatch(env['plaintext_sha256']) is not None,'INLINE_SHA_INVALID')
    try:
        compressed=base64.b64decode(env['payload_base64'],validate=True)
    except Exception as exc:
        raise HandoffError('INLINE_BASE64_INVALID') from exc
    try:
        raw=lzma.decompress(compressed,format=lzma.FORMAT_XZ)
    except Exception as exc:
        raise HandoffError('INLINE_XZ_INVALID') from exc
    _require(len(raw)==env['byte_length'],'INLINE_LENGTH_MISMATCH')
    _require(sha256_bytes(raw)==env['plaintext_sha256'],'INLINE_SHA_MISMATCH')
    try:
        payload=json.loads(raw.decode('utf-8'))
    except Exception as exc:
        raise HandoffError('INLINE_PAYLOAD_JSON_INVALID') from exc
    validate_handoff(payload)
    canonical=(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode('utf-8')
    _require(raw==canonical,'INLINE_PAYLOAD_NOT_CANONICAL')
    output_dir.mkdir(parents=True,exist_ok=True)
    out=output_dir/HANDOFF_FILENAME
    out.write_bytes(raw)
    _require(sha256_bytes(out.read_bytes())==env['plaintext_sha256'],'INLINE_WRITTEN_SHA_MISMATCH')
    return out

def main(argv=None):
    p=argparse.ArgumentParser()
    sp=p.add_subparsers(dest='cmd',required=True)
    a=sp.add_parser('validate'); a.add_argument('handoff')
    a=sp.add_parser('canonicalize'); a.add_argument('handoff'); a.add_argument('output')
    a=sp.add_parser('inline-pack'); a.add_argument('handoff'); a.add_argument('inline_output')
    a=sp.add_parser('inline-unpack'); a.add_argument('inline_input'); a.add_argument('output_dir')
    ns=p.parse_args(argv)
    try:
        if ns.cmd=='validate':
            _,raw=read_validate_handoff(Path(ns.handoff)); print(json.dumps({'status':'SYSTEM4_HANDOFF_VALIDATE_PASS','sha256':sha256_bytes(raw)},separators=(',',':')))
        elif ns.cmd=='canonicalize':
            raw=canonicalize_handoff(Path(ns.handoff),Path(ns.output)); print(json.dumps({'status':'SYSTEM4_HANDOFF_CANONICALIZE_PASS','sha256':sha256_bytes(raw),'bytes':len(raw)},separators=(',',':')))
        elif ns.cmd=='inline-pack':
            env=inline_pack(Path(ns.handoff),Path(ns.inline_output)); print(json.dumps({'status':'SYSTEM4_INLINE_PACK_PASS','sha256':env['plaintext_sha256'],'bytes':env['byte_length']},separators=(',',':')))
        else:
            out=inline_unpack(Path(ns.inline_input),Path(ns.output_dir)); print(json.dumps({'status':'SYSTEM4_INLINE_UNPACK_PASS','file':str(out),'sha256':sha256_bytes(out.read_bytes())},separators=(',',':')))
        return 0
    except HandoffError as exc:
        print('SYSTEM4_HANDOFF_BLOCK:'+str(exc))
        return 2

if __name__=='__main__':
    raise SystemExit(main())
