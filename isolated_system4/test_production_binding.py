import copy
import hashlib
import json
import unittest
from pathlib import Path

import production_binding
import production_checks

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SNAPSHOT = REPO / production_binding.PORTAL_STRUCTURE_REL

CASES = [
    (
        {
            'title': 'Das Wichtigste über Hindernisstangen für Pferde',
            'target_keyword': 'Hindernisstangen für Pferde',
            'category': 'hindernisstangen-beratung',
            'article_type': 'Beratung',
            'plan_slot': '9c229b0e6a784a482575e3deb16d105e3b5355becbbbb8ecfc8e1f600b529c56',
        },
        ['/training/', '/training/training-reitplatz-training/', '/training/training-reitplatz-training/hindernisstangen/'],
    ),
    (
        {
            'title': 'Eine richtige Reitplatzbeleuchtung ohne Mast finden',
            'target_keyword': 'Reitplatzbeleuchtung ohne Mast',
            'category': 'reitplatzbeleuchtung-beratung',
            'article_type': 'Beratung',
            'plan_slot': '6ce9a1e47446daf84e85f08e84c33ada214f92612a654d79e68df18ea4e9fa19',
        },
        ['/weide/', '/weide/weide-reitplatz/', '/weide/weide-reitplatz/reitplatzbeleuchtung/'],
    ),
    (
        {
            'title': 'Mistcontainer mit Deckel wählen',
            'target_keyword': 'Mistcontainer mit Deckel',
            'category': 'mistcontainer-beratung',
            'article_type': 'Beratung',
            'plan_slot': '7b0e8f8b0653eb3a40aee2a68f4b9909df9d8bda374db0ec8c49e7b53ecbee87',
        },
        ['/stall/', '/stall/stall-mist-und-entsorgung/', '/stall/stall-mist-und-entsorgung/mistcontainer/'],
    ),
]


def inputs(article):
    state = {'article': copy.deepcopy(article)}
    facts = {'contract': 'canonical_fact_pack_v1', 'claims': []}
    plan = {
        'article_type': article['article_type'],
        'target_keyword': article['target_keyword'],
        'topic': article['title'],
        'runtime_order': {
            'order_id': 'machine-test-order',
            'article_type': article['article_type'],
            'title': article['title'],
            'slug': 'machine-test',
            'subject_scope': 'machine_test',
            'subject_label': article['target_keyword'],
            'lead': 'Gebundener Testwert.',
            'conclusion': 'Gebundener Testwert.',
            'allowed_fact_ids': [],
        },
    }
    return state, facts, plan


class ProductionBindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.snapshot = SNAPSHOT.read_bytes()
        cls.snapshot_sha = hashlib.sha256(cls.snapshot).hexdigest()

    def test_three_real_metadata_positions_bind_exact_portal_hierarchy(self):
        for article, expected_hrefs in CASES:
            with self.subTest(category=article['category']):
                state, facts, plan = inputs(article)
                bound = production_binding.bind_plan_from_snapshot(state, facts, plan, self.snapshot)
                quality = bound['quality_binding']
                links = quality['link_bindings']
                self.assertEqual([row['role'] for row in links], ['parent_category', 'semantic_related', 'further_information'])
                self.assertEqual([row['href'] for row in links], expected_hrefs)
                self.assertEqual([row['section_id'] for row in links], ['criteria', 'decision', 'further_information'])
                self.assertEqual(bound['runtime_order']['links'], links)
                self.assertEqual(quality['wordpress_category']['slug'], article['category'])
                self.assertEqual(quality['wordpress_category']['category_source_snapshot_hash'], self.snapshot_sha)
                self.assertEqual(quality['portal_link_registry']['snapshot_source_sha256'], self.snapshot_sha)
                self.assertEqual(quality['portal_link_registry_hash'], production_checks.stable_hash(quality['portal_link_registry']))
                self.assertEqual(bound['quality_binding_hash'], production_checks.stable_hash(quality))
                self.assertRegex(quality['internal_test_marker'], r'^LT[0-9A-Z-]{6,}$')

    def test_wrong_category_blocks(self):
        article = copy.deepcopy(CASES[0][0]); article['category'] = 'does-not-exist-beratung'
        state, facts, plan = inputs(article)
        with self.assertRaisesRegex(production_binding.ProductionBindingError, 'PORTAL_CATEGORY_NOT_UNIQUE'):
            production_binding.bind_plan_from_snapshot(state, facts, plan, self.snapshot)

    def test_wrong_article_type_blocks(self):
        article = copy.deepcopy(CASES[0][0]); article['article_type'] = 'FAQ'
        state, facts, plan = inputs(article)
        with self.assertRaisesRegex(production_binding.ProductionBindingError, 'PORTAL_CATEGORY_ARTICLE_TYPE_MISMATCH'):
            production_binding.bind_plan_from_snapshot(state, facts, plan, self.snapshot)

    def test_external_quality_binding_blocks(self):
        article = copy.deepcopy(CASES[0][0]); state, facts, plan = inputs(article)
        plan['quality_binding'] = {'contract': 'content_structure_language_binding_v2'}
        with self.assertRaisesRegex(production_binding.ProductionBindingError, 'EXTERNAL_QUALITY_BINDING_FORBIDDEN'):
            production_binding.bind_plan_from_snapshot(state, facts, plan, self.snapshot)

    def test_external_runtime_links_block(self):
        article = copy.deepcopy(CASES[0][0]); state, facts, plan = inputs(article)
        plan['runtime_order']['links'] = [{'role': 'parent_category', 'href': '/fake/'}]
        with self.assertRaisesRegex(production_binding.ProductionBindingError, 'EXTERNAL_RUNTIME_LINK_BINDING_FORBIDDEN'):
            production_binding.bind_plan_from_snapshot(state, facts, plan, self.snapshot)

    def test_tampered_snapshot_cannot_silently_keep_same_binding_hash(self):
        article = copy.deepcopy(CASES[0][0]); state, facts, plan = inputs(article)
        original = production_binding.bind_plan_from_snapshot(state, facts, plan, self.snapshot)
        altered_value = json.loads(self.snapshot.decode('utf-8'))
        altered_value['_system4_negative_test'] = 'changed-byte-authority'
        altered = json.dumps(altered_value, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        rebound = production_binding.bind_plan_from_snapshot(state, facts, plan, altered)
        self.assertNotEqual(
            original['quality_binding']['wordpress_category']['category_source_snapshot_hash'],
            rebound['quality_binding']['wordpress_category']['category_source_snapshot_hash'],
        )
        self.assertNotEqual(original['quality_binding_hash'], rebound['quality_binding_hash'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
