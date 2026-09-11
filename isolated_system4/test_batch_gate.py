import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import batch_gate


def sha_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def make_fixture(root: Path, count=7):
    items=[]
    for i in range(count):
        slot=hashlib.sha256(f"slot-{i}".encode()).hexdigest()
        items.append({
            "title": f"Titel {i}",
            "target_keyword": f"Keyword {i}",
            "category": f"kategorie-{i}",
            "article_type": "Beratung",
            "plan_slot": slot,
        })
    snapshot={
        "contract":"SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1",
        "next_textmachine_metadata_batch":{
            "contract":"PSERC_TEXTMACHINE_METADATA_BATCH_V2",
            "status":"READY_FOR_TEXTMACHINE_METADATA_INTAKE",
            "batch_sha256":hashlib.sha256(b"batch").hexdigest(),
            "item_count":count,
            "items":items,
            "publish_allowed":False,
        }
    }
    snap=root/"snapshot.json"; snap.write_text(json.dumps(snapshot,ensure_ascii=False),encoding="utf-8")
    snap_sha=hashlib.sha256(snap.read_bytes()).hexdigest(); batch_sha=snapshot["next_textmachine_metadata_batch"]["batch_sha256"]
    paths=[]
    for i,item in enumerate(items):
        draft=f"# {item['title']}\n\n## A\n\nText {i} {item['target_keyword']}\n\n## B\n\nMehr Text"
        fact={"contract":"canonical_fact_pack_v1","x":i}
        plan={"plan_slot":item["plan_slot"],"canonical_article":{"body_html":draft}}
        context={"fact_pack":fact,"production_plan_item":plan}
        state={
            "contract":batch_gate.STATE_CONTRACT,
            "source_snapshot_sha256":snap_sha,
            "batch_sha256":batch_sha,
            "article":item,
            "immutable_core_sha256":"",
            "publish_allowed":False,
            "phase":"OUTPUT_GATE_REQUIRED",
            "revision":1,
            "research":{"text":"research","sha256":sha_text("research")},
            "facts":{"text":"facts","sha256":sha_text("facts")},
            "production_context":{"fact_pack":fact,"production_plan_item":plan,"sha256":batch_gate.stable_hash(context)},
            "draft_markdown":draft,
            "draft_sha256":sha_text(draft),
            "checks":{"status":"PASS","mode":"FULL_PRODUCTION","errors":[],"checked_draft_sha256":sha_text(draft),"production_evidence":{"ok":True}},
            "last_error":None,
            "release_prepared":None,
            "released":False,
        }
        state["immutable_core_sha256"]=batch_gate.stable_hash(batch_gate.immutable_core(state))
        p=root/f"state-{i}.json"; p.write_text(json.dumps(state,ensure_ascii=False),encoding="utf-8"); paths.append(p)
    return snap,paths


