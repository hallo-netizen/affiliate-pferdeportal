import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import batch_gate
import design_guard
import test_batch_gate


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


class UniversalBatchGateTests(unittest.TestCase):
    TYPES = ['Beratung', 'Produktvergleich', 'Pferderasse', 'Glossar Begriff']

    def evidence(self, i: int):
        source_id = f'src-{i}'
        e1 = f'Erster konkreter Beleg für Artikel {i} mit fachlicher Aussage und eindeutiger Bindung.'
        e2 = f'Zweiter konkreter Beleg für Artikel {i} mit einer davon verschiedenen fachlichen Aussage.'
        e3 = f'Dritter konkreter Beleg für Artikel {i} bestätigt einen weiteren eigenständigen fachlichen Prüfpunkt.'
        evidence = e1 + '\n' + e2 + '\n' + e3 + '\n' + f'Zusätzlicher gesicherter Quellenkontext für Artikel {i}.'
        source = {'source_id': source_id, 'source_title': f'Fachquelle {i}', 'source_url': f'https://example.org/source-{i}', 'retrieved_at': '2026-09-13T08:00:00Z', 'snapshot_sha256': sha_text(evidence), 'evidence': evidence}
        claims = [
            {'fact_id': f'fact-{i}-a', 'source_id': source_id, 'statement': f'Konkrete erste Aussage für Artikel {i}.', 'evidence_text': e1, 'evidence_text_sha256': sha_text(e1)},
            {'fact_id': f'fact-{i}-b', 'source_id': source_id, 'statement': f'Konkrete zweite Aussage für Artikel {i}.', 'evidence_text': e2, 'evidence_text_sha256': sha_text(e2)},
            {'fact_id': f'fact-{i}-c', 'source_id': source_id, 'statement': f'Konkrete dritte Aussage für Artikel {i}.', 'evidence_text': e3, 'evidence_text_sha256': sha_text(e3)},
        ]
        research = {'contract': 'SYSTEM4_RESEARCH_EVIDENCE_V1', 'sources': [dict(source)]}
        facts = {'contract': 'SYSTEM4_FACTS_EVIDENCE_V1', 'claims': claims}
        pack = {'contract': 'canonical_fact_pack_v1', 'status': 'SOURCE_VERIFIED_PRODUCTION_READY', 'sources': [dict(source)], 'claims': [dict(row) for row in claims]}
        return research, facts, pack

    def production_evidence(self, draft: str):
        d = sha_text(draft)
        return {
            'contract': 'SYSTEM4_FULL_PRODUCTION_CHECK_V1', 'status': 'PASS', 'checked_draft_sha256': d, 'publish_allowed': False,
            'evidence': {
                'no_legacy': {'status': 'PASS', 'legacy_import_count': 0},
                'no_external_links': {'status': 'PASS', 'external_link_count': 0},
                'languagetool': {'status': 'PASS', 'engine': 'LanguageTool 6.8 / Bestand 43', 'finding_count': 0},
                'ppm679': {'status': 'PASS', 'ppm_version': '6.7.9', 'technical_status': 'TECHNICAL_CHECK_OK', 'content_quality_status': 'CONTENT_QUALITY_CHECK_OK', 'fail_closed_aggregate_status': 'PASS', 'content_sha256': d, 'language_evidence_source': 'REAL_LT68_CURRENT_DRAFT_REFRESHED'},
            },
        }

    def make_fixture(self, root: Path, count: int):
        items = []
        for i in range(count):
            article_type = self.TYPES[i % len(self.TYPES)]
            items.append({'title': f'Titel {i}', 'target_keyword': f'Keyword {i}', 'category': f'kategorie-{i}', 'article_type': article_type, 'plan_slot': sha_text(f'slot-{i}')})
        batch_sha = sha_text(f'batch-{count}')
        snapshot = {'contract': 'SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1', 'next_textmachine_metadata_batch': {'contract': 'PSERC_TEXTMACHINE_METADATA_BATCH_V2', 'status': 'READY_FOR_TEXTMACHINE_METADATA_INTAKE', 'batch_sha256': batch_sha, 'item_count': count, 'items': items, 'publish_allowed': False}}
        snap = root / 'snapshot.json'
        snap.write_text(json.dumps(snapshot, ensure_ascii=False), encoding='utf-8')
        snap_sha = hashlib.sha256(snap.read_bytes()).hexdigest()
        bound_snapshot = {'contract': 'SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1', 'next_textmachine_metadata_batch': snapshot['next_textmachine_metadata_batch'], 'system4_root_manifest_sha256': '1' * 64}
        bound_raw = json.dumps(bound_snapshot, ensure_ascii=False).encode('utf-8')
        bound_sha = hashlib.sha256(bound_raw).hexdigest()
        if bound_sha == snap_sha:
            raise AssertionError('FIXTURE_MUST_MODEL_DISTINCT_RUNTIME_AND_BOUND_SNAPSHOT_HASHES')
        paths = []
        for i, item in enumerate(items):
            article_type = item['article_type']
            type_class = design_guard.article_type_class(article_type)
            unique = ' '.join(f'eigen{i}_{n}' for n in range(40))
            draft = f'<article class="ppm-generated {type_class}" data-article-type="{article_type}"><h2>{item["title"]}</h2><p data-fact-ids="fact-{i}-a fact-{i}-b fact-{i}-c">{item["target_keyword"]} {unique}</p><table class="system-129-table comparison-table"><tr><th>Kriterium</th><th>Wert</th></tr><tr><td>{i}</td><td>{i}</td></tr></table></article>'
            research, facts, pack = self.evidence(i)
            plan = {'canonical_article': {'body_html': draft}}
            context_core = {'fact_pack': pack, 'production_plan_item': plan}
            research_text = json.dumps(research, ensure_ascii=False, sort_keys=True)
            facts_text = json.dumps(facts, ensure_ascii=False, sort_keys=True)
            state = {
                'contract': batch_gate.STATE_CONTRACT,
                'source_snapshot_sha256': bound_sha,
                'batch_sha256': batch_sha,
                'article': item,
                'immutable_core_sha256': '',
                'publish_allowed': False,
                'phase': 'OUTPUT_GATE_REQUIRED',
                'revision': 1,
                'research': {'text': research_text, 'sha256': sha_text(research_text)},
                'facts': {'text': facts_text, 'sha256': sha_text(facts_text)},
                'production_context': {'fact_pack': pack, 'production_plan_item': plan, 'sha256': batch_gate.stable_hash(context_core)},
                'draft_markdown': draft,
                'draft_sha256': sha_text(draft),
                'checks': {'status': 'PASS', 'mode': 'FULL_PRODUCTION', 'errors': [], 'checked_draft_sha256': sha_text(draft), 'production_evidence': self.production_evidence(draft)},
                'last_error': None,
                'release_prepared': None,
                'released': False,
            }
            test_batch_gate.bind_authoring_contract(state)
            state['immutable_core_sha256'] = batch_gate.stable_hash(batch_gate.immutable_core(state))
            workspace = root / f'item-{i:06d}'
            workspace.mkdir()
            (workspace / 'bound_snapshot.json').write_bytes(bound_raw)
            path = workspace / 'state.json'
            path.write_text(json.dumps(state, ensure_ascii=False), encoding='utf-8')
            paths.append(path)
        return snap, paths

    def test_batch_gate_accepts_one_and_mixed_sizes(self):
        for count in (1, 3, 25):
            with self.subTest(count=count), tempfile.TemporaryDirectory() as td:
                root = Path(td)
                snap, states = self.make_fixture(root, count)
                result = batch_gate.collect_batch(snap, states, root / 'out')
                self.assertEqual(result['article_count'], count)
                self.assertEqual(result['status'], 'SYSTEM4_BATCH_FULL_PASS_COLLECTED')


if __name__ == '__main__':
    unittest.main(verbosity=2)
