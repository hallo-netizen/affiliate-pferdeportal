from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path
from xml.sax.saxutils import escape

import content_guard
import production_checks
import release_adapter

CONTRACT='SYSTEM4_CANONICAL_ARTICLE_STATE_V1'
ALLOWED_ITEM_KEYS={'title','target_keyword','category','article_type','plan_slot'}
FORBIDDEN_CONTROL_KEYS={'route','next_state','workflow','prompt','system_prompt','publish_allowed','rules','ruleset','toolchain'}

class Fail(RuntimeError): pass

def canon(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def sha(v): return hashlib.sha256(canon(v).encode()).hexdigest()
def file_sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def immutable_core(state):
    return {k:state[k] for k in ('contract','source_snapshot_sha256','batch_sha256','article')}

def verify_state(state):
    if state.get('contract')!=CONTRACT: raise Fail('STATE_CONTRACT_FAIL')
    if sha(immutable_core(state))!=state.get('immutable_core_sha256'): raise Fail('IMMUTABLE_CORE_TAMPERED')
    if state.get('publish_allowed') is not False: raise Fail('PUBLISH_AUTHORITY_FAIL')
    if not re.fullmatch(r'[0-9a-f]{64}',str(state.get('batch_sha256') or '')): raise Fail('BATCH_BINDING_INVALID')
    for field in ('research','facts'):
        value=state.get(field)
        if value is not None:
            if not isinstance(value,dict) or not isinstance(value.get('text'),str) or hashlib.sha256(value['text'].encode()).hexdigest()!=value.get('sha256'):
                raise Fail(field.upper()+'_INTEGRITY_FAIL')
    draft=state.get('draft_markdown')
    if draft is not None and (not isinstance(draft,str) or hashlib.sha256(draft.encode()).hexdigest()!=state.get('draft_sha256')):
        raise Fail('DRAFT_INTEGRITY_FAIL')
    context=state.get('production_context')
    if context is not None:
        if not isinstance(context,dict) or set(context)!={'fact_pack','production_plan_item','sha256'}: raise Fail('PRODUCTION_CONTEXT_SCHEMA_FAIL')
        if sha({'fact_pack':context['fact_pack'],'production_plan_item':context['production_plan_item']})!=context.get('sha256'):
            raise Fail('PRODUCTION_CONTEXT_INTEGRITY_FAIL')
    phase=state.get('phase')
    allowed={'RESEARCH_REQUIRED','FACT_CHECK_REQUIRED','DRAFT_REQUIRED','CHECK_REQUIRED','REPAIR_REQUIRED','OUTPUT_GATE_REQUIRED','SIGNATURE_REQUIRED','RELEASED'}
    if phase not in allowed: raise Fail('PHASE_INVALID')
    if phase=='FACT_CHECK_REQUIRED' and state.get('research') is None: raise Fail('PHASE_STATE_MISMATCH')
    if phase in {'DRAFT_REQUIRED','CHECK_REQUIRED','REPAIR_REQUIRED','OUTPUT_GATE_REQUIRED','SIGNATURE_REQUIRED','RELEASED'} and (state.get('research') is None or state.get('facts') is None): raise Fail('PHASE_STATE_MISMATCH')
    if phase in {'CHECK_REQUIRED','REPAIR_REQUIRED','OUTPUT_GATE_REQUIRED','SIGNATURE_REQUIRED','RELEASED'} and not draft: raise Fail('PHASE_STATE_MISMATCH')
    if phase=='REPAIR_REQUIRED' and (state.get('checks',{}).get('status')!='FAIL' or not state.get('last_error')): raise Fail('PHASE_STATE_MISMATCH')
    if phase in {'OUTPUT_GATE_REQUIRED','SIGNATURE_REQUIRED','RELEASED'} and (state.get('checks',{}).get('status')!='PASS' or state.get('checks',{}).get('checked_draft_sha256')!=state.get('draft_sha256')): raise Fail('PHASE_STATE_MISMATCH')
    if phase=='SIGNATURE_REQUIRED' and not isinstance(state.get('release_prepared'),dict): raise Fail('PHASE_STATE_MISMATCH')
    if phase=='RELEASED' and state.get('released') is not True: raise Fail('PHASE_STATE_MISMATCH')

def extract_ready(snapshot,item_index=0):
    batch=snapshot.get('next_textmachine_metadata_batch')
    if not isinstance(batch,dict) or batch.get('status')!='READY_FOR_TEXTMACHINE_METADATA_INTAKE': raise Fail('WORDPRESS_READY_BATCH_MISSING')
    items=batch.get('items')
    if not isinstance(items,list) or not items: raise Fail('WORDPRESS_READY_ITEMS_MISSING')
    if batch.get('item_count')!=len(items): raise Fail('WORDPRESS_BATCH_COUNT_MISMATCH')
    if batch.get('publish_allowed') is not False: raise Fail('WORDPRESS_PUBLISH_AUTHORITY_FAIL')
    if not isinstance(item_index,int) or isinstance(item_index,bool) or item_index<0 or item_index>=len(items): raise Fail('WORDPRESS_ITEM_INDEX_INVALID')
    item=items[item_index]
    if not isinstance(item,dict) or set(item)!=ALLOWED_ITEM_KEYS: raise Fail('WORDPRESS_ITEM_SCHEMA_FAIL')
    if any(k in item for k in FORBIDDEN_CONTROL_KEYS): raise Fail('EXTERNAL_CONTROL_FIELD_BLOCKED')
    if not all(isinstance(item[k],str) and item[k].strip() for k in ALLOWED_ITEM_KEYS): raise Fail('WORDPRESS_ITEM_VALUE_FAIL')
    batch_sha=str(batch.get('batch_sha256') or '')
    if not re.fullmatch(r'[0-9a-f]{64}',batch_sha): raise Fail('WORDPRESS_BATCH_SHA_FAIL')
    return dict(item),batch_sha

def extract_first_ready(snapshot): return extract_ready(snapshot,0)

def cmd_ingress(snapshot_path, workspace, item_index=0):
    p=Path(snapshot_path); w=Path(workspace); w.mkdir(parents=True,exist_ok=True)
    if p.suffix.lower()!='.json': raise Fail('WORDPRESS_INPUT_FORMAT_FAIL')
    snap=json.loads(p.read_text(encoding='utf-8'))
    article,batch_sha=extract_ready(snap,item_index)
    state={'contract':CONTRACT,'source_snapshot_sha256':file_sha(p),'batch_sha256':batch_sha,'article':article,'immutable_core_sha256':'','publish_allowed':False,'phase':'RESEARCH_REQUIRED','revision':0,'research':None,'facts':None,'production_context':None,'draft_markdown':None,'draft_sha256':None,'checks':{},'last_error':None,'release_prepared':None,'released':False}
    state['immutable_core_sha256']=sha(immutable_core(state))
    (w/'state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2,sort_keys=True),encoding='utf-8')
    print('SYSTEM4_INGRESS_PASS:RESEARCH_REQUIRED')

def load(workspace):
    p=Path(workspace)/'state.json'
    if not p.is_file(): raise Fail('STATE_MISSING')
    s=json.loads(p.read_text(encoding='utf-8')); verify_state(s); return s,p

def save(s,p): verify_state(s); p.write_text(json.dumps(s,ensure_ascii=False,indent=2,sort_keys=True),encoding='utf-8')

def cmd_research(workspace,research_path):
    s,p=load(workspace)
    if s['phase']!='RESEARCH_REQUIRED': raise Fail('PHASE_FAIL:RESEARCH')
    text=Path(research_path).read_text(encoding='utf-8').strip()
    try: content_guard.validate_research_document(text)
    except content_guard.ContentGuardError as e: raise Fail('RESEARCH_EVIDENCE_FAIL:'+str(e)) from e
    s['research']={'text':text,'sha256':hashlib.sha256(text.encode()).hexdigest()}; s['phase']='FACT_CHECK_REQUIRED'; save(s,p)
    print('SYSTEM4_RESEARCH_PASS:FACT_CHECK_REQUIRED')

def cmd_facts(workspace,facts_path):
    s,p=load(workspace)
    if s['phase']!='FACT_CHECK_REQUIRED': raise Fail('PHASE_FAIL:FACTS')
    text=Path(facts_path).read_text(encoding='utf-8').strip()
    try: content_guard.validate_facts_document(text,s['research']['text'])
    except content_guard.ContentGuardError as e: raise Fail('FACTS_EVIDENCE_FAIL:'+str(e)) from e
    s['facts']={'text':text,'sha256':hashlib.sha256(text.encode()).hexdigest()}; s['phase']='DRAFT_REQUIRED'; save(s,p)
    print('SYSTEM4_FACTS_PASS:DRAFT_REQUIRED')

def _read_context_files(fact_pack_path,plan_item_path):
    fact=json.loads(Path(fact_pack_path).read_text(encoding='utf-8'))
    plan=json.loads(Path(plan_item_path).read_text(encoding='utf-8'))
    if not isinstance(fact,dict) or not isinstance(plan,dict): raise Fail('PRODUCTION_CONTEXT_OBJECT_REQUIRED')
    return fact,plan

def cmd_context(workspace,fact_pack_path,plan_item_path):
    s,p=load(workspace)
    if s['phase']!='DRAFT_REQUIRED': raise Fail('PHASE_FAIL:CONTEXT')
    if s.get('production_context') is not None: raise Fail('PRODUCTION_CONTEXT_ALREADY_BOUND')
    fact,plan=_read_context_files(fact_pack_path,plan_item_path)
    try:
        content_guard.validate_fact_pack(fact,s['research']['text'],s['facts']['text'])
        production_checks.validate_bound_context(s,fact,plan)
    except content_guard.ContentGuardError as e:
        raise Fail('PRODUCTION_CONTEXT_FAIL:'+str(e)) from e
    except production_checks.ProductionCheckError as e:
        raise Fail('PRODUCTION_CONTEXT_FAIL:'+str(e)) from e
    s['production_context']={'fact_pack':fact,'production_plan_item':plan,'sha256':sha({'fact_pack':fact,'production_plan_item':plan})}
    save(s,p)
    print('SYSTEM4_PRODUCTION_CONTEXT_PASS:DRAFT_REQUIRED')

def _guard_article_against_context(s,text):
    context=s.get('production_context')
    if not isinstance(context,dict): raise Fail('PRODUCTION_CONTEXT_MISSING')
    try: content_guard.validate_single_article(text,context['fact_pack'])
    except content_guard.ContentGuardError as e: raise Fail('ARTICLE_CONTENT_GUARD_FAIL:'+str(e)) from e

def cmd_draft(workspace,draft_path):
    s,p=load(workspace)
    if s['phase']!='DRAFT_REQUIRED': raise Fail('PHASE_FAIL:DRAFT')
    if s.get('production_context') is None: raise Fail('PRODUCTION_CONTEXT_MISSING')
    text=Path(draft_path).read_text(encoding='utf-8').strip()
    if not text: raise Fail('DRAFT_EMPTY')
    _guard_article_against_context(s,text)
    s['draft_markdown']=text; s['draft_sha256']=hashlib.sha256(text.encode()).hexdigest(); s['revision']+=1
    s['checks']={}; s['last_error']=None; s['release_prepared']=None; s['phase']='CHECK_REQUIRED'; save(s,p)
    print(f"SYSTEM4_DRAFT_ACCEPTED:REVISION={s['revision']}:CHECK_REQUIRED")

def cmd_repair(workspace,draft_path):
    s,p=load(workspace)
    if s['phase']!='REPAIR_REQUIRED': raise Fail('PHASE_FAIL:REPAIR')
    old_context=json.loads(json.dumps(s.get('production_context'),ensure_ascii=False))
    old_research=json.loads(json.dumps(s.get('research'),ensure_ascii=False))
    old_facts=json.loads(json.dumps(s.get('facts'),ensure_ascii=False))
    old_immutable=s.get('immutable_core_sha256')
    if not isinstance(old_context,dict): raise Fail('PRODUCTION_CONTEXT_MISSING')
    old_text=str(s.get('draft_markdown') or '')
    text=Path(draft_path).read_text(encoding='utf-8').strip()
    if not text: raise Fail('DRAFT_EMPTY')
    if text==old_text: raise Fail('REPAIR_DRAFT_UNCHANGED')
    try: content_guard.validate_repair_continuity(old_text,text)
    except content_guard.ContentGuardError as e: raise Fail('REPAIR_SCOPE_FAIL:'+str(e)) from e
    _guard_article_against_context(s,text)
    s['draft_markdown']=text; s['draft_sha256']=hashlib.sha256(text.encode()).hexdigest(); s['revision']+=1
    s['checks']={}; s['last_error']=None; s['release_prepared']=None; s['phase']='CHECK_REQUIRED'
    if s.get('production_context')!=old_context: raise Fail('REPAIR_CONTEXT_MUTATION_FORBIDDEN')
    if s.get('research')!=old_research or s.get('facts')!=old_facts: raise Fail('REPAIR_EVIDENCE_MUTATION_FORBIDDEN')
    if s.get('immutable_core_sha256')!=old_immutable: raise Fail('REPAIR_IMMUTABLE_CORE_MUTATION_FORBIDDEN')
    save(s,p)
    print(f"SYSTEM4_REPAIR_ACCEPTED:REVISION={s['revision']}:CHECK_REQUIRED")

def run_checks(s):
    text=s.get('draft_markdown') or ''; a=s['article']; errors=[]
    lines=[x.strip() for x in text.splitlines() if x.strip()]
    if not lines or lines[0] != '# '+a['title']: errors.append('TITLE_BINDING_FAIL')
    if a['target_keyword'].casefold() not in text.casefold(): errors.append('TARGET_KEYWORD_MISSING')
    if sum(1 for x in text.splitlines() if x.startswith('## '))<2: errors.append('STRUCTURE_H2_FAIL')
    words=re.findall(r'\b[\wÄÖÜäöüß-]+\b',text,re.UNICODE)
    if len(words)<250: errors.append('QUALITY_LENGTH_FAIL')
    if '<script' in text.casefold() or 'javascript:' in text.casefold(): errors.append('UNSAFE_HTML_FAIL')
    return errors, {'word_count':len(words),'h2_count':sum(1 for x in text.splitlines() if x.startswith('## '))}

def cmd_check(workspace):
    s,p=load(workspace)
    if s['phase']!='CHECK_REQUIRED': raise Fail('PHASE_FAIL:CHECK')
    errors,metrics=run_checks(s)
    s['checks']={'status':'FAIL' if errors else 'PASS','mode':'BASIC_ARCHITECTURE','errors':errors,'metrics':metrics,'checked_draft_sha256':s['draft_sha256']}
    if errors:
        s['last_error']=errors[0]; s['phase']='REPAIR_REQUIRED'; save(s,p); print('SYSTEM4_CHECK_FAIL:'+errors[0]+':REPAIR_REQUIRED'); return 3
    s['phase']='OUTPUT_GATE_REQUIRED'; save(s,p); print('SYSTEM4_CHECK_PASS:OUTPUT_GATE_REQUIRED'); return 0

def cmd_fullcheck(workspace):
    s,p=load(workspace)
    if s['phase']!='CHECK_REQUIRED': raise Fail('PHASE_FAIL:FULLCHECK')
    context=s.get('production_context')
    if not isinstance(context,dict): raise Fail('PRODUCTION_CONTEXT_MISSING')
    try: content_guard.validate_single_article(str(s.get('draft_markdown') or ''),context['fact_pack'])
    except content_guard.ContentGuardError as e: raise Fail('FULL_CHECK_HARD_BLOCK:CONTENT_GUARD:'+str(e)) from e
    repo=Path(__file__).resolve().parent.parent
    try:
        result=production_checks.run_all(repo,s,context['fact_pack'],context['production_plan_item'])
    except production_checks.RepairRequired as e:
        findings=e.findings
        code=str(findings[0].get('error_code') or e.checker) if findings else e.checker
        error='FULL:'+e.checker+':'+code
        s['checks']={'status':'FAIL','mode':'FULL_PRODUCTION','errors':[error],'findings':findings,'checker':e.checker,'checked_draft_sha256':s['draft_sha256']}
        s['last_error']=error; s['phase']='REPAIR_REQUIRED'; save(s,p)
        print('SYSTEM4_FULL_CHECK_FAIL:'+error+':REPAIR_REQUIRED'); return 3
    except production_checks.ProductionCheckError as e:
        raise Fail('FULL_CHECK_HARD_BLOCK:'+str(e)) from e
    s['checks']={'status':'PASS','mode':'FULL_PRODUCTION','errors':[],'checked_draft_sha256':s['draft_sha256'],'production_evidence':result}
    s['last_error']=None; s['phase']='OUTPUT_GATE_REQUIRED'; save(s,p)
    print('SYSTEM4_FULL_CHECK_PASS:OUTPUT_GATE_REQUIRED'); return 0

def slugify(s):
    s=s.casefold().replace('ä','ae').replace('ö','oe').replace('ü','ue').replace('ß','ss'); s=re.sub(r'[^a-z0-9]+','-',s).strip('-'); return s[:180] or 'artikel'

def md_to_html(md):
    out=[]
    for block in re.split(r'\n\s*\n',md.strip()):
        lines=block.splitlines(); first=lines[0].strip()
        if first.startswith('# '): continue
        if first.startswith('## '): out.append('<h2>'+escape(first[3:])+'</h2>'); rest=' '.join(x.strip() for x in lines[1:] if x.strip())
        else: rest=' '.join(x.strip() for x in lines if x.strip())
        if rest: out.append('<p>'+escape(rest)+'</p>')
    return '\n'.join(out)

def cmd_release(workspace,out_dir):
    s,p=load(workspace)
    if s['phase']!='OUTPUT_GATE_REQUIRED': raise Fail('OUTPUT_GATE_CLOSED')
    if s.get('checks',{}).get('mode')!='BASIC_ARCHITECTURE': raise Fail('BASIC_RELEASE_FOR_FULL_PRODUCTION_FORBIDDEN')
    if s.get('checks',{}).get('status')!='PASS' or s['checks'].get('checked_draft_sha256')!=s.get('draft_sha256'): raise Fail('CHECK_BINDING_FAIL')
    out=Path(out_dir); out.mkdir(parents=True,exist_ok=True); a=s['article']; html=md_to_html(s['draft_markdown'])
    wxr=f'''<?xml version="1.0" encoding="UTF-8" ?>\n<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:wp="http://wordpress.org/export/1.2/">\n<channel><title>System 4 Draft Export</title><wp:wxr_version>1.2</wp:wxr_version>\n<item><title>{escape(a['title'])}</title><content:encoded><![CDATA[{html}]]></content:encoded><wp:post_name>{slugify(a['title'])}</wp:post_name><wp:status>draft</wp:status><wp:post_type>post</wp:post_type><category domain="category" nicename="{escape(a['category'])}"><![CDATA[{a['category']}]]></category></item>\n</channel></rss>\n'''
    wxr_path=out/'wordpress_draft.xml'; wxr_path.write_text(wxr,encoding='utf-8')
    release={'contract':'SYSTEM4_RELEASE_V1','article':a,'draft_sha256':s['draft_sha256'],'state_immutable_core_sha256':s['immutable_core_sha256'],'wordpress_wxr_sha256':file_sha(wxr_path),'publish_allowed':False,'wordpress_status':'draft'}; release['release_sha256']=sha(release)
    (out/'release.json').write_text(json.dumps(release,ensure_ascii=False,indent=2,sort_keys=True),encoding='utf-8'); s['phase']='RELEASED'; s['released']=True; save(s,p); print('SYSTEM4_RELEASE_PASS:'+release['wordpress_wxr_sha256'])

def cmd_prepare_release(workspace,out_dir):
    s,p=load(workspace)
    if s['phase']!='OUTPUT_GATE_REQUIRED': raise Fail('OUTPUT_GATE_CLOSED')
    if s.get('checks',{}).get('mode')!='FULL_PRODUCTION': raise Fail('FULL_PRODUCTION_CHECK_PASS_REQUIRED')
    try: prepared=release_adapter.build_unsigned(s,Path(out_dir))
    except release_adapter.ReleaseError as e: raise Fail('ENDSTEMPEL_PREPARE_FAIL:'+str(e)) from e
    s['release_prepared']=prepared; s['phase']='SIGNATURE_REQUIRED'; save(s,p); print('SYSTEM4_ENDSTEMPEL_SIGNATURE_REQUIRED:'+prepared['manifest_sha256'])

def cmd_finalize_signed(workspace,signature_path,final_path):
    s,p=load(workspace)
    if s['phase']!='SIGNATURE_REQUIRED': raise Fail('SIGNATURE_PHASE_REQUIRED')
    signature=json.loads(Path(signature_path).read_text(encoding='utf-8'))
    if not isinstance(signature,dict): raise Fail('SIGNATURE_OBJECT_REQUIRED')
    try: result=release_adapter.finalize_signed(s['release_prepared'],signature,Path(final_path))
    except release_adapter.ReleaseError as e: raise Fail('ENDSTEMPEL_FINALIZE_FAIL:'+str(e)) from e
    s['phase']='RELEASED'; s['released']=True; s['release_final']=result; save(s,p); print('SYSTEM4_WORDPRESS_SIGNED_JSON_READY:'+result['final_sha256'])

def main(argv):
    try:
      cmd=argv[1]
      if cmd=='ingress': cmd_ingress(argv[2],argv[3],int(argv[4]) if len(argv)>4 else 0)
      elif cmd=='research': cmd_research(argv[2],argv[3])
      elif cmd=='facts': cmd_facts(argv[2],argv[3])
      elif cmd=='context': cmd_context(argv[2],argv[3],argv[4])
      elif cmd=='draft': cmd_draft(argv[2],argv[3])
      elif cmd=='repair': cmd_repair(argv[2],argv[3])
      elif cmd=='check': return cmd_check(argv[2])
      elif cmd=='fullcheck': return cmd_fullcheck(argv[2])
      elif cmd=='release': cmd_release(argv[2],argv[3])
      elif cmd=='prepare-release': cmd_prepare_release(argv[2],argv[3])
      elif cmd=='finalize-signed': cmd_finalize_signed(argv[2],argv[3],argv[4])
      elif cmd=='verify': load(argv[2]); print('SYSTEM4_STATE_VERIFY_PASS')
      else: raise Fail('BAD_COMMAND')
      return 0
    except (Fail,KeyError,IndexError,ValueError,json.JSONDecodeError) as e:
      print('SYSTEM4_FAIL:'+str(e)); return 2
if __name__=='__main__': raise SystemExit(main(sys.argv))