class BatchGateTests(unittest.TestCase):
    def run_collect(self, mutate=None, count=7, path_count=None):
        td=tempfile.TemporaryDirectory(); root=Path(td.name); snap,paths=make_fixture(root,count=count)
        if mutate:
            mutate(root,snap,paths)
        if path_count is not None:
            paths=paths[:path_count]
        out=root/"out"
        try:
            result=batch_gate.collect_batch(snap,paths,out)
            return td,result,out,paths,snap
        except Exception:
            td.cleanup(); raise

    def assert_blocked(self, code, mutate=None, path_count=None):
        with self.assertRaisesRegex(batch_gate.BatchGateError, code):
            self.run_collect(mutate=mutate,path_count=path_count)

    def test_positive(self):
        td,result,out,paths,snap=self.run_collect()
        try:
            self.assertEqual(result["status"],"SYSTEM4_BATCH_FULL_PASS_COLLECTED")
            self.assertEqual(result["article_count"],7)
            self.assertEqual(result["next_required"],"SIGNED_WORKFLOW_RELEASE")
            self.assertFalse(result["publish_allowed"])
            self.assertEqual(len(list(out.glob("ARTICLE_*.md"))),7)
            evidence=json.loads((out/"system4_batch_evidence.json").read_text(encoding="utf-8"))
            self.assertEqual(evidence["article_count"],7)
            self.assertEqual(evidence["next_required"],"SIGNED_WORKFLOW_RELEASE")
        finally: td.cleanup()

    def test_missing_state(self): self.assert_blocked("STATE_COUNT_MISMATCH", path_count=6)
    def test_basic_check_blocked(self):
        def m(root,snap,paths):
            s=json.loads(paths[2].read_text()); s["checks"]["mode"]="BASIC_ARCHITECTURE"; paths[2].write_text(json.dumps(s))
        self.assert_blocked("FULL_PRODUCTION_PASS_REQUIRED",m)
    def test_failed_check_blocked(self):
        def m(root,snap,paths):
            s=json.loads(paths[2].read_text()); s["checks"]["status"]="FAIL"; paths[2].write_text(json.dumps(s))
        self.assert_blocked("FULL_PRODUCTION_PASS_REQUIRED",m)
    def test_draft_tamper_blocked(self):
        def m(root,snap,paths):
            s=json.loads(paths[2].read_text()); s["draft_markdown"]+="x"; paths[2].write_text(json.dumps(s))
        self.assert_blocked("STATE_DRAFT_HASH_INVALID",m)
    def test_publish_true_blocked(self):
        def m(root,snap,paths):
            s=json.loads(paths[2].read_text()); s["publish_allowed"]=True; paths[2].write_text(json.dumps(s))
        self.assert_blocked("STATE_PUBLISH_MUST_BE_FALSE",m)
    def test_wrong_batch_blocked(self):
        def m(root,snap,paths):
            s=json.loads(paths[2].read_text()); s["batch_sha256"]="0"*64; s["immutable_core_sha256"]=batch_gate.stable_hash(batch_gate.immutable_core(s)); paths[2].write_text(json.dumps(s))
        self.assert_blocked("STATE_BATCH_MISMATCH",m)
    def test_wrong_snapshot_blocked(self):
        def m(root,snap,paths):
            s=json.loads(paths[2].read_text()); s["source_snapshot_sha256"]="0"*64; s["immutable_core_sha256"]=batch_gate.stable_hash(batch_gate.immutable_core(s)); paths[2].write_text(json.dumps(s))
        self.assert_blocked("STATE_SOURCE_SNAPSHOT_MISMATCH",m)
    def test_metadata_tamper_blocked(self):
        def m(root,snap,paths):
            s=json.loads(paths[2].read_text()); s["article"]["title"]="Falsch"; s["immutable_core_sha256"]=batch_gate.stable_hash(batch_gate.immutable_core(s)); paths[2].write_text(json.dumps(s))
        self.assert_blocked("STATE_ARTICLE_BINDING_MISMATCH",m)
    def test_per_article_release_blocked(self):
        def m(root,snap,paths):
            s=json.loads(paths[2].read_text()); s["release_prepared"]={"x":1}; paths[2].write_text(json.dumps(s))
        self.assert_blocked("PER_ARTICLE_RELEASE_PREPARED_FORBIDDEN",m)
    def test_context_hash_blocked(self):
        def m(root,snap,paths):
            s=json.loads(paths[2].read_text()); s["production_context"]["sha256"]="0"*64; paths[2].write_text(json.dumps(s))
        self.assert_blocked("PRODUCTION_CONTEXT_HASH_INVALID",m)
    def test_duplicate_state_slot_blocked(self):
        def m(root,snap,paths):
            s0=json.loads(paths[0].read_text()); s1=json.loads(paths[1].read_text()); s1["article"]["plan_slot"]=s0["article"]["plan_slot"]; s1["immutable_core_sha256"]=batch_gate.stable_hash(batch_gate.immutable_core(s1)); paths[1].write_text(json.dumps(s1))
        self.assert_blocked("STATE_PLAN_SLOT_DUPLICATE",m)

if __name__=="__main__": unittest.main(verbosity=2)
