import json
from pathlib import Path
from .core import load_catalog
from .field_coverage import audit
ROOT=Path(__file__).resolve().parents[1]

def verify():
    findings=[]
    catalog=load_catalog()
    entries={r['id']:r for r in catalog['rules']}
    coverage=audit()
    if coverage['status']!='PASS':
        findings.append('FIELD_COVERAGE_NOT_PASS')
    required={r['rule_id']:(r['owner']) for r in coverage['rows'] if r.get('classification')=='HARD' and r.get('rule_id')}
    for rid,owner in sorted(required.items()):
        if rid not in entries:
            findings.append('HARD_RULE_MISSING_FROM_CATALOG:'+rid)
        elif entries[rid].get('owner')!=owner:
            findings.append('HARD_RULE_OWNER_MISMATCH:'+rid)
    hard_entries=[r for r in catalog['rules'] if r.get('classification')=='HARD']
    ids=[r['id'] for r in hard_entries]
    if len(ids)!=len(set(ids)):
        findings.append('DUPLICATE_HARD_RULE_ID')
    return {'status':'PASS' if not findings else 'BLOCKED','findings':findings,'required_rule_ids':sorted(required)}
