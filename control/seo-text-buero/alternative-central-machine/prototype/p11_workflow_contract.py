from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

class Blocked(RuntimeError):
    pass

# 1:1 stage checklist from the current authoritative Fachworkflow source.
# IMPORTANT: this is a mandatory set, not the runtime execution order.
# Runtime order remains owned exclusively by the deterministic central machine.
REQUIRED_STAGES=(
    "research_fact_pack",
    "textmachine_article_type_structure",
    "table_contract",
    "internal_links",
    "languagetool",
    "ppm",
    "pserc",
    "pste",
    "duplicate_cannibalization",
    "seo",
    "design_format",
    "publish_safety",
)

STAGE_RESULT_KEYS={
    "stage",
    "status",
    "execution_performed",
    "content_or_quality_rules_changed",
    "publish_allowed",
}

def _verify_exact_stage_set(actual: list[str]) -> None:
    if len(actual)!=len(REQUIRED_STAGES):
        raise Blocked("STAGE_COUNT_INVALID")
    if len(set(actual))!=len(actual):
        raise Blocked("STAGE_DUPLICATE")
    if set(actual)!=set(REQUIRED_STAGES):
        missing=[x for x in REQUIRED_STAGES if x not in actual]
        unknown=[x for x in actual if x not in REQUIRED_STAGES]
        raise Blocked("STAGE_SET_DRIFT:missing="+",".join(missing)+";unknown="+",".join(unknown))

def verify_authoritative_stage_source(source_path: Path) -> None:
    tree=ast.parse(source_path.read_text(encoding="utf-8"))
    value=None
    for node in tree.body:
        if isinstance(node,ast.Assign):
            for target in node.targets:
                if isinstance(target,ast.Name) and target.id=="STAGES":
                    value=ast.literal_eval(node.value)
    actual=list(value or ())
    try:
        _verify_exact_stage_set(actual)
    except Blocked as exc:
        raise Blocked("AUTHORITATIVE_STAGE_SET_DRIFT:"+str(exc)) from exc

def verify_stage_results(results: Any) -> None:
    if not isinstance(results,list):
        raise Blocked("STAGE_RESULTS_LIST_REQUIRED")

    actual=[]
    for row in results:
        if not isinstance(row,dict) or set(row)!=STAGE_RESULT_KEYS:
            raise Blocked("STAGE_RESULT_SCHEMA_INVALID")
        actual.append(row["stage"])
        if row["status"]!="PASS":
            raise Blocked("STAGE_NONPASS:"+str(row["stage"]))
        if row["execution_performed"] is not True:
            raise Blocked("STAGE_NOT_EXECUTED:"+str(row["stage"]))
        if row["content_or_quality_rules_changed"] is not False:
            raise Blocked("RULE_CHANGE_FORBIDDEN:"+str(row["stage"]))
        if row["publish_allowed"] is not False:
            raise Blocked("PUBLISH_FORBIDDEN:"+str(row["stage"]))

    # Checklist semantics only: every required proof exactly once.
    # The checklist must never become a second workflow controller.
    _verify_exact_stage_set(actual)

def canonical_pass_results() -> list[dict]:
    return [
        {
            "stage":stage,
            "status":"PASS",
            "execution_performed":True,
            "content_or_quality_rules_changed":False,
            "publish_allowed":False,
        }
        for stage in REQUIRED_STAGES
    ]
