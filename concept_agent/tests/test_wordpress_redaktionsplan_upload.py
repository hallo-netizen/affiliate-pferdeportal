import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import wordpress_redaktionsplan_upload as w
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
    def setUp(self):self.x=w.build("b"*64,[article(0)])
    def test_positive(self):self.assertEqual([],w.validate(self.x))
    def test_mixed_types_positive(self):self.assertEqual([],w.validate(w.build("c"*64,[article(0,"Beratung"),article(1,"Produktvergleich")])))
    def test_wrong_contract_blocks(self):
        x=copy.deepcopy(self.x);x["contract"]="PSERC_APPROVED_PRODUCTION_PACKAGE_V1";self.assertIn("CONTRACT",w.validate(x))
    def test_publish_blocks(self):
        x=copy.deepcopy(self.x);x["publish_allowed"]=True;self.assertIn("PUBLISH",w.validate(x))
    def test_body_tamper_blocks(self):
        x=copy.deepcopy(self.x);x["articles"][0]["body"]+="x";self.assertIn("BODY_HASH:0",w.validate(x))
    def test_bad_lt_blocks(self):
        x=copy.deepcopy(self.x);x["articles"][0]["languagetool"]["finding_count"]=1;self.assertIn("LT:0",w.validate(x))
    def test_bad_ppm_blocks(self):
        x=copy.deepcopy(self.x);x["articles"][0]["ppm679"]["status"]="FAIL";self.assertIn("PPM:0",w.validate(x))
if __name__=="__main__":unittest.main()
