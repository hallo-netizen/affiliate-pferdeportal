#!/usr/bin/env python3
from __future__ import annotations

import base64, copy, hashlib, json, tempfile
from dataclasses import dataclass
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import single_door_preproduction_handoff as h7

class FakeBoundary:
    BOUNDARY_CONTRACT='PFERDE_ATELIER_SINGLE_DOOR_EXECUTION_BOUNDARY_V1'
    @dataclass(frozen=True)
    class _Door:
        room_token:str; action_token:str; receipt_token:str; next_room_token:str; input_handles:tuple[str,...]
    class DoorBinding:
        @classmethod
        def from_mapping(cls,raw):
            return FakeBoundary._Door(raw['room_token'],raw['action_token'],raw['receipt_token'],raw['next_room_token'],tuple(raw['input_handles']))
    @staticmethod
    def build_worker_request(*,binding,model):
        return {'model':model,'input':binding.room_token,'tools':[{'type':'function','name':'execute_bound_action','description':'opaque','parameters':{'type':'object','properties':{},'required':[],'additionalProperties':False},'strict':True}],'tool_choice':{'type':'function','name':'execute_bound_action'},'parallel_tool_calls':False,'metadata':{'single_door_contract':FakeBoundary.BOUNDARY_CONTRACT,'room_token':binding.room_token}}
    @staticmethod
    def validate_action_receipt(binding,receipt):
        expected={'contract':FakeBoundary.BOUNDARY_CONTRACT,'room_token':binding.room_token,'action_token':binding.action_token,'receipt_token':binding.receipt_token,'next_room_token':binding.next_room_token}
        for k,v in expected.items():
            if receipt.get(k)!=v: raise RuntimeError('RECEIPT_MISMATCH:'+k)
        if receipt.get('status') not in {'PASS','BLOCKED','USER_ACTION_REQUIRED'}: raise RuntimeError('STATUS')
        return dict(receipt)

def stable(obj): return hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def make_package(path:Path):
    private=Ed25519PrivateKey.generate(); public=private.public_key().public_bytes(encoding=serialization.Encoding.Raw,format=serialization.PublicFormat.Raw)
    key_id='test-ed25519-key'; key_sha=hashlib.sha256(public).hexdigest(); trusted={key_id:{'sha256':key_sha,'public_key_b64':base64.b64encode(public).decode()}}
    bundle={'contract':'canonical_fact_pack_import_v1','fact_packs':[{'fact_pack_id':'F1'}]}; plan={'contract':'production_plan_v4','items':[{'canonical_article_id':'article:test'}]}; bh,ph=stable(bundle),stable(plan)
    release={'contract':h7.RELEASE_CONTRACT,'status':'PASS','signature_algorithm':'ED25519','signing_key_id':key_id,'signing_public_key_sha256':key_sha,'fact_pack_bundle_sha256':bh,'production_plan_sha256':ph,'exact_five_batch_sha256':'0'*64,'exact_five_item_count':1,'items':[{'plan_slot':'1'*64,'canonical_article_id':'article:test'}]}
    payload_sha=stable(release); release['release_payload_sha256']=payload_sha; release['signature_b64']=base64.b64encode(private.sign(payload_sha.encode('ascii'))).decode(); release['release_sha256']=stable(release); rh=stable(release)
    env={'contract':h7.PACKAGE_CONTRACT,'fact_pack_bundle_sha256':bh,'production_plan_sha256':ph,'workflow_release_sha256':rh,'package_id':stable({'contract':h7.PACKAGE_CONTRACT,'fact_pack_bundle_sha256':bh,'production_plan_sha256':ph,'workflow_release_sha256':rh}),'source':'TEST','fact_pack_bundle':bundle,'production_plan':plan,'workflow_release':release}; env['package_payload_sha256']=stable(env)
    path.write_text(json.dumps(env),encoding='utf-8'); return env,trusted

def blocked(fn,code):
    try: fn()
    except Exception as e:
        assert code in str(e),(code,str(e)); return
    raise AssertionError('expected block:'+code)

