from pathlib import Path
import zipfile,hashlib,subprocess,difflib,json,io
old=Path('/mnt/data/PSTE-0.57.144.22-TEST.zip'); root=Path('/mnt/data/work_pste_exportfix'); plug=root/'Portal SEO Topic Engine'; new=Path('/mnt/data/PSTE-0.57.144.23-EXPORTFIX-NUR-TEST.zip'); combined=Path('/mnt/data/PFERDEATELIER-PSTE-05714423-PSERC-02855-QA-PAAR.zip'); pserc=Path('/mnt/data/PSERC-0.28.55-TEST.zip')
php_files=sorted(plug.rglob('*.php'))
for f in php_files:
 p=subprocess.run(['php','-l',str(f)],capture_output=True,text=True)
 if p.returncode:raise Exception(p.stdout+p.stderr)
with zipfile.ZipFile(new,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as dst:
 for f in sorted(plug.rglob('*')):
  if f.is_file():dst.write(f,f.relative_to(root).as_posix())
with zipfile.ZipFile(old) as a,zipfile.ZipFile(new) as b:
 assert a.testzip() is None and b.testzip() is None
 namesOld=set(a.namelist()); namesNew=set(b.namelist());assert namesOld==namesNew,(namesOld-namesNew,namesNew-namesOld)
 changed=sorted(n for n in namesOld if a.read(n)!=b.read(n));expected=['Portal SEO Topic Engine/includes/class-pste-admin.php','Portal SEO Topic Engine/includes/class-pste-mini-workflow.php','Portal SEO Topic Engine/includes/class-pste-snapshot.php','Portal SEO Topic Engine/portal-seo-topic-engine.php']
 assert changed==expected,changed
 diff='';
 for n in changed:
  aa=a.read(n).decode('utf8').splitlines(keepends=True);bb=b.read(n).decode('utf8').splitlines(keepends=True)
  diff+=''.join(difflib.unified_diff(aa,bb,fromfile='a/'+n,tofile='b/'+n))
 Path('/mnt/data/PSTE_05714422_to_05714423_EXPORTFIX.patch').write_text(diff)
for f in (new,pserc):
 with zipfile.ZipFile(f) as z:assert z.testzip() is None
with zipfile.ZipFile(combined,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 z.write(new,new.name);z.write(pserc,pserc.name)
with zipfile.ZipFile(combined) as z:
 assert z.testzip() is None
 assert hashlib.sha256(z.read(new.name)).hexdigest()==hashlib.sha256(new.read_bytes()).hexdigest()
 assert hashlib.sha256(z.read(pserc.name)).hexdigest()==hashlib.sha256(pserc.read_bytes()).hexdigest()
log=subprocess.run(['php','-d','display_errors=1','-d','error_reporting=E_ALL','/mnt/data/test_pste_exportfix.php'],capture_output=True,text=True)
assert log.returncode==0,(log.stdout,log.stderr)
assert not log.stderr,log.stderr
assert all(l.startswith('PASS') for l in log.stdout.strip().splitlines()),log.stdout
Path('/mnt/data/PSTE_05714423_QA_LOCAL_TEST_LOG.txt').write_text(log.stdout)
manifest={'status':'QA_ONLY_NOT_WORDPRESS_DEPLOYED','pste_new':{'filename':new.name,'version':'0.57.144.23','size_bytes':new.stat().st_size,'sha256':hashlib.sha256(new.read_bytes()).hexdigest(),'zip_entries':len(namesNew),'php_files_lint_pass':len(php_files)},'pste_original':{'filename':old.name,'version':'0.57.144.22','size_bytes':old.stat().st_size,'sha256':hashlib.sha256(old.read_bytes()).hexdigest()},'pserc_unchanged':{'filename':pserc.name,'version':'0.28.55','size_bytes':pserc.stat().st_size,'sha256':hashlib.sha256(pserc.read_bytes()).hexdigest()},'combined':{'filename':combined.name,'size_bytes':combined.stat().st_size,'sha256':hashlib.sha256(combined.read_bytes()).hexdigest()},'diff_changed_files':changed,'tests':{'pass_count':sum(l.startswith('PASS ') for l in log.stdout.splitlines()),'log':'PSTE_05714423_QA_LOCAL_TEST_LOG.txt','real_export':'pferdeatelier-mini-ergebnisse-20261108-150347.json','real_wordpress_count':1024,'real_ppm_runtime_count':144,'real_ppm_linked_titles':141,'unknown_ppm_post_ids_count':3,'unknown_imported_editorial_plan_title_count':9,'positive_full_snapshot_used_synthetic_missing_three_post_titles':True,'live_wordpress_test':False,'seo_decision_produced':False,'k0_changed':False}}
Path('/mnt/data/PSTE_05714423_TEST_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(json.dumps(manifest,ensure_ascii=False,indent=2))