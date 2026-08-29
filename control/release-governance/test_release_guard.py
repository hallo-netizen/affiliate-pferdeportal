#!/usr/bin/env python3
import importlib.util,json,pathlib,shutil,tempfile
HERE=pathlib.Path(__file__).resolve().parent; ROOT=HERE.parents[1]
s=importlib.util.spec_from_file_location('rg',HERE/'release_guard.py'); rg=importlib.util.module_from_spec(s); s.loader.exec_module(rg)
def blocked(fn,name):
    try: fn()
    except rg.GuardError: return
    raise AssertionError('expected block:'+name)
def clone():
    t=tempfile.TemporaryDirectory(); d=pathlib.Path(t.name)/'r'; shutil.copytree(ROOT,d); return t,d
cases=0
rg.tree_check(ROOT); cases+=1
blocked(lambda:rg.release_check(ROOT),'premature'); cases+=1
blocked(lambda:rg.start(ROOT,'v6638-fix'),'branch'); cases+=1
rg.start(ROOT,'affiliate-release-current'); cases+=1
for rel,label in [
 ('release/affiliate-zentrale/archive/artifacts/v6620.b64/chunk000.txt','v6620'),
 ('release/affiliate-zentrale/archive/artifacts/v6634.b64/chunk000.txt','v6634'),
 ('release/affiliate-zentrale/current/CURRENT_WORKING_SOURCE.b64/chunk000.txt','current')]:
    t,r=clone(); p=r/rel; p.write_text('A'+p.read_text()[1:]); blocked(lambda r=r:rg.tree_check(r),label); t.cleanup(); cases+=1
t,r=clone(); p=r/'release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt'; p.write_text(p.read_text()+'0'*64+'  affiliate-portal-router/evil.php\n'); blocked(lambda:rg.tree_check(r),'manifest'); t.cleanup(); cases+=1
t,r=clone(); (r/'release/affiliate-zentrale/tests/real_db_gate_v6638.php').unlink(); blocked(lambda:rg.tree_check(r),'test'); t.cleanup(); cases+=1
t,r=clone(); p=r/'control/release-governance/CURRENT_RELEASE.json'; d=json.loads(p.read_text()); d['no_reconstruction']=False; p.write_text(json.dumps(d)); blocked(lambda:rg.tree_check(r),'flag'); t.cleanup(); cases+=1
t,r=clone(); p=r/'control/release-governance/CURRENT_RELEASE.json'; d=json.loads(p.read_text());
for g in d['required_release_gates'].values(): g.update(status='PASS',evidence_ref='protocol/fake.txt',evidence_sha256='0'*64)
d['active_candidate'].update(release_allowed=True,status='RELEASED',final_artifact_ref='release/affiliate-zentrale/current/no.zip',final_artifact_sha256='0'*64); p.write_text(json.dumps(d)); blocked(lambda:rg.release_check(r),'evidence'); t.cleanup(); cases+=1
a,b=clone(); c,h=clone(); p=h/'release/affiliate-zentrale/archive/BASELINE_V6620_SOURCE_SHA256.txt'; p.write_text(p.read_text()+'\n'); blocked(lambda:rg.pr_check(b,h,'affiliate-release-current','base'),'archive_scope'); a.cleanup(); c.cleanup(); cases+=1
print('AFFILIATE_RELEASE_GUARD_TESTS_PASS:'+str(cases))
