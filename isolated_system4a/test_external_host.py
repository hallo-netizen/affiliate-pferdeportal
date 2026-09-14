import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from external_host import ExternalHostError, ExternalSupervisorHost, PersistentArticleWorkerPool, REPO
from test_full_chain_local import Checks, snapshot


def write_worker(path: Path, mode: str = "good") -> None:
    code = r'''
import hashlib,json,sys
from pathlib import Path
MODE=__MODE__
def sh(s): return hashlib.sha256(s.encode()).hexdigest()
def payload(req):
    a=req['article']; idx=a['title'].split()[-1]; task=req['task']
    e1=f'Gesicherter konkreter Beleg A für Artikel {idx} mit eindeutiger fachlicher Aussage und sicherer Nutzung.'
    e2=f'Gesicherter konkreter Beleg B für Artikel {idx} mit einer zweiten fachlichen Aussage zur Auswahl.'
    ev=e1+'\\n'+e2+'\\n'+f'Zusätzlicher gesicherter Quellenkontext für Artikel {idx}.'
    sid=f'src-{idx}'
    src={'source_id':sid,'source_title':f'Fachquelle {idx}','source_url':f'https://example.org/source-{idx}','retrieved_at':'2026-09-13T08:00:00Z','snapshot_sha256':sh(ev),'evidence':ev}
    claims=[{'fact_id':f'f-{idx}-a','source_id':sid,'statement':f'Konkrete erste Aussage für Artikel {idx}.','evidence_text':e1,'evidence_text_sha256':sh(e1)},{'fact_id':f'f-{idx}-b','source_id':sid,'statement':f'Konkrete zweite Aussage für Artikel {idx}.','evidence_text':e2,'evidence_text_sha256':sh(e2)}]
    if task=='research': return json.dumps({'contract':'SYSTEM4_RESEARCH_EVIDENCE_V1','sources':[src]},ensure_ascii=False,sort_keys=True)
    if task=='facts': return json.dumps({'contract':'SYSTEM4_FACTS_EVIDENCE_V1','claims':claims},ensure_ascii=False,sort_keys=True)
    if task=='context':
        pack={'contract':'canonical_fact_pack_v1','status':'SOURCE_VERIFIED_PRODUCTION_READY','sources':[src],'claims':claims}
        plan={'article_type':a['article_type'],'topic':a['title'],'target_keyword':a['target_keyword'],'category_binding':{'slug':a['category']}}
        return json.dumps({'fact_pack':pack,'production_plan_item':plan},ensure_ascii=False,sort_keys=True)
    repaired=' und nach Prüfbefund gezielt korrigiert' if task=='repair' else ''
    unique=' '.join(f'eigen{idx}_{n}' for n in range(90))
    return f'<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung"><section data-block="criteria"><h2>{a["title"]}</h2><p data-fact-ids="f-{idx}-a f-{idx}-b">Inhalt {idx}{repaired} {unique} mit eindeutiger fachlicher Struktur.</p><table class="system-129-table comparison-table"><tr><th>Kriterium</th><th>Prüfung</th></tr><tr><td>{idx}</td><td>Gebundener Wert {idx}</td></tr></table></section></article>'
for line in sys.stdin:
    env=json.loads(line); req=env['request']; sid=env['session_id']; contract=env['contract']
    if MODE=='malformed': print('not-json',flush=True); continue
    if MODE=='inject': print(json.dumps({'contract':contract,'session_id':sid,'result':{'content':'x','phase':'ARTICLE_PASS'}}),flush=True); continue
    if MODE=='wrong-session': print(json.dumps({'contract':contract,'session_id':'wrong','result':{'content':'x'}}),flush=True); continue
    if MODE=='fake-state': Path('state.json').write_text('{\"phase\":\"ARTICLE_PASS\"}')
    content=payload(req)
    print(json.dumps({'contract':contract,'session_id':sid,'result':{'content':content}},ensure_ascii=False),flush=True)
'''.replace("__MODE__", repr(mode))
    path.write_text(code, encoding="utf-8")
    path.chmod(0o755)


