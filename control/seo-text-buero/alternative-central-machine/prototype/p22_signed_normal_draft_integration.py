#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from p7_release_boundary import Blocked, build_release, canon, verify_for_import, write_release

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"

PREPARE_PHP=r'''<?php
require __DIR__.'/tests/normal-draft-production/fixture-builder.php';
nd_reset();
$statuses=array('publish','draft','trash','private','pending','future');
$before=count(PPM679_WP::get_all_post_inventory($statuses));
$p=nd_build_plan(1,'p22-signed');
$item=$p['items'][0];
$pack=PPM679_Storage::load_fact_pack($item['source_snapshot_id']);
$g=PPM679_Content_Generator::generate($item,$pack);
$ev=PPM679_Content_Validator::check($g,$item,'p22-prep','p22-state');
$prepared=PPM679_Normal_Draft_Adapter::prepare(
    $g,$item,
    array(
      'technical_status'=>$ev['technical_status'],
      'content_quality_status'=>$ev['content_quality_status'],
      'content_hash'=>$ev['content_hash']
    ),
    nd_runtime($p,'p22-fixed-request'),
    'p22-run',
    PPM679_Diagnostic::stable_hash($p),
    'p22-state'
);
$after=count(PPM679_WP::get_all_post_inventory($statuses));
echo json_encode(array(
  'status'=>!empty($prepared['ok'])?'P22_PREPARED_NO_WRITE':'P22_PREPARE_BLOCKED',
  'before_count'=>$before,
  'after_count'=>$after,
  'prepared'=>$prepared
),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
'''

WRITE_PHP=r'''<?php
require __DIR__.'/tests/normal-draft-production/fixture-builder.php';
nd_reset();
/* Seed the same test-side live category registry, but do not generate/write an article here. */
nd_build_plan(1,'p22-write-seed');
$prepared=json_decode(file_get_contents($argv[1]),true);
$before_publish=count(PPM679_WP::get_all_post_inventory(array('publish')));
$before_draft=count(PPM679_WP::get_all_post_inventory(array('draft')));
$write=PPM679_Normal_Draft_Adapter::create_draft($prepared);
$after_publish=count(PPM679_WP::get_all_post_inventory(array('publish')));
$after_draft=count(PPM679_WP::get_all_post_inventory(array('draft')));
$snapshot=!empty($write['ok'])?PPM679_WP::get_post_snapshot($write['post_id']):array();
$readback=!empty($write['ok'])?PPM679_Normal_Draft_Readback_Validator::validate_batch(array($snapshot),array($prepared['expected']),1):array('ok'=>false);
echo json_encode(array(
  'status'=>!empty($write['ok'])?'P22_SIGNED_PREPARED_DRAFT_WRITTEN':'P22_WRITE_BLOCKED',
  'write'=>$write,
  'before_publish'=>$before_publish,
  'after_publish'=>$after_publish,
  'before_draft'=>$before_draft,
  'after_draft'=>$after_draft,
  'snapshot_status'=>$snapshot['post_status']??null,
  'readback_ok'=>!empty($readback['ok']),
  'readback'=>$readback
),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\\n";
'''

def run_json(cmd, cwd):
    p=subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
    if p.returncode!=0:
        raise RuntimeError("COMMAND_FAILED:"+p.stdout[-3000:])
    lines=[x for x in p.stdout.splitlines() if x.strip()]
    decoder=json.JSONDecoder()
    for line in reversed(lines):
        stripped=line.lstrip()
        try:
            obj,end=decoder.raw_decode(stripped)
        except Exception:
            continue
        if isinstance(obj,dict):
            return obj
    raise RuntimeError("JSON_RESULT_NOT_FOUND:"+p.stdout[-3000:])

