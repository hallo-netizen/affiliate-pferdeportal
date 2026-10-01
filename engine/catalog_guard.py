from collections import Counter
from .core import load_catalog

VALID_SCOPES={'ARTICLE','SYSTEM','PACKAGE_INTEGRITY'}

def validate_catalog():
    catalog=load_catalog(); rules=catalog['rules']; findings=[]
    ids=[r['id'] for r in rules]
    dup=[k for k,v in Counter(ids).items() if v>1]
    if dup: findings.append('K10_DUPLICATE_RULE_ID:'+','.join(sorted(dup)))
    for r in rules:
        if r.get('classification')=='HARD':
            if not str(r.get('owner') or '').strip(): findings.append('K10_HARD_RULE_WITHOUT_OWNER:'+r['id'])
            if not str(r.get('check_stage') or '').strip(): findings.append('K10_HARD_RULE_WITHOUT_STAGE:'+r['id'])
            if r.get('scope') not in VALID_SCOPES: findings.append('K10_HARD_RULE_SCOPE_INVALID:'+r['id'])
            if r.get('implementation_status')!='IMPLEMENTED': findings.append('K10_HARD_RULE_NOT_IMPLEMENTED:'+r['id'])
    return {'status':'PASS' if not findings else 'BLOCKED','findings':findings,'hard_rule_count':sum(r.get('classification')=='HARD' for r in rules)}
