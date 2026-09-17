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
RETURN_CONTRACT='SYSTEM4_REPAIR_RETURN_V2'
MAX_MACHINE_REPAIR_CYCLES=8
ALLOWED_OWNERS=frozenset({'PARENT_METADATA','CONTEXT_BINDING','RESEARCH_BINDING','DRAFT_BODY'})
GROUP_PRIORITY={
    ('PARENT_METADATA','TITLE_BINDING'):0,
    ('PARENT_METADATA','CATEGORY_BINDING'):1,
    ('PARENT_METADATA','PLAN_SLOT_BINDING'):2,
    ('RESEARCH_BINDING','RESEARCH_OR_FACT_BINDING'):3,
    ('CONTEXT_BINDING','LINK_BINDING'):4,
    ('DRAFT_BODY','SAME_ARTICLE_BODY'):5,
}

class RepairRouteError(RuntimeError):
    pass

def canon(value:Any)->bytes:
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode('utf-8')

def sha256(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()

def _all_findings(state:Mapping[str,Any])->list[dict[str,Any]]:
    checks=state.get('checks') if isinstance(state.get('checks'),Mapping) else {}
    raw=checks.get('findings') if isinstance(checks.get('findings'),list) else []
    findings=[dict(row) for row in raw if isinstance(row,Mapping)]
    if findings:
        return findings
    last=str(state.get('last_error') or '').strip()
    return [{'error_code':last,'reason':last}] if last else []

def _first_finding(state:Mapping[str,Any])->dict[str,Any]:
    findings=_all_findings(state)
    return dict(findings[0]) if findings else {}

def _classify_finding(finding:Mapping[str,Any],state:Mapping[str,Any])->dict[str,Any]:
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
    return {'owner':owner,'target':target,'error_code':code,'field':field,'rule':rule,'finding':dict(finding)}

def _group_sort_key(group:Mapping[str,Any])->tuple[int,str,str]:
    owner=str(group.get('owner') or ''); target=str(group.get('target') or '')
    return (GROUP_PRIORITY.get((owner,target),99),owner,target)

def _group_summary(group:Mapping[str,Any])->dict[str,Any]:
    findings=[dict(row) for row in group.get('findings',[]) if isinstance(row,Mapping)]
    return {'owner':str(group.get('owner') or ''),'target':str(group.get('target') or ''),'finding_count':len(findings),'findings_sha256':sha256(canon(findings))}

def classify(state:Mapping[str,Any])->dict[str,Any]:
    findings=_all_findings(state)
    if not findings:
        findings=[{}]
    classified=[_classify_finding(row,state) for row in findings]
    grouped:dict[tuple[str,str],dict[str,Any]]={}
    for row in classified:
        key=(row['owner'],row['target'])
        group=grouped.setdefault(key,{'owner':row['owner'],'target':row['target'],'classified':[],'findings':[]})
        group['classified'].append(row); group['findings'].append(dict(row['finding']))
    groups=sorted(grouped.values(),key=_group_sort_key)
    active=groups[0]; first=active['classified'][0]
    summaries=[_group_summary(group) for group in groups]
    active_findings=[dict(row) for row in active['findings']]
    return {
        'contract':CONTRACT,
        'owner':active['owner'],
        'target':active['target'],
        'finding':dict(active_findings[0]),
        'findings':active_findings,
        'finding_count':len(active_findings),
        'owner_target_groups':summaries,
        'pending_owner_target_groups':summaries[1:],
        'all_findings':[dict(row) for row in findings],
        'all_finding_count':len(findings),
        'all_findings_sha256':sha256(canon(findings)),
        'error_code':first['error_code'],
        'field':first['field'],
        'rule':first['rule'],
    }

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

def _continuation_envelope(workspace:Path,state:Mapping[str,Any],route:Mapping[str,Any],status:str,reason:str)->dict[str,Any]:
    article=state.get('article') if isinstance(state.get('article'),Mapping) else {}
    cycle=int(state.get('machine_repair_cycle') or 0)+1
    if cycle>MAX_MACHINE_REPAIR_CYCLES:
        raise RepairRouteError('MACHINE_REPAIR_CYCLE_LIMIT')
    findings=[dict(row) for row in route.get('findings',[]) if isinstance(row,Mapping)]
    if not findings:
        finding=dict(route.get('finding') or {})
        findings=[finding] if finding else []
    if not findings:
        raise RepairRouteError('REPAIR_FINDINGS_MISSING')
    all_findings=[dict(row) for row in route.get('all_findings',findings) if isinstance(row,Mapping)]
    if not all_findings:
        raise RepairRouteError('REPAIR_ALL_FINDINGS_MISSING')
    finding=dict(findings[0])
    return {
        'contract':RETURN_CONTRACT,
        'router_contract':CONTRACT,
        'status':status,
        'repairable':True,
        'terminal':False,
        'continuation_required':True,
        'owner':route['owner'],
        'owner_stage':route['owner'],
        'target':route['target'],
        'repair_target':route['target'],
        'reason':reason,
        'finding':finding,
        'finding_sha256':sha256(canon(finding)),
        'findings':findings,
        'finding_count':len(findings),
        'findings_sha256':sha256(canon(findings)),
        'all_findings':all_findings,
        'all_finding_count':len(all_findings),
        'all_findings_sha256':sha256(canon(all_findings)),
        'owner_target_groups':list(route.get('owner_target_groups') or []),
        'pending_owner_target_groups':list(route.get('pending_owner_target_groups') or []),
        'cycle':cycle,
        'max_cycles':MAX_MACHINE_REPAIR_CYCLES,
        'article':dict(article),
        'workspace':str(workspace),
    }

def verify_continuation_result(workspace:Path,result:Mapping[str,Any])->dict[str,Any]:
    if result.get('contract')!=RETURN_CONTRACT:
        raise RepairRouteError('REPAIR_RETURN_CONTRACT_INVALID')
    if result.get('repairable') is not True or result.get('terminal') is not False or result.get('continuation_required') is not True:
        raise RepairRouteError('REPAIR_RETURN_MUST_BE_NONTERMINAL')
    owner=str(result.get('owner') or '')
    if owner not in ALLOWED_OWNERS or result.get('owner_stage')!=owner:
        raise RepairRouteError('REPAIR_RETURN_OWNER_INVALID')
    target=str(result.get('target') or '')
    if not target or result.get('repair_target')!=target:
        raise RepairRouteError('REPAIR_RETURN_TARGET_INVALID')
    finding=result.get('finding')
    if not isinstance(finding,Mapping) or result.get('finding_sha256')!=sha256(canon(dict(finding))):
        raise RepairRouteError('REPAIR_RETURN_FINDING_HASH_INVALID')
    findings=result.get('findings')
    if not isinstance(findings,list) or not findings or not all(isinstance(row,Mapping) for row in findings):
        raise RepairRouteError('REPAIR_RETURN_FINDINGS_INVALID')
    normalized=[dict(row) for row in findings]
    if int(result.get('finding_count') or 0)!=len(normalized):
        raise RepairRouteError('REPAIR_RETURN_FINDING_COUNT_INVALID')
    if result.get('findings_sha256')!=sha256(canon(normalized)):
        raise RepairRouteError('REPAIR_RETURN_FINDINGS_HASH_INVALID')
    if dict(normalized[0])!=dict(finding):
        raise RepairRouteError('REPAIR_RETURN_FIRST_FINDING_MISMATCH')
    all_findings=result.get('all_findings')
    if not isinstance(all_findings,list) or not all_findings or not all(isinstance(row,Mapping) for row in all_findings):
        raise RepairRouteError('REPAIR_RETURN_ALL_FINDINGS_INVALID')
    all_normalized=[dict(row) for row in all_findings]
    if int(result.get('all_finding_count') or 0)!=len(all_normalized):
        raise RepairRouteError('REPAIR_RETURN_ALL_FINDING_COUNT_INVALID')
    if result.get('all_findings_sha256')!=sha256(canon(all_normalized)):
        raise RepairRouteError('REPAIR_RETURN_ALL_FINDINGS_HASH_INVALID')
    remaining=[canon(row) for row in all_normalized]
    for row in normalized:
        encoded=canon(row)
        if encoded not in remaining:
            raise RepairRouteError('REPAIR_RETURN_GROUP_FINDING_NOT_IN_ALL')
        remaining.remove(encoded)
    groups=result.get('owner_target_groups')
    if not isinstance(groups,list) or not groups:
        raise RepairRouteError('REPAIR_RETURN_OWNER_TARGET_GROUPS_INVALID')
    active=groups[0] if isinstance(groups[0],Mapping) else {}
    if active.get('owner')!=owner or active.get('target')!=target:
        raise RepairRouteError('REPAIR_RETURN_ACTIVE_GROUP_MISMATCH')
    if int(active.get('finding_count') or 0)!=len(normalized) or active.get('findings_sha256')!=sha256(canon(normalized)):
        raise RepairRouteError('REPAIR_RETURN_ACTIVE_GROUP_FINDINGS_INVALID')
    pending=result.get('pending_owner_target_groups')
    if not isinstance(pending,list) or pending!=groups[1:]:
        raise RepairRouteError('REPAIR_RETURN_PENDING_GROUPS_INVALID')
    cycle=int(result.get('cycle') or 0)
    if cycle<1 or cycle>MAX_MACHINE_REPAIR_CYCLES or int(result.get('max_cycles') or 0)!=MAX_MACHINE_REPAIR_CYCLES:
        raise RepairRouteError('REPAIR_RETURN_CYCLE_INVALID')
    status=str(result.get('status') or '')
    if status not in {'SAME_ARTICLE_BODY_REPAIR','RETURN_TO_OWNER','RESTARTED'}:
        raise RepairRouteError('REPAIR_RETURN_STATUS_INVALID')
    if status!='RESTARTED' and Path(str(result.get('workspace') or ''))!=Path(workspace):
        raise RepairRouteError('REPAIR_RETURN_WORKSPACE_INVALID')
    return dict(result)

def _write_request(workspace:Path,result:Mapping[str,Any])->None:
    (workspace/'machine_repair_request.json').write_bytes(canon(dict(result)))

def _return_to_owner(workspace:Path,state:Mapping[str,Any],route:Mapping[str,Any],reason:str='AUTHORITATIVE_REBIND_REQUIRED')->dict[str,Any]:
    request=_continuation_envelope(workspace,state,route,'RETURN_TO_OWNER',reason)
    _write_request(workspace,request)
    verify_continuation_result(workspace,request)
    return request

def _same_article_body(workspace:Path,state:Mapping[str,Any],route:Mapping[str,Any])->dict[str,Any]:
    request=_continuation_envelope(workspace,state,route,'SAME_ARTICLE_BODY_REPAIR','SAME_ARTICLE_REPAIR_REQUIRED')
    _write_request(workspace,request)
    verify_continuation_result(workspace,request)
    return request

def _restart_parent_metadata(workspace:Path,state:dict[str,Any],route:dict[str,Any])->dict[str,Any]:
    if route['target']!='TITLE_BINDING':
        return _return_to_owner(workspace,state,route)
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
    candidate=_punctuation_repairs(str(item.get('title') or ''),finding)
    if not candidate or candidate==item.get('title'):
        return _return_to_owner(workspace,state,route,'NO_DETERMINISTIC_MACHINE_TITLE_REPAIR')
    item['title']=candidate
    new_raw=_rebuild_batch(prod,index,item)
    manifest=root_entry._critical_manifest_sha256(); head=root_entry._git('rev-parse','--verify','HEAD')
    prepared=point0_snapshot.prepare(production_snapshot_bytes=new_raw,root_manifest_sha256=manifest,head_sha=head)
    sources=old_point0['research_runtime']['sources']
    final=point0_snapshot.finalize(prepared,research_provider='SYSTEM4_MACHINE_REPAIR_REBOUND_SNAPSHOT_V1',sources=sources)
    new_point0=runtime_root/f'point0-{index}-repair-{cycle}.json'; new_point0.write_bytes(point0_snapshot.canon(final))
    new_workspace=_next_workspace(runtime_root,index,cycle)
    rc=root_entry.main(['root_entry.py','start-point0',str(new_point0),str(new_workspace),str(index)])
    if rc!=0: raise RepairRouteError('REPAIR_ROOT_RESTART_FAILED:'+str(rc))
    new_state_path=new_workspace/'state.json'; new_state=json.loads(new_state_path.read_text(encoding='utf-8')); new_state['machine_repair_cycle']=cycle; new_state['machine_repair_lineage']={'owner':'PARENT_METADATA','target':route['target'],'from_article':original,'to_article':item,'finding':finding,'findings':list(route.get('findings') or []),'previous_workspace':str(workspace)}; new_state_path.write_text(json.dumps(new_state,ensure_ascii=False,indent=2,sort_keys=True),encoding='utf-8')
    result=_continuation_envelope(workspace,state,route,'RESTARTED','DETERMINISTIC_PARENT_METADATA_REPAIR_APPLIED')
    result.update({'cycle':cycle,'workspace':str(new_workspace),'point0':str(new_point0),'from_article':original,'to_article':item})
    verify_continuation_result(workspace,result)
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
        return _same_article_body(workspace,state,route)
    if route['owner']=='PARENT_METADATA':
        return _restart_parent_metadata(workspace,state,route)
    return _return_to_owner(workspace,state,route)
