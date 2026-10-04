import json
import tempfile
import unittest
from pathlib import Path

from engine.k0_research_freshness_guard import verify, Blocked

def ctx(source, statement):
    return {
        'production_context': {
            'fact_pack': {
                'contract':'canonical_fact_pack_v1',
                'sources':[{'source_title':'S','source_url':source}],
                'claims':[statement],
            }
        },
        'rule_context': {
            'research_claims': {
                'F1': {'source_title':'S','source_url':source,'statement':statement}
            }
        }
    }

class TestK0ResearchFreshnessGuard(unittest.TestCase):
    def test_new_packet_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            old=root/'real_runs/k0/old/AUTHORING_CONTEXT.json'
            new=root/'real_runs/k0/new/AUTHORING_CONTEXT.json'
            old.parent.mkdir(parents=True); new.parent.mkdir(parents=True)
            old.write_text(json.dumps(ctx('https://example.org/old','alte aussage')),encoding='utf-8')
            new.write_text(json.dumps(ctx('https://example.org/new','neue aussage')),encoding='utf-8')
            r=verify('real_runs/k0/new/AUTHORING_CONTEXT.json',root)
            self.assertEqual(r['status'],'PASS')

    def test_exact_old_fact_pack_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            old=root/'real_runs/k0/old/AUTHORING_CONTEXT.json'
            new=root/'real_runs/k0/new/AUTHORING_CONTEXT.json'
            old.parent.mkdir(parents=True); new.parent.mkdir(parents=True)
            x=ctx('https://example.org/same','gleiche aussage')
            old.write_text(json.dumps(x),encoding='utf-8')
            y=ctx('https://example.org/same','gleiche aussage')
            y['rule_context']['research_claims']['F1']['extra']='new'
            new.write_text(json.dumps(y),encoding='utf-8')
            with self.assertRaisesRegex(Blocked,'HISTORICAL_FACT_PACK_REUSE_BLOCKED'):
                verify('real_runs/k0/new/AUTHORING_CONTEXT.json',root)

    def test_exact_old_research_claims_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            old=root/'real_runs/k0/old/AUTHORING_CONTEXT.json'
            new=root/'real_runs/k0/new/AUTHORING_CONTEXT.json'
            old.parent.mkdir(parents=True); new.parent.mkdir(parents=True)
            x=ctx('https://example.org/same','gleiche aussage')
            old.write_text(json.dumps(x),encoding='utf-8')
            y=ctx('https://example.org/same','gleiche aussage')
            y['production_context']['fact_pack']['claims'].append('zusatz')
            new.write_text(json.dumps(y),encoding='utf-8')
            with self.assertRaisesRegex(Blocked,'HISTORICAL_RESEARCH_PACKET_REUSE_BLOCKED'):
                verify('real_runs/k0/new/AUTHORING_CONTEXT.json',root)

if __name__ == '__main__':
    unittest.main()
