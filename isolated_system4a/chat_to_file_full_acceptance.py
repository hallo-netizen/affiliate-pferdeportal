#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, subprocess
from pathlib import Path
from typing import Any

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
SYSTEM4=REPO/'isolated_system4'
CONTRACT='SYSTEM4A_CHAT_TO_FILE_FULL_ACCEPTANCE_V2'
MANIFEST_CONTRACT='SYSTEM4_PROVEN_RUNTIME_MANIFEST_V1'
HANDOFF_CONTRACT='SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2'

# Exact locally proven Punkt-0/Supervisor candidate. Partial transfer is forbidden.
REQUIRED_PROVEN_RUNTIME={
 'proof_head':'cd6c134a3ee27f4535ea91bfe6cc223a34c9eb25',
 'point0_snapshot.py':'4dab3cc58da04cf2d5d53f22bc7e837b3cca7c88',
 'supervisor.py':'0afb25204fe8cac1dc24912f638451842a68399b',
 'root_supervisor_bridge.py':'2c9e0ce6e22efee20ceedfef5e3ba37c044eeb2f',
 'worker_dispatch.py':'608627f4d9d1b09758e42fd7ece4690fe9761575',
 'codex_entry.py':'c74044a85e9da6de3e9af6472555306e8f6fb28c',
 'root_entry.py':'b533e8223351ef291be6b624bb803b9f888d5268',
}

# Errors that previously escaped green tests and/or appeared only in real Codex runs.
LIVE_ESCAPE_CLASSES=(
 'chat_trigger_not_bound','partial_or_wrong_runtime_bytes','point0_missing_or_mutated',
 'legacy_root_instead_of_start_point0','root_manifest_binding_missing','supervisor_authority_not_external',
 'cross_uid_worker_path_inaccessible','private_python_interpreter_leak','worker_factory_signature_drift',
 'worker_exits_without_response','worker_authority_field_injection','research_not_bound_to_point0_sources',
 'facts_not_bound_to_research','unknown_or_foreign_fact_id','context_snapshot_mismatch',
 'prebound_quality_binding','ppm_quality_binding_missing','noncanonical_category','wrong_or_missing_plan_slot',
 'wrong_internal_link_binding','prebound_runtime_links','missing_textmachine_authoring_binding',
 'repair_restarts_article_or_mutates_context','lt_dependency_missing_or_wrong','lt_not_run_via_fullcheck',
 'ppm_dependency_missing_or_wrong','ppm_not_actually_executed','synthetic_or_pregenerated_pass',
 'ppm_content_hash_not_final_article','required_table_or_design_missing','batch_drop_duplicate_or_reorder',
 'batch_context_mismatch','handoff_schema_or_canonical_bytes_mismatch','inline_transport_tamper',
 'parent_chat_not_byte_identical','publish_allowed_not_false',
)

class Blocked(RuntimeError): pass

def req(ok:bool,code:str)->None:
 if not ok: raise Blocked(code)

