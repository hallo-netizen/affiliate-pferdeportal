import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONTROLLER = HERE / 'controller.py'
CODEX_ENTRY = HERE / 'codex_entry.py'


def h(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


class ContextRequiredRegressionTests(unittest.TestCase):
    def test_facts_cannot_open_draft_directly(self):
        with tempfile.TemporaryDirectory(prefix='system4-context-required-') as td:
            td = Path(td)
            snapshot = td / 'snapshot.json'
            workspace = td / 'workspace'
            evidence = (
                'Diese reale Testquelle enthält genügend gebundenen Belegtext für zwei '
                'unterschiedliche, nachvollziehbare Aussagen im System-4-Test.'
            )
            snapshot.write_text(json.dumps({
                'next_textmachine_metadata_batch': {
                    'contract': 'PSERC_TEXTMACHINE_METADATA_BATCH_V2',
                    'status': 'READY_FOR_TEXTMACHINE_METADATA_INTAKE',
                    'publish_allowed': False,
                    'batch_sha256': h('context-required-batch'),
                    'item_count': 1,
                    'items': [{
                        'title': 'Kontext muss vor Draft gebunden sein',
                        'target_keyword': 'Kontextbindung',
                        'category': 'test-beratung',
                        'article_type': 'Beratung',
                        'plan_slot': h('context-required-slot'),
                    }],
                }
            }, ensure_ascii=False), encoding='utf-8')
            research = td / 'research.json'
            research.write_text(json.dumps({
                'contract': 'SYSTEM4_RESEARCH_EVIDENCE_V1',
                'sources': [{
                    'source_id': 'src-1',
                    'source_title': 'Reale Testquelle Kontextbindung',
                    'source_url': 'https://example.org/system4/contextbindung',
                    'retrieved_at': '2026-09-13T16:00:00Z',
                    'snapshot_sha256': h(evidence),
                    'evidence': evidence,
                }],
            }, ensure_ascii=False), encoding='utf-8')
            ev1 = 'Diese reale Testquelle enthält genügend gebundenen Belegtext'
            ev2 = 'für zwei unterschiedliche, nachvollziehbare Aussagen im System-4-Test.'
            facts = td / 'facts.json'
            facts.write_text(json.dumps({
                'contract': 'SYSTEM4_FACTS_EVIDENCE_V1',
                'claims': [
                    {'fact_id': 'fact-1', 'source_id': 'src-1', 'statement': 'Der Kontext muss vor dem Schreiben verbindlich gebunden sein.', 'evidence_text': ev1, 'evidence_text_sha256': h(ev1)},
                    {'fact_id': 'fact-2', 'source_id': 'src-1', 'statement': 'Eine spätere bekannte Pflicht darf nicht erst im Fullcheck auftauchen.', 'evidence_text': ev2, 'evidence_text_sha256': h(ev2)},
                ],
            }, ensure_ascii=False), encoding='utf-8')
            draft = td / 'draft.html'; draft.write_text('<article>nicht zulässig vor Context</article>', encoding='utf-8')

            for argv in (
                [sys.executable, str(CONTROLLER), 'ingress', str(snapshot), str(workspace)],
                [sys.executable, str(CONTROLLER), 'research', str(workspace), str(research)],
                [sys.executable, str(CONTROLLER), 'facts', str(workspace), str(facts)],
            ):
                cp = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                self.assertEqual(cp.returncode, 0, cp.stdout.decode() + cp.stderr.decode())

            state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
            self.assertEqual(state['phase'], 'CONTEXT_REQUIRED')
            self.assertIsNone(state['production_context'])
            self.assertIsNone(state['authoring_contract'])

            blocked = subprocess.run(
                [sys.executable, str(CONTROLLER), 'draft', str(workspace), str(draft)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(blocked.returncode, 2)
            self.assertIn('PHASE_FAIL:DRAFT', blocked.stdout.decode())
            state_after = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
            self.assertEqual(state_after['phase'], 'CONTEXT_REQUIRED')
            self.assertEqual(state_after['revision'], 0)

            entry = subprocess.run(
                [sys.executable, str(CODEX_ENTRY), 'next', str(workspace)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(entry.returncode, 0, entry.stdout.decode() + entry.stderr.decode())
            self.assertIn('SYSTEM4_CODEX_ENTRY_PASS:CONTEXT_REQUIRED', entry.stdout.decode())


if __name__ == '__main__':
    unittest.main(verbosity=2)
