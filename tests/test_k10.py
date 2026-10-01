import copy, sys, unittest, json, tempfile
from pathlib import Path
from unittest import mock
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from engine.catalog_guard import validate_catalog
from engine.checkers import run_article_checks, article_hash
from engine.final_integrity import verify_article, verify_system, verify_package, verify_package_pre_wordpress
from engine.isolation_guard import verify as isolation_verify
from engine.owner_guard import verify as owner_verify
from engine.field_coverage import audit as field_audit
from engine.system_guard import run_system_checks
from engine.package_adapters import make_package_receipts, make_pre_wordpress_package_receipts
from engine.ppm_parity_guard import verify as ppm_parity_verify
from engine.core import hard_rules
from engine.package_adapters import PACKAGE_RESULT_MAP


def words(prefix,n):
    # Unique numbered sentences avoid accidental duplicate-sentence failures.
    out=[]; i=1
    base=prefix.split()+['erklärt','den','praktischen','Zusammenhang','klar','sachlich','für','Pferde','im','Training','und','nennt','wichtige','Punkte','für','den','sicheren','Alltag']
    while len(out)<n:
        sent=base+[f'aspekt{i}']
        out.extend(sent); i+=1
    return ' '.join(out[:n])+'.'

def trace(fid,title,h):
    return f'<span class="ppm-source-trace" data-fact-id="{fid}" data-source-hash="{h}" data-source-title="{title}"></span>'

def make_base():
    import hashlib
    evidence={
      'F1':'Einleitung Training Pferde sichere Longierarbeit Quelle',
      'F2':'Aufgabe Longierpeitsche Longieren Hilfe Training Pferd',
      'F3':'Stimme Longe Zusammenspiel Longieren Hilfen Pferd',
      'F4':'Sicherer Einsatz Longieren Kontrolle Abstand Pferd',
      'F5':'Fazit Einsatz Longierpeitsche Sicherheit Training Pferd',
    }
    hashes={fid:hashlib.sha256(text.encode()).hexdigest() for fid,text in evidence.items()}
    claims={fid:{
      'source_title':f'Fachquelle {fid}','evidence_text_sha256':hashes[fid],
      'statement':text,'evidence_text':text,'claim_status':'FULLY_SUPPORTED','article_types':['FAQ','Beratung','Vergleich','Pflege']
    } for fid,text in evidence.items()}
    def para(fid,prefix,n,with_trace=False,link=''):
        tr=trace(fid,f'Fachquelle {fid}',hashes[fid]) if with_trace else ''
        return f'<p data-fact-ids="{fid}">{tr} {words(prefix,n)} {link}</p>'
    intro='<section data-block="intro"><p data-fact-ids="F1">'+trace('F1','Fachquelle F1',hashes['F1'])+' Eine Longierpeitsche unterstützt die Hilfengebung beim Longieren und ergänzt Stimme und Longe. '+words('Einleitung Training Pferde',82)+' <a data-link-role="parent_category" href="/training/">Training</a></p></section>'
    answer='<section data-block="answer"><h2>Welche Aufgabe die Longierpeitsche hat</h2>'+''.join([
      para('F2','Aufgabe Longierpeitsche Longieren A',55,True),para('F2','Aufgabe Longierpeitsche Longieren B',54),
      para('F2','Aufgabe Longierpeitsche Longieren C',54),para('F2','Aufgabe Longierpeitsche Longieren D',54)])+'</section>'
    details='<section data-block="details"><h2>Stimme und Longe im Zusammenspiel</h2>'+''.join([
      para('F3','Stimme Longe Zusammenspiel A',55,True,'<a data-link-role="semantic_related" href="/training/longieren/">Longieren</a>'),
      para('F3','Stimme Longe Zusammenspiel B',54),para('F3','Stimme Longe Zusammenspiel C',54),para('F3','Stimme Longe Zusammenspiel D',54)])+'</section>'
    checklist_ps=''.join([para('F4','Sicherer Einsatz Longieren A',52,True),para('F4','Sicherer Einsatz Longieren B',51),para('F4','Sicherer Einsatz Longieren C',51),para('F4','Sicherer Einsatz Longieren D',51)])
    checklist='<section data-block="checklist"><h2>Sicherer Einsatz beim Longieren</h2>'+checklist_ps+'<ul data-list="key_answers">'+''.join(
      f'<li data-fact-ids="F4">Sicherer Punkt {w}</li>' for w in ('eins','zwei','drei','vier'))+'</ul></section>'
    conclusion='<section data-block="conclusion"><h2>Fazit</h2>'+para('F5','Fazit Einsatz Sicherheit A',40,True)+para('F5','Fazit Einsatz Sicherheit B',40)+'</section>'
    further='<section data-block="further_information"><h2>Weiterführende Informationen</h2><p>'+words('Weitere Hinweise',30)+' <a data-link-role="further_information" href="/training/longierpeitschen/">Longierpeitschen</a></p></section>'
    html='<article>'+intro+answer+details+checklist+conclusion+further+'</article>'
    bound_links=[
      {'role':'parent_category','href':'/training/','anchor':'Training','block':'intro'},
      {'role':'semantic_related','href':'/training/longieren/','anchor':'Longieren','block':'details'},
      {'role':'further_information','href':'/training/longierpeitschen/','anchor':'Longierpeitschen','block':'further_information'},
    ]
    return {
      'article_id':'A1','article_type':'FAQ','title':'Was ist eine Longierpeitsche?','target_keyword':'Was ist eine Longierpeitsche',
      'type_meta':{'primary_question':'Was ist eine Longierpeitsche?'},'research_claims':claims,'required_fact_ids':list(claims),'allowed_fact_ids':list(claims),
      'bound_links':bound_links,'link_registry':[{'href':x['href'],'active':True} for x in bound_links],
      'runtime_link_roles':['parent_category','semantic_related','further_information'],
      'wordpress_category':{'id':12,'slug':'training'},
      'heading_intent_terms':['Aufgabe','Longierpeitsche','Stimme','Longe','Zusammenspiel','Sicherer','Einsatz','Longieren'],
      'comparison_source_bindings':[],
      'table_decision':{'decision':'OMIT_NO_ADDED_VALUE','rationale':'FAQ enthält eine klare Schrittfolge ohne zusätzlichen Tabellenmehrwert.'},
      'html':html,'external_results':{'LanguageTool 6.8':'PASS'},'semantic_rule_results':{}
    }

