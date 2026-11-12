from pathlib import Path
import hashlib, zipfile, difflib, subprocess, json
old=Path('/mnt/data/PSTE-0.57.144.23-EXPORTFIX-NUR-TEST.zip')
root=Path('/mnt/data/work_pste_05714424')
plug=root/'Portal SEO Topic Engine'
new=Path('/mnt/data/PSTE-0.57.144.24-PARKHAUS-QUELLFIX-NUR-TEST.zip')
ps=Path('/mnt/data/PSERC-0.28.55-TEST.zip')
paired=Path('/mnt/data/PFERDEATELIER-PSTE-05714424-PSERC-02855-QA-PAAR.zip')
php=sorted(plug.rglob('*.php'))
for f in php:
 proc=subprocess.run(['php','-l',str(f)],capture_output=True,text=True)
 if proc.returncode:raise RuntimeError(proc.stdout+proc.stderr)
with zipfile.ZipFile(new,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in sorted(plug.rglob('*')):
  if f.is_file():z.write(f,f.relative_to(root).as_posix())
with zipfile.ZipFile(old) as a,zipfile.ZipFile(new) as b:
 assert a.testzip() is None and b.testzip() is None
 assert set(a.namelist())==set(b.namelist())
 changed=sorted(n for n in b.namelist() if a.read(n)!=b.read(n))
 assert changed == [
 'Portal SEO Topic Engine/includes/class-pste-mini-workflow.php',
 'Portal SEO Topic Engine/includes/class-pste-snapshot.php',
 'Portal SEO Topic Engine/portal-seo-topic-engine.php'],changed
 patch=''.join(''.join(difflib.unified_diff(a.read(n).decode().splitlines(True),b.read(n).decode().splitlines(True),fromfile='a/'+n,tofile='b/'+n)) for n in changed)
 Path('/mnt/data/PSTE_05714423_to_05714424_PARKHAUS_QUELLFIX.patch').write_text(patch,encoding='utf8')
 count=len(b.namelist())
with zipfile.ZipFile(ps) as z: assert z.testzip() is None
with zipfile.ZipFile(paired,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 z.write(new,new.name);z.write(ps,ps.name)
with zipfile.ZipFile(paired) as z:
 assert z.testzip() is None
 assert z.read(new.name)==new.read_bytes()
 assert z.read(ps.name)==ps.read_bytes()
proc=subprocess.run(['php','-d','display_errors=1','-d','error_reporting=E_ALL','/mnt/data/test_pste_05714424.php'],capture_output=True,text=True)
assert proc.returncode==0,(proc.stdout,proc.stderr)
assert not proc.stderr,proc.stderr
assert all(line.startswith('PASS') for line in proc.stdout.strip().splitlines()),proc.stdout
log=Path('/mnt/data/PSTE_05714424_QA_LOCAL_TEST_LOG.txt');log.write_text(proc.stdout)
countpass=len([line for line in proc.stdout.strip().splitlines() if line.startswith('PASS ') and 'TOTAL LOCAL' not in line]); assert countpass>=45,countpass
fingerprint=lambda p:{'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
manifest={'scope':'PFERDEATELIER_ISOLATED_QA','status':'QA_ONLY_NOT_INSTALLED','original_pste':fingerprint(old),'new_pste':fingerprint(new),'unchanged_pserc':fingerprint(ps),'paired_archive':fingerprint(paired),'new_pste_version':'0.57.144.24','zip_entries_pass':count,'php_lint_pass':len(php),'changed_files':changed,'original_user_data':'pferdeatelier-mini-ergebnisse-20261108-150347.json; pferdeatelier-mini-ergebnisse-20261108-160331.json','original_count':1179,'retained_after_error':1179,'unresolved_editorial_titles':9,'unresolved_runtime_post_ids':3,'real_wp_title_joins':141,'tests_pass':countpass,'semantic_owner_done':False,'reimport_done':False,'wordpress_real_install_done':False,'k0_changed':False,'positive_fully_complete_fixture_with_fake_9_titles_and_3_posts':True}
Path('/mnt/data/PSTE_05714424_TEST_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))