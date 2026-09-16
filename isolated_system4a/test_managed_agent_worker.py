import hashlib
import unittest
from managed_agent_worker import ManagedAgentWorkerPool, ManagedAgentWorkerError


def article(i=0):
    return {'title':f'T{i}','target_keyword':f'K{i}','category':'c','article_type':'Neue Art','plan_slot':hashlib.sha256(f's{i}'.encode()).hexdigest()}


def req(task='research', i=0, **extra):
    value={'task':task,'article':article(i)}; value.update(extra); return value


class FakeTransport:
    def __init__(self, isolated=True):
        self.isolated=isolated; self.created=[]; self.turns=[]; self.deleted=[]; self.n=0
    def authority_isolated(self): return self.isolated
    def create_session(self, *, input_text, plan_slot):
        self.n+=1; sid=f'sess-{self.n}'; self.created.append((sid,plan_slot,input_text)); return sid
    def run_turn(self, session_id, *, input_text):
        self.turns.append((session_id,input_text)); return 'CONTENT:'+session_id+':'+str(len(self.turns))
    def delete_session(self, session_id): self.deleted.append(session_id)


class ManagedWorkerTests(unittest.TestCase):
    def test_positive_one_persistent_session_per_article(self):
        t=FakeTransport(); pool=ManagedAgentWorkerPool(t)
        a=pool.request(req('research',0)); b=pool.request(req('facts',0,research='r')); c=pool.request(req('research',1))
        self.assertEqual(len(t.created),2); self.assertEqual(pool.session_bindings()[article(0)['plan_slot']]['turns'],2)
        self.assertEqual(set(a),{'content'}); self.assertEqual(set(b),{'content'}); self.assertEqual(set(c),{'content'})
        self.assertEqual(pool.runtime_pids(),[]); self.assertEqual(pool.max_runtime_processes(),0); self.assertTrue(pool.authority_isolated())
        pool.close(); self.assertCountEqual(t.deleted,['sess-1','sess-2'])
    def test_negative_transport_without_authority_isolation(self):
        with self.assertRaisesRegex(ManagedAgentWorkerError,'MANAGED_AGENT_AUTHORITY_BOUNDARY_INVALID'): ManagedAgentWorkerPool(FakeTransport(False))
    def test_negative_authority_field_in_request(self):
        pool=ManagedAgentWorkerPool(FakeTransport())
        with self.assertRaisesRegex(ManagedAgentWorkerError,'MANAGED_WORKER_AUTHORITY_FIELD_FORBIDDEN'): pool.request(req('research',0,phase='ARTICLE_PASS'))
    def test_negative_article_schema_extra_control_field(self):
        t=FakeTransport(); pool=ManagedAgentWorkerPool(t); bad=req(); bad['article']=dict(bad['article']); bad['article']['checks']='PASS'
        with self.assertRaisesRegex(ManagedAgentWorkerError,'MANAGED_WORKER_ARTICLE_INVALID'): pool.request(bad)
    def test_negative_closed_pool(self):
        pool=ManagedAgentWorkerPool(FakeTransport()); pool.close()
        with self.assertRaisesRegex(ManagedAgentWorkerError,'MANAGED_AGENT_POOL_CLOSED'): pool.request(req())

if __name__=='__main__': unittest.main(verbosity=2)
