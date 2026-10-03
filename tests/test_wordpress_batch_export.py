import hashlib
import unittest

from engine.wordpress_batch_export import combine, BatchBlocked

def slot(article_id):
    return hashlib.sha256(("pserc-plan-slot-v2|"+article_id).encode()).hexdigest()

def single(idx,title,keyword,category,article_type,article_id):
    ps=slot(article_id)
    body=f'<article class="ppm-generated ppm-type-{article_type.lower()}" data-article-type="{article_type}"><section data-block="intro"><p>Einleitung {idx}.</p></section><section data-block="conclusion"><h2>Fazit</h2><p>Fazit {idx}.</p></section></article>'
    return {
      "contract":"SYSTEM4_WORDPRESS_HANDOFF_V1",
      "batch_sha256":"a"*64,
      "article_count":1,
      "publish_allowed":False,
      "signing_deferred":True,
      "batch_gate_status":"SYSTEM4_BATCH_FULL_PASS_COLLECTED",
      "no_legacy_status":"PASS",
      "test_suite_status":"PASS",
      "wordpress_review":{"direct_wordpress_upload_ready":True},
      "articles":[{
        "index":0,"title":title,"target_keyword":keyword,
        "category":category,"article_type":article_type,"plan_slot":ps,
        "final_draft_sha256":hashlib.sha256(body.encode()).hexdigest(),
        "revision_count":1,"body":body,
        "production_context":{"production_plan_item":{"canonical_article_id":article_id}},
        "languagetool":{"status":"PASS","finding_count":0},
        "ppm679":{"status":"PASS"}
      }]
    }

def intake(rows):
    return {
      "contract":"PSERC_TEXTMACHINE_METADATA_BATCH_V2",
      "status":"READY_FOR_TEXTMACHINE_METADATA_INTAKE",
      "item_count":len(rows),
      "maximum_articles":0,
      "maximum_articles_per_type":0,
      "publish_allowed":False,
      "content_or_format_payload_present":False,
      "batch_sha256":"a"*64,
      "items":rows,
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
        self.assertEqual(out["article_count"],3)
        self.assertEqual([x["title"] for x in out["articles"]],["A?","B?","C?"])
        self.assertTrue(all(x["body"].startswith('<article class="ppm-generated ppm-type-faq"') for x in out["articles"]))
        self.assertFalse(out["publish_allowed"])

    def test_wrong_canonical_article_id_slot_binding_blocks(self):
        i,docs=self.make_three()
        docs[0]["articles"][0]["production_context"]["production_plan_item"]["canonical_article_id"]="article:aaaaaaaaaaaaaaaaaaaaaaaa"
        with self.assertRaisesRegex(BatchBlocked,"SINGLE_CANONICAL_ARTICLE_ID_PLAN_SLOT_MISMATCH"):
            combine(i,docs)

    def test_top_level_article_id_is_blocked(self):
        i,docs=self.make_three()
        docs[0]["articles"][0]["article_id"]="article:111111111111111111111111"
        with self.assertRaisesRegex(BatchBlocked,"SINGLE_TOPLEVEL_ARTICLE_ID_FORBIDDEN"):
            combine(i,docs)

    def test_bare_article_html_blocks(self):
        i,docs=self.make_three()
        row=docs[0]["articles"][0]
        row["body"]=row["body"].replace('<article class="ppm-generated ppm-type-faq" data-article-type="FAQ">','<article>')
        row["final_draft_sha256"]=hashlib.sha256(row["body"].encode()).hexdigest()
        with self.assertRaisesRegex(BatchBlocked,"SINGLE_HTML_INVALID"):
            combine(i,docs)

    def test_missing_article_blocks(self):
        i,docs=self.make_three()
        with self.assertRaisesRegex(BatchBlocked,"BATCH_ARTICLE_MISSING"):
            combine(i,docs[:2])

    def test_identity_mismatch_blocks(self):
        i,docs=self.make_three()
        docs[1]["articles"][0]["title"]="Falscher Titel"
        with self.assertRaisesRegex(BatchBlocked,"BATCH_IDENTITY_MISMATCH"):
            combine(i,docs)

if __name__=="__main__":
    unittest.main()
