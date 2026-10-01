import json, unittest
import k9_writer_plan as p

META={
    "title":"Was ist eine Longierpeitsche?",
    "target_keyword":"Was ist eine Longierpeitsche",
    "category":"longierpeitschen-faq",
    "article_type":"FAQ",
    "plan_slot":"slot-1",
}
RESEARCH={
    "portal_links":[
        {"role":"parent_category","anchor":"Training","href":"/training/","section_id":"answer"},
        {"role":"semantic_related","anchor":"Longieren","href":"/training/training-longieren/","section_id":"details"},
        {"role":"further_information","anchor":"Longierpeitschen","href":"/training/training-longieren/longierpeitschen/","section_id":"further_information"},
    ],
    "fact_pack":{"fact_ids":["F1","F2"]},
}
PPM={
    "ppm_version":"6.7.9",
    "global_requirements":{"min_words":750},
    "structure_requirements":{"x":1},
    "type_requirements":{"y":2},
}

class WriterPlanTests(unittest.TestCase):
    def test_plan_compiles_all_hard_writer_constraints(self):
        plan=p.build(META,RESEARCH,PPM)
        self.assertEqual(plan["contract"],"K9_WRITER_ACCEPTANCE_PLAN_V1")
        self.assertEqual(plan["word_budget"]["hard_total_min"],750)
        self.assertEqual(plan["word_budget"]["hard_total_max"],900)
        self.assertEqual(plan["fact_binding"]["source_trace_per_fact_exact"],1)
        self.assertEqual(plan["portal_links"][0]["section_id"],"answer")
        self.assertEqual(plan["portal_links"][1]["section_id"],"details")
        self.assertEqual(plan["table"]["other_cells_hard_max_words"],7)
        self.assertEqual(plan["language"]["unresolved_findings_max"],0)
        self.assertIn("Longierpeitsche",plan["language"]["authoritative_domain_terms"])
        self.assertIn("Longierpeitschen",plan["language"]["authoritative_domain_terms"])
        self.assertEqual(len(plan["plan_sha256"]),64)

    def test_plan_is_deterministic(self):
        self.assertEqual(p.build(META,RESEARCH,PPM),p.build(META,RESEARCH,PPM))

    def test_unsupported_type_fails_closed(self):
        bad=dict(META); bad["article_type"]="Unbekannt"
        with self.assertRaisesRegex(p.WriterPlanError,"WRITER_PLAN_ARTICLE_TYPE_UNSUPPORTED"):
            p.build(bad,RESEARCH,PPM)

if __name__=="__main__": unittest.main()
