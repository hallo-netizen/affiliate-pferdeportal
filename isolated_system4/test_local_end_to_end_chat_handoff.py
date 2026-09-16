import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import batch_gate
import codex_entry
import controller
import handoff_transport
import production_checks

ROOT = Path(__file__).resolve().parent
SNAPSHOT = ROOT / 'live_fixture' / 'wordpress_snapshot.json'
PROOF = ROOT / 'FIRST_FULL_RULE_TEST_ARTICLE_PROOF.json'


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def write_json(path: Path, value: dict) -> Path:
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True), encoding='utf-8')
    return path


def stage_payloads(index: int):
    source_id = f'src-e2e-{index}'
    e1 = f'Gesicherter konkreter Beleg A für End-to-End-Artikel {index} mit eindeutiger fachlicher Aussage.'
    e2 = f'Gesicherter konkreter Beleg B für End-to-End-Artikel {index} mit einer zweiten fachlichen Aussage.'
    evidence = e1 + '\n' + e2 + '\n' + f'Zusätzlicher Quellenkontext für den gebundenen End-to-End-Testartikel {index}.'
    source = {
        'source_id': source_id,
        'source_title': f'Fachquelle End-to-End {index}',
        'source_url': f'https://example.org/e2e-source-{index}',
        'retrieved_at': '2026-09-13T06:00:00Z',
        'snapshot_sha256': sha_text(evidence),
        'evidence': evidence,
    }
    claims = [
        {'fact_id': f'fact-e2e-{index}-a', 'source_id': source_id, 'statement': f'Konkrete Aussage A für End-to-End-Artikel {index}.', 'evidence_text': e1, 'evidence_text_sha256': sha_text(e1)},
        {'fact_id': f'fact-e2e-{index}-b', 'source_id': source_id, 'statement': f'Konkrete Aussage B für End-to-End-Artikel {index}.', 'evidence_text': e2, 'evidence_text_sha256': sha_text(e2)},
    ]
    research = {'contract': 'SYSTEM4_RESEARCH_EVIDENCE_V1', 'sources': [dict(source)]}
    facts = {'contract': 'SYSTEM4_FACTS_EVIDENCE_V1', 'claims': claims}
    fact_pack = {'contract': 'canonical_fact_pack_v1', 'status': 'SOURCE_VERIFIED_PRODUCTION_READY', 'sources': [dict(source)], 'claims': claims}
    return research, facts, fact_pack


def article_body(item: dict, index: int) -> str:
    unique = ' '.join(f'eigenstaendig{index}_{n}' for n in range(90))
    return (
        '<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung">'
        f'<section data-block="intro"><p data-fact-ids="fact-e2e-{index}-a fact-e2e-{index}-b">{item["target_keyword"]} {unique}</p></section>'
        f'<section data-block="criteria"><h2>Prüfkriterien {index}</h2><p data-fact-id="fact-e2e-{index}-a">Konkrete Prüfung {index}.</p>'
        '<table class="system-129-table comparison-table"><tr><th>Kriterium</th><th>Prüfung</th></tr>'
        f'<tr><td>Artikel {index}</td><td>Gebundener Wert {index}</td></tr></table></section>'
        f'<section data-block="conclusion"><h2>Fazit {index}</h2><p data-fact-id="fact-e2e-{index}-b">Gebundene Schlussfolgerung {index}.</p></section>'
        '</article>'
    )


def production_pass(draft: str) -> dict:
    draft_sha = sha_text(draft)
    return {
        'contract': 'SYSTEM4_FULL_PRODUCTION_CHECK_V1',
        'status': 'PASS',
        'checked_draft_sha256': draft_sha,
        'publish_allowed': False,
        'evidence': {
            'no_legacy': {'status': 'PASS', 'legacy_import_count': 0},
            'no_external_links': {'status': 'PASS', 'external_link_count': 0},
            'languagetool': {'status': 'PASS', 'engine': 'LanguageTool 6.8 / Bestand 43', 'finding_count': 0},
            'ppm679': {
                'status': 'PASS',
                'ppm_version': '6.7.9',
                'technical_status': 'TECHNICAL_CHECK_OK',
                'content_quality_status': 'CONTENT_QUALITY_CHECK_OK',
                'fail_closed_aggregate_status': 'PASS',
                'content_sha256': draft_sha,
                'language_evidence_source': 'REAL_LT68_FULLCHECK_REUSED',
            },
        },
    }


