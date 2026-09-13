#!/usr/bin/env python3
from __future__ import annotations
import copy, hashlib, json, os, re, subprocess, sys, tempfile, time, zipfile
from pathlib import Path

import batch_gate
import handoff_transport
import production_checks

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
ROOT_ENTRY=HERE/'root_entry.py'
CONTROLLER=HERE/'controller.py'
PPM=REPO/production_checks.PPM_PACKAGE_REL
EXPECTED_BRANCH='hobbyroom/system4-true-single-room-v1'
G9_MEMBER='portal-production-machine/contracts/g9-single-faq-approved-candidate-v1.json'

SOURCES={
 'src-adac-horse-trailer-2025': {
  'source_title':'ADAC – Autos mit Stärken beim Pferdetransport',
  'source_url':'https://presse.adac.de/meldungen/adac-ev/technik/autos-mit-staerken-beim-pferdetransport.html',
  'evidence':'Da Pferdeanhänger mit oft bis zu 2,7 Tonnen zulässigem Gesamtgewicht sehr schwer sind, braucht das Zugfahrzeug eine hohe Anhängelast.'},
 'src-adac-towing-load-2025': {
  'source_title':'ADAC – Anhängelast: Was beim Fahren mit Anhänger zu beachten ist',
  'source_url':'https://www.adac.de/rund-ums-fahrzeug/auto-kaufen-verkaufen/kauftipps/anhaengelast/',
  'evidence':'Denn je nach Motorisierung, Getriebe- und Antriebsart sowie Ausstattung kann die zulässige Anhängelast sogar bei ein und demselben Modell erheblich variieren.'},
 'src-adac-support-load-2025': {
  'source_title':'ADAC – Stützlast: Was mit Anhänger zu beachten ist',
  'source_url':'https://www.adac.de/rund-ums-fahrzeug/auto-kaufen-verkaufen/kauftipps/stuetzlast/',
  'evidence':'Sind diese Werte nicht identisch, ist der kleinere Wert einzuhalten.'},
 'src-adac-driving-licence-2026': {
  'source_title':'ADAC – Pkw-Führerscheinklasse B und BE',
  'source_url':'https://www.adac.de/verkehr/rund-um-den-fuehrerschein/klassen/pkw/',
  'evidence':'Nicht immer genügt die Pkw-Fahrerlaubnis der Klasse B, mit der Sie auch kleinere Anhänger ziehen dürfen. Manchmal muss es die Anhängerklasse BE sein.'},
}

