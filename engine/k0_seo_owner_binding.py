"""K0's technical receipt of the EXISTING approved PSERC SEO decision.

This does not decide search intent, modify the exact-five PSERC handoff, or run
any fresh SEO logic. Accepted source: unmodified PSERC compiler manifest.
"""
from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path

from .core import stable
from .k0_portal_resolver import validate_intake

MANIFEST_MODE = 'READ_ONLY_METADATA_ONLY_EXACT_FIVE_FIELDS'
OWNER_PROFILE = 'PSTE_INTENT_PROFILE_V2_SEO_FIRST_EVIDENCE_BOUND_MULTI_BRANCH'

class Blocked(RuntimeError):
    pass

def _hex64(value):
    return isinstance(value, str) and bool(re.fullmatch(r'[a-f0-9]{64}',value))

def _strict_item(item):
    return isinstance(item, dict) and set(item)=={'title','target_keyword','category','article_type','plan_slot'}

def inspect(manifest):
    """Return (unchanged five-field batch, upstream-decision index)."""
    if not isinstance(manifest,dict) or manifest.get('mode')!=MANIFEST_MODE:
        raise Blocked('K0_OWNER_MANIFEST_OR_MODE_INVALID')
    claimed=manifest.get('manifest_sha256')
    content={k:v for k,v in manifest.items() if k!='manifest_sha256'}
    if not _hex64(claimed) or stable(content)!=claimed:
        raise Blocked('K0_OWNER_MANIFEST_HASH_MISMATCH')
    batch=manifest.get('next_textmachine_metadata_batch')
    try:
        items=validate_intake(batch)
    except Exception as exc:
        raise Blocked('K0_OWNER_FIVE_FIELD_BATCH_INVALID:'+str(exc)) from exc
    boundary=manifest.get('metadata_boundary')
    if not isinstance(boundary,dict) or boundary.get('ok') is not True:
        raise Blocked('K0_OWNER_METADATA_BOUNDARY_NOT_PASS')
    details=manifest.get('items')
    if not isinstance(details,list) or len(details)!=len(items):
        raise Blocked('K0_OWNER_MANIFEST_ITEM_COUNT_MISMATCH')
    expected={x['plan_slot']:x for x in items}
    if len(expected)!=len(items):
        raise Blocked('K0_OWNER_DUPLICATE_PLAN_SLOT')
    records={}
    for row in details:
        if not isinstance(row,dict) or row.get('status')!='READY_FOR_METADATA_HANDOFF':
            raise Blocked('K0_OWNER_ITEM_NOT_READY')
        binding=row.get('metadata_binding')
        if not _strict_item(binding):
            raise Blocked('K0_OWNER_DETAIL_FIVE_FIELDS_INVALID')
        slot=binding['plan_slot']
        if slot not in expected or binding!=expected[slot] or slot in records:
            raise Blocked('K0_OWNER_DETAIL_IDENTITY_MISMATCH')
        profile=row.get('intent_profile')
        if not isinstance(profile,dict) or profile.get('contract')!=OWNER_PROFILE or profile.get('status')!='PASS' or profile.get('ok') is not True:
            raise Blocked('K0_OWNER_UPSTREAM_INTENT_NOT_APPROVED')
        intent=profile.get('search_intent')
        if not isinstance(intent,str) or not intent.strip() or profile.get('article_type')!=binding['article_type']:
            raise Blocked('K0_OWNER_UPSTREAM_INTENT_IDENTITY_INVALID')
        if not _hex64(profile.get('profile_sha256')):
            raise Blocked('K0_OWNER_PROFILE_HASH_MISSING')
        records[slot]={'search_intent':intent,'profile_sha256':profile['profile_sha256']}
    if set(records)!=set(expected):
        raise Blocked('K0_OWNER_MISSING_DECISION')
    return batch,records

def bind_context(manifest, single_intake, context):
    """No new judgement: transfer exactly the single approved PSERC value."""
    batch, records=inspect(manifest)
    try:
        one=validate_intake(single_intake)
    except Exception as exc:
        raise Blocked('K0_OWNER_SINGLE_ITEM_INTAKE_INVALID:'+str(exc)) from exc
    if len(one)!=1:
        raise Blocked('K0_OWNER_INTAKE_NOT_SINGLE_ITEM')
    ident=one[0]
    original={x['plan_slot']:x for x in batch['items']}
    if ident.get('plan_slot') not in original or ident!=original[ident['plan_slot']]:
        raise Blocked('K0_OWNER_SINGLE_ITEM_NOT_IN_SOURCE_BATCH')
    if not isinstance(context,dict) or context.get('identity')!=ident:
        raise Blocked('K0_OWNER_AUTHORING_CONTEXT_IDENTITY_MISMATCH')
    cp=context.get('content_profile')
    if not isinstance(cp,dict):
        raise Blocked('K0_OWNER_CONTENT_PROFILE_MISSING')
    source=records[ident['plan_slot']]
    existing=cp.get('search_intent')
    if existing not in (None,'',source['search_intent']):
        raise Blocked('K0_OWNER_INTENT_CONFLICT_WITH_EDITORIAL_APPROVAL')
    # Rebinding is deterministic and adds provenance only inside the existing
    # K0 authoring context (never to PSERC's five-field metadata handoff).
    result=copy.deepcopy(context)
    result['content_profile']=dict(cp)
    result['content_profile']['search_intent']=source['search_intent']
    for key,value in (
        ('seo_owner_manifest_sha256',manifest['manifest_sha256']),
        ('seo_owner_profile_sha256',source['profile_sha256']),
        ('seo_owner_original_batch_sha256',batch['batch_sha256']),
    ):
        prior=result['content_profile'].get(key)
        if prior not in (None,'',value):
            raise Blocked('K0_OWNER_SOURCE_PROVENANCE_CONFLICT:'+key)
        result['content_profile'][key]=value
    return result

def verify_context(manifest,single_intake,context):
    expected=bind_context(manifest,single_intake,context)
    if expected!=context:
        raise Blocked('K0_OWNER_AUTHORING_INTENT_NOT_BOUND')
    return {'contract':'K0_UPSTREAM_SEO_OWNER_BINDING_V1','status':'PASS','plan_slot':single_intake['items'][0]['plan_slot'],'source_manifest_sha256':manifest['manifest_sha256'],'search_intent':expected['content_profile']['search_intent'],'publish_allowed':False}

def _read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def main():
    mode=sys.argv[1]
    if mode=='extract' and len(sys.argv)==4:
        batch,_=inspect(_read(sys.argv[2]))
        Path(sys.argv[3]).write_text(json.dumps(batch,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({'status':'PASS','count':batch['item_count'],'batch_sha256':batch['batch_sha256']}))
    elif mode=='bind' and len(sys.argv)==6:
        ctx=bind_context(_read(sys.argv[2]),_read(sys.argv[3]),_read(sys.argv[4]))
        Path(sys.argv[5]).write_text(json.dumps(ctx,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({'status':'PASS','search_intent':ctx['content_profile']['search_intent']}))
    elif mode=='verify' and len(sys.argv)==5:
        out=verify_context(_read(sys.argv[2]),_read(sys.argv[3]),_read(sys.argv[4]))
        print(json.dumps(out,ensure_ascii=False))
    else:
        raise Blocked('K0_OWNER_BINDING_USAGE_INVALID')

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps({'status':'BLOCKED','reason':str(exc),'publish_allowed':False}))
        raise SystemExit(2)