from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

import handoff_transport

READY_TOKEN='SYSTEM4_BOUND_BATCH_READY_FOR_ARTIFACT'
PASS_TOKEN='SYSTEM4_BOUND_BATCH_PASS'
RECEIPT_CONTRACT='SYSTEM4_ACTIONS_ARTIFACT_RECEIPT_V1'
RECEIPT_FILENAME='SYSTEM4_ACTIONS_ARTIFACT_RECEIPT_V1.json'
SHA_LABEL='SYSTEM4_WORDPRESS_HANDOFF_V1_SHA256'
BYTES_LABEL='SYSTEM4_WORDPRESS_HANDOFF_V1_BYTES'
PARTS_LABEL='SYSTEM4_PARENT_CHAT_INLINE_V2_PARTS'

class ArtifactRelayError(RuntimeError):
    pass

def _require(ok:bool,code:str)->None:
    if not ok:
        raise ArtifactRelayError(code)

def _sha(raw:bytes)->str:
    return hashlib.sha256(raw).hexdigest()

def _canon(value:dict)->bytes:
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode('utf-8')

def _meta(text:str,label:str)->str:
    m=re.search(r'(?m)^'+re.escape(label)+r':([^\r\n]+)$',text)
    _require(m is not None,'RELAY_METADATA_MISSING:'+label)
    return m.group(1).strip()

def extract_inline(text:str)->str:
    _require(READY_TOKEN in text,'RELAY_READY_TOKEN_MISSING')
    begin=text.find(handoff_transport.INLINE_BEGIN)
    _require(begin>=0,'RELAY_INLINE_BEGIN_MISSING')
    _require(text.find(handoff_transport.INLINE_BEGIN,begin+1)<0,'RELAY_INLINE_BEGIN_DUPLICATE')
    end=text.find(handoff_transport.INLINE_END,begin+len(handoff_transport.INLINE_BEGIN))
    _require(end>=0,'RELAY_INLINE_END_MISSING')
    _require(text.find(handoff_transport.INLINE_END,end+1)<0,'RELAY_INLINE_END_DUPLICATE')
    return text[begin:end+len(handoff_transport.INLINE_END)]+'\n'

def reconstruct_from_comment(text:str,output_dir:Path,source_comment_id:str)->tuple[Path,Path,dict]:
    expected_sha=_meta(text,SHA_LABEL)
    expected_bytes_text=_meta(text,BYTES_LABEL)
    expected_parts_text=_meta(text,PARTS_LABEL)
    _require(re.fullmatch(r'[0-9a-f]{64}',expected_sha) is not None,'RELAY_EXPECTED_SHA_INVALID')
    _require(expected_bytes_text.isdigit() and int(expected_bytes_text)>0,'RELAY_EXPECTED_BYTES_INVALID')
    _require(expected_parts_text.isdigit() and int(expected_parts_text)>0,'RELAY_EXPECTED_PARTS_INVALID')
    inline_text=extract_inline(text)
    envs=handoff_transport._parse_inline_text(inline_text)
    _require(len(envs)==int(expected_parts_text),'RELAY_PART_COUNT_MISMATCH')
    output_dir=Path(output_dir)
    output_dir.mkdir(parents=True,exist_ok=True)
    inline_path=output_dir/handoff_transport.INLINE_FILENAME
    inline_path.write_text(inline_text,encoding='utf-8')
    artifact=handoff_transport.inline_unpack(inline_path,output_dir)
    payload,raw=handoff_transport.read_validate_handoff(artifact)
    _require(_sha(raw)==expected_sha,'RELAY_SHA_MISMATCH')
    _require(len(raw)==int(expected_bytes_text),'RELAY_BYTES_MISMATCH')
    _require(payload.get('publish_allowed') is False,'RELAY_PUBLISH_MUST_BE_FALSE')
    receipt={
        'contract':RECEIPT_CONTRACT,
        'status':'READY_FOR_GITHUB_ACTIONS_ARTIFACT_UPLOAD',
        'artifact_filename':handoff_transport.HANDOFF_FILENAME,
        'sha256':expected_sha,
        'byte_length':len(raw),
        'part_count':len(envs),
        'article_count':len(payload['articles']),
        'source_comment_id':str(source_comment_id),
        'publish_allowed':False,
        'overall_acceptance_status':'PENDING_ACTIONS_ARTIFACT_PERSISTENCE_VERIFY',
    }
    receipt_path=output_dir/RECEIPT_FILENAME
    receipt_path.write_bytes(_canon(receipt))
    verify_persisted(artifact,receipt_path)
    return artifact,receipt_path,receipt

