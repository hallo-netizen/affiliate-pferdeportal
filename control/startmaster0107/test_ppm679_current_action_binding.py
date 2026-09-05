from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ACTION = HERE.parent / "single-door-boundary" / "codex_current_action.py"

def module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

action = module(ACTION, "ppm679_current_action_test")

class PPM679BindingTest(unittest.TestCase):
    def prepare(self):
        temp = tempfile.TemporaryDirectory()
        repo = Path(temp.name)
        root = "out/"
        final_ref = root + "ARTICLE.html"
        report_ref = root + "PPM_REPORT.json"
        final = repo / final_ref
        final.parent.mkdir(parents=True, exist_ok=True)
        final.write_text("<p>final</p>", encoding="utf-8")
        final_sha = action.sha(final)
        report = {
            "ok": True,
            "technical_status": "TECHNICAL_CHECK_OK",
            "content_quality_status": "CONTENT_QUALITY_CHECK_OK",
            "content_hash": final_sha,
            "checks": {
                "content_hash": final_sha,
                "fail_closed_aggregate_status": "PASS",
                "draft_create_allowed": False,
                "publish_allowed": False,
            },
        }
        report_path = repo / report_ref
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        report_sha = action.sha(report_path)
        proof = {
            "input_sha256": final_sha,
            "artifacts": [
                {"ref": final_ref, "sha256": final_sha},
                {"ref": report_ref, "sha256": report_sha},
            ],
            "ppm679_binding": {
                "ppm_version": action.PPM679_VERSION,
                "ppm_package_sha256": action.PPM679_PACKAGE_SHA256,
                "article_type_templates_sha256": action.ARTICLE_TYPE_TEMPLATES_SHA,
                "final_article_ref": final_ref,
                "final_article_sha256": final_sha,
                "ppm_report_ref": report_ref,
                "ppm_report_sha256": report_sha,
            },
        }
        outputs = [{"ref": final_ref, "sha256": final_sha}]
        return temp, repo, root, proof, outputs, report_path

    def test_pre_ppm_binding_requires_only_final_article(self):
        requirement = action._ppm_requirement()
        self.assertEqual(["final_article_ref", "final_article_sha256"], requirement["pre_ppm_binding_required_fields"])
        self.assertNotIn("ppm_report_ref", requirement["pre_ppm_binding_required_fields"])

    def test_final_ppm_binding_still_requires_real_report(self):
        requirement = action._ppm_requirement()
        self.assertIn("ppm_report_ref", requirement["final_ppm679_binding_required_fields"])
        self.assertIn("ppm_report_sha256", requirement["final_ppm679_binding_required_fields"])

    def test_exact_ppm_result_binding_passes(self):
        temp, repo, root, proof, outputs, _ = self.prepare()
        try:
            action._validate_ppm_stage(repo, root, proof, outputs)
        finally:
            temp.cleanup()

    def test_generic_fake_ppm_pass_is_blocked(self):
        temp, repo, root, proof, outputs, _ = self.prepare()
        try:
            proof.pop("ppm679_binding")
            with self.assertRaises(action.ViewError):
                action._validate_ppm_stage(repo, root, proof, outputs)
        finally:
            temp.cleanup()

    def test_wrong_final_content_hash_is_blocked(self):
        temp, repo, root, proof, outputs, report_path = self.prepare()
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
            report["content_hash"] = "0" * 64
            report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            proof["ppm679_binding"]["ppm_report_sha256"] = action.sha(report_path)
            proof["artifacts"][1]["sha256"] = action.sha(report_path)
            with self.assertRaises(action.ViewError):
                action._validate_ppm_stage(repo, root, proof, outputs)
        finally:
            temp.cleanup()

    def test_wrong_ppm_package_hash_is_blocked(self):
        temp, repo, root, proof, outputs, _ = self.prepare()
        try:
            proof["ppm679_binding"]["ppm_package_sha256"] = "0" * 64
            with self.assertRaises(action.ViewError):
                action._validate_ppm_stage(repo, root, proof, outputs)
        finally:
            temp.cleanup()

if __name__ == "__main__":
    unittest.main()
