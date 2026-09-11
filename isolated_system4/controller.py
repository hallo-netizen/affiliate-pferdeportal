from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path
from xml.sax.saxutils import escape

CONTRACT='SYSTEM4_CANONICAL_ARTICLE_STATE_V1'
ALLOWED_ITEM_KEYS={'title','target_keyword','category','article_type','plan_slot'}
FORBIDDEN_CONTROL_KEYS={'route','next_state','workflow','prompt','system_prompt','publish_allowed','rules','ruleset','toolchain'}

class Fail(RuntimeError): pass

def canon(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def sha(v): return hashlib.sha256(canon(v).encode()).hexdigest()
def file_sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def immutable_core(state):
    return {k:state[k] for k in ('contract','source_snapshot_sha256','article')}

def verify_state(state):
    if state.get('contract')!=CONTRACT: raise Fail('STATE_CONTRACT_FAIL')
    if sha(immutable_core(state))!=state.get('immutable_core_sha256'): raise Fail('IMMUTABLE_CORE_TAMPERED')
    if state.get('publish_allowed') is not False: raise Fail('PUBLISH_AUTHORITY_FAIL')

def extract_first_ready(snapshot):
    batch=snapshot.get('next_textmachine_metadata_batch')
    if not isinstance(batch,dict) or batch.get('status')!='READY_FOR_TEXTMACHINE_METADATA_INTAKE': raise Fail('WORDPRESS_READY_BATCH_MISSING')
    items=batch.get('items')
    if not isinstance(items,list) or not items: raise Fail('WORDPRESS_READY_ITEMS_MISSING')
    item=items[0]
    if set(item)!=ALLOWED_ITEM_KEYS: raise Fail('WORDPRESS_ITEM_SCHEMA_FAIL')
    if any(k in item for k in FORBIDDEN_CONTROL_KEYS): raise Fail('EXTERNAL_CONTROL_FIELD_BLOCKED')
    if not all(isinstance(item[k],str) and item[k].strip() for k in ALLOWED_ITEM_KEYS): raise Fail('WORDPRESS_ITEM_VALUE_FAIL')
    return dict(item)

def cmd_ingress(snapshot_path, workspace):
    p=Path(snapshot_path); w=Path(workspace); w.mkdir(parents=True,exist_ok=True)
    if p.suffix.lower()!='.json': raise Fail('WORDPRESS_INPUT_FORMAT_FAIL')
    snap=json.loads(p.read_text(encoding='utf-8'))
    article=extract_first_ready(snap)
    state={
      'contract':CONTRACT,'source_snapshot_sha256':file_sha(p),'article':article,
      'immutable_core_sha256':'','publish_allowed':False,'phase':'RESEARCH_REQUIRED',
      'revision':0,'research':None,'facts':None,'draft_markdown':None,'draft_sha256':None,
      'checks':{},'last_error':None,'released':False
    }
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
    if len(text)<40: raise Fail('RESEARCH_TOO_THIN')
    s['research']={'text':text,'sha256':hashlib.sha256(text.encode()).hexdigest()}; s['phase']='FACT_CHECK_REQUIRED'; save(s,p)
    print('SYSTEM4_RESEARCH_PASS:FACT_CHECK_REQUIRED')

def cmd_facts(workspace,facts_path):
    s,p=load(workspace)
    if s['phase']!='FACT_CHECK_REQUIRED': raise Fail('PHASE_FAIL:FACTS')
    text=Path(facts_path).read_text(encoding='utf-8').strip()
    if len(text)<40: raise Fail('FACTS_TOO_THIN')
    s['facts']={'text':text,'sha256':hashlib.sha256(text.encode()).hexdigest()}; s['phase']='DRAFT_REQUIRED'; save(s,p)
    print('SYSTEM4_FACTS_PASS:DRAFT_REQUIRED')

def cmd_draft(workspace,draft_path):
    s,p=load(workspace)
    if s['phase'] not in ('DRAFT_REQUIRED','REPAIR_REQUIRED'): raise Fail('PHASE_FAIL:DRAFT')
    text=Path(draft_path).read_text(encoding='utf-8').strip()
    if not text: raise Fail('DRAFT_EMPTY')
    s['draft_markdown']=text; s['draft_sha256']=hashlib.sha256(text.encode()).hexdigest(); s['revision']+=1
    s['checks']={}; s['last_error']=None; s['phase']='CHECK_REQUIRED'; save(s,p)
    print(f"SYSTEM4_DRAFT_ACCEPTED:REVISION={s['revision']}:CHECK_REQUIRED")

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
    s['checks']={'status':'FAIL' if errors else 'PASS','errors':errors,'metrics':metrics,'checked_draft_sha256':s['draft_sha256']}
    if errors:
        s['last_error']=errors[0]; s['phase']='REPAIR_REQUIRED'; save(s,p); print('SYSTEM4_CHECK_FAIL:'+errors[0]+':REPAIR_REQUIRED'); return 3
    s['phase']='OUTPUT_GATE_REQUIRED'; save(s,p); print('SYSTEM4_CHECK_PASS:OUTPUT_GATE_REQUIRED'); return 0

def slugify(s):
    s=s.casefold().replace('ä','ae').replace('ö','oe').replace('ü','ue').replace('ß','ss')
    s=re.sub(r'[^a-z0-9]+','-',s).strip('-'); return s[:180] or 'artikel'

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
    if s.get('checks',{}).get('status')!='PASS' or s['checks'].get('checked_draft_sha256')!=s.get('draft_sha256'): raise Fail('CHECK_BINDING_FAIL')
    out=Path(out_dir); out.mkdir(parents=True,exist_ok=True)
    a=s['article']; html=md_to_html(s['draft_markdown'])
    wxr=f'''<?xml version="1.0" encoding="UTF-8" ?>\n<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:wp="http://wordpress.org/export/1.2/">\n<channel><title>System 4 Draft Export</title><wp:wxr_version>1.2</wp:wxr_version>\n<item><title>{escape(a['title'])}</title><content:encoded><![CDATA[{html}]]></content:encoded><wp:post_name>{slugify(a['title'])}</wp:post_name><wp:status>draft</wp:status><wp:post_type>post</wp:post_type><category domain="category" nicename="{escape(a['category'])}"><![CDATA[{a['category']}]]></category></item>\n</channel></rss>\n'''
    wxr_path=out/'wordpress_draft.xml'; wxr_path.write_text(wxr,encoding='utf-8')
    release={'contract':'SYSTEM4_RELEASE_V1','article':a,'draft_sha256':s['draft_sha256'],'state_immutable_core_sha256':s['immutable_core_sha256'],'wordpress_wxr_sha256':file_sha(wxr_path),'publish_allowed':False,'wordpress_status':'draft'}
    release['release_sha256']=sha(release)
    (out/'release.json').write_text(json.dumps(release,ensure_ascii=False,indent=2,sort_keys=True),encoding='utf-8')
    s['phase']='RELEASED'; s['released']=True; save(s,p)
    print('SYSTEM4_RELEASE_PASS:'+release['wordpress_wxr_sha256'])

def main(argv):
    try:
      cmd=argv[1]
      if cmd=='ingress': cmd_ingress(argv[2],argv[3])
      elif cmd=='research': cmd_research(argv[2],argv[3])
      elif cmd=='facts': cmd_facts(argv[2],argv[3])
      elif cmd=='draft': cmd_draft(argv[2],argv[3])
      elif cmd=='check': return cmd_check(argv[2])
      elif cmd=='release': cmd_release(argv[2],argv[3])
      else: raise Fail('BAD_COMMAND')
      return 0
    except (Fail,KeyError,IndexError,json.JSONDecodeError) as e:
      print('SYSTEM4_FAIL:'+str(e)); return 2
if __name__=='__main__': raise SystemExit(main(sys.argv))
