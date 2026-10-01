from .core import stable, catalog_hash, values_hash

def make_receipt(rule_id, owner, scope, subject_id, subject_sha256, status, evidence=None):
    if status not in ('PASS','FAIL'):
        raise ValueError('K10_RECEIPT_STATUS_INVALID')
    core={
        'contract':'K10_RULE_RECEIPT_V2',
        'rule_id':rule_id,
        'owner':owner,
        'scope':scope,
        'subject_id':subject_id,
        'subject_sha256':subject_sha256,
        'catalog_sha256':catalog_hash(),
        'rule_values_sha256':values_hash(),
        'status':status,
        'evidence':evidence or {}
    }
    out=dict(core)
    out['receipt_sha256']=stable(core)
    return out

def verify_receipt(receipt):
    if receipt.get('contract')!='K10_RULE_RECEIPT_V2':
        return False
    core=dict(receipt)
    claimed=core.pop('receipt_sha256',None)
    return bool(claimed and claimed==stable(core))