def verify_persisted(artifact_path:Path,receipt_path:Path)->dict:
    artifact_path=Path(artifact_path); receipt_path=Path(receipt_path)
    _require(artifact_path.is_file(),'RELAY_PERSISTED_ARTIFACT_MISSING')
    _require(receipt_path.is_file(),'RELAY_PERSISTED_RECEIPT_MISSING')
    try:
        receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
    except Exception as exc:
        raise ArtifactRelayError('RELAY_RECEIPT_JSON_INVALID') from exc
    required={'contract','status','artifact_filename','sha256','byte_length','part_count','article_count','source_comment_id','publish_allowed','overall_acceptance_status'}
    _require(isinstance(receipt,dict) and set(receipt)==required,'RELAY_RECEIPT_SCHEMA_INVALID')
    _require(receipt['contract']==RECEIPT_CONTRACT,'RELAY_RECEIPT_CONTRACT_INVALID')
    _require(receipt['status']=='READY_FOR_GITHUB_ACTIONS_ARTIFACT_UPLOAD','RELAY_RECEIPT_STATUS_INVALID')
    _require(receipt['artifact_filename']==handoff_transport.HANDOFF_FILENAME,'RELAY_ARTIFACT_FILENAME_INVALID')
    _require(receipt['publish_allowed'] is False,'RELAY_RECEIPT_PUBLISH_INVALID')
    _require(receipt['overall_acceptance_status']=='PENDING_ACTIONS_ARTIFACT_PERSISTENCE_VERIFY','RELAY_OVERALL_STATUS_INVALID')
    payload,raw=handoff_transport.read_validate_handoff(artifact_path)
    _require(_sha(raw)==receipt['sha256'],'RELAY_PERSISTED_SHA_MISMATCH')
    _require(len(raw)==receipt['byte_length'],'RELAY_PERSISTED_BYTES_MISMATCH')
    _require(len(payload['articles'])==receipt['article_count'],'RELAY_PERSISTED_ARTICLE_COUNT_MISMATCH')
    return receipt

def _event_comment(path:Path)->tuple[str,str]:
    try:
        event=json.loads(path.read_text(encoding='utf-8'))
        comment=event['comment']
        return str(comment['body']),str(comment['id'])
    except Exception as exc:
        raise ArtifactRelayError('RELAY_EVENT_JSON_INVALID') from exc

def main(argv=None):
    p=argparse.ArgumentParser()
    sp=p.add_subparsers(dest='cmd',required=True)
    a=sp.add_parser('from-comment'); a.add_argument('comment_file'); a.add_argument('output_dir'); a.add_argument('--comment-id',default='local')
    a=sp.add_parser('from-event'); a.add_argument('event_json'); a.add_argument('output_dir')
    a=sp.add_parser('verify'); a.add_argument('artifact'); a.add_argument('receipt')
    ns=p.parse_args(argv)
    try:
        if ns.cmd=='from-comment':
            text=Path(ns.comment_file).read_text(encoding='utf-8'); source_id=ns.comment_id
            artifact,receipt,value=reconstruct_from_comment(text,Path(ns.output_dir),source_id)
            print(json.dumps({'status':'SYSTEM4_ACTIONS_ARTIFACT_RELAY_READY','artifact':str(artifact),'receipt':str(receipt),'sha256':value['sha256'],'bytes':value['byte_length'],'parts':value['part_count']},separators=(',',':')))
        elif ns.cmd=='from-event':
            text,source_id=_event_comment(Path(ns.event_json))
            artifact,receipt,value=reconstruct_from_comment(text,Path(ns.output_dir),source_id)
            print(json.dumps({'status':'SYSTEM4_ACTIONS_ARTIFACT_RELAY_READY','artifact':str(artifact),'receipt':str(receipt),'sha256':value['sha256'],'bytes':value['byte_length'],'parts':value['part_count']},separators=(',',':')))
        else:
            value=verify_persisted(Path(ns.artifact),Path(ns.receipt))
            print(json.dumps({'status':'SYSTEM4_ACTIONS_ARTIFACT_PERSISTENCE_VERIFY_PASS','sha256':value['sha256'],'bytes':value['byte_length'],'parts':value['part_count']},separators=(',',':')))
        return 0
    except (ArtifactRelayError,handoff_transport.HandoffError,OSError) as exc:
        print('SYSTEM4_ACTIONS_ARTIFACT_RELAY_BLOCK:'+str(exc))
        return 2

if __name__=='__main__':
    raise SystemExit(main())
