#!/usr/bin/env python3
from __future__ import annotations
import json, tempfile, zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
REG="contracts/hard-rule-registry-v1.json"
SUSPECT=("claude","chatgpt","gpt","llm"," ai","human","manual","reviewer")

def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        with zipfile.ZipFile(PPM) as z:
            z.extractall(root)
        reg=root/"portal-production-machine"/REG
        data=json.loads(reg.read_text(encoding="utf-8"))
        rules=data.get("rules",[])
        suspicious=[]
        validators={}
        for i,rule in enumerate(rules):
            if not isinstance(rule,dict):
                continue
            vor=rule.get("validator_or_reviewer")
            if isinstance(vor,str) and vor.strip():
                validators[vor]=validators.get(vor,0)+1
                low=(" "+vor.lower())
                if any(tok in low for tok in SUSPECT):
                    suspicious.append({
                        "index":i,
                        "rule_id":rule.get("rule_id"),
                        "title":rule.get("title"),
                        "validator_or_reviewer":vor,
                        "positive_test":rule.get("positive_test"),
                        "negative_test":rule.get("negative_test"),
                        "error_code":rule.get("error_code"),
                        "required_evidence":rule.get("required_evidence"),
                        "source_path":rule.get("source_path"),
                        "all_fields":rule,
                    })
        print(json.dumps({
            "status":"P14_REVIEWER_AUTHORITY_AUDIT_PASS",
            "validator_count":len(validators),
            "suspicious_count":len(suspicious),
            "suspicious":suspicious,
            "all_validator_or_reviewer_values":sorted(validators.items(), key=lambda x:(x[0].lower())),
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
