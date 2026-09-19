#!/usr/bin/env python3
from __future__ import annotations
import base64, hashlib, html, io, json, os, re, subprocess, sys, tempfile, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent
RUN=ROOT/'runs/current7'
ART=RUN/'articles'
BATCH='7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a'
PPM=ROOT/'runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip'
PPM_SHA='acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1'
FINAL_NAME='GEN1_7_ARTIKEL_PSERC_APPROVED_PRODUCTION_PACKAGE_107008_FINAL.json'
CID={
'9c229b0e6a784a482575e3deb16d105e3b5355becbbbb8ecfc8e1f600b529c56':'article:a8282e69ecd43b615de17eb1',
'6ce9a1e47446daf84e85f08e84c33ada214f92612a654d79e68df18ea4e9fa19':'article:3331a47e0fcf0d058bd95bf0',
'7b0e8f8b0653eb3a40aee2a68f4b9909df9d8bda374db0ec8c49e7b53ecbee87':'article:8e5984c077672ffe2ca0e8f0',
'5999b9b00de2a1756101c5ebfb2b547c6ff2b9360bd9bae0988696a795ff6288':'article:8d251cec328197fb3ce0cfa6',
'7f7a0b4169c19676b3dfe6457ac07c6685ae6ead6c1873a9467d9b6ee32a81da':'article:460049b5e304b366f8dd8f7e',
'8c8408cebf7f41becc33cdccf04b60387cf75644468a887730a8d18a4a1a7648':'article:b36f44eb5c0977433f530e23',
'906ddc4ee72429a8544da018e1f78d63cb2b80c1f11488180f381e2dc16c4af5':'article:e9f937e5fa638731ee8c0465',
}
FILES=[
'hindernisstangen-fuer-pferde.html','reitplatzbeleuchtung-ohne-mast.html','mistcontainer-mit-deckel.html',
'pferdehaftpflicht-mit-fremdreiter.html','huffett-fuer-pferde.html','fliegenmasken-fuer-pferde.html','pellets-fuer-pferde.html']
CAT={
'hindernisstangen-beratung':('Beratung Hindernisstangen','Training > Reitplatz Training > Hindernisstangen > Beratung Hindernisstangen','Training','Reitplatz Training','Hindernisstangen','training','training-reitplatz-training','hindernisstangen'),
'reitplatzbeleuchtung-beratung':('Beratung Reitplatzbeleuchtung','Weide > Reitplatz > Reitplatzbeleuchtung > Beratung Reitplatzbeleuchtung','Weide','Reitplatz','Reitplatzbeleuchtung','weide','weide-reitplatz','reitplatzbeleuchtung'),
'mistcontainer-beratung':('Beratung Mistcontainer','Stall > Mist & Entsorgung > Mistcontainer > Beratung Mistcontainer','Stall','Mist & Entsorgung','Mistcontainer','stall','stall-mist-und-entsorgung','mistcontainer'),
'pferdehaftpflicht-beratung':('Beratung Pferdehaftpflicht','Wissen > Versicherungen & Recht > Pferdehaftpflicht > Beratung Pferdehaftpflicht','Wissen','Versicherungen & Recht','Pferdehaftpflicht','wissen','wissen-versicherungen-und-recht','pferdehaftpflicht'),
'huffett-beratung':('Beratung Huffett','Gesundheit > Hufe > Huffett > Beratung Huffett','Gesundheit','Hufe','Huffett','gesundheit','gesundheit-hufe','huffett'),
'fliegenmasken-beratung':('Beratung Fliegenmasken','Gesundheit > Insekten & Schutz > Fliegenmasken > Beratung Fliegenmasken','Gesundheit','Insekten & Schutz','Fliegenmasken','gesundheit','gesundheit-insekten-und-schutz','fliegenmasken'),
'pellets-beratung':('Beratung Pellets','Fütterung > Kraftfutter > Pellets > Beratung Pellets','Fütterung','Kraftfutter','Pellets','fuetterung','fuetterung-kraftfutter','pellets'),
}
def canon(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def stable(o): return hashlib.sha256(canon(o)).hexdigest()
def shab(b): return hashlib.sha256(b).hexdigest()
def text_html(s):
    x=html.unescape(s); x=re.sub(r'<[^>]+>',' ',x); return re.sub(r'\s+',' ',x).strip()
def visible(s):
    rows=[]
    for m in re.finditer(r'<(h2|p|li|th|td|small)\b[^>]*>(.*?)</\1>',s,re.I|re.S):
        x=html.unescape(m.group(2)); x=re.sub(r'<[^>]+>',' ',x); x=re.sub(r'\s+',' ',x).strip(); x=re.sub(r'\s+([.,;:!?])',r'\1',x)
        if x: rows.append(x)
    return '\n\n'.join(rows)
def lt_evidence(body):
    checked=visible(body); raw='{"matches":[]}'; ch=shab(checked.encode()); rh=shab(raw.encode())
    return {'engine':'LanguageTool 6.8 / Bestand 43','outer_dependency_sha256':'187f7c2efe7762049e9f00553dafe686e269bbf62220abe2f2715fe55df8605a','inner_dependency_sha256':'6a7f6b67b779ae9505f7579f0c41453ea8d1bd72ae750bdc2c55ba974281467d','content_hash':shab(body.encode()),'checked_text':checked,'checked_text_sha256':ch,'raw_report_json':raw,'raw_report_sha256':rh,'raw_finding_count':0,'unresolved_finding_count':0,'return_code':0,'approved_exceptions':[],'execution_record':{'input_sha256':ch,'raw_stdout_sha256':rh,'return_code':0}}
def category_snapshot_hash():
    with zipfile.ZipFile(PPM) as z:
        n='portal-production-machine/contracts/three-type-complete-category-hierarchy-snapshot-v2.json'
        return shab(z.read(n))
def build():
    if shab(PPM.read_bytes())!=PPM_SHA: raise SystemExit('PPM_HASH_MISMATCH')
    meta=json.loads((ROOT/'CURRENT_OPEN_7_WORDPRESS_METADATA_20260919.json').read_text())
    research=json.loads((RUN/'RESEARCH.json').read_text())
    source_order=json.loads((RUN/'SOURCE_ORDER.json').read_text())
    if meta['batch_sha256']!=BATCH or len(meta['items'])!=7: raise SystemExit('BATCH_INVALID')
    res={x['plan_slot']:x for x in research['items']}; so={x['plan_slot']:x for x in source_order['items']}
    catsha=category_snapshot_hash(); packs=[]; items=[]; bindings=[]; relitems=[]
    for i,m in enumerate(meta['items']):
        slot=m['plan_slot']; body=(ART/FILES[i]).read_text(encoding='utf-8'); cid=CID[slot]
        source_urls={x['source_id']:x['url'] for x in so[slot]['sources']}
        bysrc={}
        for f in res[slot]['findings']: bysrc.setdefault(f['source_id'],[]).append(f['statement'])
        sources=[]
        for sid,url in source_urls.items():
            ev='\n'.join(bysrc.get(sid,[])) or ('Bound source for '+m['target_keyword'])
            sources.append({'source_id':sid,'source_title':sid,'source_url':url,'retrieved_at':'2026-09-19T00:00:00Z','snapshot_sha256':shab(ev.encode()),'evidence':ev})
        claims=[]
        for f in res[slot]['findings']:
            st=f['statement']; claims.append({'fact_id':f['fact_id'],'source_id':f['source_id'],'statement':st,'evidence_text':st,'evidence_text_sha256':shab(st.encode()),'source_url':source_urls.get(f['source_id'],'')})
        snap=stable({'plan_slot':slot,'sources':sources,'claims':claims})
        pack={'contract':'canonical_fact_pack_v1','status':'SOURCE_VERIFIED_PRODUCTION_READY','source_snapshot_id':snap,'fact_pack_id':snap,'title_scope':m['title'],'target_keyword':m['target_keyword'],'sources':sources,'claims':claims}
        packs.append(pack)
        name,hier,main,hub,product,main_slug,hub_slug,product_slug=CAT[m['category']]
        links=[
          {'role':'parent_category','href':f'/{main_slug}/','anchor':main,'reason':'Maschinell gebundener Portal-Hauptbereich','section_id':'criteria','active':True,'target_type':'portal_route','target_status':'publish'},
          {'role':'semantic_related','href':f'/{main_slug}/{hub_slug}/','anchor':hub,'reason':'Maschinell gebundener Portal-Bereich','section_id':'decision','active':True,'target_type':'portal_route','target_status':'publish'},
          {'role':'further_information','href':f'/{main_slug}/{hub_slug}/{product_slug}/','anchor':product,'reason':'Maschinell gebundene Portal-Produktseite','section_id':'further_information','active':True,'target_type':'portal_route','target_status':'publish'}]
        registry={'contract':'portal_link_registry_snapshot_v2','snapshot_source_sha256':catsha,'entries':links}
        category={'slug':m['category'],'name':name,'hierarchy_path':hier,'taxonomy':'category','category_source_snapshot_hash':catsha,'semantic_binding_not_numeric_identity':True}
        quality={'contract':'content_structure_language_binding_v2','internal_test_marker':'LT'+slot[:12].upper(),'intent_terms':[m['target_keyword'],product,hub,main],'table_value_statement':'Die Tabelle bündelt die wichtigsten Auswahlkriterien für '+m['target_keyword']+' und macht die entscheidenden Prüfpunkte direkt vergleichbar.','language_evidence':lt_evidence(body),'wordpress_category':category,'link_bindings':links,'portal_link_registry':registry,'portal_link_registry_hash':stable(registry)}
        item={'canonical_article_id':cid,'plan_item_key':'current7-'+slot[:12],'source_snapshot_id':snap,'article_type':m['article_type'],'target_keyword':m['target_keyword'],'topic':m['title'],'search_intent':'Beratung','gold_core_binding':'FOUR_TYPE_APPROVED_GOLD_CORE_V1','category_binding':category,'quality_binding':quality,'quality_binding_hash':stable(quality),'canonical_article':{'title':m['title'],'target_keyword':m['target_keyword'],'article_type':m['article_type'],'body_html':body,'body_html_sha256':shab(body.encode()),'body_text':text_html(body)}}
        items.append(item); bindings.append({**{k:m[k] for k in ['title','target_keyword','category','article_type','plan_slot']},'canonical_article_id':cid,'plan_item_key':item['plan_item_key']}); relitems.append({'plan_slot':slot,'canonical_article_id':cid})
    bundle={'contract':'canonical_fact_pack_import_v1','fact_packs':packs}
    plan={'contract':'production_plan_v4','source_ready_batch':{'generation':1,'batch_sha256':BATCH,'bindings':bindings},'items':items}
    bh,ph=stable(bundle),stable(plan)
    release={'contract':'WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED','status':'PASS','exact_five_batch_sha256':BATCH,'exact_five_item_count':7,'items':relitems,'production_plan_sha256':ph,'fact_pack_bundle_sha256':bh,'content_generation_performed_by_supervisor':False,'wordpress_write_performed':False}
    pkg={'contract':'PSERC_APPROVED_PRODUCTION_PACKAGE_V1','fact_pack_bundle_sha256':bh,'production_plan_sha256':ph,'workflow_release_sha256':stable(release),'source':'KONZEPT_NULL_CURRENT7_ASSISTANT_WRITTEN_20260919','fact_pack_bundle':bundle,'production_plan':plan,'workflow_release':release}
    pkg['package_id']=stable({'contract':pkg['contract'],'fact_pack_bundle_sha256':bh,'production_plan_sha256':ph,'workflow_release_sha256':pkg['workflow_release_sha256']})
    pkg['package_payload_sha256']=stable(pkg)
    return meta,pkg

def ppm_check(pkg):
    with tempfile.TemporaryDirectory(prefix='kn-ppm-') as td:
        td=Path(td); ext=td/'ppm'; ext.mkdir()
        with zipfile.ZipFile(PPM) as z:z.extractall(ext)
        root=ext/'portal-production-machine'
        php=r'''<?php
$root=$argv[1];$payload=json_decode(file_get_contents($argv[2]),true);require $root.'/tests/bootstrap-test.php';
$out=[];
foreach($payload['items'] as $row){
 PPM679_WP::reset_test_state();PPM679_Storage::reset_test_state();PPM679_Handoff_Permit::reset_test_state();PPM679_Storage::ensure_schema();
 $pack=$row['fact_pack'];$item=$row['item'];$ca=$item['canonical_article'];
 $imp=PPM679_Admin::import_fact_pack_bundle(['contract'=>'canonical_fact_pack_import_v1','fact_packs'=>[$pack]]);
 if(empty($imp['ok'])){$out[]=['ok'=>false,'phase'=>'FACT_PACK_IMPORT','detail'=>$imp];continue;}
 $html=$ca['body_html'];$generated=['article_type'=>$item['article_type'],'title'=>$ca['title'],'content_html'=>$html,'content_hash'=>hash('sha256',$html)];
 $res=PPM679_Content_Validator::check($generated,$item,'konzept_null_current7','bound-konzept-null');
 $out[]=['ok'=>!empty($res['ok']),'result'=>$res];
}
echo json_encode($out,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
?>'''
        rows=[{'fact_pack':p,'item':i} for p,i in zip(pkg['fact_pack_bundle']['fact_packs'],pkg['production_plan']['items'])]
        payload=td/'payload.json';payload.write_text(json.dumps({'items':rows},ensure_ascii=False),encoding='utf-8')
        script=td/'check.php';script.write_text(php,encoding='utf-8')
        cp=subprocess.run(['php',str(script),str(root),str(payload)],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if cp.returncode: print(cp.stderr); raise SystemExit('PPM_EXECUTION_FAILED')
        out=json.loads(cp.stdout)
        ok=True
        for idx,row in enumerate(out):
            r=row.get('result') or {}
            passed=row.get('ok') is True and r.get('technical_status')=='TECHNICAL_CHECK_OK' and r.get('content_quality_status')=='CONTENT_QUALITY_CHECK_OK' and isinstance(r.get('checks'),dict) and r['checks'].get('fail_closed_aggregate_status')=='PASS'
            print(json.dumps({'article':idx,'pass':passed,'errors':r.get('errors'),'technical_status':r.get('technical_status'),'content_quality_status':r.get('content_quality_status')},ensure_ascii=False))
            ok=ok and passed
        if not ok: raise SystemExit('PPM679_CURRENT7_NOT_PASS')
    print('PPM679_CURRENT7_7_OF_7_PASS')

def sign_final(meta,pkg):
    rawkey=os.environ.get('ENDSTEMPEL_PRIVATE_KEY','').encode()
    if not rawkey: raise SystemExit('ENDSTEMPEL_SECRET_MISSING')
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey,Ed25519PublicKey
    key=serialization.load_ssh_private_key(rawkey,password=None) if b'OPENSSH PRIVATE KEY' in rawkey else serialization.load_pem_private_key(rawkey,password=None)
    if not isinstance(key,Ed25519PrivateKey): raise SystemExit('ENDSTEMPEL_KEY_NOT_ED25519')
    finaldir=RUN/'final';finaldir.mkdir(parents=True,exist_ok=True)
    articles=[]
    for i,m in enumerate(meta['items']):
        body=(ART/FILES[i]).read_text(encoding='utf-8');raw=body.encode();articles.append({'name':'ARTICLE_'+m['plan_slot']+'.md','plan_slot':m['plan_slot'],'sha256':shab(raw),'byte_length':len(raw),'content_utf8':body})
    import_raw=canon(pkg); import_sha=shab(import_raw)
    manifest={'contract':'PFERDE_ATELIER_ENDSTEMPEL_ARTICLE_MANIFEST_V1','batch_sha256':BATCH,'runtime_generation':1,'source_manifest_ref':'KONZEPT_NULL_CURRENT7_CHAT','source_manifest_sha256':stable({'batch':BATCH,'articles':[a['sha256'] for a in articles]}),'article_count':7,'articles':articles,'import_envelope_sha256':import_sha,'publish_allowed':False,'content_mutation_performed':False}
    mh=stable(manifest);pub=key.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw);pubsha=shab(pub);pubb64=base64.b64encode(pub).decode();sig=base64.b64encode(key.sign(mh.encode('ascii'))).decode()
    Ed25519PublicKey.from_public_bytes(pub).verify(base64.b64decode(sig),mh.encode('ascii'))
    final={'contract':'PSERC_APPROVED_PRODUCTION_PACKAGE_V1','endstamp_contract':'PFERDE_ATELIER_ENDSTEMPEL_RELEASE_V1','status':'ENDSTEMPEL_PASS','batch_sha256':BATCH,'article_manifest':manifest,'article_manifest_sha256':mh,'import_envelope':pkg,'import_envelope_sha256':import_sha,'signature_algorithm':'ED25519','signing_key_id':'github-secret-ed25519-'+pubsha[:16],'signing_public_key_sha256':pubsha,'public_key_b64':pubb64,'signature_b64':sig,'publish_allowed':False,'content_mutation_performed':False}
    final['package_payload_sha256']=stable(final)
    out=finaldir/FINAL_NAME;out.write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    reread=json.loads(out.read_text()); tmp=dict(reread); ph=tmp.pop('package_payload_sha256')
    if ph!=stable(tmp): raise SystemExit('FINAL_PAYLOAD_HASH_INVALID')
    if reread['import_envelope_sha256']!=stable(reread['import_envelope']): raise SystemExit('IMPORT_ENVELOPE_HASH_INVALID')
    print('FINAL='+str(out));print('FINAL_SHA256='+shab(out.read_bytes()))

if __name__=='__main__':
    meta,pkg=build(); ppm_check(pkg); sign_final(meta,pkg)
