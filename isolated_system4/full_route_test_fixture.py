from __future__ import annotations
import copy,hashlib,json
from pathlib import Path

import root_entry
from live_route_test_support import LIVE,canon
from new_topic_real_source_fixture import source_and_claims

SINGLE_ITEMS=[{
    'article_type':'Beratung',
    'category':'pferdehaftpflicht-beratung',
    'plan_slot':'0063dc0f27259aa6a39a2fcdf1475a1617181286e2aeb4c30b96bb9f37ceec47',
    'target_keyword':'Pferdehaftpflicht für Fremdreiter',
    'title':'Pferdehaftpflicht für Fremdreiter richtig prüfen',
}]

THREE_ITEMS=[
    {
        'article_type':'Beratung',
        'category':'fliegenmasken-beratung',
        'plan_slot':'65f2c06e7f246c49617b57bbc56cea940cb3bd566722bd423cfd433eb313a56e',
        'target_keyword':'UV-Schutz bei Fliegenmasken',
        'title':'UV-Schutz bei Fliegenmasken für Pferde prüfen',
    },
    {
        'article_type':'Beratung',
        'category':'pellets-beratung',
        'plan_slot':'d524a4f24316bdd37a25341a3a4918681b598c9b676b09355ce8ca593ada305e',
        'target_keyword':'Pellets aus Luzerne als Heuersatz',
        'title':'Pellets aus Luzerne als Heuersatz für Pferde einordnen',
    },
    {
        'article_type':'Beratung',
        'category':'pferdehaftpflicht-beratung',
        'plan_slot':'7d965ba06f9027a5497291a31345f7f78e166e1e9a2776ef17caeea0d02b5f0b',
        'target_keyword':'Pferdehaftpflicht für Pferdehüter',
        'title':'Pferdehaftpflicht für Pferdehüter richtig prüfen',
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