def main():
    cases=0
    actual=h7.boundary_module(); blob=hashlib.sha1(b'blob '+str(h7.BOUNDARY_PATH.stat().st_size).encode()+b'\0'+h7.BOUNDARY_PATH.read_bytes()).hexdigest(); assert blob=='4921624e0b6d24ce35549bec28e6d43035b2f098'
    req=h7.worker_request('gpt-5.6-sol',boundary=actual); assert req['input']==h7.ROOM_TOKEN and len(req['tools'])==1 and req['parallel_tool_calls'] is False; cases+=1
    bad=copy.deepcopy(req); bad['tools'].append(copy.deepcopy(bad['tools'][0])); blocked(lambda:actual.assert_single_door_request(bad),'EXACTLY_ONE_TOOL_REQUIRED'); cases+=1
    bad=copy.deepcopy(req); bad['tools'][0]['name']='web'; bad['tool_choice']['name']='web'; blocked(lambda:actual.assert_single_door_request(bad),'BOUND_TOOL_INVALID'); cases+=1
    b=FakeBoundary; req=h7.worker_request('gpt-5.6-sol',boundary=b); assert req['input']==h7.ROOM_TOKEN and len(req['tools'])==1; cases+=1
    blocked(lambda:h7.worker_request('gpt-5.6-sol',boundary=b,worker_input='Artikeltext'),'unexpected keyword'); cases+=1
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); pkg=root/'approved.json'; env,trusted=make_package(pkg); proof=h7.validate_production_package(pkg,trusted_keys=trusted); assert proof['status']=='SIGNED_PRODUCTION_PACKAGE_HANDOFF_VALID'; cases+=1
        wrong=root/'production-plan.json'; wrong.write_text(json.dumps(env['production_plan'])); blocked(lambda:h7.validate_production_package(wrong,trusted_keys=trusted),'HANDOFF_PACKAGE_SCHEMA_INVALID'); cases+=1
        md=root/'articles.md'; md.write_text('# article'); blocked(lambda:h7.validate_production_package(md,trusted_keys=trusted),'HANDOFF_FILE_MUST_BE_JSON'); cases+=1
        tampered=copy.deepcopy(env); tampered['production_plan']['items'].append({'canonical_article_id':'tampered'}); tp=root/'tampered.json'; tp.write_text(json.dumps(tampered)); blocked(lambda:h7.validate_production_package(tp,trusted_keys=trusted),'HANDOFF_COMPONENT_HASH_MISMATCH'); cases+=1
        badsig=copy.deepcopy(env); badsig['workflow_release']['signature_b64']=base64.b64encode(b'x'*64).decode(); badsig['workflow_release_sha256']=stable(badsig['workflow_release']); badsig['package_id']=stable({'contract':h7.PACKAGE_CONTRACT,'fact_pack_bundle_sha256':badsig['fact_pack_bundle_sha256'],'production_plan_sha256':badsig['production_plan_sha256'],'workflow_release_sha256':badsig['workflow_release_sha256']}); cp=copy.deepcopy(badsig); cp.pop('package_payload_sha256',None); badsig['package_payload_sha256']=stable(cp); sp=root/'badsig.json'; sp.write_text(json.dumps(badsig)); blocked(lambda:h7.validate_production_package(sp,trusted_keys=trusted),'WORKFLOW_RELEASE_SIGNATURE_INVALID'); cases+=1
        hm={h7.INPUT_HANDLE:'approved.json'}; receipt=h7.execute_bound_preproduction_action(handle_map=hm,repo=root,attach_callable=lambda p:{'ok':True,'status':'RUNTIME_BATCH_EXECUTION_READY'},boundary=b,trusted_keys=trusted); assert receipt['status']=='PASS' and receipt['next_room_token']==h7.NEXT_ROOM_TOKEN; cases+=1
        blocked(lambda:h7.execute_bound_preproduction_action(handle_map={'I_OTHER':'approved.json'},repo=root,attach_callable=lambda p:{'status':'RUNTIME_BATCH_EXECUTION_READY'},boundary=b,trusted_keys=trusted),'HANDLE_MAP_MUST_CONTAIN_EXACTLY_BOUND_HANDLE'); cases+=1
        blocked(lambda:h7.execute_bound_preproduction_action(handle_map=hm,repo=root,attach_callable=lambda p:{'status':'READY_WAITING_PACKAGE'},boundary=b,trusted_keys=trusted),'ATTACH_PACKAGE_DID_NOT_REACH_EXECUTION_READY'); cases+=1
        auth=h7.authoritative_handoff(receipt,boundary=b); assert auth['authoritative_origin']=='SINGLE_DOOR_EXECUTOR_ONLY'; cases+=1
        blocked(lambda:h7.authoritative_handoff(None,boundary=b),'SINGLE_DOOR_RECEIPT_REQUIRED'); cases+=1
        wrong_next=dict(receipt); wrong_next['next_room_token']='R_999'; blocked(lambda:h7.authoritative_handoff(wrong_next,boundary=b),'RECEIPT_MISMATCH:next_room_token'); cases+=1
    assert cases==16
    print(json.dumps({'ok':True,'status':'H7_PROJECT_EXECUTION_BOUNDARY_POSITIVE_NEGATIVE_PASS','cases':cases,'boundary_git_blob':blob},indent=2))
if __name__=='__main__': main()
