#!/usr/bin/env python3
from __future__ import annotations
import base64, copy, hashlib, importlib.util, json, shutil, subprocess, sys, tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent; FINALIZER=HERE/'ENDSTEMPEL_FINALIZER.py'; PHP_VERIFY=HERE/'ENDSTEMPEL_WORDPRESS_VERIFY.php'
def mod(p,n):
 s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
def dump(p,o):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fixture(root):
 b='c'*64;d=root/'.pferde-release'/b;d.mkdir(parents=True);outs=[];orig={}
 for i,text in enumerate(['eins\nOriginal\n','zwei\nOriginal\n']):
  n='ARTICLE_'+format(i+1,'064x')+'.md';p=d/n;p.write_bytes(text.encode());orig[n]=p.read_bytes();outs.append({'source_ref':'source/'+n,'released_ref':str(p.relative_to(root)),'sha256':sha(p)})
 r={'contract':'PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2','status':'OUTPUT_RELEASE_PASS_FINAL_REVIEW_AND_REARM_CONFIRMED','startmaster':'STARTMASTER0107','source_step_id':'RUN_NEW_ARTICLE_BATCH_NO_STOP','source_sequence':107007,'source_ticket_id':'t','source_state_sha256':'a'*64,'source_bundle_sha256':'b'*64,'batch_sha256':b,'worker_receipt_sha256':'d'*64,'final_review_step_id':'FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH','final_review_sequence':107008,'final_review_ticket_id':'tf','final_review_receipt_sha256':'e'*64,'main_head':'f'*40,'outputs':outs,'chat_execution_authority':'NONE','chat_output_authority':'NONE','domain_logic_authority':'NONE','quality_authority':'NONE','publish_allowed':False}
 rp=d/'RELEASE_RECEIPT.json';dump(rp,r);return b,d,rp,orig
def phprun(final,trusted,used=False,atomic=False):
 h=final.parent/'_h.php';v=str(PHP_VERIFY).replace('\\','\\\\').replace("'","\\'");tj=json.dumps(trusted,separators=(',',':')).replace('\\','\\\\').replace("'","\\'")
 if atomic: body="$p=[];$c=[];$rb=false;try{pferde_endstempel_atomic_import($argv[1],$trusted,fn($b)=>false,function(){},function($v)use(&$p){$p[]='x';throw new RuntimeException('FAIL');},function($b){},function()use(&$p,&$c){$c=$p;},function()use(&$p,&$rb){$p=[];$rb=true;});}catch(Throwable $e){} if(count($p)===0&&count($c)===0&&$rb){echo 'ZERO';exit(0);}exit(2);"
 else: body=f"$u={'true' if used else 'false'};try{{$r=pferde_endstempel_verify_before_write($argv[1],$trusted,function($b)use($u){{return $u;}});echo json_encode($r);exit(0);}}catch(Throwable $e){{echo $e->getMessage();exit(2);}}"
 h.write_text("<?php require '"+v+"';$trusted=json_decode('"+tj+"',true);"+body,encoding='utf-8');cp=subprocess.run(['php',str(h),str(final)],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE);h.unlink(missing_ok=True);return cp.returncode,cp.stdout+cp.stderr
def main():
 if shutil.which('php') is None:print('{"ok":false,"status":"HARD_BLOCK","reason":"PHP_RUNTIME_MISSING"}');return 2
 e=mod(FINALIZER,'endstamp_test');from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey;from cryptography.hazmat.primitives import serialization
 with tempfile.TemporaryDirectory() as td:
  root=Path(td);b,d,rp,orig=fixture(root);priv=Ed25519PrivateKey.generate();pub=priv.public_key().public_bytes(encoding=serialization.Encoding.Raw,format=serialization.PublicFormat.Raw);pb=base64.b64encode(pub).decode();ps=hashlib.sha256(pub).hexdigest();kid='test-'+ps[:16];trust={'signing_key_id':kid,'signing_public_key_sha256':ps,'public_key_b64':pb}
  def signer(h,*_):return {'signing_key_id':kid,'signing_public_key_sha256':ps,'public_key_b64':pb,'signature_b64':base64.b64encode(priv.sign(h.encode('ascii'))).decode()}
  z=e.finalize(root,str(rp.relative_to(root)),signer,trust);final=root/z['final_ref'];assert all((d/n).read_bytes()==raw for n,raw in orig.items());trusted={kid:{'sha256':ps,'public_key_b64':pb}};assert phprun(final,trusted)[0]==0
  wpriv=Ed25519PrivateKey.generate();wpub=wpriv.public_key().public_bytes(encoding=serialization.Encoding.Raw,format=serialization.PublicFormat.Raw);wpb=base64.b64encode(wpub).decode();wps=hashlib.sha256(wpub).hexdigest()
  def wrong(h,*_):return {'signing_key_id':'wrong','signing_public_key_sha256':wps,'public_key_b64':wpb,'signature_b64':base64.b64encode(wpriv.sign(h.encode('ascii'))).decode()}
  try:e.finalize(root,str(rp.relative_to(root)),wrong,trust);raise AssertionError('WRONG_KEY_ACCEPTED')
  except e.Blocked:pass
  first=d/sorted(orig)[0];raw=first.read_bytes();first.write_bytes(raw+b'X');assert phprun(final,trusted)[0]!=0;first.write_bytes(raw)
  pkg=json.loads(final.read_text());bad=copy.deepcopy(pkg);bad['batch_sha256']='d'*64;c=dict(bad);c.pop('package_payload_sha256',None);bad['package_payload_sha256']=e.stable_hash(c);bp=d/'BAD_BATCH.json';dump(bp,bad);assert phprun(bp,trusted)[0]!=0
  second=d/sorted(orig)[1];raw2=second.read_bytes();second.unlink();assert phprun(final,trusted)[0]!=0;second.write_bytes(raw2)
  extra=d/('ARTICLE_'+'f'*64+'.md');extra.write_text('x');assert phprun(final,trusted)[0]!=0;extra.unlink()
  bad=copy.deepcopy(pkg);bad['signature_b64']=base64.b64encode(b'0'*64).decode();c=dict(bad);c.pop('package_payload_sha256',None);bad['package_payload_sha256']=e.stable_hash(c);sp=d/'BAD_SIG.json';dump(sp,bad);assert phprun(sp,trusted)[0]!=0
  assert phprun(final,trusted,used=True)[0]!=0;rc,out=phprun(final,trusted,atomic=True);assert rc==0 and 'ZERO' in out
 print(json.dumps({'ok':True,'status':'ENDSTEMPEL_FIXED_TESTS_PASS','positive':True,'negative':True,'article_mutation_performed':False,'publish_allowed':False,'tests':['original_pass','one_character_changed_block','wrong_batch_block','missing_file_block','additional_file_block','wrong_signer_identity_block','wrong_signature_block','replay_block','import_failure_zero_committed_writes']},indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
