"""Harte WordPress-Ausgabegrenze für Concept Agent.

Diese Datei bildet ausschließlich den read-only ermittelten realen WordPress-Importer-Vertrag ab.
Sie signiert nicht selbst und ersetzt weder PSERC noch ENDSTEMPEL.
"""
from __future__ import annotations
import base64, hashlib, json, re
from typing import Any

PACKAGE_CONTRACT="PSERC_APPROVED_PRODUCTION_PACKAGE_V1"
ENDSTAMP_CONTRACT="PFERDE_ATELIER_ENDSTEMPEL_RELEASE_V1"
MANIFEST_CONTRACT="PFERDE_ATELIER_ENDSTEMPEL_ARTICLE_MANIFEST_V1"
WORKFLOW_RELEASE_CONTRACT="WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED"
SIGNATURE_ALGORITHM="ED25519"
TRUSTED_SIGNING_KEY_ID="github-secret-ed25519-d2ebbf13f6c930e9"
TRUSTED_PUBLIC_KEY_SHA256="d2ebbf13f6c930e987d097a494e3d091db5de028775e1ecc27cbf877d1912df4"
ARTICLE_RE=re.compile(r"^ARTICLE_[0-9a-f]{64}\.md$")
SHA_RE=re.compile(r"^[0-9a-f]{64}$")
TOP_LEVEL_KEYS={
    "contract","endstamp_contract","status","batch_sha256",
    "article_manifest","article_manifest_sha256",
    "import_envelope","import_envelope_sha256",
    "signature_algorithm","signing_key_id","signing_public_key_sha256",
    "public_key_b64","signature_b64",
    "publish_allowed","content_mutation_performed","package_payload_sha256",
}
IMPORT_ENVELOPE_KEYS={
    "contract","package_id","package_payload_sha256","source",
    "fact_pack_bundle","fact_pack_bundle_sha256",
    "production_plan","production_plan_sha256",
    "workflow_release","workflow_release_sha256",
}

def canonical(obj: Any)->bytes:
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")

def stable_hash(obj: Any)->str:
    return hashlib.sha256(canonical(obj)).hexdigest()

