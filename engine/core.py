import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CATALOG_PATH=ROOT/'RULE_CATALOG.json'
VALUES_PATH=ROOT/'RULE_VALUES.json'

def stable(obj):
    return hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def load_catalog():
    data=json.loads(CATALOG_PATH.read_text(encoding='utf-8'))
    if data.get('contract')!='K10_CENTRAL_RULE_CATALOG_V2':
        raise ValueError('K10_CATALOG_CONTRACT_INVALID')
    return data

def load_values():
    data=json.loads(VALUES_PATH.read_text(encoding='utf-8'))
    if data.get('contract')!='K10_RULE_VALUES_V1':
        raise ValueError('K10_RULE_VALUES_CONTRACT_INVALID')
    return data

def catalog_hash():
    return stable(load_catalog())

def values_hash():
    return stable(load_values())

def hard_rules(scope=None):
    rows=[r for r in load_catalog()['rules'] if r['classification']=='HARD']
    if scope is not None:
        rows=[r for r in rows if r.get('scope')==scope]
    return rows
