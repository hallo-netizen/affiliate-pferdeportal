from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

FIVE_FIELDS=('article_type','category','plan_slot','target_keyword','title')

class Blocked(RuntimeError):
    pass

def stable(obj):
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':'))

def load(path):
    x=json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(x,dict):
        raise Blocked('JSON_OBJECT_REQUIRED')
    return x

def validate_intake(x):
    if x.get('contract')!='PSERC_TEXTMACHINE_METADATA_BATCH_V2':
        raise Blocked('INTAKE_CONTRACT_INVALID')
    if x.get('status')!='READY_FOR_TEXTMACHINE_METADATA_INTAKE':
        raise Blocked('INTAKE_STATUS_INVALID')
    if x.get('content_or_format_payload_present') is not False:
        raise Blocked('INTAKE_CONTENT_PAYLOAD_FORBIDDEN')
    if x.get('publish_allowed') is not False:
        raise Blocked('PUBLISH_ALLOWED_MUST_BE_FALSE')
    rows=x.get('items')
    if not isinstance(rows,list) or not rows or x.get('item_count')!=len(rows):
        raise Blocked('INTAKE_ITEMS_INVALID')
    for i,row in enumerate(rows):
        if not isinstance(row,dict) or set(row)!=set(FIVE_FIELDS):
            raise Blocked('INTAKE_NOT_EXACT_FIVE_FIELDS:'+str(i))
        if any(not isinstance(row[k],str) or not row[k].strip() for k in FIVE_FIELDS):
            raise Blocked('INTAKE_FIELD_INVALID:'+str(i))
    core=dict(x); declared=str(core.pop('batch_sha256',''))
    actual=hashlib.sha256(stable(core).encode('utf-8')).hexdigest()
    if declared!=actual:
        raise Blocked('INTAKE_BATCH_SHA256_MISMATCH')
    return rows

def match_profile(category,profiles):
    hits=[]
    for p in profiles:
        exact=set(p.get('category_exact') or [])
        prefixes=tuple(p.get('category_prefixes') or [])
        if category in exact or (prefixes and category.startswith(prefixes)):
            hits.append(p)
    if len(hits)!=1:
        raise Blocked('PORTAL_ASSIGNMENT_NOT_UNIQUE:'+category+':'+str(len(hits)))
    return hits[0]

def resolve(intake,registry):
    rows=validate_intake(intake)
    if registry.get('contract')!='K0_PORTAL_REGISTRY_V1':
        raise Blocked('PORTAL_REGISTRY_CONTRACT_INVALID')
    profiles=registry.get('profiles') or []
    out=[]
    for row in rows:
        p=match_profile(row['category'],profiles)
        out.append({
          'portal_id':p['portal_id'],
          'portal_name':p['display_name'],
          'status':'AUTO_DETECTED',
          'basis':'category:'+row['category'],
          'job_identity':{k:row[k] for k in FIVE_FIELDS}
        })
    return {
      'contract':'K0_PORTAL_ASSIGNMENT_V1',
      'status':'PASS',
      'source_batch_sha256':intake['batch_sha256'],
      'item_count':len(out),
      'items':out,
      'publish_allowed':False
    }

def main():
    try:
        out=resolve(load(sys.argv[1]),load(sys.argv[2]))
        print(json.dumps(out,ensure_ascii=False,indent=2))
    except Blocked as exc:
        print(json.dumps({'contract':'K0_PORTAL_ASSIGNMENT_V1','status':'BLOCKED','reason':str(exc),'publish_allowed':False},ensure_ascii=False,indent=2))
        raise SystemExit(2)

if __name__=='__main__':
    main()
