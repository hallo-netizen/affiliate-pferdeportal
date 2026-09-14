from __future__ import annotations
import copy,hashlib,json,subprocess,sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
sys.path.insert(0,str(HERE))
import authoring_contract,controller,point0_snapshot,root_entry,supervisor

LIVE=HERE/'live_fixture/wordpress_snapshot.json'

def h(text:str)->str:return hashlib.sha256(text.encode()).hexdigest()
def canon(v)->bytes:return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write_json(path:Path,value:dict)->Path:path.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True),encoding='utf-8');return path
def head()->str:return subprocess.run(['git','rev-parse','HEAD'],cwd=REPO,text=True,capture_output=True,check=True).stdout.strip()
def word_token(n:int)->str:
 words=('Auswahl','Material','Nutzung','Pflege','Sicherheit','Komfort','Eignung','Praxis','Vergleich','Haltung','Training','Stall','Weide','Reitplatz','Pferd','Anwendung')
 return words[n%len(words)]

def production_snapshot_bytes(batch_size:int|None=None)->bytes:
 value=json.loads(LIVE.read_text(encoding='utf-8'))
 if batch_size is not None:
  batch=value['next_textmachine_metadata_batch'];items=list(batch['items'])
  if batch_size<1 or batch_size>len(items):raise AssertionError('TEST_BATCH_SIZE_INVALID')
  batch['items']=items[:batch_size];batch['item_count']=batch_size
  material={key:copy.deepcopy(val) for key,val in batch.items() if key!='batch_sha256'}
  batch['batch_sha256']=hashlib.sha256(canon(material)).hexdigest()
 value['system4_root_manifest_sha256']=root_entry._critical_manifest_sha256();return canon(value)

def source_and_claims(index:int,target_keyword:str):
 shared=(f'{target_keyword} Auswahl Material Nutzung Pflege Sicherheit Komfort Eignung Praxis Vergleich Prüfung Eigenschaft Voraussetzung Entscheidung Anwendung Kriterium gebundener Wert Abschnitt Haltung Training Stall Weide Reitplatz Pferd')
 chunks=[
  f'{shared}. Die Auswahl berücksichtigt Material, Sicherheit, Eignung und die praktische Nutzung.',
  f'{shared}. Die Nutzung berücksichtigt Pflege, Komfort, Anwendung und eine nachvollziehbare Entscheidung.',
  f'{shared}. Der Vergleich berücksichtigt Eigenschaften, Voraussetzungen, Praxis und geeignete Kriterien.',
 ]
 evidence='\n'.join(chunks);sid=f'src-live-route-{index}'
 src={'source_id':sid,'source_title':f'Gebundene Fachquelle Live Route {index}','source_url':f'https://example.org/live-route/source-{index}','retrieved_at':'2026-09-14T00:00:00Z','evidence':evidence,'snapshot_sha256':h(evidence),'http_status':200,'source_kind':'TEST_BOUND_HTTP_CONTRACT'}
 facts=[]
 for n,text in enumerate(chunks):
  facts.append({'fact_id':f'fact-live-{index}-{n}','source_id':sid,'statement':text,'evidence_text':text,'evidence_text_sha256':h(text)})
 return src,facts

