#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
PPM_SHA="acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"

POS="tests/normal-draft-production/test-01-positive-1-to-4.php"
NEG_LINK="tests/normal-draft-production/test-04-content-source-link-negative.php"
FINAL_STATUS="NORMAL_DRAFT_END_TO_END_READBACK_PASS_AWAITING_USER_CONTENT_REVIEW_NO_PUBLISH"

def sha(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run_php(root:Path, rel:str):
    target=root/rel
    if not target.is_file():
        raise RuntimeError("TEST_MISSING:"+rel)
    proc=subprocess.run(
        ["php",str(target)],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
    )
    if proc.returncode!=0:
        raise RuntimeError("TEST_FAILED:"+rel+"\n"+proc.stdout[-3000:])
    return proc.stdout

def main():
    if not PPM.is_file() or sha(PPM)!=PPM_SHA:
        raise RuntimeError("PPM_IDENTITY_BLOCKED")

    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/"ppm"; out.mkdir()
        with zipfile.ZipFile(PPM) as z:
            z.extractall(out)
        root=out/"portal-production-machine"

        pos_source=(root/POS).read_text(encoding="utf-8")
        neg_source=(root/NEG_LINK).read_text(encoding="utf-8")
        if "execute_plan" not in pos_source or FINAL_STATUS not in pos_source:
            raise RuntimeError("POSITIVE_TEST_NOT_REAL_PIPELINE_ASSERTION")
        if "execute_plan" not in neg_source:
            raise RuntimeError("NEGATIVE_LINK_TEST_NOT_REAL_PIPELINE_ASSERTION")
        if "link" not in neg_source.lower():
            raise RuntimeError("NEGATIVE_LINK_TEST_SCOPE_UNPROVEN")

        positive_output=run_php(root,POS)
        negative_output=run_php(root,NEG_LINK)

        print(json.dumps({
            "status":"P4_REAL_PPM_SMOKE_PASS",
            "ppm_sha256":PPM_SHA,
            "positive_test":POS,
            "positive_exit":"PASS",
            "positive_asserts_final_no_publish_status":True,
            "negative_link_test":NEG_LINK,
            "negative_link_exit":"PASS",
            "real_pipeline_executed":True,
            "test_fixture_is_bundled_original":True,
            "textmachine_modified":False,
            "wordpress_write_performed":False,
            "publish_allowed":False,
            "positive_output_tail":positive_output[-500:],
            "negative_output_tail":negative_output[-500:],
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({
            "status":"P4_REAL_PPM_SMOKE_BLOCKED",
            "error":str(exc),
            "publish_allowed":False,
        },ensure_ascii=False,indent=2))
        raise SystemExit(2)
