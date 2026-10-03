import hashlib
import unittest
from engine.wordpress_batch_export import combine, BatchBlocked

def single(idx,title,keyword,category,article_type,article_id):
    slot=hashlib.sha256(("pserc-plan-slot-v2|"+article_id).encode()).hexdigest()
    body=f'<article class="ppm-generated ppm-type-{article_type.lower()}" data-article-type="{article_type}"><section data-block="intro"><p>Einleitung {idx}.</p></section><section data-block="conclusion"><h2>Fazit</h2><p>Fazit {idx}.</p></section></article>'
    sha=hashlib.sha256(body.encode()).hexdigest()
    row={
      "index":0,"article_id":article_id,"title":title,"target_keyword":keyword,
      "category":category,"article_type":article_type,"plan_slot":slot,
      "final_draft_sha256":sha,"revision_count":1,"body":body,
      "production_context":{
        "fact_pack":{"contract":"canonical_fact_pack_v1","status":"SOURCE_VERIFIED_PRODUCTION_READY","sources":[],"claims":[]},
        "production_plan_item":{
          "canonical_article_id":article_id,"article_type":article_type,"target_keyword":keyword,"topic":title,
          "canonical_article":{"title":title,"article_type":article_type,"slug":"test","body_html":body,"body_html_sha256":sha},
          "quality_binding":{"wordpress_category":{"id":1,"slug":category,"taxonomy":"category"}},
          "runtime_order":{"article_type":article_type,"title":title,"slug":"test","subject_scope":title,"subject_label":keyword,"allowed_fact_ids":[]}
        }
      },
      "languagetool":{"status":"PASS","finding_count":0,"engine":"LanguageTool 6.8"},
      "ppm679":{"status":"PASS","ppm_version":"6.7.9","technical_status":"TECHNICAL_CHECK_OK","content_quality_status":"CONTENT_QUALITY_CHECK_OK","fail_closed_aggregate_status":"PASS","content_sha256":sha}
    }
    return {
      "contract":"SYSTEM4_WORDPRESS_HANDOFF_V1","batch_sha256":"a"*64,"article_count":1,
      "publish_allowed":False,"signing_deferred":True,"batch_gate_status":"SYSTEM4_BATCH_FULL_PASS_COLLECTED",
      "no_legacy_status":"PASS","test_suite_status":"PASS",
      "wordpress_review":{"direct_wordpress_upload_ready":True},
      "articles":[row]
    }

def intake(rows):
    return {
      "contract":"PSERC_TEXTMACHINE_METADATA_BATCH_V2","status":"READY_FOR_TEXTMACHINE_METADATA_INTAKE",
      "item_count":len(rows),"maximum_articles":0,"maximum_articles_per_type":0,"publish_allowed":False,
      "content_or_format_payload_present":False,"batch_sha256":"a"*64,"items":rows,
    }

class BatchExportTests(unittest.TestCase):
    def make_three(self):
        specs=[
          ("A?","A","faq-a","FAQ","article:111111111111111111111111"),
          ("B?","B","faq-b","FAQ","article:222222222222222222222222"),
          ("C?","C","faq-c","FAQ","article:333333333333333333333333"),
        ]
        docs=[single(i,*x) for i,x in enumerate(specs)]
        rows=[{k:d["articles"][0][k] for k in ("article_type","category","plan_slot","target_keyword","title")} for d in docs]
        return intake(rows),docs

    def test_positive_three_article_batch_preserves_input_order(self):
        i,docs=self.make_three()
        out=combine(i,[docs[2],docs[0],docs[1]])
        self.assertEqual(out["contract"],"SYSTEM4_WORDPRESS_HANDOFF_V1")
        self.assertEqual(out["article_count"],3)
        self.assertEqual([x["title"] for x in out["articles"]],["A?","B?","C?"])
        self.assertTrue(all(hashlib.sha256(("pserc-plan-slot-v2|"+x["article_id"]).encode()).hexdigest()==x["plan_slot"] for x in out["articles"]))
        self.assertFalse(out["publish_allowed"])

    def test_article_id_slot_mismatch_blocks(self):
        i,docs=self.make_three()
        docs[0]["articles"][0]["article_id"]="article:aaaaaaaaaaaaaaaaaaaaaaaa"
        with self.assertRaisesRegex(BatchBlocked,"SINGLE_ARTICLE_ID_PLAN_SLOT_MISMATCH"):
            combine(i,docs)

    def test_nested_canonical_id_mismatch_blocks(self):
        i,docs=self.make_three()
        docs[0]["articles"][0]["production_context"]["production_plan_item"]["canonical_article_id"]="article:aaaaaaaaaaaaaaaaaaaaaaaa"
        with self.assertRaisesRegex(BatchBlocked,"SINGLE_NESTED_CANONICAL_ID_MISMATCH"):
            combine(i,docs)

    def test_missing_article_blocks(self):
        i,docs=self.make_three()
        with self.assertRaisesRegex(BatchBlocked,"BATCH_ARTICLE_MISSING"):
            combine(i,docs[:2])

if __name__=="__main__":
    unittest.main()