def start_to_context(base:Path,index:int,batch_size:int|None=None):
 raw=production_snapshot_bytes(batch_size);snapshot=base/'production-snapshot.json';snapshot.write_bytes(raw)
 metadata=json.loads(raw.decode('utf-8'))['next_textmachine_metadata_batch']['items'][index]
 src,claims=source_and_claims(index,metadata['target_keyword'])
 p0=point0_snapshot.build(production_snapshot_bytes=raw,root_manifest_sha256=root_entry._critical_manifest_sha256(),head_sha=head(),research_provider='SYSTEM4_TEST_BOUND_SOURCE_PROVIDER',sources=[src])
 p0p=base/f'point0-{index}.json';p0p.write_bytes(point0_snapshot.canon(p0));workspace=base/f'item-{index}'
 rc=root_entry.main(['root_entry.py','start-point0',str(p0p),str(workspace),str(index)])
 if rc!=0:raise AssertionError('ROOT_POINT0_FAILED:'+str(index))
 research=supervisor.expected_research_document(workspace);rp=write_json(base/f'research-{index}.json',research)
 if controller.main(['controller.py','research',str(workspace),str(rp)])!=0:raise AssertionError('RESEARCH_FAILED:'+str(index))
 facts_doc={'contract':'SYSTEM4_FACTS_EVIDENCE_V1','claims':copy.deepcopy(claims)};fp=write_json(base/f'facts-{index}.json',facts_doc)
 if controller.main(['controller.py','facts',str(workspace),str(fp)])!=0:raise AssertionError('FACTS_FAILED:'+str(index))
 state=json.loads((workspace/'state.json').read_text(encoding='utf-8'));source_sha=state['source_snapshot_sha256']
 pack_claims=[]
 for row in claims:
  enriched=copy.deepcopy(row);enriched['claim_status']='FULLY_SUPPORTED';enriched['article_types']=[state['article']['article_type']];pack_claims.append(enriched)
 pack={'contract':'canonical_fact_pack_v1','status':'SOURCE_VERIFIED_PRODUCTION_READY','source_snapshot_id':source_sha,'fact_pack_id':source_sha,'sources':copy.deepcopy(research['sources']),'claims':pack_claims}
 ids=[row['fact_id'] for row in claims];a=state['article']
 plan={'article_type':a['article_type'],'target_keyword':a['target_keyword'],'topic':a['title'],'source_snapshot_id':source_sha,'runtime_order':{'order_id':f'live-route-{index}','article_type':a['article_type'],'title':a['title'],'slug':f'live-route-{index}','subject_scope':'live_route_test','subject_label':a['target_keyword'],'lead':'Gebundener Einstieg mit konkreter Aussage für den Artikel.','conclusion':'Gebundener Abschluss mit konkreter Aussage für den Artikel.','allowed_fact_ids':ids}}
 pp=write_json(base/f'pack-{index}.json',pack);pl=write_json(base/f'plan-{index}.json',plan)
 if controller.main(['controller.py','context',str(workspace),str(pp),str(pl)])!=0:raise AssertionError('CONTEXT_FAILED:'+str(index))
 state=json.loads((workspace/'state.json').read_text(encoding='utf-8'))
 if state['phase']!='DRAFT_REQUIRED':raise AssertionError('DRAFT_REQUIRED_NOT_REACHED')
 return workspace,snapshot,state

