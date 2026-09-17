from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("system4_107008_handoff_tested", HERE / "system4_107008_handoff.py")
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class System4V2To107008Test(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "batch-collect").mkdir(parents=True)
        evidence = self.root / "batch-collect" / "system4_batch_evidence.json"
        evidence.write_text("{}\n", encoding="utf-8")
        self.batch_sha = "a" * 64
        batch = {
            "contract": "SYSTEM4_107007_PRODUCTION_BATCH_V1",
            "status": "ITEMS_COMPLETE",
            "sequence": 107007,
            "batch_sha256": self.batch_sha,
            "item_count": 1,
            "current_index": 1,
            "completed_indices": [0],
            "started_indices": [0],
            "batch_collect": {
                "status": "SYSTEM4_BATCH_FULL_PASS_COLLECTED",
                "batch_sha256": self.batch_sha,
                "article_count": 1,
                "batch_evidence_path": str(evidence),
                "batch_evidence_sha256": mod.sha256(evidence),
                "publish_allowed": False,
            },
            "publish_allowed": False,
        }
        (self.root / mod.BATCH_STATE).write_text(json.dumps(batch) + "\n", encoding="utf-8")
        item = self.root / "item-000000"
        item.mkdir()
        state = {
            "phase": "OUTPUT_GATE_REQUIRED",
            "revision": 1,
            "draft_sha256": "b" * 64,
            "draft_markdown": "body",
            "article": {
                "title": "T",
                "target_keyword": "K",
                "category": "C",
                "article_type": "Beratung",
                "plan_slot": "c" * 64,
            },
            "production_context": {"fact_pack": {}, "production_plan_item": {}},
            "checks": {
                "status": "PASS",
                "production_evidence": {
                    "evidence": {
                        "languagetool": {"status": "PASS", "finding_count": 0, "engine": "LanguageTool 6.8 / Bestand 43"},
                        "ppm679": {"status": "PASS", "ppm_version": "6.7.9"},
                    }
                },
            },
        }
        (item / "state.json").write_text(json.dumps(state) + "\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def fake_canonicalize(self, inp: Path, out: Path):
        raw = inp.read_bytes()
        out.write_bytes(raw)
        return raw

    def fake_pack(self, inp: Path, out: Path):
        out.write_text("INLINE\n", encoding="utf-8")
        return {"plaintext_sha256": mod.sha256(inp), "byte_length": inp.stat().st_size, "part_count": 1, "compressed_sha256": "d" * 64}

    def fake_unpack(self, inline: Path, outdir: Path):
        outdir.mkdir(parents=True, exist_ok=True)
        src = self.root / "107008-handoff" / ("CANONICAL_" + mod.HANDOFF_NAME)
        dst = outdir / mod.HANDOFF_NAME
        dst.write_bytes(src.read_bytes())
        return dst

    def patches(self):
        payload = {"batch_sha256": self.batch_sha, "articles": [{}]}
        return (
            mock.patch.object(mod.handoff_transport, "validate_handoff", return_value=payload),
            mock.patch.object(mod.handoff_transport, "canonicalize_handoff", side_effect=self.fake_canonicalize),
            mock.patch.object(mod.handoff_transport, "inline_pack", side_effect=self.fake_pack),
            mock.patch.object(mod.handoff_transport, "inline_unpack", side_effect=self.fake_unpack),
            mock.patch.object(mod.handoff_transport, "read_validate_handoff", return_value=(payload, b"x")),
        )

    def test_prepare_creates_single_v2_binding_for_107008(self):
        ps = self.patches()
        with ps[0], ps[1], ps[2], ps[3], ps[4]:
            result = mod.prepare(str(self.root))
            self.assertEqual(result["status"], "SYSTEM4_107008_V2_HANDOFF_BOUND")
            self.assertEqual(result["next_sequence"], 107008)
            self.assertEqual(result["article_count"], 1)
            binding = mod.validate_binding(Path(result["binding_ref"]))
            self.assertEqual(binding["handoff_sha256"], binding["reconstructed_sha256"])
            self.assertFalse(binding["publish_allowed"])

    def test_incomplete_batch_cannot_enter_107008(self):
        p = self.root / mod.BATCH_STATE
        state = json.loads(p.read_text(encoding="utf-8"))
        state["status"] = "ACTIVE"
        p.write_text(json.dumps(state) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(mod.Blocked, "BATCH_NOT_COMPLETE"):
            mod.build_payload(self.root)

    def test_start_runs_runtime_only_after_v2_binding(self):
        ps = self.patches()
        cp = mock.Mock(returncode=0, stdout=json.dumps({"status": "OFFICIAL_RUNTIME_ENTRY_PASS", "sequence": 107008}), stderr="")
        with ps[0], ps[1], ps[2], ps[3], ps[4], mock.patch.object(mod.subprocess, "run", return_value=cp) as run:
            result = mod.start(str(self.root))
            self.assertEqual(result["status"], "SYSTEM4_107008_V2_HANDOFF_ENTRY_PASS")
            self.assertEqual(result["batch_sha256"], self.batch_sha)
            run.assert_called_once()

    def test_binding_hash_tamper_blocks(self):
        ps = self.patches()
        with ps[0], ps[1], ps[2], ps[3], ps[4]:
            result = mod.prepare(str(self.root))
            handoff = Path(result["handoff_ref"])
            handoff.write_text("tampered\n", encoding="utf-8")
            with self.assertRaisesRegex(mod.Blocked, "HANDOFF_HASH_MISMATCH"):
                mod.validate_binding(Path(result["binding_ref"]))


if __name__ == "__main__":
    unittest.main()
