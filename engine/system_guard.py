import json
from pathlib import Path
from .core import ROOT, stable, load_catalog, load_values
from .receipt import make_receipt
from .field_coverage import audit as field_audit
from .owner_guard import verify as owner_verify
from .isolation_guard import verify as isolation_verify
from .ppm_parity_guard import verify as ppm_parity_verify

SYSTEM_ID='K10_SYSTEM_SNAPSHOT'

def system_snapshot():
    names=['RULE_CATALOG.json','RULE_VALUES.json','FIELD_POLICY.json','K9_BASELINE_REFERENCE.json','K10_GOAL_CONTRACT.json','PPM_PARITY_MAP.json','evidence/PPM679_EXACT_104_RULE_INVENTORY.json']
    payload={name:json.loads((ROOT/name).read_text(encoding='utf-8')) for name in names}
    return payload,stable(payload)

def _receipt(rule_id,owner,sha,status,evidence=None):
    return make_receipt(rule_id,owner,'SYSTEM',SYSTEM_ID,sha,status,evidence)

def run_system_checks():
    payload,sha=system_snapshot(); ref=payload['K9_BASELINE_REFERENCE.json']; values=payload['RULE_VALUES.json']; goal=payload['K10_GOAL_CONTRACT.json']; catalog=payload['RULE_CATALOG.json']
    prov=values['provenance']
    baseline_ok=(
        prov.get('baseline_commit')==ref.get('source_commit') and
        prov.get('writing_rules_blob_sha')==ref.get('source_writing_rules_blob_sha') and
        prov.get('table_rule_blob_sha')==ref.get('source_table_rule_blob_sha') and
        prov.get('ppm_sha256')=='acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1' and
        prov.get('lt68_sha256')=='2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8'
    )
    cov=field_audit(); own=owner_verify(); iso=isolation_verify(); ppm_parity=ppm_parity_verify()
    table_ok=(values.get('table',{}).get('presence_policy')=={'FAQ':'OPTIONAL','Beratung':'OPTIONAL','Vergleich':'REQUIRED','Pflege':'OPTIONAL'} and float(values['table'].get('minimum_unique_content_token_ratio',0))==0.18)
    topic_ok=not any(str(r.get('id','')).startswith('topic.') or r.get('topic_override') for r in catalog.get('rules',[]))
    publish_ok=(catalog.get('publish_allowed') is False and goal.get('publish_allowed') is False and ref.get('publish_allowed') is False and values['global'].get('publish_allowed') is False)
    rows=[
      ('baseline.external_gate_hash_binding','baseline_guard',baseline_ok,{}),
      ('meta.catalog_coverage_fail_closed','catalog_guard',cov['status']=='PASS',{'total_fields':cov['total'],'bad':cov['bad']}),
      ('meta.catalog_owner_binding','catalog_guard',own['status']=='PASS',{'findings':own['findings']}),
      ('meta.ppm104_parity','catalog_guard',ppm_parity['status']=='PASS',ppm_parity),
      ('isolation.no_legacy_runtime_dependency','isolation_guard',iso['status']=='PASS',{'findings':iso['findings']}),
      ('table.rule_active','catalog_guard',table_ok,{}),
      ('structure.topic_specific_special_logic_forbidden','structural_checker',topic_ok,{}),
      ('publish.allowed','safety_checker',publish_ok,{}),
    ]
    return SYSTEM_ID,sha,[_receipt(rid,owner,sha,'PASS' if ok else 'FAIL',ev) for rid,owner,ok,ev in rows]
