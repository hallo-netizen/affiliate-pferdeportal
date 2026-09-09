#!/usr/bin/env python3
from __future__ import annotations

import base64
import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

REPO=Path(__file__).resolve().parents[4]
FINALIZER=REPO/"control/startmaster0107/ENDSTEMPEL_FINALIZER.py"
WP_VERIFY=REPO/"control/startmaster0107/ENDSTEMPEL_WORDPRESS_VERIFY.php"
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

def build_release(root:Path,count:int,batch:str):
    release=root/".pferde-release"/batch
    release.mkdir(parents=True)
    outputs=[]
    originals={}
    for i in range(1,count+1):
        name="ARTICLE_"+format(i,"064x")+".md"
        p=release/name
        raw=("Artikel "+str(i)+"\n").encode("utf-8")
        p.write_bytes(raw)
        originals[name]=raw
        outputs.append({
            "source_ref":"source/"+name,
            "released_ref":str(p.relative_to(root)),
            "sha256":sha(p),
        })
    receipt={
        "contract":"PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2",
        "status":"OUTPUT_RELEASE_PASS_FINAL_REVIEW_AND_REARM_CONFIRMED",
        "startmaster":"STARTMASTER0107",
        "source_step_id":"ACM_BOUND_ARTICLE_RELEASE",
        "source_sequence":107007,
        "source_ticket_id":"t",
        "source_state_sha256":"a"*64,
        "source_bundle_sha256":"b"*64,
        "batch_sha256":batch,
        "worker_receipt_sha256":"d"*64,
        "final_review_step_id":"ACM_BOUND_FINAL_REVIEW",
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
    rp=release/"RELEASE_RECEIPT.json"
    dump(rp,receipt)
    return release,rp,originals

def php_verify(final:Path,trusted:dict,used:bool=False):
    helper=final.parent/"_acm_verify.php"
    verifier=str(WP_VERIFY).replace("\\","\\\\").replace("'","\\'")
    trusted_json=json.dumps(trusted,separators=(",",":")).replace("\\","\\\\").replace("'","\\'")
    helper.write_text(
        "<?php require '"+verifier+"';"
        +"$trusted=json_decode('"+trusted_json+"',true);"
        +"$used="+("true" if used else "false")+";"
        +"try{$r=pferde_endstempel_verify_before_write($argv[1],$trusted,function($b)use($used){return $used;});"
        +"echo json_encode($r,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);exit(0);}"
        +"catch(Throwable $e){echo $e->getMessage();exit(2);}?>",
        encoding="utf-8",
    )
    cp=subprocess.run(["php",str(helper),str(final)],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    helper.unlink(missing_ok=True)
    return cp

def expect_block(cp,label):
    if cp.returncode==0:
        raise RuntimeError("NEGATIVE_NOT_BLOCKED:"+label+":"+cp.stdout[-1000:])
    return label

def main()->int:
    if shutil.which("php") is None:
        raise RuntimeError("PHP_RUNTIME_MISSING")
    e=load_module(FINALIZER,"acm_endstamp_generic")
    # Test-only name override. Signing, manifest, verifier and import safety stay unchanged.
    e.FINAL_FILENAME=NEUTRAL_FINAL_FILENAME

    private=Ed25519PrivateKey.generate()
    public=private.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    pub_b64=base64.b64encode(public).decode("ascii")
    pub_sha=hashlib.sha256(public).hexdigest()
    kid="test-"+pub_sha[:16]
    signer_trust={
        "signing_key_id":kid,
        "signing_public_key_sha256":pub_sha,
        "public_key_b64":pub_b64,
    }
    wp_trust={kid:{"sha256":pub_sha,"public_key_b64":pub_b64}}

    def signer(manifest_sha,*_):
        return {
            "signing_key_id":kid,
            "signing_public_key_sha256":pub_sha,
            "public_key_b64":pub_b64,
            "signature_b64":base64.b64encode(private.sign(manifest_sha.encode("ascii"))).decode("ascii"),
        }

    positive=[]
    negatives=[]
    counts=(1,3,25,1000)

    for count in counts:
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            batch=hashlib.sha256(("acm-endfile-"+str(count)).encode("ascii")).hexdigest()
            release,rp,originals=build_release(root,count,batch)
            result=e.finalize(root,str(rp.relative_to(root)),signer,signer_trust)
            final=root/result["final_ref"]

            if final.name!=NEUTRAL_FINAL_FILENAME:
                raise RuntimeError("NEUTRAL_FINAL_FILENAME_NOT_USED")
            pkg=json.loads(final.read_text(encoding="utf-8"))
            if pkg["article_manifest"]["article_count"]!=count or result["article_count"]!=count:
                raise RuntimeError("DYNAMIC_ARTICLE_COUNT_NOT_BOUND:"+str(count))
            if any((release/name).read_bytes()!=raw for name,raw in originals.items()):
                raise RuntimeError("ARTICLE_BYTES_MUTATED:"+str(count))

            cp=php_verify(final,wp_trust)
            if cp.returncode!=0:
                raise RuntimeError("WP_PREIMPORT_POSITIVE_FAILED:"+str(count)+":"+cp.stdout[-1000:])
            verified=json.loads(cp.stdout)
            if verified.get("status")!="ENDSTEMPEL_WORDPRESS_PREIMPORT_PASS":
                raise RuntimeError("WP_PREIMPORT_STATUS_WRONG:"+str(count))
            if verified.get("article_count")!=count:
                raise RuntimeError("WP_PREIMPORT_COUNT_WRONG:"+str(count))

            positive.append({
                "article_count":count,
                "endstempel_pass":True,
                "wordpress_preimport_pass":True,
                "bytes_unchanged":True,
            })

            # Full negative matrix on 25 items; replay also checked for every size below.
            if count==25:
                first=release/sorted(originals)[0]
                raw=first.read_bytes()
                first.write_bytes(raw+b"X")
                negatives.append(expect_block(php_verify(final,wp_trust),"one_byte_changed"))
                first.write_bytes(raw)

                missing=release/sorted(originals)[1]
                missing_raw=missing.read_bytes()
                missing.unlink()
                negatives.append(expect_block(php_verify(final,wp_trust),"article_missing"))
                missing.write_bytes(missing_raw)

                extra=release/("ARTICLE_"+"f"*64+".md")
                extra.write_text("extra",encoding="utf-8")
                negatives.append(expect_block(php_verify(final,wp_trust),"extra_article"))
                extra.unlink()

                bad=json.loads(final.read_text(encoding="utf-8"))
                bad["article_manifest"]["article_count"]=24
                copy_without=copy.deepcopy(bad)
                copy_without.pop("package_payload_sha256",None)
                bad["package_payload_sha256"]=e.stable_hash(copy_without)
                badpath=release/"BAD_COUNT.json"
                dump(badpath,bad)
                negatives.append(expect_block(php_verify(badpath,wp_trust),"declared_count_wrong"))

                badsig=json.loads(final.read_text(encoding="utf-8"))
                badsig["signature_b64"]=base64.b64encode(b"0"*64).decode("ascii")
                copy_without=copy.deepcopy(badsig)
                copy_without.pop("package_payload_sha256",None)
                badsig["package_payload_sha256"]=e.stable_hash(copy_without)
                sigpath=release/"BAD_SIG.json"
                dump(sigpath,badsig)
                negatives.append(expect_block(php_verify(sigpath,wp_trust),"signature_wrong"))

            negatives.append(expect_block(php_verify(final,wp_trust,used=True),"replay_"+str(count)))

    print(json.dumps({
        "status":"ACM_NEUTRAL_END_FILE_AND_WORDPRESS_BATCH_GENERIC_PASS",
        "final_filename":NEUTRAL_FINAL_FILENAME,
        "article_count_in_filename":False,
        "tested_counts":list(counts),
        "largest_tested_count":max(counts),
        "meaning":"ARBITRARY_FINITE_ARTICLE_COUNT_SUBJECT_ONLY_TO_REAL_RESOURCE_LIMITS",
        "manifest_article_count_dynamic":True,
        "existing_generic_endstempel_reused":True,
        "existing_wordpress_preimport_reused":True,
        "new_signer_created":False,
        "new_import_path_created":False,
        "positive":positive,
        "negative_tests":negatives,
        "publish_allowed":False,
    },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
