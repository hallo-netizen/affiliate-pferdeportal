#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

REPO=Path(__file__).resolve().parents[4]
FINALIZER=REPO/"control/startmaster0107/ENDSTEMPEL_FINALIZER.py"
NEUTRAL_FINAL_FILENAME="PFERDE_ATELIER_SIGNED_ARTICLE_BATCH_FINAL.json"

def load_module(path:Path,name:str):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None:
        raise RuntimeError("MODULE_LOAD_FAILED")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def dump(path:Path,obj:dict):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def sha(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main()->int:
    e=load_module(FINALIZER,"acm_endstamp_generic")
    # Test-only binding: prove the existing generic finalizer supports a neutral,
    # article-count-independent filename without changing its signing/import logic.
    e.FINAL_FILENAME=NEUTRAL_FINAL_FILENAME

    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        batch="c"*64
        release=root/".pferde-release"/batch
        release.mkdir(parents=True)
        outputs=[]
        for i,text in enumerate(("eins\n","zwei\n","drei\n"),1):
            name="ARTICLE_"+format(i,"064x")+".md"
            p=release/name
            p.write_text(text,encoding="utf-8")
            outputs.append({
                "source_ref":"source/"+name,
                "released_ref":str(p.relative_to(root)),
                "sha256":sha(p),
            })
        receipt={
            "contract":"PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2",
            "status":"OUTPUT_RELEASE_PASS_FINAL_REVIEW_AND_REARM_CONFIRMED",
            "startmaster":"STARTMASTER0107",
            "source_step_id":"RUN_NEW_ARTICLE_BATCH_NO_STOP",
            "source_sequence":107007,
            "source_ticket_id":"t",
            "source_state_sha256":"a"*64,
            "source_bundle_sha256":"b"*64,
            "batch_sha256":batch,
            "worker_receipt_sha256":"d"*64,
            "final_review_step_id":"FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH",
            "final_review_sequence":107008,
            "final_review_ticket_id":"tf",
            "final_review_receipt_sha256":"e"*64,
            "main_head":"f"*40,
            "outputs":outputs,
            "chat_execution_authority":"NONE",
            "chat_output_authority":"NONE",
            "domain_logic_authority":"NONE",
            "quality_authority":"NONE",
            "publish_allowed":False,
        }
        receipt_path=release/"RELEASE_RECEIPT.json"
        dump(receipt_path,receipt)

        private=Ed25519PrivateKey.generate()
        public=private.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        pub_b64=base64.b64encode(public).decode("ascii")
        pub_sha=hashlib.sha256(public).hexdigest()
        kid="test-"+pub_sha[:16]
        trusted={
            "signing_key_id":kid,
            "signing_public_key_sha256":pub_sha,
            "public_key_b64":pub_b64,
        }
        def signer(manifest_sha,*_):
            return {
                "signing_key_id":kid,
                "signing_public_key_sha256":pub_sha,
                "public_key_b64":pub_b64,
                "signature_b64":base64.b64encode(private.sign(manifest_sha.encode("ascii"))).decode("ascii"),
            }

        result=e.finalize(root,str(receipt_path.relative_to(root)),signer,trusted)
        final=root/result["final_ref"]
        if final.name!=NEUTRAL_FINAL_FILENAME:
            raise RuntimeError("NEUTRAL_FINAL_FILENAME_NOT_USED")
        pkg=json.loads(final.read_text(encoding="utf-8"))
        if pkg["article_manifest"]["article_count"]!=3:
            raise RuntimeError("DYNAMIC_ARTICLE_COUNT_NOT_BOUND")
        if result["article_count"]!=3:
            raise RuntimeError("DYNAMIC_RESULT_COUNT_NOT_BOUND")
        if result.get("publish_allowed") is not False:
            raise RuntimeError("PUBLISH_NOT_FALSE")

        print(json.dumps({
            "status":"ACM_NEUTRAL_END_FILE_CONTRACT_PASS",
            "final_filename":NEUTRAL_FINAL_FILENAME,
            "article_count_in_filename":False,
            "tested_article_count":3,
            "manifest_article_count_dynamic":True,
            "existing_generic_endstempel_reused":True,
            "new_signer_created":False,
            "new_import_path_created":False,
            "publish_allowed":False,
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
