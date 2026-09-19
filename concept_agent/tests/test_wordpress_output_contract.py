import copy,hashlib,sys,unittest
from pathlib import Path
OFFICE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OFFICE))
import wordpress_redaktionsplan_upload as w
from wordpress_output_contract import validate_wordpress_package

def fixture():
    slot="a"*64;body="<article><p>Test</p></article>"
    plan={"contract":"production_plan_v4","plan_contract_version":"4.0.0","required_plugin_version":"6.7.9","plan_id":"test","validation_contract_version":"GEN1_107008_RELEASED_ARTICLE_BINDING_V1","items":[{"plan_slot":slot,"canonical_article_id":"article:test","plan_item_key":"test-"+slot[:12],"article_type":"Beratung","topic":"Testtitel","target_keyword":"Testkeyword","runtime_order":{"article_type":"Beratung","title":"Testtitel","slug":"testtitel","subject_scope":"Testkeyword","subject_label":"Testkeyword"},"category_binding":{"name":"test","slug":"test","hierarchy_path":"test","portal_path":"test","taxonomy":"category","article_type":"Beratung"},"canonical_article":{"article_type":"Beratung","canonical_article_id":"article:test","plan_slot":slot,"title":"Testtitel","slug":"testtitel","target_keyword":"Testkeyword","body_html":body,"body_html_sha256":hashlib.sha256(body.encode()).hexdigest(),"body_text":"Test"}}]}
    return w.build("TEST","b"*64,plan)

class WordPressOutputContractTest(unittest.TestCase):
    def setUp(self):self.pkg=fixture()
    def test_direct_redaktionsplan_fixture_passes(self):self.assertEqual([],validate_wordpress_package(self.pkg))
    def test_system4_handoff_rejected(self):
        bad=copy.deepcopy(self.pkg);bad["contract"]="SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2"
        self.assertIn("CONTRACT",validate_wordpress_package(bad))
    def test_endstempel_wrapper_rejected(self):
        bad={"contract":"PSERC_APPROVED_PRODUCTION_PACKAGE_V1","endstamp_contract":"PFERDE_ATELIER_ENDSTEMPEL_RELEASE_V1"}
        self.assertIn("TOP_SCHEMA",validate_wordpress_package(bad))
    def test_article_mutation_breaks_hash(self):
        bad=copy.deepcopy(self.pkg);bad["production_plan"]["items"][0]["canonical_article"]["body_html"]+="X"
        self.assertIn("BODY_HASH:0",validate_wordpress_package(bad))
    def test_publish_allowed_must_stay_false(self):
        bad=copy.deepcopy(self.pkg);bad["publish_allowed"]=True
        self.assertIn("PUBLISH",validate_wordpress_package(bad))
if __name__=="__main__":unittest.main()
