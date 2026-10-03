import copy, sys, unittest, json, tempfile
from pathlib import Path
from unittest import mock
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from engine.catalog_guard import validate_catalog
from engine.checkers import run_article_checks, run_article_content_checks, article_hash, adapter_receipts
from engine.final_integrity import verify_article, verify_article_pre_lt68, verify_system, verify_package, verify_package_pre_wordpress
from engine.preflight import materialize_trace_bindings, preflight_article
from engine.lt68_external import visible_text
import engine.lt68_external as lt68
from engine.isolation_guard import verify as isolation_verify
from engine.owner_guard import verify as owner_verify
from engine.field_coverage import audit as field_audit
from engine.system_guard import run_system_checks
from engine.package_adapters import make_package_receipts, make_pre_wordpress_package_receipts
from engine.ppm_parity_guard import verify as ppm_parity_verify
from engine.core import hard_rules
from engine.package_adapters import PACKAGE_RESULT_MAP
from engine.real_proof import slug_from_title
from engine.production_entry import validate as validate_production_entry, build_job_metadata_snapshot, Blocked as ProductionEntryBlocked
from engine.wordpress_export import build_single as build_wordpress_export, ExportBlocked as WordPressExportBlocked
from engine.html_design import materialize_canonical_root, DesignBlocked as HtmlDesignBlocked


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
    intro='<section data-block="intro"><p data-fact-ids="F1">'+trace('F1','Fachquelle F1',hashes['F1'])+' Eine Longierpeitsche unterstützt die Hilfengebung beim Longieren und ergänzt Stimme und Longe. '+words('Einleitung Training Pferde',82)+'</p></section>'
    answer='<section data-block="answer"><h2>Welche Aufgabe die Longierpeitsche hat</h2>'+''.join([
      para('F2','Aufgabe Longierpeitsche Longieren A',55,True,'<a data-link-role="parent_category" href="/training/">Training</a>'),para('F2','Aufgabe Longierpeitsche Longieren B',54),
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
      {'role':'parent_category','href':'/training/','anchor':'Training','block':'answer'},
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
      'table_decision':{'decision':'OMIT_NO_ADDED_VALUE','exception_code':'EXISTING_CHECKLIST_EQUIVALENT','rationale':'Die vorhandene Checkliste bietet bereits denselben Scan- und Kontrollnutzen; eine zusätzliche Tabelle hätte keine eigene Funktion.'},
      'html':html,'external_results':{'LanguageTool 6.8':'PASS'},'semantic_rule_results':{}
    }

def package_pass_results():
    return {key:'PASS' for _,_,key in PACKAGE_RESULT_MAP}

class K10Tests(unittest.TestCase):

    def test_preflight_uses_exact_article_rules_before_lt68(self):
        a=make_base()
        prepared,receipts,report=preflight_article(a)
        expected={r['id'] for r in hard_rules('ARTICLE') if r['id']!='lt68.language_zero_unresolved'}
        self.assertEqual(report['status'],'READY_FOR_LT68',report)
        self.assertEqual({r['rule_id'] for r in receipts},expected)
        self.assertEqual(len(receipts),len(expected))
        self.assertEqual(verify_article_pre_lt68(prepared['article_id'],article_hash(prepared),receipts)['status'],'READY_FOR_LT68')

    def test_preflight_blocks_unsupported_numeric_claim_before_lt68(self):
        a=make_base()
        a['html']=a['html'].replace('Aufgabe Longierpeitsche Longieren A','Aufgabe Longierpeitsche Longieren 999 A',1)
        prepared,receipts,report=preflight_article(a)
        self.assertEqual(report['status'],'BLOCKED')
        self.assertIn('HARD_RULE_NOT_PASS:facts.numeric_claim_supported',report['verification']['findings'])

    def test_preflight_materializes_missing_conclusion_trace_without_visible_change(self):
        a=make_base()
        h=a['research_claims']['F5']['evidence_text_sha256']
        marker=trace('F5','Fachquelle F5',h)
        before=visible_text(a['html'])
        a['html']=a['html'].replace(marker,'',1)
        prepared,binding=materialize_trace_bindings(a)
        self.assertEqual(visible_text(prepared['html']),before)
        self.assertRegex(prepared['html'],r'<span class="ppm-source-trace"[^>]*data-fact-id="F5"[^>]*data-source-title="Fachquelle F5"[^>]*data-source-hash="'+h+r'"[^>]*></span>')
        self.assertTrue(any(x['fact_id']=='F5' and x['block']=='conclusion' for x in binding['inserted']))
        _,_,report=preflight_article(a)
        self.assertEqual(report['status'],'READY_FOR_LT68',report)

    def test_trace_binding_accepts_html_escaped_source_title(self):
        a=make_base()
        a['research_claims']['F1']['source_title']='Fachquelle F1 & Partner'
        a['html']=a['html'].replace('data-source-title="Fachquelle F1"','data-source-title="Fachquelle F1 &amp; Partner"')
        result=verify_article(a['article_id'],article_hash(a),run_article_checks(a))
        self.assertNotIn('HARD_RULE_NOT_PASS:facts.trace_binding',result['findings'])

    def test_trace_binding_still_blocks_different_escaped_source_title(self):
        a=make_base()
        a['research_claims']['F1']['source_title']='Fachquelle F1 & Partner'
        a['html']=a['html'].replace('data-source-title="Fachquelle F1"','data-source-title="Fachquelle F1 &amp; Andere"')
        result=verify_article(a['article_id'],article_hash(a),run_article_checks(a))
        self.assertIn('HARD_RULE_NOT_PASS:facts.trace_binding',result['findings'])

    def test_preflight_receipts_compose_with_lt68_receipt_without_content_recheck(self):
        a=make_base()
        prepared,receipts,report=preflight_article(a)
        self.assertEqual(report['status'],'READY_FOR_LT68',report)
        prepared['external_results']={'LanguageTool 6.8':'PASS'}
        full=list(receipts)+adapter_receipts(prepared)
        self.assertEqual(verify_article(prepared['article_id'],article_hash(prepared),full)['status'],'PASS')


    def test_lt68_batch_invokes_java_once_for_multiple_articles(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); jar=root/'lt.jar'; jar.write_bytes(b'x')
            a1=make_base(); a2=make_base(); a2['article_id']='A2'; a2['title']='Was ist eine zweite Longierpeitsche?'; a2['target_keyword']='Was ist eine zweite Longierpeitsche'; a2['type_meta']={'primary_question':'Was ist eine zweite Longierpeitsche?'}
            p1=root/'a1.json'; p2=root/'a2.json'
            p1.write_text(json.dumps(a1,ensure_ascii=False),encoding='utf-8'); p2.write_text(json.dumps(a2,ensure_ascii=False),encoding='utf-8')
            raw={'matches':[],'language':{'code':'de-DE'},'software':{'name':'LanguageTool'},'warnings':{}}
            with mock.patch.object(lt68,'sha_file',return_value=lt68.JAR_SHA256), mock.patch.object(lt68,'_invoke',return_value=raw) as invoke:
                reports=lt68.run_many(jar,[p1,p2])
            self.assertEqual(invoke.call_count,1)
            self.assertEqual([x['article_id'] for x in reports],['A1','A2'])
            self.assertTrue(all(x['status']=='PASS' for x in reports))

    def test_lt68_batch_fails_closed_on_cross_boundary_finding(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); jar=root/'lt.jar'; jar.write_bytes(b'x')
            a1=make_base(); a2=make_base(); a2['article_id']='A2'
            p1=root/'a1.json'; p2=root/'a2.json'
            p1.write_text(json.dumps(a1,ensure_ascii=False),encoding='utf-8'); p2.write_text(json.dumps(a2,ensure_ascii=False),encoding='utf-8')
            boundary=len(visible_text(a1['html']))+1
            raw={'matches':[{'offset':boundary,'length':1,'rule':{'id':'TEST'},'message':'boundary'}],'language':{'code':'de-DE'},'software':{'name':'LanguageTool'},'warnings':{}}
            with mock.patch.object(lt68,'sha_file',return_value=lt68.JAR_SHA256), mock.patch.object(lt68,'_invoke',return_value=raw):
                with self.assertRaises(lt68.Blocked):
                    lt68.run_many(jar,[p1,p2])

    def test_wordpress_slug_is_derived_from_current_title(self):
        self.assertEqual(slug_from_title('Kann man mit Kappzaum spazieren gehen?'),'kann-man-mit-kappzaum-spazieren-gehen')
        self.assertEqual(slug_from_title('Wie oft muss ein Pferdeanhänger zum TÜV?'),'wie-oft-muss-ein-pferdeanhaenger-zum-tuev')

    def test_wordpress_slug_is_not_historical_constant(self):
        self.assertEqual(slug_from_title('Passende Kühlgamaschen für Pferde wählen'),'passende-kuehlgamaschen-fuer-pferde-waehlen')
        self.assertNotEqual(slug_from_title('Passende Kühlgamaschen für Pferde wählen'),'wie-lege-ich-einen-longiergurt-an')

    def test_generic_production_entry_positive_and_missing_research_negative(self):
        import hashlib
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            item={'article_type':'FAQ','category':'training','plan_slot':'A1','target_keyword':'Was ist eine Longierpeitsche','title':'Was ist eine Longierpeitsche?'}
            intake={'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2','status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE','item_count':1,'maximum_articles':0,'maximum_articles_per_type':0,'publish_allowed':False,'content_or_format_payload_present':False,'items':[item]}
            intake['batch_sha256']=hashlib.sha256(json.dumps(intake,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
            a=make_base(); a['article_id']='A1'; a['planning_binding']={**item,'source_ref':'main:concept_agent/current/PSERC_METADATA_SNAPSHOT.json'}; a['publish_allowed']=False
            claims=[]
            sources=[]
            for idx,(fid,cl) in enumerate(a['research_claims'].items(),1):
                url=f'https://example.org/source-{idx}'
                cl['source_url']=url
                claims.append({'fact_id':fid,**cl})
                sources.append({'source_id':f'S{idx}','title':cl['source_title'],'url':url})
            research={'contract':'K10_REAL_RESEARCH_V1','article_id':'A1','topic':a['title'],'retrieved_at':'2026-10-02','sources':sources,'claims':claims,'publish_allowed':False}
            pserc=build_job_metadata_snapshot(intake)
            for name,obj in [('WORDPRESS_INTAKE.json',intake),('RESEARCH.json',research),('ARTICLE_INPUT.json',a),('pserc.json',pserc)]:
                (root/name).write_text(json.dumps(obj,ensure_ascii=False),encoding='utf-8')
            report=validate_production_entry(root,root/'pserc.json')
            self.assertEqual(report['status'],'READY_FOR_K10_PREFLIGHT',report)
            (root/'RESEARCH.json').unlink()
            with self.assertRaises(FileNotFoundError):
                validate_production_entry(root,root/'pserc.json')


    def test_generic_production_entry_accepts_current_three_item_upload_without_external_snapshot(self):
        import hashlib
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            items=[
              {'article_type':'FAQ','category':'faq-a','plan_slot':'1'*64,'target_keyword':'Frage A','title':'Frage A?'},
              {'article_type':'FAQ','category':'faq-b','plan_slot':'2'*64,'target_keyword':'Frage B','title':'Frage B?'},
              {'article_type':'FAQ','category':'faq-c','plan_slot':'3'*64,'target_keyword':'Frage C','title':'Frage C?'},
            ]
            intake={'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2','status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE','item_count':3,'maximum_articles':0,'maximum_articles_per_type':0,'publish_allowed':False,'content_or_format_payload_present':False,'items':items}
            intake['batch_sha256']=hashlib.sha256(json.dumps(intake,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
            item=items[1]
            a=make_base(); a['article_id']=item['plan_slot']; a['article_type']='FAQ'; a['title']=item['title']; a['target_keyword']=item['target_keyword']; a['planning_binding']={**item,'source_ref':'CURRENT_UPLOADED_WORDPRESS_INTAKE'}; a['publish_allowed']=False
            claims=[]; sources=[]
            for idx,(fid,cl) in enumerate(a['research_claims'].items(),1):
                url=f'https://example.org/current-upload-{idx}'
                cl['source_url']=url
                claims.append({'fact_id':fid,**cl})
                sources.append({'source_id':f'S{idx}','title':cl['source_title'],'url':url})
            research={'contract':'K10_REAL_RESEARCH_V1','article_id':item['plan_slot'],'topic':a['title'],'retrieved_at':'2026-10-02','sources':sources,'claims':claims,'publish_allowed':False}
            pserc=build_job_metadata_snapshot(intake)
            for name,obj in [('WORDPRESS_INTAKE.json',intake),('RESEARCH.json',research),('ARTICLE_INPUT.json',a),('pserc.json',pserc)]:
                (root/name).write_text(json.dumps(obj,ensure_ascii=False),encoding='utf-8')
            report=validate_production_entry(root,root/'pserc.json')
            self.assertEqual(report['status'],'READY_FOR_K10_PREFLIGHT',report)
            self.assertEqual(report['source_batch_item_count'],3)
            self.assertEqual(report['metadata_authority'],'CURRENT_UPLOADED_WORDPRESS_INTAKE')

    def test_generic_production_entry_rejects_stale_external_metadata_snapshot(self):
        import hashlib
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            item={'article_type':'FAQ','category':'faq-new','plan_slot':'4'*64,'target_keyword':'Neue Frage','title':'Neue Frage?'}
            intake={'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2','status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE','item_count':1,'maximum_articles':0,'maximum_articles_per_type':0,'publish_allowed':False,'content_or_format_payload_present':False,'items':[item]}
            intake['batch_sha256']=hashlib.sha256(json.dumps(intake,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
            a=make_base(); a['article_id']=item['plan_slot']; a['article_type']='FAQ'; a['title']=item['title']; a['target_keyword']=item['target_keyword']; a['planning_binding']={**item,'source_ref':'CURRENT_UPLOADED_WORDPRESS_INTAKE'}; a['publish_allowed']=False
            claims=[]; sources=[]
            for idx,(fid,cl) in enumerate(a['research_claims'].items(),1):
                url=f'https://example.org/stale-check-{idx}'
                cl['source_url']=url
                claims.append({'fact_id':fid,**cl})
                sources.append({'source_id':f'S{idx}','title':cl['source_title'],'url':url})
            research={'contract':'K10_REAL_RESEARCH_V1','article_id':item['plan_slot'],'topic':a['title'],'retrieved_at':'2026-10-02','sources':sources,'claims':claims,'publish_allowed':False}
            stale={'system_boundary':{'publish_allowed':False},'next_textmachine_metadata_batch':{'items':[{'article_type':'FAQ','category':'old','plan_slot':'5'*64,'target_keyword':'Alt','title':'Alt?'}]}}
            for name,obj in [('WORDPRESS_INTAKE.json',intake),('RESEARCH.json',research),('ARTICLE_INPUT.json',a),('pserc.json',stale)]:
                (root/name).write_text(json.dumps(obj,ensure_ascii=False),encoding='utf-8')
            with self.assertRaisesRegex(ProductionEntryBlocked,'JOB_METADATA_BINDING_MISMATCH_CURRENT_UPLOAD_REQUIRED'):
                validate_production_entry(root,root/'pserc.json')

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

    def test_negative_missing_enumeration_separator_h2_blocks_once(self):
        a=make_base()
        a['html']=a['html'].replace('Stimme und Longe im Zusammenspiel','Stimme Longe und Zusammenspiel nutzen')
        result=verify_article(a['article_id'],article_hash(a),run_article_checks(a))
        self.assertEqual(result['status'],'BLOCKED')
        self.assertEqual(sum(x=='HARD_RULE_NOT_PASS:heading.natural_concrete_section_language' for x in result['findings']),1)

    def test_positive_enumeration_h2_with_comma_passes(self):
        a=make_base()
        a['html']=a['html'].replace('Stimme und Longe im Zusammenspiel','Stimme, Longe und Zusammenspiel nutzen')
        result=verify_article(a['article_id'],article_hash(a),run_article_checks(a))
        self.assertEqual(result['status'],'PASS',result)

    def test_faq_without_table_passes_only_with_defined_exception(self):
        a=make_base(); self.assertNotIn('<table',a['html'])
        result=verify_article(a['article_id'],article_hash(a),run_article_checks(a))
        self.assertEqual(result['status'],'PASS',result)

    def test_faq_without_table_and_without_exception_blocks(self):
        a=make_base()
        a['table_decision']={'decision':'OMIT_NO_ADDED_VALUE','rationale':'Der Text ist auch ohne Tabelle verständlich genug.'}
        result=verify_article(a['article_id'],article_hash(a),run_article_checks(a))
        self.assertIn('HARD_RULE_NOT_PASS:table.presence_policy',result['findings'])
        self.assertIn('HARD_RULE_NOT_PASS:table.optional_decision_documented',result['findings'])

    def test_faq_without_table_with_unknown_exception_blocks(self):
        a=make_base()
        a['table_decision']={'decision':'OMIT_NO_ADDED_VALUE','exception_code':'TEXT_ALREADY_CLEAR','rationale':'Der Text ist bereits klar und braucht deshalb keine zusätzliche Darstellung.'}
        result=verify_article(a['article_id'],article_hash(a),run_article_checks(a))
        self.assertIn('HARD_RULE_NOT_PASS:table.presence_policy',result['findings'])


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

    def test_tautological_table_blocks_even_with_semantic_pass(self):
        a=make_base()
        h=a['research_claims']['F2']['evidence_text_sha256']
        tr=trace('F2','Fachquelle F2',h)
        table=f'<section data-block="table"><h2>Hilfsmittel beim Longieren gezielt auswählen</h2><table class="system-129-table comparison-table"><thead><tr><th>Hilfsmittel</th><th>Zweck</th><th>Kontrolle</th></tr></thead><tbody><tr><td data-fact-ids="F2">Longierpeitsche</td><td data-fact-ids="F2">Hilfe beim Longieren</td><td data-fact-ids="F2">Longierpeitsche prüfen</td></tr><tr><td data-fact-ids="F3">Stimme</td><td data-fact-ids="F3">Hilfen beim Longieren</td><td data-fact-ids="F3">Stimme kontrollieren</td></tr><tr><td data-fact-ids="F3">Longe</td><td data-fact-ids="F3">Zusammenspiel</td><td data-fact-ids="F3">Longe prüfen</td></tr><tr><td data-fact-ids="F4">Abstand</td><td data-fact-ids="F4">Sicherer Einsatz</td><td data-fact-ids="F4">Kontrolle beim Longieren</td></tr></tbody></table><p data-fact-ids="F2">{tr} Die Tabelle ordnet Aufgabe, Longierpeitsche und Hilfe beim Longieren für Training und sicheren Einsatz knapp als Entscheidungshilfe.</p></section>'
        a['html']=a['html'].replace('<section data-block="conclusion">',table+'<section data-block="conclusion">')
        a['table_decision']={'decision':'INCLUDE_ADDED_VALUE','rationale':'Die Tabelle soll Hilfsmittel und Kontrollen als Entscheidungshilfe verbinden.'}
        a['semantic_rule_results']['table.value_required_if_present']='PASS'
        result=verify_article(a['article_id'],article_hash(a),run_article_checks(a))
        self.assertIn('HARD_RULE_NOT_PASS:table.value_required_if_present',result['findings'])

    def test_non_tautological_table_passes_with_semantic_pass(self):
        a=make_base()
        h=a['research_claims']['F2']['evidence_text_sha256']
        tr=trace('F2','Fachquelle F2',h)
        table=f'<section data-block="table"><h2>Hilfsmittel beim Longieren gezielt auswählen</h2><table class="system-129-table comparison-table"><thead><tr><th>Hilfsmittel</th><th>Zweck</th><th>Kontrolle</th></tr></thead><tbody><tr><td data-fact-ids="F2">Longierpeitsche</td><td data-fact-ids="F2">Hilfe beim Longieren</td><td data-fact-ids="F2">Aufgabe im Training</td></tr><tr><td data-fact-ids="F3">Stimme</td><td data-fact-ids="F3">Hilfen beim Longieren</td><td data-fact-ids="F3">Longe im Zusammenspiel</td></tr><tr><td data-fact-ids="F3">Longe</td><td data-fact-ids="F3">Zusammenspiel</td><td data-fact-ids="F3">Stimme beim Longieren</td></tr><tr><td data-fact-ids="F4">Abstand</td><td data-fact-ids="F4">Sicherer Einsatz</td><td data-fact-ids="F4">Kontrolle beim Longieren</td></tr></tbody></table><p data-fact-ids="F2">{tr} Die Tabelle ordnet Aufgabe, Longierpeitsche und Hilfe beim Longieren für Training und sicheren Einsatz knapp als Entscheidungshilfe.</p></section>'
        a['html']=a['html'].replace('<section data-block="conclusion">',table+'<section data-block="conclusion">')
        a['table_decision']={'decision':'INCLUDE_ADDED_VALUE','rationale':'Die Tabelle verbindet Hilfsmittel mit jeweils eigenständigen Auswahl- und Kontrollpunkten.'}
        a['semantic_rule_results']['table.value_required_if_present']='PASS'
        receipts=run_article_checks(a)
        receipt=next(x for x in receipts if x['rule_id']=='table.value_required_if_present')
        self.assertEqual(receipt['status'],'PASS',receipt)

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


    def test_wordpress_export_binds_registry_article_id_to_plan_slot(self):
        import hashlib
        a=make_base()
        a,_=materialize_canonical_root(a)
        article_id='article:1234567890abcdef12345678'
        slot=hashlib.sha256(('pserc-plan-slot-v2|'+article_id).encode()).hexdigest()
        a['planning_binding']={
          'article_type':'FAQ','category':'training','plan_slot':slot,
          'target_keyword':a['target_keyword'],'title':a['title']
        }
        a['publish_allowed']=False
        for idx,(fid,claim) in enumerate(a['research_claims'].items(),1):
            claim['source_url']=f'https://example.org/source-{idx}'
        research={'contract':'K10_REAL_RESEARCH_V1','retrieved_at':'2026-10-02T00:00:00Z'}
        snapshot={'source_batch_sha256':'8'*64,'canonical_article_bindings':{slot:article_id}}
        lt={'status':'PASS','finding_count':0,'engine':'LanguageTool 6.8 / Bestand 43'}
        out=build_wordpress_export(a,research,snapshot,lt)
        self.assertEqual(out['contract'],'SYSTEM4_WORDPRESS_HANDOFF_V1')
        self.assertEqual(out['batch_sha256'],'8'*64)
        self.assertEqual(out['article_count'],1)
        self.assertIs(out['wordpress_review']['direct_wordpress_upload_ready'],True)
        row=out['articles'][0]
        self.assertEqual(set(row),{
          'index','article_id','title','target_keyword','category','article_type','plan_slot',
          'final_draft_sha256','revision_count','body','production_context',
          'languagetool','ppm679',
        })
        self.assertEqual(row['article_id'],article_id)
        self.assertNotEqual(row['article_id'],row['plan_slot'])
        self.assertEqual(row['plan_slot'],slot)
        self.assertEqual(hashlib.sha256(('pserc-plan-slot-v2|'+row['article_id']).encode()).hexdigest(),row['plan_slot'])
        self.assertEqual(row['production_context']['production_plan_item']['canonical_article_id'],article_id)
        self.assertEqual(row['final_draft_sha256'],hashlib.sha256(a['html'].encode()).hexdigest())
        self.assertEqual(row['body'],a['html'])

    def test_wordpress_export_blocks_without_canonical_registry_binding(self):
        import hashlib
        a=make_base()
        a,_=materialize_canonical_root(a)
        article_id='article:1234567890abcdef12345678'
        slot=hashlib.sha256(('pserc-plan-slot-v2|'+article_id).encode()).hexdigest()
        a['planning_binding']={
          'article_type':'FAQ','category':'training','plan_slot':slot,
          'target_keyword':a['target_keyword'],'title':a['title']
        }
        for idx,(fid,claim) in enumerate(a['research_claims'].items(),1):
            claim['source_url']=f'https://example.org/source-{idx}'
        with self.assertRaisesRegex(WordPressExportBlocked,'WORDPRESS_CANONICAL_ARTICLE_ID_MISSING'):
            build_wordpress_export(
              a,{'retrieved_at':'2026-10-02T00:00:00Z'},
              {'source_batch_sha256':'8'*64,'canonical_article_bindings':{}},
              {'status':'PASS','finding_count':0,'engine':'LanguageTool 6.8 / Bestand 43'}
            )

    def test_wordpress_export_blocks_wrong_canonical_article_id_for_slot(self):
        import hashlib
        a=make_base()
        a,_=materialize_canonical_root(a)
        correct='article:1234567890abcdef12345678'
        wrong='article:abcdef1234567890abcdef12'
        slot=hashlib.sha256(('pserc-plan-slot-v2|'+correct).encode()).hexdigest()
        a['planning_binding']={
          'article_type':'FAQ','category':'training','plan_slot':slot,
          'target_keyword':a['target_keyword'],'title':a['title']
        }
        for idx,(fid,claim) in enumerate(a['research_claims'].items(),1):
            claim['source_url']=f'https://example.org/source-{idx}'
        with self.assertRaisesRegex(WordPressExportBlocked,'WORDPRESS_CANONICAL_PLAN_SLOT_MISMATCH'):
            build_wordpress_export(
              a,{'retrieved_at':'2026-10-02T00:00:00Z'},
              {'source_batch_sha256':'8'*64,'canonical_article_bindings':{slot:wrong}},
              {'status':'PASS','finding_count':0,'engine':'LanguageTool 6.8 / Bestand 43'}
            )

    def test_wordpress_export_blocks_without_current_batch_binding(self):
        a=make_base()
        a,_=materialize_canonical_root(a)
        a['planning_binding']={
          'article_type':'FAQ','category':'training','plan_slot':'7'*64,
          'target_keyword':a['target_keyword'],'title':a['title']
        }
        for idx,(fid,claim) in enumerate(a['research_claims'].items(),1):
            claim['source_url']=f'https://example.org/source-{idx}'
        with self.assertRaisesRegex(WordPressExportBlocked,'WORDPRESS_BATCH_SHA256_MISSING'):
            build_wordpress_export(
              a,{'retrieved_at':'2026-10-02T00:00:00Z'},{},
              {'status':'PASS','finding_count':0,'engine':'LanguageTool 6.8 / Bestand 43'}
            )


    def test_wordpress_export_hard_blocks_bare_article_root(self):
        import hashlib
        a=make_base()
        article_id='article:1234567890abcdef12345678'
        slot=hashlib.sha256(('pserc-plan-slot-v2|'+article_id).encode()).hexdigest()
        a['planning_binding']={
          'article_type':'FAQ','category':'training','plan_slot':slot,
          'target_keyword':a['target_keyword'],'title':a['title']
        }
        for idx,(fid,claim) in enumerate(a['research_claims'].items(),1):
            claim['source_url']=f'https://example.org/source-{idx}'
        with self.assertRaisesRegex(HtmlDesignBlocked,'DESIGN_CANONICAL_ROOT_NOT_MATERIALIZED'):
            build_wordpress_export(
              a,{'retrieved_at':'2026-10-02T00:00:00Z'},
              {'source_batch_sha256':'8'*64,'canonical_article_bindings':{slot:article_id}},
              {'status':'PASS','finding_count':0,'engine':'LanguageTool 6.8 / Bestand 43'}
            )

if __name__=='__main__': unittest.main(verbosity=2)
