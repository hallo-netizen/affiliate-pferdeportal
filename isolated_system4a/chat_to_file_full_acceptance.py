#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SYSTEM4 = REPO / "isolated_system4"
CONTRACT = "SYSTEM4A_CHAT_TO_FILE_FULL_ACCEPTANCE_V1"
MANIFEST_CONTRACT = "SYSTEM4_PROVEN_RUNTIME_MANIFEST_V1"
HANDOFF_CONTRACT = "SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2"

# Exact locally proven Punkt-0/Supervisor candidate. A documentation head,
# partial transfer or similar runtime must never be accepted as a substitute.
REQUIRED_PROVEN_RUNTIME = {
    "proof_head": "cd6c134a3ee27f4535ea91bfe6cc223a34c9eb25",
    "point0_snapshot.py": "4dab3cc58da04cf2d5d53f22bc7e837b3cca7c88",
    "supervisor.py": "0afb25204fe8cac1dc24912f638451842a68399b",
    "root_supervisor_bridge.py": "2c9e0ce6e22efee20ceedfef5e3ba37c044eeb2f",
    "worker_dispatch.py": "608627f4d9d1b09758e42fd7ece4690fe9761575",
    "codex_entry.py": "c74044a85e9da6de3e9af6472555306e8f6fb28c",
    "root_entry.py": "b533e8223351ef291be6b624bb803b9f888d5268",
}

# Historical failures that previously escaped one or more green test routes.
# The bound live entry must prove these at the corresponding real boundary;
# this outer gate additionally prevents route/byte substitution before execution.
KNOWN_LIVE_ESCAPE_CLASSES = [
    "wrong_or_missing_chat_trigger_binding",
    "wrong_runtime_bytes_or_partial_remote_transfer",
    "point0_missing_or_mutated",
    "legacy_root_entry_used_instead_of_start_point0",
    "root_snapshot_or_manifest_binding_missing",
    "supervisor_not_external_authority",
    "worker_private_path_inaccessible_cross_uid",
    "private_python_interpreter_leak",
    "worker_factory_signature_drift",
    "worker_exits_without_response",
    "worker_can_return_authority_fields",
    "research_not_bound_to_point0_sources",
    "facts_not_bound_to_accepted_research",
    "unknown_or_foreign_fact_id",
    "context_snapshot_mismatch",
    "prebound_quality_binding",
    "quality_binding_missing_at_ppm_rebind",
    "noncanonical_category",
    "wrong_or_missing_plan_slot",
    "wrong_internal_link_binding",
    "prebound_runtime_links",
    "missing_textmachine_authoring_binding",
    "repair_restarts_article_or_mutates_context",
    "languagetool_dependency_missing_or_wrong_hash",
    "languagetool_not_executed_through_fullcheck",
    "ppm_dependency_missing_or_wrong_hash",
    "ppm_not_actually_executed",
    "synthetic_or_pregenerated_checker_pass",
    "ppm_content_hash_not_final_article_hash",
    "required_table_or_design_contract_missing",
    "batch_drops_duplicates_or_reorders_articles",
    "batch_context_mismatch",
    "handoff_schema_or_canonical_bytes_mismatch",
    "inline_part_missing_duplicate_reordered_or_tampered",
    "parent_chat_reconstruction_not_byte_identical",
    "publish_allowed_not_false",
]

class AcceptanceBlocked(RuntimeError):
    pass


def require(ok: bool, code: str) -> None:
    if not ok:
        raise AcceptanceBlocked(code)


