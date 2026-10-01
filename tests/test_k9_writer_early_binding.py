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


    def test_source_traces_are_machine_canonicalized_exactly_once(self):
        research={
            "fact_pack":{
                "fact_ids":["F1"],
                "claims":[{
                    "fact_id":"F1",
                    "source_id":"S1",
                    "evidence_text_sha256":"HASH1",
                    "statement":"Heunetze können die Fressdauer verlängern."
                }]
            },
            "sources":[{"source_id":"S1","title":"Quelle"}]
        }
        stale='<span class="ppm-source-trace" data-fact-id="F1" data-source-hash="OLD" data-source-title="OLD"></span>'
        markup='<p data-fact-ids="F1">'+stale+stale+'Heunetze können die Fressdauer verlängern.</p>'
        out=k9_write_packager.ensure_all_fact_traces(markup,research)
        self.assertEqual(out.count('class="ppm-source-trace"'),1)
        self.assertIn('data-fact-id="F1"',out)
        self.assertIn('data-source-hash="HASH1"',out)
        self.assertIn('data-source-title="S1"',out)
        self.assertNotIn('data-source-hash="OLD"',out)
        self.assertEqual(k9_write_packager.text_of(markup),k9_write_packager.text_of(out))

if __name__=="__main__":
    unittest.main()
