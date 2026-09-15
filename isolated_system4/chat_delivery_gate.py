from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import handoff_transport

CONTRACT='SYSTEM4_CHAT_DELIVERY_RECEIPT_V1'
STATUS_READY='ARTIFACT_READY_FOR_REQUESTING_CHAT'
RECEIPT_FILENAME='SYSTEM4_CHAT_DELIVERY_RECEIPT_V1.json'
ARTIFACT_FILENAME=handoff_transport.HANDOFF_FILENAME

class ChatDeliveryError(RuntimeError):
    pass

def canon(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode('utf-8')

def sha256(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()

def _require(ok:bool,code:str)->None:
    if not ok:
        raise ChatDeliveryError(code)

def stage(handoff_path:Path,output_dir:Path)->tuple[Path,Path]:
    handoff_path=Path(handoff_path); output_dir=Path(output_dir)
    try:
        payload,raw=handoff_transport.read_validate_handoff(handoff_path)
    except handoff_transport.HandoffError as exc:
        raise ChatDeliveryError('CHAT_SOURCE_HANDOFF_INVALID:'+str(exc)) from exc
    wr=payload['wordpress_review']
    _require(wr['direct_wordpress_upload_ready'] is True,'CHAT_WORDPRESS_IMPORT_NOT_READY')
    _require(wr['intended_next_step']=='WORDPRESS_DIRECT_IMPORT','CHAT_WORDPRESS_NEXT_STEP_INVALID')
    _require(wr['plugin_name']=='Portal SEO Editorial Plan Compiler','CHAT_WORDPRESS_PLUGIN_INVALID')
    _require(wr['plugin_version_verified_against']=='0.28.23','CHAT_WORDPRESS_PLUGIN_VERSION_INVALID')
    _require(wr['ppm_version_verified_against']=='6.7.9','CHAT_WORDPRESS_PPM_VERSION_INVALID')
    _require(payload['publish_allowed'] is False,'CHAT_PUBLISH_MUST_BE_FALSE')
    output_dir.mkdir(parents=True,exist_ok=True)
    artifact=output_dir/ARTIFACT_FILENAME
    artifact.write_bytes(raw)
    try:
        verified,verified_raw=handoff_transport.read_validate_handoff(artifact)
    except handoff_transport.HandoffError as exc:
        raise ChatDeliveryError('CHAT_WRITTEN_ARTIFACT_INVALID:'+str(exc)) from exc
    _require(verified_raw==raw,'CHAT_ARTIFACT_BYTE_MISMATCH')
    receipt={
        'contract':CONTRACT,
        'status':STATUS_READY,
        'artifact_filename':ARTIFACT_FILENAME,
        'mime_type':'application/json',
        'sha256':sha256(raw),
        'byte_length':len(raw),
        'article_count':len(verified['articles']),
        'publish_allowed':False,
        'wordpress_import':dict(wr),
        'chat_surface_requirement':'MUST_BE_ATTACHED_IN_REQUESTING_CHAT_BEFORE_OVERALL_PASS',
        'overall_acceptance_status':'PENDING_CHAT_ATTACHMENT',
    }
    receipt_path=output_dir/RECEIPT_FILENAME
    receipt_path.write_bytes(canon(receipt))
    verify(artifact,receipt_path)
    return artifact,receipt_path

def verify(artifact_path:Path,receipt_path:Path)->dict:
    artifact_path=Path(artifact_path); receipt_path=Path(receipt_path)
    _require(artifact_path.is_file(),'CHAT_ARTIFACT_MISSING')
    _require(receipt_path.is_file(),'CHAT_RECEIPT_MISSING')
    try:
        receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
    except Exception as exc:
        raise ChatDeliveryError('CHAT_RECEIPT_JSON_INVALID') from exc
    required={'contract','status','artifact_filename','mime_type','sha256','byte_length','article_count','publish_allowed','wordpress_import','chat_surface_requirement','overall_acceptance_status'}
    _require(isinstance(receipt,dict) and set(receipt)==required,'CHAT_RECEIPT_SCHEMA_INVALID')
    _require(receipt['contract']==CONTRACT,'CHAT_RECEIPT_CONTRACT_INVALID')
    _require(receipt['status']==STATUS_READY,'CHAT_RECEIPT_STATUS_INVALID')
    _require(receipt['artifact_filename']==ARTIFACT_FILENAME,'CHAT_ARTIFACT_FILENAME_INVALID')
    _require(receipt['mime_type']=='application/json','CHAT_ARTIFACT_MIME_INVALID')
    _require(receipt['publish_allowed'] is False,'CHAT_RECEIPT_PUBLISH_INVALID')
    _require(receipt['chat_surface_requirement']=='MUST_BE_ATTACHED_IN_REQUESTING_CHAT_BEFORE_OVERALL_PASS','CHAT_SURFACE_REQUIREMENT_INVALID')
    _require(receipt['overall_acceptance_status']=='PENDING_CHAT_ATTACHMENT','CHAT_OVERALL_STATUS_MUST_REMAIN_PENDING')
    raw=artifact_path.read_bytes()
    _require(receipt['sha256']==sha256(raw),'CHAT_ARTIFACT_SHA_MISMATCH')
    _require(receipt['byte_length']==len(raw),'CHAT_ARTIFACT_LENGTH_MISMATCH')
    try:
        payload,_=handoff_transport.read_validate_handoff(artifact_path)
    except handoff_transport.HandoffError as exc:
        raise ChatDeliveryError('CHAT_ARTIFACT_HANDOFF_INVALID:'+str(exc)) from exc
    _require(receipt['article_count']==len(payload['articles']),'CHAT_ARTICLE_COUNT_MISMATCH')
    _require(receipt['wordpress_import']==payload['wordpress_review'],'CHAT_WORDPRESS_METADATA_MISMATCH')
    return receipt

def main(argv=None):
    parser=argparse.ArgumentParser()
    sub=parser.add_subparsers(dest='cmd',required=True)
    p=sub.add_parser('stage'); p.add_argument('handoff'); p.add_argument('output_dir')
    p=sub.add_parser('verify'); p.add_argument('artifact'); p.add_argument('receipt')
    ns=parser.parse_args(argv)
    try:
        if ns.cmd=='stage':
            artifact,receipt=stage(Path(ns.handoff),Path(ns.output_dir))
            value=verify(artifact,receipt)
            print(json.dumps({'status':'SYSTEM4_CHAT_ARTIFACT_READY','artifact':str(artifact),'receipt':str(receipt),'sha256':value['sha256'],'bytes':value['byte_length'],'overall_acceptance_status':value['overall_acceptance_status']},separators=(',',':')))
        else:
            value=verify(Path(ns.artifact),Path(ns.receipt))
            print(json.dumps({'status':'SYSTEM4_CHAT_ARTIFACT_VERIFY_PASS','sha256':value['sha256'],'bytes':value['byte_length'],'overall_acceptance_status':value['overall_acceptance_status']},separators=(',',':')))
        return 0
    except ChatDeliveryError as exc:
        print('SYSTEM4_CHAT_DELIVERY_BLOCK:'+str(exc))
        return 2

if __name__=='__main__':
    raise SystemExit(main())