def package_pass_results():
    return {key:'PASS' for _,_,key in PACKAGE_RESULT_MAP}

class K10Tests(unittest.TestCase):
    def test_field_inventory_is_complete(self):
        r=field_audit(); self.assertEqual(r['status'],'PASS',r); self.assertEqual(r['total'],151); self.assertEqual(r['bad'],[])

    def test_catalog_has_unique_owner_and_no_pending_hard_rule(self):
        self.assertEqual(validate_catalog()['status'],'PASS',validate_catalog())
        self.assertEqual(owner_verify()['status'],'PASS',owner_verify())

    def test_isolation_has_no_active_k9_runtime(self):
        self.assertEqual(isolation_verify()['status'],'PASS',isolation_verify())

    def test_system_rules_pass_once(self):
        sid,sha,receipts=run_system_checks(); result=verify_system(sid,sha,receipts)
        self.assertEqual(result['status'],'PASS',result)

    def test_positive_article_passes_all_article_rules(self):
        a=make_base(); receipts=run_article_checks(a); result=verify_article(a['article_id'],article_hash(a),receipts)
        self.assertEqual(result['status'],'PASS',result)

    def test_negative_abstract_h2_blocks_once(self):
        a=make_base(); a['html']=a['html'].replace('Welche Aufgabe die Longierpeitsche hat','Funktion beim Longieren verständlich erklärt')
        receipts=run_article_checks(a); result=verify_article(a['article_id'],article_hash(a),receipts)
        self.assertEqual(result['status'],'BLOCKED')
        self.assertEqual(sum(x=='HARD_RULE_NOT_PASS:heading.natural_concrete_section_language' for x in result['findings']),1)

    def test_faq_without_table_passes(self):
        a=make_base(); self.assertNotIn('<table',a['html']); result=verify_article(a['article_id'],article_hash(a),run_article_checks(a))
        self.assertEqual(result['status'],'PASS',result)

    def test_comparison_without_table_blocks(self):
        a=make_base(); a['article_type']='Vergleich'; a['title']='Longierpeitschen vergleichen'; a['target_keyword']='Longierpeitschen vergleichen'; a['type_meta']={'comparison_targets':['A','B'],'comparison_criteria':['Preis','Einsatz']}
        result=verify_article(a['article_id'],article_hash(a),run_article_checks(a))
        self.assertIn('HARD_RULE_NOT_PASS:table.required_for_comparison',result['findings'])

    def test_table_without_semantic_value_blocks(self):
        a=make_base()
        table='<section data-block="table"><h2>Merkmale im Überblick</h2><table class="system-129-table comparison-table"><thead><tr><th>Merkmal</th><th>Bedeutung</th></tr></thead><tbody><tr><td>Funktion</td><td>Hilfe beim Longieren</td></tr><tr><td>Sicherheit</td><td>Kontrolle erhalten</td></tr></tbody></table><p>Die Übersicht fasst die genannten Punkte für den schnellen Vergleich kompakt zusammen.</p></section>'
        a['html']=a['html'].replace('<section data-block="conclusion">',table+'<section data-block="conclusion">')
        a['semantic_rule_results']['table.value_required_if_present']='FAIL'
        result=verify_article(a['article_id'],article_hash(a),run_article_checks(a))
        self.assertIn('HARD_RULE_NOT_PASS:table.value_required_if_present',result['findings'])

    def test_missing_optional_table_decision_blocks(self):
        a=make_base(); a.pop('table_decision',None)
        result=verify_article(a['article_id'],article_hash(a),run_article_checks(a))
        self.assertIn('HARD_RULE_NOT_PASS:table.optional_decision_documented',result['findings'])

    def test_missing_intro_orientation_blocks(self):
        a=make_base()
        a['html']=a['html'].replace('Eine Longierpeitsche unterstützt die Hilfengebung beim Longieren und ergänzt Stimme und Longe.','Heute betrachten wir zunächst einige wichtige praktische Punkte für den Alltag.')
        result=verify_article(a['article_id'],article_hash(a),run_article_checks(a))
        self.assertIn('HARD_RULE_NOT_PASS:intro.orientation_sentence',result['findings'])

    def test_missing_receipt_blocks_without_content_recheck(self):
        a=make_base(); receipts=run_article_checks(a); receipts=[r for r in receipts if r['rule_id']!='title.colon_forbidden']
        result=verify_article(a['article_id'],article_hash(a),receipts)
        self.assertIn('MISSING_HARD_RULE_RECEIPT:title.colon_forbidden',result['findings'])

    def test_modified_html_after_pass_invalidates_receipts(self):
        a=make_base(); receipts=run_article_checks(a); changed=copy.deepcopy(a); changed['html']=a['html']+'<!--changed-->'
        result=verify_article(changed['article_id'],article_hash(changed),receipts)
        self.assertTrue(any(x.startswith('RECEIPT_SUBJECT_HASH_MISMATCH:') for x in result['findings']))

    def test_modified_title_after_pass_invalidates_receipts(self):
        a=make_base(); receipts=run_article_checks(a); changed=copy.deepcopy(a); changed['title']='Anderer Titel'
        result=verify_article(changed['article_id'],article_hash(changed),receipts)
        self.assertTrue(any(x.startswith('RECEIPT_SUBJECT_HASH_MISMATCH:') for x in result['findings']))

    def test_duplicate_receipt_blocks(self):
        a=make_base(); receipts=run_article_checks(a); receipts.append(copy.deepcopy(receipts[0]))
        result=verify_article(a['article_id'],article_hash(a),receipts)
        self.assertTrue(any(x.startswith('DUPLICATE_HARD_RULE_RECEIPT:') for x in result['findings']))

    def test_package_integrity_uses_only_own_external_receipts(self):
        pid='P1'; psha='a'*64; receipts=make_package_receipts(pid,psha,package_pass_results())
        result=verify_package(pid,psha,receipts); self.assertEqual(result['status'],'PASS',result)

    def test_package_missing_endstempel_blocks_without_article_recheck(self):
        pid='P1'; psha='a'*64; receipts=make_package_receipts(pid,psha,{**package_pass_results(),'ENDSTEMPEL':'FAIL'})
        result=verify_package(pid,psha,receipts); self.assertIn('HARD_RULE_NOT_PASS:endstempel.signature',result['findings'])

    def test_pre_wordpress_stage_passes_without_render_receipts_but_full_stop_stays_blocked(self):
        pid='P1'; psha='a'*64; results=package_pass_results()
        for key in ('WORDPRESS_RENDERED_H1','WORDPRESS_RENDERED_DUPLICATE_HEADINGS','WORDPRESS_RENDERED_ADJACENT_HEADINGS','WORDPRESS_RENDERED_EVIDENCE_CLASS'):
            results[key]='PENDING_NO_WRITE_RENDER'
        receipts=make_pre_wordpress_package_receipts(pid,psha,results)
        expected={r['id'] for r in hard_rules('PACKAGE_INTEGRITY') if r.get('check_stage')!='WORDPRESS_VERIFY'}
        pending={r['id'] for r in hard_rules('PACKAGE_INTEGRITY') if r.get('check_stage')=='WORDPRESS_VERIFY'}
        self.assertEqual(len(receipts),17)
        self.assertEqual({r['rule_id'] for r in receipts},expected)
        pre=verify_package_pre_wordpress(pid,psha,receipts)
        self.assertEqual(pre['status'],'READY_FOR_WORDPRESS_DRAFT_IMPORT',pre)
        self.assertEqual(set(pre['pending_wordpress_rule_ids']),pending)
        full=verify_package(pid,psha,receipts)
        self.assertEqual(full['status'],'BLOCKED')
        for rid in pending:
            self.assertIn('MISSING_HARD_RULE_RECEIPT:'+rid,full['findings'])

    def test_pre_wordpress_stage_still_blocks_any_failed_pre_wordpress_rule(self):
        pid='P1'; psha='a'*64; results=package_pass_results(); results['ENDSTEMPEL']='FAIL'
        receipts=make_pre_wordpress_package_receipts(pid,psha,results)
        pre=verify_package_pre_wordpress(pid,psha,receipts)
        self.assertEqual(pre['status'],'BLOCKED')
        self.assertIn('HARD_RULE_NOT_PASS:endstempel.signature',pre['findings'])


    def test_ppm104_parity_is_exact_and_single_owner(self):
        r=ppm_parity_verify(); self.assertEqual(r['status'],'PASS',r)
        self.assertEqual(r['legacy_rule_count'],104)
        self.assertEqual(r['repairable_content_count'],89)
        self.assertEqual(r['hard_integrity_count'],15)
        self.assertEqual(r['approved_table_policy_changes'],3)

    def test_ppm104_missing_mapping_fails_closed(self):
        import engine.ppm_parity_guard as pg
        original=json.loads(pg.MAP_PATH.read_text(encoding='utf-8'))
        bad=copy.deepcopy(original); bad['entries']=bad['entries'][:-1]
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'map.json'; path.write_text(json.dumps(bad),encoding='utf-8')
            with mock.patch.object(pg,'MAP_PATH',path):
                r=pg.verify()
        self.assertEqual(r['status'],'BLOCKED')
        self.assertTrue(any('PPM_PARITY_COUNT_INVALID' in x or 'PPM_PARITY_INVENTORY_SET_MISMATCH' in x for x in r['findings']))

    def test_exactly_one_receipt_per_article_hard_rule(self):
        a=make_base(); receipts=run_article_checks(a)
        required={r['id'] for r in hard_rules('ARTICLE')}
        self.assertEqual({r['rule_id'] for r in receipts},required)
        self.assertEqual(len(receipts),len(required))

    def test_exactly_one_receipt_per_package_hard_rule(self):
        receipts=make_package_receipts('P1','a'*64,package_pass_results())
        required={r['id'] for r in hard_rules('PACKAGE_INTEGRITY')}
        self.assertEqual({r['rule_id'] for r in receipts},required)
        self.assertEqual(len(receipts),len(required))

    def test_each_package_integrity_rule_can_block(self):
        for rid,owner,key in PACKAGE_RESULT_MAP:
            results=package_pass_results(); results[key]='FAIL'
            receipts=make_package_receipts('P1','a'*64,results)
            result=verify_package('P1','a'*64,receipts)
            self.assertIn('HARD_RULE_NOT_PASS:'+rid,result['findings'],rid)

    def test_negative_ppm_migration_families_block(self):
        cases=[]
        a=make_base(); a['html']=a['html'].replace('<article>','<article><h1>Falsche H1</h1>',1); cases.append(('structure.body_h1_forbidden',a))
        a=make_base(); a['html']=__import__('re').sub(r'(?is)<ul data-list="key_answers">.*?</ul>','<ul data-list="key_answers"><li data-fact-ids="F4">Sicherer Punkt eins</li></ul>',a['html'],count=1); cases.append(('structure.list_minimum_items',a))
        a=make_base(); a['html']=a['html'].replace('Einleitung Training Pferde','[LTABCDEF] Einleitung Training Pferde',1); cases.append(('structure.visible_test_marker_forbidden',a))
        a=make_base(); a['research_claims']['F2']['claim_status']='UNVERIFIED'; cases.append(('facts.referenced_fact_verified',a))
        a=make_base(); a['required_fact_ids'].append('F999'); cases.append(('facts.fact_pack_coverage',a))
        a=make_base(); a['bound_links'][1]['block']='answer'; cases.append(('links.section_placement',a))
        a=make_base(); a['html']=a['html'].replace('</article>','',1); cases.append(('structure.html_balanced',a))
        a=make_base(); a['html']=a['html'].replace('Aufgabe Longierpeitsche Longieren A','Der fachliche Grund ist, dass Aufgabe Longierpeitsche Longieren A',1); cases.append(('surface.known_regression_patterns_forbidden',a))
        a=make_base(); a['wordpress_category']={'id':0,'slug':'uncategorized'}; cases.append(('wordpress.semantic_category_binding',a))
        for rid,a in cases:
            receipts=run_article_checks(a); result=verify_article(a['article_id'],article_hash(a),receipts)
            self.assertIn('HARD_RULE_NOT_PASS:'+rid,result['findings'],rid)

    def test_legitimate_source_title_containing_test_is_allowed(self):
        a=make_base()
        a['research_claims']['F2']['source_title']='CAVALLO – Schermaschinen im Test'
        a['html']=a['html'].replace('data-source-title="Fachquelle F2"','data-source-title="CAVALLO – Schermaschinen im Test"')
        result=verify_article(a['article_id'],article_hash(a),run_article_checks(a))
        self.assertNotIn('HARD_RULE_NOT_PASS:facts.real_source_trace',result['findings'])

    def test_placeholder_source_title_still_blocks(self):
        a=make_base()
        a['research_claims']['F2']['source_title']='Test'
        a['html']=a['html'].replace('data-source-title="Fachquelle F2"','data-source-title="Test"')
        result=verify_article(a['article_id'],article_hash(a),run_article_checks(a))
        self.assertIn('HARD_RULE_NOT_PASS:facts.real_source_trace',result['findings'])

if __name__=='__main__': unittest.main(verbosity=2)
