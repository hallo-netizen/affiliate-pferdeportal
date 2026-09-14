#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, subprocess
from pathlib import Path
from typing import Any

REPO=Path(__file__).resolve().parent.parent
SYSTEM4=REPO/'isolated_system4'
CONTRACT='SYSTEM4A_CHAT_TO_FILE_FULL_ACCEPTANCE_V4'
METADATA_CONTRACT='PSERC_TEXTMACHINE_METADATA_BATCH_V2'
MANIFEST_CONTRACT='SYSTEM4_PROVEN_RUNTIME_MANIFEST_V2'
HANDOFF_CONTRACT='SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2'
REQUIRED_RUNTIME_FILES=(
 'point0_snapshot.py','supervisor.py','root_supervisor_bridge.py','worker_dispatch.py',
 'root_entry.py','codex_entry.py','controller.py','authoring_contract.py','content_guard.py',
 'design_guard.py','production_checks.py','batch_gate.py','batch_repetition_guard.py',
 'handoff_transport.py','LT68Worker.java',
)
LIVE_ESCAPE_CLASSES=(
 'chat_trigger_not_bound','bound_metadata_changed_after_chat_start','partial_or_wrong_runtime_bytes',
 'point0_missing_or_mutated','legacy_root_instead_of_start_point0','root_manifest_binding_missing',
 'supervisor_authority_not_external','cross_uid_worker_path_inaccessible','private_python_interpreter_leak',
 'worker_factory_signature_drift','worker_exits_without_response','worker_authority_field_injection',
 'research_not_bound_to_point0_sources','facts_not_bound_to_research','unknown_or_foreign_fact_id',
 'context_snapshot_mismatch','prebound_quality_binding','ppm_quality_binding_missing',
 'noncanonical_category','wrong_or_missing_plan_slot','wrong_internal_link_binding','prebound_runtime_links',
 'missing_textmachine_authoring_binding','repair_restarts_article_or_mutates_context',
 'lt_dependency_missing_or_wrong','lt_not_run_via_fullcheck','ppm_dependency_missing_or_wrong',
 'ppm_not_actually_executed','synthetic_or_pregenerated_pass','ppm_content_hash_not_final_article',
 'required_table_or_design_missing','batch_drop_duplicate_or_reorder','batch_context_mismatch',
 'handoff_schema_or_canonical_bytes_mismatch','inline_transport_tamper',
 'parent_chat_not_byte_identical','publish_allowed_not_false',
)

class Blocked(RuntimeError): pass

def req(ok:bool,code:str)->None:
 if not ok: raise Blocked(code)

