from __future__ import annotations
import copy,hashlib,json
from pathlib import Path

import root_entry
from live_route_test_support import LIVE,canon
from new_topic_real_source_fixture import source_and_claims

SINGLE_ITEMS=[{
    'article_type':'Beratung',
    'category':'pferdehaftpflicht-beratung',
    'plan_slot':'b016d8743a04a42fcc67e734400202051a2f1fc0efa04472b9ce0a190236fdf7',
    'target_keyword':'Haftpflicht für Pferde bei Pflegebeteiligung',
    'title':'Haftpflicht für Pferde bei Pflegebeteiligung richtig prüfen',
}]

THREE_ITEMS=[
    {
        'article_type':'Beratung',
        'category':'fliegenmasken-beratung',
        'plan_slot':'992812013cee4eac3315ce699a1fe8f2ca901944b4d7b32adf40a825f8ebe373',
        'target_keyword':'Fliegenmasken für Pferde an sonnigen Tagen',
        'title':'Fliegenmasken für Pferde an sonnigen Tagen richtig auswählen',
    },
    {
        'article_type':'Beratung',
        'category':'pellets-beratung',
        'plan_slot':'b96182343e8d14acecab1278046479b4edf8cfda5dcffe4fe1781443c3c7fc5b',
        'target_keyword':'Pellets aus Luzerne für Pferde im Winter',
        'title':'Pellets aus Luzerne für Pferde im Winter einordnen',
    },
    {
        'article_type':'Beratung',
        'category':'pferdehaftpflicht-beratung',
        'plan_slot':'7b2ffe9557f23e6f290f7e3b22d39a76f893cc5961840c37391e05a87573b320',
        'target_keyword':'Haftpflicht für Pferde bei Betreuung im Urlaub',
        'title':'Haftpflicht für Pferde bei Betreuung im Urlaub richtig prüfen',
    },
]

CATEGORY_SOURCE_INDEX={
    'pferdehaftpflicht-beratung':0,
    'fliegenmasken-beratung':1,
    'pellets-beratung':2,
}

def _snapshot(items:list[dict])->dict:
    value=json.loads(LIVE.read_text(encoding='utf-8'))
    batch=value['next_textmachine_metadata_batch']; batch['items']=copy.deepcopy(items); batch['item_count']=len(items); batch['publish_allowed']=False
    material={k:copy.deepcopy(v) for k,v in batch.items() if k!='batch_sha256'}
    batch['batch_sha256']=hashlib.sha256(canon(material)).hexdigest()
    value['source_snapshot_original_sha256']=hashlib.sha256(canon(items)).hexdigest()
    value['system4_root_manifest_sha256']=root_entry._critical_manifest_sha256()
    return value

def write_start_fixture(root:Path,items:list[dict]):
    snapshot=root/'start-snapshot.json'; snapshot.write_bytes(canon(_snapshot(items)))
    articles=[]
    for item in items:
        src,_=source_and_claims(CATEGORY_SOURCE_INDEX[item['category']],item['target_keyword'])
        articles.append({'sources':[src]})
    sources=root/'start-sources.json'; sources.write_bytes(canon({'contract':'SYSTEM4_FULL_ROUTE_TEST_SOURCES_V1','articles':articles}))
    return snapshot,sources

def source_claims_for_article(article:dict):
    idx=CATEGORY_SOURCE_INDEX[article['category']]
    return source_and_claims(idx,article['target_keyword'])
