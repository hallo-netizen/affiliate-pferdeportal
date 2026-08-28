#!/usr/bin/env python3
"""STARTMASTER0103 fail-closed production package preflight.
Prevents known handoff/package reconstruction failures before live PPM execution.
No content, quality, design, SEO, PSTE, PSERC, PPM or publish rule is changed.
"""
import json, sys, hashlib
from pathlib import Path

FORBIDDEN_PPM_ITEM_FIELDS = {'plan_slot'}
REQUIRED_RELEASE_ITEM_FIELDS = {'plan_slot','canonical_article_id'}

def norm(s): return ' '.join(str(s or '').strip().split())
def stable_hash(obj): return hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def validate(env):
    errors=[]; plan=env.get('production_plan') or {}; release=env.get('workflow_release') or {}; fp_bundle=env.get('fact_pack_bundle') or {}
    fps={str(x.get('fact_pack_id')):x for x in fp_bundle.get('fact_packs',[]) if isinstance(x,dict) and x.get('fact_pack_id')}
    for i,item in enumerate(plan.get('items',[])):
        bad=sorted(FORBIDDEN_PPM_ITEM_FIELDS.intersection(item))
        if bad: errors.append({'code':'FOREIGN_METADATA_FIELD_IN_0039_PPM_PLAN','index':i,'fields':bad})
    for i,item in enumerate(release.get('items',[])):
        missing=sorted(REQUIRED_RELEASE_ITEM_FIELDS.difference(item))
        if missing: errors.append({'code':'SUPERVISOR_RELEASE_BINDING_FIELD_MISSING','index':i,'fields':missing})
    for i,item in enumerate(plan.get('items',[])):
        sid=str(item.get('source_snapshot_id') or ''); fp=fps.get(sid)
        if not fp:
            errors.append({'code':'FACT_PACK_FOR_PLAN_ITEM_NOT_FOUND','index':i,'source_snapshot_id':sid}); continue
        title_scope=norm(fp.get('title_scope')); subject_scope=norm((item.get('runtime_order') or {}).get('subject_scope'))
        if not title_scope or title_scope != subject_scope:
            errors.append({'code':'CANONICAL_FACT_PACK_SCOPE_MISMATCH_PREVENTED','index':i,'fact_pack_id':sid,'title_scope':title_scope,'subject_scope':subject_scope})
    for i,item in enumerate(plan.get('items',[])):
        cat=((item.get('quality_binding') or {}).get('wordpress_category') or {})
        name=norm(cat.get('name')); slug=norm(cat.get('slug')); taxonomy=norm(cat.get('taxonomy')); path=norm(cat.get('hierarchy_path')); leaf=norm(path.split('>')[-1]) if path else ''
        if not name or not slug or taxonomy != 'category' or not path:
            errors.append({'code':'WORDPRESS_CATEGORY_BINDING_INCOMPLETE','index':i,'name':name,'slug':slug,'taxonomy':taxonomy,'hierarchy_path':path})
        if leaf and name != leaf:
            errors.append({'code':'WORDPRESS_CATEGORY_NAME_NOT_HIERARCHY_LEAF','index':i,'name':name,'expected_name':leaf,'slug':slug})
        if name == slug and leaf and leaf != slug:
            errors.append({'code':'WORDPRESS_CATEGORY_NAME_WAS_SYNTHESIZED_FROM_SLUG','index':i,'name':name,'slug':slug,'expected_name':leaf})
        if not norm(cat.get('category_source_snapshot_hash')): errors.append({'code':'WORDPRESS_CATEGORY_SOURCE_HASH_MISSING','index':i})
    for field,objkey in [('fact_pack_bundle_sha256','fact_pack_bundle'),('production_plan_sha256','production_plan'),('workflow_release_sha256','workflow_release')]:
        expected=env.get(field)
        if expected and expected != stable_hash(env.get(objkey)):
            errors.append({'code':'PACKAGE_COMPONENT_HASH_MISMATCH','field':field,'expected':expected,'actual':stable_hash(env.get(objkey))})
    if env.get('package_payload_sha256'):
        payload={k:v for k,v in env.items() if k!='package_payload_sha256'}; actual=stable_hash(payload)
        if env['package_payload_sha256'] != actual: errors.append({'code':'PACKAGE_PAYLOAD_HASH_MISMATCH','expected':env['package_payload_sha256'],'actual':actual})
    return {'ok':not errors,'status':'PASS' if not errors else 'BLOCKED','guard':'STARTMASTER0103_PRODUCTION_PACKAGE_PREFLIGHT_V1','errors':errors}

def main(path):
    result=validate(json.loads(Path(path).read_text(encoding='utf-8'))); print(json.dumps(result,ensure_ascii=False,indent=2)); return 0 if result['ok'] else 2
if __name__=='__main__':
    if len(sys.argv)!=2: print('usage: guard.py production-package.json',file=sys.stderr); sys.exit(64)
    sys.exit(main(sys.argv[1]))
