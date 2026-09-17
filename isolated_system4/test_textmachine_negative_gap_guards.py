import hashlib
import unittest

import content_guard
import design_guard
import production_checks


def sha(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


E1 = 'Die konkrete Auswahl richtet sich nach dem tatsächlichen Einsatzzweck und der sicheren Handhabung.'
E2 = 'Materialzustand und passende Nutzung müssen vor dem Einsatz konkret geprüft werden.'
SOURCE_EVIDENCE = E1 + '\n' + E2 + '\nZusätzlicher Quellenkontext für den lokalen Nachweis.'


def good_pack():
    source = {
        'source_id': 'src-official-1',
        'source_title': 'Fachquelle – konkrete Anleitung',
        'source_url': 'https://example.org/fachquelle',
        'retrieved_at': '2026-09-12T20:00:00Z',
        'snapshot_sha256': sha(SOURCE_EVIDENCE),
        'evidence': SOURCE_EVIDENCE,
    }
    return {
        'contract': 'canonical_fact_pack_v1',
        'status': 'SOURCE_VERIFIED_PRODUCTION_READY',
        'sources': [source],
        'claims': [
            {'fact_id': 'fact-a', 'source_id': 'src-official-1', 'statement': 'Der Einsatzzweck ist ein konkretes Auswahlkriterium.', 'evidence_text': E1, 'evidence_text_sha256': sha(E1)},
            {'fact_id': 'fact-b', 'source_id': 'src-official-1', 'statement': 'Der Materialzustand ist vor der Nutzung zu prüfen.', 'evidence_text': E2, 'evidence_text_sha256': sha(E2)},
        ],
    }


def canonical_body(extra: str = '') -> str:
    return (
        '<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung">'
        '<section data-block="intro"><p>Einleitung.</p></section>'
        '<section data-block="criteria"><h2>Auswahl</h2><p>Inhalt.</p>'
        '<table class="system-129-table comparison-table">'
        '<tr><th>Kriterium</th><th>Wert</th></tr><tr><td>A</td><td>B</td></tr>'
        '</table></section>' + extra + '</article>'
    )


class TextmachineNegativeGapGuardTests(unittest.TestCase):
    def assert_content_code(self, code, fn):
        with self.subTest(code=code):
            with self.assertRaisesRegex(content_guard.ContentGuardError, code):
                fn()

    def test_25_content_guard_gap_codes_are_exact(self):
        cases = []

        cases.append(('FACT_PACK_OBJECT_REQUIRED', lambda: content_guard.validate_fact_pack(None)))

        def mutate_pack(mutator):
            def run():
                pack = good_pack(); mutator(pack); content_guard.validate_fact_pack(pack)
            return run

        cases += [
            ('FACT_PACK_CONTRACT_INVALID', mutate_pack(lambda p: p.__setitem__('contract', 'wrong'))),
            ('FACT_PACK_NOT_PRODUCTION_READY', mutate_pack(lambda p: p.__setitem__('status', 'NOT_READY'))),
            ('FACT_PACK_SOURCE_OBJECT_REQUIRED', mutate_pack(lambda p: p.__setitem__('sources', [None]))),
            ('FACT_PACK_SOURCE_ID_INVALID', mutate_pack(lambda p: p['sources'][0].__setitem__('source_id', ''))),
            ('FACT_PACK_SOURCE_TITLE_INVALID', mutate_pack(lambda p: p['sources'][0].__setitem__('source_title', ''))),
            ('FACT_PACK_SOURCE_URL_INVALID', mutate_pack(lambda p: p['sources'][0].__setitem__('source_url', 'not-a-url'))),
            ('FACT_PACK_SOURCE_RETRIEVED_AT_INVALID', mutate_pack(lambda p: p['sources'][0].__setitem__('retrieved_at', ''))),
            ('FACT_PACK_SOURCE_HASH_INVALID', mutate_pack(lambda p: p['sources'][0].__setitem__('snapshot_sha256', 'bad'))),
            ('FACT_PACK_SOURCE_TITLE_SYNTHETIC', mutate_pack(lambda p: p['sources'][0].__setitem__('source_title', p['sources'][0]['source_id']))),
            ('FACT_PACK_SOURCE_HASH_MISMATCH', mutate_pack(lambda p: p['sources'][0].__setitem__('snapshot_sha256', '0' * 64))),
            ('FACT_PACK_SOURCE_ID_DUPLICATE', mutate_pack(lambda p: p.__setitem__('sources', [p['sources'][0], dict(p['sources'][0], snapshot_sha256=sha(SOURCE_EVIDENCE + 'x'), evidence=SOURCE_EVIDENCE + 'x')]))),
            ('FACT_PACK_CLAIMS_TOO_LOW', mutate_pack(lambda p: p.__setitem__('claims', []))),
            ('FACT_PACK_CLAIM_OBJECT_REQUIRED', mutate_pack(lambda p: p.__setitem__('claims', [None, p['claims'][1]]))),
            ('FACT_ID_INVALID', mutate_pack(lambda p: p['claims'][0].__setitem__('fact_id', ''))),
            ('FACT_SOURCE_ID_INVALID', mutate_pack(lambda p: p['claims'][0].__setitem__('source_id', ''))),
            ('FACT_STATEMENT_INVALID', mutate_pack(lambda p: p['claims'][0].__setitem__('statement', 'kurz'))),
            ('FACT_EVIDENCE_TEXT_INVALID', mutate_pack(lambda p: p['claims'][0].__setitem__('evidence_text', 'kurz'))),
            ('FACT_EVIDENCE_HASH_INVALID', mutate_pack(lambda p: p['claims'][0].__setitem__('evidence_text_sha256', 'bad'))),
            ('FACT_EVIDENCE_HASH_MISMATCH', mutate_pack(lambda p: p['claims'][0].__setitem__('evidence_text_sha256', '0' * 64))),
            ('FACT_PACK_FACT_ID_DUPLICATE', mutate_pack(lambda p: p['claims'][1].__setitem__('fact_id', p['claims'][0]['fact_id']))),
            ('FACT_PACK_CLAIM_SOURCE_URL_MISMATCH', mutate_pack(lambda p: p['claims'][0].__setitem__('source_url', 'https://wrong.example/'))),
            ('ARTICLE_FACT_PACK_CLAIMS_MISSING', lambda: content_guard.validate_article_fact_ids('<p data-fact-id="fact-a">Text</p>', {'claims': []})),
            ('ARTICLE_FACT_IDS_MISSING', lambda: content_guard.validate_article_fact_ids('<p>Text</p>', {'claims': [{'statement': 'x'}]})),
            ('ARTICLE_FACT_TRACE_MISSING', lambda: content_guard.validate_single_article('<article><p>Text ohne Fact-Trace</p></article>', good_pack())),
        ]
        self.assertEqual(len(cases), 25)
        for code, fn in cases:
            self.assert_content_code(code, fn)

    def assert_design_code(self, code, fn):
        with self.subTest(code=code):
            with self.assertRaisesRegex(design_guard.DesignGuardError, code):
                fn()

    def test_11_design_guard_gap_codes_are_exact(self):
        body = canonical_body()
        cases = [
            ('DESIGN_ARTICLE_TYPE_TOKEN_INVALID', lambda: design_guard.article_type_class('***')),
            ('DESIGN_BODY_EMPTY', lambda: design_guard.validate_design_neutrality('', 'Beratung')),
            ('DESIGN_ARTICLE_TYPE_MISSING', lambda: design_guard.validate_design_neutrality(body, '')),
            ('DESIGN_ACTIVE_OR_GLOBAL_HTML_FORBIDDEN', lambda: design_guard.validate_design_neutrality(body.replace('<p>Einleitung.</p>', '<script>bad()</script><p>Einleitung.</p>'), 'Beratung')),
            ('DESIGN_EVENT_HANDLER_FORBIDDEN', lambda: design_guard.validate_design_neutrality(body.replace('<p>Einleitung.</p>', '<p onclick="bad()">Einleitung.</p>'), 'Beratung')),
            ('DESIGN_JAVASCRIPT_URL_FORBIDDEN', lambda: design_guard.validate_design_neutrality(body.replace('<p>Einleitung.</p>', '<p><a href="javascript:bad()">Einleitung</a></p>'), 'Beratung')),
            ('DESIGN_CANONICAL_ARTICLE_ROOT_MISSING', lambda: design_guard.validate_design_neutrality('<div>Text</div>', 'Beratung')),
            ('DESIGN_ARTICLE_TYPE_ATTRIBUTE_MISMATCH', lambda: design_guard.validate_design_neutrality(body.replace('data-article-type="Beratung"', 'data-article-type="FAQ"'), 'Beratung')),
            ('DESIGN_NESTED_ARTICLE_FORBIDDEN', lambda: design_guard.validate_design_neutrality(body.replace('</article>', '<article></article></article>'), 'Beratung')),
            ('DESIGN_TABLE_COMPARISON_CLASS_MISSING', lambda: design_guard.validate_design_neutrality(body.replace('system-129-table comparison-table', 'system-129-table'), 'Beratung')),
            ('DESIGN_TABLE_INLINE_STYLE_FORBIDDEN', lambda: design_guard.validate_design_neutrality(body.replace('<table class="system-129-table comparison-table">', '<table class="system-129-table comparison-table" style="width:100%">'), 'Beratung')),
        ]
        self.assertEqual(len(cases), 11)
        for code, fn in cases:
            self.assert_design_code(code, fn)

    def test_2_external_link_gap_codes_are_exact(self):
        cases = [
            ('EXTERNAL_LINK_FORBIDDEN', '<article><a href="https://example.org/x">Extern</a></article>'),
            ('EXTERNAL_URL_FORBIDDEN', '<article><p>Siehe https://example.org/x für Details.</p></article>'),
        ]
        for expected, article in cases:
            with self.subTest(expected=expected):
                with self.assertRaises(production_checks.RepairRequired) as ctx:
                    production_checks.no_external_links(article)
                self.assertEqual(ctx.exception.checker, 'no_external_links')
                codes = [str(x.get('error_code') or '') for x in ctx.exception.findings]
                self.assertIn(expected, codes)


if __name__ == '__main__':
    unittest.main(verbosity=2)
