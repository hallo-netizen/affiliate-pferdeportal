from __future__ import annotations
import copy,json
from pathlib import Path

import controller,point0_snapshot,root_entry,supervisor
from live_route_test_support import head,production_snapshot_bytes,write_json
from real_source_fixture import source_and_claims


def start_to_context_real(base:Path,index:int):
    raw=production_snapshot_bytes(3)
    snapshot=base/'production-snapshot.json'
    snapshot.write_bytes(raw)
    metadata=json.loads(raw.decode('utf-8'))['next_textmachine_metadata_batch']['items'][index]
    src,claims=source_and_claims(index,metadata['target_keyword'])
    prepared=point0_snapshot.prepare(
        production_snapshot_bytes=raw,
        root_manifest_sha256=root_entry._critical_manifest_sha256(),
        head_sha=head(),
    )
    p0=point0_snapshot.finalize(
        prepared,
        research_provider='PARENT_CHAT_REAL_WEB_SNAPSHOT',
        sources=[src],
    )
    p0p=base/f'point0-real-{index}.json'
    p0p.write_bytes(point0_snapshot.canon(p0))
    workspace=base/f'real-item-{index}'
    rc=root_entry.main(['root_entry.py','start-point0',str(p0p),str(workspace),str(index)])
    if rc!=0:
        raise AssertionError('ROOT_POINT0_REAL_SOURCE_FAILED:'+str(index))
    research=supervisor.expected_research_document(workspace)
    rp=write_json(base/f'research-real-{index}.json',research)
    if controller.main(['controller.py','research',str(workspace),str(rp)])!=0:
        raise AssertionError('REAL_RESEARCH_FAILED:'+str(index))
    facts_doc={'contract':'SYSTEM4_FACTS_EVIDENCE_V1','claims':copy.deepcopy(claims)}
    fp=write_json(base/f'facts-real-{index}.json',facts_doc)
    if controller.main(['controller.py','facts',str(workspace),str(fp)])!=0:
        raise AssertionError('REAL_FACTS_FAILED:'+str(index))
    state=json.loads((workspace/'state.json').read_text(encoding='utf-8'))
    source_sha=state['source_snapshot_sha256']
    pack_claims=[]
    for row in claims:
        enriched=copy.deepcopy(row)
        enriched['claim_status']='FULLY_SUPPORTED'
        enriched['article_types']=[state['article']['article_type']]
        pack_claims.append(enriched)
    pack={
        'contract':'canonical_fact_pack_v1',
        'status':'SOURCE_VERIFIED_PRODUCTION_READY',
        'source_snapshot_id':source_sha,
        'fact_pack_id':source_sha,
        'sources':copy.deepcopy(research['sources']),
        'claims':pack_claims,
    }
    ids=[row['fact_id'] for row in claims]
    a=state['article']
    plan={
        'article_type':a['article_type'],
        'target_keyword':a['target_keyword'],
        'topic':a['title'],
        'source_snapshot_id':source_sha,
        'runtime_order':{
            'order_id':f'real-route-{index}',
            'article_type':a['article_type'],
            'title':a['title'],
            'slug':f'real-route-{index}',
            'subject_scope':'real_source_corridor',
            'subject_label':a['target_keyword'],
            'lead':'Gebundener Einstieg ausschließlich aus dem realen Quellensnapshot.',
            'conclusion':'Gebundener Abschluss ausschließlich aus dem realen Quellensnapshot.',
            'allowed_fact_ids':ids,
        },
    }
    pp=write_json(base/f'pack-real-{index}.json',pack)
    pl=write_json(base/f'plan-real-{index}.json',plan)
    if controller.main(['controller.py','context',str(workspace),str(pp),str(pl)])!=0:
        raise AssertionError('REAL_CONTEXT_FAILED:'+str(index))
    state=json.loads((workspace/'state.json').read_text(encoding='utf-8'))
    if state['phase']!='DRAFT_REQUIRED':
        raise AssertionError('REAL_DRAFT_REQUIRED_NOT_REACHED')
    return workspace,snapshot,state
