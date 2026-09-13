import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from external_host import ExternalHostError, ExternalSupervisorHost
from managed_agent_worker import ManagedAgentWorkerPool
from test_full_chain_local import Checks, snapshot


def sh(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def request_from_prompt(prompt: str) -> dict:
    marker = 'Gebundener Arbeitsauftrag: '
    if marker not in prompt:
        raise RuntimeError('PROMPT_BINDING_MISSING')
    return json.loads(prompt.split(marker, 1)[1])


def content_for(req: dict) -> str:
    article = req['article']
    idx = article['title'].split()[-1]
    task = req['task']
    e1 = f'Gesicherter konkreter Beleg A für Artikel {idx} mit eindeutiger fachlicher Aussage und sicherer Nutzung.'
    e2 = f'Gesicherter konkreter Beleg B für Artikel {idx} mit einer zweiten fachlichen Aussage zur Auswahl.'
    evidence = e1 + '\n' + e2 + '\n' + f'Zusätzlicher gesicherter Quellenkontext für Artikel {idx}.'
    sid = f'src-{idx}'
    source = {
        'source_id': sid,
        'source_title': f'Fachquelle {idx}',
        'source_url': f'https://example.org/source-{idx}',
        'retrieved_at': '2026-09-13T08:00:00Z',
        'snapshot_sha256': sh(evidence),
        'evidence': evidence,
    }
    claims = [
        {'fact_id': f'f-{idx}-a', 'source_id': sid, 'statement': f'Konkrete erste Aussage für Artikel {idx}.', 'evidence_text': e1, 'evidence_text_sha256': sh(e1)},
        {'fact_id': f'f-{idx}-b', 'source_id': sid, 'statement': f'Konkrete zweite Aussage für Artikel {idx}.', 'evidence_text': e2, 'evidence_text_sha256': sh(e2)},
    ]
    if task == 'research':
        return json.dumps({'contract': 'SYSTEM4_RESEARCH_EVIDENCE_V1', 'sources': [source]}, ensure_ascii=False, sort_keys=True)
    if task == 'facts':
        return json.dumps({'contract': 'SYSTEM4_FACTS_EVIDENCE_V1', 'claims': claims}, ensure_ascii=False, sort_keys=True)
    if task == 'context':
        pack = {'contract': 'canonical_fact_pack_v1', 'status': 'SOURCE_VERIFIED_PRODUCTION_READY', 'sources': [source], 'claims': claims}
        plan = {'article_type': article['article_type'], 'topic': article['title'], 'target_keyword': article['target_keyword'], 'category_binding': {'slug': article['category']}}
        return json.dumps({'fact_pack': pack, 'production_plan_item': plan}, ensure_ascii=False, sort_keys=True)
    repaired = ' und nach Prüfbefund gezielt korrigiert' if task == 'repair' else ''
    unique = ' '.join(f'eigen{idx}_{n}' for n in range(90))
    return (
        f'<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung">'
        f'<section data-block="criteria"><h2>{article["title"]}</h2>'
        f'<p data-fact-ids="f-{idx}-a f-{idx}-b">Inhalt {idx}{repaired} {unique} mit eindeutiger fachlicher Struktur.</p>'
        f'<table class="system-129-table comparison-table"><tr><th>Kriterium</th><th>Prüfung</th></tr>'
        f'<tr><td>{idx}</td><td>Gebundener Wert {idx}</td></tr></table></section></article>'
    )


class FakeManagedTransport:
    def __init__(self, isolated: bool = True):
        self.isolated = isolated
        self.created = []
        self.deleted = []
        self.initial_prompt = {}
        self.counter = 0

    def authority_isolated(self):
        return self.isolated

    def create_session(self, *, input_text: str, plan_slot: str) -> str:
        self.counter += 1
        sid = f'managed-{self.counter}'
        self.created.append((sid, plan_slot))
        self.initial_prompt[sid] = input_text
        return sid

    def run_turn(self, session_id: str, *, input_text: str) -> str:
        prompt = self.initial_prompt[session_id] if input_text == '__READ_INITIAL_OUTPUT__' else input_text
        return content_for(request_from_prompt(prompt))

    def delete_session(self, session_id: str) -> None:
        self.deleted.append(session_id)


class ManagedExternalHostTests(unittest.TestCase):
    def test_positive_managed_agent_full_chain_to_parent_chat_with_repair(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            snap = root / 'snapshot.json'
            out = root / 'SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json'
            parent = root / 'parent-chat'
            snapshot(snap, 2)
            transport = FakeManagedTransport()
            pool = ManagedAgentWorkerPool(transport)
            host = ExternalSupervisorHost(mode='test', checks=Checks(fail_first=True))
            result = host.run_architecture(snap, pool, out, parent)
            self.assertEqual(result['status'], 'SYSTEM4A_EXTERNAL_HOST_ARCHITECTURE_PASS')
            self.assertEqual(result['worker_boundary'], 'MANAGED_AGENT_WORKER')
            self.assertEqual(result['article_count'], 2)
            self.assertEqual(result['runtime_pids'], [])
            self.assertEqual(result['runtime_limit'], 0)
            self.assertEqual(len(result['worker_sessions']), 2)
            payload = json.loads(out.read_text(encoding='utf-8'))
            self.assertTrue(all(row['revision_count'] == 2 for row in payload['articles']))
            rebuilt = parent / 'SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json'
            self.assertEqual(rebuilt.read_bytes(), out.read_bytes())
            self.assertCountEqual(transport.deleted, ['managed-1', 'managed-2'])

    def test_negative_managed_authority_loss_blocks_before_worker_use(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            snap = root / 'snapshot.json'
            snapshot(snap, 1)
            transport = FakeManagedTransport()
            pool = ManagedAgentWorkerPool(transport)
            transport.isolated = False
            host = ExternalSupervisorHost(mode='test', checks=Checks())
            with self.assertRaisesRegex(ExternalHostError, 'MANAGED_AGENT_AUTHORITY_BOUNDARY_INVALID'):
                host.run_architecture(snap, pool, root / 'out.json', root / 'parent')
            self.assertEqual(transport.created, [])
            pool.close()

    def test_positive_production_boundary_accepts_managed_agent_before_authority_root_gate(self):
        transport = FakeManagedTransport()
        pool = ManagedAgentWorkerPool(transport)
        host = ExternalSupervisorHost(mode='production')
        with self.assertRaisesRegex(ExternalHostError, 'HOST_AUTHORITY_ROOT_REQUIRED'):
            host.run_production(Path('not-opened.json'), pool, Path('out.json'), Path('parent'))
        self.assertEqual(transport.created, [])
        pool.close()

    def test_negative_unknown_worker_type_is_rejected(self):
        host = ExternalSupervisorHost(mode='test', checks=Checks())
        with self.assertRaisesRegex(ExternalHostError, 'EXTERNAL_WORKER_POOL_REQUIRED'):
            host.run_architecture(Path('x.json'), object(), Path('out.json'), Path('parent'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
