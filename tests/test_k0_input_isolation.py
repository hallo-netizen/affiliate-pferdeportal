import hashlib
import json
import unittest

from engine.k0_input_isolation import validate, Blocked

def stable(x):
    return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def context(source_url='https://example.org/fresh-source'):
    fact_pack = {
        'contract': 'canonical_fact_pack_v1',
        'status': 'SOURCE_VERIFIED_PRODUCTION_READY',
        'sources': [{'source_title': 'Fresh', 'source_url': source_url}],
        'claims': ['Fresh claim'],
    }
    research_claims = {
        'F1': {
            'source_title': 'Fresh',
            'source_url': source_url,
            'statement': 'Fresh claim',
        }
    }
    return {
        'production_context': {
            'fact_pack': fact_pack,
            'production_plan_item': {},
        },
        'rule_context': {
            'research_claims': research_claims,
        },
        'research_freshness_receipt': {
            'contract':'K0_RESEARCH_FRESHNESS_GUARD_V1',
            'status':'PASS',
            'historical_fact_pack_reuse':False,
            'historical_research_packet_reuse':False,
            'fact_pack_sha256':stable(fact_pack),
            'research_claims_sha256':stable(research_claims),
        },
    }

class TestK0InputIsolation(unittest.TestCase):
    def test_fresh_external_research_passes(self):
        r = validate(context(), 'run:' + 'a'*24)
        self.assertEqual(r['status'], 'PASS')
        self.assertFalse(r['historical_article_content_allowed'])
        self.assertTrue(r['current_upload_identity_authority'])

    def test_missing_freshness_receipt_blocks(self):
        x = context()
        x.pop('research_freshness_receipt')
        with self.assertRaisesRegex(Blocked, 'RESEARCH_FRESHNESS_RECEIPT_MISSING'):
            validate(x, 'run:' + 'f'*24)

    def test_repository_source_blocks(self):
        with self.assertRaisesRegex(Blocked, 'HISTORICAL_OR_PORTAL_SOURCE_FORBIDDEN'):
            validate(context('https://raw.githubusercontent.com/hallo-netizen/affiliate-pferdeportal/main/old.json'), 'run:' + 'b'*24)

    def test_live_portal_article_as_research_blocks(self):
        with self.assertRaisesRegex(Blocked, 'HISTORICAL_OR_PORTAL_SOURCE_FORBIDDEN'):
            validate(context('https://pferde-atelier.de/alter-artikel/'), 'run:' + 'c'*24)

    def test_historical_repo_path_reference_blocks(self):
        x = context()
        x['note'] = 'recovery/current16-input/old.md'
        with self.assertRaisesRegex(Blocked, 'HISTORY_REFERENCE_FORBIDDEN'):
            validate(x, 'run:' + 'd'*24)

    def test_claim_must_belong_to_current_fact_pack(self):
        x = context()
        x['rule_context']['research_claims']['F1']['source_url'] = 'https://other.example/fact'
        with self.assertRaisesRegex(Blocked, 'CLAIM_SOURCE_NOT_IN_FRESH_FACT_PACK'):
            validate(x, 'run:' + 'e'*24)

if __name__ == '__main__':
    unittest.main()
