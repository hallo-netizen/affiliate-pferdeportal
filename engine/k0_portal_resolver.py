from __future__ import annotations
import csv, hashlib, io, json, subprocess, sys
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

def _central_category_slugs(source):
    if source!='refs/remotes/origin/affiliate-release-current:CATEGORY_INTEGRATION_HOBBYRAUM/PFERDEPORTAL_KATEGORIEN/KATEGORIEN.tsv':
        raise Blocked('PORTAL_CATEGORY_SOURCE_UNAUTHORIZED')
    try:
        run=subprocess.run(['git','show',source],cwd=Path(__file__).resolve().parents[1],capture_output=True,text=True,timeout=15)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise Blocked('PORTAL_CATEGORY_SOURCE_UNAVAILABLE') from exc
    if run.returncode!=0:
        raise Blocked('PORTAL_CATEGORY_SOURCE_UNAVAILABLE')
    reader=csv.DictReader(io.StringIO(run.stdout),delimiter='\t')
    if reader.fieldnames!=['term_id','slug','name','parent_slug']:
        raise Blocked('PORTAL_CATEGORY_SOURCE_SCHEMA_INVALID')
    slugs=set()
    for row in reader:
        slug=str(row.get('slug') or '').strip()
        term_id=str(row.get('term_id') or '').strip()
        if not slug or slug in slugs or not term_id.isdecimal() or int(term_id)<1:
            raise Blocked('PORTAL_CATEGORY_SOURCE_ROW_INVALID')
        slugs.add(slug)
    if not slugs:
        raise Blocked('PORTAL_CATEGORY_SOURCE_EMPTY')
    return slugs

def wordpress_site_for_portal(registry,portal_id):
    """Resolve only the exact portal's configured WordPress origin; never fall back."""
    from urllib.parse import urlsplit
    profiles=registry.get('profiles') if isinstance(registry,dict) else None
    matches=[p for p in (profiles or []) if isinstance(p,dict) and p.get('portal_id')==portal_id]
    if len(matches)!=1:
        raise Blocked('PORTAL_WORDPRESS_PROFILE_NOT_UNIQUE:'+str(portal_id))
    raw=matches[0].get('wordpress_base_url')
    if not isinstance(raw,str) or not raw:
        raise Blocked('PORTAL_WORDPRESS_SITE_NOT_CONFIGURED:'+str(portal_id))
    parsed=urlsplit(raw)
    if parsed.scheme!='https' or not parsed.hostname or parsed.path not in ('','/') or parsed.query or parsed.fragment or parsed.username or parsed.password:
        raise Blocked('PORTAL_WORDPRESS_SITE_INVALID:'+str(portal_id))
    origin='https://'+parsed.netloc.lower()
    for p in profiles:
        if not isinstance(p,dict) or p is matches[0]:
            continue
        other=p.get('wordpress_base_url')
        if isinstance(other,str) and other.rstrip('/').casefold()==origin.casefold():
            raise Blocked('PORTAL_WORDPRESS_SITE_SHARED:'+str(portal_id))
    return origin


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
    profiles=[dict(p) for p in registry.get('profiles') or []]
    static_profiles=[p for p in profiles if not p.get('category_git_source')]
    central_loaded=False
    out=[]
    for row in rows:
        category=row['category']
        direct=any(category in (p.get('category_exact') or []) or
                   (p.get('category_prefixes') and category.startswith(tuple(p['category_prefixes'])))
                   for p in static_profiles)
        if direct:
            p=match_profile(category,static_profiles)
        else:
            if not central_loaded:
                for p in profiles:
                    if p.get('category_git_source'):
                        p['category_exact']=sorted(_central_category_slugs(p['category_git_source']))
                        p['category_prefixes']=[]
                central_loaded=True
            p=match_profile(category,profiles)
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
