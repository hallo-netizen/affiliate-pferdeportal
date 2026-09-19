import copy,hashlib,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import wordpress_redaktionsplan_upload as w

def plan():
    slot="a"*64
    body="<article><p>Test</p></article>"
    return {"contract":"production_plan_v4","plan_contract_version":"4.0.0","required_plugin_version":"6.7.9","plan_id":"test","validation_contract_version":"GEN1_107008_RELEASED_ARTICLE_BINDING_V1","items":[{"plan_slot":slot,"canonical_article_id":"article:test","plan_item_key":"test-"+slot[:12],"article_type":"Beratung","topic":"Testtitel","target_keyword":"Testkeyword","runtime_order":{"article_type":"Beratung","title":"Testtitel","slug":"testtitel","subject_scope":"Testkeyword","subject_label":"Testkeyword"},"category_binding":{"name":"test","slug":"test","hierarchy_path":"test","portal_path":"test","taxonomy":"category","article_type":"Beratung"},"canonical_article":{"article_type":"Beratung","canonical_article_id":"article:test","plan_slot":slot,"title":"Testtitel","slug":"testtitel","target_keyword":"Testkeyword","body_html":body,"body_html_sha256":hashlib.sha256(body.encode()).hexdigest(),"body_text":"Test"}}]}

class T(unittest.TestCase):
    def setUp(self):self.x=w.build("TEST","b"*64,plan())
    def test_positive(self):self.assertEqual([],w.validate(self.x))
    def test_wrong_contract_blocks(self):
        x=copy.deepcopy(self.x);x["contract"]="SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2";self.assertIn("CONTRACT",w.validate(x))
    def test_wrong_count_blocks(self):
        x=copy.deepcopy(self.x);x["article_count"]=2;self.assertIn("PLAN_COUNT",w.validate(x))
    def test_wrong_plan_hash_blocks(self):
        x=copy.deepcopy(self.x);x["production_plan_sha256"]="0"*64;self.assertIn("PLAN_HASH",w.validate(x))
    def test_wrong_binding_status_blocks(self):
        x=copy.deepcopy(self.x);x["redaktionsplan_binding"]["status"]="PASS";self.assertIn("BINDING_STATUS",w.validate(x))
    def test_body_tamper_blocks(self):
        x=copy.deepcopy(self.x);x["production_plan"]["items"][0]["canonical_article"]["body_html"]+="x";self.assertIn("BODY_HASH:0",w.validate(x))
    def test_wrong_package_hash_blocks(self):
        x=copy.deepcopy(self.x);x["package_payload_sha256"]="0"*64;self.assertIn("PACKAGE_HASH",w.validate(x))
if __name__=="__main__":unittest.main()