def git_blob(path: Path) -> str:
    cp = subprocess.run(["git", "hash-object", str(path)], cwd=REPO,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        text=True, check=False)
    require(cp.returncode == 0, "RUNTIME_GIT_BLOB_UNAVAILABLE:" + path.name)
    return cp.stdout.strip()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_trigger(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(value.get("contract") == CONTRACT, "CHAT_TRIGGER_CONTRACT_INVALID")
    count = value.get("article_count")
    require(isinstance(count, int) and 1 <= count <= 3,
            "CHAT_TRIGGER_ARTICLE_COUNT_MUST_BE_1_TO_3")
    require(value.get("publish_allowed") is False, "PUBLISH_ALLOWED_MUST_BE_FALSE")
    articles = value.get("articles")
    require(isinstance(articles, list) and len(articles) == count,
            "CHAT_TRIGGER_ARTICLE_COUNT_MISMATCH")
    for i, article in enumerate(articles):
        require(isinstance(article, dict), f"CHAT_TRIGGER_ARTICLE_INVALID:{i}")
        for field in ("article_type", "category", "plan_slot", "target_keyword", "title"):
            require(isinstance(article.get(field), str) and article[field].strip(),
                    f"CHAT_TRIGGER_FIELD_MISSING:{i}:{field}")
        require(len(article["plan_slot"]) == 64, f"CHAT_TRIGGER_PLAN_SLOT_INVALID:{i}")
    return value


def verify_runtime_identity() -> tuple[dict[str, Any], dict[str, str]]:
    # Known new-layer blobs are checked first so a partial transfer is visible explicitly.
    actual: dict[str, str] = {}
    for name, expected in REQUIRED_PROVEN_RUNTIME.items():
        if name == "proof_head":
            continue
        path = SYSTEM4 / name
        require(path.is_file(), "CURRENT_RUNTIME_FILE_MISSING:" + name)
        blob = git_blob(path)
        actual[name] = blob
        require(blob == expected,
                "CURRENT_RUNTIME_IDENTITY_MISMATCH:" + name + ":" + blob + ":EXPECTED:" + expected)

    # The complete locally proven candidate (notably controller.py) must be transferred
    # atomically and recorded here. Missing manifest = hard stop, never a degraded test.
    manifest_path = SYSTEM4 / "CURRENT_PROVEN_RUNTIME_MANIFEST.json"
    require(manifest_path.is_file(), "CURRENT_PROVEN_RUNTIME_MANIFEST_MISSING")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest.get("contract") == MANIFEST_CONTRACT,
            "CURRENT_PROVEN_RUNTIME_MANIFEST_INVALID")
    require(manifest.get("proof_head") == REQUIRED_PROVEN_RUNTIME["proof_head"],
            "CURRENT_PROVEN_RUNTIME_PROOF_HEAD_MISMATCH")
    blobs = manifest.get("git_blobs")
    require(isinstance(blobs, dict) and isinstance(blobs.get("controller.py"), str),
            "CURRENT_PROVEN_CONTROLLER_BINDING_MISSING")
    for name, expected in blobs.items():
        path = SYSTEM4 / name
        require(path.is_file(), "BOUND_RUNTIME_FILE_MISSING:" + name)
        actual_blob = git_blob(path)
        require(actual_blob == expected,
                "BOUND_RUNTIME_FILE_MISMATCH:" + name + ":" + actual_blob + ":EXPECTED:" + expected)
        actual[name] = actual_blob

    # No test-only orchestration is allowed to impersonate the live route. The manifest
    # must identify one exact, hash-bound entry that is also the future production entry.
    entry_rel = manifest.get("chat_to_file_entry")
    entry_sha = manifest.get("chat_to_file_entry_sha256")
    require(isinstance(entry_rel, str) and entry_rel.startswith("isolated_system4/"),
            "BOUND_CHAT_TO_FILE_ENTRY_MISSING")
    entry = REPO / entry_rel
    require(entry.is_file(), "BOUND_CHAT_TO_FILE_ENTRY_FILE_MISSING")
    require(isinstance(entry_sha, str) and sha256_file(entry) == entry_sha,
            "BOUND_CHAT_TO_FILE_ENTRY_SHA_MISMATCH")
    return manifest, actual


def run_bound_live_entry(manifest: dict[str, Any], trigger: Path, work_root: Path,
                         lt_jar: Path) -> dict[str, Any]:
    entry = REPO / manifest["chat_to_file_entry"]
    command = [
        "python3", str(entry),
        "--chat-trigger", str(trigger),
        "--workspace", str(work_root),
        "--worker-mode", "simulation-no-codex",
        "--languagetool-jar", str(lt_jar),
    ]
    cp = subprocess.run(command, cwd=REPO, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, text=True, check=False)
    require(cp.returncode == 0,
            "BOUND_LIVE_ENTRY_BLOCKED:RC=" + str(cp.returncode) + ":" + (cp.stdout + cp.stderr)[-1200:])
    try:
        result = json.loads(cp.stdout.strip().splitlines()[-1])
    except Exception as exc:
        raise AcceptanceBlocked("BOUND_LIVE_ENTRY_RESULT_JSON_INVALID") from exc
    return result


