import json, sys, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import k9_write_packager

class K9WriterEarlyBindingTest(unittest.TestCase):
    def research(self):
        data=json.loads((ROOT/"warehouse/research/K9-RESEARCH-7ce57ca68dad6301.json").read_text(encoding="utf-8"))
        return data["results"][0]["research_product"]

    def article(self,path):
        data=json.loads((ROOT/path).read_text(encoding="utf-8"))
        return data["results"][0]["article_product"]

    def test_repaired_real_article_passes_exact_ppm_authoring_preflight(self):
        article=self.article("warehouse/repair/K9-REPAIR-e9b15e6f95bc2453.json")
        self.assertTrue(k9_write_packager.exact_ppm_authoring_preflight(article,self.research()))

    def test_original_real_article_is_blocked_before_acceptance(self):
        article=self.article("warehouse/write/K9-WRITE-447847ccdea9ad47.json")
        with self.assertRaisesRegex(
            k9_write_packager.PackError,
            "PPM679_AUTHORING_PREFLIGHT_REPAIR_REQUIRED:.*BLOCKED_CONTENT_FACT_REFS_MISSING"
        ):
            k9_write_packager.exact_ppm_authoring_preflight(article,self.research())

if __name__=="__main__":
    unittest.main()
