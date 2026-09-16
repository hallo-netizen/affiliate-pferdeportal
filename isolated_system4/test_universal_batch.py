import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import batch_repetition_guard
import content_guard
import design_guard
import handoff_transport as ht


def sha(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


class UniversalBatchTests(unittest.TestCase):
    TYPES = ['Beratung', 'Produktvergleich', 'Pferderasse', 'Glossar Begriff']

    def fact_pack(self, i: int):
        source_id = f'src-{i}'
        e1 = f'Konkreter Quellenbeleg A für Artikel {i} mit eindeutig gebundener fachlicher Aussage.'
        e2 = f'Konkreter Quellenbeleg B für Artikel {i} mit zweiter eindeutig gebundener fachlicher Aussage.'
        evidence = e1 + '\n' + e2 + '\n' + f'Gesicherter Zusatzkontext für Artikel {i}.'
        return {
            'contract': 'canonical_fact_pack_v1',
            'status': 'SOURCE_VERIFIED_PRODUCTION_READY',
            'sources': [{
                'source_id': source_id,
                'source_title': f'Fachquelle {i}',
                'source_url': f'https://example.org/source-{i}',
                'retrieved_at': '2026-09-13T08:00:00Z',
                'snapshot_sha256': sha(evidence),
                'evidence': evidence,
            }],
            'claims': [
                {'fact_id': f'fact-{i}-a', 'source_id': source_id, 'statement': f'Aussage A {i} ist fachlich gebunden.', 'evidence_text': e1, 'evidence_text_sha256': sha(e1)},
                {'fact_id': f'fact-{i}-b', 'source_id': source_id, 'statement': f'Aussage B {i} ist fachlich gebunden.', 'evidence_text': e2, 'evidence_text_sha256': sha(e2)},
            ],
        }

    def body(self, i: int, article_type: str) -> str:
        type_class = design_guard.article_type_class(article_type)
        unique = ' '.join(f'unique{i}_{n}' for n in range(30))
        return (
            f'<article class="ppm-generated {type_class}" data-article-type="{article_type}">'
            f'<h2>Abschnitt {i}</h2>'
            f'<p data-fact-ids="fact-{i}-a fact-{i}-b">Einzigartiger Inhalt {i}: {unique}</p>'
            '<table class="system-129-table comparison-table">'
            f'<tr><th>Kriterium {i}</th><th>Wert {i}</th></tr>'
            f'<tr><td>Eigen {i}</td><td>Gebunden {i}</td></tr></table>'
            '</article>'
        )

    def payload(self, count: int):
        rows = []
        for i in range(count):
            article_type = self.TYPES[i % len(self.TYPES)]
            body = self.body(i, article_type)
            body_sha = sha(body)
            rows.append({
                'index': i,
                'title': f'Titel {i}',
                'target_keyword': f'Keyword {i}',
                'category': f'cat-{i}',
                'article_type': article_type,
                'plan_slot': sha(f'slot-{i}'),
                'final_draft_sha256': body_sha,
                'revision_count': 1,
                'body': body,
                'production_context': {'fact_pack': self.fact_pack(i), 'production_plan_item': {'contract': 'production_plan_v4'}},
                'languagetool': {'status': 'PASS', 'finding_count': 0, 'engine': 'LanguageTool 6.8 / Bestand 43'},
                'ppm679': {'status': 'PASS', 'ppm_version': '6.7.9', 'technical_status': 'TECHNICAL_CHECK_OK', 'content_quality_status': 'CONTENT_QUALITY_CHECK_OK', 'fail_closed_aggregate_status': 'PASS', 'content_sha256': body_sha},
            })
        return {
            'contract': ht.HANDOFF_CONTRACT,
            'batch_sha256': sha(f'batch-{count}'),
            'publish_allowed': False,
            'signing_deferred': True,
            'batch_gate_status': 'SYSTEM4_BATCH_FULL_PASS_COLLECTED',
            'no_legacy_status': 'PASS',
            'test_suite_status': 'PASS',
            'wordpress_review': {
                'file_format': 'JSON', 'mime_type': 'application/json', 'intended_next_step': 'WORDPRESS_DIRECT_IMPORT',
                'plugin_name': 'Portal SEO Editorial Plan Compiler', 'plugin_version_verified_against': ht.DIRECT_IMPORT_PLUGIN_VERSION,
                'ppm_version_verified_against': '6.7.9', 'direct_wordpress_upload_ready': True,
                'direct_upload_block_reason': None, 'required_downstream_components': [],
            },
            'articles': rows,
        }

    def test_single_article_is_valid(self):
        payload = self.payload(1)
        self.assertEqual(ht.validate_handoff(payload), payload)
        self.assertEqual(content_guard.validate_batch_distinctness([payload['articles'][0]['body']])['article_count'], 1)
        self.assertEqual(batch_repetition_guard.validate_batch_repetition([payload['articles'][0]['body']])['article_count'], 1)

    def test_multiple_article_counts_are_not_hardcoded(self):
        for count in (3, 7, 25):
            with self.subTest(count=count):
                payload = self.payload(count)
                self.assertEqual(len(ht.validate_handoff(payload)['articles']), count)

    def test_mixed_and_new_article_types_are_not_hardcoded(self):
        payload = self.payload(len(self.TYPES))
        ht.validate_handoff(payload)
        self.assertEqual([row['article_type'] for row in payload['articles']], self.TYPES)

    def test_large_batch_1000_validates_and_transport_chunks(self):
        payload = self.payload(1000)
        ht.validate_handoff(payload)
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            src = td / 'src.json'
            canonical = td / ht.HANDOFF_FILENAME
            inline = td / ht.INLINE_FILENAME
            src.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
            expected = ht.canonicalize_handoff(src, canonical)
            summary = ht.inline_pack(canonical, inline)
            self.assertGreater(summary['part_count'], 1)
            out = ht.inline_unpack(inline, td / 'out')
            self.assertEqual(out.read_bytes(), expected)

    def test_zero_articles_remains_fail_closed(self):
        payload = self.payload(1)
        payload['articles'] = []
        with self.assertRaisesRegex(ht.HandoffError, 'HANDOFF_ARTICLE_COUNT_INVALID'):
            ht.validate_handoff(payload)


if __name__ == '__main__':
    unittest.main(verbosity=2)
