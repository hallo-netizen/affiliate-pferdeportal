import hashlib
import unittest

import content_guard


def sha(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


E1 = 'Die konkrete Auswahl richtet sich nach dem tatsächlichen Einsatzzweck und der sicheren Handhabung.'
E2 = 'Materialzustand und passende Nutzung müssen vor dem Einsatz konkret geprüft werden.'
SOURCE_EVIDENCE = E1 + '\n' + E2 + '\nZusätzlicher Quellenkontext für den lokalen Nachweis.'


def good_research():
    return {
        'contract': content_guard.RESEARCH_CONTRACT,
        'sources': [{
            'source_id': 'src-official-1',
            'source_title': 'Fachquelle – konkrete Anleitung',
            'source_url': 'https://example.org/fachquelle',
            'retrieved_at': '2026-09-12T20:00:00Z',
            'snapshot_sha256': sha(SOURCE_EVIDENCE),
            'evidence': SOURCE_EVIDENCE,
        }],
    }


def good_facts():
    return {
        'contract': content_guard.FACTS_CONTRACT,
        'claims': [
            {'fact_id': 'fact-a', 'source_id': 'src-official-1', 'statement': 'Der Einsatzzweck ist ein konkretes Auswahlkriterium.', 'evidence_text': E1, 'evidence_text_sha256': sha(E1)},
            {'fact_id': 'fact-b', 'source_id': 'src-official-1', 'statement': 'Der Materialzustand ist vor der Nutzung zu prüfen.', 'evidence_text': E2, 'evidence_text_sha256': sha(E2)},
        ],
    }


def good_pack():
    research = good_research(); facts = good_facts(); source = research['sources'][0]
    return {
        'contract': 'canonical_fact_pack_v1',
        'status': 'SOURCE_VERIFIED_PRODUCTION_READY',
        'sources': [dict(source)],
        'claims': list(facts['claims']),
    }


class ContentGuardTests(unittest.TestCase):
    def test_positive_research_facts_pack_and_article(self):
        research = good_research(); facts = good_facts(); pack = good_pack()
        content_guard.validate_research_document(research)
        content_guard.validate_facts_document(facts, research)
        content_guard.validate_fact_pack(pack, research, facts)
        article = '<article><p data-fact-ids="fact-a fact-b">Konkreter Artikelinhalt mit belegten Aussagen.</p></article>'
        self.assertEqual(content_guard.validate_single_article(article, pack)['status'], 'PASS')

    def test_historical_plain_research_text_is_blocked(self):
        with self.assertRaisesRegex(content_guard.ContentGuardError, 'RESEARCH_JSON_INVALID'):
            content_guard.validate_research_document('R' * 100)

    def test_self_certified_source_hash_is_blocked(self):
        research = good_research(); research['sources'][0]['snapshot_sha256'] = '0' * 64
        with self.assertRaisesRegex(content_guard.ContentGuardError, 'RESEARCH_SOURCE_HASH_MISMATCH'):
            content_guard.validate_research_document(research)

    def test_fact_without_accepted_source_is_blocked(self):
        facts = good_facts(); facts['claims'][0]['source_id'] = 'fresh-system4-source-self-made'
        with self.assertRaisesRegex(content_guard.ContentGuardError, 'FACT_SOURCE_NOT_IN_RESEARCH'):
            content_guard.validate_facts_document(facts, good_research())

    def test_fact_text_not_present_in_captured_source_is_blocked(self):
        facts = good_facts(); invented = 'Diese erfundene Belegbehauptung steht nicht im gesicherten Quellenausschnitt.'; facts['claims'][0]['evidence_text'] = invented; facts['claims'][0]['evidence_text_sha256'] = sha(invented)
        with self.assertRaisesRegex(content_guard.ContentGuardError, 'FACT_EVIDENCE_NOT_IN_SOURCE:0'):
            content_guard.validate_facts_document(facts, good_research())

    def test_historical_bad_fact_pack_without_sources_is_blocked(self):
        bad = {'contract': 'canonical_fact_pack_v1', 'status': 'SOURCE_VERIFIED_PRODUCTION_READY', 'claims': good_facts()['claims']}
        with self.assertRaisesRegex(content_guard.ContentGuardError, 'FACT_PACK_SOURCES_MISSING'):
            content_guard.validate_fact_pack(bad)

    def test_fact_pack_source_without_captured_evidence_is_blocked(self):
        bad = good_pack(); bad['sources'][0].pop('evidence')
        with self.assertRaisesRegex(content_guard.ContentGuardError, 'FACT_PACK_SOURCE_EVIDENCE_INVALID'):
            content_guard.validate_fact_pack(bad)

    def test_unknown_article_fact_id_is_blocked(self):
        with self.assertRaisesRegex(content_guard.ContentGuardError, 'ARTICLE_UNKNOWN_FACT_ID'):
            content_guard.validate_single_article('<p data-fact-id="fact-invented">Text</p>', good_pack())

    def test_good_batch_is_distinct(self):
        bodies = [f'<article><p data-fact-id="fact-a">Thema {i} mit eigener Formulierung ' + ' '.join(f'eigen{i}_{n}' for n in range(80)) + '</p></article>' for i in range(7)]
        self.assertEqual(content_guard.validate_batch_distinctness(bodies)['status'], 'PASS')

    def test_historical_template_batch_is_blocked(self):
        common = 'Eine gute Entscheidung beginnt mit einer Bestandsaufnahme. Notiere wie häufig die Lösung gebraucht wird und welche Bedingungen bestehen. '
        bodies = [f'<article><p>{common}{common}Thema {i}.</p></article>' for i in range(7)]
        with self.assertRaisesRegex(content_guard.ContentGuardError, 'BATCH_TEMPLATE_REUSE_BLOCKED'):
            content_guard.validate_batch_distinctness(bodies)

    def test_small_repair_passes_broad_rewrite_blocks(self):
        old = '<article><p>' + ('Konkreter fachlicher Satz. ' * 30) + '</p></article>'
        new = old.replace('Konkreter fachlicher Satz.', 'Konkreter fachlicher Satz!', 1)
        self.assertEqual(content_guard.validate_repair_continuity(old, new)['status'], 'PASS')
        replacement = '<article><p>' + ('Völlig anderer Inhalt ohne Bezug. ' * 12) + '</p></article>'
        with self.assertRaisesRegex(content_guard.ContentGuardError, 'REPAIR_SCOPE_TOO_LARGE'):
            content_guard.validate_repair_continuity(old, replacement)


if __name__ == '__main__':
    unittest.main(verbosity=2)
