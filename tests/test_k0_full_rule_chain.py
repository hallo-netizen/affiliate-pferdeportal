import copy,re,unittest

from engine.k0_full_rules import (
    Blocked, RULE_CONTEXT_CONTRACT, writer_rule_bundle, rule_binding,
    verify_pre_lt68, verify_final, validate_rule_context, verify_live_link_targets,
)
from tests.test_k10 import make_base
from engine.checkers import structural_receipts


def package_from_article(a):
    identity={
      'article_type':a['article_type'],
      'category':a['wordpress_category']['slug'],
      'plan_slot':'a'*64,
      'target_keyword':a['target_keyword'],
      'title':a['title'],
    }
    claims=copy.deepcopy(a['research_claims'])
    for idx,(fid,row) in enumerate(claims.items(),1):
        row.setdefault('source_url',f'https://example.test/source-{idx}')
    rc={
      'contract':RULE_CONTEXT_CONTRACT,
      'type_meta':copy.deepcopy(a['type_meta']),
      'research_claims':claims,
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
    # Make room in the global word budget without reducing the paragraph floor.
    short={
      'answer':'<p data-fact-ids="F2">Aufgabe und Longierpeitsche bleiben beim Longieren als Hilfe im Training klar.</p>',
      'details':'<p data-fact-ids="F3">Stimme und Longe bleiben beim Longieren im Zusammenspiel klar verständlich.</p>',
      'checklist':'<p data-fact-ids="F4">Sicherer Einsatz braucht beim Longieren Kontrolle und ausreichenden Abstand zum Pferd.</p>',
    }
    for block in ('answer','details','checklist'):
        pat=re.compile(r'(?is)(<section data-block="'+block+r'">.*?)(</section>)')
        m=pat.search(a['html'])
        body=m.group(1)
        ps=list(re.finditer(r'(?is)<p\b[^>]*>.*?</p>',body))
        if ps:
            q=ps[-1]
            body=body[:q.start()]+short[block]+body[q.end():]
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


class K0LinkRegressionTests(unittest.TestCase):
    def test_one_parent_link_without_further_information_is_blocked(self):
        a=make_base()
        retained=a['bound_links'][0]
        for item in a['bound_links'][1:]:
            m=re.search(r'(?is)<a\b[^>]*data-link-role="'+re.escape(item['role'])+r'"[^>]*>(.*?)</a>',a['html'])
            self.assertIsNotNone(m)
            a['html']=a['html'][:m.start()]+m.group(1)+a['html'][m.end():]
        a['bound_links']=[retained]
        a['link_registry']=[x for x in a['link_registry'] if x['href']==retained['href']]
        a['runtime_link_roles']=['parent_category']
        p,_=package_from_article(a)
        with self.assertRaisesRegex(Blocked,'K0_RULE_CONTEXT_LINK_COUNT_INVALID'):
            validate_rule_context(p['rule_context'],p['identity'])
        receipts={x['rule_id']:x for x in structural_receipts(a)}
        self.assertEqual(receipts['links.visible_exact']['status'],'FAIL')
        self.assertEqual(receipts['links.required_roles']['status'],'FAIL')
        self.assertEqual(receipts['links.further_information_position']['status'],'FAIL')

    def test_parent_and_further_link_without_semantic_related_is_valid(self):
        a=make_base()
        removed=a['bound_links'][1]
        m=re.search(r'(?is)<a\b[^>]*data-link-role="'+re.escape(removed['role'])+r'"[^>]*>(.*?)</a>',a['html'])
        self.assertIsNotNone(m)
        a['html']=a['html'][:m.start()]+m.group(1)+a['html'][m.end():]
        a['bound_links']=[a['bound_links'][0],a['bound_links'][2]]
        a['link_registry']=[x for x in a['link_registry'] if x['href']!=removed['href']]
        a['runtime_link_roles']=['parent_category','further_information']
        p,_=package_from_article(a)
        out=validate_rule_context(p['rule_context'],p['identity'])
        self.assertEqual(len(out['bound_links']),2)
        receipts={x['rule_id']:x for x in structural_receipts(a)}
        for name in ('links.visible_exact','links.required_roles','links.runtime_roles_bound',
                     'links.further_information_position','links.bound_pairs_exact'):
            self.assertEqual(receipts[name]['status'],'PASS',name)

    def test_good_links_still_pass_existing_rule_context(self):
        p,_=package_from_article(make_base())
        out=validate_rule_context(p['rule_context'],p['identity'])
        self.assertEqual(out['bound_links'],p['rule_context']['bound_links'])
        self.assertEqual(out['link_registry'],p['rule_context']['link_registry'])

    def test_uninformative_prepared_link_is_blocked(self):
        p,_=package_from_article(make_base())
        p['rule_context']['bound_links'][1]['anchor']='Weitere Informationen zum Thema'
        with self.assertRaisesRegex(Blocked,'K0_RULE_CONTEXT_LINK_ANCHOR_UNINFORMATIVE'):
            validate_rule_context(p['rule_context'],p['identity'])

    def test_category_slug_used_as_faq_anchor_is_blocked(self):
        p,_=package_from_article(make_base())
        p['rule_context']['bound_links'][0]['anchor']='FAQ zu training'
        with self.assertRaisesRegex(Blocked,'K0_RULE_CONTEXT_LINK_ANCHOR_UNINFORMATIVE'):
            validate_rule_context(p['rule_context'],p['identity'])

    def test_not_explicitly_active_cannot_be_self_certified(self):
        p,_=package_from_article(make_base())
        p['rule_context']['link_registry'][1]['active']=None
        with self.assertRaisesRegex(Blocked,'K0_RULE_CONTEXT_LINK_REGISTRY_INACTIVE'):
            validate_rule_context(p['rule_context'],p['identity'])

    def test_live_target_positive_with_category_and_published_page(self):
        p,_=package_from_article(make_base())
        links=p['rule_context']['bound_links']
        links[0]['href']='/category/zuegel-faq/'
        links[1]['href']='/category/zuegel-beratung/'
        links[2]['href']='/wissen/lenken/'
        calls=[]
        def wordpress(url):
            calls.append(url)
            slug=url.rsplit('=',1)[-1]
            if '/categories?' in url:
                return [] if slug=='lenken' else [{'slug':slug,'name':'Kategorie '+slug,'count':2,'link':'https://example.org/category/'+slug+'/'}]
            if '/pages?' in url:
                return [{'slug':'lenken','status':'publish','link':'https://example.org/wissen/lenken/','title':{'rendered':'Lenken'}}]
            raise AssertionError('Unexpected API lookup: '+url)
        report=verify_live_link_targets(p['rule_context'],'https://example.org',wordpress,lambda url:'<html><body>Seite</body></html>')
        self.assertEqual(report['status'],'PASS')
        self.assertEqual(report['checked'],3)
        self.assertEqual([x['official_name'] for x in report['canonical_links']],['Kategorie zuegel-faq','Kategorie zuegel-beratung','Lenken'])
        self.assertEqual([x['target_type'] for x in report['canonical_links']],['C_CATEGORY','C_CATEGORY','C_PAGE'])
        self.assertEqual(len(calls),4)

    def test_published_post_never_allowed_as_link_target(self):
        p,_=package_from_article(make_base())
        p['rule_context']['bound_links']=[
            {'role':'parent_category','href':'/category/zuegel-faq/','block':'details'},
            {'role':'semantic_related','href':'/category/zuegel-beratung/','block':'checklist'},
            {'role':'further_information','href':'/artikel/lenken/','block':'further_information'},
        ]
        calls=[]
        def wordpress(url):
            calls.append(url)
            slug=url.rsplit('=',1)[-1]
            if '/categories?' in url:
                return [] if slug=='lenken' else [{'slug':slug,'name':'Kategorie '+slug,'count':2,'link':'https://example.org/category/'+slug+'/'}]
            if '/pages?' in url:
                return []
            if '/posts?' in url:
                raise AssertionError('Article lookup must not happen')
            return []
        with self.assertRaisesRegex(Blocked,'K0_LINK_TARGET_NOT_C_CATEGORY_OR_PUBLISHED_PAGE'):
            verify_live_link_targets(p['rule_context'],'https://example.org',wordpress,lambda url:'<html></html>')
        self.assertFalse(any('/posts?' in call for call in calls))

    def test_draft_or_wrong_path_page_rejected(self):
        p,_=package_from_article(make_base())
        p['rule_context']['bound_links'][0]['href']='/category/zuegel-faq/'
        p['rule_context']['bound_links'][1]['href']='/category/zuegel-beratung/'
        p['rule_context']['bound_links'][2]['href']='/wissen/lenken/'
        for status,link in [('draft','https://example.org/wissen/lenken/'),('publish','https://example.org/artikel/lenken/')]:
            def wordpress(url):
                slug=url.rsplit('=',1)[-1]
                if '/categories?' in url:
                    return [] if slug=='lenken' else [{'slug':slug,'name':'Kategorie '+slug,'count':2,'link':'https://example.org/category/'+slug+'/'}]
                if '/pages?' in url:
                    return [{'slug':'lenken','status':status,'link':link,'title':{'rendered':'Lenken'}}]
                raise AssertionError(url)
            with self.assertRaisesRegex(Blocked,'K0_LINK_TARGET_NOT_C_CATEGORY_OR_PUBLISHED_PAGE'):
                verify_live_link_targets(p['rule_context'],'https://example.org',wordpress,lambda url:'<html></html>')

    def _topic_link_category_lookup(self, url):
        from urllib.parse import unquote
        slug=unquote(url.rsplit('=',1)[-1])
        names={
            'pferdegesundheit-verstehen':'Pferdegesundheit verstehen',
            'pferdewissen-grundlagen':'Pferdewissen & Grundlagen',
            'gesundheit-regeneration-kuehlgamaschen-faq':'FAQ Kühlgamaschen',
            'hautpilz-pferd':'Hautpilz beim Pferd',
            'pilzinfektionen-pferd':'Pilzinfektionen beim Pferd',
            'parasiten-beim-pferd':'Parasiten beim Pferd',
            'pfriemenschwanz-eier':'Pfriemenschwanz-Eier erkennen',
        }
        if slug not in names:
            return []
        return [{'slug':slug,'name':names[slug],'count':3,
                 'link':'https://example.org/category/'+slug+'/'}]

    def _topic_link_context(self, related, further, statement):
        return {'bound_links':[
            {'role':'parent_category','href':'/category/pferdegesundheit-verstehen/','block':'details'},
            {'role':'semantic_related','href':'/category/'+related+'/','block':'research'},
            {'role':'further_information','href':'/category/'+further+'/','block':'further_information'},
            ],'research_claims':{'F1':{'statement':statement}},'heading_intent_terms':[]}

    def test_real_lebermoos_unrelated_link_targets_block_before_writer(self):
        # Both real wrong links from the 18.11.2026 2-article handoff.
        subject={'title':'Hilft Lebermoos tatsächlich gegen Pilzprobleme beim Pferd?',
                 'target_keyword':'lebermoos pferd pilz'}
        ctx=self._topic_link_context(
            'pferdewissen-grundlagen','gesundheit-regeneration-kuehlgamaschen-faq',
            'Lebermoos wirkt im Labor gegen Pilze, aber Hautpilz ist am Pferd nicht bewiesen.')
        filtered=verify_live_link_targets(ctx,'https://example.org',
                                     self._topic_link_category_lookup,topic=subject)
        self.assertEqual(filtered['checked'],1)
        self.assertEqual(len(filtered['omitted_links']),2)
        ctx['bound_links'][1]['href']='/category/hautpilz-pferd/'
        filtered=verify_live_link_targets(ctx,'https://example.org',
                                     self._topic_link_category_lookup,topic=subject)
        self.assertEqual(filtered['checked'],2)
        self.assertEqual(filtered['omitted_links'][0]['role'],'further_information')
        ctx['bound_links'][2]['href']='/category/pilzinfektionen-pferd/'
        result=verify_live_link_targets(ctx,'https://example.org',
                                        self._topic_link_category_lookup,topic=subject)
        self.assertEqual(result['checked'],3)
        self.assertEqual(result['canonical_links'][1]['official_name'],'Hautpilz beim Pferd')

    def test_real_pfriemenschwanz_unrelated_link_targets_block_before_writer(self):
        subject={'title':'Pfriemenschwanz-Eier beim Pferd erkennen und einen Befall abklären',
                 'target_keyword':'pfriemenschwanz pferd eier'}
        ctx=self._topic_link_context(
            'pferdewissen-grundlagen','gesundheit-regeneration-kuehlgamaschen-faq',
            'Pfriemenschwanz ist ein Parasit, der Eier am After ablegt.')
        filtered=verify_live_link_targets(ctx,'https://example.org',
                                     self._topic_link_category_lookup,topic=subject)
        self.assertEqual(filtered['checked'],1)
        ctx['bound_links'][1]['href']='/category/parasiten-beim-pferd/'
        filtered=verify_live_link_targets(ctx,'https://example.org',
                                     self._topic_link_category_lookup,topic=subject)
        self.assertEqual(filtered['checked'],2)
        ctx['bound_links'][2]['href']='/category/pfriemenschwanz-eier/'
        result=verify_live_link_targets(ctx,'https://example.org',
                                        self._topic_link_category_lookup,topic=subject)
        self.assertEqual([x['role'] for x in result['canonical_links']],
                         ['parent_category','semantic_related','further_information'])

    def test_actual_page_content_can_match_when_page_title_is_broad(self):
        topic={'title':'Aufbau und Funktion der Eierstöcke bei der Stute',
               'target_keyword':'eierstöcke pferd'}
        ctx={'bound_links':[
            {'role':'parent_category','href':'/category/pferdewissen-grundlagen/'},
            {'role':'semantic_related','href':'/wissen/gesundheitsvorsorge-grundlagen/'},
            {'role':'further_information','href':'/wissen/fortpflanzung/'},
        ],'heading_intent_terms':['Eierstöcke','Follikel','Fortpflanzung'],
        'research_claims':{'F1':{'statement':'Die Eierstöcke der Stute enthalten Follikel.'}}}
        def wordpress(url):
            from urllib.parse import unquote
            slug=unquote(url.rsplit('=',1)[-1])
            if '/categories?' in url:
                if slug=='pferdewissen-grundlagen':
                    return [{'slug':slug,'name':'Pferdewissen & Grundlagen',
                             'count':2,'link':'https://example.org/category/'+slug+'/'}]
                return []
            if '/pages?' in url:
                content={'gesundheitsvorsorge-grundlagen':'Bei der Stute zeigen Follikel und Fortpflanzung gesundheitliche Veränderungen.',
                         'fortpflanzung':'Der Eisprung der Stute folgt auf die Entwicklung der Follikel.'}
                return [{'slug':slug,'status':'publish',
                         'link':'https://example.org/wissen/'+slug+'/',
                         'title':{'rendered':('Gesundheitsvorsorge Grundlagen' if slug=='gesundheitsvorsorge-grundlagen' else 'Fortpflanzung')},
                         'content':{'rendered':content[slug]}}]
            raise AssertionError('Only categories and pages allowed: '+url)
        out=verify_live_link_targets(ctx,'https://example.org',
                                     wordpress,lambda url:'<html><body>Seite</body></html>',topic=topic)
        self.assertEqual(out['status'],'PASS')
        self.assertEqual([r['target_type'] for r in out['canonical_links']],
                         ['C_CATEGORY','C_PAGE','C_PAGE'])

    def test_generic_word_only_page_is_not_a_topic_match(self):
        topic={'title':'Eierstöcke bei der Stute','target_keyword':'eierstöcke pferd'}
        ctx={'bound_links':[
            {'role':'parent_category','href':'/category/pferdewissen-grundlagen/'},
            {'role':'semantic_related','href':'/wissen/gesundheitsvorsorge-grundlagen/'}
        ],'heading_intent_terms':['Eierstöcke','Fortpflanzung'],
        'research_claims':{'F1':{'statement':'Eierstöcke sind Organe der Stute.'}}}
        def wordpress(url):
            if '/categories?' in url:
                return [{'slug':'pferdewissen-grundlagen','name':'Pferdewissen & Grundlagen','count':0,
                         'link':'https://example.org/category/pferdewissen-grundlagen/'}] if 'pferdewissen-grundlagen' in url else []
            if '/pages?' in url:
                return [{'slug':'gesundheitsvorsorge-grundlagen','status':'publish',
                         'link':'https://example.org/wissen/gesundheitsvorsorge-grundlagen/',
                         'title':{'rendered':'Gesundheitsvorsorge Grundlagen'},
                         'content':{'rendered':'Hier geht es um allgemeine Grundlagen und Pferdewissen.'}}]
            raise AssertionError(url)
        filtered=verify_live_link_targets(ctx,'https://example.org',wordpress,
                                     lambda url:'<html></html>',topic=topic)
        self.assertEqual(filtered['checked'],1)
        self.assertEqual(filtered['omitted_links'][0]['reason'],'NO_MEANINGFUL_TOPIC_MATCH')

    def test_category_description_binds_topic_without_exact_title_words(self):
        topic={'title':'Pfriemenschwanz-Eier beim Pferd erkennen',
               'target_keyword':'pfriemenschwanz pferd eier'}
        ctx={'bound_links':[{'role':'parent_category','href':'/category/pferdewissen-grundlagen/'},
                            {'role':'semantic_related','href':'/category/parasitenkunde/'}],
             'heading_intent_terms':['Pfriemenschwanz','Parasiten'],
             'research_claims':{'F1':{'statement':'Pfriemenschwanz ist ein Parasit, der Eier am After ablegt.'}}}
        def wordpress(url):
            if '/categories?' in url:
                slug=url.rsplit('=',1)[-1]
                if slug=='pferdewissen-grundlagen':
                    return [{'slug':slug,'count':0,'name':'Pferdewissen & Grundlagen',
                             'link':'https://example.org/category/'+slug+'/'}]
                return [{'slug':'parasitenkunde','count':2,'name':'Parasitenkunde',
                         'link':'https://example.org/category/parasitenkunde/',
                         'description':'Pfriemenschwanz: Eier und Parasiten beim Pferd.'}]
            raise AssertionError('No page/post query expected')
        out=verify_live_link_targets(ctx,'https://example.org',wordpress,topic=topic)
        self.assertEqual(out['status'],'PASS')
        self.assertEqual(out['canonical_links'][0]['target_type'],'C_CATEGORY')

    def test_live_target_missing_category_blocks_before_writer(self):
        p,_=package_from_article(make_base())
        p['rule_context']['bound_links'][0]['href']='/category/training/'
        p['rule_context']['bound_links'][1]['href']='/category/absent/'
        p['rule_context']['bound_links'][2]['href']='/category/longierpeitschen/'
        def category_lookup(url):
            slug=url.rsplit('=',1)[-1]
            return [] if slug=='absent' else [{'slug':slug,'name':'Kategorie '+slug,'count':2}]
        with self.assertRaisesRegex(Blocked,'K0_LINK_TARGET_CATEGORY_MISSING'):
            verify_live_link_targets(p['rule_context'],'https://example.org',category_lookup,lambda url:'<html></html>')

    def test_live_target_empty_related_category_blocks_before_writer(self):
        p,_=package_from_article(make_base())
        p['rule_context']['bound_links'][0]['href']='/category/training/'
        p['rule_context']['bound_links'][1]['href']='/category/empty-beratung/'
        p['rule_context']['bound_links'][2]['href']='/category/longierpeitschen/'
        def category_lookup(url):
            slug=url.rsplit('=',1)[-1]
            return [{'slug':slug,'name':'Kategorie '+slug,'count':0 if slug=='empty-beratung' else 2}]
        with self.assertRaisesRegex(Blocked,'K0_LINK_TARGET_CATEGORY_EMPTY'):
            verify_live_link_targets(p['rule_context'],'https://example.org',category_lookup,lambda url:'<html></html>')

    def test_official_c_title_uses_existing_bound_pair_rule_only(self):
        a=make_base()
        a['link_registry'][0]['official_name']=a['bound_links'][0]['anchor']
        good={x['rule_id']:x for x in structural_receipts(a)}
        self.assertEqual(good['links.bound_pairs_exact']['status'],'PASS')
        a['link_registry'][0]['official_name']='Ein anderer offizieller C-Name'
        bad={x['rule_id']:x for x in structural_receipts(a)}
        self.assertEqual(bad['links.bound_pairs_exact']['status'],'FAIL')
        self.assertNotIn('links.canonical_name_second_gate',bad)

    def test_existing_section_placement_rejects_detached_nav_links(self):
        a=make_base()
        link='<a data-link-role="semantic_related" href="/training/longieren/">Longieren</a>'
        self.assertIn(link,a['html'])
        a['html']=a['html'].replace(link,'Longieren',1)
        section_end='</section><section data-block="checklist">'
        self.assertIn(section_end,a['html'])
        a['html']=a['html'].replace(section_end,'<nav class="ppm-related-nav">'+link+'</nav>'+section_end,1)
        receipt={x['rule_id']:x for x in structural_receipts(a)}['links.section_placement']
        self.assertEqual(receipt['status'],'FAIL')

    def test_real_approved_article_runs_writer_to_wordpress_batch(self):
        # Production artifact, not a constructed toy article. LT status comes from
        # the archived PASS result; the external LT engine is not rerun here.
        import json,hashlib
        from pathlib import Path
        from engine.k0_writer_station import verify as verify_writer
        from engine.k0_production_gate import verify as production_verify
        from engine.k0_wordpress_export import build as build_wordpress,verify_export
        from engine.wordpress_batch_export import combine
        base=Path('real_runs/k0/k0-20261026-9544ba8b-01')
        load=lambda name: json.loads((base/name).read_text(encoding='utf-8'))
        # Rebind the genuine archived article to the CURRENT approved rule bundle.
        # An old 85-rule seal must never be silently treated as an 81-rule seal.
        from engine.k0_writer_station import prepare, seal
        archived_job=load('WRITER_JOB.json')
        archived_product=load('SEALED_WRITER_PRODUCT.json')
        intake=load('WORDPRESS_INTAKE.json')
        original=load('WORDPRESS_SINGLE.json')
        ident=archived_product['identity']
        cat=[original['articles'][0]['production_context']['production_plan_item']['quality_binding']['wordpress_category']]
        portal={'contract':'K0_PORTAL_ASSIGNMENT_V1','status':'PASS','items':[{'portal_id':'pferdeatelier','status':'AUTO_DETECTED','job_identity':ident}]}
        context=load('AUTHORING_CONTEXT.json')
        context['run_instance_id']=archived_job['run_instance_id']
        job=prepare(intake,portal,context)
        # Archived source packs from 2026-10-26 may lack original-source
        # excerpts. They now return to the SAME research owner, rather than
        # being re-sealed as newly approved articles.
        if job.get('status')=='REPAIR_REQUIRED':
            self.assertEqual(job['owner'],'SAME_RESEARCH_OWNER')
            self.assertEqual(job['identity'],ident)
            self.assertTrue(job['issues'])
            return
        draft={
            'contract':'K0_WRITER_DRAFT_V1',
            'job_id':job['job_id'],
            'title':ident['title'],
            'content_html':archived_product['html'],
            'table_decision':copy.deepcopy(job['rule_context']['table_decision']),
            'lt_authoritative_terms':copy.deepcopy(archived_product['lt_authoritative_terms']),
            'revision_count':archived_product['revision_count'],
            'publish_allowed':False,
        }
        product=seal(job,draft)
        self.assertEqual(job['writer_rule_binding']['article_hard_rule_count'],81)
        self.assertEqual(product['html'],archived_product['html'])
        self.assertEqual(verify_writer(job,product)['status'],'PASS')
        self.assertEqual(verify_pre_lt68(product,cat)['status'],'READY_FOR_LT68')
        gate=production_verify(product,portal,cat)
        self.assertEqual(gate['status'],'PASS')
        lt={'status':'PASS','finding_count':0,'html_sha256':hashlib.sha256(product['html'].encode('utf-8')).hexdigest()}
        final=verify_final(product,cat,lt)
        self.assertEqual(final['status'],'PASS')
        bindings={'contract':'K10_CANONICAL_ARTICLE_BINDINGS_V1','status':'PASS','bindings':{ident['plan_slot']:original['articles'][0]['article_id']}}
        exported=build_wordpress(intake,product,portal,gate,lt,final,bindings,cat)
        self.assertEqual(verify_export(exported,intake)['status'],'PASS')
        batch=combine(intake,[exported])
        self.assertEqual(batch['article_count'],1)
        self.assertEqual(batch['articles'][0]['body'],product['html'])
        self.assertFalse(batch['publish_allowed'])

    def test_existing_section_placement_accepts_real_paragraph_links(self):
        a=make_base()
        receipt={x['rule_id']:x for x in structural_receipts(a)}['links.section_placement']
        self.assertEqual(receipt['status'],'PASS')


class K0FullRuleChainTests(unittest.TestCase):
    def test_writer_bundle_contains_all_article_hard_rules(self):
        b=writer_rule_bundle('FAQ')
        self.assertEqual(b['contract'],'K0_FULL_RULE_BUNDLE_V1')
        self.assertEqual(b['article_hard_rule_count'],81)
        self.assertIn('links.visible_exact',b['article_hard_rule_ids'])
        self.assertIn('structure.required_lists',b['article_hard_rule_ids'])
        self.assertIn('table.post_summary_policy',b['article_hard_rule_ids'])

    def test_positive_full_rule_chain_passes(self):
        p,cat=package_from_article(make_base())
        pre=verify_pre_lt68(p,cat)
        self.assertEqual(pre['status'],'READY_FOR_LT68',pre)
        final=verify_final(p,cat,{'status':'PASS','finding_count':0})
        self.assertEqual(final['status'],'PASS',final)
        self.assertEqual(final['article_hard_rule_count'],81)

    def test_title_is_not_rejudged_by_k0_after_upstream_approval(self):
        # Editorial keyword/title judgment was delegated upstream on 10 Nov.
        for title in (
            'Kann man einen Kappzaum über einer Trense tragen?',
            'Kann man eine Trense über einem Kappzaum tragen?',
        ):
            a=make_base()
            a['target_keyword']='Kappzaum über Trense'
            a['title']=title
            ids={r['rule_id'] for r in structural_receipts(a)}
            self.assertFalse({'title.keyword_required','title.colon_forbidden','type.question_mark_policy'} & ids)

    def test_h2_keyword_phrase_gate_is_delegated_but_repetition_protection_remains(self):
        from engine.checkers import run_article_checks
        ids={r['rule_id'] for r in run_article_checks(make_base())}
        self.assertNotIn('heading.target_phrase_control',ids)
        self.assertIn('heading.keyword_staccato_forbidden',ids)

    def test_missing_internal_links_blocks(self):
        a=make_base()
        a['html']=re.sub(r'(?is)<a\b[^>]*>(.*?)</a>',r'\1',a['html'])
        p,cat=package_from_article(a)
        with self.assertRaisesRegex(Blocked,'links.visible_exact'):
            verify_pre_lt68(p,cat)

    def test_parent_and_related_links_must_be_in_main_body(self):
        a=make_base()
        a['bound_links'][0]['block']='intro'
        p,cat=package_from_article(a)
        with self.assertRaisesRegex(Blocked,'K0_RULE_CONTEXT_MAIN_LINK_DISTRIBUTION_INVALID'):
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
