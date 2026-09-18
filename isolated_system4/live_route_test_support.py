from __future__ import annotations
import copy,hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parent;sys.path.insert(0,str(HERE))
import authoring_contract,block_semantics,controller,point0_snapshot,root_entry,supervisor
LIVE=HERE/'live_fixture/wordpress_snapshot.json'
def h(text:str)->str:return hashlib.sha256(text.encode()).hexdigest()
def canon(v)->bytes:return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write_json(path:Path,value:dict)->Path:path.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True),encoding='utf-8');return path
def head()->str:return subprocess.run(['git','rev-parse','HEAD'],cwd=REPO,text=True,capture_output=True,check=True).stdout.strip()
def word_token(n:int)->str:
 words=('Auswahl','Material','Nutzung','Pflege','Sicherheit','Komfort','Eignung','Praxis','Vergleich','Haltung','Training','Stall','Weide','Reitplatz','Pferd','Anwendung','Entscheidung','Kontrolle','Ausstattung','Planung','Untergrund','Lagerung','Beleuchtung','Hindernis');return words[n%len(words)]
def production_snapshot_bytes(batch_size:int|None=None)->bytes:
 value=json.loads(LIVE.read_text(encoding='utf-8'))
 if batch_size is not None:
  batch=value['next_textmachine_metadata_batch'];items=list(batch['items'])
  if batch_size<1 or batch_size>len(items):raise AssertionError('TEST_BATCH_SIZE_INVALID')
  batch['items']=items[:batch_size];batch['item_count']=batch_size;material={k:copy.deepcopy(v) for k,v in batch.items() if k!='batch_sha256'};batch['batch_sha256']=hashlib.sha256(canon(material)).hexdigest()
 value['system4_root_manifest_sha256']=root_entry._critical_manifest_sha256();return canon(value)
def source_and_claims(index:int,target_keyword:str):
 vocab=' '.join(word_token(index*5+n) for n in range(8));chunks=[f'{target_keyword}: {vocab}. Die Auswahl berücksichtigt Material, Sicherheit, Eignung und die praktische Nutzung.',f'{target_keyword}: {vocab}. Die Nutzung berücksichtigt Pflege, Komfort, Anwendung und eine nachvollziehbare Entscheidung.',f'{target_keyword}: {vocab}. Der Vergleich berücksichtigt Eigenschaften, Voraussetzungen, Praxis und geeignete Kriterien.'];evidence='\n'.join(chunks);sid=f'src-live-route-{index}'
 src={'source_id':sid,'source_title':f'Gebundene Fachquelle Live Route {index}','source_url':f'https://example.org/live-route/source-{index}','retrieved_at':'2026-09-14T00:00:00Z','evidence':evidence,'snapshot_sha256':h(evidence),'http_status':200,'source_kind':'TEST_BOUND_HTTP_CONTRACT'}
 return src,[{'fact_id':f'fact-live-{index}-{n}','source_id':sid,'statement':text,'evidence_text':text,'evidence_text_sha256':h(text)} for n,text in enumerate(chunks)]