def verify_terminal(result: dict[str, Any], count: int, work_root: Path) -> dict[str, Any]:
    require(result.get("status") == "SYSTEM4_CHAT_TO_FILE_PASS",
            "FULL_ROUTE_NOT_PASS:" + str(result.get("status")))
    require(result.get("article_count") == count, "FINAL_ARTICLE_COUNT_MISMATCH")
    require(result.get("codex_used") is False, "CODEX_USED_IN_SIMULATION")
    require(result.get("publish_allowed") is False, "FINAL_PUBLISH_ALLOWED_INVALID")
    require(result.get("point0_pass") is True, "POINT0_NOT_PROVEN")
    require(result.get("root_pass") is True, "ROOT_NOT_PROVEN")
    require(result.get("supervisor_pass") is True, "SUPERVISOR_NOT_PROVEN")
    require(result.get("worker_boundary_pass") is True, "WORKER_BOUNDARY_NOT_PROVEN")
    require(result.get("languagetool", {}).get("version") == "6.8" and
            result.get("languagetool", {}).get("executed") is True and
            result.get("languagetool", {}).get("status") == "PASS",
            "LANGUAGETOOL_REAL_PASS_NOT_PROVEN")
    require(result.get("ppm679", {}).get("version") == "6.7.9" and
            result.get("ppm679", {}).get("executed") is True and
            result.get("ppm679", {}).get("status") == "PASS",
            "PPM679_REAL_PASS_NOT_PROVEN")
    require(result.get("batch_pass") is True, "BATCH_NOT_PROVEN")
    require(result.get("handoff_contract") == HANDOFF_CONTRACT, "HANDOFF_CONTRACT_INVALID")
    require(result.get("inline_unpack_pass") is True, "INLINE_UNPACK_NOT_PROVEN")
    require(result.get("parent_chat_byte_equal") is True, "PARENT_CHAT_NOT_BYTE_IDENTICAL")
    output = work_root / HANDOFF_CONTRACT.replace("_V2", "_V2.json")
    # Entry may expose a different exact output path; it must at least report and bind it.
    reported = result.get("output_path")
    if isinstance(reported, str):
        output = Path(reported)
    require(output.is_file(), "FINAL_PARENT_CHAT_FILE_MISSING")
    require(isinstance(result.get("output_sha256"), str) and
            sha256_file(output) == result["output_sha256"], "FINAL_FILE_SHA_MISMATCH")
    return result


def run_simulation(trigger: Path, work_root: Path, lt_jar: Path) -> dict[str, Any]:
    request = load_trigger(trigger)
    # Identity comes before Point 0/research/article work: no more false-green old runtimes.
    manifest, identity = verify_runtime_identity()
    require(lt_jar.is_file(), "LANGUAGETOOL_JAR_MISSING")
    require(sha256_file(lt_jar) ==
            "2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8",
            "LANGUAGETOOL_JAR_SHA_MISMATCH")
    ppm = REPO / "control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
    require(ppm.is_file(), "PPM679_PACKAGE_MISSING")
    require(sha256_file(ppm) ==
            "acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1",
            "PPM679_PACKAGE_SHA_MISMATCH")
    result = run_bound_live_entry(manifest, trigger, work_root, lt_jar)
    verify_terminal(result, request["article_count"], work_root)
    return {
        "status": "SYSTEM4A_CHAT_TO_FILE_FULL_ACCEPTANCE_PASS",
        "article_count": request["article_count"],
        "codex_used": False,
        "runtime_identity": identity,
        "historical_escape_classes_bound": len(KNOWN_LIVE_ESCAPE_CLASSES),
        "publish_allowed": False,
        "live_result": result,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--trigger", required=True)
    p.add_argument("--work-root", required=True)
    p.add_argument("--lt-jar", required=True)
    args = p.parse_args(argv)
    try:
        result = run_simulation(Path(args.trigger), Path(args.work_root), Path(args.lt_jar))
    except Exception as exc:
        print(json.dumps({
            "status": "SYSTEM4A_CHAT_TO_FILE_FULL_ACCEPTANCE_BLOCKED",
            "first_blocker": str(exc),
            "codex_used": False,
            "publish_allowed": False,
            "historical_escape_classes_bound": len(KNOWN_LIVE_ESCAPE_CLASSES),
        }, ensure_ascii=False, sort_keys=True))
        return 4
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