def handoff_from_states(states: list[dict]) -> dict:
    rows = []
    for index, state in enumerate(states):
        body = state['draft_markdown']
        prod = state['checks']['production_evidence']['evidence']
        rows.append({
            'index': index,
            'title': state['article']['title'],
            'target_keyword': state['article']['target_keyword'],
            'category': state['article']['category'],
            'article_type': state['article']['article_type'],
            'plan_slot': state['article']['plan_slot'],
            'final_draft_sha256': state['draft_sha256'],
            'revision_count': state['revision'],
            'body': body,
            'production_context': {
                'fact_pack': state['production_context']['fact_pack'],
                'production_plan_item': state['production_context']['production_plan_item'],
            },
            'languagetool': prod['languagetool'],
            'ppm679': prod['ppm679'],
        })
    return {
        'contract': handoff_transport.HANDOFF_CONTRACT,
        'batch_sha256': states[0]['batch_sha256'],
        'publish_allowed': False,
        'signing_deferred': True,
        'batch_gate_status': 'SYSTEM4_BATCH_FULL_PASS_COLLECTED',
        'no_legacy_status': 'PASS',
        'test_suite_status': 'PASS',
        'wordpress_review': handoff_transport.wordpress_review(),
        'articles': rows,
    }


class LocalEndToEndChatHandoffTests(unittest.TestCase):
    def test_authoritative_textmachine_bindings_are_unchanged_from_proven_full_rule_pass(self):
        proof = json.loads(PROOF.read_text(encoding='utf-8'))
        self.assertEqual(production_checks.PPM_VERSION, proof['authoritative_tool_bindings']['ppm']['version'])
        self.assertEqual(production_checks.PPM_PACKAGE_SHA256, proof['authoritative_tool_bindings']['ppm']['package_sha256'])
        self.assertEqual(production_checks.LT_ENGINE, proof['authoritative_tool_bindings']['languagetool']['engine'])
        self.assertEqual(production_checks.LT_JAR_SHA256, proof['authoritative_tool_bindings']['languagetool']['commandline_jar_sha256'])
        ppm_path = ROOT.parent / production_checks.PPM_PACKAGE_REL
        self.assertTrue(ppm_path.is_file())
        self.assertEqual(production_checks.file_sha256(ppm_path), production_checks.PPM_PACKAGE_SHA256)

    def test_positive_from_codex_entry_to_exact_parent_chat_json(self):
        snapshot = json.loads(SNAPSHOT.read_text(encoding='utf-8'))
        items = snapshot['next_textmachine_metadata_batch']['items']
        with tempfile.TemporaryDirectory(prefix='system4-local-e2e-') as td:
            root = Path(td)
            state_paths = []
            expected_bodies = []

            first_workspace = root / 'item-0'
            controller.cmd_ingress(SNAPSHOT, first_workspace, 0)

            with mock.patch.object(controller.production_checks, 'validate_bound_context', return_value=None), mock.patch.object(controller.authoring_contract, 'build', return_value={'contract':'SYSTEM4_LOCAL_HANDOFF_TEST_AUTHORING_V1'}), mock.patch.object(controller.authoring_contract, 'validate_bound', return_value={'contract':'SYSTEM4_LOCAL_HANDOFF_TEST_AUTHORING_V1'}), mock.patch.object(controller.authoring_contract, 'validate_candidate', return_value=None), mock.patch.object(
                controller.production_checks,
                'run_all',
                side_effect=lambda repo, state, fact_pack, plan: production_pass(state['draft_markdown']),
            ):
                for index, item in enumerate(items):
                    workspace = root / f'item-{index}'
                    if index:
                        controller.cmd_ingress(SNAPSHOT, workspace, index)
                    research, facts, pack = stage_payloads(index)
                    body = article_body(item, index)
                    plan = {
                        'contract': 'SYSTEM4_LOCAL_E2E_PLAN_V1',
                        'article_type': item['article_type'],
                        'topic': item['title'],
                        'target_keyword': item['target_keyword'],
                        'canonical_article': {'body_html': body},
                    }
                    controller.cmd_research(workspace, write_json(root / f'research-{index}.json', research))
                    controller.cmd_facts(workspace, write_json(root / f'facts-{index}.json', facts))
                    controller.cmd_context(workspace, write_json(root / f'pack-{index}.json', pack), write_json(root / f'plan-{index}.json', plan))
                    draft_path = root / f'article-{index}.html'; draft_path.write_text(body, encoding='utf-8')
                    controller.cmd_draft(workspace, draft_path)
                    self.assertEqual(controller.cmd_fullcheck(workspace), 0)
                    state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
                    self.assertEqual(state['phase'], 'OUTPUT_GATE_REQUIRED')
                    self.assertEqual(state['draft_markdown'], body)
                    self.assertEqual(state['draft_sha256'], sha_text(body))
                    self.assertFalse(state['publish_allowed'])
                    state_paths.append(workspace / 'state.json')
                    expected_bodies.append(body)

            batch_out = root / 'batch'
            with mock.patch.object(batch_gate.authoring_contract, 'validate_bound', return_value={'contract':'SYSTEM4_LOCAL_HANDOFF_TEST_AUTHORING_V1'}):
                collected = batch_gate.collect_batch(SNAPSHOT, state_paths, batch_out)
            self.assertEqual(collected['status'], 'SYSTEM4_BATCH_FULL_PASS_COLLECTED')
            self.assertEqual(collected['article_count'], 7)
            batch_evidence = json.loads((batch_out / 'system4_batch_evidence.json').read_text(encoding='utf-8'))
            self.assertFalse(batch_evidence['content_mutation_performed'])
            self.assertFalse(batch_evidence['design_mutation_performed'])
            self.assertEqual([row['content_utf8'] for row in batch_evidence['articles']], expected_bodies)

            states = [json.loads(path.read_text(encoding='utf-8')) for path in state_paths]
            payload = handoff_from_states(states)
            source = root / 'handoff-source.json'; write_json(source, payload)
            canonical = root / handoff_transport.HANDOFF_FILENAME
            canonical_bytes = handoff_transport.canonicalize_handoff(source, canonical)
            inline = root / handoff_transport.INLINE_FILENAME
            envelope = handoff_transport.inline_pack(canonical, inline)
            reconstructed = handoff_transport.inline_unpack(inline, root / 'parent-chat')

            self.assertEqual(reconstructed.read_bytes(), canonical_bytes)
            self.assertEqual(envelope['plaintext_sha256'], hashlib.sha256(canonical_bytes).hexdigest())
            final_payload = json.loads(reconstructed.read_text(encoding='utf-8'))
            self.assertFalse(final_payload['publish_allowed'])
            self.assertFalse(final_payload['wordpress_review']['direct_wordpress_upload_ready'])
            self.assertEqual(final_payload['wordpress_review']['intended_next_step'], 'WORDPRESS_PREIMPORT_REVIEW')
            self.assertEqual(final_payload['wordpress_review']['direct_upload_block_reason'], handoff_transport.WORDPRESS_DIRECT_BLOCK_REASON)
            self.assertEqual([row['body'] for row in final_payload['articles']], expected_bodies)
            self.assertEqual([row['final_draft_sha256'] for row in final_payload['articles']], [sha_text(body) for body in expected_bodies])

    def test_negative_fake_fact_is_blocked_before_article_stage(self):
        with tempfile.TemporaryDirectory(prefix='system4-local-neg-fact-') as td:
            root = Path(td); workspace = root / 'item'
            controller.cmd_ingress(SNAPSHOT, workspace, 0)
            research, facts, _ = stage_payloads(0)
            controller.cmd_research(workspace, write_json(root / 'research.json', research))
            invented = 'Dieser frei erfundene Beleg steht nicht im gebundenen Quellenausschnitt.'
            facts['claims'][0]['evidence_text'] = invented
            facts['claims'][0]['evidence_text_sha256'] = sha_text(invented)
            with self.assertRaisesRegex(controller.Fail, 'FACTS_EVIDENCE_FAIL:FACT_EVIDENCE_NOT_IN_SOURCE:0'):
                controller.cmd_facts(workspace, write_json(root / 'facts.json', facts))
            state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
            self.assertEqual(state['phase'], 'FACT_CHECK_REQUIRED')
            self.assertIsNone(state['facts'])

    def test_negative_design_drift_is_blocked_before_fullcheck(self):
        with tempfile.TemporaryDirectory(prefix='system4-local-neg-design-') as td:
            root = Path(td); workspace = root / 'item'
            snapshot = json.loads(SNAPSHOT.read_text(encoding='utf-8')); item = snapshot['next_textmachine_metadata_batch']['items'][0]
            controller.cmd_ingress(SNAPSHOT, workspace, 0)
            research, facts, pack = stage_payloads(0); body = article_body(item, 0)
            plan = {'contract': 'SYSTEM4_LOCAL_E2E_PLAN_V1', 'canonical_article': {'body_html': body}}
            controller.cmd_research(workspace, write_json(root / 'research.json', research)); controller.cmd_facts(workspace, write_json(root / 'facts.json', facts))
            with mock.patch.object(controller.production_checks, 'validate_bound_context', return_value=None), mock.patch.object(controller.authoring_contract, 'build', return_value={'contract':'SYSTEM4_LOCAL_HANDOFF_TEST_AUTHORING_V1'}):
                controller.cmd_context(workspace, write_json(root / 'pack.json', pack), write_json(root / 'plan.json', plan))
            bad = body.replace('system-129-table comparison-table', 'comparison-table')
            bad_path = root / 'bad.html'; bad_path.write_text(bad, encoding='utf-8')
            with mock.patch.object(controller.authoring_contract, 'validate_bound', return_value={'contract':'SYSTEM4_LOCAL_HANDOFF_TEST_AUTHORING_V1'}), mock.patch.object(controller.authoring_contract, 'validate_candidate', return_value=None), self.assertRaisesRegex(controller.Fail, 'ARTICLE_DESIGN_GUARD_FAIL:DESIGN_TABLE_SYSTEM129_CLASS_MISSING'):
                controller.cmd_draft(workspace, bad_path)
            state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
            self.assertEqual(state['phase'], 'DRAFT_REQUIRED')
            self.assertIsNone(state['draft_markdown'])

    def test_negative_historical_cross_article_template_is_blocked_at_final_handoff(self):
        rows = []
        for index in range(7):
            _, _, pack = stage_payloads(index)
            common = (
                '<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung">'
                f'<h2>Auswahl {index}</h2><p data-fact-ids="fact-e2e-{index}-a fact-e2e-{index}-b">'
                'Eine gute Entscheidung beginnt mit einer Bestandsaufnahme. Notiere wie häufig die Lösung gebraucht wird und welche Bedingungen bestehen. '
                'Eine gute Entscheidung beginnt mit einer Bestandsaufnahme. Notiere wie häufig die Lösung gebraucht wird und welche Bedingungen bestehen. '
                f'Artikel {index}</p><table class="system-129-table comparison-table"><tr><th>A</th><th>B</th></tr><tr><td>X</td><td>Y</td></tr></table></article>'
            )
            body_sha = sha_text(common)
            rows.append({
                'index': index, 'title': f'Titel {index}', 'target_keyword': f'Keyword {index}', 'category': f'cat-{index}', 'article_type': 'Beratung',
                'plan_slot': hashlib.sha256(f'slot-{index}'.encode()).hexdigest(), 'final_draft_sha256': body_sha, 'revision_count': 1, 'body': common,
                'production_context': {'fact_pack': pack, 'production_plan_item': {'contract': 'SYSTEM4_LOCAL_E2E_PLAN_V1'}},
                'languagetool': {'status': 'PASS', 'finding_count': 0, 'engine': 'LanguageTool 6.8 / Bestand 43'},
                'ppm679': {'status': 'PASS', 'ppm_version': '6.7.9', 'technical_status': 'TECHNICAL_CHECK_OK', 'content_quality_status': 'CONTENT_QUALITY_CHECK_OK', 'fail_closed_aggregate_status': 'PASS', 'content_sha256': body_sha},
            })
        payload = {
            'contract': handoff_transport.HANDOFF_CONTRACT, 'batch_sha256': hashlib.sha256(b'batch').hexdigest(), 'publish_allowed': False, 'signing_deferred': True,
            'batch_gate_status': 'SYSTEM4_BATCH_FULL_PASS_COLLECTED', 'no_legacy_status': 'PASS', 'test_suite_status': 'PASS',
            'wordpress_review': handoff_transport.wordpress_review(),
            'articles': rows,
        }
        with self.assertRaisesRegex(handoff_transport.HandoffError, 'BATCH_TEMPLATE_REUSE_BLOCKED'):
            handoff_transport.validate_handoff(payload)


if __name__ == '__main__':
    unittest.main(verbosity=2)