def start_to_context(base:Path,index:int,batch_size:int|None=None):
 raw=production_snapshot_bytes(batch_size);snapshot=base/'production-snapshot.json';snapshot.write_bytes(raw);metadata=json.loads(raw.decode())['next_textmachine_metadata_batch']['items'][index];src,claims=source_and_claims(index,metadata['target_keyword']);p0=point0_snapshot.build(production_snapshot_bytes=raw,root_manifest_sha256=root_entry._critical_manifest_sha256(),head_sha=head(),research_provider='SYSTEM4_TEST_BOUND_SOURCE_PROVIDER',sources=[src]);p0p=base/f'point0-{index}.json';p0p.write_bytes(point0_snapshot.canon(p0));workspace=base/f'item-{index}'
 if root_entry.main(['root_entry.py','start-point0',str(p0p),str(workspace),str(index)])!=0:raise AssertionError('ROOT_POINT0_FAILED:'+str(index))
 research=supervisor.expected_research_document(workspace);rp=write_json(base/f'research-{index}.json',research)
 if controller.main(['controller.py','research',str(workspace),str(rp)])!=0:raise AssertionError('RESEARCH_FAILED:'+str(index))
 fp=write_json(base/f'facts-{index}.json',{'contract':'SYSTEM4_FACTS_EVIDENCE_V1','claims':copy.deepcopy(claims)})
 if controller.main(['controller.py','facts',str(workspace),str(fp)])!=0:raise AssertionError('FACTS_FAILED:'+str(index))
 state=json.loads((workspace/'state.json').read_text());source_sha=state['source_snapshot_sha256'];pack_claims=[]
 for row in claims:
  x=copy.deepcopy(row);x['claim_status']='FULLY_SUPPORTED';x['article_types']=[state['article']['article_type']];pack_claims.append(x)
 pack={'contract':'canonical_fact_pack_v1','status':'SOURCE_VERIFIED_PRODUCTION_READY','source_snapshot_id':source_sha,'fact_pack_id':source_sha,'sources':copy.deepcopy(research['sources']),'claims':pack_claims};ids=[r['fact_id'] for r in claims];a=state['article'];plan={'article_type':a['article_type'],'target_keyword':a['target_keyword'],'topic':a['title'],'source_snapshot_id':source_sha,'runtime_order':{'order_id':f'live-route-{index}','article_type':a['article_type'],'title':a['title'],'slug':f'live-route-{index}','subject_scope':'live_route_test','subject_label':a['target_keyword'],'lead':'Gebundener Einstieg mit konkreter Aussage für den Artikel.','conclusion':'Gebundener Abschluss mit konkreter Aussage für den Artikel.','allowed_fact_ids':ids}}
 pp=write_json(base/f'pack-{index}.json',pack);pl=write_json(base/f'plan-{index}.json',plan)
 if controller.main(['controller.py','context',str(workspace),str(pp),str(pl)])!=0:raise AssertionError('CONTEXT_FAILED:'+str(index))
 state=json.loads((workspace/'state.json').read_text());
 if state['phase']!='DRAFT_REQUIRED':raise AssertionError('DRAFT_REQUIRED_NOT_REACHED')
 return workspace,snapshot,state
