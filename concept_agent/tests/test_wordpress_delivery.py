import hashlib,sys,unittest
from pathlib import Path
OFFICE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OFFICE))
import wordpress_redaktionsplan_upload as w
from wordpress_delivery import wordpress_delivery_bytes,wordpress_delivery_filename

def good():
    s="a"*64;b="<article><p>Test</p></article>"
    p={"contract":"production_plan_v4","plan_contract_version":"4.0.0","required_plugin_version":"6.7.9","plan_id":"test","validation_contract_version":"GEN1_107008_RELEASED_ARTICLE_BINDING_V1","items":[{"plan_slot":s,"canonical_article_id":"article:test","plan_item_key":"test-"+s[:12],"article_type":"Beratung","topic":"Testtitel","target_keyword":"Testkeyword","runtime_order":{"article_type":"Beratung","title":"Testtitel","slug":"testtitel","subject_scope":"Testkeyword","subject_label":"Testkeyword"},"category_binding":{"name":"test","slug":"test","hierarchy_path":"test","portal_path":"test","taxonomy":"category","article_type":"Beratung"},"canonical_article":{"article_type":"Beratung","canonical_article_id":"article:test","plan_slot":s,"title":"Testtitel","slug":"testtitel","target_keyword":"Testkeyword","body_html":b,"body_html_sha256":hashlib.sha256(b.encode()).hexdigest(),"body_text":"Test"}}]}
    return w.build("TEST","b"*64,p)

class T(unittest.TestCase):
    def test_direct_payload_leaves(self):
        x=good();self.assertTrue(wordpress_delivery_bytes(x));self.assertEqual("GEN1_7_ARTIKEL_WORDPRESS_REDAKTIONSPLAN_UPLOAD_107008_PASS.json",wordpress_delivery_filename(x))
    def test_internal_handoff_blocks(self):
        with self.assertRaisesRegex(RuntimeError,"WORDPRESS_PACKAGE_BLOCKED"):wordpress_delivery_bytes({"contract":"CONCEPT_AGENT_7_ARTICLE_CHAT_HANDOFF_V1"})
    def test_endstempel_wrapper_blocks(self):
        with self.assertRaisesRegex(RuntimeError,"WORDPRESS_PACKAGE_BLOCKED"):wordpress_delivery_bytes({"contract":"PSERC_APPROVED_PRODUCTION_PACKAGE_V1","endstamp_contract":"PFERDE_ATELIER_ENDSTEMPEL_RELEASE_V1"})
if __name__=="__main__":unittest.main()