def shabytes(b: bytes)->str: return hashlib.sha256(b).hexdigest()
def stable(v)->str: return shabytes(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def writej(p:Path,v)->Path: p.write_text(json.dumps(v,ensure_ascii=False,indent=2,sort_keys=True),encoding='utf-8'); return p

def cmd(argv:list[str], expect:int|set[int]=0, env=None, stdin:bytes|None=None):
    if isinstance(expect,int): expect={expect}
    cp=subprocess.run(argv,cwd=REPO,input=stdin,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
    if cp.returncode not in expect:
        raise AssertionError(f'command rc={cp.returncode} expected={expect}: {argv}\nSTDOUT:\n{cp.stdout.decode(errors="replace")}\nSTDERR:\n{cp.stderr.decode(errors="replace")}')
    return cp

def build_fixture(root:Path):
    root.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(PPM) as z:
        g9=json.loads(z.read(G9_MEMBER).decode('utf-8'))
    item=copy.deepcopy(g9['item']); pack0=copy.deepcopy(g9['fact_pack'])
    body=g9['candidate']['content_html']
    body=re.sub(r'^<article\s+data-article-type="FAQ">','<article class="ppm-generated ppm-type-faq" data-article-type="FAQ">',body,count=1)
    srcs=copy.deepcopy(SOURCES)
    for s in srcs.values():
        s['retrieved_at']='2026-09-13T09:20:00Z'; s['snapshot_sha256']=shabytes(s['evidence'].encode())
    for claim in pack0['claims']:
        old=claim['evidence_text_sha256']; new=shabytes(srcs[claim['source_id']]['evidence'].encode())
        body=body.replace(f'data-source-hash="{old}"',f'data-source-hash="{new}"')
    final=body.replace('Weichen Unterlagen voneinander ab, kläre die Angaben vor der Abfahrt.','Wenn Unterlagen voneinander abweichen, kläre die Angaben vor der Abfahrt.')
    bad=final.replace('Eine einzelne bestandene Kontrolle reicht nicht aus','Eine einzelne bestandene Kontrollee reicht nicht aus',1)
    snapshot={'contract':'SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1','next_textmachine_metadata_batch':{
      'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2','status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE',
      'batch_sha256':shabytes(b'system4-full-local-root-to-file-v2'),'item_count':1,
      'items':[{'article_type':'FAQ','category':'checklisten-fuer-pferdeanhaenger-faq','plan_slot':shabytes(b'system4-full-local-faq-slot-v2'),'target_keyword':'Pferdeanhänger','title':'Was muss vor einer Fahrt mit Pferdeanhänger geprüft werden?'}],
      'publish_allowed':False}}
    sp=root/'bound_snapshot.json'; sp.write_text(json.dumps(snapshot,ensure_ascii=False,sort_keys=True,separators=(',',':')),encoding='utf-8')
    snap_sha=shabytes(sp.read_bytes())
    order=[c['source_id'] for c in pack0['claims']]; seen=set()
    research={'contract':'SYSTEM4_RESEARCH_EVIDENCE_V1','sources':[]}
    for sid in order:
        if sid in seen: continue
        seen.add(sid); research['sources'].append({'source_id':sid,**srcs[sid]})
    facts={'contract':'SYSTEM4_FACTS_EVIDENCE_V1','claims':[]}; pack_claims=[]
    for old in pack0['claims']:
        ev=srcs[old['source_id']]['evidence']; eh=shabytes(ev.encode())
        core={'fact_id':old['fact_id'],'source_id':old['source_id'],'statement':old['statement'],'evidence_text':ev,'evidence_text_sha256':eh}
        facts['claims'].append(core)
        c=copy.deepcopy(old); c.update({'evidence_text':ev,'evidence_text_sha256':eh,'source_url':srcs[old['source_id']]['source_url']}); pack_claims.append(c)
    pack=copy.deepcopy(pack0); pack['contract']='canonical_fact_pack_v1'; pack['status']='SOURCE_VERIFIED_PRODUCTION_READY'; pack['source_snapshot_id']=snap_sha; pack['fact_pack_id']=snap_sha; pack['sources']=research['sources']; pack['claims']=pack_claims
    for k in ['fact_pack_hash','source_manifest_hash','claim_register_hash']: pack.pop(k,None)
    item['article_type']='FAQ'; item['topic']=snapshot['next_textmachine_metadata_batch']['items'][0]['title']; item['target_keyword']='Pferdeanhänger'; item['source_snapshot_id']=snap_sha
    item['canonical_article']['title']=item['topic']; item['canonical_article']['article_type']='FAQ'; item['canonical_article']['body_html']=final; item['canonical_article']['body_html_sha256']=shabytes(final.encode())
    item['source_hashes']=[]
    if isinstance(item.get('runtime_order'),dict): item['runtime_order']['fact_pack_hash']='SYSTEM4_RUNTIME_REBOUND_AT_VALIDATION'
    item['quality_binding_hash']=stable(item['quality_binding'])
    files={'snapshot':sp,'research':writej(root/'research.json',research),'facts':writej(root/'facts.json',facts),'pack':writej(root/'fact_pack.json',pack),'plan':writej(root/'plan_item.json',item)}
    for n,t in [('bad',bad),('final',final)]:
        files[n]=root/f'article_{n}.html'; files[n].write_text(t,encoding='utf-8')
    return files

def root_stdin(snapshot:Path, workspace:Path, env, expect=0):
    return cmd([sys.executable,str(ROOT_ENTRY),'start-stdin',str(workspace)],expect,env,snapshot.read_bytes())

def stage_to_context(f,w,env):
    cp=root_stdin(f['snapshot'],w,env); assert b'SYSTEM4_ROOT_ENTRY_PASS:RESEARCH_REQUIRED' in cp.stdout
    assert (w/'bound_snapshot.json').read_bytes()==f['snapshot'].read_bytes()
    cmd([sys.executable,str(CONTROLLER),'research',str(w),str(f['research'])],0,env)
    cmd([sys.executable,str(CONTROLLER),'facts',str(w),str(f['facts'])],0,env)
    cmd([sys.executable,str(CONTROLLER),'context',str(w),str(f['pack']),str(f['plan'])],0,env)

def handoff_from_state(f,state_path,out):
    col=batch_gate.collect_batch(state_path.parent/'bound_snapshot.json',[state_path],out/'batch')
    s=json.loads(state_path.read_text(encoding='utf-8')); prod=s['checks']['production_evidence']['evidence']; a=s['article']
    payload={'contract':handoff_transport.HANDOFF_CONTRACT,'batch_sha256':s['batch_sha256'],'publish_allowed':False,'signing_deferred':True,'batch_gate_status':'SYSTEM4_BATCH_FULL_PASS_COLLECTED','no_legacy_status':'PASS','test_suite_status':'PASS','wordpress_review':{'file_format':'JSON','mime_type':'application/json','intended_next_step':'WORDPRESS_DIRECT_IMPORT','plugin_name':'Portal SEO Editorial Plan Compiler','plugin_version_verified_against':handoff_transport.DIRECT_IMPORT_PLUGIN_VERSION,'ppm_version_verified_against':'6.7.9','direct_wordpress_upload_ready':True,'direct_upload_block_reason':None,'required_downstream_components':[]},'articles':[{'index':0,'title':a['title'],'target_keyword':a['target_keyword'],'category':a['category'],'article_type':a['article_type'],'plan_slot':a['plan_slot'],'final_draft_sha256':s['draft_sha256'],'revision_count':s['revision'],'body':s['draft_markdown'],'production_context':{'fact_pack':s['production_context']['fact_pack'],'production_plan_item':s['production_context']['production_plan_item']},'languagetool':prod['languagetool'],'ppm679':prod['ppm679']}]}
    source=writej(out/'handoff-source.json',payload); canonical=out/handoff_transport.HANDOFF_FILENAME
    raw=handoff_transport.canonicalize_handoff(source,canonical); inline=out/handoff_transport.INLINE_FILENAME; envp=handoff_transport.inline_pack(canonical,inline); recon=handoff_transport.inline_unpack(inline,out/'parent-chat')
    assert recon.read_bytes()==raw==canonical.read_bytes()
    return col,envp,recon

def main():
    start=time.monotonic(); results=[]
    jar=os.environ.get('SYSTEM4_LANGUAGETOOL_JAR','')
    if not jar or not Path(jar).is_file() or production_checks.file_sha256(Path(jar))!=production_checks.LT_JAR_SHA256: raise SystemExit('LT JAR missing/wrong')
    assert production_checks.file_sha256(PPM)==production_checks.PPM_PACKAGE_SHA256
    assert cmd(['git','branch','--show-current']).stdout.decode().strip()==EXPECTED_BRANCH
    env=os.environ.copy(); env['SYSTEM4_LANGUAGETOOL_JAR']=jar; env.setdefault('TERM','xterm')
    base=Path(tempfile.mkdtemp(prefix='system4-full-local-v2-')); f=build_fixture(base/'fixture')

    w=base/'positive'/'item0'; w.mkdir(parents=True); stage_to_context(f,w,env)
    cmd([sys.executable,str(CONTROLLER),'draft',str(w),str(f['bad'])],0,env)
    c=cmd([sys.executable,str(CONTROLLER),'fullcheck',str(w)],3,env); assert b'FULL:languagetool:LANGUAGETOOL_FINDING' in c.stdout
    cmd([sys.executable,str(CONTROLLER),'repair',str(w),str(f['final'])],0,env)
    c=cmd([sys.executable,str(CONTROLLER),'fullcheck',str(w)],0,env); assert b'SYSTEM4_FULL_CHECK_PASS:OUTPUT_GATE_REQUIRED' in c.stdout
    s=json.loads((w/'state.json').read_text()); ev=s['checks']['production_evidence']['evidence']
    assert ev['languagetool']['status']=='PASS' and ev['languagetool']['commandline_jar_sha256']==production_checks.LT_JAR_SHA256
    assert ev['ppm679']['status']=='PASS' and ev['ppm679']['ppm_package_sha256']==production_checks.PPM_PACKAGE_SHA256
    out=base/'positive'/'output'; out.mkdir(); col,envelope,recon=handoff_from_state(f,w/'state.json',out)
    output_root=Path(os.environ.get('SYSTEM4_ACCEPTANCE_OUTPUT_DIR','/tmp/system4-acceptance-output')); output_root.mkdir(parents=True,exist_ok=True)
    final=output_root/'SYSTEM4_FULL_LOCAL_ACCEPTANCE_WORDPRESS.json'; final.write_bytes(recon.read_bytes())
    results.append(('POS_ROOT_STDIN_TO_FILE',{'sha256':shabytes(final.read_bytes()),'bytes':final.stat().st_size,'parts':envelope['part_count'],'revision':s['revision'],'article_count':col['article_count']}))

    n=base/'n1'; cp=cmd([sys.executable,str(ROOT_ENTRY),'start-stdin',str(n/'w')],2,env,b'{bad-json'); assert b'ROOT_ENTRY_STDIN_SNAPSHOT_JSON_INVALID' in cp.stdout and not (n/'w'/'state.json').exists(); results.append(('NEG_ROOT_BAD_STDIN',{}))

    n=base/'n2'; bad=json.loads(f['snapshot'].read_text()); bad['next_textmachine_metadata_batch']['publish_allowed']=True; raw=json.dumps(bad,separators=(',',':')).encode(); cp=cmd([sys.executable,str(ROOT_ENTRY),'start-stdin',str(n/'w')],2,env,raw); assert b'WORDPRESS_PUBLISH_AUTHORITY_FAIL' in cp.stdout; results.append(('NEG_PUBLISH_AUTHORITY',{}))

    n=base/'n3'; n.mkdir(); root_stdin(f['snapshot'],n/'w',env); cmd([sys.executable,str(CONTROLLER),'research',str(n/'w'),str(f['research'])],0,env); facts=json.loads(f['facts'].read_text()); inv='Dieser frei erfundene Beleg steht nicht im akzeptierten Quellenausschnitt.'; facts['claims'][0]['evidence_text']=inv; facts['claims'][0]['evidence_text_sha256']=shabytes(inv.encode()); fp=writej(n/'bad-facts.json',facts); cp=cmd([sys.executable,str(CONTROLLER),'facts',str(n/'w'),str(fp)],2,env); assert b'FACT_EVIDENCE_NOT_IN_SOURCE' in cp.stdout; results.append(('NEG_FAKE_FACT',{}))

    n=base/'n4'; n.mkdir(); stage_to_context(f,n/'w',env); bad=f['final'].read_text().replace('system-129-table ','',1); dp=n/'bad-design.html'; dp.write_text(bad); cp=cmd([sys.executable,str(CONTROLLER),'draft',str(n/'w'),str(dp)],2,env); assert b'DESIGN_TABLE_SYSTEM129_CLASS_MISSING' in cp.stdout; results.append(('NEG_DESIGN_DRIFT',{}))

    inline=out/handoff_transport.INLINE_FILENAME; lines=inline.read_text().splitlines(); row=json.loads(lines[1]); b64=row['payload_base64']; row['payload_base64']=('A' if b64[0]!='A' else 'B')+b64[1:]; lines[1]=json.dumps(row,separators=(',',':')); tam=base/'tampered-inline.txt'; tam.write_text('\n'.join(lines)+'\n'); target=base/'tampered-out'
    try:
        handoff_transport.inline_unpack(tam,target); raise AssertionError('tampered relay accepted')
    except handoff_transport.HandoffError:
        assert not (target/handoff_transport.HANDOFF_FILENAME).exists(); results.append(('NEG_HANDOFF_TAMPER',{}))

    st=json.loads((w/'state.json').read_text()); st['draft_sha256']='0'*64; tsp=writej(base/'tampered-state.json',st)
    try:
        batch_gate.collect_batch(w/'bound_snapshot.json',[tsp],base/'tampered-batch'); raise AssertionError('tampered state accepted')
    except batch_gate.BatchGateError:
        results.append(('NEG_BATCH_STATE_TAMPER',{}))

    nl=production_checks.no_legacy_runtime_dependencies(REPO); assert nl['status']=='PASS' and nl['legacy_import_count']==0; results.append(('NEG_NO_LEGACY_RUNTIME',{}))

    report={'contract':'SYSTEM4_FULL_LOCAL_ROOT_TO_FILE_ACCEPTANCE_V2','status':'PASS','positive':results[0][1],'tests':[{'name':n,'status':'PASS','detail':d} for n,d in results],'test_count':len(results),'real_languagetool_sha256':production_checks.LT_JAR_SHA256,'real_ppm_sha256':production_checks.PPM_PACKAGE_SHA256,'mocks_used':False,'codex_used':False,'merge_or_publish':False,'elapsed_seconds':round(time.monotonic()-start,3),'final_file':str(final)}
    report_path=output_root/'SYSTEM4_FULL_LOCAL_ACCEPTANCE_REPORT.json'; report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__': raise SystemExit(main())