def valid_article(state:dict,index:int,variant:str='basis')->str:
 c=state['authoring_contract'];identity=c['article_identity'];g=c['global_requirements'];s=c['structure_requirements'];t=c['type_requirements'];b=c['bound_requirements'];allowed=list(b['allowed_fact_ids']);fid=allowed[0];claims=state.get('production_context',{}).get('fact_pack',{}).get('claims',[]);claim_map={str(r.get('fact_id') or ''):str(r.get('statement') or '').strip() for r in claims if isinstance(r,dict)}
 if any(not claim_map.get(x) for x in allowed):raise AssertionError('BOUND_FACT_STATEMENT_MISSING')
 def fact_stem(x):return claim_map[x].rstrip(' .!?')
 templates=('Aus der gebundenen Quelle folgt: {fact}. Für {a} und {d} wird diese Aussage beim Thema {kw} sachlich eingeordnet.','Für {kw} ist gebunden: {fact}. Die Einordnung verbindet diesen Beleg mit {a} sowie {d}.','Der Quellenbeleg zu {kw} lautet: {fact}. Daraus werden ausschließlich {a} und {d} als Einordnungsrahmen verwendet.','Beim Thema {kw} gilt nach der gebundenen Quelle: {fact}. Der Bezug zu {a} und {d} erweitert den Beleg nicht.','Gebunden für {kw} ist folgende Aussage: {fact}. Sie wird im Zusammenhang von {a} und {d} betrachtet.','Die Quelle bindet für {kw}: {fact}. Für die Darstellung dienen {a} und {d} nur als sachlicher Rahmen.','Für den Artikel zu {kw} ist belegt: {fact}. Die Begriffe {a} und {d} strukturieren lediglich die Einordnung.')
 def sent(fact,seed):return templates[index%len(templates)].format(fact=fact_stem(fact),a=word_token(seed+index*3),d=word_token(seed+index*3+7),kw=identity['target_keyword'])
 min_words=int(g.get('min_words') or 0);min_paras=int(g.get('min_paragraphs') or 0);min_h2=int(g.get('min_h2') or 0);intro=s.get('intro') if isinstance(s.get('intro'),dict) else {};intro_name=str(intro.get('required_block') or 'intro');terms=[str(x).strip() for x in b.get('intent_terms',[]) if str(x).strip()]
 if not terms:raise AssertionError('BOUND_INTENT_TERMS_MISSING')
 ilo=max(int(intro.get('minimum_words') or 1),20);ihi=int(intro.get('maximum_words') or 200);intro_text=sent(fid,1)+(' Die Formulierung entspricht der gebundenen Ausgangsfassung.' if variant=='basis' else ' Die Formulierung wurde sprachlich korrigiert.')
 if len(intro_text.split())<ilo:intro_text+=f' {identity["target_keyword"]} wird nach Auswahl, Material, Nutzung, Sicherheit, Pflege und Eignung sachlich eingeordnet.'
 if len(intro_text.split())>ihi:intro_text=' '.join(intro_text.split()[:ihi])
 blocks=[f'<section data-block="{intro_name}"><p data-fact-ids="{fid}">{intro_text}</p></section>'];other=[x for x in list(t.get('required_blocks') or []) if x!=intro_name]
 while len(other)<max(min_h2,2):other.append(f'content_{len(other)+1}')
 target_paras=max(min_paras-1,len(other)*2,4);target_words=max(min_words-len(intro_text.split()),400);paras_per=max(2,(target_paras+len(other)-1)//len(other));words_per=max(45,(target_words+len(other)*paras_per-1)//(len(other)*paras_per));links=[r for r in b.get('link_bindings',[]) if isinstance(r,dict) and r.get('active') is not False]
 missing=[str(r.get('section_id') or '') for r in links if str(r.get('section_id') or '') not in other]
 if missing:raise AssertionError('BOUND_LINK_SECTION_MISSING:'+','.join(missing))
 suffix=('sicher auswählen','Material sinnvoll vergleichen','Nutzung praktisch einordnen','Pflege passend planen','Sicherheit gezielt prüfen','Entscheidung nachvollziehbar treffen','Eignung im Alltag bewerten','Anwendung sinnvoll abstimmen')
 for bi,name in enumerate(other):
  semantic_heading=block_semantics.canonical_heading(c,name)
  heading=semantic_heading or f'{terms[bi%len(terms)]} {suffix[(bi+index)%len(suffix)]}'
  parts=[f'<h2>{heading}</h2>'];section_links=[r for r in links if str(r.get('section_id') or '')==name]
  for pi in range(paras_per):
   fact=allowed[(bi+pi)%len(allowed)];seed=10+bi*paras_per+pi;text=sent(fact,seed);extra=seed+11
   while len(text.split())<words_per:
    text+=f' Bei {identity["target_keyword"]} bleibt im Bereich {word_token(extra+index)} derselbe Quellenbeleg maßgeblich; {word_token(extra+5+index)} beschreibt nur die Einordnung.';extra+=3
   if pi==0:
    for r in section_links:text+=f' <a href="{r["href"]}">{r["anchor"]}</a>'
   parts.append(f'<p data-fact-ids="{fact}">{text}</p>')
  blocks.append(f'<section data-block="{name}">'+''.join(parts)+'</section>')
 if len(blocks)>1:
  lis=[]
  for n in range(4):
   fact=allowed[n%len(allowed)];lis.append(f'<li data-fact-ids="{fact}">{sent(fact,40+n*2)}</li>')
  blocks[1]=blocks[1].replace('</section>','<ul>'+''.join(lis)+'</ul></section>',1)
 if int(t.get('table_count_exact') or 0):
  positions=[i for i,name in enumerate(other,start=1) if name=='table']
  if len(positions)!=1:raise AssertionError('BOUND_TABLE_BLOCK_MISSING_OR_DUPLICATE')
  rows=[]
  for r in range(max(int(g.get('min_table_body_rows') or 1),4)):
   fact=allowed[r%len(allowed)];rows.append(f'<tr><td data-fact-ids="{fact}">{sent(fact,60+r*5)}</td><td data-fact-ids="{fact}">{sent(fact,61+r*5)}</td><td data-fact-ids="{fact}">{sent(fact,62+r*5)}</td></tr>')
  table=f'<table class="system-129-table comparison-table"><thead><tr><th data-fact-ids="{fid}">{identity["target_keyword"]} Auswahlmerkmal</th><th data-fact-ids="{fid}">{identity["target_keyword"]} praktische Einordnung</th><th data-fact-ids="{fid}">{identity["target_keyword"]} Entscheidungshinweis</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table>';blocks[positions[0]]=blocks[positions[0]].replace('</section>',table+'</section>',1)
 if t.get('fact_trace_required') is True:
  traces=''
  for fact in allowed[:max(int(b.get('source_trace_minimum') or 0),1)]:
   m=b['fact_authority'][fact];traces+=f'<span class="ppm-source-trace" data-fact-id="{fact}" data-source-title="{m["source_id"]}" data-source-hash="{m["evidence_text_sha256"]}"></span>'
  blocks[0]=blocks[0].replace('</p>',traces+'</p>',1)
 article=f'<article class="{" ".join(c["system4_guards"]["design"]["required_root_classes"])}" data-article-type="{identity["article_type"]}">'+''.join(blocks)+'</article>';authoring_contract.validate_candidate(article,c);return article
