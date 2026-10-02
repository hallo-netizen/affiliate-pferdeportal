import copy
import unittest

from engine.html_design import (
    DesignBlocked,
    article_type_token,
    materialize_canonical_root,
    validate_canonical_html,
    visible_text,
)


def base(article_type="FAQ", body=None):
    return {
        "article_type": article_type,
        "html": body or (
            '<article>'
            '<section data-block="intro"><p>Ein sichtbarer Satz bleibt unverändert.</p></section>'
            '<section data-block="details"><h2>Details</h2><p>Noch ein sichtbarer Satz.</p></section>'
            '<section data-block="conclusion"><h2>Fazit</h2><p>Das Fazit bleibt ebenfalls unverändert.</p></section>'
            '</article>'
        ),
    }


class K10CanonicalHtmlTests(unittest.TestCase):
    def test_bare_root_is_repaired_without_visible_text_change(self):
        a=base("FAQ")
        before=visible_text(a["html"])
        out,receipt=materialize_canonical_root(a)
        self.assertTrue(receipt["root_repaired"])
        self.assertFalse(receipt["visible_text_changed"])
        self.assertEqual(before,visible_text(out["html"]))
        self.assertTrue(out["html"].startswith('<article class="ppm-generated ppm-type-faq" data-article-type="FAQ">'))
        self.assertEqual(validate_canonical_html(out)["status"],"PASS")

    def test_existing_valid_root_is_not_rewritten(self):
        body=(
            '<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung">'
            '<section data-block="intro"><p>Text bleibt Text.</p></section>'
            '<section data-block="conclusion"><h2>Fazit</h2><p>Weiterer Text.</p></section>'
            '</article>'
        )
        a=base("Beratung",body)
        out,receipt=materialize_canonical_root(a)
        self.assertFalse(receipt["root_repaired"])
        self.assertEqual(out["html"],body)

    def test_partial_or_conflicting_root_does_not_get_silently_repaired(self):
        for body,code in [
            ('<article class="ppm-type-faq" data-article-type="FAQ"><p>Text</p></article>',"DESIGN_PPM_GENERATED_CLASS_MISSING"),
            ('<article class="ppm-generated ppm-type-pflege" data-article-type="FAQ"><p>Text</p></article>',"DESIGN_ARTICLE_TYPE_CLASS_MISSING"),
            ('<article class="ppm-generated ppm-type-faq" data-article-type="Pflege"><p>Text</p></article>',"DESIGN_ARTICLE_TYPE_ATTRIBUTE_MISMATCH"),
        ]:
            with self.subTest(code=code):
                with self.assertRaisesRegex(DesignBlocked,code):
                    materialize_canonical_root(base("FAQ",body))

    def test_active_or_inline_html_is_hard_blocked(self):
        bad=[
            ('<article><script>alert(1)</script><p>Text</p></article>',"DESIGN_ACTIVE_OR_GLOBAL_HTML_FORBIDDEN"),
            ('<article><p style="display:none">Text</p></article>',"DESIGN_INLINE_STYLE_FORBIDDEN"),
            ('<article><p onclick="bad()">Text</p></article>',"DESIGN_EVENT_HANDLER_FORBIDDEN"),
            ('<article><a href="javascript:bad()">Text</a></article>',"DESIGN_JAVASCRIPT_URL_FORBIDDEN"),
        ]
        for body,code in bad:
            with self.subTest(code=code):
                with self.assertRaisesRegex(DesignBlocked,code):
                    materialize_canonical_root(base("FAQ",body))

    def test_table_classes_are_required(self):
        good=(
            '<article>'
            '<section data-block="intro"><p>Einleitung.</p></section>'
            '<section data-block="table"><h2>Tabelle</h2>'
            '<table class="system-129-table comparison-table"><tr><th>A</th><th>B</th></tr><tr><td>X</td><td>Y</td></tr></table>'
            '</section><section data-block="conclusion"><h2>Fazit</h2><p>Fazit.</p></section></article>'
        )
        out,_=materialize_canonical_root(base("FAQ",good))
        self.assertEqual(validate_canonical_html(out)["table_count"],1)

        bad=good.replace('system-129-table comparison-table','comparison-table')
        with self.assertRaisesRegex(DesignBlocked,"DESIGN_TABLE_SYSTEM129_CLASS_MISSING"):
            materialize_canonical_root(base("FAQ",bad))

    def test_type_token_matches_historical_selector_convention(self):
        self.assertEqual(article_type_token("FAQ"),"ppm-type-faq")
        self.assertEqual(article_type_token("Beratung"),"ppm-type-beratung")
        self.assertEqual(article_type_token("Pflege"),"ppm-type-pflege")
        self.assertEqual(article_type_token("Vergleich"),"ppm-type-vergleich")


if __name__=="__main__":
    unittest.main()
