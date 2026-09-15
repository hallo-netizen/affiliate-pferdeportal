from __future__ import annotations
import hashlib, json, re, subprocess, sys
from pathlib import Path

import content_guard, root_entry, supervisor, worker_dispatch

HERE=Path(__file__).resolve().parent
REPO=HERE.parent

def canon(v)->bytes:
    return (json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()

def writej(p:Path,v)->Path:
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return p

def _head()->str:
    return subprocess.check_output(['git','rev-parse','--verify','HEAD'],cwd=REPO,text=True).strip()

def _gate(workspace:Path)->dict:
    bundle_path=workspace/'worker_dispatch.json'
    if not bundle_path.is_file(): raise RuntimeError('TESTWORKER_DISPATCH_MISSING')
    bundle=json.loads(bundle_path.read_text(encoding='utf-8'))
    manifest=root_entry._critical_manifest_sha256(); head=_head()
    wc,_=worker_dispatch.verify_bundle(bundle,actual_manifest=manifest,actual_head=head)
    supervisor.verify_controller_binding(workspace)
    if wc.get('external_web_search_allowed') is not False: raise RuntimeError('TESTWORKER_FREE_WEB_NOT_BLOCKED')
    if wc.get('machine_prewrite_mutation_allowed') is not False: raise RuntimeError('TESTWORKER_PREWRITE_MUTATION_NOT_BLOCKED')
    return wc

def _state(workspace:Path)->dict:
    _gate(workspace)
    p=workspace/'state.json'
    if not p.is_file(): raise RuntimeError('TESTWORKER_STATE_MISSING')
    return json.loads(p.read_text(encoding='utf-8'))

def _sentences(text:str)->list[str]:
    out=[]
    for raw in re.split(r'(?<=[.!?])\s+',text.strip()):
        value=' '.join(raw.split()).strip()
        if len(value)>=25: out.append(value)
    return out

def research(workspace:Path,out:Path)->dict:
    s=_state(workspace)
    if s.get('phase')!='RESEARCH_REQUIRED': raise RuntimeError('TESTWORKER_PHASE_NOT_RESEARCH')
    value=supervisor.expected_research_document(workspace)
    content_guard.validate_research_document(value); writej(out,value)
    return {'status':'PASS','stage':'RESEARCH','sha256':hashlib.sha256(canon(value)).hexdigest()}

def facts(workspace:Path,out:Path)->dict:
    s=_state(workspace)
    if s.get('phase')!='FACT_CHECK_REQUIRED': raise RuntimeError('TESTWORKER_PHASE_NOT_FACTS')
    research_obj=content_guard.validate_research_document(s['research']['text'])
    claims=[]; n=0
    for source in research_obj['sources']:
        for sentence in _sentences(source['evidence']):
            n+=1
            claims.append({'fact_id':f'fact-{s["article"]["plan_slot"][:12]}-{n}','source_id':source['source_id'],'statement':sentence,'evidence_text':sentence,'evidence_text_sha256':hashlib.sha256(sentence.encode()).hexdigest()})
    if len(claims)<4: raise RuntimeError('TESTWORKER_FACT_SOURCE_TOO_THIN')
    value={'contract':'SYSTEM4_FACTS_EVIDENCE_V1','claims':claims}
    content_guard.validate_facts_document(value,research_obj); writej(out,value)
    return {'status':'PASS','stage':'FACTS','claim_count':len(claims),'sha256':hashlib.sha256(canon(value)).hexdigest()}

def _slug(text:str)->str:
    value=text.casefold().replace('ä','ae').replace('ö','oe').replace('ü','ue').replace('ß','ss')
    return re.sub(r'[^a-z0-9]+','-',value).strip('-')[:160] or 'system4-testartikel'

def context(workspace:Path,pack_out:Path,plan_out:Path)->dict:
    s=_state(workspace)
    if s.get('phase')!='CONTEXT_REQUIRED': raise RuntimeError('TESTWORKER_PHASE_NOT_CONTEXT')
    research_obj=content_guard.validate_research_document(s['research']['text'])
    facts_obj=content_guard.validate_facts_document(s['facts']['text'],research_obj)
    pre=json.loads((workspace/'bound_machine_prewrite.json').read_text(encoding='utf-8'))
    rails=json.loads(json.dumps(pre['production_plan_rails'],ensure_ascii=False))
    snapshot_sha=hashlib.sha256((workspace/'bound_snapshot.json').read_bytes()).hexdigest()
    source_by_id={r['source_id']:r for r in research_obj['sources']}
    pack_claims=[]
    for row in facts_obj['claims']:
        c=dict(row); c['source_url']=source_by_id[row['source_id']]['source_url']; c['claim_status']='FULLY_SUPPORTED'; c['article_types']=[s['article']['article_type']]; pack_claims.append(c)
    pack={'contract':'canonical_fact_pack_v1','status':'SOURCE_VERIFIED_PRODUCTION_READY','source_snapshot_id':snapshot_sha,'fact_pack_id':snapshot_sha,'sources':research_obj['sources'],'claims':pack_claims}
    quality=rails['quality_binding']; allowed=[c['fact_id'] for c in pack_claims]
    direct=str(quality.get('faq_direct_answer') or '').strip(); links=quality.get('link_bindings') if isinstance(quality.get('link_bindings'),list) else []
    title=s['article']['title']; keyword=s['article']['target_keyword']; article_type=s['article']['article_type']
    runtime={'order_id':'system4-test-'+s['article']['plan_slot'][:16],'article_type':article_type,'title':title,'slug':_slug(title),'subject_scope':title,'subject_label':keyword,'lead':direct or title,'conclusion':'Die gebundenen Prüfpunkte werden vor der Fahrt vollständig kontrolliert und erkennbare Abweichungen vor dem Start geklärt.','links':links,'allowed_fact_ids':allowed,'question':title,'answer':direct or title,'faq_question':title,'faq_answer':direct or title,'summary':direct or title,'search_intent':rails.get('search_intent') or 'informational'}
    plan=dict(rails); plan['source_snapshot_id']=snapshot_sha; plan['runtime_order']=runtime; plan['canonical_article']={'title':title,'article_type':article_type,'slug':runtime['slug']}; plan['source_hashes']=[row['snapshot_sha256'] for row in research_obj['sources']]
    writej(pack_out,pack); writej(plan_out,plan)
    return {'status':'PASS','stage':'CONTEXT','fact_pack_claims':len(pack_claims),'allowed_fact_ids':len(allowed)}

PARAGRAPH_TAILS=[
 'Für den Ablauf vor der Abfahrt ist dieser Hinweis praktisch: Der Punkt wird bewusst angesehen und nicht nur vorausgesetzt. Eine Auffälligkeit führt deshalb zu einer erneuten Prüfung, bevor die Fahrt beginnt.',
 'Bei der Vorbereitung hilft eine feste Reihenfolge. So bleibt nachvollziehbar, welcher Zustand bereits kontrolliert wurde und welcher Punkt noch offen ist. Das verhindert, dass ein sichtbarer Hinweis zwischen anderen Handgriffen verloren geht.',
 'Die Kontrolle braucht keine komplizierte Zusatztechnik. Entscheidend ist, den beschriebenen Zustand gezielt zu betrachten, das Ergebnis einzuordnen und eine erkennbare Abweichung vor dem Losfahren zu klären.',
 'Im Alltag ist ein kurzer, immer gleicher Kontrollgang sinnvoll. Dadurch wird aus einer beiläufigen Beobachtung ein fester Prüfschritt, der vor jeder Fahrt erneut durchgeführt und nicht aus einer früheren Kontrolle übernommen wird.',
 'Ein eindeutiges Ergebnis ist wichtiger als Geschwindigkeit. Wenn der Zustand nicht klar beurteilt werden kann, bleibt der Prüfschritt offen, bis die Ursache verstanden und der vorgesehene Zustand wieder hergestellt ist.',
 'Für die Praxis bedeutet das eine klare Trennung zwischen Prüfen und Vermuten. Sichtbare oder funktionale Auffälligkeiten werden nicht weginterpretiert, sondern vor dem Start noch einmal gezielt untersucht.',
 'Der Nutzen einer festen Kontrolle liegt in der Wiederholbarkeit. Dieselben Punkte werden in derselben Vorbereitung erneut betrachtet, sodass Veränderungen gegenüber der letzten Fahrt leichter auffallen können.',
 'Auch bei vertrauter Ausrüstung bleibt der einzelne Prüfschritt bestehen. Routine ersetzt die Kontrolle nicht, sondern macht sie schneller nachvollziehbar, wenn jeder Punkt bewusst bestätigt wird.',
 'Eine dokumentierbare Reihenfolge hilft besonders dann, wenn mehrere Personen vorbereiten. Jede Person kann erkennen, welcher Punkt bereits geprüft wurde und wo vor der Fahrt noch eine Klärung erforderlich ist.',
 'Der Prüfschritt gehört zeitlich vor die Abfahrt. Dadurch bleibt genug Raum, eine Auffälligkeit zu beheben, statt sie erst während der Fahrt oder nach einer weiteren Belastung zu bemerken.',
 'Bei einer Abweichung wird nicht der gesamte Ablauf verworfen. Der betroffene Punkt wird gezielt geklärt und anschließend erneut kontrolliert; erst danach geht die Vorbereitung an der vorgesehenen Stelle weiter.',
 'Die Aussage der Quelle wird damit in eine konkrete Handlung übersetzt. Prüfen, Ergebnis bewerten und bei Unklarheit nacharbeiten bilden einen nachvollziehbaren Ablauf ohne zusätzliche Annahmen.',
 'Für einen sicheren Arbeitsablauf wird der Zustand nicht nur aus der Entfernung betrachtet. Die jeweilige Funktion oder Verbindung wird so kontrolliert, wie es der gebundene Prüfpunkt verlangt, bevor der nächste Schritt folgt.',
 'Der gleiche Prüfpunkt kann bei jeder Fahrt erneut relevant sein. Deshalb wird ein früheres positives Ergebnis nicht als dauerhafte Freigabe behandelt, sondern der aktuelle Zustand vor dem Start neu betrachtet.',
 'Eine klare Reihenfolge reduziert Auslassungen. Wer jeden Punkt nacheinander prüft, kann die Vorbereitung abschließen, ohne zwischen mehreren offenen Beobachtungen hin und her zu springen.',
 'Am Ende zählt ein nachvollziehbarer Ist-Zustand. Erst wenn der jeweilige Punkt eindeutig kontrolliert ist, wird er als erledigt betrachtet und die Vorbereitung mit dem nächsten gebundenen Prüfschritt fortgesetzt.',
]

def _trace(fact_id:str,authority:dict)->str:
    meta=authority[fact_id]
    return f'<span class="ppm-source-trace" data-fact-id="{fact_id}" data-source-title="{meta["source_id"]}" data-source-hash="{meta["evidence_text_sha256"]}"></span>'

def _p(fact_id:str,text:str,authority:dict)->str:
    return f'<p data-fact-ids="{fact_id}">{text}{_trace(fact_id,authority)}</p>'

def draft(workspace:Path,out:Path,repair:bool=False)->dict:
    s=_state(workspace); expected='REPAIR_REQUIRED' if repair else 'DRAFT_REQUIRED'
    if s.get('phase')!=expected: raise RuntimeError('TESTWORKER_PHASE_NOT_'+expected)
    c=s.get('authoring_contract')
    if not isinstance(c,dict): raise RuntimeError('TESTWORKER_AUTHORING_CONTRACT_MISSING')
    identity=c['article_identity']; bound=c['bound_requirements']; req=c['global_requirements']; type_req=c['type_requirements']; structure=c['structure_requirements']
    ids=list(bound['canonical_fact_ids']); authority=bound['fact_authority']; claims={row['fact_id']:row for row in s['production_context']['fact_pack']['claims']}
    if len(ids)<4: raise RuntimeError('TESTWORKER_FACTS_TOO_LOW_FOR_DRAFT')
    intro_name=str((structure.get('intro') or {}).get('required_block') or 'intro'); direct=str(bound.get('faq_direct_answer') or '').strip()
    sections=[f'<section data-block="{intro_name}">{_p(ids[0],direct,authority)}</section>']
    required=list(type_req.get('required_blocks') or []); non_intro=[str(x) for x in required if str(x)!=intro_name]
    labels=['Welche Kontrolle zuerst wichtig ist','Was der sichtbare Zustand zeigt','Wie die Prüfung praktisch abläuft','Wann eine Abweichung geklärt wird','Was vor dem Start noch zählt','Wie der Kontrollgang abgeschlossen wird']
    section_count=max(len(non_intro),max(0,int(req.get('min_h2') or 0)),4); used_blocks=list(non_intro)
    while len(used_blocks)<section_count: used_blocks.append('system4-section-'+str(len(used_blocks)+1))
    para_target=max(int(req.get('min_paragraphs') or 0)+3,14); cursor=0
    for si,block in enumerate(used_blocks):
        parts=[f'<h2>{labels[si%len(labels)]}</h2>']; per=max(2,(para_target-1+len(used_blocks)-1)//len(used_blocks))
        for _ in range(per):
            fid=ids[cursor%len(ids)]; text=claims[fid]['statement']+' '+PARAGRAPH_TAILS[cursor%len(PARAGRAPH_TAILS)]
            if not repair and identity['title'].startswith('Warum muss die Beleuchtung') and cursor==1: text+=' Als belastbares Ergebnis muss dieser Prüfschritt dokumentiert bleiben.'
            parts.append(_p(fid,text,authority)); cursor+=1
        sections.append(f'<section data-block="{block}">{"".join(parts)}</section>')
    links=list(bound.get('link_bindings') or [])
    if links:
        fid=ids[cursor%len(ids)]; link_parts=['<h2>Passende Bereiche im Portal</h2>']
        for row in links:
            link_parts.append(_p(fid,f'Weitere gebundene Informationen stehen unter <a href="{str(row.get("href") or "")}">{str(row.get("anchor") or "")}</a>.',authority)); cursor+=1; fid=ids[cursor%len(ids)]
        sections.append('<section data-block="portal-links">'+''.join(link_parts)+'</section>')
    rows=[]
    for r in range(max(3,int(req.get('min_table_body_rows') or 0))):
        fid=ids[r%len(ids)]; statement=claims[fid]['statement']; rows.append(f'<tr><td data-fact-ids="{fid}">Prüfpunkt {r+1}{_trace(fid,authority)}</td><td data-fact-ids="{fid}">{statement}{_trace(fid,authority)}</td></tr>')
    tfid=ids[0]; table=_p(tfid,str(bound.get('table_value_statement') or '').strip(),authority)+'<table class="system-129-table comparison-table"><thead><tr><th>Prüfpunkt</th><th>Gebundene Aussage</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table>'
    sections.append('<section data-block="comparison">'+table+'</section>')
    cfid=ids[-1]; conclusion=claims[cfid]['statement']+' Vor der Abfahrt werden deshalb alle gebundenen Punkte in einer festen Reihenfolge geprüft. Bleibt eine Beobachtung unklar, wird genau dieser Punkt erneut kontrolliert, bevor die Vorbereitung abgeschlossen wird. So endet der Ablauf mit einem aktuellen Prüfergebnis statt mit einer Annahme aus einer früheren Fahrt.'
    sections.append('<section data-block="conclusion"><h2>Was vor der Abfahrt zählt</h2>'+_p(cfid,conclusion,authority)+'</section>')
    body='<article class="ppm-generated ppm-type-faq" data-article-type="FAQ">'+''.join(sections)+'</article>'
    def wc(v:str)->int: return len(re.findall(r'\b[\wÄÖÜäöüß-]+\b',re.sub(r'<[^>]+>',' ',v),re.UNICODE))
    extra_index=0; min_words=int(req.get('min_words') or 0)
    while wc(body)<min_words+80:
        fid=ids[extra_index%len(ids)]; addition='<section data-block="detail-'+str(extra_index+1)+'"><h2>'+labels[(extra_index+2)%len(labels)]+'</h2>'+_p(fid,claims[fid]['statement']+' '+PARAGRAPH_TAILS[(extra_index+7)%len(PARAGRAPH_TAILS)],authority)+'</section>'; body=body.replace('</article>',addition+'</article>'); extra_index+=1
        if extra_index>20: raise RuntimeError('TESTWORKER_WORD_FLOOR_UNREACHABLE')
    out.write_text(body,encoding='utf-8')
    return {'status':'PASS','stage':'REPAIR' if repair else 'DRAFT','word_count':wc(body),'sha256':hashlib.sha256(body.encode()).hexdigest()}

def main(argv:list[str])->int:
    if len(argv)<3: raise SystemExit('usage: deterministic_test_worker.py <gate|research|facts|context|draft|repair> <workspace> [outputs...]')
    cmd=argv[1]; w=Path(argv[2])
    if cmd=='gate': wc=_gate(w); print(json.dumps({'status':'PASS','stage':'GATE','item_index':wc['item_index']},sort_keys=True)); return 0
    if cmd=='research' and len(argv)==4: result=research(w,Path(argv[3]))
    elif cmd=='facts' and len(argv)==4: result=facts(w,Path(argv[3]))
    elif cmd=='context' and len(argv)==5: result=context(w,Path(argv[3]),Path(argv[4]))
    elif cmd=='draft' and len(argv)==4: result=draft(w,Path(argv[3]),False)
    elif cmd=='repair' and len(argv)==4: result=draft(w,Path(argv[3]),True)
    else: raise SystemExit('TESTWORKER_BAD_COMMAND')
    print(json.dumps(result,ensure_ascii=False,sort_keys=True)); return 0

if __name__=='__main__': raise SystemExit(main(sys.argv))
