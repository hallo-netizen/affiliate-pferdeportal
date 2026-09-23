import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE=Path(__file__).resolve().parents[1]
REPO=HERE.parent
sys.path.insert(0,str(HERE))
import intake_bridge
import fresh_batch_executor as fresh


class FreshBatchExecutorTests(unittest.TestCase):
    def _sources(self, article):
        rows=[]
        for i in range(3):
            sentences=[
                f"Quelle {i+1} erläutert für {article['target_keyword']} einen fachlich relevanten und nachvollziehbaren Prüfpunkt mit genügend Kontext.",
                f"Ein weiterer belegter Hinweis zu {article['title']} beschreibt konkrete Zusammenhänge und Grenzen für die fachliche Einordnung.",
                f"Die dritte Passage dieser Quelle ergänzt einen eigenständigen Sachverhalt, der im späteren Artikel korrekt belegt werden kann.",
            ]
            evidence=" ".join(sentences)
            rows.append({
                "source_id":f"src-{article['item_index']}-{i}",
                "source_title":f"Fachquelle {article['item_index']}-{i}",
                "source_url":f"https://example.org/{article['item_index']}/{i}",
                "retrieved_at":"2026-09-23T08:00:00+00:00",
                "evidence":evidence,
                "snapshot_sha256":fresh.sha_text(evidence),
                "http_status":200,
                "source_kind":"UNIT_BOUND_SOURCE",
            })
        return rows

    def _facts(self, article, research):
        claims=[]
        number=0
        for source in research["sources"]:
            for sentence in [s.strip()+'.' for s in source["evidence"].split(". ") if s.strip()][:2]:
                number+=1
                claims.append({
                    "fact_id":f"fact-{article['plan_slot'][:12]}-{number}",
                    "source_id":source["source_id"],
                    "statement":f"Belegter Sachverhalt {number} für {article['target_keyword']} ist für die fachliche Einordnung relevant.",
                    "evidence_text":sentence,
                    "evidence_text_sha256":fresh.sha_text(sentence),
                })
        return {"contract":"SYSTEM4_FACTS_EVIDENCE_V1","claims":claims}

    def _context(self, article, facts):
        answer=(
            "Die Frage lässt sich nur anhand der konkreten Situation zuverlässig beantworten. "
            "Entscheidend sind die gebundenen fachlichen Hinweise, der aktuelle Zustand und die genannten Grenzen. "
            "Prüfe deshalb die im Artikel beschriebenen Punkte in ihrer Reihenfolge und beachte Abweichungen, "
            "bevor du eine Entscheidung triffst oder etwas veränderst."
        )
        return {
            "lead":"Die gebundenen Fakten ordnen das Thema sachlich ein und zeigen die wichtigsten Prüfpunkte.",
            "conclusion":"Die Entscheidung sollte sich an den belegten Fakten und den konkreten Rahmenbedingungen orientieren. Abweichungen müssen vor der Umsetzung geklärt werden.",
            "faq_direct_answer":answer if article["article_type"]=="FAQ" else "",
        }

    def test_current_16_builds_real_system4_bindings_and_exact_three_links(self):
        snapshot_path=HERE/"current/PSERC_METADATA_SNAPSHOT.json"
        snapshot=json.loads(snapshot_path.read_text(encoding="utf-8"))
        intake=intake_bridge.prepare(snapshot)
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            sp=root/"snapshot.json"; ip=root/"intake.json"; op=root/"binding.json"
            sp.write_text(json.dumps(snapshot,ensure_ascii=False),encoding="utf-8")
            ip.write_text(json.dumps(intake,ensure_ascii=False),encoding="utf-8")
            with mock.patch.object(fresh,"_acquire_sources",side_effect=self._sources), \
                 mock.patch.object(fresh,"_facts_from_model",side_effect=self._facts), \
                 mock.patch.object(fresh,"_context_text",side_effect=self._context):
                binding=fresh.build(sp,ip,op)
            self.assertEqual(binding["item_count"],16)
            self.assertEqual(binding["batch_sha256"],snapshot["next_textmachine_metadata_batch"]["batch_sha256"])
            self.assertFalse(binding["publish_allowed"])
            for item in binding["items"]:
                self.assertEqual(item["research_binding"]["status"],"BOUND")
                self.assertEqual(item["authoring_binding"]["status"],"BOUND")
                self.assertEqual(len(item["authoring_binding"]["internal_links"]),3)
                bound=item["system4_bound"]
                self.assertEqual(bound["contract"],fresh.SYSTEM4_BOUND_CONTRACT)
                core=copy.deepcopy(bound); declared=core.pop("binding_sha256")
                self.assertEqual(declared,fresh.stable(core))

    def test_intake_tamper_blocks(self):
        snapshot=json.loads((HERE/"current/PSERC_METADATA_SNAPSHOT.json").read_text(encoding="utf-8"))
        intake=intake_bridge.prepare(snapshot)
        intake["items"][0]["title"]="manipuliert"
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); sp=root/"s.json"; ip=root/"i.json"; op=root/"o.json"
            sp.write_text(json.dumps(snapshot),encoding="utf-8")
            ip.write_text(json.dumps(intake),encoding="utf-8")
            with self.assertRaisesRegex(fresh.Blocked,"INTAKE_NOT_EXACT_REPREPARATION"):
                fresh.build(sp,ip,op)


if __name__=="__main__":
    unittest.main(verbosity=2)
