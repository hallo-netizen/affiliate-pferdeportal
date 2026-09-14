from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
import chat_start_gate, point0_snapshot, root_entry, source_acquisition

class MachinePoint0Error(RuntimeError): pass

def _head(repo:Path)->str:
    return subprocess.check_output(['git','rev-parse','--verify','HEAD'],cwd=repo,text=True).strip()

def bind_chat_start(snapshot:dict,event:dict)->dict:
    try: return chat_start_gate.bind(snapshot,event)
    except Exception as exc: raise MachinePoint0Error(str(exc)) from exc

def validate_chat_start(snapshot:dict)->dict:
    try: return chat_start_gate.validate(snapshot)
    except Exception as exc: raise MachinePoint0Error(str(exc)) from exc

def build_from_acquired(*, snapshot_bytes:bytes, acquired_batch:dict, prewrite_plan_batch:dict, provider:str, manifest:str, head:str)->dict:
    prod=point0_snapshot._validate_prod(snapshot_bytes); validate_chat_start(prod)
    try:
        chat_start_gate.forbid_dataforseo(provider); chat_start_gate.forbid_dataforseo(acquired_batch); chat_start_gate.forbid_dataforseo(prewrite_plan_batch)
    except Exception as exc: raise MachinePoint0Error(str(exc)) from exc
    items=prod['next_textmachine_metadata_batch']['items']
    acquired=acquired_batch.get('items') if isinstance(acquired_batch,dict) and acquired_batch.get('contract')==source_acquisition.RESULT_CONTRACT else None
    plans=prewrite_plan_batch.get('items') if isinstance(prewrite_plan_batch,dict) and prewrite_plan_batch.get('contract')=='SYSTEM4_MACHINE_PREWRITE_PLAN_BATCH_V1' else None
    if not isinstance(acquired,list) or acquired_batch.get('item_count')!=len(items) or len(acquired)!=len(items): raise MachinePoint0Error('ACQUIRED_SOURCE_BATCH_INVALID')
    if not isinstance(plans,list) or prewrite_plan_batch.get('item_count')!=len(items) or len(plans)!=len(items): raise MachinePoint0Error('PREWRITE_PLAN_BATCH_INVALID')
    pools=[]; bindings=[]
    for i,article in enumerate(items):
        ar=acquired[i]; pr=plans[i]
        if ar.get('item_index')!=i or ar.get('plan_slot')!=article['plan_slot']: raise MachinePoint0Error('ACQUIRED_SOURCE_ITEM_MISMATCH:'+str(i))
        if pr.get('item_index')!=i or pr.get('plan_slot')!=article['plan_slot'] or not isinstance(pr.get('production_plan_item'),dict): raise MachinePoint0Error('PREWRITE_PLAN_ITEM_MISMATCH:'+str(i))
        pools.append(ar['sources']); bindings.append(point0_snapshot.prewrite_from_plan(article,i,pr['production_plan_item']))
    return point0_snapshot.build(production_snapshot_bytes=snapshot_bytes,root_manifest_sha256=manifest,head_sha=head,research_provider=provider,source_pools=pools,prewrite_bindings=bindings)

def main(argv:list[str])->int:
    try:
        if len(argv)>=2 and argv[1]=='bind-start':
            if len(argv)!=5: raise MachinePoint0Error('BAD_COMMAND')
            snapshot=Path(argv[2]); event=Path(argv[3]); out=Path(argv[4])
            value=bind_chat_start(json.loads(snapshot.read_text(encoding='utf-8')),json.loads(event.read_text(encoding='utf-8')))
            out.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n',encoding='utf-8')
            print('SYSTEM4_CHAT_START_PASS:'+value['system4_chat_start']['receipt_sha256']); return 0
        if len(argv)!=7 or argv[1] not in {'build-acquired','build-fetch'}: raise MachinePoint0Error('BAD_COMMAND')
        snapshot=Path(argv[2]); sources=Path(argv[3]); plans=Path(argv[4]); out=Path(argv[5]); provider=argv[6]
        repo=Path(__file__).resolve().parent.parent; manifest=root_entry._critical_manifest_sha256(); head=_head(repo); raw=snapshot.read_bytes()
        source_value=json.loads(sources.read_text(encoding='utf-8'))
        if argv[1]=='build-fetch':
            try: chat_start_gate.forbid_dataforseo(source_value)
            except Exception as exc: raise MachinePoint0Error(str(exc)) from exc
            source_value=source_acquisition.acquire_batch(source_value)
        plan_value=json.loads(plans.read_text(encoding='utf-8'))
        value=build_from_acquired(snapshot_bytes=raw,acquired_batch=source_value,prewrite_plan_batch=plan_value,provider=provider,manifest=manifest,head=head)
        out.write_bytes(point0_snapshot.canon(value)); print('SYSTEM4_MACHINE_POINT0_PASS:'+value['point0_core_sha256']); return 0
    except Exception as exc:
        print('SYSTEM4_MACHINE_POINT0_FAIL:'+str(exc)); return 2
if __name__=='__main__': raise SystemExit(main(sys.argv))
