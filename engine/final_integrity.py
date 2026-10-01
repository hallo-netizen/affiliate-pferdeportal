from collections import Counter
from .core import hard_rules, catalog_hash, values_hash
from .receipt import verify_receipt

def _verify_required(scope, subject_id, subject_sha256, receipts, required_rows):
    findings=[]
    required={r['id']:r for r in required_rows}
    all_scope={r['id']:r for r in hard_rules(scope)}
    seen=[]
    for rec in receipts:
        if rec.get('scope')!=scope:
            continue
        rid=rec.get('rule_id')
        if rid not in all_scope:
            findings.append('UNKNOWN_HARD_RULE_RECEIPT:'+str(rid)); continue
        if rid not in required:
            # A receipt from a later stage is irrelevant for this stage-specific check.
            continue
        seen.append(rid)
        if not verify_receipt(rec):
            findings.append('RECEIPT_HASH_INVALID:'+str(rid)); continue
        if rec.get('owner')!=required[rid]['owner']:
            findings.append('RECEIPT_OWNER_MISMATCH:'+rid)
        if rec.get('subject_id')!=subject_id:
            findings.append('RECEIPT_SUBJECT_ID_MISMATCH:'+rid)
        if rec.get('subject_sha256')!=subject_sha256:
            findings.append('RECEIPT_SUBJECT_HASH_MISMATCH:'+rid)
        if rec.get('catalog_sha256')!=catalog_hash():
            findings.append('RECEIPT_CATALOG_HASH_MISMATCH:'+rid)
        if rec.get('rule_values_sha256')!=values_hash():
            findings.append('RECEIPT_RULE_VALUES_HASH_MISMATCH:'+rid)
        if rec.get('status')!='PASS':
            findings.append('HARD_RULE_NOT_PASS:'+rid)
    counts=Counter(seen)
    for rid in required:
        if counts[rid]==0:
            findings.append('MISSING_HARD_RULE_RECEIPT:'+rid)
        elif counts[rid]>1:
            findings.append('DUPLICATE_HARD_RULE_RECEIPT:'+rid)
    return {'status':'PASS' if not findings else 'BLOCKED','findings':findings,'publish_allowed':False}

def verify_scope(scope, subject_id, subject_sha256, receipts):
    return _verify_required(scope,subject_id,subject_sha256,receipts,hard_rules(scope))

def verify_article(article_id, article_sha256, receipts):
    return verify_scope('ARTICLE',article_id,article_sha256,receipts)

def verify_system(system_id, system_sha256, receipts):
    return verify_scope('SYSTEM',system_id,system_sha256,receipts)

def verify_package(package_id, package_sha256, receipts):
    return verify_scope('PACKAGE_INTEGRITY',package_id,package_sha256,receipts)

def verify_package_pre_wordpress(package_id, package_sha256, receipts):
    all_rows=hard_rules('PACKAGE_INTEGRITY')
    required=[r for r in all_rows if r.get('check_stage')!='WORDPRESS_VERIFY']
    pending=[r['id'] for r in all_rows if r.get('check_stage')=='WORDPRESS_VERIFY']
    out=_verify_required('PACKAGE_INTEGRITY',package_id,package_sha256,receipts,required)
    out['required_receipt_count']=len(required)
    out['pending_wordpress_rule_ids']=pending
    if out['status']=='PASS':
        out['status']='READY_FOR_WORDPRESS_DRAFT_IMPORT'
    return out
