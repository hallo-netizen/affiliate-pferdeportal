from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping

import point0_snapshot
import root_entry

CONTRACT='SYSTEM4_MACHINE_REPAIR_ROUTE_V1'
MAX_MACHINE_REPAIR_CYCLES=8

class RepairRouteError(RuntimeError):
    pass

def canon(value:Any)->bytes:
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode('utf-8')

def sha256(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()

def _first_finding(state:Mapping[str,Any])->dict[str,Any]:
    checks=state.get('checks') if isinstance(state.get('checks'),Mapping) else {}
    findings=checks.get('findings') if isinstance(checks.get('findings'),list) else []
    return dict(findings[0]) if findings and isinstance(findings[0],Mapping) else {}

def classify(state:Mapping[str,Any])->dict[str,Any]:
    finding=_first_finding(state)
    code=str(finding.get('error_code') or state.get('last_error') or '').upper()
    field=str(finding.get('field') or '').strip().lower()
    rule=str(finding.get('failed_rule') or finding.get('rule_id') or '').upper()
    text='|'.join((code,field,rule))
    if any(token in text for token in ('CONTENT.TITLE','TITLE_','ARTICLE_TITLE')):
        owner='PARENT_METADATA'; target='TITLE_BINDING'
    elif any(token in text for token in ('CATEGORY','TAXONOMY')):
        owner='PARENT_METADATA'; target='CATEGORY_BINDING'
    elif any(token in text for token in ('PLAN_SLOT','SLOT_')):
        owner='PARENT_METADATA'; target='PLAN_SLOT_BINDING'
    elif any(token in text for token in ('LINK','HREF','ANCHOR')):
        owner='CONTEXT_BINDING'; target='LINK_BINDING'
    elif any(token in text for token in ('SOURCE','FACT','RESEARCH')):
        owner='RESEARCH_BINDING'; target='RESEARCH_OR_FACT_BINDING'
    else:
        owner='DRAFT_BODY'; target='SAME_ARTICLE_BODY'
    return {'contract':CONTRACT,'owner':owner,'target':target,'finding':finding,'error_code':code,'field':field,'rule':rule}

def _punctuation_repairs(title:str,finding:Mapping[str,Any])->str:
    expected=str(finding.get('expected') or '').casefold()
    rule=str(finding.get('failed_rule') or finding.get('error_code') or '').casefold()
    text=' '.join((expected,rule))
    table={'colon':':','doppelpunkt':':','comma':',','komma':',','semicolon':';','semikolon':';','question mark':'?','fragezeichen':'?','exclamation mark':'!','ausrufezeichen':'!'}
    repaired=title
    for name,char in table.items():
        if ('no '+name) in text or ('must_not_contain_'+name.replace(' ','_')) in text or ('kein '+name) in text:
            repaired=repaired.replace(char,' ')
    repaired=re.sub(r'\s+',' ',repaired).strip(' -–—')
    return repaired

def _decode_point0(path:Path)->tuple[dict[str,Any],dict[str,Any],bytes]:
    value=json.loads(path.read_text(encoding='utf-8'))
    raw=point0_snapshot.verify(value)
    prod=json.loads(raw.decode('utf-8'))
    return value,prod,raw

def _rebuild_batch(prod:dict[str,Any],index:int,new_item:dict[str,Any])->bytes:
    out=copy.deepcopy(prod)
    batch=out['next_textmachine_metadata_batch']
    items=copy.deepcopy(batch['items'])
    items[index]=new_item
    batch['items']=items
    batch['item_count']=len(items)
    material={k:copy.deepcopy(v) for k,v in batch.items() if k!='batch_sha256'}
    batch['batch_sha256']=sha256(canon(material))
    out['source_snapshot_original_sha256']=sha256(canon(items))
    return canon(out)

def _next_workspace(runtime_root:Path,index:int,cycle:int)->Path:
    return runtime_root/f'item-{index}-repair-{cycle}'

def _restart_parent_metadata(workspace:Path,state:dict[str,Any],route:dict[str,Any])->dict[str,Any]:
    runtime_root=workspace.parent
    m=re.fullmatch(r'item-(\d+)(?:-repair-\d+)?',workspace.name)
    if not m: raise RepairRouteError('REPAIR_WORKSPACE_NAME_INVALID')
    index=int(m.group(1))
    cycle=int(state.get('machine_repair_cycle') or 0)+1
    if cycle>MAX_MACHINE_REPAIR_CYCLES: raise RepairRouteError('MACHINE_REPAIR_CYCLE_LIMIT')
    point0_path=runtime_root/f'point0-{index}.json'
    if not point0_path.is_file():
        candidates=sorted(runtime_root.glob(f'point0-{index}-repair-*.json'))
        if not candidates: raise RepairRouteError('REPAIR_POINT0_SOURCE_MISSING')
        point0_path=candidates[-1]
    old_point0,prod,_=_decode_point0(point0_path)
    batch=prod.get('next_textmachine_metadata_batch')
    items=batch.get('items') if isinstance(batch,dict) else None
    if not isinstance(items,list) or index>=len(items): raise RepairRouteError('REPAIR_BATCH_ITEM_MISSING')
    item=copy.deepcopy(items[index])
    original=copy.deepcopy(item)
    finding=route['finding']
    if route['target']=='TITLE_BINDING':
        candidate=_punctuation_repairs(str(item.get('title') or ''),finding)
        if not candidate or candidate==item.get('title'):
            request={'contract':CONTRACT,'status':'RETURN_TO_OWNER','owner':'PARENT_METADATA','target':'TITLE_BINDING','reason':'NO_DETERMINISTIC_MACHINE_TITLE_REPAIR','finding':finding,'article':item}
            (workspace/'machine_repair_request.json').write_bytes(canon(request))
            return request
        item['title']=candidate
    else:
        request={'contract':CONTRACT,'status':'RETURN_TO_OWNER','owner':'PARENT_METADATA','target':route['target'],'reason':'AUTHORITATIVE_REBIND_REQUIRED','finding':finding,'article':item}
        (workspace/'machine_repair_request.json').write_bytes(canon(request))
        return request
    new_raw=_rebuild_batch(prod,index,item)
    manifest=root_entry._critical_manifest_sha256(); head=root_entry._git('rev-parse','--verify','HEAD')
    prepared=point0_snapshot.prepare(production_snapshot_bytes=new_raw,root_manifest_sha256=manifest,head_sha=head)
    sources=old_point0['research_runtime']['sources']
    final=point0_snapshot.finalize(prepared,research_provider='SYSTEM4_MACHINE_REPAIR_REBOUND_SNAPSHOT_V1',sources=sources)
    new_point0=runtime_root/f'point0-{index}-repair-{cycle}.json'; new_point0.write_bytes(point0_snapshot.canon(final))
    new_workspace=_next_workspace(runtime_root,index,cycle)
    rc=root_entry.main(['root_entry.py','start-point0',str(new_point0),str(new_workspace),str(index)])
    if rc!=0: raise RepairRouteError('REPAIR_ROOT_RESTART_FAILED:'+str(rc))
    new_state_path=new_workspace/'state.json'; new_state=json.loads(new_state_path.read_text(encoding='utf-8')); new_state['machine_repair_cycle']=cycle; new_state['machine_repair_lineage']={'owner':'PARENT_METADATA','target':route['target'],'from_article':original,'to_article':item,'finding':finding,'previous_workspace':str(workspace)}; new_state_path.write_text(json.dumps(new_state,ensure_ascii=False,indent=2,sort_keys=True),encoding='utf-8')
    result={'contract':CONTRACT,'status':'RESTARTED','owner':'PARENT_METADATA','target':route['target'],'cycle':cycle,'workspace':str(new_workspace),'point0':str(new_point0),'from_article':original,'to_article':item,'finding':finding}
    (workspace/'machine_repair_redirect.json').write_bytes(canon(result)); (runtime_root/f'machine_repair_redirect-{index}.json').write_bytes(canon(result))
    return result

def route(workspace:Path)->dict[str,Any]:
    workspace=Path(workspace)
    state_path=workspace/'state.json'
    if not state_path.is_file(): raise RepairRouteError('REPAIR_STATE_MISSING')
    state=json.loads(state_path.read_text(encoding='utf-8'))
    if state.get('phase')!='REPAIR_REQUIRED': raise RepairRouteError('REPAIR_PHASE_REQUIRED')
    route=classify(state)
    if route['owner']=='DRAFT_BODY':
        return {'contract':CONTRACT,'status':'SAME_ARTICLE_BODY_REPAIR','owner':'DRAFT_BODY','target':'SAME_ARTICLE_BODY','finding':route['finding']}
    if route['owner']=='PARENT_METADATA':
        return _restart_parent_metadata(workspace,state,route)
    request={'contract':CONTRACT,'status':'RETURN_TO_OWNER','owner':route['owner'],'target':route['target'],'reason':'AUTHORITATIVE_REBIND_REQUIRED','finding':route['finding'],'workspace':str(workspace)}
    (workspace/'machine_repair_request.json').write_bytes(canon(request))
    return request
