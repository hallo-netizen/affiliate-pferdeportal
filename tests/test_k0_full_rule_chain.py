import copy,re,unittest

from engine.k0_full_rules import (
    Blocked, RULE_CONTEXT_CONTRACT, writer_rule_bundle, rule_binding,
    verify_pre_lt68, verify_final,
)
from tests.test_k10 import make_base


def package_from_article(a):
    identity={
      'article_type':a['article_type'],
      'category':a['wordpress_category']['slug'],
      'plan_slot':'a'*64,
      'target_keyword':a['target_keyword'],
      'title':a['title'],
    }
    rc={
      'contract':RULE_CONTEXT_CONTRACT,
      'type_meta':copy.deepcopy(a['type_meta']),
      'research_claims':copy.deepcopy(a['research_claims']),
      'required_fact_ids':copy.deepcopy(a['required_fact_ids']),
      'allowed_fact_ids':copy.deepcopy(a['allowed_fact_ids']),
      'bound_links':copy.deepcopy(a['bound_links']),
      'link_registry':copy.deepcopy(a['link_registry']),
      'runtime_link_roles':copy.deepcopy(a['runtime_link_roles']),
      'wordpress_category':{'id':0,'slug':identity['category'],'taxonomy':'category','id_source':'WORDPRESS_REST_RESOLVE_AT_RUNTIME'},
      'heading_intent_terms':copy.deepcopy(a['heading_intent_terms']),
      'comparison_source_bindings':copy.deepcopy(a['comparison_source_bindings']),
      'table_decision':copy.deepcopy(a['table_decision']),
      'semantic_rule_results':copy.deepcopy(a.get('semantic_rule_results') or {}),
      'table_multiword_exceptions':copy.deepcopy(a.get('table_multiword_exceptions') or []),
    }
    bundle=writer_rule_bundle(identity['article_type'])
    return {
      'contract':'K0_ARTICLE_PACKAGE_V1',
      'identity':identity,
      'html':a['html'],
      'rule_context':rc,
      'writer_rule_binding':rule_binding(bundle),
      'publish_allowed':False,
    }, [{'id':12,'slug':identity['category']}]


def with_valid_table(a):
    a=copy.deepcopy(a)
    # Make room in the global word budget while keeping normal sections comfortably above minimum.
    for block in ('answer','details','checklist'):
        pat=re.compile(r'(?is)(<section data-block="'+block+r'">.*?)(</section>)')
        m=pat.search(a['html'])
        body=m.group(1)
        ps=list(re.finditer(r'(?is)<p\b[^>]*>.*?</p>',body))
        if ps:
            q=ps[-1]
            body=body[:q.start()]+body[q.end():]
            a['html']=a['html'][:m.start()]+body+m.group(2)+a['html'][m.end():]
    h=a['research_claims']['F2']['evidence_text_sha256']
    tr=f'<span class="ppm-source-trace" data-fact-id="F2" data-source-hash="{h}" data-source-title="Fachquelle F2"></span>'
    table=f'''<section data-block="table"><h2>Aufgabe und Einsatz direkt vergleichen</h2>
<table class="system-129-table comparison-table"><thead><tr><th>Hilfsmittel</th><th>Zweck</th><th>Praxis</th></tr></thead><tbody>
<tr><td data-fact-ids="F2">Longierpeitsche</td><td data-fact-ids="F2">Hilfe</td><td data-fact-ids="F2">Training</td></tr>
<tr><td data-fact-ids="F3">Stimme</td><td data-fact-ids="F3">Hilfen</td><td data-fact-ids="F3">Zusammenspiel</td></tr>
<tr><td data-fact-ids="F3">Longe</td><td data-fact-ids="F3">Zusammenspiel</td><td data-fact-ids="F3">Stimme</td></tr>
<tr><td data-fact-ids="F4">Abstand</td><td data-fact-ids="F4">Sicherheit</td><td data-fact-ids="F4">Kontrolle</td></tr>
</tbody></table>
<p data-fact-ids="F2">{tr} Die Tabelle verbindet Aufgabe, Hilfe und sicheren Einsatz, damit die wichtigsten Unterschiede beim Longieren direkt erkennbar bleiben.</p></section>'''
    a['html']=a['html'].replace('<section data-block="conclusion">',table+'<section data-block="conclusion">')
    a['table_decision']={'decision':'INCLUDE_ADDED_VALUE','exception_code':None,'rationale':'Die Tabelle verbindet Hilfsmittel mit eigenständigen Auswahl- und Kontrollpunkten.'}
    a['semantic_rule_results']={'table.value_required_if_present':'PASS'}
    return a


class K0FullRuleChainTests(unittest.TestCase):
    def test_writer_bundle_contains_all_article_hard_rules(self):
        b=writer_rule_bundle('FAQ')
        self.assertEqual(b['contract'],'K0_FULL_RULE_BUNDLE_V1')
        self.assertEqual(b['article_hard_rule_count'],85)
        self.assertIn('links.visible_exact',b['article_hard_rule_ids'])
        self.assertIn('structure.required_lists',b['article_hard_rule_ids'])
        self.assertIn('table.post_summary_policy',b['article_hard_rule_ids'])

    def test_positive_full_rule_chain_passes(self):
        p,cat=package_from_article(make_base())
        pre=verify_pre_lt68(p,cat)
        self.assertEqual(pre['status'],'READY_FOR_LT68',pre)
        final=verify_final(p,cat,{'status':'PASS','finding_count':0})
        self.assertEqual(final['status'],'PASS',final)
        self.assertEqual(final['article_hard_rule_count'],85)

    def test_missing_internal_links_blocks(self):
        a=make_base()
        a['html']=re.sub(r'(?is)<a\b[^>]*>(.*?)</a>',r'\1',a['html'])
        p,cat=package_from_article(a)
        with self.assertRaisesRegex(Blocked,'links.visible_exact'):
            verify_pre_lt68(p,cat)

    def test_missing_required_list_blocks(self):
        a=make_base()
        a['html']=re.sub(r'(?is)<ul\b[^>]*data-list="key_answers"[^>]*>.*?</ul>','',a['html'])
        p,cat=package_from_article(a)
        with self.assertRaisesRegex(Blocked,'structure.required_lists'):
            verify_pre_lt68(p,cat)

    def test_table_with_summary_passes_and_without_summary_blocks(self):
        a=with_valid_table(make_base())
        p,cat=package_from_article(a)
        pre=verify_pre_lt68(p,cat)
        self.assertEqual(pre['status'],'READY_FOR_LT68',pre)
        bad=copy.deepcopy(a)
        bad['html']=re.sub(r'(?is)(</table>)\s*<p\b[^>]*>.*?</p>',r'\1',bad['html'],count=1)
        p2,cat2=package_from_article(bad)
        with self.assertRaisesRegex(Blocked,'table.post_summary_policy'):
            verify_pre_lt68(p2,cat2)


if __name__=='__main__':
    unittest.main()