def _parse_args(argv:list[str]):
    job_id="P22-JOB"
    expected_item_id=None
    expected_canonical_article_id=None
    i=0
    while i<len(argv):
        arg=argv[i]
        if arg=="--job-id" and i+1<len(argv):
            job_id=argv[i+1]; i+=2; continue
        if arg=="--expected-item-id" and i+1<len(argv):
            expected_item_id=argv[i+1]; i+=2; continue
        if arg=="--expected-canonical-article-id" and i+1<len(argv):
            expected_canonical_article_id=argv[i+1]; i+=2; continue
        raise RuntimeError("P22_ARGUMENT_INVALID")
    if not isinstance(job_id,str) or not job_id:
        raise RuntimeError("P22_JOB_ID_INVALID")
    if expected_item_id is not None and (not isinstance(expected_item_id,str) or not expected_item_id):
        raise RuntimeError("P22_EXPECTED_ITEM_ID_INVALID")
    if expected_canonical_article_id is not None and (not isinstance(expected_canonical_article_id,str) or not expected_canonical_article_id):
        raise RuntimeError("P22_EXPECTED_CANONICAL_ID_INVALID")
    return job_id,expected_item_id,expected_canonical_article_id


def main(argv:list[str]|None=None):
    job_id,expected_item_id,expected_canonical_article_id=_parse_args(list(argv or []))
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        ppm_out=root/"ppm"
        ppm_out.mkdir()
        with zipfile.ZipFile(PPM) as z:z.extractall(ppm_out)
        ppm=ppm_out/"portal-production-machine"

        prepare_php=ppm/"p22-prepare.php"
        write_php=ppm/"p22-write.php"
        prepare_php.write_text(PREPARE_PHP,encoding="utf-8")
        write_php.write_text(WRITE_PHP,encoding="utf-8")

        prep=run_json(["php",str(prepare_php)],ppm)
        if prep["status"]!="P22_PREPARED_NO_WRITE":
            raise RuntimeError("PREPARE_FAILED")
        if prep["before_count"]!=prep["after_count"]:
            raise RuntimeError("PREPARE_PERFORMED_WRITE")
        prepared=prep["prepared"]
        if not prepared.get("ok"):
            raise RuntimeError("PREPARED_NOT_OK")
        prepared_item_id=str(prepared.get("plan_item_key") or "")
        prepared_canonical_article_id=str(prepared.get("canonical_article_id") or "")
        if not prepared_item_id:
            raise RuntimeError("PREPARED_ITEM_ID_MISSING")
        if not prepared_canonical_article_id:
            raise RuntimeError("PREPARED_CANONICAL_ID_MISSING")
        if expected_item_id is not None and prepared_item_id!=expected_item_id:
            print(json.dumps({
                "status":"P22_BOUND_ITEM_ID_BLOCKED",
                "expected_item_id":expected_item_id,
                "prepared_item_id":prepared_item_id,
                "prepare_no_write":prep["before_count"]==prep["after_count"],
                "signing_started":False,
                "write_started":False,
                "publish_allowed":False,
            },ensure_ascii=False,indent=2))
            raise RuntimeError("BOUND_ITEM_ID_MISMATCH")
        bound_item_id=expected_item_id or prepared_item_id

        if expected_canonical_article_id is not None and prepared_canonical_article_id!=expected_canonical_article_id:
            print(json.dumps({
                "status":"P22_BOUND_CANONICAL_ID_BLOCKED",
                "expected_canonical_article_id":expected_canonical_article_id,
                "prepared_canonical_article_id":prepared_canonical_article_id,
                "prepare_no_write":prep["before_count"]==prep["after_count"],
                "signing_started":False,
                "write_started":False,
                "publish_allowed":False,
            },ensure_ascii=False,indent=2))
            raise RuntimeError("BOUND_CANONICAL_ID_MISMATCH")

        bound_canonical_article_id=expected_canonical_article_id or prepared_canonical_article_id

        fp=prepared.get("planned_write_fingerprint")
        payload_fp=(prepared.get("payload") or {}).get("meta",{}).get("_ppm679_planned_write_fingerprint")
        if not isinstance(fp,str) or len(fp)!=64 or fp!=payload_fp:
            raise RuntimeError("PREPARED_FINGERPRINT_INVALID")

        private=root/"private.pem"
        public=root/"public.pem"
        release_path=root/"release.json"
        signature=root/"release.sig"
        subprocess.run(["openssl","genpkey","-algorithm","Ed25519","-out",str(private)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        subprocess.run(["openssl","pkey","-in",str(private),"-pubout","-out",str(public)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        release=build_release(job_id,bound_item_id,prepared)
        write_release(release_path,release)
        subprocess.run(["openssl","pkeyutl","-sign","-inkey",str(private),"-rawin","-in",str(release_path),"-out",str(signature)],
                       check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        verified=verify_for_import(release_path,signature,public)
        if verified["status"]!="IMPORT_VERIFIED_NO_PUBLISH":
            raise RuntimeError("SIGNED_IMPORT_NOT_VERIFIED")
        if verified["job_id"]!=job_id or verified["item_id"]!=bound_item_id:
            raise RuntimeError("SIGNED_ITEM_IDENTITY_DRIFT")

        # The write input is materialized only from the verified signed release, never from an alternate object.
        raw=release_path.read_bytes()
        signed_release=json.loads(raw.decode("utf-8"))
        if str((signed_release.get("payload") or {}).get("canonical_article_id") or "")!=bound_canonical_article_id:
            raise RuntimeError("SIGNED_CANONICAL_IDENTITY_DRIFT")
        if raw!=canon(signed_release):
            raise RuntimeError("SIGNED_RELEASE_NOT_CANONICAL")
        signed_prepared=signed_release["payload"]
        if hashlib.sha256(canon(signed_prepared)).hexdigest()!=signed_release["content_sha256"]:
            raise RuntimeError("SIGNED_PREPARED_HASH_DRIFT")
        prepared_path=root/"signed-prepared.json"
        prepared_path.write_bytes(canon(signed_prepared))

        positive=run_json(["php",str(write_php),str(prepared_path)],ppm)
        if positive["status"]!="P22_SIGNED_PREPARED_DRAFT_WRITTEN":
            raise RuntimeError("SIGNED_PREPARED_WRITE_FAILED")
        if positive["after_publish"]!=positive["before_publish"]:
            raise RuntimeError("PUBLISH_COUNT_CHANGED")
        if positive["after_draft"]!=positive["before_draft"]+1:
            raise RuntimeError("DRAFT_COUNT_NOT_EXACTLY_ONE")
        if positive["snapshot_status"]!="draft":
            raise RuntimeError("WRITTEN_STATUS_NOT_DRAFT")
        if positive.get("readback_ok") is not True:
            raise RuntimeError("SIGNED_PREPARED_READBACK_DRIFT:"+json.dumps(positive.get("readback"),ensure_ascii=False))

        # Tamper after signature: must be blocked before any write helper is invoked.
        tampered=copy.deepcopy(signed_release)
        tampered["payload"]["payload"]["content"]+=" MANIPULIERT"
        release_path.write_bytes(canon(tampered))
        tamper_blocked=False
        try:
            verify_for_import(release_path,signature,public)
        except Blocked:
            tamper_blocked=True
        if not tamper_blocked:
            raise RuntimeError("POST_SIGNATURE_TAMPER_NOT_BLOCKED")

        # Recompute ordinary content hash: external signature must still fail.
        tampered["content_sha256"]=hashlib.sha256(canon(tampered["payload"])).hexdigest()
        release_path.write_bytes(canon(tampered))
        rehash_blocked=False
        try:
            verify_for_import(release_path,signature,public)
        except Blocked:
            rehash_blocked=True
        if not rehash_blocked:
            raise RuntimeError("POST_SIGNATURE_REHASH_TAMPER_NOT_BLOCKED")

        print(json.dumps({
            "status":"P22_SIGNED_NORMAL_DRAFT_BOUNDARY_PASS",
            "job_id":job_id,
            "item_id":bound_item_id,
            "canonical_article_id":bound_canonical_article_id,
            "prepare_no_write":True,
            "prepared_fingerprint_bound":True,
            "external_signature_verified":True,
            "write_source":"VERIFIED_SIGNED_RELEASE_PAYLOAD_ONLY",
            "exact_one_draft_written":True,
            "publish_count_unchanged":True,
            "post_signature_tamper_blocked":True,
            "post_signature_rehash_tamper_blocked":True,
            "planned_write_fingerprint":fp,
            "release_content_sha256":verified["content_sha256"],
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main(sys.argv[1:]))
