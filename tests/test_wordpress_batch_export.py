import hashlib
import unittest

from engine.wordpress_batch_export import combine, BatchBlocked
from engine.k0_wordpress_export import slug_from_title

def single(idx,title,keyword,category,article_type,article_id):
    plan_slot=hashlib.sha256(("pserc-plan-slot-v2|"+article_id).encode()).hexdigest()
    body=f'<article class="ppm-generated ppm-type-{article_type.lower()}" data-article-type="{article_type}"><section data-block="intro"><p>Einleitung {idx}.</p></section><section data-block="conclusion"><h2>Fazit</h2><p>Fazit {idx}.</p></section></article>'
    return {
      "contract":"PFERDE_ATELIER_WORDPRESS_IMPORT_V1",
      "source":"K0_CANONICAL_WORKFLOW",
      "article_count":1,
      "publish_allowed":False,
      "articles":[{
        "article_id":article_id,"plan_slot":plan_slot,"title":title,"slug":slug_from_title(title),
        "target_keyword":keyword,"category":category,"article_type":article_type,"body":body
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
        self.assertEqual(out["contract"],"PFERDE_ATELIER_WORDPRESS_IMPORT_V1")
        self.assertEqual(out["article_count"],3)
        self.assertEqual([x["title"] for x in out["articles"]],["A?","B?","C?"])
        self.assertTrue(all(hashlib.sha256(("pserc-plan-slot-v2|"+x["article_id"]).encode()).hexdigest()==x["plan_slot"] for x in out["articles"]))
        self.assertTrue(all(x["slug"]==slug_from_title(x["title"]) for x in out["articles"]))
        self.assertFalse(out["publish_allowed"])

    def test_article_id_must_bind_to_plan_slot(self):
        i,docs=self.make_three()
        docs[0]["articles"][0]["article_id"]="article:aaaaaaaaaaaaaaaaaaaaaaaa"
        with self.assertRaisesRegex(BatchBlocked,"SINGLE_CANONICAL_PLAN_SLOT_MISMATCH"):
            combine(i,docs)

    def test_article_id_format_blocks(self):
        i,docs=self.make_three()
        docs[0]["articles"][0]["article_id"]=docs[0]["articles"][0]["plan_slot"]
        with self.assertRaisesRegex(BatchBlocked,"SINGLE_ARTICLE_ID_INVALID"):
            combine(i,docs)

    def test_slug_mismatch_blocks(self):
        i,docs=self.make_three()
        docs[0]["articles"][0]["slug"]="falsch"
        with self.assertRaisesRegex(BatchBlocked,"SINGLE_SLUG_MISMATCH"):
            combine(i,docs)

    def test_bare_article_html_blocks(self):
        i,docs=self.make_three()
        row=docs[0]["articles"][0]
        row["body"]=row["body"].replace('<article class="ppm-generated ppm-type-faq" data-article-type="FAQ">','<article>')
        with self.assertRaisesRegex(BatchBlocked,"SINGLE_HTML_INVALID"):
            combine(i,docs)

    def test_missing_article_blocks(self):
        i,docs=self.make_three()
        with self.assertRaisesRegex(BatchBlocked,"BATCH_ARTICLE_MISSING"):
            combine(i,docs[:2])

    def test_identity_mismatch_blocks(self):
        i,docs=self.make_three()
        docs[1]["articles"][0]["title"]="Falscher Titel"
        docs[1]["articles"][0]["slug"]=slug_from_title("Falscher Titel")
        with self.assertRaisesRegex(BatchBlocked,"BATCH_IDENTITY_MISMATCH"):
            combine(i,docs)

if __name__=="__main__":
    unittest.main()