def valid_article(state:dict,index:int,variant:str='basis')->str:
 c=state['authoring_contract'];identity=c['article_identity'];g=c['global_requirements'];s=c['structure_requirements'];t=c['type_requirements'];b=c['bound_requirements'];allowed=list(b['allowed_fact_ids']);fid=allowed[0]
 claims=state.get('production_context',{}).get('fact_pack',{}).get('claims',[])
 claim_map={str(row.get('fact_id') or ''):str(row.get('statement') or '').strip() for row in claims if isinstance(row,dict)}
 if any(not claim_map.get(fact_id) for fact_id in allowed):raise AssertionError('BOUND_FACT_STATEMENT_MISSING')
 def fact_stem(fact_id:str)->str:return claim_map[fact_id].rstrip(' .!?')
 def bound_sentence(fact_id:str,seed:int)->str:
  a=word_token(seed);d=word_token(seed+5)
  return f'Nach der gebundenen Quelle gilt: {fact_stem(fact_id)}; diese Aussage wird für {a} und {d} im Zusammenhang mit {identity["target_keyword"]} eingeordnet.'
 min_words=int(g.get('min_words') or 0);min_paragraphs=int(g.get('min_paragraphs') or 0);min_h2=int(g.get('min_h2') or 0);intro=s.get('intro') if isinstance(s.get('intro'),dict) else {};intro_name=str(intro.get('required_block') or 'intro')
 intent_terms=[str(x).strip() for x in b.get('intent_terms',[]) if str(x).strip()]
 if not intent_terms:raise AssertionError('BOUND_INTENT_TERMS_MISSING')
 required=list(t.get('required_blocks') or []);blocks=[]
 ilo=max(int(intro.get('minimum_words') or 1),20);ihi=int(intro.get('maximum_words') or max(ilo,200));intro_text=bound_sentence(fid,1)
 intro_words=intro_text.split()
 if len(intro_words)<ilo:intro_text+=' '+f'{identity["target_keyword"]} wird dabei nach Auswahl, Material, Nutzung, Sicherheit, Pflege und Eignung sachlich eingeordnet.'
 if len(intro_text.split())>ihi:intro_text=' '.join(intro_text.split()[:ihi])
 blocks.append(f'<section data-block="{intro_name}"><p data-fact-ids="{fid}">{intro_text}</p></section>')
 other=[x for x in required if x!=intro_name]
 while len(other)<max(min_h2,2):other.append(f'content_{len(other)+1}')
 target_paras=max(min_paragraphs-1,len(other)*2,4);target_words=max(min_words-len(intro_text.split()),400);paras_per=max(2,(target_paras+len(other)-1)//len(other));words_per=max(45,(target_words+len(other)*paras_per-1)//(len(other)*paras_per))
 link_rows=[row for row in b.get('link_bindings',[]) if isinstance(row,dict) and row.get('active') is not False]
 expected_link_blocks=[str(row.get('section_id') or '') for row in link_rows]
 missing_link_blocks=[name for name in expected_link_blocks if name not in other]
 if missing_link_blocks:raise AssertionError('BOUND_LINK_SECTION_MISSING:'+','.join(missing_link_blocks))
 heading_suffixes=('sicher auswählen','Material sinnvoll vergleichen','Nutzung praktisch einordnen','Pflege passend planen','Sicherheit gezielt prüfen','Entscheidung nachvollziehbar treffen','Eignung im Alltag bewerten','Anwendung sinnvoll abstimmen')
 for bi,name in enumerate(other):
  intent=intent_terms[bi%len(intent_terms)];heading=f'{intent} {heading_suffixes[bi%len(heading_suffixes)]}'
  parts=[f'<h2>{heading}</h2>']
  section_links=[row for row in link_rows if str(row.get('section_id') or '')==name]
  for pi in range(paras_per):
   fact_id=allowed[(bi+pi)%len(allowed)];seed=10+bi*paras_per+pi;text=bound_sentence(fact_id,seed)
   extra_seed=seed+7
   while len(text.split())<words_per:
    text+=f' Für {word_token(extra_seed)} und {word_token(extra_seed+3)} bleibt die gebundene Aussage maßgeblich, ohne ihren Inhalt zu erweitern.';extra_seed+=2
   if pi==0:
    for row in section_links:text+=f' <a href="{row["href"]}">{row["anchor"]}</a>'
   parts.append(f'<p data-fact-ids="{fact_id}">{text}</p>')
  blocks.append(f'<section data-block="{name}">'+''.join(parts)+'</section>')
 if sum(1 for name in other for row in link_rows if str(row.get('section_id') or '')==name)!=len(link_rows):raise AssertionError('BOUND_LINK_NOT_PLACED_EXACTLY_ONCE')
 if len(blocks)>1:
  list_rows=[]
  for n in range(4):
   fact_id=allowed[n%len(allowed)];list_rows.append(f'<li data-fact-ids="{fact_id}">{bound_sentence(fact_id,40+n)}</li>')
  blocks[1]=blocks[1].replace('</section>','<ul>'+''.join(list_rows)+'</ul></section>',1)
 table_count=int(t.get('table_count_exact') or 0)
 if table_count:
  if table_count!=1:raise AssertionError('SYNTHETIC_TABLE_COUNT_NOT_SUPPORTED')
  table_positions=[i for i,name in enumerate(other,start=1) if name=='table']
  if len(table_positions)!=1:raise AssertionError('BOUND_TABLE_BLOCK_MISSING_OR_DUPLICATE')
  rows=max(int(g.get('min_table_body_rows') or 1),4);body=[]
  for r in range(rows):
   fact=allowed[r%len(allowed)]
   body.append(f'<tr><td data-fact-ids="{fact}">{bound_sentence(fact,60+r*3)}</td><td data-fact-ids="{fact}">{bound_sentence(fact,61+r*3)}</td><td data-fact-ids="{fact}">{bound_sentence(fact,62+r*3)}</td></tr>')
  table=(f'<table class="system-129-table comparison-table"><thead><tr>'
         f'<th data-fact-ids="{fid}">{identity["target_keyword"]} Auswahlmerkmal</th>'
         f'<th data-fact-ids="{fid}">{identity["target_keyword"]} praktische Einordnung</th>'
         f'<th data-fact-ids="{fid}">{identity["target_keyword"]} Entscheidungshinweis</th>'
         f'</tr></thead><tbody>'+''.join(body)+'</tbody></table>')
  pos=table_positions[0];blocks[pos]=blocks[pos].replace('</section>',table+'</section>',1)
 traces=''
 if t.get('fact_trace_required') is True:
  need=max(int(b.get('source_trace_minimum') or 0),1)
  for fact_id in allowed[:need]:
   meta=b['fact_authority'][fact_id];traces+=f'<span class="ppm-source-trace" data-fact-id="{fact_id}" data-source-title="{meta["source_id"]}" data-source-hash="{meta["evidence_text_sha256"]}"></span>'
  blocks[0]=blocks[0].replace('</p>',traces+'</p>',1)
 classes=' '.join(c['system4_guards']['design']['required_root_classes']);article=f'<article class="{classes}" data-article-type="{identity["article_type"]}">'+''.join(blocks)+'</article>'
 authoring_contract.validate_candidate(article,c)
 return article
