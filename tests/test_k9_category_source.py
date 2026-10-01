import unittest

import k9_category_source as c

CENTRAL="""term_id\tslug\tname\tparent_slug
534\theutaschen-beratung\tBeratung Heutaschen\t
513\theunetze-faq\tFAQ Heunetze\t
857\tlongierpeitschen-faq\tFAQ Longierpeitschen\t
"""

PORTAL={"categories":[
    {"category_slug":"heutaschen-beratung","category_name":"Beratung Heutaschen","theme":"Beratung","product_slug":"heutaschen","product":"Heutaschen","main_slug":"fuetterung","main_hub":"Fütterung","hub_slug":"fuetterung-raufutter","hub":"Raufutter","path":"Fütterung > Raufutter > Heutaschen > Beratung Heutaschen"},
    {"category_slug":"heunetze-faq","category_name":"FAQ Heunetze","theme":"FAQ","product_slug":"heunetze","product":"Heunetze","main_slug":"fuetterung","main_hub":"Fütterung","hub_slug":"fuetterung-raufutter","hub":"Raufutter","path":"Fütterung > Raufutter > Heunetze > FAQ Heunetze"},
    {"category_slug":"longierpeitschen-faq","category_name":"FAQ Longierpeitschen","theme":"FAQ","product_slug":"longierpeitschen","product":"Longierpeitschen","main_slug":"training","main_hub":"Training","hub_slug":"training-longieren","hub":"Longieren","path":"Training > Longieren > Longierpeitschen > FAQ Longierpeitschen"},
]}

class CentralCategoryTests(unittest.TestCase):
    def test_three_current_categories_resolve_from_central_source(self):
        cases=[
            ("heutaschen-beratung","Beratung","/fuetterung/fuetterung-raufutter/heutaschen/"),
            ("heunetze-faq","FAQ","/fuetterung/fuetterung-raufutter/heunetze/"),
            ("longierpeitschen-faq","FAQ","/training/training-longieren/longierpeitschen/"),
        ]
        for slug,article_type,leaf in cases:
            result=c.portal_context({"category":slug,"article_type":article_type},CENTRAL,PORTAL)
            self.assertEqual(len(result["portal_links"]),3)
            self.assertEqual(result["portal_links"][2]["href"],leaf)

    def test_unknown_central_category_fails_closed(self):
        with self.assertRaisesRegex(c.CategorySourceError,"CENTRAL_CATEGORY_MISSING:wirklich-neu-faq"):
            c.portal_context({"category":"wirklich-neu-faq","article_type":"FAQ"},CENTRAL,PORTAL)

    def test_missing_portal_context_fails_closed(self):
        portal={"categories":PORTAL["categories"][1:]}
        with self.assertRaisesRegex(c.CategorySourceError,"CENTRAL_CATEGORY_PORTAL_CONTEXT_MISSING:heutaschen-beratung"):
            c.portal_context({"category":"heutaschen-beratung","article_type":"Beratung"},CENTRAL,portal)

    def test_article_type_drift_fails_closed(self):
        with self.assertRaisesRegex(c.CategorySourceError,"CENTRAL_CATEGORY_ARTICLE_TYPE_MISMATCH:heutaschen-beratung"):
            c.portal_context({"category":"heutaschen-beratung","article_type":"FAQ"},CENTRAL,PORTAL)

    def test_batch_preflight_validates_all_rows_before_production(self):
        rows=[
            {"category":"heutaschen-beratung","article_type":"Beratung"},
            {"category":"heunetze-faq","article_type":"FAQ"},
            {"category":"longierpeitschen-faq","article_type":"FAQ"},
        ]
        result=c.validate_batch(rows,CENTRAL,PORTAL)
        self.assertEqual(result["status"],"PASS")
        self.assertEqual(result["validated"],3)

if __name__=="__main__":
    unittest.main()
