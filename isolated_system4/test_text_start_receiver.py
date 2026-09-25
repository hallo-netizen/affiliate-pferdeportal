from __future__ import annotations

import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import parent_start


class TextStartReceiverGuardTests(unittest.TestCase):
    def _fixture(self, root: Path):
        state = {
            "next_allowed_step": "RUN_NEW_ARTICLE_BATCH_NO_STOP",
            "publish_allowed": False,
            "execution_gate": {
                "step_id": "RUN_NEW_ARTICLE_BATCH_NO_STOP",
                "sequence": 107007,
            },
        }
        state_path = root / "CURRENT_STATE.json"
        state_raw = (json.dumps(state, sort_keys=True) + "\n").encode("utf-8")
        state_path.write_bytes(state_raw)

        start_here = {
            "current_state_sha256": hashlib.sha256(state_raw).hexdigest(),
            "next_allowed_step": "RUN_NEW_ARTICLE_BATCH_NO_STOP",
        }
        root_path = root / "PFERDE_ATELIER_START_HERE.json"
        root_path.write_text(json.dumps(start_here), encoding="utf-8")

        auth = {
            "contract": "PFERDE_ATELIER_TEXT_START_AUTH_V1",
            "status": "PASS",
            "source_repository": "hallo-netizen/text-start",
            "source_run_id": 123,
            "source_issue_number": 45,
            "target_repository": "hallo-netizen/affiliate-pferdeportal",
            "target_ref": "main",
            "target_head_sha": "a" * 40,
            "canonical_start_command": "python3 isolated_system4/parent_start.py start-current-bound",
            "article_content_rules_changed": False,
            "quality_rules_changed": False,
            "production_logic_changed": False,
            "publish_allowed": False,
        }
        auth_path = root / ".text-start-receiver-auth.json"
        auth_path.write_text(json.dumps(auth), encoding="utf-8")
        return state_path, root_path, auth_path, auth

    def _call(self, state_path: Path, root_path: Path, auth_path: Path):
        guard = parent_start.pre_codex_start_hardlock
        with mock.patch.object(guard, "STATE", state_path), \
             mock.patch.object(guard, "ROOT", root_path), \
             mock.patch.object(guard, "TEXT_START_AUTH", auth_path), \
             mock.patch.object(guard, "_git_head", return_value="a" * 40), \
             mock.patch.dict(os.environ, {
                 "GITHUB_REPOSITORY": "hallo-netizen/affiliate-pferdeportal",
                 "GITHUB_REF_NAME": "main",
                 "GITHUB_EVENT_NAME": "workflow_dispatch",
             }, clear=False):
            return guard._validate_text_start(parent_start.REPO)

    def test_valid_central_start_authorization_passes(self):
        with tempfile.TemporaryDirectory() as td:
            state, root, auth, _ = self._fixture(Path(td))
            result = self._call(state, root, auth)
            self.assertEqual(result["status"], "TEXT_START_PREFLIGHT_PASS")
            self.assertEqual(result["source_run_id"], 123)
            self.assertEqual(result["source_issue_number"], 45)
            self.assertIs(result["publish_allowed"], False)

    def test_tampered_start_command_is_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            state, root, auth, payload = self._fixture(Path(td))
            payload["canonical_start_command"] = "python3 anything_else.py"
            auth.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(
                parent_start.pre_codex_start_hardlock.StartAuthorizationBlocked,
                "TEXT_START_AUTH_FIELD_INVALID:canonical_start_command",
            ):
                self._call(state, root, auth)

    def test_wrong_target_head_is_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            state, root, auth, payload = self._fixture(Path(td))
            payload["target_head_sha"] = "b" * 40
            auth.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(
                parent_start.pre_codex_start_hardlock.StartAuthorizationBlocked,
                "TEXT_START_TARGET_HEAD_DRIFT",
            ):
                self._call(state, root, auth)

    def test_publish_or_route_drift_is_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            state, root, auth, payload = self._fixture(Path(td))
            payload["publish_allowed"] = True
            auth.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(
                parent_start.pre_codex_start_hardlock.StartAuthorizationBlocked,
                "TEXT_START_AUTH_FIELD_INVALID:publish_allowed",
            ):
                self._call(state, root, auth)

        with tempfile.TemporaryDirectory() as td:
            state, root, auth, _ = self._fixture(Path(td))
            current = json.loads(state.read_text(encoding="utf-8"))
            current["next_allowed_step"] = "ANYTHING_ELSE"
            raw = (json.dumps(current, sort_keys=True) + "\n").encode("utf-8")
            state.write_bytes(raw)
            start_here = json.loads(root.read_text(encoding="utf-8"))
            start_here["current_state_sha256"] = hashlib.sha256(raw).hexdigest()
            start_here["next_allowed_step"] = "ANYTHING_ELSE"
            root.write_text(json.dumps(start_here), encoding="utf-8")
            with self.assertRaisesRegex(
                parent_start.pre_codex_start_hardlock.StartAuthorizationBlocked,
                "TEXT_START_STEP_NOT_107007",
            ):
                self._call(state, root, auth)


if __name__ == "__main__":
    unittest.main()
