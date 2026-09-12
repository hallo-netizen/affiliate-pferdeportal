import unittest

import design_guard


def canonical_body(extra: str = '') -> str:
    return (
        '<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung">'
        '<section data-block="intro"><p>Einleitung.</p></section>'
        '<section data-block="criteria"><h2>Auswahl</h2><p>Inhalt.</p>'
        '<table class="system-129-table comparison-table">'
        '<tr><th>Kriterium</th><th>Wert</th></tr><tr><td>A</td><td>B</td></tr>'
        '</table></section>'
        + extra +
        '</article>'
    )


class DesignGuardTests(unittest.TestCase):
    def test_existing_canonical_design_passes_without_mutation(self):
        body = canonical_body()
        result = design_guard.validate_design_neutrality(body, 'Beratung')
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(result['table_count'], 1)
        self.assertFalse(result['content_mutation_performed'])
        self.assertFalse(result['design_mutation_performed'])
        self.assertEqual(body, canonical_body())

    def test_historical_missing_root_classes_is_blocked(self):
        body = '<article><h2>Auswahl</h2><p>Text.</p><table class="comparison-table"><tr><td>A</td><td>B</td></tr></table></article>'
        with self.assertRaisesRegex(design_guard.DesignGuardError, 'DESIGN_PPM_GENERATED_CLASS_MISSING'):
            design_guard.validate_design_neutrality(body, 'Beratung')

    def test_historical_table_class_drift_is_blocked(self):
        body = canonical_body().replace('system-129-table comparison-table', 'comparison-table')
        with self.assertRaisesRegex(design_guard.DesignGuardError, 'DESIGN_TABLE_SYSTEM129_CLASS_MISSING'):
            design_guard.validate_design_neutrality(body, 'Beratung')

    def test_beratung_h3_design_drift_is_blocked(self):
        body = canonical_body('<h3>Abweichende Zwischenüberschrift</h3>')
        with self.assertRaisesRegex(design_guard.DesignGuardError, 'DESIGN_BERATUNG_HEADING_LEVEL_FORBIDDEN'):
            design_guard.validate_design_neutrality(body, 'Beratung')

    def test_inline_style_is_blocked_not_repaired(self):
        body = canonical_body().replace('<p>Einleitung.</p>', '<p style="color:red">Einleitung.</p>')
        with self.assertRaisesRegex(design_guard.DesignGuardError, 'DESIGN_INLINE_STYLE_FORBIDDEN'):
            design_guard.validate_design_neutrality(body, 'Beratung')
        self.assertIn('style="color:red"', body)

    def test_wrong_article_type_class_is_blocked(self):
        body = canonical_body().replace('ppm-type-beratung', 'ppm-type-pflege')
        with self.assertRaisesRegex(design_guard.DesignGuardError, 'DESIGN_ARTICLE_TYPE_CLASS_MISSING:ppm-type-beratung'):
            design_guard.validate_design_neutrality(body, 'Beratung')


if __name__ == '__main__':
    unittest.main(verbosity=2)
