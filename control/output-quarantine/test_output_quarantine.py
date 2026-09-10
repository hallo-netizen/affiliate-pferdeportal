#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("MODULE_LOAD_FAILED")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check(condition: bool, message: str):
    if not condition:
        raise AssertionError(message)


def main() -> int:
    policy = json.loads((HERE / "OUTPUT_VISIBILITY_POLICY.json").read_text(encoding="utf-8"))
    check(policy["chat_execution_authority"] == "NONE", "CHAT_EXECUTION_AUTHORITY")
    check(policy["chat_output_authority"] == "NONE", "CHAT_OUTPUT_AUTHORITY")
    check(policy["visible_project_result_authority"] == "RELEASE_RECEIPT_ONLY", "VISIBLE_RESULT_AUTHORITY")
    check(policy["staging_is_not_visible_project_result"] is True, "STAGING_VISIBILITY")
    check(policy["visible_release_only_after_107008_pass_and_rearm"] is True, "FINAL_RELEASE_TIMING")
    check(policy["domain_logic_authority"] == "NONE", "DOMAIN_AUTHORITY")
    check(policy["quality_authority"] == "NONE", "QUALITY_AUTHORITY")
    check(policy["publish_allowed"] is False, "PUBLISH")
    check(policy["unbound_output_policy"] == "QUARANTINE_INVALID_NEVER_SURFACE_AS_PROJECT_RESULT", "UNBOUND_POLICY")

    gate = load_module(HERE / "output_release_gate.py", "output_release_gate_test")
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        q = base / ".pferde-quarantine"
        q.mkdir()
        f = q / "x.bin"
        f.write_bytes(b"ok")
        digest = hashlib.sha256(b"ok").hexdigest()

        old_repo = gate.REPO
        gate.REPO = base
        try:
            verified = gate.verify_quarantine_outputs(
                {"worker_quarantine_root": ".pferde-quarantine"},
                [{"ref": ".pferde-quarantine/x.bin", "sha256": digest}],
            )
            check(len(verified) == 1, "POSITIVE_OUTPUT_VERIFY")
            for bad_ref, bad_hash, reason in [
                ("outside/x.bin", digest, "OUTPUT_OUTSIDE_QUARANTINE"),
                (".pferde-quarantine/x.bin", "0" * 64, "OUTPUT_HASH_MISMATCH"),
            ]:
                try:
                    gate.verify_quarantine_outputs(
                        {"worker_quarantine_root": ".pferde-quarantine"},
                        [{"ref": bad_ref, "sha256": bad_hash}],
                    )
                    raise AssertionError("NEGATIVE_NOT_BLOCKED:" + reason)
                except gate.Blocked as exc:
                    check(str(exc).startswith(reason), "NEGATIVE_REASON:" + reason)
        finally:
            gate.REPO = old_repo

    files = [
        "worker_freshness_guard.py",
        "output_release_gate.py",
        "runtime_entry_gate.py",
        "final_review_visibility_guard.py",
    ]
    forbidden_content_mutation_tokens = [
        "body_html", "body_text", "post_content", "rewrite_article",
        "keyword_density", "quality_score", "seo_score", "design_score",
    ]
    for name in files:
        source = (HERE / name).read_text(encoding="utf-8")
        for token in forbidden_content_mutation_tokens:
            check(token not in source, "CONTENT_OR_QUALITY_MUTATION_TOKEN:" + name + ":" + token)

    worker_path = HERE / "worker_freshness_guard.py"
    worker_source = worker_path.read_text(encoding="utf-8")
    check(
        "PFERDE_ATELIER_CODEX_PRODUCTION_ENVIRONMENT_PREFLIGHT_V" not in worker_source,
        "SECOND_PREFLIGHT_CONTRACT_TRUTH_IN_CONSUMER",
    )
    worker = load_module(worker_path, "worker_freshness_contract_test")
    producer = load_module(worker.PREFLIGHT_PRODUCER, "preflight_contract_producer_test")
    expected_contract = worker.expected_preflight_contract()
    check(expected_contract == producer.CONTRACT, "PRODUCER_CONSUMER_CONTRACT_NOT_SINGLE_TRUTH")

    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        statep = base / "state.json"
        bundlep = base / "bundle.json"
        statep.write_text("{}\n", encoding="utf-8")
        bundlep.write_text("{}\n", encoding="utf-8")
        head = "1" * 40
        runtime = {
            "status": "EXECUTION_READY",
            "generation": 1,
            "batch_sha256": "2" * 64,
            "production_package_ref": "x",
            "production_package_sha256": "3" * 64,
        }
        state = {
            "next_allowed_step": "RUN_NEW_ARTICLE_BATCH_NO_STOP",
            "execution_gate": {"sequence": 107007},
        }
        proof = {
            "contract": expected_contract,
            "status": "CODEX_PRODUCTION_PREFLIGHT_PASS",
            "repository": worker.EXPECTED_REPOSITORY,
            "main_authority_source": "CODEX_CHECKOUT_REMOTE_TRACKING_MAIN",
            "expected_main_sha": head,
            "local_head_sha": head,
            "ed25519_runtime": True,
            "chat_execution_authority": "NONE",
            "chat_output_authority": "NONE",
            "domain_logic_authority": "NONE",
            "quality_authority": "NONE",
            "content_semantics_inspected": False,
            "workflow_navigation_decision": False,
            "publish_allowed": False,
            "runtime_status": "EXECUTION_READY",
            "generation": 1,
            "batch_sha256": "2" * 64,
            "production_package_ref": "x",
            "production_package_sha256": "3" * 64,
            "step_id": "RUN_NEW_ARTICLE_BATCH_NO_STOP",
            "sequence": 107007,
            "state_sha256": worker.sha256(statep),
            "bundle_sha256": worker.sha256(bundlep),
        }
        worker.validate_environment_proof(
            proof,
            expected_contract=expected_contract,
            head=head,
            state=state,
            statep=statep,
            bundlep=bundlep,
            runtime=runtime,
        )
        tampered = dict(proof)
        tampered["contract"] = expected_contract + "_TAMPERED"
        try:
            worker.validate_environment_proof(
                tampered,
                expected_contract=expected_contract,
                head=head,
                state=state,
                statep=statep,
                bundlep=bundlep,
                runtime=runtime,
            )
            raise AssertionError("TAMPERED_PREFLIGHT_CONTRACT_NOT_BLOCKED")
        except worker.Blocked as exc:
            check(str(exc) == "CODEX_ENVIRONMENT_PROOF_CONTRACT_INVALID", "TAMPERED_CONTRACT_REASON")

        original_producer = worker.PREFLIGHT_PRODUCER
        try:
            worker.PREFLIGHT_PRODUCER = base / "missing.py"
            try:
                worker.expected_preflight_contract()
                raise AssertionError("MISSING_PREFLIGHT_CONTRACT_SOURCE_NOT_BLOCKED")
            except worker.Blocked as exc:
                check(
                    str(exc) == "CODEX_ENVIRONMENT_PROOF_CONTRACT_SOURCE_MISSING",
                    "MISSING_CONTRACT_SOURCE_REASON",
                )
            invalid = base / "invalid.py"
            invalid.write_text("CONTRACT = None\n", encoding="utf-8")
            worker.PREFLIGHT_PRODUCER = invalid
            try:
                worker.expected_preflight_contract()
                raise AssertionError("INVALID_PREFLIGHT_CONTRACT_SOURCE_NOT_BLOCKED")
            except worker.Blocked as exc:
                check(
                    str(exc) == "CODEX_ENVIRONMENT_PROOF_CONTRACT_SOURCE_INVALID",
                    "INVALID_CONTRACT_SOURCE_REASON",
                )
        finally:
            worker.PREFLIGHT_PRODUCER = original_producer

    bind_check = worker_source.index("for ref, digest in required.items():")
    contract_read = worker_source.index("expected_contract = expected_preflight_contract()")
    check(bind_check < contract_read, "PREFLIGHT_CONTRACT_SOURCE_MUST_BE_HASH_BOUND_BEFORE_READ")

    runtime_source = (HERE / "runtime_entry_gate.py").read_text(encoding="utf-8")
    check("prepare_107007" in runtime_source, "PREPARE_107007_MISSING")
    check("authorize_final_107008" in runtime_source, "FINAL_AUTH_MISSING")
    check("commit_after_rearm" in runtime_source, "COMMIT_AFTER_REARM_MISSING")
    check("BOUND_PREPARED_RELEASE_REF.json" in runtime_source, "FINAL_REVIEW_PREPARED_BINDING_MISSING")

    idx_prepare = runtime_source.index("prepare_107007")
    idx_advance = runtime_source.index("advanced = c.complete(receipt_path)")
    check(idx_prepare < idx_advance, "107007_PREPARE_MUST_PRECEDE_STATE_ADVANCE")

    idx_auth = runtime_source.index("authorize_final_107008")
    idx_finish = runtime_source.index("finished = c.complete(receipt_path)")
    idx_commit = runtime_source.index("commit_after_rearm")
    check(idx_auth < idx_finish < idx_commit, "VISIBLE_RELEASE_MUST_FOLLOW_107008_PASS_AND_REARM")

    print("OUTPUT_QUARANTINE_ROOTFIX_TEST_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
