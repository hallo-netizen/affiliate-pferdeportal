import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import wordpress_redaktionsplan_upload as w
from wordpress_output_contract import validate_wordpress_package
import hashlib

def article(i=0,article_type="Beratung"):
    body=f'<article class="ppm-generated"><h2>Test {i}</h2><p>Inhalt {i}</p></article>'
    sha=hashlib.sha256(body.encode()).hexdigest()
    slot=hashlib.sha256(f"slot-{i}".encode()).hexdigest()
    slug=f"test-{i}";category=f"test-{i}";title=f"Testtitel {i}";keyword=f"Testkeyword {i}"
    return {
      "index":i,"title":title,"target_keyword":keyword,"category":category,"article_type":article_type,
      "plan_slot":slot,"final_draft_sha256":sha,"revision_count":1,"body":body,
      "production_context":{"fact_pack":{"contract":"canonical_fact_pack_v1"},"production_plan_item":{
        "article_type":article_type,"target_keyword":keyword,
        "runtime_order":{"title":title,"article_type":article_type,"slug":slug},
        "category_binding":{"slug":category},
        "quality_binding":{"wordpress_category":{"slug":category,"taxonomy":"category"}}}},
      "languagetool":{"status":"PASS","engine":"LanguageTool 6.8 / Bestand 43","finding_count":0},
      "ppm679":{"status":"PASS","ppm_version":"6.7.9","technical_status":"TECHNICAL_CHECK_OK","content_quality_status":"CONTENT_QUALITY_CHECK_OK","fail_closed_aggregate_status":"PASS","content_sha256":sha}
    }

class T(unittest.TestCase):
    def setUp(self):self.pkg=w.build("b"*64,[article(0)])
    def test_current_contract_passes(self):self.assertEqual([],validate_wordpress_package(self.pkg))
    def test_old_pseudo_direct_contract_rejected(self):
        bad=copy.deepcopy(self.pkg);bad["contract"]="PSERC_APPROVED_PRODUCTION_PACKAGE_V1";self.assertIn("CONTRACT",validate_wordpress_package(bad))
    def test_internal_handoff_rejected(self):
        bad=copy.deepcopy(self.pkg);bad["contract"]="SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2";self.assertIn("CONTRACT",validate_wordpress_package(bad))
    def test_article_mutation_breaks_hash(self):
        bad=copy.deepcopy(self.pkg);bad["articles"][0]["body"]+="X";self.assertIn("BODY_HASH:0",validate_wordpress_package(bad))
if __name__=="__main__":unittest.main()
