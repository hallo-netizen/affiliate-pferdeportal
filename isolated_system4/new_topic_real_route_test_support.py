from __future__ import annotations
import copy,hashlib,json,re
from pathlib import Path

import authoring_contract,controller,point0_snapshot,root_entry,supervisor
from live_route_test_support import LIVE,canon,head,write_json
from new_topic_real_source_fixture import source_and_claims
from real_route_test_support import valid_real_article as _valid_real_article

NEW_ITEMS=[
    {
        'article_type':'Beratung',
        'category':'pferdehaftpflicht-beratung',
        'plan_slot':'5ee07d4ca0aed6c411eea9f52f89fc33cdd53de2ad93a9b25cb77f8ed0a9417c',
        'target_keyword':'Pferdehaftpflicht bei Reitbeteiligung',
        'title':'Pferdehaftpflicht bei Reitbeteiligung richtig prüfen',
    },
    {
        'article_type':'Beratung',
        'category':'fliegenmasken-beratung',
        'plan_slot':'8c006e3b323fe839ca560aa61e837eb11f9350b79173767a58c25d01210fbb72',
        'target_keyword':'Fliegenmaske mit UV-Schutz',
        'title':'Fliegenmaske mit UV-Schutz für Pferde auswählen',
    },
    {
        'article_type':'Beratung',
        'category':'pellets-beratung',
        'plan_slot':'c1f48c8f76ba397cdecc3c542d79ecc4c9efd6e65e176ebe47b8123ced68a924',
        'target_keyword':'Pellets aus Luzerne für Pferde',
        'title':'Pellets aus Luzerne für Pferde sinnvoll auswählen',
    },
]


def new_topic_snapshot_bytes()->bytes:
    value=json.loads(LIVE.read_text(encoding='utf-8'))
    batch=value['next_textmachine_metadata_batch']
    batch['items']=copy.deepcopy(NEW_ITEMS)
    batch['item_count']=3
    material={k:copy.deepcopy(v) for k,v in batch.items() if k!='batch_sha256'}
    batch['batch_sha256']=hashlib.sha256(canon(material)).hexdigest()
    value['source_snapshot_original_sha256']=hashlib.sha256(canon(NEW_ITEMS)).hexdigest()
    value['system4_root_manifest_sha256']=root_entry._critical_manifest_sha256()
    return canon(value)


def start_to_context_new_topic(base:Path,index:int):
    raw=new_topic_snapshot_bytes()
    snapshot=base/'new-topic-production-snapshot.json'
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
    p0p=base/f'point0-new-topic-{index}.json'
    p0p.write_bytes(point0_snapshot.canon(p0))
    workspace=base/f'new-topic-item-{index}'
    rc=root_entry.main(['root_entry.py','start-point0',str(p0p),str(workspace),str(index)])
    if rc!=0:
        raise AssertionError('ROOT_POINT0_NEW_TOPIC_FAILED:'+str(index))
    research=supervisor.expected_research_document(workspace)
    rp=write_json(base/f'research-new-topic-{index}.json',research)
    if controller.main(['controller.py','research',str(workspace),str(rp)])!=0:
        raise AssertionError('NEW_TOPIC_RESEARCH_FAILED:'+str(index))
    facts_doc={'contract':'SYSTEM4_FACTS_EVIDENCE_V1','claims':copy.deepcopy(claims)}
    fp=write_json(base/f'facts-new-topic-{index}.json',facts_doc)
    if controller.main(['controller.py','facts',str(workspace),str(fp)])!=0:
        raise AssertionError('NEW_TOPIC_FACTS_FAILED:'+str(index))
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
            'order_id':f'new-topic-real-route-{index}',
            'article_type':a['article_type'],
            'title':a['title'],
            'slug':f'new-topic-real-route-{index}',
            'subject_scope':'new_topic_real_source_corridor',
            'subject_label':a['target_keyword'],
            'lead':'Gebundener Einstieg ausschließlich aus dem neuen realen Quellenstand.',
            'conclusion':'Gebundener Abschluss ausschließlich aus dem neuen realen Quellenstand.',
            'allowed_fact_ids':ids,
        },
    }
    pp=write_json(base/f'pack-new-topic-{index}.json',pack)
    pl=write_json(base/f'plan-new-topic-{index}.json',plan)
    if controller.main(['controller.py','context',str(workspace),str(pp),str(pl)])!=0:
        raise AssertionError('NEW_TOPIC_CONTEXT_FAILED:'+str(index))
    state=json.loads((workspace/'state.json').read_text(encoding='utf-8'))
    if state['phase']!='DRAFT_REQUIRED':
        raise AssertionError('NEW_TOPIC_DRAFT_REQUIRED_NOT_REACHED')
    return workspace,snapshot,state


def valid_real_article(state:dict,index:int)->str:
    article=_valid_real_article(state,index)
    if index!=2:
        return article
    pattern=re.compile(r'(<section data-block="conclusion">.*?)(</section>)',re.S)
    match=pattern.search(article)
    if not match:
        raise AssertionError('NEW_TOPIC_CONCLUSION_BLOCK_MISSING')
    section=match.group(1)
    addition=' Zusätzlich bleibt für Pellets aus Luzerne für Pferde der gebundene Quellenstand maßgeblich; weitergehende Tatsachen werden im Fazit ausdrücklich nicht ergänzt.'
    last_p=section.rfind('</p>')
    if last_p<0:
        raise AssertionError('NEW_TOPIC_CONCLUSION_PARAGRAPH_MISSING')
    section=section[:last_p]+addition+section[last_p:]
    article=article[:match.start(1)]+section+article[match.end(1):]
    authoring_contract.validate_candidate(article,state['authoring_contract'])
    return article