class ExternalHostFullChainTests(unittest.TestCase):
    def _root(self, td: str) -> Path:
        root = Path(td); root.chmod(0o755); return root

    def test_positive_cross_uid_entry_to_parent_chat_with_same_article_repair(self):
        if os.geteuid() != 0 or shutil.which("runuser") is None:
            self.skipTest("cross-uid test requires root + runuser")
        with tempfile.TemporaryDirectory() as td:
            root=self._root(td); snap=root/'snapshot.json'; snapshot(snap,2); worker=root/'worker.py'; write_worker(worker)
            work=root/'workers'; out=root/'SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json'; parent=root/'parent-chat'
            pool=PersistentArticleWorkerPool([sys.executable,str(worker)],work,run_as_user='nobody',require_cross_uid=True,runtime_processes=1)
            host=ExternalSupervisorHost(mode='test',checks=Checks(fail_first=True))
            result=host.run_architecture(snap,pool,out,parent)
            self.assertEqual(result['status'],'SYSTEM4A_EXTERNAL_HOST_ARCHITECTURE_PASS')
            self.assertEqual(result['article_count'],2)
            self.assertEqual(len(result['worker_sessions']),2)
            self.assertEqual(len(result['runtime_pids']),1)
            self.assertEqual(result['runtime_limit'],1)
            payload=json.loads(out.read_text(encoding='utf-8'))
            self.assertTrue(all(row['revision_count']==2 for row in payload['articles']))
            rebuilt=parent/'SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json'
            self.assertEqual(rebuilt.read_bytes(),out.read_bytes())
            for workspace in work.iterdir():
                self.assertFalse(any(p.name in {'state.json','authority.key','AGENTS.md','.git'} for p in workspace.rglob('*')))

    def test_positive_complete_external_process_scale_1_3_25(self):
        for count in (1,3,25):
            with self.subTest(count=count), tempfile.TemporaryDirectory() as td:
                root=self._root(td); snap=root/'s.json'; snapshot(snap,count); worker=root/'worker.py'; write_worker(worker)
                pool=PersistentArticleWorkerPool([sys.executable,str(worker)],root/'workers',runtime_processes=2)
                host=ExternalSupervisorHost(mode='test',checks=Checks())
                result=host.run_architecture(snap,pool,root/'o.json',root/'parent')
                self.assertEqual(result['article_count'],count)
                self.assertEqual(len(result['worker_sessions']),count)
                self.assertLessEqual(len(result['runtime_pids']),2)
                self.assertEqual(result['runtime_limit'],2)

    def test_negative_worker_pass_injection_blocks_before_output(self):
        with tempfile.TemporaryDirectory() as td:
            root=self._root(td); snap=root/'s.json'; snapshot(snap,1); worker=root/'worker.py'; write_worker(worker,'inject'); out=root/'o.json'
            pool=PersistentArticleWorkerPool([sys.executable,str(worker)],root/'workers'); host=ExternalSupervisorHost(mode='test',checks=Checks())
            with self.assertRaisesRegex(ExternalHostError,'WORKER_RESULT_SCHEMA_INVALID'): host.run_architecture(snap,pool,out,root/'parent')
            self.assertFalse(out.exists())

    def test_negative_worker_fake_state_file_blocks_before_output(self):
        with tempfile.TemporaryDirectory() as td:
            root=self._root(td); snap=root/'s.json'; snapshot(snap,1); worker=root/'worker.py'; write_worker(worker,'fake-state'); out=root/'o.json'
            pool=PersistentArticleWorkerPool([sys.executable,str(worker)],root/'workers'); host=ExternalSupervisorHost(mode='test',checks=Checks())
            with self.assertRaisesRegex(ExternalHostError,'WORKER_AUTHORITY_FILE_FORBIDDEN:state.json'): host.run_architecture(snap,pool,out,root/'parent')
            self.assertFalse(out.exists())

    def test_negative_malformed_worker_response_blocks_before_output(self):
        with tempfile.TemporaryDirectory() as td:
            root=self._root(td); snap=root/'s.json'; snapshot(snap,1); worker=root/'worker.py'; write_worker(worker,'malformed'); out=root/'o.json'
            pool=PersistentArticleWorkerPool([sys.executable,str(worker)],root/'workers'); host=ExternalSupervisorHost(mode='test',checks=Checks())
            with self.assertRaisesRegex(ExternalHostError,'WORKER_RESPONSE_JSON_INVALID'): host.run_architecture(snap,pool,out,root/'parent')
            self.assertFalse(out.exists())

    def test_negative_worker_root_inside_repository_is_rejected(self):
        with self.assertRaisesRegex(ExternalHostError,'WORKER_ROOT_MUST_BE_OUTSIDE_REPOSITORY'):
            PersistentArticleWorkerPool([sys.executable,'worker.py'],REPO/'forbidden-worker-root')

    def test_negative_production_host_rejects_non_external_pool_before_backend_load(self):
        host=ExternalSupervisorHost(mode='production')
        with self.assertRaisesRegex(ExternalHostError,'EXTERNAL_WORKER_POOL_REQUIRED'):
            host.run_production(Path('x.json'),object(),Path('o.json'),Path('parent'))

    def test_negative_production_host_requires_cross_uid_before_backend_load(self):
        with tempfile.TemporaryDirectory() as td:
            root=self._root(td); worker=root/'worker.py'; write_worker(worker)
            pool=PersistentArticleWorkerPool([sys.executable,str(worker)],root/'workers')
            host=ExternalSupervisorHost(mode='production')
            with self.assertRaisesRegex(ExternalHostError,'PRODUCTION_CROSS_UID_BOUNDARY_REQUIRED'):
                host.run_production(root/'s.json',pool,root/'o.json',root/'parent')
            pool.close()

    def test_negative_cross_uid_production_requires_private_authority_root_before_backend_load(self):
        if os.geteuid() != 0 or shutil.which('runuser') is None:
            self.skipTest('cross-uid test requires root + runuser')
        with tempfile.TemporaryDirectory() as td:
            root=self._root(td); worker=root/'worker.py'; write_worker(worker); snap=root/'s.json'; snapshot(snap,1)
            pool=PersistentArticleWorkerPool([sys.executable,str(worker)],root/'workers',run_as_user='nobody',require_cross_uid=True)
            host=ExternalSupervisorHost(mode='production')
            with self.assertRaisesRegex(ExternalHostError,'HOST_AUTHORITY_ROOT_REQUIRED'):
                host.run_production(snap,pool,root/'o.json',root/'parent')
            self.assertEqual(pool.runtime_pids(),[])
            self.assertFalse((root/'o.json').exists())
            pool.close()


if __name__=='__main__': unittest.main(verbosity=2)
