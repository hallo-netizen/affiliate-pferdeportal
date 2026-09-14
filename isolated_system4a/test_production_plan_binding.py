import hashlib
import json
import unittest
import zipfile

import production_plan_binding as ppb


def canonical_article():
    package=ppb.REPO/ppb.PPM_PACKAGE_REL
    with zipfile.ZipFile(package) as z:
        plan=json.loads(z.read('portal-production-machine/contracts/canonical-complete-editorial-plan-v1.json'))
    slot=[s for s in plan['slots'] if s.get('canonical_article_id')=='article:fe39320b47c1ba40194c8d69'][0]
    return {
        'title':slot['working_title'], 'target_keyword':'Checklisten für Pferdeanhänger',
        'category':slot['category_slug'], 'article_type':slot['article_type'], 'plan_slot':ppb.stable_hash(slot)
    }


class ProductionPlanBindingTests(unittest.TestCase):
    def article(self, category='checklisten-fuer-pferdeanhaenger-beratung', article_type='Beratung'):
        a=canonical_article(); a['category']=category; a['article_type']=article_type; return a
    def bare_plan(self):
        a=canonical_article()
        return {'article_type':a['article_type'],'target_keyword':a['target_keyword'],'topic':a['title'],'runtime_order':{}}
    def bind(self, article=None, plan=None):
        return ppb.bind_production_plan(article or self.article(), plan or self.bare_plan(), {'claims':[]})
    def test_positive_bare_plan_gets_supervisor_binding_from_pinned_wp_snapshot(self):
        out=self.bind(); q=out['quality_binding']
        self.assertEqual(q['contract'],'content_structure_language_binding_v2')
        self.assertEqual(out['quality_binding_hash'],ppb.stable_hash(q))
        self.assertEqual(q['wordpress_category']['id'],1049)
        self.assertEqual([x['role'] for x in q['link_bindings']],['parent_category','semantic_related','further_information'])
        self.assertEqual([x['section_id'] for x in q['link_bindings']],['criteria','decision','further_information'])
        self.assertEqual([x['href'] for x in q['link_bindings']],[
            '/transport/transport-anhaengerpflege/checklisten-fuer-pferdeanhaenger/',
            '/transport/transport-anhaengerpflege/', '/transport/'
        ])
        ppb.validate_link_bindings_against_wp_snapshot(q)
    def test_negative_prebound_quality_is_forbidden(self):
        plan=self.bare_plan(); plan['quality_binding']={}
        with self.assertRaisesRegex(ppb.ProductionPlanBindingError,'PRODUCTION_PLAN_PREBOUND_FIELD_FORBIDDEN'): self.bind(plan=plan)
    def test_negative_prebound_runtime_links_are_forbidden(self):
        plan=self.bare_plan(); plan['runtime_order']={'links':[{'role':'x'}]}
        with self.assertRaisesRegex(ppb.ProductionPlanBindingError,'PRODUCTION_PLAN_PREBOUND_RUNTIME_LINKS_FORBIDDEN'): self.bind(plan=plan)
    def test_negative_noncanonical_category_blocks(self):
        with self.assertRaisesRegex(ppb.ProductionPlanBindingError,'PPM679_CATEGORY_NOT_UNIQUE'): self.bind(article=self.article(category='pferdeanhaenger-beratung'))
    def test_negative_wrong_link_binding_is_rejected_against_pinned_wp_snapshot(self):
        q=self.bind()['quality_binding']; q=json.loads(json.dumps(q)); q['link_bindings'][0]['href']='/wrong/'
        with self.assertRaisesRegex(ppb.ProductionPlanBindingError,'^PORTAL_LINK_BINDING_SOURCE_MISMATCH:parent_category$'):
            ppb.validate_link_bindings_against_wp_snapshot(q)
    def test_positive_fact_pack_terms_are_bound_before_draft(self):
        fp={'claims':[{'display_label':'Stützlast','subject_scope':'support_load_selection'}]}
        out=ppb.bind_production_plan(self.article(),self.bare_plan(),fp); terms=[x.lower() for x in out['quality_binding']['intent_terms']]
        self.assertIn('stützlast',terms); self.assertIn('support load selection',terms)

if __name__=='__main__': unittest.main(verbosity=2)
