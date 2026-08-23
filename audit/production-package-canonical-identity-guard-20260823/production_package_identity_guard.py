#!/usr/bin/env python3
import argparse, hashlib, json, sys
from pathlib import Path

DOMAIN='pserc-plan-slot-v2|'
CONTRACT='PRODUCTION_PACKAGE_CANONICAL_IDENTITY_GUARD_V1'

def slot_from_canonical_id(cid:str)->str:
    cid=cid.strip()
    if not cid:
        raise ValueError('CANONICAL_ARTICLE_ID_MISSING')
    return hashlib.sha256((DOMAIN+cid).encode('utf-8')).hexdigest()

def load_json(p:Path):
    with p.open('r',encoding='utf-8') as f:
        return json.load(f)

def resolve(canonical_plan:dict, plan_slot:str, category:str, article_type:str)->dict:
    matches=[]
    for row in canonical_plan.get('slots',canonical_plan.get('items',[])):
        if not isinstance(row,dict):
            continue
        cid=str(row.get('canonical_article_id','')).strip()
        if not cid:
            continue
        if slot_from_canonical_id(cid)==plan_slot:
            matches.append(row)
    if len(matches)!=1:
        raise RuntimeError(f'IDENTITY_GUARD_SLOT_RESOLUTION_COUNT_{len(matches)}')
    row=matches[0]
    if str(row.get('category_slug',''))!=category:
        raise RuntimeError('IDENTITY_GUARD_CATEGORY_MISMATCH')
    if str(row.get('article_type',''))!=article_type:
        raise RuntimeError('IDENTITY_GUARD_ARTICLE_TYPE_MISMATCH')
    cid=str(row['canonical_article_id'])
    if slot_from_canonical_id(cid)!=plan_slot:
        raise RuntimeError('IDENTITY_GUARD_REVERSE_SLOT_MISMATCH')
    return row

def validate(production_plan:dict, canonical_plan:dict, plan_slot:str, category:str, article_type:str)->dict:
    items=production_plan.get('items') if isinstance(production_plan,dict) else None
    if not isinstance(items,list) or len(items)!=1 or not isinstance(items[0],dict):
        raise RuntimeError('IDENTITY_GUARD_PRODUCTION_PLAN_SINGLE_ITEM_REQUIRED')
    pitem=items[0]
    row=resolve(canonical_plan,plan_slot,category,article_type)
    expected=str(row['canonical_article_id'])
    actual=str(pitem.get('canonical_article_id','')).strip()
    if actual!=expected:
        raise RuntimeError(f'IDENTITY_GUARD_CANONICAL_ID_MISMATCH::{actual}::{expected}')
    derived=slot_from_canonical_id(actual)
    if derived!=plan_slot:
        raise RuntimeError('IDENTITY_GUARD_PRODUCTION_PLAN_REVERSE_SLOT_MISMATCH')
    if str(pitem.get('article_type',''))!=article_type:
        raise RuntimeError('IDENTITY_GUARD_PRODUCTION_PLAN_TYPE_MISMATCH')
    return {
        'contract':CONTRACT,'status':'PASS','ok':True,
        'plan_slot':plan_slot,'canonical_article_id':actual,
        'derived_plan_slot':derived,'category_slug':category,'article_type':article_type,
        'canonical_plan_match_count':1,
        'policy':{
            'canonical_article_id_generation_allowed':False,
            'canonical_article_id_source':'CANONICAL_COMPLETE_EDITORIAL_PLAN_V1_BY_PLAN_SLOT',
            'reverse_slot_verification_required':True,
            'zero_or_multiple_matches_block':True,
        }
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--canonical-plan',required=True,type=Path)
    ap.add_argument('--production-plan',required=True,type=Path)
    ap.add_argument('--plan-slot',required=True)
    ap.add_argument('--category',required=True)
    ap.add_argument('--article-type',required=True)
    ap.add_argument('--out',type=Path)
    args=ap.parse_args()
    try:
        result=validate(load_json(args.production_plan),load_json(args.canonical_plan),args.plan_slot,args.category,args.article_type)
        rc=0
    except Exception as e:
        result={'contract':CONTRACT,'status':'IDENTITY_GUARD_BLOCKED','ok':False,'reason':str(e),'plan_slot':args.plan_slot,'category_slug':args.category,'article_type':args.article_type}
        rc=2
    text=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.out:
        args.out.write_text(text,encoding='utf-8')
    sys.stdout.write(text)
    raise SystemExit(rc)
if __name__=='__main__': main()
