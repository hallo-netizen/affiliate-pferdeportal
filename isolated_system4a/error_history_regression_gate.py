from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent

# Every historical/user-mandated failure class must map to a real executable negative test.
# Missing executable coverage is itself terminal BLOCKED.
CATALOG = [
    ("private_worker_path", "test_worker_runtime_boundary.WorkerRuntimeBoundaryTests.test_negative_codex_like_private_temp_path_blocks_before_worker_start"),
    ("private_interpreter", "test_worker_runtime_boundary.WorkerRuntimeBoundaryTests.test_negative_private_interpreter_blocks_even_when_worker_is_accessible"),
    ("no_accessible_system_python", "test_worker_runtime_boundary.WorkerRuntimeBoundaryTests.test_negative_no_accessible_system_python_fails_closed"),
    ("supervisor_path_leak", "test_worker_runtime_boundary.WorkerRuntimeBoundaryTests.test_positive_worker_environment_does_not_inherit_supervisor_path"),
    ("worker_crash_surface", "test_worker_runtime_boundary.WorkerRuntimeBoundaryTests.test_negative_real_worker_crash_surfaces_exit_code_and_stderr"),
    ("codex_entry_cross_uid_switch", "test_codex_worker_entry.CodexWorkerEntryTests.test_negative_codex_entry_exposes_no_cross_uid_switch"),
    ("realinput_mismatch", "test_realcase_acceptance_gate.RealcaseAcceptanceGateTests.test_negative_raw_input_mismatch"),
    ("alternate_entry", "test_realcase_acceptance_gate.RealcaseAcceptanceGateTests.test_negative_alternate_entry"),
    ("fixture_plan_builder", "test_realcase_acceptance_gate.RealcaseAcceptanceGateTests.test_negative_fixture_plan_builder"),
    ("prebound_quality_binding", "test_realcase_context_gate.RealcaseContextGateTests.test_negative_prebound_quality_binding_is_blocked_before_normal_validation"),
    ("noncanonical_category", "test_production_ingress_category.ProductionIngressCategoryTests.test_negative_last_real_noncanonical_category_blocks_before_research"),
    ("prebound_runtime_links", "test_production_plan_binding.ProductionPlanBindingTests.test_negative_prebound_runtime_links_are_forbidden"),
    ("unknown_fact_id", "test_error_history_remaining.ErrorHistoryRemainingTests.test_unknown_fact_id"),
    ("fact_id_not_in_canonical_fact_pack", "test_error_history_remaining.ErrorHistoryRemainingTests.test_fact_id_not_in_canonical_fact_pack"),
    ("wrong_or_missing_plan_slot", "test_error_history_remaining.ErrorHistoryRemainingTests.test_wrong_or_missing_plan_slot"),
    ("context_runtime_mismatch", "test_error_history_remaining.ErrorHistoryRemainingTests.test_context_runtime_mismatch"),
    ("hash_manifest_mismatch", "test_error_history_remaining.ErrorHistoryRemainingTests.test_hash_manifest_mismatch"),
    ("wrong_link_binding", "test_error_history_remaining.ErrorHistoryRemainingTests.test_wrong_link_binding"),
    ("missing_required_fields", "test_error_history_remaining.ErrorHistoryRemainingTests.test_missing_required_fields"),
    ("wrong_article_identity", "test_error_history_remaining.ErrorHistoryRemainingTests.test_wrong_article_identity"),
    ("batch_article_context_mismatch", "test_error_history_remaining.ErrorHistoryRemainingTests.test_batch_article_context_mismatch"),
    ("handoff_manipulation", "test_error_history_remaining.ErrorHistoryRemainingTests.test_handoff_manipulation"),
    ("synthetic_pass_authority", "test_error_history_remaining.ErrorHistoryRemainingTests.test_synthetic_pass_authority"),
    ("ppm_quality_binding_missing", "test_error_history_remaining.ErrorHistoryRemainingTests.test_ppm_quality_binding_missing"),
    ("root_bound_snapshot_missing", "test_error_history_remaining.ErrorHistoryRemainingTests.test_root_bound_snapshot_missing"),
    ("languagetool_dependency_missing", "test_error_history_remaining.ErrorHistoryRemainingTests.test_languagetool_dependency_missing"),
    ("worker_factory_signature_drift", "test_error_history_remaining.ErrorHistoryRemainingTests.test_worker_factory_signature_drift"),
]


def run_test(test_id: str) -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "-v", test_id],
        cwd=HERE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    return proc.returncode == 0, proc.stdout


def main() -> int:
    results = []
    failed = 0
    missing = 0
    for name, test_id in CATALOG:
        if not test_id:
            missing += 1
            results.append({"error_type": name, "status": "BLOCKED_NO_EXECUTABLE_NEGATIVE_TEST"})
            continue
        ok, output = run_test(test_id)
        if not ok:
            failed += 1
        results.append({
            "error_type": name,
            "status": "PASS" if ok else "FAIL",
            "test_id": test_id,
            "output_tail": output[-1200:],
        })
    status = "SYSTEM4A_ERROR_HISTORY_REGRESSION_PASS" if failed == 0 and missing == 0 else "SYSTEM4A_ERROR_HISTORY_REGRESSION_BLOCKED"
    print(json.dumps({
        "status": status,
        "known_error_types": len(CATALOG),
        "negative_executable": len(CATALOG) - missing,
        "passed": sum(1 for r in results if r["status"] == "PASS"),
        "failed": failed,
        "missing_negative_tests": missing,
        "results": results,
    }, ensure_ascii=False, sort_keys=True))
    return 0 if status.endswith("_PASS") else 4


if __name__ == "__main__":
    raise SystemExit(main())
