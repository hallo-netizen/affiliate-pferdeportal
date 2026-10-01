import json
from collections import Counter
from pathlib import Path
from .core import ROOT, load_catalog

MAP_PATH=ROOT/'PPM_PARITY_MAP.json'
INV_PATH=ROOT/'evidence/PPM679_EXACT_104_RULE_INVENTORY.json'
EXPECTED_PPM_SHA='acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1'
ALLOWED_ACTIONS={'PRESERVE','SUPERSEDED_BY_USER_APPROVED_K10_TABLE_POLICY'}
EXPECTED_SUPERSEDED={
    'BLOCKED_CONTENT_TABLE_COUNT',
    'BLOCKED_CONTENT_REQUIRED_TABLE_MISSING',
    'BLOCKED_CONTENT_FORBIDDEN_TABLE_PRESENT',
}

def verify():
    findings=[]
    try:
        mapping=json.loads(MAP_PATH.read_text(encoding='utf-8'))
        inventory=json.loads(INV_PATH.read_text(encoding='utf-8'))
        catalog=load_catalog()
    except Exception as exc:
        return {'status':'BLOCKED','findings':['PPM_PARITY_LOAD_FAILED:'+type(exc).__name__]}

    if mapping.get('contract')!='K10_PPM679_104_PARITY_MAP_V1':
        findings.append('PPM_PARITY_CONTRACT_INVALID')
    if inventory.get('contract')!='K10_PPM679_EXACT_104_RULE_INVENTORY_V2':
        findings.append('PPM_INVENTORY_CONTRACT_INVALID')
    if mapping.get('source_package_sha256')!=EXPECTED_PPM_SHA or inventory.get('package_sha256')!=EXPECTED_PPM_SHA:
        findings.append('PPM_SOURCE_HASH_MISMATCH')

    entries=mapping.get('entries') if isinstance(mapping.get('entries'),list) else []
    inv_rules=inventory.get('rules') if isinstance(inventory.get('rules'),list) else []
    if len(entries)!=104: findings.append('PPM_PARITY_COUNT_INVALID:'+str(len(entries)))
    if len(inv_rules)!=104: findings.append('PPM_INVENTORY_COUNT_INVALID:'+str(len(inv_rules)))
    mids=[str(x.get('legacy_rule_id') or '') for x in entries]
    iids=[str(x.get('legacy_rule_id') or '') for x in inv_rules]
    if len(set(mids))!=104 or '' in mids: findings.append('PPM_PARITY_LEGACY_ID_DUPLICATE_OR_EMPTY')
    if set(mids)!=set(iids): findings.append('PPM_PARITY_INVENTORY_SET_MISMATCH')

    classes=Counter(str(x.get('legacy_classification') or '') for x in entries)
    if classes!=Counter({'REPAIRABLE_CONTENT':89,'HARD_INTEGRITY':15}):
        findings.append('PPM_PARITY_CLASS_PARTITION_INVALID:'+repr(dict(classes)))
    actions=Counter(str(x.get('parity_action') or '') for x in entries)
    if set(actions)-ALLOWED_ACTIONS:
        findings.append('PPM_PARITY_ACTION_UNKNOWN:'+repr(dict(actions)))
    superseded={str(x.get('error_code') or '') for x in entries if x.get('parity_action')=='SUPERSEDED_BY_USER_APPROVED_K10_TABLE_POLICY'}
    if superseded!=EXPECTED_SUPERSEDED:
        findings.append('PPM_PARITY_APPROVED_TABLE_CHANGE_SET_INVALID:'+repr(sorted(superseded)))

    catalog_rows={r.get('id'):r for r in catalog.get('rules',[]) if isinstance(r,dict)}
    for x in entries:
        rid=str(x.get('canonical_rule_id') or '')
        row=catalog_rows.get(rid)
        if not row:
            findings.append('PPM_PARITY_TARGET_RULE_MISSING:'+rid); continue
        if row.get('classification')!='HARD': findings.append('PPM_PARITY_TARGET_NOT_HARD:'+rid)
        if row.get('owner')!=x.get('canonical_owner'): findings.append('PPM_PARITY_OWNER_MISMATCH:'+rid)
        if row.get('scope')!=x.get('canonical_scope'): findings.append('PPM_PARITY_SCOPE_MISMATCH:'+rid)
        if row.get('implementation_status')!='IMPLEMENTED': findings.append('PPM_PARITY_TARGET_NOT_IMPLEMENTED:'+rid)

    return {
        'status':'PASS' if not findings else 'BLOCKED',
        'findings':findings,
        'legacy_rule_count':len(entries),
        'unique_canonical_rules':len({x.get('canonical_rule_id') for x in entries}),
        'repairable_content_count':classes.get('REPAIRABLE_CONTENT',0),
        'hard_integrity_count':classes.get('HARD_INTEGRITY',0),
        'approved_table_policy_changes':len(superseded),
    }
