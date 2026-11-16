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

# Additional article types are append-only, isolated rule packages. The four
# historical types and their sealed writer-job hashes remain byte-identical.
TYPE_SHELF=ROOT/'ARTIKELTYPEN'
TYPE_PACKAGE_CONTRACT='K0_ARTICLE_TYPE_RULE_PACKAGE_V1'

def _type_package(name):
    import re
    if not isinstance(name,str) or not re.fullmatch(r'[A-Za-zÄÖÜäöüß][A-Za-z0-9ÄÖÜäöüß _-]{0,59}',name):
        raise ValueError('K0_TYPE_NAME_INVALID')
    path=TYPE_SHELF/(name+'.json')
    if not path.is_file():
        return None
    try:
        data=json.loads(path.read_text(encoding='utf-8'))
    except (ValueError,OSError) as exc:
        raise ValueError('K0_TYPE_PACKAGE_UNREADABLE:'+name) from exc
    if not isinstance(data,dict) or data.get('contract')!=TYPE_PACKAGE_CONTRACT or data.get('article_type')!=name or data.get('inherit_global_rules') is not True:
        raise ValueError('K0_TYPE_PACKAGE_IDENTITY_INVALID:'+name)
    if data.get('status')!='READY':
        raise ValueError('K0_TYPE_NOT_READY:'+name+':'+str(data.get('status')))
    boundary=data.get('intent_boundary')
    if not isinstance(boundary,dict) or not all(isinstance(boundary.get(k),str) and boundary[k].strip() for k in ('primary_goal_code','primary_goal','outside_scope')):
        raise ValueError('K0_TYPE_INTENT_BOUNDARY_INCOMPLETE:'+name)
    cfg=data.get('rules')
    required=('required_blocks','required_lists','fact_trace_required_blocks','type_meta_schema','conclusion_min_ratio','table_policy')
    if not isinstance(cfg,dict) or any(k not in cfg for k in required):
        raise ValueError('K0_TYPE_RULES_INCOMPLETE:'+name)
    if any(not isinstance(cfg[k],list) or not cfg[k] or len(cfg[k])!=len(set(cfg[k])) for k in ('required_blocks','required_lists','fact_trace_required_blocks')):
        raise ValueError('K0_TYPE_RULE_LISTS_INVALID:'+name)
    if not set(cfg['fact_trace_required_blocks'])-{'table'} <= set(cfg['required_blocks']):
        raise ValueError('K0_TYPE_FACT_BLOCKS_NOT_BOUND:'+name)
    schema=cfg['type_meta_schema']
    if not isinstance(schema,dict) or not isinstance(schema.get('fields'),dict) or not isinstance(schema.get('required'),list) or not schema['required'] or not set(schema['required'])<=set(schema['fields']):
        raise ValueError('K0_TYPE_METADATA_SCHEMA_INCOMPLETE:'+name)
    for field,spec in schema['fields'].items():
        if not isinstance(spec,dict) or spec.get('type') not in ('list','string'):
            raise ValueError('K0_TYPE_METADATA_FIELD_INVALID:'+name+':'+str(field))
        if spec.get('type')=='list' and (not isinstance(spec.get('min_items'),int) or spec['min_items']<1):
            raise ValueError('K0_TYPE_METADATA_FIELD_INVALID:'+name+':'+str(field))
        if spec.get('type')=='string' and (not isinstance(spec.get('min_length'),int) or spec['min_length']<1):
            raise ValueError('K0_TYPE_METADATA_FIELD_INVALID:'+name+':'+str(field))
    if cfg['table_policy'] not in ('REQUIRED','REQUIRED_UNLESS_EXCEPTION','OPTIONAL'):
        raise ValueError('K0_TYPE_TABLE_POLICY_INVALID:'+name)
    if not isinstance(cfg['conclusion_min_ratio'],(int,float)) or not 0<cfg['conclusion_min_ratio']<0.25:
        raise ValueError('K0_TYPE_CONCLUSION_RATIO_INVALID:'+name)
    return cfg

def load_values(article_type=None):
    data=json.loads(VALUES_PATH.read_text(encoding='utf-8'))
    if data.get('contract')!='K10_RULE_VALUES_V1':
        raise ValueError('K10_RULE_VALUES_CONTRACT_INVALID')
    if article_type is not None and article_type not in data['types']:
        definition=_type_package(article_type)
        if definition is None:
            raise ValueError('K0_TYPE_NOT_DEFINED:'+str(article_type))
        # Only the requested type is added to this job's sealed rule snapshot.
        # Registering any other type cannot change this article's rule hash.
        data['types'][article_type]=definition
        data['table']['presence_policy'][article_type]=definition['table_policy']
    return data

def catalog_hash():
    return stable(load_catalog())

def values_hash(article_type=None):
    return stable(load_values(article_type))

def hard_rules(scope=None):
    rows=[r for r in load_catalog()['rules'] if r['classification']=='HARD']
    if scope is not None:
        rows=[r for r in rows if r.get('scope')==scope]
    return rows