def validate_wordpress_package(pkg:dict[str,Any],verify_signature:bool=True)->list[str]:
    e=[]
    if set(pkg)!=TOP_LEVEL_KEYS: e.append("WP_TOP_LEVEL_SCHEMA_INVALID")
    if pkg.get("contract")!=PACKAGE_CONTRACT: e.append("WP_PACKAGE_CONTRACT_INVALID")
    if pkg.get("endstamp_contract")!=ENDSTAMP_CONTRACT: e.append("WP_ENDSTEMPEL_CONTRACT_INVALID")
    if pkg.get("status")!="ENDSTEMPEL_PASS": e.append("WP_ENDSTEMPEL_STATUS_INVALID")
    if pkg.get("signature_algorithm")!=SIGNATURE_ALGORITHM: e.append("WP_SIGNATURE_ALGORITHM_INVALID")
    if pkg.get("signing_key_id")!=TRUSTED_SIGNING_KEY_ID: e.append("WP_SIGNING_KEY_ID_INVALID")
    if pkg.get("signing_public_key_sha256")!=TRUSTED_PUBLIC_KEY_SHA256: e.append("WP_SIGNING_PUBLIC_KEY_SHA256_INVALID")
    if pkg.get("publish_allowed") is not False: e.append("WP_PUBLISH_ALLOWED_MUST_BE_FALSE")
    if pkg.get("content_mutation_performed") is not False: e.append("WP_CONTENT_MUTATION_MUST_BE_FALSE")
    batch=str(pkg.get("batch_sha256") or "")
    if not SHA_RE.fullmatch(batch): e.append("WP_BATCH_SHA256_INVALID")

    manifest=pkg.get("article_manifest")
    if not isinstance(manifest,dict):
        e.append("WP_ARTICLE_MANIFEST_MISSING")
        return e
    if manifest.get("contract")!=MANIFEST_CONTRACT: e.append("WP_MANIFEST_CONTRACT_INVALID")
    mhash=stable_hash(manifest)
    if pkg.get("article_manifest_sha256")!=mhash: e.append("WP_MANIFEST_HASH_INVALID")
    if manifest.get("batch_sha256")!=batch: e.append("WP_MANIFEST_BATCH_INVALID")
    if manifest.get("publish_allowed") is not False: e.append("WP_MANIFEST_PUBLISH_INVALID")
    if manifest.get("content_mutation_performed") is not False: e.append("WP_MANIFEST_MUTATION_INVALID")

    articles=manifest.get("articles")
    count=manifest.get("article_count")
    if not isinstance(articles,list) or isinstance(count,bool) or not isinstance(count,int) or count<1 or len(articles)!=count:
        e.append("WP_ARTICLE_COUNT_INVALID")
        articles=[]

    seen=set()
    for row in articles:
        if not isinstance(row,dict):
            e.append("WP_ARTICLE_ROW_INVALID"); continue
        name=str(row.get("name") or ""); slot=str(row.get("plan_slot") or "")
        digest=str(row.get("sha256") or ""); body=row.get("content_utf8"); length=row.get("byte_length")
        if not SHA_RE.fullmatch(slot) or name!=f"ARTICLE_{slot}.md" or not ARTICLE_RE.fullmatch(name):
            e.append("WP_ARTICLE_NAME_SLOT_INVALID:"+slot)
        if name in seen: e.append("WP_ARTICLE_DUPLICATE:"+name)
        seen.add(name)
        if not isinstance(body,str): e.append("WP_ARTICLE_CONTENT_INVALID:"+slot); continue
        raw=body.encode("utf-8")
        if hashlib.sha256(raw).hexdigest()!=digest: e.append("WP_ARTICLE_HASH_INVALID:"+slot)
        if length!=len(raw): e.append("WP_ARTICLE_LENGTH_INVALID:"+slot)

    env=pkg.get("import_envelope")
    if not isinstance(env,dict):
        e.append("WP_IMPORT_ENVELOPE_MISSING")
    else:
        if set(env)!=IMPORT_ENVELOPE_KEYS: e.append("WP_IMPORT_ENVELOPE_SCHEMA_INVALID")
        if env.get("contract")!=PACKAGE_CONTRACT: e.append("WP_IMPORT_ENVELOPE_CONTRACT_INVALID")
        env_hash=stable_hash(env)
        if manifest.get("import_envelope_sha256")!=env_hash or pkg.get("import_envelope_sha256")!=env_hash:
            e.append("WP_IMPORT_ENVELOPE_HASH_INVALID")
        for field,objname in (
            ("fact_pack_bundle_sha256","fact_pack_bundle"),
            ("production_plan_sha256","production_plan"),
            ("workflow_release_sha256","workflow_release"),
        ):
            obj=env.get(objname)
            if not isinstance(obj,dict) or env.get(field)!=stable_hash(obj):
                e.append("WP_IMPORT_COMPONENT_HASH_INVALID:"+field)
        release=env.get("workflow_release")
        if not isinstance(release,dict) or release.get("contract")!=WORKFLOW_RELEASE_CONTRACT or release.get("status")!="PASS":
            e.append("WP_WORKFLOW_RELEASE_INVALID")
        elif release.get("wordpress_write_performed") is not False:
            e.append("WP_PREMATURE_WORDPRESS_WRITE")

    copy=dict(pkg)
    declared=copy.pop("package_payload_sha256",None)
    if declared!=stable_hash(copy): e.append("WP_PACKAGE_PAYLOAD_HASH_INVALID")

    if verify_signature and not e:
        try:
            from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
            pub=base64.b64decode(pkg["public_key_b64"],validate=True)
            sig=base64.b64decode(pkg["signature_b64"],validate=True)
            if len(pub)!=32 or hashlib.sha256(pub).hexdigest()!=TRUSTED_PUBLIC_KEY_SHA256:
                e.append("WP_PUBLIC_KEY_INVALID")
            elif len(sig)!=64:
                e.append("WP_SIGNATURE_ENCODING_INVALID")
            else:
                Ed25519PublicKey.from_public_bytes(pub).verify(sig,mhash.encode("ascii"))
        except Exception:
            e.append("WP_SIGNATURE_INVALID")
    return e

def assert_wordpress_ready(pkg:dict[str,Any])->None:
    errors=validate_wordpress_package(pkg,verify_signature=True)
    if errors:
        raise RuntimeError("WORDPRESS_PACKAGE_BLOCKED:"+",".join(errors))
