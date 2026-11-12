from pathlib import Path
import hashlib, zipfile, difflib, subprocess, json, re
old=Path('/mnt/data/PSTE-0.57.144.24-PARKHAUS-QUELLFIX-NUR-TEST.zip')
root=Path('/mnt/data/work_pste_05714425')
plug=root/'Portal SEO Topic Engine'
new=Path('/mnt/data/PSTE-0.57.144.25-QUELLEN-IDENTITAET-KISS-NUR-TEST.zip')
ps=Path('/mnt/data/PSERC-0.28.55-TEST.zip')
paired=Path('/mnt/data/PFERDEATELIER-PSTE-05714425-PSERC-02855-QA-PAAR.zip')
php=sorted(plug.rglob('*.php'))
for f in php:
 proc=subprocess.run(['php','-l',str(f)],capture_output=True,text=True)
 if proc.returncode:raise RuntimeError(proc.stdout+proc.stderr)
# Preserve every original ZIP entry's name, time and metadata; only the three
# actual changed PHP file contents differ. Rebuilding never changes the ZIP hash.
with zipfile.ZipFile(old) as a,zipfile.ZipFile(new,'w') as z:
 for info in a.infolist():
  src=plug/info.filename.removeprefix('Portal SEO Topic Engine/')
  if info.is_dir():z.writestr(info,b'')
  else:z.writestr(info,src.read_bytes())
with zipfile.ZipFile(old) as a,zipfile.ZipFile(new) as b:
 assert a.testzip() is None and b.testzip() is None
 assert set(a.namelist())==set(b.namelist())
 changed=sorted(n for n in b.namelist() if a.read(n)!=b.read(n))
 assert changed == ['Portal SEO Topic Engine/includes/class-pste-mini-workflow.php','Portal SEO Topic Engine/includes/class-pste-snapshot.php','Portal SEO Topic Engine/portal-seo-topic-engine.php'],changed
 patch=''.join(''.join(difflib.unified_diff(a.read(n).decode().splitlines(True),b.read(n).decode().splitlines(True),fromfile='a/'+n,tofile='b/'+n)) for n in changed)
 Path('/mnt/data/PSTE_05714424_to_05714425_QUELLEN_IDENTITAET_KISS.patch').write_text(patch,encoding='utf8')
 count=len(b.namelist())
 assert re.search('Version:\\s*0\\.57\\.144\\.25',b.read('Portal SEO Topic Engine/portal-seo-topic-engine.php').decode())
with zipfile.ZipFile(ps) as z: assert z.testzip() is None
with zipfile.ZipFile(paired,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for file in [new,ps]:
  info=zipfile.ZipInfo(file.name,(2026,11,8,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
  z.writestr(info,file.read_bytes())
with zipfile.ZipFile(paired) as z:
 assert z.testzip() is None
 assert z.read(new.name)==new.read_bytes()
 assert z.read(ps.name)==ps.read_bytes()
proc=subprocess.run(['php','-d','display_errors=1','-d','error_reporting=E_ALL','/mnt/data/test_pste_05714425_real_1179.php'],capture_output=True,text=True)
assert proc.returncode==0,(proc.stdout[-8000:],proc.stderr)
assert not proc.stderr,proc.stderr
assert all(line.startswith('PASS') for line in proc.stdout.strip().splitlines()),proc.stdout
log=Path('/mnt/data/PSTE_05714425_QA_LOCAL_TEST_LOG.txt');log.write_text(proc.stdout)
countpass=len([line for line in proc.stdout.strip().splitlines() if line.startswith('PASS ') and 'TOTAL LOCAL' not in line]); assert countpass>=85,countpass
fingerprint=lambda p:{'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
manifest={'scope':'PFERDEATELIER_ISOLATED_QA','status':'QA_ONLY_NOT_INSTALLED','original_pste':fingerprint(old),'new_pste':fingerprint(new),'unchanged_pserc':fingerprint(ps),'paired_archive':fingerprint(paired),'new_pste_version':'0.57.144.25','zip_entries_pass':count,'php_lint_pass':len(php),'changed_files':changed,'original_user_export':'pferdeatelier-mini-ergebnisse-20261108-162920.json','original_count':1179,'retained_after_reconciliation':1179,'legacy_identityless_editorial_rows':9,'historical_orphan_reserved_slots':3,'real_wp_title_joins':141,'canonical_id_duplicate_wp_article_groups':1,'canonical_collision_wp_post_ids':[16029,972638],'tests_pass':countpass,'single_external_seo_owner_completed':False,'reimport_done':False,'wordpress_real_install_done':False,'k0_changed':False,'production_write_attempted':False,'positive_test_synthetic_values_present':True,
 'source_provenance_on_real_wp_pending':True,'wrong_wp_canonical_meta_cleanup_pending':True,
 'all_144_slots_retained':True,'source_qa_note':'Real 1179-row source recreated with PHP mocks; three missing posts simulated as absent; synthetic content only in explicitly labelled positive fixtures. Reconcile legacy empty placeholders and orphaned reservations without declaring them active articles. No WordPress DB writes.'}
Path('/mnt/data/PSTE_05714425_TEST_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))