def sha256_file(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()

def git_blob(p:Path)->str:
 cp=subprocess.run(['git','hash-object',str(p)],cwd=REPO,text=True,capture_output=True,check=False)
 req(cp.returncode==0,'RUNTIME_GIT_BLOB_UNAVAILABLE:'+p.name)
 return cp.stdout.strip()

def load_raw_chat_trigger(path:Path)->dict[str,Any]:
 v=json.loads(path.read_text(encoding='utf-8'))
 req(v.get('contract')==CONTRACT,'CHAT_TRIGGER_CONTRACT_INVALID')
 req(v.get('publish_allowed') is False,'CHAT_TRIGGER_PUBLISH_ALLOWED_INVALID')
 n=v.get('article_count'); req(isinstance(n,int) and 1<=n<=3,'CHAT_TRIGGER_COUNT_NOT_1_TO_3')
 rows=v.get('raw_articles'); req(isinstance(rows,list) and len(rows)==n,'CHAT_TRIGGER_ROWS_INVALID')
 for i,row in enumerate(rows):
  req(isinstance(row,dict) and isinstance(row.get('topic_seed'),str) and row['topic_seed'].strip(),f'CHAT_TRIGGER_TOPIC_MISSING:{i}')
  # Critical: chat may NOT smuggle machine-owned production bindings into the test.
  forbidden={'title','target_keyword','category','plan_slot','links','quality_binding','quality_binding_hash','checks','pass'}
  req(not(forbidden & set(row)),f'CHAT_TRIGGER_PREBOUND_MACHINE_FIELD_FORBIDDEN:{i}')
 return v

def verify_runtime()->tuple[dict[str,Any],dict[str,str]]:
 actual={}
 for name,expected in REQUIRED_PROVEN_RUNTIME.items():
  if name=='proof_head': continue
  p=SYSTEM4/name; req(p.is_file(),'CURRENT_RUNTIME_FILE_MISSING:'+name)
  got=git_blob(p); actual[name]=got
  req(got==expected,'CURRENT_RUNTIME_IDENTITY_MISMATCH:'+name+':'+got+':EXPECTED:'+expected)
 manifest_path=SYSTEM4/'CURRENT_PROVEN_RUNTIME_MANIFEST.json'
 req(manifest_path.is_file(),'CURRENT_PROVEN_RUNTIME_MANIFEST_MISSING')
 m=json.loads(manifest_path.read_text(encoding='utf-8'))
 req(m.get('contract')==MANIFEST_CONTRACT,'CURRENT_PROVEN_RUNTIME_MANIFEST_INVALID')
 req(m.get('proof_head')==REQUIRED_PROVEN_RUNTIME['proof_head'],'CURRENT_PROVEN_RUNTIME_PROOF_HEAD_MISMATCH')
 blobs=m.get('git_blobs'); req(isinstance(blobs,dict) and blobs.get('controller.py'),'CURRENT_PROVEN_CONTROLLER_BINDING_MISSING')
 for name,expected in blobs.items():
  p=SYSTEM4/name; req(p.is_file(),'BOUND_RUNTIME_FILE_MISSING:'+name)
  got=git_blob(p); actual[name]=got; req(got==expected,'BOUND_RUNTIME_FILE_MISMATCH:'+name)
 entry_rel=m.get('chat_to_file_entry'); entry_sha=m.get('chat_to_file_entry_sha256')
 req(isinstance(entry_rel,str) and entry_rel.startswith('isolated_system4/'),'BOUND_CHAT_TO_FILE_ENTRY_MISSING')
 entry=REPO/entry_rel; req(entry.is_file(),'BOUND_CHAT_TO_FILE_ENTRY_FILE_MISSING')
 req(isinstance(entry_sha,str) and sha256_file(entry)==entry_sha,'BOUND_CHAT_TO_FILE_ENTRY_SHA_MISMATCH')
 return m,actual

def run_live_entry(m:dict[str,Any],trigger:Path,work:Path,lt:Path)->dict[str,Any]:
 entry=REPO/m['chat_to_file_entry']
 cp=subprocess.run(['python3',str(entry),'--chat-trigger',str(trigger),'--workspace',str(work),
                    '--worker-mode','simulation-no-codex','--languagetool-jar',str(lt)],
                   cwd=REPO,text=True,capture_output=True,check=False)
 req(cp.returncode==0,'BOUND_LIVE_ENTRY_BLOCKED:RC='+str(cp.returncode)+':'+(cp.stdout+cp.stderr)[-1200:])
 try: return json.loads(cp.stdout.strip().splitlines()[-1])
 except Exception as e: raise Blocked('BOUND_LIVE_ENTRY_RESULT_JSON_INVALID') from e

def verify_terminal(r:dict[str,Any],count:int)->None:
 req(r.get('status')=='SYSTEM4_CHAT_TO_FILE_PASS','FULL_ROUTE_NOT_PASS:'+str(r.get('status')))
 req(r.get('article_count')==count,'FINAL_ARTICLE_COUNT_MISMATCH')
 req(r.get('codex_used') is False,'CODEX_USED_IN_SIMULATION')
 req(r.get('publish_allowed') is False,'FINAL_PUBLISH_ALLOWED_INVALID')
 for key in ('chat_trigger_pass','point0_pass','root_pass','supervisor_pass','worker_boundary_pass','batch_pass','inline_unpack_pass','parent_chat_byte_equal'):
  req(r.get(key) is True,'TERMINAL_PROOF_MISSING:'+key)
 bindings=r.get('machine_bindings'); req(isinstance(bindings,list) and len(bindings)==count,'MACHINE_BINDINGS_MISSING')
 for i,b in enumerate(bindings):
  req(isinstance(b,dict),f'MACHINE_BINDING_INVALID:{i}')
  for k in ('title','target_keyword','category','plan_slot','links','textmachine_contract_sha256'):
   req(b.get(k),f'MACHINE_BINDING_FIELD_MISSING:{i}:{k}')
  req(isinstance(b.get('links'),list) and len(b['links'])==3,f'MACHINE_THREE_LINK_BINDING_MISSING:{i}')
 lt=r.get('languagetool') or {}; ppm=r.get('ppm679') or {}
 req(lt.get('version')=='6.8' and lt.get('executed') is True and lt.get('status')=='PASS','REAL_LT68_PASS_NOT_PROVEN')
 req(ppm.get('version')=='6.7.9' and ppm.get('executed') is True and ppm.get('status')=='PASS','REAL_PPM679_PASS_NOT_PROVEN')
 req(r.get('handoff_contract')==HANDOFF_CONTRACT,'HANDOFF_CONTRACT_INVALID')
 out=Path(str(r.get('output_path',''))); req(out.is_file(),'FINAL_PARENT_CHAT_FILE_MISSING')
 req(isinstance(r.get('output_sha256'),str) and sha256_file(out)==r['output_sha256'],'FINAL_FILE_SHA_MISMATCH')

def run(trigger:Path,work:Path,lt:Path)->dict[str,Any]:
 chat=load_raw_chat_trigger(trigger)
 # Mandatory ordering: wrong bytes block before Point 0/research/text.
 manifest,identity=verify_runtime()
 req(lt.is_file(),'LANGUAGETOOL_JAR_MISSING')
 req(sha256_file(lt)=='2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8','LANGUAGETOOL_JAR_SHA_MISMATCH')
 ppm=REPO/'control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip'
 req(ppm.is_file(),'PPM679_PACKAGE_MISSING')
 req(sha256_file(ppm)=='acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1','PPM679_PACKAGE_SHA_MISMATCH')
 result=run_live_entry(manifest,trigger,work,lt); verify_terminal(result,chat['article_count'])
 return {'status':'SYSTEM4A_CHAT_TO_FILE_FULL_ACCEPTANCE_PASS','article_count':chat['article_count'],
         'codex_used':False,'historical_escape_classes_bound':len(LIVE_ESCAPE_CLASSES),
         'runtime_identity':identity,'publish_allowed':False,'live_result':result}

def main(argv:list[str]|None=None)->int:
 p=argparse.ArgumentParser(); p.add_argument('--trigger',required=True); p.add_argument('--work-root',required=True); p.add_argument('--lt-jar',required=True); a=p.parse_args(argv)
 try: result=run(Path(a.trigger),Path(a.work_root),Path(a.lt_jar))
 except Exception as e:
  print(json.dumps({'status':'SYSTEM4A_CHAT_TO_FILE_FULL_ACCEPTANCE_BLOCKED','first_blocker':str(e),'codex_used':False,
                    'historical_escape_classes_bound':len(LIVE_ESCAPE_CLASSES),'publish_allowed':False},ensure_ascii=False,sort_keys=True)); return 4
 print(json.dumps(result,ensure_ascii=False,sort_keys=True)); return 0

if __name__=='__main__': raise SystemExit(main())
