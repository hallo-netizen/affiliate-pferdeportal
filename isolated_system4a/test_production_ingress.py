import importlib.util
import json
import shutil
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parent.parent
SOURCE_INGRESS = SOURCE_ROOT / 'isolated_system4a' / 'production_ingress.py'
SOURCE_ROOT_ENTRY = SOURCE_ROOT / 'isolated_system4' / 'root_entry.py'
CRITICAL = (
    'AGENTS.md','AGENTS.override.md','isolated_system4/root_entry.py','isolated_system4/codex_entry.py',
    'isolated_system4/controller.py','isolated_system4/content_guard.py','isolated_system4/design_guard.py',
    'isolated_system4/production_checks.py','isolated_system4/batch_gate.py','isolated_system4/batch_repetition_guard.py',
    'isolated_system4/handoff_transport.py','isolated_system4/LT68Worker.java',
)

def run(argv,cwd):
    return subprocess.run(argv,cwd=cwd,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def make_repo():
    td=tempfile.TemporaryDirectory(prefix='system4a-ingress-test-'); repo=Path(td.name)/'repo'
    (repo/'isolated_system4a').mkdir(parents=True); (repo/'isolated_system4').mkdir(parents=True)
    shutil.copy2(SOURCE_INGRESS,repo/'isolated_system4a'/'production_ingress.py')
    shutil.copy2(SOURCE_ROOT_ENTRY,repo/'isolated_system4'/'root_entry.py')
    for rel in CRITICAL:
        p=repo/rel; p.parent.mkdir(parents=True,exist_ok=True)
        if rel=='isolated_system4/root_entry.py': continue
        if rel=='AGENTS.md': p.write_text('python3 control/cloud-entry-gate/cloud_entry.py start\n',encoding='utf-8')
        elif rel=='AGENTS.override.md': p.write_text('SYSTEM4_ISOLATED_ROOT_ENTRY_V3\npython3 isolated_system4/root_entry.py start\npython3 isolated_system4/root_entry.py start-stdin\nSYSTEM4 branch: DO NOT run `control/cloud-entry-gate/cloud_entry.py` before or instead of the System-4 root entry.\n',encoding='utf-8')
        else: p.write_text('fixed '+rel+'\n',encoding='utf-8')
    run(['git','init','-q'],repo); run(['git','config','user.email','test@example.invalid'],repo); run(['git','config','user.name','Test'],repo); run(['git','add','.'],repo); run(['git','commit','-qm','fixture'],repo)
    spec=importlib.util.spec_from_file_location('_ingress_test_module',repo/'isolated_system4a'/'production_ingress.py'); mod=importlib.util.module_from_spec(spec); sys.modules[spec.name]=mod; spec.loader.exec_module(mod)
    return td,repo,mod

def write_external(root,extra=None,batch_extra=None,item_extra=None):
    item={'title':'T','target_keyword':'K','category':'c','article_type':'Beratung','plan_slot':'1'*64}
    if item_extra: item.update(item_extra)
    batch={'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2','status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE','batch_sha256':'2'*64,'item_count':1,'publish_allowed':False,'items':[item]}
    if batch_extra: batch.update(batch_extra)
    value={'contract':'SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1','next_textmachine_metadata_batch':batch}
    if extra: value.update(extra)
    p=root/'external.json'; p.write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8'); return p,value

class ProductionIngressTests(unittest.TestCase):
    def test_positive_supervisor_owns_manifest_binding(self):
        td,repo,mod=make_repo(); self.addCleanup(td.cleanup); ext,original=write_external(Path(td.name)); authority=Path(td.name)/'authority'
        result=mod.bind_external_snapshot(ext,authority); bound=json.loads(result.bound_snapshot_path.read_text()); manifest=bound.pop('system4_root_manifest_sha256')
        self.assertEqual(bound,original); self.assertEqual(manifest,result.system4_manifest_sha256); self.assertEqual(authority.stat().st_mode & 0o777,0o700); self.assertEqual(result.bound_snapshot_path.stat().st_mode & 0o777,0o600)
    def test_negative_external_control_field_is_forbidden(self):
        td,repo,mod=make_repo(); self.addCleanup(td.cleanup); ext,_=write_external(Path(td.name),{'system4_root_manifest_sha256':'0'*64}); authority=Path(td.name)/'authority'
        with self.assertRaisesRegex(mod.ProductionIngressError,'EXTERNAL_CONTROL_FIELD_FORBIDDEN'): mod.bind_external_snapshot(ext,authority)
        self.assertFalse((authority/'ingress').exists())
    def test_negative_dirty_system4_control_bytes_block(self):
        td,repo,mod=make_repo(); self.addCleanup(td.cleanup); ext,_=write_external(Path(td.name)); (repo/'isolated_system4/controller.py').write_text('tampered\n')
        with self.assertRaisesRegex(mod.ProductionIngressError,'SYSTEM4_ROOT_MANIFEST_EVALUATION_FAILED'): mod.bind_external_snapshot(ext,Path(td.name)/'authority')
    def test_negative_authority_root_inside_repository_is_forbidden(self):
        td,repo,mod=make_repo(); self.addCleanup(td.cleanup); ext,_=write_external(Path(td.name))
        with self.assertRaisesRegex(mod.ProductionIngressError,'AUTHORITY_ROOT_INSIDE_REPOSITORY'): mod.bind_external_snapshot(ext,repo/'private')
    def test_negative_unknown_top_level_control_field_is_forbidden(self):
        td,repo,mod=make_repo(); self.addCleanup(td.cleanup); ext,_=write_external(Path(td.name),{'route':'skip-to-output'}); authority=Path(td.name)/'authority'
        with self.assertRaisesRegex(mod.ProductionIngressError,'EXTERNAL_SNAPSHOT_SCHEMA_INVALID'): mod.bind_external_snapshot(ext,authority)
        self.assertFalse((authority/'ingress').exists())
    def test_negative_unknown_batch_control_field_is_forbidden(self):
        td,repo,mod=make_repo(); self.addCleanup(td.cleanup); ext,_=write_external(Path(td.name),batch_extra={'next_phase':'ARTICLE_PASS'}); authority=Path(td.name)/'authority'
        with self.assertRaisesRegex(mod.ProductionIngressError,'EXTERNAL_BATCH_SCHEMA_INVALID'): mod.bind_external_snapshot(ext,authority)
        self.assertFalse((authority/'ingress').exists())
    def test_negative_unknown_item_control_field_is_forbidden(self):
        td,repo,mod=make_repo(); self.addCleanup(td.cleanup); ext,_=write_external(Path(td.name),item_extra={'checks':'PASS'}); authority=Path(td.name)/'authority'
        with self.assertRaisesRegex(mod.ProductionIngressError,'EXTERNAL_ITEM_SCHEMA_INVALID'): mod.bind_external_snapshot(ext,authority)
        self.assertFalse((authority/'ingress').exists())
    def test_positive_new_article_type_value_remains_open(self):
        td,repo,mod=make_repo(); self.addCleanup(td.cleanup); ext,_=write_external(Path(td.name)); value=json.loads(ext.read_text()); value['next_textmachine_metadata_batch']['items'][0]['article_type']='Neue Beitragsart 2040'; ext.write_text(json.dumps(value,ensure_ascii=False)); authority=Path(td.name)/'authority'
        result=mod.bind_external_snapshot(ext,authority); bound=json.loads(result.bound_snapshot_path.read_text())
        self.assertEqual(bound['next_textmachine_metadata_batch']['items'][0]['article_type'],'Neue Beitragsart 2040')

if __name__=='__main__': unittest.main(verbosity=2)
