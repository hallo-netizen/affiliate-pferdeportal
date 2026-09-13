import unittest

import production_plan_binding as ppb


class ProductionPlanBindingTests(unittest.TestCase):
    def article(self, category='checklisten-fuer-pferdeanhaenger-beratung', article_type='Beratung'):
        return {
            'title': 'Checklisten für Pferdeanhänger auswählen die wichtigsten Entscheidungskriterien',
            'target_keyword': 'Checklisten für Pferdeanhänger',
            'category': category,
            'article_type': article_type,
            'plan_slot': 'a' * 64,
        }

    def bare_plan(self):
        return {
            'article_type': 'Beratung',
            'target_keyword': 'Checklisten für Pferdeanhänger',
            'topic': 'Checklisten für Pferdeanhänger auswählen die wichtigsten Entscheidungskriterien',
            'runtime_order': {},
        }

    def bind(self, article=None, plan=None):
        return ppb.bind_production_plan(article or self.article(), plan or self.bare_plan(), {'claims':[]})

    def test_positive_bare_plan_gets_supervisor_binding(self):
        out = self.bind()
        q = out['quality_binding']
        self.assertEqual(q['contract'], 'content_structure_language_binding_v2')
        self.assertEqual(out['quality_binding_hash'], ppb.stable_hash(q))
        self.assertEqual(q['wordpress_category']['slug'], self.article()['category'])
        self.assertTrue(q['wordpress_category']['semantic_binding_not_numeric_identity'])
        self.assertEqual([x['role'] for x in q['link_bindings']], ['parent_category','semantic_related','further_information'])
        self.assertEqual([x['section_id'] for x in q['link_bindings']], ['criteria','decision','further_information'])
        self.assertEqual([x['href'] for x in q['link_bindings']], [
            '/transport/transport-anhaengerpflege/checklisten-fuer-pferdeanhaenger/',
            '/transport/transport-anhaengerpflege/',
            '/transport/',
        ])
        self.assertEqual(out['runtime_order']['links'], q['link_bindings'])
        self.assertEqual(q['portal_link_registry']['source_snapshot_sha256'], ppb.PORTAL_AUDIT_SHA256)

    def test_negative_prebound_quality_is_forbidden(self):
        plan = self.bare_plan(); plan['quality_binding'] = {}
        with self.assertRaisesRegex(ppb.ProductionPlanBindingError, 'PRODUCTION_PLAN_PREBOUND_FIELD_FORBIDDEN'):
            self.bind(plan=plan)

    def test_negative_prebound_runtime_links_are_forbidden(self):
        plan = self.bare_plan(); plan['runtime_order'] = {'links':[{'role':'x'}]}
        with self.assertRaisesRegex(ppb.ProductionPlanBindingError, 'PRODUCTION_PLAN_PREBOUND_RUNTIME_LINKS_FORBIDDEN'):
            self.bind(plan=plan)

    def test_negative_noncanonical_category_blocks(self):
        with self.assertRaisesRegex(ppb.ProductionPlanBindingError, 'PPM679_CATEGORY_NOT_UNIQUE'):
            self.bind(article=self.article(category='pferdeanhaenger-beratung'))

    def test_positive_fact_pack_terms_are_bound_before_draft(self):
        fp={'claims':[{'display_label':'Stützlast','subject_scope':'support_load_selection'}]}
        out=ppb.bind_production_plan(self.article(),self.bare_plan(),fp)
        terms=[x.lower() for x in out['quality_binding']['intent_terms']]
        self.assertIn('stützlast',terms)
        self.assertIn('support load selection',terms)


if __name__ == '__main__': unittest.main(verbosity=2)
