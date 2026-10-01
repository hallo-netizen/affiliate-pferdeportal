from .receipt import make_receipt
from .core import hard_rules

BASE_MAPPING=[
  ('pserc.final_integrity','pserc_adapter','PSERC'),
  ('endstempel.signature','endstempel_adapter','ENDSTEMPEL'),
  ('wordpress.final_verify','wordpress_verify_adapter','WORDPRESS_VERIFY'),
]

PARITY_PACKAGE_MAPPING=[
  ('wordpress.rendered_h1_integrity','wordpress_verify_adapter','WORDPRESS_RENDERED_H1'),
  ('wordpress.rendered_duplicate_heading_integrity','wordpress_verify_adapter','WORDPRESS_RENDERED_DUPLICATE_HEADINGS'),
  ('wordpress.rendered_adjacent_heading_integrity','wordpress_verify_adapter','WORDPRESS_RENDERED_ADJACENT_HEADINGS'),
  ('integrity.rendered_evidence_class','wordpress_verify_adapter','WORDPRESS_RENDERED_EVIDENCE_CLASS'),
  ('integrity.content_validator_contract_supported','integrity_guard','CONTENT_VALIDATOR_CONTRACT_SUPPORTED'),
  ('integrity.article_type_definition_bound','integrity_guard','ARTICLE_TYPE_DEFINITION_BOUND'),
  ('integrity.article_content_hash_bound','integrity_guard','ARTICLE_CONTENT_HASH_BOUND'),
  ('integrity.section_requirements_present','integrity_guard','SECTION_REQUIREMENTS_PRESENT'),
  ('integrity.section_requirements_hash','integrity_guard','SECTION_REQUIREMENTS_HASH'),
  ('integrity.canonical_validation_binding','integrity_guard','CANONICAL_VALIDATION_BINDING'),
  ('integrity.wave2_contract','integrity_guard','WAVE2_CONTRACT'),
  ('integrity.quality_binding_present','integrity_guard','QUALITY_BINDING_PRESENT'),
  ('integrity.quality_binding_hash','integrity_guard','QUALITY_BINDING_HASH'),
  ('integrity.internal_marker_bound','integrity_guard','INTERNAL_MARKER_BOUND'),
  ('integrity.link_registry_hash','integrity_guard','LINK_REGISTRY_HASH'),
  ('integrity.language_delta_evidence','integrity_guard','LANGUAGE_DELTA_EVIDENCE'),
  ('integrity.language_evidence','lt68_adapter','LANGUAGE_EVIDENCE'),
  ('integrity.known_error_contract','integrity_guard','KNOWN_ERROR_CONTRACT'),
]

PACKAGE_RESULT_MAP=BASE_MAPPING+PARITY_PACKAGE_MAPPING

def _make_selected(package_id,package_sha256,external_results,allowed_rule_ids):
    rows=[]
    for rid,owner,key in PACKAGE_RESULT_MAP:
        if rid not in allowed_rule_ids:
            continue
        value=external_results.get(key)
        status='PASS' if value=='PASS' else 'FAIL'
        rows.append(make_receipt(rid,owner,'PACKAGE_INTEGRITY',package_id,package_sha256,status,{'external_result':value,'external_key':key}))
    return rows

def make_package_receipts(package_id,package_sha256,external_results):
    allowed={r['id'] for r in hard_rules('PACKAGE_INTEGRITY')}
    return _make_selected(package_id,package_sha256,external_results,allowed)

def make_pre_wordpress_package_receipts(package_id,package_sha256,external_results):
    allowed={r['id'] for r in hard_rules('PACKAGE_INTEGRITY') if r.get('check_stage')!='WORDPRESS_VERIFY'}
    return _make_selected(package_id,package_sha256,external_results,allowed)
