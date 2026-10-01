import json, unittest
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str((ROOT/"quality").resolve()))
import k9_structural_guard as g

class StructuralCollectAllTests(unittest.TestCase):
    def setUp(self):
        self.rules=json.loads((ROOT/"contracts/K9_WRITING_RULES.json").read_text())
        self.meta={
            "title":"Was ist eine Longierpeitsche?",
            "target_keyword":"Was ist eine Longierpeitsche",
            "article_type":"FAQ",
            "category":"longierpeitschen-faq",
            "plan_slot":"slot",
        }
        self.research={
            "portal_links":[
                {"role":"parent_category","href":"/training/","anchor":"Training","section_id":"answer"},
                {"role":"semantic_related","href":"/training/training-longieren/","anchor":"Longieren","section_id":"details"},
                {"role":"further_information","href":"/training/training-longieren/longierpeitschen/","anchor":"Longierpeitschen","section_id":"further_information"},
            ],
            "fact_pack":{
                "fact_ids":["F1","F2"],
                "claims":[
                    {"fact_id":"F1","source_id":"S1","evidence_text_sha256":"H1"},
                    {"fact_id":"F2","source_id":"S2","evidence_text_sha256":"H2"},
                ],
            },
            "sources":[
                {"source_id":"S1","title":"One"},
                {"source_id":"S2","title":"Two"},
            ],
        }

    def test_many_structural_failures_are_returned_together(self):
        result=g.evaluate("<article><p>kurz</p></article>","FAQ",self.meta,self.research,self.rules)
        self.assertEqual(result["status"],"REPAIR_REQUIRED")
        codes={x["code"] for x in result["findings"]}
        for expected in (
            "REQUIRED_BLOCK_MISSING",
            "TABLE_COUNT_NOT_EXACT_ONE",
            "TABLE_SECTION_MISSING",
            "PPM_SOURCE_TRACE_FACT_SET_MISMATCH",
            "PPM_SOURCE_TRACE_COUNT_INVALID",
            "AI_DISCLOSURE_MISSING",
            "VISIBLE_LINK_COUNT_NOT_EXACT_THREE",
            "LINK_BINDING_MISMATCH",
            "FACT_ID_BINDING_INVALID",
            "NOT_ALL_RESEARCH_FACTS_USED",
        ):
            self.assertIn(expected,codes)

    def test_duplicate_and_missing_traces_are_reported_in_same_pass(self):
        markup='''<article>
<section data-block="intro"><p data-fact-ids="F1 F2"><span class="ppm-source-trace" data-fact-id="F1" data-source-hash="H1" data-source-title="S1"></span><span class="ppm-source-trace" data-fact-id="F1" data-source-hash="H1" data-source-title="S1"></span>Text</p></section>
<section data-block="answer"><p>Antwort</p><a data-link-role="parent_category" href="/training/">Training</a></section>
<section data-block="details"><p>Details</p><a data-link-role="semantic_related" href="/training/training-longieren/">Longieren</a></section>
<section data-block="checklist"><p>Liste</p></section>
<section data-block="table"><table class="system-129-table comparison-table"><tbody><tr><td>x</td></tr></tbody></table><p>Diese Zusammenfassung enthält ausreichend Wörter für den vorgesehenen kurzen Absatz nach der Tabelle.</p></section>
<section data-block="conclusion"><p>Fazit</p></section>
<section data-block="further_information"><a data-link-role="further_information" href="/training/training-longieren/longierpeitschen/">Longierpeitschen</a><p class="ppm-ai-disclosure">KI</p></section>
</article>'''
        result=g.evaluate(markup,"FAQ",self.meta,self.research,self.rules)
        trace=[x for x in result["findings"] if x["code"]=="PPM_SOURCE_TRACE_COUNT_INVALID"]
        self.assertEqual(len(trace),1)
        self.assertEqual(trace[0]["counts"],{"F1":2,"F2":0})

if __name__=="__main__": unittest.main()