def sha256_bytes(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def sha256_file(p:Path)->str:return sha256_bytes(p.read_bytes())
def canon(v:Any)->bytes:return (json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()

def git_blob(p:Path)->str:
 cp=subprocess.run(['git','hash-object',str(p)],cwd=REPO,text=True,capture_output=True,check=False)
 req(cp.returncode==0,'RUNTIME_GIT_BLOB_UNAVAILABLE:'+p.name); return cp.stdout.strip()

def git_head()->str:
 cp=subprocess.run(['git','rev-parse','HEAD'],cwd=REPO,text=True,capture_output=True,check=False)
 req(cp.returncode==0,'RUNTIME_HEAD_UNAVAILABLE'); return cp.stdout.strip()

def load_chat_start(path:Path)->dict[str,Any]:
 v=json.loads(path.read_text(encoding='utf-8'))
 req(v.get('contract')==CONTRACT,'CHAT_TRIGGER_CONTRACT_INVALID')
 req(v.get('action')=='START_BOUND_ARTICLE_TEST_BATCH','CHAT_TRIGGER_ACTION_INVALID')
 req(v.get('publish_allowed') is False,'CHAT_TRIGGER_PUBLISH_ALLOWED_INVALID')
 batch=v.get('bound_metadata_batch'); req(isinstance(batch,dict),'BOUND_METADATA_BATCH_MISSING')
 req(batch.get('contract')==METADATA_CONTRACT,'BOUND_METADATA_CONTRACT_INVALID')
 req(batch.get('status')=='READY_FOR_TEXTMACHINE_METADATA_INTAKE','BOUND_METADATA_NOT_READY')
 req(batch.get('publish_allowed') is False,'BOUND_METADATA_PUBLISH_ALLOWED_INVALID')
 rows=batch.get('items'); n=batch.get('item_count')
 req(isinstance(n,int) and 1<=n<=3,'BOUND_METADATA_COUNT_NOT_1_TO_3')
 req(isinstance(rows,list) and len(rows)==n,'BOUND_METADATA_ITEM_COUNT_MISMATCH')
 for i,row in enumerate(rows):
  req(isinstance(row,dict) and set(row)=={'article_type','category','plan_slot','target_keyword','title'},f'BOUND_METADATA_EXACT_FIVE_FIELDS_FAIL:{i}')
  for k in ('article_type','category','plan_slot','target_keyword','title'):
   req(isinstance(row.get(k),str) and row[k].strip(),f'BOUND_METADATA_FIELD_INVALID:{i}:{k}')
  req(len(row['plan_slot'])==64,f'BOUND_METADATA_PLAN_SLOT_INVALID:{i}')
 req(v.get('bound_metadata_sha256')==sha256_bytes(canon(batch)),'CHAT_METADATA_BINDING_SHA_MISMATCH')
 compiler=v.get('metadata_compiler_proof'); req(isinstance(compiler,dict),'METADATA_COMPILER_PROOF_MISSING')
 req(compiler.get('version')=='0.28.19','METADATA_COMPILER_VERSION_MISMATCH')
 req(compiler.get('build')=='0.28.19-endstempel-frozen-signed-import-rootfix-ppm679','METADATA_COMPILER_BUILD_MISMATCH')
 req(compiler.get('package_binding_sha256')=='760669761ce010d9b7f0ca18982e01c211953fb8a06def38e1c894817882da3d','METADATA_COMPILER_PACKAGE_BINDING_MISMATCH')
 req(isinstance(compiler.get('source_snapshot_sha256'),str) and len(compiler['source_snapshot_sha256'])==64,'METADATA_SOURCE_SNAPSHOT_BINDING_MISSING')
 return v

def verify_proof_manifest()->tuple[dict[str,Any],dict[str,str]]:
 path=SYSTEM4/'CURRENT_PROVEN_RUNTIME_MANIFEST.json'; req(path.is_file(),'CURRENT_PROVEN_RUNTIME_MANIFEST_MISSING')
 m=json.loads(path.read_text(encoding='utf-8')); req(m.get('contract')==MANIFEST_CONTRACT,'CURRENT_PROVEN_RUNTIME_MANIFEST_INVALID')
 proof_head=m.get('proof_head'); req(isinstance(proof_head,str) and len(proof_head)==40,'PROOF_HEAD_INVALID'); req(git_head()==proof_head,'CURRENT_HEAD_NOT_PROVEN_HEAD')
 blobs=m.get('git_blobs'); req(isinstance(blobs,dict),'RUNTIME_BLOB_MANIFEST_MISSING'); actual={}
 for name in REQUIRED_RUNTIME_FILES:
  expected=blobs.get(name); req(isinstance(expected,str) and len(expected)==40,'RUNTIME_BLOB_BINDING_MISSING:'+name)
  p=SYSTEM4/name; req(p.is_file(),'CURRENT_RUNTIME_FILE_MISSING:'+name)
  got=git_blob(p); actual[name]=got; req(got==expected,'CURRENT_RUNTIME_IDENTITY_MISMATCH:'+name)
 proof=m.get('acceptance_proof'); req(isinstance(proof,dict),'ACCEPTANCE_PROOF_MISSING')
 hist=proof.get('historical_error_matrix'); req(isinstance(hist,dict),'HISTORICAL_MATRIX_PROOF_MISSING')
 total=hist.get('total'); req(isinstance(total,int) and total>=len(LIVE_ESCAPE_CLASSES),'HISTORICAL_MATRIX_INCOMPLETE')
 req(hist.get('passed')==total and hist.get('failed')==0,'HISTORICAL_MATRIX_NOT_FULL_PASS')
 zero=proof.get('zero_to_file'); req(isinstance(zero,dict) and zero.get('status')=='PASS','ZERO_TO_FILE_PROOF_MISSING')
 req(zero.get('same_runtime_head')==proof_head,'ZERO_TO_FILE_HEAD_MISMATCH')
 req(zero.get('real_languagetool_6_8') is True,'ZERO_TO_FILE_REAL_LT_MISSING'); req(zero.get('real_ppm_6_7_9') is True,'ZERO_TO_FILE_REAL_PPM_MISSING')
 req(zero.get('batch_pass') is True and zero.get('inline_unpack_pass') is True and zero.get('parent_chat_byte_equal') is True,'ZERO_TO_FILE_TERMINAL_PROOF_INCOMPLETE')
 entry_rel=m.get('chat_to_file_entry'); entry_sha=m.get('chat_to_file_entry_sha256')
 req(isinstance(entry_rel,str) and entry_rel.startswith('isolated_system4/'),'BOUND_CHAT_TO_FILE_ENTRY_MISSING')
 entry=REPO/entry_rel; req(entry.is_file(),'BOUND_CHAT_TO_FILE_ENTRY_FILE_MISSING'); req(isinstance(entry_sha,str) and sha256_file(entry)==entry_sha,'BOUND_CHAT_TO_FILE_ENTRY_SHA_MISMATCH')
 req(m.get('simulation_and_live_same_entry') is True,'SIMULATION_LIVE_ENTRY_PARITY_NOT_PROVEN'); return m,actual

def run_live_entry(m:dict[str,Any],trigger:Path,work:Path,lt:Path)->dict[str,Any]:
 entry=REPO/m['chat_to_file_entry']
 cp=subprocess.run(['python3',str(entry),'--chat-trigger',str(trigger),'--workspace',str(work),'--worker-mode','simulation-no-codex','--languagetool-jar',str(lt)],cwd=REPO,text=True,capture_output=True,check=False)
 req(cp.returncode==0,'BOUND_LIVE_ENTRY_BLOCKED:RC='+str(cp.returncode)+':'+(cp.stdout+cp.stderr)[-1200:])
 try:return json.loads(cp.stdout.strip().splitlines()[-1])
 except Exception as e:raise Blocked('BOUND_LIVE_ENTRY_RESULT_JSON_INVALID') from e

def verify_terminal(r:dict[str,Any],chat:dict[str,Any])->None:
 rows=chat['bound_metadata_batch']['items']; count=len(rows)
 req(r.get('status')=='SYSTEM4_CHAT_TO_FILE_PASS','FULL_ROUTE_NOT_PASS:'+str(r.get('status'))); req(r.get('article_count')==count,'FINAL_ARTICLE_COUNT_MISMATCH')
 req(r.get('codex_used') is False,'CODEX_USED_IN_SIMULATION'); req(r.get('publish_allowed') is False,'FINAL_PUBLISH_ALLOWED_INVALID')
 for key in ('chat_trigger_pass','metadata_binding_pass','point0_pass','root_pass','supervisor_pass','worker_boundary_pass','batch_pass','inline_unpack_pass','parent_chat_byte_equal'):
  req(r.get(key) is True,'TERMINAL_PROOF_MISSING:'+key)
 preserved=r.get('bound_metadata_items'); req(preserved==rows,'BOUND_METADATA_NOT_PRESERVED_EXACTLY')
 bindings=r.get('machine_bindings'); req(isinstance(bindings,list) and len(bindings)==count,'MACHINE_BINDINGS_MISSING')
 for i,b in enumerate(bindings):
  req(isinstance(b,dict),f'MACHINE_BINDING_INVALID:{i}'); req(b.get('input_metadata')==rows[i],f'MACHINE_INPUT_METADATA_MISMATCH:{i}')
  req(isinstance(b.get('links'),list) and len(b['links'])==3,f'MACHINE_THREE_LINK_BINDING_MISSING:{i}')
  req(isinstance(b.get('textmachine_contract_sha256'),str) and len(b['textmachine_contract_sha256'])==64,f'TEXTMACHINE_BINDING_MISSING:{i}')
 lt=r.get('languagetool') or {}; ppm=r.get('ppm679') or {}
 req(lt.get('version')=='6.8' and lt.get('executed') is True and lt.get('status')=='PASS','REAL_LT68_PASS_NOT_PROVEN')
 req(ppm.get('version')=='6.7.9' and ppm.get('executed') is True and ppm.get('status')=='PASS','REAL_PPM679_PASS_NOT_PROVEN')
 req(r.get('handoff_contract')==HANDOFF_CONTRACT,'HANDOFF_CONTRACT_INVALID')
 out=Path(str(r.get('output_path',''))); req(out.is_file(),'FINAL_PARENT_CHAT_FILE_MISSING'); req(isinstance(r.get('output_sha256'),str) and sha256_file(out)==r['output_sha256'],'FINAL_FILE_SHA_MISMATCH')

def run(trigger:Path,work:Path,lt:Path)->dict[str,Any]:
 chat=load_chat_start(trigger); manifest,identity=verify_proof_manifest()
 req(lt.is_file(),'LANGUAGETOOL_JAR_MISSING'); req(sha256_file(lt)=='2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8','LANGUAGETOOL_JAR_SHA_MISMATCH')
 ppm=REPO/'control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip'; req(ppm.is_file(),'PPM679_PACKAGE_MISSING'); req(sha256_file(ppm)=='acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1','PPM679_PACKAGE_SHA_MISMATCH')
 result=run_live_entry(manifest,trigger,work,lt); verify_terminal(result,chat)
 return {'status':'SYSTEM4A_CHAT_TO_FILE_FULL_ACCEPTANCE_PASS','article_count':chat['bound_metadata_batch']['item_count'],'codex_used':False,'historical_escape_classes_bound':len(LIVE_ESCAPE_CLASSES),'runtime_identity':identity,'publish_allowed':False,'live_result':result}

def main(argv:list[str]|None=None)->int:
 p=argparse.ArgumentParser(); p.add_argument('--trigger',required=True); p.add_argument('--work-root',required=True); p.add_argument('--lt-jar',required=True); a=p.parse_args(argv)
 try:result=run(Path(a.trigger),Path(a.work_root),Path(a.lt_jar))
 except Exception as e:
  print(json.dumps({'status':'SYSTEM4A_CHAT_TO_FILE_FULL_ACCEPTANCE_BLOCKED','first_blocker':str(e),'codex_used':False,'historical_escape_classes_bound':len(LIVE_ESCAPE_CLASSES),'publish_allowed':False},ensure_ascii=False,sort_keys=True)); return 4
 print(json.dumps(result,ensure_ascii=False,sort_keys=True)); return 0

if __name__=='__main__': raise SystemExit(main())
